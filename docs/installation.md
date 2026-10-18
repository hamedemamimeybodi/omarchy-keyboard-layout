# Installation, disable, removal and fallback

These instructions are for a new installation. Do not run them on an already functioning installation just to validate publication. Read the source and review the desired commit first. The original plugin ID is preserved, so upstream and this fork cannot be installed side by side.

## Prepare

Set `FORK_URL` to this fork's actual GitHub Code URL and `REVIEWED_COMMIT` to the full reviewed commit. Neither is an invitation to install unreviewed mutable HEAD. Omarchy's normal add command clones the repository's default branch, so verify that it is the restoration branch before proceeding. Required tools are Git, Omarchy/Quickshell, a C compiler, Make, pkg-config and json-c headers; use your package manager if missing.

Build a clean checkout outside the watched plugin directory. Keep the checkout for review and recovery:

```bash
work=$(mktemp -d)
git clone -- "$FORK_URL" "$work/source"
git -C "$work/source" checkout --detach "$REVIEWED_COMMIT"
make -C "$work/source/native" clean all
omarchy plugin validate "$work/source"
```

Inspect the active shell configuration. Require the built-in widget selected, this plugin ID absent from configuration and its target directory absent; stop to review any existing installation or stale clone markers. Preserve a private copy of `~/.config/omarchy/shell.json` with ownership, modes and timestamps before modifying it. Do not change keyboard settings unnecessarily. For the tested setup, effective XKB options are `kb_layout = "us,ir"` and `kb_options = "grp:alt_shift_toggle"` in the existing Hyprland input configuration.

## Add without enabling, then validate

```bash
omarchy plugin add "$FORK_URL" --yes
target="$HOME/.config/omarchy/plugins/io.github.ilyazar.keyboard-layout"
test "$(git -C "$target" rev-parse HEAD)" = "$REVIEWED_COMMIT" || exit 1
install -m 755 "$work/source/native/keyboard-layoutd" "$target/native/keyboard-layoutd"
omarchy plugin validate "$target"
omarchy plugin enable io.github.ilyazar.keyboard-layout
```

The absence of an existing config entry is essential: adding an ID already selected by stale config can enable it automatically. Omarchy watches plugin files, so publication/build replacement can hot-reload plugin widgets and other non-retained components. No desktop or auth/lock service restart is prescribed. Stop if current session safety cannot be established. Rebuilding before enable avoids executing an incompatible bundled binary. A locally rebuilt tracked binary may make later git updates dirty; keep its source commit/build record and review updates explicitly.

## Disable or restore the built-in

```bash
omarchy plugin disable io.github.ilyazar.keyboard-layout
```

The supported clone mechanism is designed to restore `omarchy.keyboard-layout` and retain applicable inline settings. Check its registration/selection and that the candidate helper has stopped. Do not assume rendering merely from a registry flag. If reversal is ambiguous, preserve logs/state and stop; do not restart authentication or the compositor. Live fallback has not been independently tested in this restoration.

## Remove

First back up any plugin modifications and inline settings outside the watched directory, then disable and verify the built-in. The supported removal command deletes a Git-managed checkout:

```bash
omarchy plugin remove io.github.ilyazar.keyboard-layout --yes
```

Do not use removal as a backup mechanism or restore an old whole configuration over unrelated edits. Preserve your existing US/Persian and switching options throughout. The separate staged source checkout can be kept until acceptance is complete.
