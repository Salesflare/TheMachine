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
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import org.json.JSONObject;

/**
 * Push on Android (mobile/README.md). The push says nothing about the to-do: its kind, a ready or needs-you state, an
 * opaque id and fixed words. For one that leaves showing it to the app (data "fetch"), the app asks the owner's own
 * Machine for that to-do's short line (GET api/notice, with the WebView's own sign-in, or over Tailscale for a Machine
 * of their own) and shows "Ready: Reply about the listing". Without an answer (offline, signed out, Tailscale off) it
 * shows the fixed words, or how many are waiting ("2 to-dos need you"). The lock screen gets only the fixed words when
 * the phone hides sensitive content (the public version). Replaces Capacitor's own service, which it still runs.
 */
public class MachinePushService extends MessagingService {

    static final String CHANNEL = "todos";
    private static final String PREFS = "machine_push";
    private static final int TIMEOUT = 5000;
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
        if (!NotificationManagerCompat.from(c).areNotificationsEnabled()) return;
        String many = text(data.get("many"));
        String group = PushText.group(kind, state);
        int count = many.isEmpty() ? 1 : waiting(c, group, tag);
        String plain = PushText.fallback(data.get("body"), many, count);
        if (plain.isEmpty()) plain = PushText.fallback(data.get("title"), null, 1);
        String line = PushText.line(fetchLine(c, tag));
        // With its line: one notification per to-do, opening it. Without: one for the kind, with the count, that a
        // second one replaces ("2 to-dos need you"), opening the dashboard
        String shown = line != null ? line : plain;
        String id = line != null ? tag : group;
        String opens = line != null || count == 1 ? tag : null;
        channel(c);
        NotificationCompat.Builder hidden = base(c).setContentTitle(plain);
        NotificationCompat.Builder full = base(c)
            .setContentTitle(shown)
            .setContentIntent(open(c, id, opens))
            .setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
            .setPublicVersion(hidden.build());
        try {
            NotificationManagerCompat.from(c).notify(id, 0, full.build());
        } catch (SecurityException e) {
            // notifications were turned off in the meantime
        }
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

    private static NotificationCompat.Builder base(Context c) {
        return new NotificationCompat.Builder(c, CHANNEL)
            .setSmallIcon(R.drawable.ic_stat_notify)
            .setColor(ContextCompat.getColor(c, R.color.colorPrimary))
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT);
    }

    private static void channel(Context c) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return;
        NotificationManager manager = c.getSystemService(NotificationManager.class);
        if (manager != null && manager.getNotificationChannel(CHANNEL) == null) {
            manager.createNotificationChannel(new NotificationChannel(CHANNEL, c.getString(R.string.push_channel), NotificationManager.IMPORTANCE_DEFAULT));
        }
    }

    private static PendingIntent open(Context c, String id, String tag) {
        Intent intent = new Intent(c, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        if (tag != null) intent.putExtra("tag", tag); // MachineShellPlugin.handleIntent opens that to-do
        return PendingIntent.getActivity(c, id.hashCode(), intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    /** The to-do's line from the saved Machine, or null. Never follows a redirect (a signed-out hosted Machine sends one). */
    private static String fetchLine(Context c, String tag) {
        String machine = MachineShellPlugin.normalMachine(c.getSharedPreferences("machine_shell", Context.MODE_PRIVATE).getString("machine", null));
        String url = PushText.noticeUrl(machine, tag);
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
                cookies = CookieManager.getInstance().getCookie(url); // the WebView's own sign-in on this Machine
            } catch (RuntimeException e) {
                // no WebView on this phone right now: a Machine of their own still answers over Tailscale
            }
            if (cookies != null && !cookies.isEmpty()) conn.setRequestProperty("Cookie", cookies);
            if (conn.getResponseCode() != 200) return null;
            try (InputStream in = conn.getInputStream()) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                byte[] buf = new byte[1024];
                int n;
                while ((n = in.read(buf)) > 0 && out.size() <= MAX_BYTES) out.write(buf, 0, n);
                if (out.size() > MAX_BYTES) return null;
                return new JSONObject(out.toString(StandardCharsets.UTF_8.name())).optString("line", "");
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
