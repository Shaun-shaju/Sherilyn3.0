import sys
import os
import subprocess
import time
import requests
import webbrowser
import logging
from PyQt6 import QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

# 🔥 Fix PyQt6 GPU issues

# 🔹 Log directory in %APPDATA%
LOG_DIR = os.path.join(os.environ.get("APPDATA", os.getcwd()), "Sherilyn3")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 🔹 Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def is_streamlit_running():
    """Check if Streamlit is already running."""
    try:
        response = requests.get("http://localhost:8501")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('cache/logo.png'))
        self.setWindowTitle("Sherilyn 3.0 by S. Shaun Benedict")
        self.setGeometry(100, 100, 1200, 800)

        self.streamlit_process = None
        if not is_streamlit_running():
            logging.info("Starting Streamlit...")
            self.streamlit_process = subprocess.Popen(
                ["streamlit", "run", "app.py", "--server.headless", "true"], shell=True
            )
            time.sleep(7)  # Give Streamlit time to start

        # 🔹 Try to embed Streamlit
        self.browser = QWebEngineView()
        try:
            self.browser.setUrl(QUrl("http://localhost:8501"))
            logging.info("Streamlit embedded successfully.")
        except Exception as e:
            logging.error(f"Failed to embed Streamlit: {e}")
            webbrowser.open("http://localhost:8501")

        # 🔹 Set layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        """Stop Streamlit when closing the app."""
        if self.streamlit_process:
            logging.info("Stopping Streamlit...")
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
            logging.info("Streamlit stopped.")
        event.accept()

# 🔹 Run PyQt6 application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
