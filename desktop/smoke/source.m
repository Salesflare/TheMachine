// A window to drag from, for mac.py, until it is stopped: in its top left corner two files (its arguments), text and a
// link, each 120 points wide and as Finder, an editor and a browser put them.
#import <AppKit/AppKit.h>

@interface Thing : NSView <NSDraggingSource>
@property(strong) NSArray<id<NSPasteboardWriting>> *what;
@end

@implementation Thing
- (BOOL)acceptsFirstMouse:(NSEvent *)e { return YES; }
- (void)drawRect:(NSRect)r { [NSColor.lightGrayColor setFill]; NSRectFill(self.bounds); }
- (void)mouseDown:(NSEvent *)e {}
- (void)mouseDragged:(NSEvent *)e {
  NSMutableArray *items = [NSMutableArray array];
  for (id<NSPasteboardWriting> w in self.what) {
    NSDraggingItem *item = [[NSDraggingItem alloc] initWithPasteboardWriter:w];
    [item setDraggingFrame:NSMakeRect(0, 0, 16, 16) contents:[NSImage imageNamed:NSImageNameMultipleDocuments]];
    [items addObject:item];
  }
  [self beginDraggingSessionWithItems:items event:e source:self];
}
- (NSDragOperation)draggingSession:(NSDraggingSession *)s sourceOperationMaskForDraggingContext:(NSDraggingContext)c { return NSDragOperationCopy; }
@end

int main(int n, const char **given) {
  [NSApplication sharedApplication].activationPolicy = NSApplicationActivationPolicyAccessory;
  NSRect all = NSScreen.screens.firstObject.frame;
  NSPanel *window = [[NSPanel alloc] initWithContentRect:NSMakeRect(40, all.size.height - 200, 400, 100) styleMask:NSWindowStyleMaskBorderless | NSWindowStyleMaskNonactivatingPanel backing:NSBackingStoreBuffered defer:NO];
  window.hidesOnDeactivate = NO;
  window.level = NSFloatingWindowLevel;
  NSMutableArray *files = [NSMutableArray array];
  for (int i = 1; i < n; i++) [files addObject:[NSURL fileURLWithPath:@(given[i])]];
  NSArray *each = @[ files, @[ @"Ask Dana <b>about</b> the pilot" ], @[ [NSURL URLWithString:@"https://example.com/pilot?x=1"] ] ];
  for (NSUInteger i = 0; i < each.count; i++) {
    Thing *thing = [[Thing alloc] initWithFrame:NSMakeRect(130 * i, 0, 120, 100)];
    thing.what = each[i];
    [window.contentView addSubview:thing];
  }
  [window orderFrontRegardless];
  [NSApp run];
}
