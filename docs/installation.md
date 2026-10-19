# Installation, disable, removal and fallback

These instructions are for a new installation. Do not run them on an already functioning installation just to validate publication. Read the source and review the desired commit first. The original plugin ID is preserved, so upstream and this fork cannot be installed side by side.

## Prepare

The tested runtime source is `restoration/qt612` at `5e4679aa47d488df1237706810da7c4ede03b705`. Documentation-only successors do not retroactively receive a new GUI or CI result. Required tools include Git, Omarchy/Quickshell, a C compiler, Make, pkg-config and json-c headers; use your package manager if missing.

Build a clean checkout outside the watched plugin directory. Keep the checkout for review and recovery:

```bash
work=$(mktemp -d)
FORK_URL=https://github.com/hamedemamimeybodi/omarchy-keyboard-layout.git
REVIEWED_COMMIT=5e4679aa47d488df1237706810da7c4ede03b705
git clone --branch restoration/qt612 --single-branch -- "$FORK_URL" "$work/source"
git -C "$work/source" checkout --detach "$REVIEWED_COMMIT"
test "$(git -C "$work/source" rev-parse HEAD)" = "$REVIEWED_COMMIT" || exit 1
make -C "$work/source/native" clean all
omarchy plugin validate "$work/source"
```

Inspect the active shell configuration. Require the built-in widget selected, this plugin ID absent from configuration and its target directory absent; stop to review any existing installation or stale clone markers. Preserve a private copy of `~/.config/omarchy/shell.json` with ownership, modes and timestamps before modifying it. Do not change keyboard settings unnecessarily. For the tested setup, effective XKB options are `kb_layout = "us,ir"` and `kb_options = "grp:alt_shift_toggle"` in the existing Hyprland input configuration.

## Live installation gate

The installed Omarchy add command clones mutable default HEAD and has no branch/SHA option. A GitHub `/tree/restoration/qt612` URL is not a Git clone URL. The branch-pinned preparation above is not a live installation. Check what the standard installer would fetch:

```bash
git ls-remote --symref "$FORK_URL" HEAD
```

The current default branch/HEAD has not been freshly verified in this documentation review. If it differs from the exact reviewed runtime source, stop before `omarchy plugin add`; a post-add checkout would already have published files into a watched directory. Do not assume that a documentation-only successor, another default branch, or mutable branch HEAD was tested. Ask for a reviewed installation route selecting the intended source instead of inventing a branch flag, changing the repository default, or modifying a functioning installation. No universal one-command install readiness is claimed here.

If a future live installation is reviewed, require absence of this ID in both configuration and the target directory, preserve the built-in configuration/settings, validate a staged source build, and verify the exact installed commit before activation. Absence of stale selection matters: adding a configured ID can activate code automatically. The normal add command requests plugin rediscovery even without enabling; publication/build replacement can hot-reload watched components. Rebuild the native helper for the destination before activation. No shell/compositor or auth/lock restart is prescribed. A locally rebuilt tracked binary may make later updates dirty; preserve its source/build record and review updates explicitly.

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
