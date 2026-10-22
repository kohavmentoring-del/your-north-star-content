#!/usr/bin/env bash
# Installs the ig-* skill pack and Kohav's voice profile so reel-kit works in a fresh session.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PACK_URL="https://github.com/postzen-dev/instagram-agent-skill.git"
# Pinned so an upstream change can't silently alter the skills.
PACK_COMMIT="b38be357f1a72e248f50883af4d379ac66c8aa43"

mkdir -p "$HOME/.claude/skills" "$HOME/.claude/instagram"

if [ ! -f "$HOME/.claude/skills/ig-reel/hookscore.py" ]; then
  tmp="$(mktemp -d)"
  git clone --quiet "$PACK_URL" "$tmp/pack"
  git -C "$tmp/pack" checkout --quiet "$PACK_COMMIT"
  cp -r "$tmp/pack/skills/"ig-* "$HOME/.claude/skills/"
  rm -rf "$tmp"
fi

# HeyGen's hosted HyperFrames renderer refuses Claude Code, so render locally with their skills + CLI.
HF_URL="https://github.com/heygen-com/hyperframes.git"
HF_COMMIT="4371981b740d92f70e520cfbec34db68a1c93434"

if [ ! -f "$HOME/.claude/skills/hyperframes/SKILL.md" ]; then
  tmp="$(mktemp -d)"
  git clone --quiet --filter=blob:none --no-checkout "$HF_URL" "$tmp/hf"
  git -C "$tmp/hf" -c gc.auto=0 checkout --quiet "$HF_COMMIT" -- skills
  for s in hyperframes hyperframes-cli media-use hyperframes-registry; do
    cp -r "$tmp/hf/skills/$s" "$HOME/.claude/skills/"
  done
  rm -rf "$tmp"
fi

if [ ! -d "$HOME/.cache/hyperframes/chrome" ]; then
  (cd "$REPO_DIR" && npx -y hyperframes@0.8.185 browser ensure >/dev/null 2>&1) || true
fi

cp "$REPO_DIR/brand/voice.md" "$HOME/.claude/instagram/voice.md"
