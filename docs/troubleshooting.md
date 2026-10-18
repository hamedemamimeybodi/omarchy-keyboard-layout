# Troubleshooting

| Symptom | Check and response |
| --- | --- |
| Undefined color or Qt Color namespace error | Verify the running copy imports `qs.Commons as Commons` and the nine repaired lookups use `Commons.Color`. Check the installed commit; do not edit packaged shell QML. |
| Helper fails with GLIBC/loader errors | Build the native source on the destination machine while the plugin is disabled; validate and only then enable. |
| Per-window mode is unavailable | Confirm x86-64 support, json-c availability, and the per-window preference. The original architecture gate is retained. |
| Layout restores track a hotkey pseudo-keyboard | Confirm both widget and daemon include the laptop extra-button/WMI exclusions and match the restored source. |
| Widget absent | Check `omarchy plugin list --json`, bar placement, and the show-with-one-layout preference. A generic active flag is not a rendering assertion. |
| Shortcut does not change groups | Inspect `hyprctl getoption input:kb_layout`, `hyprctl getoption input:kb_options` and `hyprctl devices -j`; expect us,ir and grp:alt_shift_toggle for the tested setup. Resolve conflicting rules with the configuration owner. |
| Shell command says not running | Try from the existing graphical-session terminal. A sandbox socket-access denial does not prove the host shell stopped. Do not respond with a forced restart. |
| Generic font/spacing/bar lint warnings | Use real Omarchy import context; consult the root-cause breakdown in restoration-report.md. Do not suppress arbitrary warnings. |
| CI private-socket test cannot bind | Record the restriction; run in a disposable environment that permits local sockets. Do not route the test to live Hyprland. |

For reports, provide the fork commit, software versions, minimal redacted diagnostics and reproduction steps. Do not attach personal configuration dumps, raw desktop logs, credentials or machine identifiers. A fallback should use the supported keyboard-plugin disable path only when the current session is responsive and safe.
