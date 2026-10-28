"""Voice input's local engine (voice_input.py starts it): faster-whisper in its own virtualenv, one model loaded once.

It runs under that virtualenv's Python, never the service's, so the service itself stays on the standard library.
It reads requests on stdin and answers on stdout, one at a time:

    request:  one JSON line {"bytes": n, "language": "nl" or null, "languages": ["en", "nl", …]}, then n bytes of
              16 kHz mono 16-bit PCM
    answer:   one JSON line {"text": "…", "language": "nl"} or {"error": "…"}

The audio is only ever in memory here. It exits when stdin closes."""
from __future__ import annotations

import json
import sys


def main(model_dir, threads):
    import numpy as np
    from faster_whisper import WhisperModel

    model = WhisperModel(model_dir, device='cpu', compute_type='int8', cpu_threads=threads, num_workers=1)
    out = sys.stdout
    out.write(json.dumps({'ready': True}) + '\n')
    out.flush()
    source = sys.stdin.buffer
    while True:
        line = source.readline()
        if not line:
            return
        try:
            head = json.loads(line)
            size = int(head['bytes'])
            raw = source.read(size)
            if len(raw) != size:
                return
            audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            language = head.get('language') or None
            if not language:
                # Detect, but only among the languages the owner may speak to it in (the app's), so a short Dutch
                # sentence never comes back as Afrikaans
                allowed = [code for code in head.get('languages') or [] if isinstance(code, str)]
                _, _, scores = model.detect_language(audio)
                ranked = [code for code, _ in sorted(scores, key=lambda pair: -pair[1]) if not allowed or code in allowed]
                language = ranked[0] if ranked else None
            segments, info = model.transcribe(audio, language=language, beam_size=1, condition_on_previous_text=False,
                                              vad_filter=False, without_timestamps=False)
            text = ' '.join(segment.text.strip() for segment in segments).strip()
            answer = {'text': text, 'language': info.language}
        except Exception as error:  # one bad request never ends the worker; the service says what went wrong
            answer = {'error': type(error).__name__}
        out.write(json.dumps(answer) + '\n')
        out.flush()


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2)
