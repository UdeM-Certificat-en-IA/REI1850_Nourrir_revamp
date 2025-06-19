SSH Key Setup & Troubleshooting Guide
====================================

This repository comes bundled with a tiny helper script that fixes 95 % of
all *“Permission denied (publickey)”* headaches in a single command.

Quick start
-----------

```bash
./scripts/setup_ssh_key.sh
```

The script will:

1. Check for `~/.ssh/id_ed25519` (default key-type).
2. Create one *if it does not exist*, keeping your existing keys untouched.
3. Enforce correct permissions (`600` for private, `644` for public key).
4. Ensure an `ssh-agent` is running and load the key into it.
5. Display the **public key** so you can copy-paste it into:
   • `~/.ssh/authorized_keys` on a server, or
   • Your user profile on GitHub, GitLab, Gitea …

Advanced usage
--------------

```bash
# Generate an RSA key instead of ed25519
./scripts/setup_ssh_key.sh rsa

# Place the key in a custom location
./scripts/setup_ssh_key.sh ed25519 /path/to/key
```

Mounting host keys into Docker
------------------------------

If you need password-less Git access *inside* a Docker container (e.g. during
CI pipelines):

1. Start an `ssh-agent` on the host and run the setup script above.
2. Add the following lines to the service in `docker-compose.yml`:

```yaml
volumes:
  - ~/.ssh:/root/.ssh:ro            # read-only keys
  - $SSH_AUTH_SOCK:/ssh-agent       # forward agent socket
environment:
  - SSH_AUTH_SOCK=/ssh-agent
```

3. Re-create the container: `docker compose up -d --build`.

Common pitfalls
---------------

• **Wrong permissions** – private key must be `600`, public key `644`.
• **Missing key on server** – copy the `*.pub` contents into
  `/home/<user>/.ssh/authorized_keys` on the remote.
• **Multiple Git remotes** – verify the host in `.git/config` matches the
  host entry in `~/.ssh/config` or your hosting provider’s URL.

The helper script emits verbose logs; feel free to inspect the `logs/` folder
for additional output if you redirect stdout/stderr there.
