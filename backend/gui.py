import sys
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
from PyQt6.QtGui import QPixmap

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
        results = test_dict
        # results = main()
        self.update_status.emit("")
        self.finished.emit(results)


class ToggleFrame(QFrame):
    def __init__(self, matchups, week, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.week = week

        # Toggle button to show/hide the matchups
        self.toggle_button = QPushButton(f"Week {self.week}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_text)

        # Layout for the toggle button and the matchups
        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)

        # Card layout to hold all matchups for this week
        self.card_layout = QVBoxLayout()

        # Adding each matchup as a horizontal layout within the card
        for team1, team2 in matchups:
            matchup_layout = QHBoxLayout()

            # Team 1 Logo and Name
            team1_logo = QLabel()
            # Assuming 'team1_logo_path' is the path to the logo image
            team1_logo.setPixmap(QPixmap("team1_logo_path"))
            team1_name = QLabel("Team 1 Name")  # Replace with actual team name

            # Team 2 Logo and Name
            team2_logo = QLabel()
            # Assuming 'team2_logo_path' is the path to the logo image
            team2_logo.setPixmap(QPixmap("team2_logo_path"))
            team2_name = QLabel("Team 2 Name")  # Replace with actual team name

            # Adding widgets to the horizontal layout
            matchup_layout.addWidget(team1_logo)
            matchup_layout.addWidget(team1_name)
            matchup_layout.addWidget(QLabel("@"))  # "@" symbol
            matchup_layout.addWidget(team2_name)
            matchup_layout.addWidget(team2_logo)

            # Add the horizontal layout to the card layout
            self.card_layout.addLayout(matchup_layout)

        # Initially hide the card layout
        self.card_layout.setSpacing(10)
        self.card_layout.setContentsMargins(10, 10, 10, 10)
        self.card_widget = QWidget()
        self.card_widget.setLayout(self.card_layout)
        self.card_widget.hide()

        layout.addWidget(self.card_widget)
        self.setLayout(layout)
    
    def toggle_text(self):
        if self.toggle_button.isChecked():
            self.card_widget.show()
        else:
            self.card_widget.hide()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.generated_matchups_once = False

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

        # Solving... Text
        self.loading_label = QLabel("")  # Placeholder for "Loading..." text
        top_layout.addWidget(self.loading_label)
        self.main_layout.addLayout(top_layout)

        # Scroll Area
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

    def generate_schedule(self):
        self.generate_button.setEnabled(False)  # Disable button to prevent multiple clicks

        self.worker = GenerateScheduleWorker()
        self.worker.update_status.connect(self.loading_label.setText)
        self.worker.finished.connect(self.on_generation_complete)
        self.worker.start()

    def on_generation_complete(self, matchups: Dict):
        # Clear the existing widgets in the scroll_layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Delete the widget
            else:
                self.scroll_layout.removeItem(self.scroll_layout.itemAt(i))  # Remove stretch item

        # Add the toggles with the generated matchups
        for i, matchup in matchups.items():
            toggle_frame = ToggleFrame(matchup, week=i+1)
            self.scroll_layout.addWidget(toggle_frame)
        
        self.scroll_layout.setSpacing(0)  # Adjust space between toggles
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)  # Adjust margins
        # Re-add the stretch to ensure the toggles are top-aligned
        self.scroll_layout.addStretch(1)
        
        # Remove the "No Matchups Generated" label
        try:
            if self.no_matchups_label is not None and self.no_matchups_label.isVisible():
                self.no_matchups_label.hide()
                self.generated_matchups_once = True
        except:
            pass

        self.generate_button.setEnabled(True)  # Re-enable the button


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except:
        sys.exit(1)
