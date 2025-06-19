#!/usr/bin/env bash

# =========================================================================
# setup_ssh_key.sh
# -------------------------------------------------------------------------
# A tiny helper script that makes the most common SSH-key problems vanish.
#
# It will:
#   1. Verify that an SSH key exists (default: Ed25519).
#   2. Generate one if it does not.
#   3. Make sure correct file permissions are enforced (600 for the key,
#      644 for the corresponding public key).
#   4. Start an ssh-agent if none is running and add the key to it.
#   5. Spit out the public key at the end so it can be copied to a server or
#      a Git forge such as GitHub / GitLab / Gitea.
#
# Usage
#   ./scripts/setup_ssh_key.sh [key_type] [key_path]
#
#   key_type  – rsa | ed25519 | ecdsa (default: ed25519)
#   key_path  – absolute or relative path to private key (optional).
#               If omitted, ~/.ssh/id_<key_type> is used.
#
# NOTE: The script is idempotent – it can be re-run safely; if the key is
#       already present it will *not* be overwritten.
# =========================================================================

set -euo pipefail

DEFAULT_KEY_TYPE="ed25519"
# shellcheck disable=SC2034 # (KEY_TYPE may be overridden by positional arg)
KEY_TYPE="${1:-${DEFAULT_KEY_TYPE}}"

# Determine key path
if [[ $# -ge 2 ]]; then
  KEY_PATH="$2"
else
  KEY_PATH="$HOME/.ssh/id_${KEY_TYPE}"
fi

PUB_KEY_PATH="${KEY_PATH}.pub"

mkdir -p "$(dirname "$KEY_PATH")"

generate_key() {
  echo "[ssh-setup] Generating a new ${KEY_TYPE^^} key at ${KEY_PATH}" >&2
  ssh-keygen -t "$KEY_TYPE" -C "$(whoami)@$(hostname)-$(date +%Y-%m-%d)" -f "$KEY_PATH" -N ""
}

ensure_permissions() {
  chmod 600 "$KEY_PATH"
  chmod 644 "$PUB_KEY_PATH"
}

start_agent_and_add_key() {
  # Detect existing ssh-agent; start one if necessary.
  if [[ -z "${SSH_AUTH_SOCK:-}" ]] || ! ssh-add -l >/dev/null 2>&1; then
    echo "[ssh-setup] Starting new ssh-agent session" >&2
    eval "$(ssh-agent -s)" >/dev/null
  fi

  # Add key if not already loaded.
  if ! ssh-add -l 2>/dev/null | grep -q "$(basename "$KEY_PATH")"; then
    echo "[ssh-setup] Adding key to ssh-agent" >&2
    ssh-add "$KEY_PATH" >/dev/null
  fi
}

if [[ -f "$KEY_PATH" ]]; then
  echo "[ssh-setup] An existing key was found at ${KEY_PATH}, skipping creation." >&2
  ensure_permissions
else
  generate_key
fi

start_agent_and_add_key

echo "\n[ssh-setup] Public key ready to be copied to your server / Git provider:\n"
cat "$PUB_KEY_PATH"

echo "\n[ssh-setup] All done!" >&2
