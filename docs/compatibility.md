# Compatibility matrix

| Component | Reported restoration environment | Coverage |
| --- | --- | --- |
| Omarchy | 4.0.4 | Operator manual GUI acceptance |
| Quickshell | 0.3.2 | Widget/service loaded in deployment receipt |
| Qt | 6.12.0 | Namespace repair; isolated parse/color probes |
| Hyprland | 0.56.2 | US/IR, Alt+Shift and window-memory acceptance reported |
| CPU | x86-64 | Native service support gate preserved |
| Native JSON dependency | json-c 0.19 | Build/parser/memory coverage |
| Layouts | us,ir | Operator report; other layout/variant cases have model tests |

Upstream declares Omarchy >=4.0.0; this restoration does not claim every such version was exercised. Other architectures, mixed keyboard arrangements, alternate bars and future Qt/Hyprland releases require testing. The helper uses control/event UNIX sockets and json-c, rather than a Hyprland C++ plugin ABI. That reduces ABI coupling but does not guarantee compatibility with future IPC changes.

The optional helper starts only when per-window tracking is enabled and architecture support is available. No system service is installed. A shipped binary may require newer libc than the destination machine: rebuild it locally before enabling, as described in installation.md.

Live rollback, actual compositor disconnect/reconnect, and the complete GUI matrix have not been independently tested. Private-socket reconnection tests cover the simulated transport only.
