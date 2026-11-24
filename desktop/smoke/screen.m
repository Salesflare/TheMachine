// A second screen that isn't there, for mac.py: 1280 x 800 points at two pixels each, until it is stopped.
#import <AppKit/AppKit.h>

@interface CGVirtualDisplayDescriptor : NSObject
@property unsigned int vendorID, productID, serialNum, maxPixelsWide, maxPixelsHigh;
@property(strong) NSString *name;
@property CGSize sizeInMillimeters;
@property(strong) dispatch_queue_t queue;
@end
@interface CGVirtualDisplayMode : NSObject
- (instancetype)initWithWidth:(unsigned int)w height:(unsigned int)h refreshRate:(double)r;
@end
@interface CGVirtualDisplaySettings : NSObject
@property unsigned int hiDPI;
@property(strong) NSArray *modes;
@end
@interface CGVirtualDisplay : NSObject
@property(readonly) unsigned int displayID;
- (instancetype)initWithDescriptor:(CGVirtualDisplayDescriptor *)d;
- (BOOL)applySettings:(CGVirtualDisplaySettings *)s;
@end

int main(void) {
  [NSApplication sharedApplication];
  CGVirtualDisplayDescriptor *d = [NSClassFromString(@"CGVirtualDisplayDescriptor") new];
  if (!d) return 1;
  d.queue = dispatch_get_main_queue();
  d.name = @"Made-up screen";
  d.vendorID = 0x1234; d.productID = 0x5678; d.serialNum = 1;
  d.maxPixelsWide = 2560; d.maxPixelsHigh = 1600;
  d.sizeInMillimeters = CGSizeMake(300, 190);
  CGVirtualDisplay *display = [[NSClassFromString(@"CGVirtualDisplay") alloc] initWithDescriptor:d];
  CGVirtualDisplaySettings *s = [NSClassFromString(@"CGVirtualDisplaySettings") new];
  s.hiDPI = 1;
  s.modes = @[ [[NSClassFromString(@"CGVirtualDisplayMode") alloc] initWithWidth:1280 height:800 refreshRate:60] ];
  if (!display || ![display applySettings:s]) return 1;
  printf("%u\n", display.displayID);
  fflush(stdout);
  [[NSRunLoop mainRunLoop] run];
  return display == nil;
}
