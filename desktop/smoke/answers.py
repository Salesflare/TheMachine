"""After each step: what is there of the app answers within 3 seconds, with the pointer over the robot too, and its own watch
(hangs.log) saw nothing, but where a step makes it hang."""
import shutil
import time

wanted = False  # the steps look themselves (hangs.py)
seen = ''


def after(log, out, number, robot, pointer, move, page):
    """What is wrong, or nothing. robot: the middle of it while it is there; page: what its page makes of 1."""
    global seen
    was, seen = seen, log.read_text(encoding='utf-8') if log.exists() else ''
    if seen and seen != was and not wanted:
        for file in (log, *log.parent.glob('hang-*.txt')):
            shutil.copy(file, out / f'{number:02d}-{file.name}')
        return 'hangs.log: ' + seen.strip().replace('\n', ' | ')
    try:
        at = robot()
    except AssertionError:
        at = None
    if not at:
        return ''
    back = pointer()
    move(*at)
    time.sleep(0.2)
    since, told = time.time(), None
    try:
        told = page()
    except (ConnectionError, StopIteration):
        told = 1  # the build for people has no such door
    except (OSError, ValueError) as e:
        if isinstance(getattr(e, 'reason', None), ConnectionError):
            told = 1
    took = time.time() - since
    move(*back)
    return '' if told == 1 and took < 3 else f'the robot does not answer within 3 s ({told}, {took:.1f} s)'
