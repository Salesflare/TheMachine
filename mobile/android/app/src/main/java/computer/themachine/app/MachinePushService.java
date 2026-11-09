package computer.themachine.app;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.webkit.CookieManager;
import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;
import com.capacitorjs.plugins.pushnotifications.MessagingService;
import com.google.firebase.messaging.RemoteMessage;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Push on Android (mobile/README.md). The push says nothing about the to-do: its kind, a ready or needs-you state, an
 * opaque id and fixed words. For one that leaves showing it to the app (data "fetch"), the app asks the owner's own
 * Machine about that to-do (GET api/notice, with the WebView's own sign-in, or over Tailscale for a Machine of their
 * own) and shows its title and next step ("Pick a time with Sam", "Send to Sam: Tuesday 10:00 works") with its
 * buttons (NotificationActions). Without an answer (offline, signed out, Tailscale off) it shows the fixed words with
 * "Tap to open.", or how many are waiting ("2 to-dos need you"), and asks once more: an answer then takes their
 * place. Still none: it asks again once the phone is online (NoticeRetry), while the fixed one shows. The lock screen gets only the fixed words
 * when the phone hides sensitive content (the public version). A "clear" push takes a to-do's notification away.
 * Replaces Capacitor's own service, which it still runs.
 */
public class MachinePushService extends MessagingService {

    static final String CHANNEL = "todos";
    private static final String PREFS = "machine_push";
    private static final int TIMEOUT = 5000;
    private static final int RETRY = 2000;
    private static final int MAX_BYTES = 4096;

    @Override
    public void onMessageReceived(@NonNull RemoteMessage message) {
        super.onMessageReceived(message); // Capacitor's: the page's own listeners, while it runs
        Map<String, String> data = message.getData();
        if (message.getNotification() != null || !"1".equals(data.get("fetch"))) return; // the phone shows that one itself
        show(getApplicationContext(), data);
    }

    static void show(Context c, Map<String, String> data) {
        String kind = text(data.get("kind")), state = text(data.get("state")), tag = text(data.get("tag"));
        if (!PushText.TAG.matcher(kind).matches() || !PushText.TAG.matcher(tag).matches()) return;
        if ("clear".equals(kind)) { // the to-do no longer waits (done, snoozed, sent, here or on another device)
            NoticeRetry.cancel(c, tag);
            clear(c, tag);
            return;
        }
        if (!NotificationManagerCompat.from(c).areNotificationsEnabled()) return;
        Notice notice = fetchNotice(c, tag, kind);
        if (notice == null) {
            // No answer yet (the phone's network still waking up, the Machine busy): the fixed words now, so the
            // phone says something at once, then once more a moment later, while FCM's time for a push lasts. With
            // the answer the to-do's own notification takes the fixed one's place, quietly: it already buzzed.
            present(c, data, null, false);
            try {
                Thread.sleep(RETRY);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
            notice = fetchNotice(c, tag, kind);
            if (notice == null) { // still nothing (no network yet, Tailscale off): again once the phone is online
                NoticeRetry.schedule(c, data);
                return;
            }
            late(c, data, notice);
            return;
        }
        if (notice.gone) { // handled in the meantime: nothing to show
            clear(c, tag);
            return;
        }
        present(c, data, notice, false);
    }

    /**
     * A late answer for a wakeup shown with the fixed words: the to-do's own notification takes their place, quietly
     * (it already buzzed), or both go when the to-do no longer waits.
     */
    static void late(Context c, Map<String, String> data, Notice notice) {
        String kind = text(data.get("kind")), state = text(data.get("state")), tag = text(data.get("tag"));
        clear(c, tag); // out of the fixed one's count, which goes once it counts nothing
        if (text(data.get("many")).isEmpty()) NotificationManagerCompat.from(c).cancel(PushText.group(kind, state), 0); // one that counts nothing
        if (notice.gone) return;
        present(c, data, notice, true);
    }

    /**
     * Whether a wakeup's fixed notification still shows and still stands for it: not tapped, swiped away or taken away
     * by a "clear", and the app not opened since (seen) for a kind that counts.
     */
    static boolean fixedShows(Context c, Map<String, String> data) {
        String group = PushText.group(text(data.get("kind")), text(data.get("state")));
        boolean shown = false;
        NotificationManager manager = c.getSystemService(NotificationManager.class);
        try {
            for (android.service.notification.StatusBarNotification n : manager == null ? new android.service.notification.StatusBarNotification[0] : manager.getActiveNotifications()) {
                if (group.equals(n.getTag())) shown = true;
            }
        } catch (RuntimeException e) {
            return false;
        }
        Set<String> tags = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getStringSet(group, new HashSet<>());
        return PushText.stillWaiting(shown, data.get("many"), tags, text(data.get("tag")));
    }

    /** The notification for a wakeup: the to-do's own with its notice, else the fixed words for its kind. */
    private static void present(Context c, Map<String, String> data, Notice notice, boolean quiet) {
        String kind = text(data.get("kind")), state = text(data.get("state")), tag = text(data.get("tag"));
        String many = text(data.get("many"));
        String group = PushText.group(kind, state);
        int count = many.isEmpty() || (notice != null && notice.title != null) ? 1 : waiting(c, group, tag);
        String plain = PushText.fallback(data.get("body"), many, count);
        if (plain.isEmpty()) plain = PushText.fallback(data.get("title"), null, 1);
        String line = notice == null ? null : notice.title;
        // With its notice: one notification per to-do, the to-do's title and next step, its buttons, opening it; a
        // newer one for the same to-do (Preparing, then Ready) replaces it. Without: one for the kind, with the
        // count, that a second one replaces ("2 to-dos need you"), opening the kind's own view (the dashboard's pushRoute)
        String id = line != null ? tag : group;
        String opens = line != null || count == 1 ? tag : kind;
        channel(c);
        // Never a title alone: the Machine's line under it, else the plain "Tap to open."
        String under = PushText.body(line != null ? notice.body : null, c.getString(R.string.push_open));
        NotificationCompat.Builder full = base(c, plain)
            .setContentTitle(line != null ? line : plain)
            .setContentText(under)
            .setStyle(new NotificationCompat.BigTextStyle().bigText(under))
            .setContentIntent(open(c, id, opens));
        if (quiet) full.setSilent(true);
        if (line != null) {
            for (String action : notice.actions) {
                String label = notice.labels.get(action);
                if (label == null || label.isEmpty()) continue;
                // Open, Open draft, Answer, Sign in: the to-do in the app, where the owner sees it first
                if (PushText.opens(action)) full.addAction(new NotificationCompat.Action.Builder(0, label, open(c, tag + ":" + action, tag, "draft".equals(action))).build());
                else if (PushText.choice(action) != null) full.addAction(button(c, tag, action, label, line, notice.events.get(action), notice.events.get("failed")));
            }
        }
        post(c, id, full);
    }

    /** After a button: the to-do's title and what happened ("Snoozed it"), without buttons, quietly. */
    static void after(Context c, String tag, String title, String line, boolean stays) {
        if (!PushText.TAG.matcher(tag).matches()) return;
        channel(c);
        NotificationCompat.Builder b = base(c, title)
            .setContentTitle(title)
            .setContentText(line)
            .setOnlyAlertOnce(true)
            .setSilent(true)
            .setContentIntent(open(c, tag, tag));
        if (!stays) b.setTimeoutAfter(4000); // done or snoozed: the line shows, then it goes
        post(c, tag, b);
    }

    /**
     * A to-do's notification goes: done, snoozed or sent, here or elsewhere. One shown without its line (the kind's,
     * "A to-do is ready") goes too once nothing it counted still waits.
     */
    static synchronized void clear(Context c, String tag) {
        NotificationManagerCompat manager = NotificationManagerCompat.from(c);
        manager.cancel(tag, 0);
        SharedPreferences prefs = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        SharedPreferences.Editor edit = prefs.edit();
        for (Map.Entry<String, ?> entry : prefs.getAll().entrySet()) {
            if (!(entry.getValue() instanceof Set)) continue;
            @SuppressWarnings("unchecked")
            Set<String> tags = new HashSet<>((Set<String>) entry.getValue());
            if (!tags.remove(tag)) continue;
            edit.putStringSet(entry.getKey(), tags);
            if (tags.isEmpty()) manager.cancel(entry.getKey(), 0);
        }
        edit.apply();
    }

    private static void post(Context c, String id, NotificationCompat.Builder b) {
        try {
            NotificationManagerCompat.from(c).notify(id, 0, b.build());
        } catch (SecurityException e) {
            // notifications were turned off in the meantime
        }
    }

    /** A button: runs in NotificationActions after unlocking, never opens the app, never sends anything. */
    private static NotificationCompat.Action button(Context c, String tag, String action, String label, String title, String event, String failed) {
        Intent intent = new Intent(c, NotificationActions.class)
            .putExtra("tag", tag)
            .putExtra("action", action)
            .putExtra("title", title)
            .putExtra("event", text(event))
            .putExtra("failed", text(failed));
        PendingIntent pending = PendingIntent.getBroadcast(c, (tag + ":" + action).hashCode(), intent,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        return new NotificationCompat.Action.Builder(0, label, pending)
            .setAuthenticationRequired(true) // Android 12+: the phone unlocks first
            .setShowsUserInterface(false)
            .build();
    }

    /** Opening the app: what was waiting counts as seen (MainActivity). */
    static void seen(Context c) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().clear().apply();
    }

    /** How many of this kind came in since the app was last opened, this one included. */
    private static synchronized int waiting(Context c, String group, String tag) {
        SharedPreferences prefs = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        Set<String> tags = new HashSet<>(prefs.getStringSet(group, new HashSet<>()));
        if (tags.size() < 99) tags.add(tag);
        prefs.edit().putStringSet(group, tags).apply();
        return tags.size();
    }

    /**
     * A notification whose lock-screen version, when the phone hides sensitive content, says only `plain` and "Tap to
     * open.": nothing of the to-do, never a title alone.
     */
    private static NotificationCompat.Builder base(Context c, String plain) {
        NotificationCompat.Builder hidden = icon(c, new NotificationCompat.Builder(c, CHANNEL)).setContentTitle(plain)
            .setContentText(c.getString(R.string.push_open));
        return icon(c, new NotificationCompat.Builder(c, CHANNEL))
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
            .setPublicVersion(hidden.build());
    }

    private static NotificationCompat.Builder icon(Context c, NotificationCompat.Builder b) {
        return b.setSmallIcon(R.drawable.ic_stat_notify).setColor(ContextCompat.getColor(c, R.color.colorPrimary));
    }

    private static void channel(Context c) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return;
        NotificationManager manager = c.getSystemService(NotificationManager.class);
        if (manager != null && manager.getNotificationChannel(CHANNEL) == null) {
            manager.createNotificationChannel(new NotificationChannel(CHANNEL, c.getString(R.string.push_channel), NotificationManager.IMPORTANCE_DEFAULT));
        }
    }

    private static PendingIntent open(Context c, String id, String tag) {
        return open(c, id, tag, false);
    }

    /** card: Open draft, the to-do in the list (#card=), where its draft shows in full; else its chat. */
    private static PendingIntent open(Context c, String id, String tag, boolean card) {
        Intent intent = new Intent(c, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        if (tag != null) intent.putExtra("tag", tag); // MachineShellPlugin.handleIntent opens that to-do
        if (tag != null && card) intent.putExtra("card", true);
        return PendingIntent.getActivity(c, id.hashCode(), intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    /** What the Machine says about a to-do (GET api/notice), or null when it can't be reached or says nothing. */
    static final class Notice {
        String title;
        String body = "";
        boolean gone;
        final List<String> actions = new ArrayList<>();
        final Map<String, String> labels = new HashMap<>();
        final Map<String, String> events = new HashMap<>();
    }

    static Notice fetchNotice(Context c, String tag, String kind) {
        String answer = request(c, PushText.noticeUrl(machine(c), tag, kind), null, null, null);
        if (answer == null) return null;
        try {
            JSONObject json = new JSONObject(answer);
            Notice notice = new Notice();
            notice.gone = json.optBoolean("gone", false);
            notice.title = PushText.line(json.optString("title", json.optString("line", "")));
            notice.body = PushText.body(json.optString("body", ""));
            JSONArray actions = json.optJSONArray("actions");
            for (int i = 0; actions != null && i < actions.length() && i < 4; i++) notice.actions.add(actions.optString(i, ""));
            copy(json.optJSONObject("labels"), notice.labels, 24);
            copy(json.optJSONObject("events"), notice.events, PushText.LIMIT * 2);
            return notice.gone || notice.title != null ? notice : null;
        } catch (Exception e) {
            return null;
        }
    }

    /** The to-do's title as the Machine says it now ("Preparing: ..."), or null. */
    static String title(Context c, String tag) {
        Notice notice = fetchNotice(c, tag, null);
        return notice == null || notice.gone ? null : notice.title;
    }

    private static void copy(JSONObject from, Map<String, String> to, int limit) {
        if (from == null) return;
        for (java.util.Iterator<String> keys = from.keys(); keys.hasNext(); ) {
            String key = keys.next();
            to.put(key, PushText.clip(from.optString(key, ""), limit));
        }
    }

    static String machine(Context c) {
        return MachineShellPlugin.normalMachine(c.getSharedPreferences("machine_shell", Context.MODE_PRIVATE).getString("machine", null));
    }

    /**
     * One request to the saved Machine with the WebView's own sign-in (or over Tailscale for a Machine of the owner's
     * own): its answer, or null for anything but a 200. Never follows a redirect (a signed-out hosted Machine sends one).
     */
    static String request(Context c, String url, String body, String origin, String csrf) {
        if (url == null) return null;
        HttpURLConnection conn = null;
        try {
            conn = (HttpURLConnection) new URL(url).openConnection();
            conn.setInstanceFollowRedirects(false);
            conn.setConnectTimeout(TIMEOUT);
            conn.setReadTimeout(TIMEOUT);
            conn.setUseCaches(false);
            conn.setRequestProperty("Accept", "application/json");
            String cookies = null;
            try {
                cookies = CookieManager.getInstance().getCookie(url);
            } catch (RuntimeException e) {
                // no WebView on this phone right now: a Machine of their own still answers over Tailscale
            }
            if (cookies != null && !cookies.isEmpty()) conn.setRequestProperty("Cookie", cookies);
            if (body != null) {
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setRequestProperty("Origin", origin);
                conn.setRequestProperty("X-CSRF-Token", csrf);
                byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
                conn.setFixedLengthStreamingMode(bytes.length);
                try (OutputStream out = conn.getOutputStream()) {
                    out.write(bytes);
                }
            }
            if (conn.getResponseCode() != 200) return null;
            try (InputStream in = conn.getInputStream()) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                byte[] buf = new byte[1024];
                int n;
                while ((n = in.read(buf)) > 0 && out.size() <= MAX_BYTES) out.write(buf, 0, n);
                if (out.size() > MAX_BYTES) return null;
                return out.toString(StandardCharsets.UTF_8.name());
            }
        } catch (Exception e) {
            return null;
        } finally {
            if (conn != null) conn.disconnect();
        }
    }

    private static String text(String value) {
        return value == null ? "" : value;
    }
}
