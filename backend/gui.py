import sys
import time
from typing import Dict
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QFrame,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtCore import QThread, pyqtSignal

from main import main
from utils.debug import debug

test_dict = {
    0: [(1, 31), (2, 30)],
    1: [(3, 8)],
    2: [(9, 18), (14, 17)],
    3: [(30, 28)],
    4: [(24, 21)]
}

class GenerateScheduleWorker(QThread):
    update_status = pyqtSignal(str)
    finished = pyqtSignal(dict)

    def run(self):
        # Simulate a long-running task
        self.update_status.emit("Solving...")
        # results = main()
        results = test_dict
        # time.sleep(3)
        self.update_status.emit("")
        self.finished.emit(results)


class ToggleFrame(QFrame):
    def __init__(self, text, week, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.text_label = QLabel(str(text))
        self.text_label.setWordWrap(True)
        self.text_label.hide()
        self.week = week

        self.toggle_button = QPushButton(f"Week {self.week}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_text)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def toggle_text(self):
        if self.toggle_button.isChecked():
            self.text_label.show()
            # self.toggle_button.setText(f"Week {self.week}")
        else:
            self.text_label.hide()
            # self.toggle_button.setText(f"Week {self.week}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NFL Matchups and Schedules")
        self.setGeometry(100, 100, 800, 600)  # Increase the size of the window

        self.main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        # Title
        title_label = QLabel("NFL Schedule by Week")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        top_layout.addWidget(title_label)

        # "Generate Schedule" button
        self.generate_button = QPushButton("Generate Schedule")
        self.generate_button.clicked.connect(self.generate_schedule)
        top_layout.addStretch()  # Push the button to the right
        top_layout.addWidget(self.generate_button)

        self.loading_label = QLabel("")  # Placeholder for "Loading..." text
        top_layout.addWidget(self.loading_label)
        self.main_layout.addLayout(top_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # Label for no matchups
        self.no_matchups_label = QLabel("No Matchups Generated")
        self.no_matchups_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.no_matchups_label)

        # # Add toggles with hidden text
        # texts = [
        #     "This is the first text to be shown when the first toggle is clicked.",
        #     "This is the second text to be shown when the second toggle is clicked.",
        #     "This is the third text to be shown when the third toggle is clicked.",
        #     # Add more text entries as needed
        # ]

        # for i in range(len(texts)):
        #     text = texts[i]
        #     toggle_frame = ToggleFrame(text, week=i+1)
        #     self.scroll_layout.addWidget(toggle_frame)

        # Add stretch to ensure alignment at the top
        self.scroll_layout.addStretch(1)

    def generate_schedule(self):
        self.generate_button.setEnabled(False)  # Disable button to prevent multiple clicks

        self.worker = GenerateScheduleWorker()
        self.worker.update_status.connect(self.loading_label.setText)
        self.worker.finished.connect(self.on_generation_complete)
        self.worker.start()

    def on_generation_complete(self, matchups: Dict):
        # Remove the "No Matchups Generated" label
        self.no_matchups_label.hide()

        # Add the toggles with the generated matchups
        for i, matchup in matchups.items():
            debug(matchup)
            debug(i)
            toggle_frame = ToggleFrame(matchup, week=i+1)
            self.scroll_layout.addWidget(toggle_frame)

        self.generate_button.setEnabled(True)  # Re-enable the button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Application interrupted by user, exiting.")
        sys.exit(0)
