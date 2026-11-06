"""Patch a name everywhere it is bound, not only on the module a test names.

`patch.object(a, 'now', ...)` replaces `now` on the assistant module only. Code that moved to another module (machine/,
a root module) looks the name up there, so it would quietly keep the real clock, credentials or sends while the test
still passes. `patch_everywhere(a, 'now', ...)` replaces it on `a` and on every module of this app that binds the very
same object (the module it came from, and each module that imported it), and puts them all back after.

It takes what `patch.object` takes and works the same way: `with`, as a decorator (also on a class), and start()/stop().
Methods of a class (`a.App`, `a.Store`) need no help: patch the class attribute as before."""
from pathlib import Path
import sys
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
_MISSING = object()


def ours(module):
    """Whether a loaded module is part of this app (its own code or a test's copy of it), never the standard library or
    a package: only those are patched besides the one named."""
    try:
        path = Path(getattr(module, '__file__', None) or '').resolve()
    except (OSError, TypeError, ValueError):
        return False
    return bool(path.name) and path.is_relative_to(ROOT) and 'site-packages' not in path.parts


def bindings(module, name, value):
    """The other loaded modules of this app that bind name to value itself."""
    found = []
    for other in list(sys.modules.values()):
        if other is None or other is module or not ours(other):
            continue
        try:
            if vars(other).get(name, _MISSING) is value:
                found.append(other)
        except TypeError:
            continue
    return found


class _Everywhere(mock._patch):
    """A patch.object that also patches each other module binding the same object."""

    def __enter__(self):
        target = self.getter()
        original = vars(target).get(self.attribute, _MISSING) if hasattr(target, '__dict__') else _MISSING
        others = bindings(target, self.attribute, original) if original is not _MISSING else []
        result = super().__enter__()
        value = getattr(target, self.attribute)
        self._everywhere = [(other, original) for other in others]
        for other in others:
            setattr(other, self.attribute, value)
        return result

    def __exit__(self, *exc):
        for other, original in reversed(getattr(self, '_everywhere', [])):
            setattr(other, self.attribute, original)
        self._everywhere = []
        return super().__exit__(*exc)

    def copy(self):
        patcher = super().copy()
        patcher.__class__ = type(self)
        return patcher


def patch_everywhere(target, attribute, new=mock.DEFAULT, **kwargs):
    """patch.object(target, attribute, new, **kwargs), also on every module of this app that binds the same object."""
    patcher = mock.patch.object(target, attribute, new, **kwargs)
    patcher.__class__ = _Everywhere
    return patcher


def replace_everywhere(target, attribute, new):
    """For good (a sandbox, a process of its own): target.attribute and every binding of the same object become new.
    Returns the modules changed besides target."""
    original = vars(target).get(attribute, _MISSING)
    others = bindings(target, attribute, original) if original is not _MISSING else []
    for module in [target, *others]:
        setattr(module, attribute, new)
    return others
