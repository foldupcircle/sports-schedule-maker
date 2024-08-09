import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
    QStackedWidget, QScrollArea, QGroupBox, QGridLayout, QToolButton, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NFL Matchups and Schedules")
        self.setGeometry(100, 100, 800, 600)  # Increase the size of the window

        # Main Layout
        main_layout = QVBoxLayout()

        # Stacked Widget for Multiple Views
        self.stacked_widget = QStackedWidget()

        # Matchups View
        self.matchups_view = self.create_matchups_view()
        self.stacked_widget.addWidget(self.matchups_view)

        # Team Schedule View
        self.schedule_view = self.create_schedule_view()
        self.stacked_widget.addWidget(self.schedule_view)

        # Add stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        matchups_button = QPushButton("View Matchups")
        matchups_button.clicked.connect(self.show_matchups_view)
        schedule_button = QPushButton("View Schedule")
        schedule_button.clicked.connect(self.show_schedule_view)
        
        nav_layout.addWidget(matchups_button)
        nav_layout.addWidget(schedule_button)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)

    def create_matchups_view(self):
        # Matchups View Widget
        widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("NFL Schedule by Week")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Layout for toggles
        toggles_layout = QVBoxLayout()

        # Scrollable area for matchups
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(400)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        # Example matchups for each week (replace with actual matchups and logos)
        weeks_matchups = {
            "Week 1": [("Team A", "Team B", "team_a_logo.png", "team_b_logo.png"),
                       ("Team C", "Team D", "team_c_logo.png", "team_d_logo.png")],
            "Week 2": [("Team E", "Team F", "team_e_logo.png", "team_f_logo.png"),
                       ("Team G", "Team H", "team_g_logo.png", "team_h_logo.png")],
            # Add more weeks and matchups as needed
        }

        for week, matchups in weeks_matchups.items():
            # Create a collapsible group box for each week
            toggle_button = QToolButton()
            toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            toggle_button.setText(week)
            toggle_button.setCheckable(True)
            toggle_button.setChecked(False)
            toggle_button.setArrowType(Qt.ArrowType.RightArrow)
            toggle_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            toggle_button.clicked.connect(lambda checked, btn=toggle_button: self.toggle_group_box(btn))

            # Create a group box for the matchups
            group_box = QGroupBox()
            group_box.setVisible(False)  # Start collapsed
            group_layout = QGridLayout()

            for i, (team1, team2, logo1, logo2) in enumerate(matchups):
                matchup_layout = QHBoxLayout()

                # Team 1 logo
                logo1_label = QLabel()
                if QPixmap(logo1).isNull():
                    logo1_label.setText(f"{team1} Logo")
                else:
                    logo1_pixmap = QPixmap(logo1).scaled(50, 50)
                    logo1_label.setPixmap(logo1_pixmap)
                matchup_layout.addWidget(logo1_label)

                # Matchup label
                matchup_label = QLabel(f"{team1} vs {team2}")
                matchup_layout.addWidget(matchup_label)

                # Team 2 logo
                logo2_label = QLabel()
                if QPixmap(logo2).isNull():
                    logo2_label.setText(f"{team2} Logo")
                else:
                    logo2_pixmap = QPixmap(logo2).scaled(50, 50)
                    logo2_label.setPixmap(logo2_pixmap)
                matchup_layout.addWidget(logo2_label)

                group_layout.addLayout(matchup_layout)

            group_box.setLayout(group_layout)

            toggles_layout.addWidget(toggle_button)
            scroll_layout.addWidget(group_box)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addLayout(toggles_layout)
        main_layout.addWidget(scroll_area)

        widget.setLayout(main_layout)

        return widget

    def toggle_group_box(self, button):
        # Find the corresponding group box
        group_box = button.nextInFocusChain()
        if button.isChecked():
            button.setArrowType(Qt.ArrowType.DownArrow)
            group_box.setVisible(True)
        else:
            button.setArrowType(Qt.ArrowType.RightArrow)
            group_box.setVisible(False)

    def create_schedule_view(self):
        # Schedule View Widget
        widget = QWidget()
        layout = QVBoxLayout()

        # Example team schedule (replace with actual data)
        team_schedule = {
            "Week 1": "Opponent A",
            "Week 2": "Opponent B",
            "Week 3": "Opponent C"
        }

        # Add a list of games to the layout
        for week, opponent in team_schedule.items():
            label = QLabel(f"{week}: {opponent}")
            layout.addWidget(label)

        widget.setLayout(layout)
        return widget

    def show_matchups_view(self):
        self.stacked_widget.setCurrentWidget(self.matchups_view)

    def show_schedule_view(self):
        self.stacked_widget.setCurrentWidget(self.schedule_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
