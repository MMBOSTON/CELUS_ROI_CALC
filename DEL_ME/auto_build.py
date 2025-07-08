import time
import subprocess
import os
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FILES = ["roi_calculator_app.py", "run_app.py"]
EXE_PATH = os.path.join("dist", "run_app.exe")

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.proc = None
        self.build_and_run()

    def build_and_run(self):
        print("Building .exe...")
        subprocess.run([
            "pyinstaller", "--onefile", "--add-data",
            "roi_calculator_app.py;.", "run_app.py"
        ])
        print("Build complete. Starting .exe...")
        if self.proc and self.proc.poll() is None:
            print("Killing previous instance...")
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = subprocess.Popen([EXE_PATH])

    def on_modified(self, event):
        if any(event.src_path.endswith(f) for f in WATCHED_FILES):
            print(f"Detected change in {event.src_path}, rebuilding and restarting .exe...")
            self.build_and_run()

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    print("Watching for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        observer.stop()
        if event_handler.proc and event_handler.proc.poll() is None:
            event_handler.proc.terminate()
    observer.join()
