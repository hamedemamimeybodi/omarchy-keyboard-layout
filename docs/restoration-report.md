# Technical restoration report

## Source lineage

The restoration starts at upstream commit `bd2cdf809f755ffa03cebeb6dcd237d252fca594` (0.2.3). The original 38-commit ancestry is retained. Root/native license notices, manifest, service and settings interfaces remain intact. There is no claim that these changes have been merged upstream.

## Qt namespace and QML scope

Qt 6.12 introduces an ambiguous `Color` lookup in this import environment. Both affected files import `qs.Commons as Commons` and use `Commons.Color` for nine existing references. This resolves the intended singleton explicitly instead of guessing that undefined colors are missing theme values.

Twenty formerly implicit scope references in the main widget are qualified with their owning IDs; an explicit row ID makes its layout bindings unambiguous. The changes preserve pulse behavior, settings, custom-color validation, variant labels, shortcut display, picker and scrolling.

The 63 retained lint warnings were reviewed individually: 39 concern the generic bar facade, 14 the font object, eight the spacing object and two valid function-scoped var declarations. The generic QtObject declarations hide concrete members from static analysis. No warning was blindly suppressed, and this classification is not proof that every lazy GUI branch has executed.

## Native keyboard and window logic

The widget already excludes laptop extra-button and WMI-hotkey devices. The native keyboard selector now applies the same two exclusions. A parser regression covers the laptop fixture, keeping the daemon and widget aligned.

The existing daemon observes focus/layout events and restores per-window state through Hyprland IPC. Closing a window removes its memory; configuration reload and socket reconnection resynchronize state. It uses bounded JSON/event parsing and does not execute shell commands to switch layouts. Only the two filtering exclusions and their test are new native source changes; the state machine was preserved.

## Validation and limits

The operator reported five manual PASS observations: rendering; US/Persian Alt+Shift; independent A/B layouts; close/reopen behavior; repeated switching stability. The saved deployment result reported registry activation, a matching rebuilt helper, initial process stability, expected configuration and no matching new critical QML log diagnostics. Raw machine evidence is deliberately not distributed.

Seven original private fake-IPC scenarios passed, covering startup synchronization, A/B state, closed-address reuse, unfocused changes, config reload, malformed/fragmented events and event reconnect. Native parser/memory units, thirteen widget model regressions and local Qt syntax/color checks have separate saved results. The adapted public fixture was locally blocked before daemon startup by socket-binding restrictions.

The [published Actions run](https://github.com/hamedemamimeybodi/omarchy-keyboard-layout/actions/runs/39181234084) completed successfully at restoration source commit `5e4679aa47d488df1237706810da7c4ede03b705`. Authenticated host review verified the completed/successful public IPC step and its actual PASS output with all seven scenarios and empty daemon stderr. This separately establishes the adapted fixture's execution; it is not inferred from the overall run conclusion or the original private test. The fixture's reconnection scenario uses fake sockets, not live Hyprland reconnection. [Validation details](validation-summary.md).

Live rollback and live daemon reconnection have not been independently tested. A successful fake socket, model test, process check or CI run cannot establish full GUI compatibility. Existing native ASan/UBSan checks used leak detection disabled because of tooling constraints; no leak-check PASS is claimed.
