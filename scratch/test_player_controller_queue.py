import os
import sys

sys.path.insert(0, os.path.abspath('KivyMusicApp'))

from models.track_model import TrackModel
from controllers.player_controller import PlayerController

def test_controller_queue():
    t1 = TrackModel(video_id="v1", title="Track 1")
    t2 = TrackModel(video_id="v2", title="Track 2")
    t3 = TrackModel(video_id="v3", title="Track 3")
    
    class MockPlaylist:
        tracks = [t1, t2, t3]
        
    pc = PlayerController()
    pc.set_playlist(MockPlaylist())
    pc.set_track(t1)
    
    # 1. Initial queue
    assert pc.queue == [t1, t2, t3]
    assert pc.queue_index == 0
    
    # 2. Next track
    next_t = pc.get_next_track()
    assert next_t == t2
    pc.set_track(next_t)
    assert pc.queue_index == 1
    
    # 3. Toggle Shuffle: active track (t2) stays at index 0, others shuffled
    pc.toggle_shuffle()
    assert pc.is_shuffle is True
    assert pc.queue[0] == t2
    assert set(pc.queue) == {t1, t2, t3}
    assert pc.queue_index == 0
    
    # 4. Toggle Unshuffle: restores original order, queue_index points to t2 (index 1)
    pc.toggle_shuffle()
    assert pc.is_shuffle is False
    assert pc.queue == [t1, t2, t3]
    assert pc.queue_index == 1
    
    # 5. Repeat mode cycle: off -> all -> one -> off
    assert pc.repeat_mode == "off"
    pc.cycle_repeat_mode()
    assert pc.repeat_mode == "all"
    pc.cycle_repeat_mode()
    assert pc.repeat_mode == "one"
    pc.cycle_repeat_mode()
    assert pc.repeat_mode == "off"
    
    print("PlayerController queue verification test passed!")

if __name__ == "__main__":
    test_controller_queue()
