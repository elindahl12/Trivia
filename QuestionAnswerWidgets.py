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
from datetime import datetime
import random

class RoundScreen(QWidget):
    def __init__(self, round):
        super().__init__()
        layout = QVBoxLayout()
        self.round = round
        self.round_label = QLabel(f'Round {self.round}')
        layout.addWidget(self.round_label, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def final_round(self):
        self.round_label.setText('Final Round')

class WagerRules(QWidget):
    def __init__(self):
        super().__init__()
        wager_rules = ['- You are able to wager any amount of points you currently have for the round',
                        '- You cannot change your submission or your team\'s wager amount once you submit your answer. ',
                        '- You are not required to answer.',
                        ]
        
        self.layout = QVBoxLayout()
        self.title = QLabel('Wager Question')
        self.title.setFixedHeight(75)
        self.layout.addWidget(self.title, 1, Qt.AlignmentFlag.AlignHCenter)
        for rule in wager_rules:
            self.rule = QLabel(rule)
            self.rule.setWordWrap(True)
            self.layout.addWidget(self.rule)
        self.setLayout(self.layout)


class MultipleChoiceQuestion(QWidget):
    def __init__(self, question, correct_answer, distractor1, distractor2, distractor3, minutes, seconds):
        super().__init__()
        answer_list = [correct_answer, distractor1, distractor2, distractor3]
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 10px;
                                        font: 30px;
                                        }
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        }''')
        self.timer = Timer(minutes, seconds)
        main_layout = QGridLayout()
        self.question = QLabel(str(question))
        self.question.setWordWrap(True)
        main_layout.addWidget(self.question, 0, 0, 1, 2)
        self.a = QLabel(f'A. {answer_list[0]}')
        main_layout.addWidget(self.a, 1, 0, 1, 1)
        self.c = QLabel(f'C. {answer_list[1]}')
        main_layout.addWidget(self.c, 1, 1, 1, 1)
        self.b = QLabel(f'B. {answer_list[2]}')
        main_layout.addWidget(self.b, 2, 0, 1, 1)
        self.d = QLabel(f'D. {answer_list[3]}')
        main_layout.addWidget(self.d, 2, 1, 1, 1)
        main_layout.addWidget(self.timer, 3, 0, 1, 2)
        self.setLayout(main_layout)

class MultipleChoiceQuestion2(QWidget):
    def __init__(self, question, correct_answer, distractor1, distractor2, distractor3, minutes, seconds):
        super().__init__()
        self.correct = correct_answer
        answer_list = [correct_answer, distractor1, distractor2, distractor3]
        random.shuffle(answer_list)
        print(correct_answer)
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget {    background-color: darkblue;
                                            padding: 5px;
                                            font: 30px;
                                        }
                            ''')
        self.timer = Timer(minutes, seconds)
        main_layout = QGridLayout()
        self.question = QLabel(str(question))
        self.question.setStyleSheet('''background-color: lightgrey;
                                        border-radius: 5px;
                                        margin: 30%;
                                        ''')
        self.question.setWordWrap(True)
        main_layout.addWidget(self.question, 0, 0, 1, 1)

        self.answer_widget = QWidget()
        self.answer_widget.setStyleSheet('''background-color: lightgrey;
                                                border-radius: 5px;
                                                font: 40px;
                                                padding: 5px;
                                                margin: 30%;''')
        self.answer_layout = QGridLayout()
        self.answer_widget.setLayout(self.answer_layout)
        self.a = QLabel(f'A. {answer_list[0]}')
        self.answer_layout.addWidget(self.a, 0, 0, 1, 1)
        self.c = QLabel(f'C. {answer_list[1]}')
        self.answer_layout.addWidget(self.c, 0, 1, 1, 1)
        self.b = QLabel(f'B. {answer_list[2]}')
        self.answer_layout.addWidget(self.b, 1, 0, 1, 1)
        self.d = QLabel(f'D. {answer_list[3]}')
        self.answer_layout.addWidget(self.d, 1, 1, 1, 1)

        main_layout.addWidget(self.answer_widget, 1, 0, 1, 1)
        main_layout.addWidget(self.timer, 2, 0, 1, 1)
        self.setLayout(main_layout)

class MultipleChoiceAnswer(QWidget):
    def __init__(self, question, correct_answer):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 5px; 
                                        font: 30px;}
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        margin: 20%;
                                        }''')
        main_layout = QGridLayout()
        self.question = QLabel(str(question))
        self.question.setWordWrap(True)
        main_layout.addWidget(self.question, 0, 0, 1, 2)
        self.a = QLabel(str(correct_answer))
        main_layout.addWidget(self.a, 1, 0, 1, 1)
        self.c = QLabel(str(''))
        main_layout.addWidget(self.c, 1, 1, 1, 1)
        self.b = QLabel(str(''))
        main_layout.addWidget(self.b, 2, 0, 1, 1)
        self.d = QLabel(str(''))
        main_layout.addWidget(self.d, 2, 1, 1, 1)
        self.setLayout(main_layout)

class TrueFalseQuestion(QWidget):
    def __init__(self, question, minutes, seconds):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 5px;
                                        font: 30px;}
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        
                                        }''')
        self.timer = Timer(minutes, seconds)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel('True or False: \n' + question)
        self.question.setWordWrap(True)
        
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.timer)
        
        
        
        self.setLayout(main_layout)

class TrueFalseAnswer(QWidget):
    def __init__(self, question, answer):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 5px;
                                        font: 30px;}
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        margin: 20%;
                                        }''')
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel('True or False: '+ question)
        self.question.setWordWrap(True)
        self.answer = QLabel(answer)
        self.answer.setWordWrap(True)
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.answer)
        
        
        self.setLayout(main_layout)

class FillInBlankQuestion(QWidget):
    def __init__(self, question, minutes, seconds):
        super().__init__()
        self.question = question
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 5px;
                                        font: 30px;}
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        
                                        }''')
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'Fill in the Blank: {self.question}')
        self.question.setWordWrap(True)
        self.timer = Timer(minutes, seconds)
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.timer)
        
        
        self.setLayout(main_layout)

class FillInBlankAnswer(QWidget):
    def __init__(self, question, answer):
        super().__init__()
        self.question = question
        self.answer = answer
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(''' QWidget { background-color: darkblue;
                                        padding: 5px;
                                        font: 30px;}
                                QLabel { background-color: lightgrey;
                                        border-radius: 5px;
                                        
                                        }''')
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'Fill in the Blank: {self.question}')
        self.question.setWordWrap(True)
        self.answer = QLabel(f'{self.answer}')
        self.answer.setWordWrap(True)
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.answer)
        
        
        self.setLayout(main_layout)

class Rules(QWidget):
    def __init__(self, rule_list):
        super().__init__()
        self.rules = rule_list
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        main_layout = QVBoxLayout()
        self.title = QLabel('Rules of the Game')
    
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(75)
        main_layout.addWidget(self.title)
        num = 1
        for rule in self.rules:
            self.rule = QLabel(f"{num}. {rule}")
            self.rule.setWordWrap(True)
            main_layout.addWidget(self.rule)
            num = num + 1
        
        
        self.setLayout(main_layout)

class Leaderboard(QWidget):
    def __init__(self, teams):
        super().__init__()
        self.teams = teams

        self.layout = QVBoxLayout()
        self.leader_label = QLabel('Leaderboard')
        self.leader_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.leader_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.header_layout = QHBoxLayout()
        self.team_label = QLabel('Team Name')
        self.header_layout.addWidget(self.team_label)
        
        if len(self.teams) is 0:
            self.leader_label.setText('No Current Teams')
        else:
            
            self.layout.addLayout(self.header_layout)
            self.total_label = QLabel('Score')
            self.header_layout.addWidget(self.total_label, 0, Qt.AlignmentFlag.AlignRight)
            
            self.placement = self.team_score()
            self.layout.addWidget(self.placement, 0, Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.layout)
    
    def team_name_display(self):
        widget = QWidget()
        layout = QVBoxLayout()
        for t in self.teams:
            name = QLabel(t['team'])
            layout.addWidget(name)

        widget.setLayout(layout)
        self.layout.addWidget(widget)
        

    def team_score(self):
        col = 0
        row = 0
        for t in self.teams:
            widget = QWidget()
            layout = QGridLayout()
            widget.setLayout(layout)
            
            name = QLabel(t['team'])
            layout.addWidget(name, row, 0, 1, 1)
            
            col += 1
            score = QLabel(t['total'])
            layout.addWidget(score, row, col, 1, 1, Qt.AlignmentFlag.AlignRight)

            row += 1 
            self.layout.addWidget(widget)

class Timer(QWidget):
    def __init__(self, minute, second):
        super().__init__()
        self.minute = minute
        self.second = second
        self.total_seconds = (self.minute * 60) + self.second
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # create a label to display the timer
        self.label = QLabel(f"{self.minute:02}:{self.second:02}")
        self.label.setMaximumSize(250, 150)
        self.label.setStyleSheet(''' QLabel {   background-color: lightgrey;
                                                border-radius: 5px;
                                                font: 32px;
                                                padding: 5px;
                                                margin: 30%;}

                                ''')
        self.main_layout.addWidget(self.label)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.end_time = QDateTime.currentDateTime().addSecs(self.total_seconds)

        # create a timer and set the interval to 100 milliseconds
        self.timer = QTimer(self)
        self.timer.setInterval(100)

        # connect the timer's timeout signal to the update_timer slot
        self.timer.timeout.connect(self.update_timer)

        self.timer.start()
        
        

    def update_timer(self):
        # get the time remaining until the end time
        remaining_time = QDateTime.currentDateTime().secsTo(self.end_time)
        if remaining_time < 0:
            remaining_time = 0

        # format the remaining time as a string with minutes and seconds
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        current_time = f"{minutes:02}:{seconds:02}"

        # update the label with the current time remaining
        self.label.setText(f"{current_time}")

        if minutes is 0 and seconds <= 10:
            self.label.setStyleSheet('''background-color: lightgrey;
                                        border-radius: 5px;
                                        font: 32px;
                                        padding: 5px;
                                        margin: 30%;
                                        color: red;
                                        
                                     ''')
        if minutes is 0 and seconds is 0:
            self.timer.stop()
            self.label.setText('TIME\'S UP!')

    def start_timer(self):
        self.end_time = QDateTime.currentDateTime().addSecs(self.total_seconds)
        self.timer.start()

    def pause_timer(self):
        self.timer.stop()


if __name__ == '__main__':
    rules = ['Be Nice', 'Have Fun', 'No Phones', '1', '2', '3', '4', '6', '7',]
    teams = ['team1', 'team2', 'team3', 'team4']
    round_scores = [(1 , 3, 5), (1 , 3, 5), (1 , 3, 5), (1 , 3, 5)]
    minutes = 0
    seconds = 15
    app = QApplication(sys.argv)

    window = WagerRules()
    window.show()

    app.exec()