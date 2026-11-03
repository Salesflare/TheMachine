package computer.themachine.app;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

/** The words of a notification the app shows itself (PushText, MachinePushService). */
public class PushTextTest {

    @Test
    public void theMachinesLineShowsAsItIsWhenShort() {
        assertEquals("Ready: Reply to Gianni about the listing", PushText.line("Ready: Reply to Gianni about the listing"));
        assertEquals("Needs your help: Pick a time with Sam", PushText.line(" Needs your help:\nPick a time with Sam "));
    }

    @Test
    public void aLongLineIsCutAtAWordUnderTheLimit() {
        String line = PushText.line("Ready: Reply to the landlord about the listing on Main Street, with the photos and the lease");
        assertTrue(line, line.length() <= PushText.LIMIT);
        assertTrue(line, line.endsWith("…"));
        assertTrue(line, line.startsWith("Ready: Reply to the landlord"));
        assertEquals("xxxxxxxxx…", PushText.clip("xxxxxxxxxxxxxxxxxxxx", 10));
    }

    @Test
    public void noLineMeansTheFixedWords() {
        assertNull(PushText.line(""));
        assertNull(PushText.line("  "));
        assertNull(PushText.line(null));
    }

    @Test
    public void theFixedWordsSayTheKindAndHowMany() {
        assertEquals("A to-do needs you", PushText.fallback("A to-do needs you", "{} to-dos need you", 1));
        assertEquals("2 to-dos need you", PushText.fallback("A to-do needs you", "{} to-dos need you", 2));
        assertEquals("Er wachten 3 to-do's op je", PushText.fallback("Er wacht een to-do op je", "Er wachten {} to-do's op je", 3));
        // A kind that comes one at a time (the morning, a test) keeps its own words
        assertEquals("Your morning", PushText.fallback("Your morning", "", 4));
        assertEquals("", PushText.fallback(null, null, 2));
    }

    @Test
    public void onlyAPlainIdIsAskedFor() {
        assertEquals("https://sam.app.themachine.computer/api/notice?tag=card_1", PushText.noticeUrl("https://sam.app.themachine.computer/", "card_1"));
        assertEquals("https://desk.tail1234.ts.net:8443/assistant/api/notice?tag=abc", PushText.noticeUrl("https://desk.tail1234.ts.net:8443/assistant/", "abc"));
        assertNull(PushText.noticeUrl("https://sam.app.themachine.computer/", "a&b=c"));
        assertNull(PushText.noticeUrl("https://sam.app.themachine.computer/", ""));
        assertNull(PushText.noticeUrl("http://sam.app.themachine.computer/", "card_1"));
        assertNull(PushText.noticeUrl(null, "card_1"));
    }

    @Test
    public void severalOfAKindShareOneNotification() {
        assertEquals("machine-result-needs", PushText.group("result", "needs"));
        assertEquals("machine-todo", PushText.group("todo", ""));
    }
}
