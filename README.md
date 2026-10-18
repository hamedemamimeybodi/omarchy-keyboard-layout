# Keyboard Layout Pulse

A compatibility restoration of [omarchy-QOL/omarchy-keyboard-layout](https://github.com/omarchy-QOL/omarchy-keyboard-layout), preserving its Git ancestry, plugin identity and original features. Original plugin by **Ilya Zarubin (ilyaZar)**; native component derived from **Liran Shternberg's hypr-type-flow-C**. This is a community fork, without official Omarchy endorsement.

![Original upstream keyboard menu and settings](preview.png)

The widget shows configured layouts and variants, provides a picker and scroll navigation, offers configurable pulse animation/colors, and optionally remembers a layout for each window. Existing inline preferences and shortcut display remain supported. It does not rewrite your Hyprland keyboard configuration or install a system service.

## Compatibility restoration

- Qualify the Commons color singleton to avoid the Qt 6.12 `Color` name collision.
- Make twenty QML scope references explicit without removing settings or visual behavior.
- Align native keyboard filtering with the widget for laptop extra-button and WMI-hotkey devices.
- Preserve the original `io.github.ilyazar.keyboard-layout` ID and version `0.2.3`; identify this restoration by its Git commit, not an invented upstream release number.

See [installation and safe fallback](docs/installation.md), [troubleshooting](docs/troubleshooting.md), [compatibility](docs/compatibility.md), [technical report](docs/restoration-report.md), [testing](docs/testing.md), and [changelog](CHANGELOG.md).

## Reported acceptance

The operator reported PASS for rendering, US/Persian switching with Alt+Shift, independent layouts per window, closing/reopening windows, and repeated switching stability. Seven private fake-socket IPC scenarios also passed in the restoration work. These reports are narrower than independent verification of every platform or lifecycle branch. Live rollback and live daemon reconnection have **not** been independently tested.

The retained lint diagnostics were classified as generic QtObject typing limitations and two style diagnostics; no confirmed runtime defect was found in that set. This does not guarantee the absence of runtime defects.

## Build and test

From this checkout, with a C compiler, Make, pkg-config, json-c development files, Node.js and Python 3:

```bash
make -C native clean all build/test_hypr_ipc build/test_layout_memory
native/build/test_hypr_ipc
native/build/test_layout_memory
node tests/layout-state.test.mjs
python3 tests/private_ipc_integration.py native/keyboard-layoutd
```

The integration fixture creates private sockets and controls only its freshly compiled child. It never targets a running Hyprland instance. CI covers these checks; a successful CI result is not GUI acceptance.

## License and credits

[MIT](LICENSE), copyright 2026 Ilya Zarubin. The native port preserves its separate [MIT notice](native/LICENSE), copyright 2025 liran, and upstream source attribution in [native/README.md](native/README.md). Changes in this restoration are provided under those applicable MIT terms. Keep both notices when redistributing. Original visual assets and upstream commit authorship remain credited. See [contribution guidance](CONTRIBUTING.md).
