# Publication validation status

The native helper was rebuilt in a separate publication checkout. Build and both parser/memory executables passed; the rebuilt executable matched the restoration build. The bundled Node widget model suite passed, and all five QML files parsed with Qt 6.12 qmlformat without modifying source. These syntax checks do not establish imports or GUI behavior.

The adapted public private-IPC test was attempted here, but the execution environment denied UNIX socket binding before the daemon was launched. Its result is BLOCKED_BY_ENVIRONMENT, not PASS. The original private fixture previously passed seven scenarios; that historical result is not substituted for testing the adapted fixture. Run the public test in a disposable environment that permits sockets, or inspect its eventual hosted CI result.

At the preparation checkpoint, GitHub Actions has not run and no remote fork, release or upstream PR has been independently verified. The operator has configured GitHub authentication; the restricted preparation environment still cannot resolve GitHub. The host publication procedure must record actual remote links and CI results. This paragraph is a preparation snapshot, not a statement about subsequent hosted runs.

The operator reported five manual PASS observations on the restored plugin: rendering, US/Persian Alt+Shift switching, per-window independence, closing/reopening windows, and repeated-switch stability. Live rollback and actual daemon reconnection were not independently tested.

A deterministic scan checked every reachable object in the 38-commit upstream history and all proposed publication files for credential signatures, personal absolute paths, machine identifiers and disallowed artifacts. No unresolved pattern findings remain. Seven UUID-like matches were original public GitHub attachment URLs, not machine IDs. Three historical preview images were visually reviewed without finding personal paths, usernames or machine identifiers. This is a bounded scan, not proof that no arbitrary secret could ever exist.
