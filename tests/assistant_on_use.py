"""assistant.py, loaded the first time a test asks for it.

The shared test helpers (test_assistant, test_connectors, test_graph, test_intercom_replies, test_ux) import what they use
from its own module, so importing one doesn't run assistant.py. They still hand it out (`a`, or test_assistant's
`assistant`) to the tests that read names through it, loaded on first use: those tests are the split's remaining work."""
import functools
import importlib.util
from pathlib import Path


@functools.lru_cache(maxsize=None)
def load(name):
    """assistant.py as a module called name, once per name (each helper keeps the name it loaded it under before)."""
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parent.parent / 'assistant.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def handed_out(attribute, name):
    """A module-level __getattr__ (PEP 562) that hands out assistant.py, loaded as name, as the helper's attribute."""
    def __getattr__(wanted):
        if wanted == attribute:
            return load(name)
        raise AttributeError(f'module has no attribute {wanted!r}')
    return __getattr__
