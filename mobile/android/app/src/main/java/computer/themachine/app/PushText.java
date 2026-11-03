package computer.themachine.app;

import java.util.regex.Pattern;

/**
 * The words of a notification the app shows itself (MachinePushService), kept apart so they are tested on their own
 * (PushTextTest). The to-do's line comes from the owner's Machine (GET api/notice), already short; the fixed words and
 * the "{} to-dos need you" line come with the push, in the owner's language, for when the Machine can't be reached.
 */
final class PushText {

    static final int LIMIT = 60;
    static final int BODY = 120;
    static final Pattern TAG = Pattern.compile("[A-Za-z0-9_-]{1,64}");

    private PushText() {}

    /** One plain line of at most `limit` characters, cut at a word with an ellipsis. "" for nothing. */
    static String clip(String text, int limit) {
        if (text == null) return "";
        String plain = text.replaceAll("[\\x00-\\x1f\\x7f]", " ").trim().replaceAll("\\s+", " ");
        if (plain.length() <= limit) return plain;
        String cut = plain.substring(0, limit - 1);
        int space = cut.lastIndexOf(' ');
        String word = space >= limit / 2 ? cut.substring(0, space) : cut;
        return word.replaceAll("[ ,;:.-]+$", "") + "…";
    }

    /** The fixed line: `one` for a single one, `many` with the count for several (a kind without it: `one`). */
    static String fallback(String one, String many, int count) {
        if (count > 1 && many != null && many.contains("{}")) return clip(many.replace("{}", String.valueOf(count)), LIMIT);
        return clip(one, LIMIT);
    }

    /** The Machine's line for this to-do, or null when it had none (unknown, or Text in notifications is off there). */
    static String line(String fetched) {
        String text = clip(fetched, LIMIT);
        return text.isEmpty() ? null : text;
    }

    /** The next step under the title ("Reply to Sam: confirm Tuesday 10:00"), or "" for none. */
    static String body(String fetched) {
        return clip(fetched, BODY);
    }

    /**
     * The dashboard's own decision for a notification button, or null for one the phone never does from a
     * notification: Prepare starts a to-do not started yet, Snooze is until tomorrow, Mark done closes it. Sending and
     * every final step open the app instead.
     */
    static String choice(String action) {
        if ("prepare".equals(action)) return "accept";
        if ("snooze".equals(action)) return "snooze";
        if ("done".equals(action)) return "complete";
        return null;
    }

    /** The POST api/action body for a button, as the dashboard sends it; null for anything that isn't one. */
    static String decide(String tag, String action, String decisionId) {
        String choice = choice(action);
        if (choice == null || tag == null || !TAG.matcher(tag).matches() || decisionId == null || !decisionId.matches("[A-Za-z0-9-]{8,64}")) return null;
        return "{\"action\":\"decide\",\"args\":{\"suggestion_id\":\"" + tag + "\",\"choice\":\"" + choice + "\",\"feedback\":\"\","
            + ("snooze".equals(choice) ? "\"snooze_option\":\"tomorrow\"," : "") + "\"decision_id\":\"" + decisionId + "\"}}";
    }

    /** The Origin a button's request carries: the saved Machine's own, as its page sends (the Machine checks it). */
    static String origin(String machine) {
        if (machine == null || !machine.startsWith("https://")) return null;
        int slash = machine.indexOf('/', 8);
        String origin = slash < 0 ? machine : machine.substring(0, slash);
        return origin.length() > 8 ? origin : null;
    }

    /** The saved Machine's address for one of its routes (api/session, api/action), or null. */
    static String route(String machine, String path) {
        if (machine == null || !machine.startsWith("https://") || !machine.endsWith("/")) return null;
        return machine + path;
    }

    /** Where several of a kind without their line add up: one notification that says how many. */
    static String group(String kind, String state) {
        return "machine-" + kind + (state == null || state.isEmpty() ? "" : "-" + state);
    }

    /** The saved Machine's address for a wakeup's line, or null for anything that isn't a plain id. */
    static String noticeUrl(String machine, String tag) {
        if (machine == null || !machine.startsWith("https://") || !machine.endsWith("/") || tag == null || !TAG.matcher(tag).matches()) return null;
        return machine + "api/notice?tag=" + tag;
    }
}
