# Testing

Run the commands in README.md from a separate source checkout. Build the native helper first; do not execute an arbitrary saved executable solely because its checksum matches.

- `test_hypr_ipc`: keyboard selection, JSON parsing and IPC input handling.
- `test_layout_memory`: window-address lifetime and layout memory.
- `layout-state.test.mjs`: thirteen widget model regressions, including variants and restore/pulse behavior.
- `private_ipc_integration.py`: seven scenarios against disposable local sockets, including resynchronization after reconnect. It starts and terminates only its own freshly built child and uses a unique runtime directory/signature.

The public integration fixture is adapted from the previously successful private test by replacing its fixed sandbox-only directory with a private temporary directory and unique signature. Its new result must be reported separately. Socket bind restrictions can block it in restricted environments; that is not a passed test and must not be silently skipped.

Optional Qt syntax checks may use qmlformat without `--inplace`. Real semantic/import checking needs the installed Omarchy Commons/UI context and Quickshell registration. Standalone Qt import failures are not equivalent to actual Quickshell failures. Keep warnings visible and separate tool limitations from real diagnostics.

Manual acceptance should cover visible widget/picker/settings, typed text and physical shortcut, two windows with independent groups, close/reopen, repeated switches and a separate approved fallback rehearsal. Do not force a compositor restart or authentication disruption for tests. Reconnection in the fake transport is not a live reconnection result.

CI is defined in `.github/workflows/tests.yml`. Its hosted status must be checked after push; the presence of this file is not evidence that Actions ran.
