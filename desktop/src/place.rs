//! Where the robot and its box go, in one monitor's work area. The robot is kept as a distance from the bottom right
//! corner, so it stays in its corner when the resolution, the scale or the taskbar changes. Plain numbers, no windows.
use serde::{Deserialize, Serialize};

/// Logical pixels from the right and bottom edge of the work area.
#[derive(Clone, Copy, Debug, PartialEq, Serialize, Deserialize)]
pub struct Corner {
    pub right: f64,
    pub bottom: f64,
}

impl Default for Corner {
    fn default() -> Self {
        Corner { right: 16.0, bottom: 12.0 }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Rect {
    pub x: f64,
    pub y: f64,
    pub w: f64,
    pub h: f64,
}

pub const ROBOT: (f64, f64) = (88.0, 88.0);
/// How much of a hidden robot still shows: it looks over the bottom edge, so it is there to click.
pub const PEEK: f64 = 40.0;
pub const BOX_WIDTH: f64 = 340.0;
pub const BUBBLE_WIDTH: f64 = 300.0;
pub const GAP: f64 = 6.0;
/// The box always has room for a shadow around it, so its window is this much larger on every side.
pub const SHADOW: f64 = 14.0;

impl Corner {
    /// Kept inside an area of this size, whatever was saved or dragged.
    pub fn inside(self, w: f64, h: f64) -> Corner {
        let keep = |v: f64, max: f64| if v.is_finite() { v.max(0.0).min(max.max(0.0)) } else { 0.0 };
        Corner { right: keep(self.right, w - ROBOT.0), bottom: keep(self.bottom, h - ROBOT.1) }
    }

    pub fn robot(self, area: Rect) -> Rect {
        let c = self.inside(area.w, area.h);
        Rect { x: area.x + area.w - ROBOT.0 - c.right, y: area.y + area.h - ROBOT.1 - c.bottom, w: ROBOT.0, h: ROBOT.1 }
    }

    /// The corner of a robot that stands at this point.
    pub fn at(x: f64, y: f64, area: Rect) -> Corner {
        Corner { right: area.x + area.w - ROBOT.0 - x, bottom: area.y + area.h - ROBOT.1 - y }.inside(area.w, area.h)
    }
}

/// How much larger all of it is for a person who has larger text: as their text, while a screen of this size still has room.
#[cfg_attr(not(windows), allow(dead_code))]
pub fn larger(text: f64, w: f64, h: f64) -> f64 {
    text.min(w / 400.0).min(h / 480.0).max(1.0)
}

/// A hidden robot: down at the bottom edge, where it stood.
pub fn peek(robot: Rect, area: Rect) -> Rect {
    Rect { y: area.y + area.h - PEEK, h: PEEK, ..robot }
}

/// How tall the box is with a to-do open in it: comfortable, in the larger space above or below the robot.
pub fn tall(robot: Rect, area: Rect) -> f64 {
    room(robot, area).clamp(420.0, 640.0).min(area.h - 16.0).max(200.0)
}

/// How tall the box can be above or below the robot.
pub fn room(robot: Rect, area: Rect) -> f64 {
    let (above, below) = (robot.y - area.y, area.y + area.h - robot.y - robot.h);
    above.max(below) - GAP - 8.0
}

/// Where the robot's middle is along a bubble, so that its tail points there.
pub fn tail(robot: Rect, bubble: Rect) -> f64 {
    let half = (BUBBLE_WIDTH / 2.0 - 24.0).max(0.0);
    (robot.x + robot.w / 2.0 - bubble.x - bubble.w / 2.0).clamp(-half, half) + BUBBLE_WIDTH / 2.0
}

/// The window of the box, or of a bubble, for a robot: above it, its right edge over the robot's, below it when there is no room above, beside it
/// when there is none there either, and always within the area. height is the page's own, without the shadow.
pub fn box_at(robot: Rect, area: Rect, width: f64, height: f64) -> Rect {
    let (w, h) = (width + 2.0 * SHADOW, height.min(area.h) + 2.0 * SHADOW);
    let over = SHADOW - 8.0; // the box keeps 8 from the edges, its shadow not
    let x = (robot.x + robot.w - width - SHADOW).max(area.x - over).min(area.x + area.w - w + over);
    let above = robot.y - GAP - height - SHADOW;
    let mut y = if above >= area.y - over { above } else { robot.y + robot.h + GAP - SHADOW };
    let inside = |y: f64| y.min(area.y + area.h - h + over).max(area.y - over);
    let mut x = x;
    if y >= robot.y && inside(y) < y {
        let (left, right) = (robot.x - GAP - width - SHADOW, robot.x + robot.w + GAP - SHADOW);
        let fits = |x: f64| x >= area.x - over && x + w <= area.x + area.w + over;
        if let Some(beside) = [left, right].into_iter().find(|x| fits(*x)) {
            (x, y) = (beside, robot.y + robot.h - height - SHADOW);
        }
    }
    Rect { x, y: inside(y), w, h }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_grows_with_the_text_where_there_is_room() {
        assert_eq!(larger(1.0, 1920.0, 1032.0), 1.0);
        assert_eq!(larger(1.5, 1920.0, 1152.0), 1.5);
        assert_eq!(larger(2.25, 1920.0, 1152.0), 2.25);
        assert_eq!(larger(2.25, 1280.0, 672.0), 1.4);
        assert_eq!(larger(1.5, 640.0, 400.0), 1.0); // never smaller
        for (text, w, h) in [(1.5, 1280.0, 672.0), (2.25, 1280.0, 672.0), (2.25, 1920.0, 1032.0)] {
            let by = larger(text, w, h);
            let area = Rect { x: 0.0, y: 0.0, w: w / by, h: h / by };
            let at = box_at(Corner::default().robot(area), area, BOX_WIDTH, 700.0_f64.min(area.h - 16.0));
            assert!(at.x >= -SHADOW && at.x + at.w <= area.w + SHADOW && at.y >= -SHADOW && at.y + at.h <= area.h + SHADOW, "{at:?} in {area:?}");
        }
    }

    const AREA: Rect = Rect { x: 1920.0, y: 30.0, w: 1280.0, h: 690.0 };

    #[test]
    fn a_to_do_in_the_box_fits_the_screen() {
        for (bottom, h) in [(12.0, 690.0), (12.0, 1040.0), (12.0, 400.0), (300.0, 690.0), (602.0, 690.0)] {
            let area = Rect { h, ..AREA };
            let robot = Corner { right: 16.0, bottom }.robot(area);
            let tall = tall(robot, area);
            let r = box_at(robot, area, BOX_WIDTH, tall);
            assert!(tall >= 360.0 && r.y >= area.y - SHADOW && r.y + r.h <= area.y + area.h + SHADOW, "{bottom} {h}: {tall} {r:?}");
        }
    }

    #[test]
    fn starts_bottom_right() {
        let r = Corner::default().robot(AREA);
        assert_eq!((r.x + r.w, r.y + r.h), (3200.0 - 16.0, 720.0 - 12.0));
    }

    #[test]
    fn stays_on_the_screen() {
        for c in [Corner { right: -50.0, bottom: -50.0 }, Corner { right: 9e9, bottom: 9e9 }, Corner { right: f64::NAN, bottom: f64::INFINITY }] {
            let r = c.robot(AREA);
            assert!(r.x >= AREA.x && r.y >= AREA.y && r.x + r.w <= AREA.x + AREA.w && r.y + r.h <= AREA.y + AREA.h, "{c:?} {r:?}");
        }
        // an area smaller than the robot doesn't panic
        Corner::default().robot(Rect { w: 10.0, h: 10.0, ..AREA });
    }

    #[test]
    fn remembers_where_it_was_dropped() {
        let r = Corner::at(2000.0, 100.0, AREA).robot(AREA);
        assert_eq!((r.x, r.y), (2000.0, 100.0));
    }

    #[test]
    fn keeps_its_corner_on_another_resolution() {
        let c = Corner::at(AREA.x + AREA.w - ROBOT.0 - 20.0, AREA.y + AREA.h - ROBOT.1 - 20.0, AREA);
        let r = c.robot(Rect { x: 0.0, y: 0.0, w: 1000.0, h: 500.0 });
        assert_eq!((r.x + r.w, r.y + r.h), (980.0, 480.0));
    }

    #[test]
    fn the_box_is_on_the_screen_wherever_the_robot_is() {
        for right in [0.0, 300.0, 1192.0] {
            for bottom in [0.0, 200.0, 602.0] {
                for height in [150.0, 320.0, 480.0] {
                    let robot = Corner { right, bottom }.robot(AREA);
                    let b = box_at(robot, AREA, BOX_WIDTH, height);
                    let seen = Rect { x: b.x + SHADOW, y: b.y + SHADOW, w: b.w - 2.0 * SHADOW, h: b.h - 2.0 * SHADOW };
                    assert!(seen.x >= AREA.x && seen.x + seen.w <= AREA.x + AREA.w, "{right} {bottom} {height} {seen:?}");
                    assert!(seen.y >= AREA.y && seen.y + seen.h <= AREA.y + AREA.h, "{right} {bottom} {height} {seen:?}");
                }
            }
        }
    }

    #[test]
    fn the_box_never_covers_the_robot() {
        for area in [AREA, Rect { x: 0.0, y: 31.0, w: 1024.0, h: 648.0 }, Rect { x: 0.0, y: 0.0, w: 1366.0, h: 720.0 }] {
            for right in [0.0, 16.0, 500.0, 900.0] {
                for bottom in [0.0, 12.0, 250.0, 560.0] {
                    for height in [150.0, 420.0, 570.0, 620.0] {
                        let robot = Corner { right, bottom }.robot(area);
                        let b = box_at(robot, area, BOX_WIDTH, height);
                        let (x, y) = (b.x + SHADOW, b.y + SHADOW);
                        let over = x < robot.x + robot.w && x + BOX_WIDTH > robot.x && y < robot.y + robot.h && y + height > robot.y;
                        assert!(!over, "{area:?} {right} {bottom} {height} {b:?}");
                        assert!(x >= area.x && x + BOX_WIDTH <= area.x + area.w && y >= area.y && y + height <= area.y + area.h, "{area:?} {right} {bottom} {height} {b:?}");
                    }
                }
            }
        }
    }

    #[test]
    fn a_bubbles_tail_is_at_the_robot() {
        for right in [0.0, 16.0, 600.0, 1192.0] {
            let robot = Corner { right, bottom: 12.0 }.robot(AREA);
            let b = box_at(robot, AREA, BUBBLE_WIDTH, 90.0);
            let at = b.x + SHADOW + tail(robot, b);
            assert!((at - (robot.x + robot.w / 2.0)).abs() < 21.0, "{right} {at} {robot:?}");
        }
    }

    #[test]
    fn a_hidden_one_looks_over_the_bottom_edge() {
        let r = peek(Corner { right: 300.0, bottom: 400.0 }.robot(AREA), AREA);
        assert_eq!((r.x, r.y + r.h, r.w, r.h), (AREA.x + AREA.w - 388.0, AREA.y + AREA.h, 88.0, PEEK));
        assert!(box_at(r, AREA, BOX_WIDTH, 300.0).y + SHADOW + 300.0 <= r.y);
    }

    #[test]
    fn the_box_is_above_the_robot_then_below() {
        let low = Corner::default().robot(AREA);
        assert!(box_at(low, AREA, BOX_WIDTH, 300.0).y + SHADOW + 300.0 <= low.y);
        let high = Corner { right: 16.0, bottom: 602.0 }.robot(AREA);
        assert!(box_at(high, AREA, BOX_WIDTH, 300.0).y + SHADOW >= high.y + high.h);
    }
}
