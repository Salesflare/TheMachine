package computer.themachine.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import java.util.UUID;
import org.json.JSONObject;

/**
 * A notification's button (MachinePushService.button): Prepare, Snooze or Mark done, as the dashboard's own decision,
 * sent to the saved Machine with the owner's sign-in. The notification then says what happened ("Snoozed it") or that
 * the Machine couldn't be reached. Nothing is ever sent to anyone from here: a draft or a final step opens the app.
 */
public class NotificationActions extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        Context c = context.getApplicationContext();
        String tag = text(intent.getStringExtra("tag")), action = text(intent.getStringExtra("action"));
        String title = text(intent.getStringExtra("title")), event = text(intent.getStringExtra("event"));
        String failed = text(intent.getStringExtra("failed"));
        String body = PushText.decide(tag, action, UUID.randomUUID().toString());
        if (body == null) return;
        PendingResult pending = goAsync();
        new Thread(() -> {
            try {
                boolean ok = decide(c, body);
                if (ok && !"prepare".equals(action)) MachinePushService.clear(c, tag);
                // Prepare: "Preparing: <title>" and "Preparing it" stay until the Ready notification replaces it
                String now = ok && "prepare".equals(action) ? MachinePushService.title(c, tag) : null;
                MachinePushService.after(c, tag, now != null ? now : title, ok ? event : failed, !ok || "prepare".equals(action));
            } finally {
                pending.finish();
            }
        }).start();
    }

    private static boolean decide(Context c, String body) {
        String machine = MachinePushService.machine(c);
        String session = MachinePushService.request(c, PushText.route(machine, "api/session"), null, null, null);
        if (session == null) return false;
        try {
            String csrf = new JSONObject(session).optString("csrf", "");
            if (csrf.isEmpty()) return false;
            return MachinePushService.request(c, PushText.route(machine, "api/action"), body, PushText.origin(machine), csrf) != null;
        } catch (Exception e) {
            return false;
        }
    }

    private static String text(String value) {
        return value == null ? "" : value;
    }
}
