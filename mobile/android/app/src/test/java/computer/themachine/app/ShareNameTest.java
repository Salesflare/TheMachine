package computer.themachine.app;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/** The name a shared or opened file goes to the Machine with (ShareName). All names are made up. */
public class ShareNameTest {

    @Test
    public void aNameWithItsExtensionStaysAsItIs() {
        assertEquals("Invoice 4471.pdf", ShareName.of("Invoice 4471.pdf", "application/pdf"));
        assertEquals("Whiteboard.JPEG", ShareName.of("Whiteboard.JPEG", "image/jpeg"));
        assertEquals("notes.txt", ShareName.of("notes.txt", "text/plain; charset=utf-8"));
    }

    @Test
    public void aNameWithoutOneGetsItsTypesExtension() {
        assertEquals("Invoice 4471.pdf", ShareName.of("Invoice 4471", "application/pdf"));
        assertEquals("IMG_0042.jpg", ShareName.of("IMG_0042", "image/jpeg"));
        assertEquals("file.pdf", ShareName.of(null, "application/pdf"));
        assertEquals("file.pdf", ShareName.of("  ", "application/pdf"));
    }

    @Test
    public void anUnknownTypeKeepsTheNameAndFoldersNeverPass() {
        assertEquals("archive", ShareName.of("archive", "application/zip"));
        assertEquals("a_b_c.pdf", ShareName.of("a/b\\c", "application/pdf"));
    }
}
