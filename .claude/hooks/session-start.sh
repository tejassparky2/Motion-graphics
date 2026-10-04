#!/bin/bash
# SessionStart hook for Claude Code cloud sessions: installs what render.py, the voice clone and the checks need.
# Idempotent; each step is skipped when it's already done. See DOCTOR_CHANNEL.md "Setting up a fresh container".
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

# System libraries: Cairo headers to build pycairo.
if ! pkg-config --exists cairo 2>/dev/null; then
  (apt-get update -qq && apt-get install -y -qq libcairo2-dev pkg-config) || echo "warning: could not install libcairo2-dev" >&2
fi

# Main environment (renderer, Kokoro voices, Whisper checks) + pyflakes for linting.
if ! python -c "import docopt" 2>/dev/null; then
  SETUPTOOLS_USE_DISTUTILS=stdlib pip install -q docopt   # docopt's old setup.py fails on this image without it
fi
pip install -q -r requirements.txt pyflakes

# The doctor's cloned voice (Chatterbox) lives in its own venv: CPU torch + chatterbox-tts.
CLONE=/home/user/.venv-clone
if [ ! -x "$CLONE/bin/python" ]; then
  python -m venv "$CLONE"
fi
if ! "$CLONE/bin/python" -c "import chatterbox, faster_whisper, soundfile" 2>/dev/null; then
  "$CLONE/bin/pip" install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
  SETUPTOOLS_USE_DISTUTILS=stdlib "$CLONE/bin/pip" install -q chatterbox-tts==0.1.7 faster-whisper soundfile
fi

echo 'export PYTHONPATH="."' >> "${CLAUDE_ENV_FILE:-/dev/null}"
echo "session-start: environment ready"
