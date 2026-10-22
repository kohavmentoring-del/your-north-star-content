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

cp "$REPO_DIR/brand/voice.md" "$HOME/.claude/instagram/voice.md"
