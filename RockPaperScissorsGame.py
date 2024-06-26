import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class RockPaperScissors(QWidget):
    def __init__(self):
        super().__init__()
        self.user_score = 0
        self.computer_score = 0
        self.user_choice = None
        self.computer_choice = None
        self.countdown_timer = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rock Paper Scissors")
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                font-size: 18px;
            }
        """)
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("Rock Paper Scissors")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Countdown timer
        self.timer_label = QLabel("Next round in: 3")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px; margin-bottom: 10px;")
        main_layout.addWidget(self.timer_label)

        # Game area
        game_layout = QHBoxLayout()

        # User side
        user_layout = QVBoxLayout()
        user_label = QLabel("You")
        user_label.setAlignment(Qt.AlignCenter)
        user_layout.addWidget(user_label)

        self.user_image_label = QLabel()
        self.user_image_label.setAlignment(Qt.AlignCenter)
        user_layout.addWidget(self.user_image_label)

        button_layout = QHBoxLayout()
        choices = ['Rock', 'Paper', 'Scissors']
        for choice in choices:
            btn = QPushButton(choice)
            btn.clicked.connect(lambda _, c=choice: self.set_user_choice(c))
            button_layout.addWidget(btn)
        user_layout.addLayout(button_layout)

        game_layout.addLayout(user_layout)

        # VS label
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setStyleSheet("font-size: 48px; font-weight: bold; margin: 0 20px;")
        game_layout.addWidget(vs_label)

        # Computer side
        computer_layout = QVBoxLayout()
        computer_label = QLabel("Computer")
        computer_label.setAlignment(Qt.AlignCenter)
        computer_layout.addWidget(computer_label)

        self.computer_image_label = QLabel()
        self.computer_image_label.setAlignment(Qt.AlignCenter)
        computer_layout.addWidget(self.computer_image_label)

        game_layout.addLayout(computer_layout)

        main_layout.addLayout(game_layout)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px; margin-top: 20px;")
        main_layout.addWidget(self.result_label)

        # Score display
        self.score_label = QLabel("Score - You: 0 | Computer: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("font-size: 20px; margin-top: 10px;")
        main_layout.addWidget(self.score_label)

        # Load images
        self.images = {
            'Rock': QPixmap('rock.png').scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            'Paper': QPixmap('paper.png').scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            'Scissors': QPixmap('scissors.png').scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        }

        self.start_countdown()

    def start_countdown(self):
        self.countdown = 3
        self.timer_label.setText(f"Next round in: {self.countdown}")
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown > 0:
            self.timer_label.setText(f"Next round in: {self.countdown}")
        else:
            self.timer_label.setText("Choose now!")
            self.countdown_timer.stop()

    def set_user_choice(self, choice):
        self.user_choice = choice
        self.user_image_label.setPixmap(self.images[choice])
        self.play_game()

    def play_game(self):
        choices = ['Rock', 'Paper', 'Scissors']
        self.computer_choice = random.choice(choices)

        # Display computer's choice after a delay
        QTimer.singleShot(1000, self.show_computer_choice)

    def show_computer_choice(self):
        self.computer_image_label.setPixmap(self.images[self.computer_choice])
        self.result_label.setText(f"Computer chose {self.computer_choice}")
        
        # Delay before showing the result
        QTimer.singleShot(2000, self.show_result)

    def show_result(self):
        result = self.determine_winner(self.user_choice, self.computer_choice)

        self.result_label.setText(result)

        self.update_score(result)
        self.score_label.setText(f"Score - You: {self.user_score} | Computer: {self.computer_score}")

        # Reset game after 3 seconds
        QTimer.singleShot(3000, self.reset_game)

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (
            (user_choice == 'Rock' and computer_choice == 'Scissors') or
            (user_choice == 'Scissors' and computer_choice == 'Paper') or
            (user_choice == 'Paper' and computer_choice == 'Rock')
        ):
            return "You win!"
        else:
            return "Computer wins!"

    def update_score(self, result):
        if result == "You win!":
            self.user_score += 1
        elif result == "Computer wins!":
            self.computer_score += 1

    def reset_game(self):
        self.user_image_label.clear()
        self.computer_image_label.clear()
        self.result_label.clear()
        self.start_countdown()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissors()
    game.show()
    sys.exit(app.exec_())