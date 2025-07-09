import os
import sys
import subprocess
import webbrowser
import time
import threading
import socket


def wait_for_server(host, port, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.5)
    return False


def open_browser():
    if wait_for_server("localhost", 8501, timeout=15):
        webbrowser.open_new("http://localhost:8501")
    else:
        print("Streamlit server did not start in time. No browser opened.")


if __name__ == "__main__":
    script_path = os.path.join("scripts", "roi_calculator_app.py")
    browser_thread = None
    try:
        # Only open the browser if running as a PyInstaller executable
        if getattr(sys, 'frozen', False):
            browser_thread = threading.Thread(target=open_browser, daemon=True)
            browser_thread.start()
            # Find the embedded python.exe in the one-folder build
            exe_dir = os.path.dirname(sys.executable)
            python_exe = os.path.join(exe_dir, 'python.exe')
            if not os.path.exists(python_exe):
                print("ERROR: Embedded python.exe not found in one-folder build.")
                sys.exit(1)
            cmd = [python_exe, "-m", "streamlit", "run", script_path, "--server.headless", "true"]
        else:
            cmd = [sys.executable, "-m", "streamlit", "run", script_path, "--server.headless", "true"]
        print("Launching Streamlit with command:", cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # Print output in real time
        for line in proc.stdout:
            print(line, end="")
        proc.wait()
    except KeyboardInterrupt:
        print("Exiting gracefully.")
        sys.exit(0)
