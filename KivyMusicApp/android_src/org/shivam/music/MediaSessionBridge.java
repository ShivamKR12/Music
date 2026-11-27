package org.shivam.music;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Icon;
import android.media.MediaMetadata;
import android.media.session.MediaSession;
import android.media.session.PlaybackState;
import android.os.Build;
import android.os.Bundle;
import java.io.File;

/**
 * Native Java bridge for Android MediaSession.Callback and Notification.MediaStyle.
 * Compiles cleanly against Android Platform SDK API 21+ with zero external dependencies,
 * enabling lock-screen Now Bar / Quick Settings rich artwork, interactive seekbar,
 * custom Favorite/Shuffle actions, and reliable background transport callbacks.
 */
public final class MediaSessionBridge {

    public static final String ACTION_PLAY = "org.shivam.music.ACTION_PLAY";
    public static final String ACTION_PAUSE = "org.shivam.music.ACTION_PAUSE";
    public static final String ACTION_PLAY_PAUSE = "org.shivam.music.ACTION_PLAY_PAUSE";
    public static final String ACTION_NEXT = "org.shivam.music.ACTION_NEXT";
    public static final String ACTION_PREV = "org.shivam.music.ACTION_PREV";
    public static final String ACTION_STOP = "org.shivam.music.ACTION_STOP";
    public static final String ACTION_SEEK = "org.shivam.music.ACTION_SEEK";
    public static final String ACTION_FAVORITE = "org.shivam.music.ACTION_FAVORITE";
    public static final String ACTION_SHUFFLE = "org.shivam.music.ACTION_SHUFFLE";

    private static String sLastArtSig = "";
    private static Bitmap sLastArtBitmap = null;
    private static String sLastMetaSignature = "";

    private MediaSessionBridge() {}

    private static void sendTransportBroadcast(Context ctx, String action, long seekMs) {
        if (ctx == null || action == null) {
            return;
        }
        try {
            Context appCtx = ctx.getApplicationContext() != null ? ctx.getApplicationContext() : ctx;
            Intent intent = new Intent(action);
            intent.setPackage(appCtx.getPackageName());
            if (seekMs >= 0L) {
                intent.putExtra("seek_ms", seekMs);
            }
            appCtx.sendBroadcast(intent);
        } catch (Throwable ignored) {
        }
    }

    public static MediaSession.Callback createCallback(final Context context) {
        final Context appCtx = (context != null && context.getApplicationContext() != null)
                ? context.getApplicationContext()
                : context;
        return new MediaSession.Callback() {
            @Override
            public void onPlay() {
                sendTransportBroadcast(appCtx, ACTION_PLAY, -1L);
            }

            @Override
            public void onPause() {
                sendTransportBroadcast(appCtx, ACTION_PAUSE, -1L);
            }

            @Override
            public void onSkipToNext() {
                sendTransportBroadcast(appCtx, ACTION_NEXT, -1L);
            }

            @Override
            public void onSkipToPrevious() {
                sendTransportBroadcast(appCtx, ACTION_PREV, -1L);
            }

            @Override
            public void onStop() {
                sendTransportBroadcast(appCtx, ACTION_STOP, -1L);
            }

            @Override
            public void onSeekTo(long pos) {
                sendTransportBroadcast(appCtx, ACTION_SEEK, Math.max(0L, pos));
            }

            @Override
            public void onCustomAction(String action, Bundle extras) {
                sendTransportBroadcast(appCtx, action, -1L);
            }
        };
    }

    private static int resolveDrawable(Context ctx, String name, int fallbackRes) {
        if (ctx != null && name != null) {
            try {
                int id = ctx.getResources().getIdentifier(name, "drawable", ctx.getPackageName());
                if (id != 0) {
                    return id;
                }
            } catch (Throwable ignored) {
            }
        }
        return fallbackRes;
    }

    public static synchronized Bitmap loadScaledArtwork(String path, int maxDim) {
        String clean = (path != null) ? path.trim() : "";
        if (clean.isEmpty()) {
            return null;
        }
        try {
            File f = new File(clean);
            if (!f.exists() || !f.isFile() || f.length() <= 0L) {
                return null;
            }
            String artSig = clean + ":" + f.length() + ":" + f.lastModified();
            if (artSig.equals(sLastArtSig) && sLastArtBitmap != null && !sLastArtBitmap.isRecycled()) {
                return sLastArtBitmap;
            }
            BitmapFactory.Options bounds = new BitmapFactory.Options();
            bounds.inJustDecodeBounds = true;
            BitmapFactory.decodeFile(clean, bounds);
            if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
                return null;
            }

            int sample = 1;
            int halfW = bounds.outWidth / 2;
            int halfH = bounds.outHeight / 2;
            while ((halfW / sample) >= maxDim && (halfH / sample) >= maxDim) {
                sample *= 2;
            }

            BitmapFactory.Options opts = new BitmapFactory.Options();
            opts.inSampleSize = Math.max(1, sample);
            opts.inPreferredConfig = Bitmap.Config.ARGB_8888;
            Bitmap decoded = BitmapFactory.decodeFile(clean, opts);
            if (decoded == null) {
                return null;
            }
            if (decoded.getWidth() > maxDim || decoded.getHeight() > maxDim) {
                float scale = Math.min(
                        (float) maxDim / (float) decoded.getWidth(),
                        (float) maxDim / (float) decoded.getHeight()
                );
                int w = Math.max(1, Math.round(decoded.getWidth() * scale));
                int h = Math.max(1, Math.round(decoded.getHeight() * scale));
                Bitmap scaled = Bitmap.createScaledBitmap(decoded, w, h, true);
                if (scaled != decoded) {
                    decoded.recycle();
                    decoded = scaled;
                }
            }
            sLastArtSig = artSig;
            sLastArtBitmap = decoded;
            return decoded;
        } catch (Throwable ignored) {
            return null;
        }
    }

    public static void updateSession(
            MediaSession session,
            Context context,
            String title,
            String artist,
            String album,
            long durationMs,
            long positionMs,
            boolean isPlaying,
            boolean isFavorite,
            boolean isShuffle,
            String artPath
    ) {
        if (session == null || context == null) {
            return;
        }
        String safeTitle = (title != null && !title.isEmpty()) ? title : "Kivy Music";
        String safeArtist = (artist != null) ? artist : "";
        String safeAlbum = (album != null) ? album : "";
        long safeDur = Math.max(0L, durationMs);
        long safePos = Math.max(0L, positionMs);
        String safeArt = (artPath != null) ? artPath : "";

        Bitmap artBmp = loadScaledArtwork(safeArt, 512);
        String sig = safeTitle + "|" + safeArtist + "|" + safeAlbum + "|" + safeDur + "|" + safeArt + "|" + (artBmp != null ? 1 : 0);
        if (!sig.equals(sLastMetaSignature)) {
            MediaMetadata.Builder mb = new MediaMetadata.Builder()
                    .putString(MediaMetadata.METADATA_KEY_TITLE, safeTitle)
                    .putString(MediaMetadata.METADATA_KEY_ARTIST, safeArtist)
                    .putLong(MediaMetadata.METADATA_KEY_DURATION, safeDur);
            if (!safeAlbum.isEmpty()) {
                mb.putString(MediaMetadata.METADATA_KEY_ALBUM, safeAlbum);
            }
            if (artBmp != null) {
                mb.putBitmap(MediaMetadata.METADATA_KEY_ALBUM_ART, artBmp);
                mb.putBitmap(MediaMetadata.METADATA_KEY_DISPLAY_ICON, artBmp);
            }
            session.setMetadata(mb.build());
            sLastMetaSignature = sig;
        }

        long actions = PlaybackState.ACTION_PLAY
                | PlaybackState.ACTION_PAUSE
                | PlaybackState.ACTION_PLAY_PAUSE
                | PlaybackState.ACTION_SKIP_TO_NEXT
                | PlaybackState.ACTION_SKIP_TO_PREVIOUS
                | PlaybackState.ACTION_SEEK_TO
                | PlaybackState.ACTION_STOP;

        PlaybackState.Builder pb = new PlaybackState.Builder()
                .setActions(actions)
                .setState(
                        isPlaying ? PlaybackState.STATE_PLAYING : PlaybackState.STATE_PAUSED,
                        safePos,
                        isPlaying ? 1.0f : 0.0f
                );

        int favIcon = resolveDrawable(
                context,
                isFavorite ? "ic_favorite_filled" : "ic_favorite_border",
                android.R.drawable.btn_star_big_on
        );
        int shufIcon = resolveDrawable(
                context,
                "ic_shuffle",
                android.R.drawable.ic_menu_sort_by_size
        );
        pb.addCustomAction(new PlaybackState.CustomAction.Builder(
                ACTION_FAVORITE,
                isFavorite ? "Remove Favorite" : "Favorite",
                favIcon
        ).build());
        pb.addCustomAction(new PlaybackState.CustomAction.Builder(
                ACTION_SHUFFLE,
                isShuffle ? "Shuffle On" : "Shuffle Off",
                shufIcon
        ).build());

        session.setPlaybackState(pb.build());
    }

    private static Notification.Action makeAction(Context ctx, String actionName, String label, int iconRes, int reqCode) {
        Intent it = new Intent(actionName);
        it.setPackage(ctx.getPackageName());
        int piFlags = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0);
        PendingIntent pi = PendingIntent.getBroadcast(ctx, reqCode, it, piFlags);
        if (Build.VERSION.SDK_INT >= 23) {
            return new Notification.Action.Builder(Icon.createWithResource(ctx, iconRes), label, pi).build();
        }
        return new Notification.Action.Builder(iconRes, label, pi).build();
    }

    public static Notification buildMediaNotification(
            Service service,
            String channelId,
            String title,
            String artist,
            String album,
            boolean isPlaying,
            boolean isFavorite,
            boolean isShuffle,
            String artPath,
            MediaSession.Token token
    ) {
        NotificationManager nm = (NotificationManager) service.getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26 && nm != null) {
            NotificationChannel chan = new NotificationChannel(
                    channelId,
                    "Music Playback",
                    NotificationManager.IMPORTANCE_LOW
            );
            chan.setDescription("Active audio playback & lock screen media controls");
            chan.setShowBadge(false);
            chan.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC);
            nm.createNotificationChannel(chan);
        }

        Notification.Builder builder = (Build.VERSION.SDK_INT >= 26)
                ? new Notification.Builder(service, channelId)
                : new Notification.Builder(service);

        String safeTitle = (title != null && !title.isEmpty()) ? title : "Kivy Music";
        String safeArtist = (artist != null && !artist.isEmpty()) ? artist : "Playing Audio";

        builder.setContentTitle(safeTitle)
                .setContentText(safeArtist)
                .setOngoing(isPlaying)
                .setOnlyAlertOnce(true)
                .setShowWhen(false)
                .setVisibility(Notification.VISIBILITY_PUBLIC);

        if (album != null && !album.isEmpty()) {
            builder.setSubText(album);
        }

        int smallIcon = resolveDrawable(service, "ic_music_note", service.getApplicationInfo().icon);
        if (smallIcon != 0) {
            builder.setSmallIcon(smallIcon);
        }

        Bitmap artBmp = loadScaledArtwork(artPath, 512);
        if (artBmp != null) {
            builder.setLargeIcon(artBmp);
        }

        try {
            Intent launch = service.getPackageManager().getLaunchIntentForPackage(service.getPackageName());
            if (launch != null) {
                launch.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
                int piFlags = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0);
                PendingIntent contentPi = PendingIntent.getActivity(service, 0, launch, piFlags);
                builder.setContentIntent(contentPi);
            }
        } catch (Throwable ignored) {
        }

        int prevIcon = resolveDrawable(service, "ic_media_prev", android.R.drawable.ic_media_previous);
        int playPauseIcon = resolveDrawable(
                service,
                isPlaying ? "ic_media_pause" : "ic_media_play",
                isPlaying ? android.R.drawable.ic_media_pause : android.R.drawable.ic_media_play
        );
        int nextIcon = resolveDrawable(service, "ic_media_next", android.R.drawable.ic_media_next);

        builder.addAction(makeAction(service, ACTION_PREV, "Previous", prevIcon, 101));
        builder.addAction(makeAction(service, ACTION_PLAY_PAUSE, isPlaying ? "Pause" : "Play", playPauseIcon, 102));
        builder.addAction(makeAction(service, ACTION_NEXT, "Next", nextIcon, 103));

        Notification.MediaStyle style = new Notification.MediaStyle();
        if (token != null) {
            style.setMediaSession(token);
        }
        style.setShowActionsInCompactView(0, 1, 2);
        builder.setStyle(style);

        return builder.build();
    }
}
