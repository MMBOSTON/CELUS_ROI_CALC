# launch_app.py
import sys
import subprocess
import threading
import time
import webbrowser
import os
import shutil
import tempfile


# PyInstaller compatibility: find the correct base directory for bundled data
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Always use the absolute path to the app file, so it works from any folder or after packaging
src_app_path = os.path.join(BASE_DIR, "roi_calculator_app.py")
temp_dir = tempfile.gettempdir()
APP_FILENAME = os.path.join(temp_dir, "roi_calculator_app_extracted.py")
shutil.copyfile(src_app_path, APP_FILENAME)
PORT = 8501

# Update all file paths to use 'Template/ROI Calculator_v1.xlsx' or similar, instead of just the filename.
TEMPLATE_DIR = os.path.join(BASE_DIR, 'Template')
ROI_CALCULATOR_TEMPLATE = os.path.join(TEMPLATE_DIR, 'ROI Calculator_v1.xlsx')

# Function to open the browser after a short delay
def open_browser():
    url = f"http://localhost:{PORT}"
    for _ in range(20):  # Try for up to 10 seconds
        time.sleep(0.5)
        try:
            import socket
            with socket.create_connection(("localhost", PORT), timeout=0.5):
                webbrowser.open(url)
                return
        except Exception:
            continue

def run_streamlit():
    # Try running 'streamlit run ...' directly
    cmd = ["streamlit", "run", APP_FILENAME, "--server.port", str(PORT), "--server.headless", "true"]
    print(f"Launching Streamlit app with: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        threading.Thread(target=open_browser, daemon=True).start()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line, end='')
        proc.wait()
        return proc.returncode
    except FileNotFoundError:
        print("\n--- 'streamlit' command not found. Trying 'python -m streamlit'... ---\n")
        return None

def run_streamlit_module():
    # Fallback: Try running 'python -m streamlit run ...'
    python_exe = sys.executable
    cmd = [python_exe, '-m', 'streamlit', 'run', APP_FILENAME, '--server.port', str(PORT), '--server.headless', 'true']
    print(f"Launching Streamlit app with: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        threading.Thread(target=open_browser, daemon=True).start()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line, end='')
        proc.wait()
        return proc.returncode
    except Exception as e:
        print("\n--- Failed to launch Streamlit via python -m streamlit ---\n")
        import traceback
        traceback.print_exc()
        return -1

try:
    code = run_streamlit()
    if code is None:
        code = run_streamlit_module()
    if code != 0:
        print(f"\n--- Streamlit exited with code {code} ---\n")
    else:
        print("\nApp finished without fatal error.")
except Exception as e:
    print("\n--- Exception occurred ---")
    import traceback
    traceback.print_exc()
    print("\n--- End of exception ---\n")
finally:
    try:
        input("Press Enter to exit...")
    except Exception:
        time.sleep(10)