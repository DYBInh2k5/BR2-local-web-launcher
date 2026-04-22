from __future__ import annotations

import ctypes
import json
import subprocess
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent.parent
EXE_PATH = BASE_DIR / "BR2" / "BR2_thichlaviet.com.exe"
INDEX_PATH = Path(__file__).resolve().parent / "index.html"
SITE_URL = "https://thichlaviet.com/"

process: subprocess.Popen | None = None
last_message = "San sang."


def is_running() -> bool:
    return process is not None and process.poll() is None


def status_payload() -> dict[str, object]:
    return {
        "file": str(EXE_PATH),
        "exists": EXE_PATH.exists(),
        "running": is_running(),
        "message": last_message,
        "siteUrl": SITE_URL,
    }


def response_payload(ok: bool) -> dict[str, object]:
    payload = status_payload()
    payload["ok"] = ok
    return payload


def run_as_admin(path: Path) -> int:
    return ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        str(path),
        None,
        str(path.parent),
        1,
    )


class LauncherHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._serve_index()
            return

        if self.path == "/status":
            self._send_json(status_payload())
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        global last_message
        global process

        if self.path != "/run":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        if not EXE_PATH.exists():
            last_message = "Khong tim thay file exe."
            self._send_json(
                response_payload(False)
            )
            return

        if is_running():
            last_message = "File dang chay."
            self._send_json(response_payload(True))
            return

        try:
            process = subprocess.Popen([str(EXE_PATH)], cwd=str(EXE_PATH.parent))
            last_message = "Da chay file exe."
            self._send_json(response_payload(True))
            return
        except OSError as exc:
            if getattr(exc, "winerror", None) == 740:
                result = run_as_admin(EXE_PATH)
                if result > 32:
                    process = None
                    last_message = (
                        "Windows yeu cau quyen admin. Neu hop thoai UAC hien ra, hay bam Yes."
                    )
                    self._send_json(response_payload(True))
                    return

                last_message = f"Khong the mo file voi quyen admin. Ma loi: {result}."
                self._send_json(response_payload(False))
                return

            last_message = f"Loi khi chay file: {exc}."
            self._send_json(response_payload(False))
            return
        except Exception as exc:
            last_message = f"Loi khong xac dinh: {exc}."
            self._send_json(response_payload(False))

    def log_message(self, format: str, *args: object) -> None:
        return

    def _serve_index(self) -> None:
        content = INDEX_PATH.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(
        self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), LauncherHandler)
    print(f"Web launcher dang chay tai http://{HOST}:{PORT}")
    print(f"File target: {EXE_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()
