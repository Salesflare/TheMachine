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

    @Test
    public void theNextStepIsOneLineUnderTheTitle() {
        assertEquals("Reply to Sam: confirm Tuesday 10:00", PushText.body("Reply to Sam:\nconfirm Tuesday 10:00"));
        String body = PushText.body("Pay the invoice " + "for the office rent of the last three months ".repeat(5));
        assertTrue(body, body.length() <= PushText.BODY);
        assertEquals("", PushText.body(null));
    }

    @Test
    public void aNotificationIsNeverATitleAlone() {
        // "Your Fleet" and "A to-do is waiting for you" showed with nothing under them: the Machine's line, else the plain words
        assertEquals("Pat accepted your handoff.", PushText.body("Pat accepted your handoff.", "Tap to open."));
        assertEquals("Tap to open.", PushText.body("", "Tap to open."));
        assertEquals("Tap to open.", PushText.body(null, "Tap to open."));
        assertEquals("Tap to open.", PushText.body(" \n ", "Tap to open."));
    }

    @Test
    public void onlyPrepareSnoozeAndDoneAreButtonsAndNothingSends() {
        assertEquals("accept", PushText.choice("prepare"));
        assertEquals("snooze", PushText.choice("snooze"));
        assertEquals("complete", PushText.choice("done"));
        assertNull(PushText.choice("send"));
        assertNull(PushText.choice("accept"));
        assertNull(PushText.choice("open"));
        assertNull(PushText.choice(null));
    }

    @Test
    public void aButtonSendsTheDashboardsOwnDecision() {
        String id = "0b7c8d2e-1f3a-4b5c-9d6e-7f8a9b0c1d2e";
        assertEquals("{\"action\":\"decide\",\"args\":{\"suggestion_id\":\"card_1\",\"choice\":\"complete\",\"feedback\":\"\",\"decision_id\":\"" + id + "\"}}",
            PushText.decide("card_1", "done", id));
        assertTrue(PushText.decide("card_1", "snooze", id).contains("\"choice\":\"snooze\",\"feedback\":\"\",\"snooze_option\":\"tomorrow\""));
        assertTrue(PushText.decide("card_1", "prepare", id).contains("\"choice\":\"accept\""));
        assertNull(PushText.decide("card_1\",\"choice\":\"accept", "done", id));
        assertNull(PushText.decide("card_1", "send", id));
        assertNull(PushText.decide("card_1", "done", "x\""));
    }

    @Test
    public void theRequestGoesToTheSavedMachineWithItsOrigin() {
        assertEquals("https://sam.app.themachine.computer", PushText.origin("https://sam.app.themachine.computer/"));
        assertEquals("https://desk.tail1234.ts.net:8443", PushText.origin("https://desk.tail1234.ts.net:8443/assistant/"));
        assertNull(PushText.origin("http://desk/"));
        assertNull(PushText.origin(null));
        assertEquals("https://desk.tail1234.ts.net:8443/assistant/api/action", PushText.route("https://desk.tail1234.ts.net:8443/assistant/", "api/action"));
        assertNull(PushText.route("https://desk.tail1234.ts.net:8443/assistant", "api/action"));
    }
}
