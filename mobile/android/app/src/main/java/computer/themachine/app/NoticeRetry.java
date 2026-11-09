package computer.themachine.app;

import android.app.job.JobInfo;
import android.app.job.JobParameters;
import android.app.job.JobScheduler;
import android.app.job.JobService;
import android.content.ComponentName;
import android.content.Context;
import android.os.PersistableBundle;
import java.util.HashMap;
import java.util.Map;

/**
 * A wakeup the app couldn't ask the Machine about (the phone just back online, Tailscale still connecting, the
 * Machine briefly away) shows the fixed words ("A to-do is ready", "Tap to open."). This asks again once the phone has
 * a network, then backs off, for up to PushText.RETRY_HOURS: the answer then takes the fixed one's place quietly, with
 * the to-do's title, next step and buttons. It stops once the fixed one is gone (tapped, swiped away, the app opened)
 * or a "clear" came for the to-do. Nothing is kept but the wakeup's own fixed words and opaque id.
 */
public class NoticeRetry extends JobService {

    private static final String[] KEYS = {"kind", "state", "tag", "title", "body", "many"};
    private static final long BACKOFF = 30_000;

    static void schedule(Context c, Map<String, String> data) {
        String tag = data.get("tag");
        if (tag == null || !PushText.TAG.matcher(tag).matches()) return;
        PersistableBundle extras = new PersistableBundle();
        for (String key : KEYS) extras.putString(key, data.get(key) == null ? "" : data.get(key));
        extras.putLong("since", System.currentTimeMillis());
        JobInfo job = new JobInfo.Builder(id(tag), new ComponentName(c, NoticeRetry.class))
            .setRequiredNetworkType(JobInfo.NETWORK_TYPE_ANY)
            .setBackoffCriteria(BACKOFF, JobInfo.BACKOFF_POLICY_EXPONENTIAL)
            .setExtras(extras)
            .build();
        JobScheduler scheduler = c.getSystemService(JobScheduler.class);
        try {
            if (scheduler != null) scheduler.schedule(job);
        } catch (RuntimeException e) {
            // too many jobs right now: the fixed words stay, as before
        }
    }

    static void cancel(Context c, String tag) {
        if (tag == null || !PushText.TAG.matcher(tag).matches()) return;
        JobScheduler scheduler = c.getSystemService(JobScheduler.class);
        if (scheduler != null) scheduler.cancel(id(tag));
    }

    private static int id(String tag) {
        return ("machine-notice:" + tag).hashCode();
    }

    @Override
    public boolean onStartJob(JobParameters params) {
        PersistableBundle extras = params.getExtras();
        Map<String, String> data = new HashMap<>();
        for (String key : KEYS) data.put(key, extras.getString(key, ""));
        long since = extras.getLong("since", 0);
        Context c = getApplicationContext();
        new Thread(() -> {
            boolean again = false;
            if (!PushText.retryOver(since, System.currentTimeMillis()) && MachinePushService.fixedShows(c, data)) {
                MachinePushService.Notice notice = MachinePushService.fetchNotice(c, data.get("tag"), data.get("kind"));
                if (notice != null) MachinePushService.late(c, data, notice);
                else again = true; // the network came back but the Machine didn't answer yet: later, backing off
            }
            jobFinished(params, again);
        }).start();
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) {
        return true; // the network went again mid-way: once it is back
    }
}
