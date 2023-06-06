#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ethan Lindahl"
__version__ = "0.1.0"
__license__ = "Private"


import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from question_creator import QuestionCreator
from trivia_dashboard import *




class MainWindow(QMainWindow):
    def __init__(self, rules):
        super().__init__()
        self.rules = rules
        self.start_page()
        self.question_creator = QuestionCreator()
        self.new_dash = GameDashboard(self.rules)

    def start_page(self):
        self.setFixedSize(300, 500)
        self.setWindowTitle('Trivia 2023')
        start_widget = QWidget()
        self.start_layout = QVBoxLayout()
        label = QLabel('Trivia 2023 Edition')
        label.setFixedSize(300, 100)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton('Start New Game')
        self.start_button.clicked.connect(self.initialize_game_engine)
        question_creator = QPushButton('Open Question Creator')
        question_creator.clicked.connect(self.question_creator)
        self.start_layout.addWidget(label)
        self.start_layout.addWidget(self.start_button)
        self.start_layout.addWidget(question_creator)
        start_widget.setLayout(self.start_layout)
        self.setCentralWidget(start_widget)

    def initialize_game_engine(self):  # gives function to buttons within the game dashboard
        self.start_button.setText('Open Existing Game')
        self.new_dash.show()
        

    def load_data(self):  # load questions and saved team information from database here
        pass

    def question_creator(self):
        self.question_creator.show()



if __name__ == '__main__':
    rules = ['Be Nice', 'Have Fun', 'No Phones', '1', '2', '3', '4', '6', '7', ]

    app = QApplication(sys.argv)

    window = MainWindow(rules)
    window.show()

    app.exec()
