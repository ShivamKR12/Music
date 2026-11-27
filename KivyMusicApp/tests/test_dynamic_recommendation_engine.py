import os
import sys

# Ensure headless mode and correct paths
os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from services.recommendation_engine import DynamicRecommendationEngine
from services.recommendation_scoring import (
    ListenerFeatures,
    TrackFeatures,
    compute_engagement_quality,
    compute_recency_novelty,
    compute_recent_recall,
    compute_skip_penalty,
    compute_trending_velocity,
    rank_and_deduplicate_tracks,
    score_track,
)
from models.database import (
    init_db,
    get_connection,
    add_track,
    mark_track_played,
    record_track_skip,
    get_listening_event_stats,
    record_trend_observations,
    get_trending_velocity_map,
    toggle_favorite,
)
from models.track_model import TrackModel

def test_recommendation_engine():
    print("=== TEST SUITE: Dynamic Multi-Provider Recommendation Engine ===")
    init_db()

    # 1. Singleton instantiation
    engine1 = DynamicRecommendationEngine()
    engine2 = DynamicRecommendationEngine()
    assert engine1 is engine2, "DynamicRecommendationEngine should be a singleton"
    print("✓ Test 1: Singleton instantiation verified")

    # 2. Time context
    time_ctx = DynamicRecommendationEngine.get_time_context()
    assert "period" in time_ctx and "kicker" in time_ctx and "title" in time_ctx
    assert len(time_ctx["query"]) > 5
    print(f"✓ Test 2: Time context verified ({time_ctx['period']}: '{time_ctx['title']}')")

    # 3. Location context
    loc_ctx = DynamicRecommendationEngine.get_location_context()
    assert "region" in loc_ctx and "kicker" in loc_ctx and "title" in loc_ctx
    assert "query" in loc_ctx
    print(f"✓ Test 3: Location context verified (Region: {loc_ctx['region']})")

    # 4. Mood arbitration across all supported mood chips
    moods = ["Relax", "Sleep", "Energize", "Sad", "Romance", "Feel Good", "Workout", "Party", "Commute", "Focus", "All"]
    for m in moods:
        m_ctx = DynamicRecommendationEngine.get_mood_context(m)
        assert "kicker" in m_ctx and "title" in m_ctx and "query" in m_ctx
    print(f"✓ Test 4: All {len(moods)} mood contexts mapped correctly")

    # 5. Populate test tracks and user listening events in DB
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracks WHERE video_id LIKE 'test_rec_%'")
        conn.commit()

    add_track(
        video_id="test_rec_1",
        title="Test Song Alpha",
        artist="Favorite Artist One",
        url="https://youtube.com/watch?v=test_rec_1",
        duration=210,
        media_type="song"
    )
    add_track(
        video_id="test_rec_2",
        title="Test Song Beta",
        artist="Favorite Artist One",
        url="https://youtube.com/watch?v=test_rec_2",
        duration=195,
        media_type="song"
    )
    add_track(
        video_id="test_rec_3",
        title="Local Imported Track",
        artist="Regional Singer",
        url="file:///storage/emulated/0/Music/local.mp3",
        duration=180,
        media_type="song"
    )
    toggle_favorite("test_rec_1")

    # Record playback events to create listener history
    for _ in range(5):
        mark_track_played("test_rec_1")
    for _ in range(3):
        mark_track_played("test_rec_2")

    # 6. Listener profile aggregation
    profile = engine1.get_listener_profile()
    assert "top_artists" in profile
    assert "recent" in profile
    assert "heavy_rotation" in profile
    assert profile["has_history"] is True
    print(f"✓ Test 5: Listener profile aggregated successfully (Top artist: {profile.get('primary_artist')})")

    # 7. Synthesizing dynamic shelves (offline/headless mode)
    shelves = engine1.build_dynamic_shelves(mood="All", limit=10, offline_only=True)
    assert "quick_picks" in shelves
    assert "listen_again" in shelves
    assert "trending" in shelves
    assert "featured" in shelves
    assert "forgotten" in shelves
    assert "daily_mix" in shelves

    for shelf_key, shelf_data in shelves.items():
        assert "kicker" in shelf_data and len(shelf_data["kicker"]) > 0
        assert "title" in shelf_data and len(shelf_data["title"]) > 0
        assert "tracks" in shelf_data and len(shelf_data["tracks"]) > 0, f"Shelf {shelf_key} must have tracks"
    print("✓ Test 6: All 6 dynamic shelves synthesized with authentic non-empty tracks and kickers")

    # 8. Dynamic mood curation
    workout_shelves = engine1.build_dynamic_shelves(mood="Workout", limit=10, offline_only=True)
    qp = workout_shelves["quick_picks"]
    assert "WORKOUT" in qp["kicker"] or "Workout" in qp["title"]
    print("✓ Test 7: Active mood curation updates shelf titles and kickers dynamically")

    # 9. Dynamic category playlists
    charts = engine1.get_dynamic_playlist("Top Charts", limit=10)
    assert len(charts) > 0, "Top Charts dynamic playlist should return tracks"
    print(f"✓ Test 8: Dynamic playlist routing returned {len(charts)} tracks")

    # 10. Verify ListenerFeatures & explicit contracts on get_listener_profile()
    assert isinstance(profile.get("listener_features"), ListenerFeatures)
    assert isinstance(profile.get("events_stats_map"), dict)
    assert isinstance(profile.get("velocity_map"), dict)
    print("✓ Test 9: ListenerFeatures & telemetry data contracts verified on get_listener_profile()")

    # 11. Unit Mathematical Boundary Tests: Recency Novelty H(dt) = 1 - exp(-dt / tau)
    assert compute_recency_novelty(0.0) == 0.0, "Novelty at dt=0 MUST be 0.0 (not 1.0)"
    assert compute_recency_novelty(None) == 1.0, "Novelty for unplayed track MUST be 1.0"
    dt_samples = [0.0, 60.0, 1800.0, 3600.0, 21600.0, 86400.0, 604800.0]
    novelties = [compute_recency_novelty(dt) for dt in dt_samples]
    for i in range(len(novelties) - 1):
        assert novelties[i + 1] > novelties[i], f"Novelty must strictly increase: {novelties}"
    recalls = [compute_recent_recall(dt) for dt in dt_samples]
    assert recalls[0] == 1.0
    for i in range(len(recalls) - 1):
        assert recalls[i + 1] < recalls[i], f"Recent recall must strictly decrease: {recalls}"
    print(f"✓ Test 10: Novelty boundary curve strictly monotone ({novelties[0]:.3f} -> {novelties[-1]:.3f})")

    # 12. Unit Boundary Tests: Skip Penalty & Engagement Directionality
    assert compute_skip_penalty(5, 0) == 0.0
    p_low = compute_skip_penalty(5, 1)
    p_high = compute_skip_penalty(5, 8)
    assert p_high > p_low > 0.0
    eng_clean = compute_engagement_quality(5, 0, 900.0, 200.0, is_favorite=True)
    eng_skipped = compute_engagement_quality(5, 8, 90.0, 200.0, is_favorite=False)
    assert eng_clean > eng_skipped
    print("✓ Test 11: Skip penalty & engagement quality monotonic bounds verified")

    # 13. Unit Boundary Tests: Multi-Timestamp Trending Velocity (single snapshot = 0.0)
    assert compute_trending_velocity([(1700000000.0, 50_000_000.0)]) == 0.0, "Single snapshot MUST NOT fake trending"
    assert compute_trending_velocity([(1700000000.0, 100.0), (1700000030.0, 9999.0)]) == 0.0, "<60s window MUST be 0.0"
    assert compute_trending_velocity([(1700000000.0, 5000.0), (1700003600.0, 4000.0)]) == 0.0, "Falling views MUST be 0.0"
    vel_slow = compute_trending_velocity([(1700000000.0, 1000.0), (1700003600.0, 1200.0)])
    vel_fast = compute_trending_velocity([(1700000000.0, 1000.0), (1700003600.0, 4000.0)])
    assert 0.0 < vel_slow < vel_fast <= 1.0
    print(f"✓ Test 12: Multi-timestamp trending velocity invariant verified (slow={vel_slow:.3f}, fast={vel_fast:.3f})")

    # 14. Score Directionality & Honest Acoustic Field Contract
    sample_feats = TrackFeatures(video_id="x1", title="Song", artist="Artist")
    assert sample_feats.energy is None and sample_feats.valence is None and sample_feats.bpm is None
    listener_demo = ListenerFeatures(artist_affinities={"artist a": 0.9})
    just_played = TrackFeatures(video_id="a1", title="New Play", artist="Artist A", play_count=3, seconds_since_last_play=5.0)
    stale_forgotten = TrackFeatures(video_id="a2", title="Old Gem", artist="Artist A", play_count=3, seconds_since_last_play=7 * 86400.0)
    assert score_track(stale_forgotten, listener_demo, mode="discovery").total_score > score_track(
        just_played, listener_demo, mode="discovery"
    ).total_score

    # Canonical cross-provider deduplication test
    deduped = rank_and_deduplicate_tracks(
        [
            {"video_id": "sp_dup1", "title": "Midnight Rain (Official Audio)", "artist": "Synth Artist", "source": "spotify"},
            {"video_id": "yt_dup1", "title": "Midnight Rain", "artist": "Synth Artist", "source": "youtube"},
            {"video_id": "js_uniq", "title": "Sunrise Echoes", "artist": "Synth Artist", "source": "jiosaavn"},
        ],
        listener=listener_demo,
        mode="discovery",
        limit=10,
    )
    assert len(deduped) == 2, f"Expected canonical deduplication to collapse duplicate song across providers, got {len(deduped)}"

    # SQLite round-trip for listening_events (skip tracking) & trend_observations
    record_track_skip("test_rec_2", listened_seconds=8.0, track_duration=195.0)
    ev_stats = get_listening_event_stats()
    assert ev_stats.get("test_rec_2", {}).get("skip_count", 0) >= 1

    now_ep = 1790000000.0
    record_trend_observations([{"video_id": "test_rec_static", "view_count": 10_000_000, "source": "youtube"}], observed_at=now_ep)
    record_trend_observations([{"video_id": "test_rec_rising", "view_count": 1000, "source": "youtube"}], observed_at=now_ep - 3600.0)
    record_trend_observations([{"video_id": "test_rec_rising", "view_count": 4500, "source": "youtube"}], observed_at=now_ep)
    vel_map = get_trending_velocity_map()
    assert vel_map.get("test_rec_static", 0.0) == 0.0
    assert vel_map.get("test_rec_rising", 0.0) > 0.5
    print("✓ Test 13: Score directionality, canonical dedup, skip events & multi-timestamp SQLite velocity verified")

    # Clean up test tracks and telemetry rows
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listening_events WHERE video_id LIKE 'test_rec_%'")
        cursor.execute("DELETE FROM trend_observations WHERE video_id LIKE 'test_rec_%'")
        cursor.execute("DELETE FROM tracks WHERE video_id LIKE 'test_rec_%'")
        conn.commit()

    print("\nALL DYNAMIC RECOMMENDATION ENGINE TESTS PASSED (13/13)!")

if __name__ == "__main__":
    test_recommendation_engine()
