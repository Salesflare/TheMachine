package computer.themachine.app;

import java.util.regex.Pattern;

/**
 * The words of a notification the app shows itself (MachinePushService), kept apart so they are tested on their own
 * (PushTextTest). The to-do's line comes from the owner's Machine (GET api/notice), already short; the fixed words and
 * the "{} to-dos need you" line come with the push, in the owner's language, for when the Machine can't be reached.
 */
final class PushText {

    static final int LIMIT = 60;
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
