import sys
import json
import struct
import subprocess
import os
import winreg
import urllib.parse


class EdgeLauncher:
    def __init__(self):
        self.edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]

    def get_edge_path(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe") as key:
                return winreg.QueryValue(key, None)
        except WindowsError:
            for path in self.edge_paths:
                if os.path.exists(path):
                    return path
        return None

    def validate_url(self, url):
        try:
            parsed = urllib.parse.urlparse(url)
            return all([parsed.scheme in ['http', 'https'], parsed.netloc])
        except Exception:
            return False

    def send_response(self, success, message=None):
        response = {'success': success}
        if message:
            response['message'] = message
        encoded = json.dumps(response).encode('utf-8')
        sys.stdout.buffer.write(struct.pack('@I', len(encoded)))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()

    def handle_message(self, message):
        url = message.get('url')
        if url == 'test':
            self.send_response(True, "Test successful")
            return
        if not self.validate_url(url):
            self.send_response(False, "Invalid URL")
            return
        edge_path = self.get_edge_path()
        if edge_path:
            subprocess.Popen([edge_path, url], creationflags=subprocess.CREATE_NO_WINDOW, start_new_session=True)
            self.send_response(True, "Edge launched successfully")
        else:
            self.send_response(False, "Edge not found")

    def run(self):
        length = struct.unpack('@I', sys.stdin.buffer.read(4))[0]
        message = json.loads(sys.stdin.buffer.read(length).decode('utf-8'))
        self.handle_message(message)


if __name__ == "__main__":
    EdgeLauncher().run()
