import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QGridLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.history = []

    def initUI(self):
        self.setWindowTitle("Prakash's Calculator")
        self.setStyleSheet("""
            QWidget {
                background-color: #22252e;
                color: white;
            }
            QPushButton {
                background-color: #292d36;
                border: none;
                border-radius: 24px;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton:pressed {
                background-color: #393e4a;
            }
        """)
        self.setFixedSize(360, 640)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Display
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            background-color: #22252e;
            border: none;
            font-size: 48px;
            padding: 20px;
            margin-bottom: 20px;
        """)
        layout.addWidget(self.display)

        # Buttons
        grid_layout = QGridLayout()
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('x²', 1, 0), ('√x', 1, 1), ('log', 1, 2), ('×', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('-', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('+', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('=', 4, 3, 2, 1),
            ('0', 5, 0, 1, 2), ('.', 5, 2)
        ]

        for btn_text, row, col, *span in buttons:
            btn = QPushButton(btn_text)
            btn.setFixedSize(80, 80)
            if btn_text in '0123456789.':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #292d36;
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: #393e4a;
                    }
                """)
            elif btn_text in '+-×÷=':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f69906;
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: #ffa726;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #272b33;
                        color: #26f3d0;
                    }
                    QPushButton:pressed {
                        background-color: #373d47;
                    }
                """)
            btn.clicked.connect(self.buttonClicked)
            if len(span) == 2:
                grid_layout.addWidget(btn, row, col, span[0], span[1])
            else:
                grid_layout.addWidget(btn, row, col)

        layout.addLayout(grid_layout)

        # History button
        history_btn = QPushButton('History')
        history_btn.setFixedSize(120, 40)
        history_btn.setStyleSheet("""
            QPushButton {
                background-color: #f69906;
                color: white;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:pressed {
                background-color: #ffa726;
            }
        """)
        history_btn.clicked.connect(self.showHistory)
        layout.addWidget(history_btn, alignment=Qt.AlignCenter)

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '=':
            try:
                result = eval(self.display.text().replace('×', '*').replace('÷', '/'))
                self.history.append(f"{self.display.text()} = {result}")
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == 'C':
            self.display.setText('0')
        elif key == '±':
            current = self.display.text()
            self.display.setText(str(-float(current)) if float(current) != 0 else '0')
        elif key == '%':
            current = float(self.display.text())
            self.display.setText(str(current / 100))
        elif key == 'x²':
            current = float(self.display.text())
            result = current ** 2
            self.history.append(f"{current}² = {result}")
            self.display.setText(str(result))
        elif key == '√x':
            current = float(self.display.text())
            if current >= 0:
                result = math.sqrt(current)
                self.history.append(f"√{current} = {result}")
                self.display.setText(str(result))
            else:
                self.display.setText('Error')
        elif key == 'log':
            current = float(self.display.text())
            if current > 0:
                result = math.log10(current)
                self.history.append(f"log({current}) = {result}")
                self.display.setText(str(result))
            else:
                self.display.setText('Error')
        else:
            if self.display.text() == '0':
                self.display.setText(key)
            else:
                self.display.setText(self.display.text() + key)

    def showHistory(self):
        history_window = QListWidget()
        history_window.setWindowTitle("Calculation History")
        history_window.addItems(self.history)
        history_window.setStyleSheet("""
            background-color: #22252e;
            color: white;
            font-size: 16px;
        """)
        history_window.setMinimumSize(300, 400)
        history_window.show()
        self.history_window = history_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())