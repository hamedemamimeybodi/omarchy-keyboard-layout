"""Run only a newly compiled daemon against disposable private UNIX sockets."""
import json
import os
from pathlib import Path
import select
import socket
import subprocess
import sys
import threading
import tempfile
import time

temporary = tempfile.TemporaryDirectory(prefix='keyboard-ipc-')
root = Path(temporary.name)
signature = 'test-' + root.name
socket_dir = root / 'hypr' / signature
socket_dir.mkdir(parents=True, mode=0o700)
state = {'window': '0xa', 'layout': 0, 'queries': 0, 'switches': []}
stop = threading.Event()
control = socket.socket(socket.AF_UNIX)
control.bind(str(socket_dir / '.socket.sock'))
control.listen()
control.settimeout(0.1)
event_server = socket.socket(socket.AF_UNIX)
event_server.bind(str(socket_dir / '.socket2.sock'))
event_server.listen()
event_server.settimeout(5)


def serve():
    while not stop.is_set():
        try:
            conn, _ = control.accept()
        except TimeoutError:
            continue
        with conn:
            conn.settimeout(2)
            chunks = []
            while part := conn.recv(1024):
                chunks.append(part)
            request = b''.join(chunks).decode()
            state['queries'] += 1
            if request == 'j/activewindow':
                response = json.dumps({'address': state['window']}).encode()
            elif request == 'j/devices':
                response = json.dumps({'keyboards': [dict(name='physical-keyboard', main=True,
                    active_layout_index=state['layout'], layout='us,ir')]}).encode()
            elif request.startswith('/switchxkblayout all '):
                state['layout'] = int(request.rsplit(' ', 1)[1])
                state['switches'].append(state['layout'])
                response = b'ok'
            else:
                response = b'invalid'
            conn.sendall(response)


def wait_for(predicate, label):
    deadline = time.monotonic() + 4
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError(label)


thread = threading.Thread(target=serve, daemon=True)
thread.start()
env = dict(os.environ, XDG_RUNTIME_DIR=str(root), HYPRLAND_INSTANCE_SIGNATURE=signature)
process = subprocess.Popen([sys.argv[1]], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
events = None
checks = []
try:
    events, _ = event_server.accept()
    wait_for(lambda: state['queries'] >= 2, 'startup state queries')
    checks.append('startup_private_socket_sync')

    def layout(index):
        before = state['queries']
        state['layout'] = index
        events.sendall(b'activelayout>>physical-keyboard,fixture\n')
        wait_for(lambda: state['queries'] > before, 'layout observation query')

    def focus(address):
        state['window'] = address
        events.sendall(('activewindowv2>>' + address + '\n').encode())

    layout(1)  # Window A remembers Persian.
    focus('0xb')
    layout(0)  # Window B remembers English.
    focus('0xa')
    wait_for(lambda: state['switches'] == [1], 'A restores Persian')
    focus('0xb')
    wait_for(lambda: state['switches'] == [1, 0], 'B restores English')
    checks.append('us_ir_independent_A_B_window_layouts')

    focus('0xa')
    wait_for(lambda: state['switches'] == [1, 0, 1], 'A restores before reuse')
    events.sendall(b'closewindow>>0xb\n')
    focus('0xb')
    layout(1)  # Wait for preceding close/focus processing.
    assert state['switches'] == [1, 0, 1]
    checks.append('closed_window_address_reuse_forgets_old_layout')

    focus('')
    layout(0)
    focus('0xa')
    wait_for(lambda: state['switches'] == [1, 0, 1, 1], 'unfocused change not assigned to A')
    checks.append('unfocused_layout_not_attributed')

    before = state['queries']
    events.sendall(b'configreloaded>>\n')
    wait_for(lambda: state['queries'] >= before + 2, 'reload resets state')
    focus('0xb')
    layout(1)
    assert len(state['switches']) == 4
    checks.append('configuration_reload_forgets_stale_layouts')

    events.sendall(b'x' * 5000 + b'\nmalformed-event\nactivewind')
    events.sendall(b'owv2>>0xa\n')
    layout(0)
    focus('0xb')
    wait_for(lambda: state['switches'][-1] == 1 and len(state['switches']) == 5,
             'fragmented valid event after oversized line')
    checks.append('oversized_malformed_and_fragmented_event_recovery')

    events.close()
    state.update(window='0xa', layout=0)
    before = state['queries']
    events, _ = event_server.accept()
    wait_for(lambda: state['queries'] >= before + 2, 'socket reconnect resynchronizes')
    focus('0xb')
    layout(0)
    assert len(state['switches']) == 5
    checks.append('event_socket_reconnect_resynchronizes_memory')
finally:
    process.terminate()  # Only this test child; no host daemon or shell process is targeted.
    if events is not None:
        events.close()
    stdout, stderr = process.communicate(timeout=4)
    stop.set()
    thread.join(timeout=1)
    event_server.close()
    control.close()
    temporary.cleanup()

assert process.returncode == 0, stderr
assert stdout.count('restore:') == 5, stdout
print(json.dumps(dict(status='PASS', checks=checks, daemon_stdout=stdout,
                      daemon_stderr=stderr, switches=state['switches'],
                      scope='Private fake UNIX sockets only; rebuilt daemon; no host IPC'), indent=2))
