#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ethan Lindahl"
__version__ = "0.1.0"
__license__ = "Private"


import typing
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtWidgets import *
import sys
from random import shuffle
import sqlite3

from PyQt6.QtWidgets import QWidget

class GameDashboard(QMainWindow):

    def __init__(self, rules):
        super().__init__()
        self.rules = rules
        self.row = 0
        self.col = 0
    #creates variables for the passed args
        self.categories = ['All']
        self.types = []
        self.current_teams = [] 
        #^List of dictionaries -- layout: {'team': '', 'players': '', 'bonus': '', 'r1': '', 'r2': '', 'r3': '', 'r4': '', 'r5': '', 'total': '',}
        #self.question_scores = [] #List of dictionaries -- layout {'team': '', 'q1': '', 'q2': '', 'q3': '', 'q4': '', 'q5': '', 'total': '', }
        self.questions = []
        self.filtered_questions = self.questions
        
    #creates default data for the team information and game builder section
        self.x = ['1', '2', '3', '4', '5']
        self.diff = ['5', '4', '3', '2', '1']
        self.fx = []
        self.min = ['00', '01', '02', '03']
        self.sec = ['00', '15', '30', '45']
        self.filters = {'types': [], 'category': '', 'difficulty': '', }

    #create the toggle counters for the buttons
        self.player_screen = PlayerScreen(self.current_teams, self.rules)
        self.player_screen_toggle = 0
        self.create_game_toggle = 1
        self.start_pause_button_text_toggle = 1
        self.leaderboard_toggle = 1
        self.rules_toggle = 1
        self.round_counter = 1
        self.question_counter = 1
        self.question_index = 0
        self.stage_counter = 1
    #initialize the variables for the game
        self.category_selection = ''
        self.question_type_selection = []
        self.qpr_selection = None
        self.total_round_selection = 3
        self.minute_selection = None
        self.second_selection = None
        self.game_questions = []
        self.total_questions = None
        self.question_index = 0
#customize window attributes
        self.setWindowTitle('Trivia 2023')
        self.move(0, 0)
#load the questions from database
        self.load_questions()
#Create the central widget and main layout
        self.mainwidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainwidget.setLayout(self.mainLayout)
#Add the dashboard label to the main layout
        self.dashboard_label = QLabel('Dashboard')
        self.dashboard_label.setStyleSheet('''font: 40px;''')
        self.mainLayout.addWidget(self.dashboard_label, 0, Qt.AlignmentFlag.AlignHCenter)
#Create the tab widget and add it to the main layout
        self.tabWidget = QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)
#Create the settings tab
        self.settings_tab = QTabWidget()
        self.tab_1_layout = QVBoxLayout()
        self.settings_tab.setLayout(self.tab_1_layout)
        self.team_info_tab = QWidget()
        self.team_info_tab_layout = QGridLayout()
        self.team_info_tab.setLayout(self.team_info_tab_layout)
    #Create team info widget
        self.team_info_widget = QWidget()
        self.team_info_layout = QGridLayout()
        self.team_name_label = QLabel('Team Name: ')
        self.team_info_layout.addWidget(self.team_name_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.team_name = QComboBox()
        self.team_name.setEditable(True)
        self.team_name.setFixedSize(250, 27)
        self.team_name.activated.connect(self.add_team)
        self.team_info_layout.addWidget(self.team_name, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.player_num_label = QLabel('Number of Players: ')
        self.team_info_layout.addWidget(self.player_num_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.player_number = QLineEdit()
        self.player_number.setFixedWidth(40)
        self.player_number.returnPressed.connect(self.add_team)
        self.player_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.team_info_layout.addWidget(self.player_number, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.bonus_pt_label = QLabel('Bonus Points: ')
        self.team_info_layout.addWidget(self.bonus_pt_label, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.bonus_pts = QLineEdit()
        self.bonus_pts.setFixedWidth(40)
        self.bonus_pts.setText('0')
        self.bonus_pts.returnPressed.connect(self.add_team)
        self.bonus_pts.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.team_info_layout.addWidget(self.bonus_pts, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.add_team_button = QPushButton('Add Team')
        self.add_team_button.clicked.connect(self.add_team)
        self.add_team_button.setFixedWidth(100)
        self.team_info_layout.addWidget(self.add_team_button, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.error_label = QLabel('')
        self.error_label.setStyleSheet('''color: red;
                                       font 14px;''')
        self.team_info_layout.addWidget(self.error_label, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.team_info_widget.setLayout(self.team_info_layout)
        self.team_info_tab_layout.addWidget(self.team_info_widget, 0, 0, 1, 2)
        #Create current team widget
        self.current_team_label = QLabel('Current Teams')
        self.team_info_tab_layout.addWidget(self.current_team_label, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.current_team_list = QWidget()
        self.current_team_list.setFixedWidth(500)
        self.current_team_list_layout = QVBoxLayout()
        self.current_team_list.setLayout(self.current_team_list_layout)
        self.team_info_tab_layout.addWidget(self.current_team_list, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        
    #create Game Builder tab
        self.game_builder_tab = QWidget()
        self.game_builder_tab_layout = QGridLayout()
        self.game_builder_tab.setLayout(self.game_builder_tab_layout)
        self.game_info_label = QLabel('Game Configuration')
        self.game_builder_tab_layout.addWidget(self.game_info_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        #create a filters 'Widget' that holds a custom layout for the filterable options
        self.filters_widget = QWidget()
        self.filters_layout = QGridLayout()
        self.layout_label = QLabel('Layout:')
        self.filters_layout.addWidget(self.layout_label, 0, 0, 1, 1)
        self.ques_per_round_label = QLabel('Questions Per Round:')
        self.filters_layout.addWidget(self.ques_per_round_label, 1, 1, 1, 1)
        self.qpr_num = QComboBox()
        self.qpr_num.addItems(self.x)
        self.qpr_num.setCurrentIndex(2)
        self.qpr_num.activated.connect(self.game_layout_preview)
        self.qpr_num.setMaximumWidth(40)
        self.filters_layout.addWidget(self.qpr_num, 1, 2, 1, 1)
        self.Rounds = QLabel('Rounds:')
        self.filters_layout.addWidget(self.Rounds, 2, 1, 1, 1)
        self.num_round = QComboBox()
        self.num_round.addItems(self.x)
        self.num_round.setCurrentIndex(2)
        self.num_round.activated.connect(self.game_layout_preview)
        self.num_round.setMaximumWidth(40)
        self.filters_layout.addWidget(self.num_round, 2, 2, 1, 1)
        self.filters_label = QLabel('Filters:')
        self.filters_layout.addWidget(self.filters_label, 3, 0, 1, 1)
        self.type_label = QLabel('Question Types:')
        self.filters_layout.addWidget(self.type_label, 4, 1, 1, 1)
        self.type_widget = QWidget()
        self.type_layout = QVBoxLayout()
        for i in self.types:
            self.type = QCheckBox(i)
            self.type.setChecked(True)
            self.type_layout.addWidget(self.type)
        self.type_widget.setLayout(self.type_layout)
        self.filters_layout.addWidget(self.type_widget, 4, 2, 1, 2)
        self.filters_widget.setLayout(self.filters_layout)
        self.game_builder_tab_layout.addWidget(self.filters_widget, 5, 0, 1, 2)
        self.category_label = QLabel('Category:')
        self.filters_layout.addWidget(self.category_label, 5, 1, 1, 1)
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        self.category_combo.setMaximumWidth(150)
        self.filters_layout.addWidget(self.category_combo, 5, 2, 1, 1)
        self.game_layout_widget = QWidget()
        self.glw_layout = QGridLayout()
        self.game_layout_label = QLabel('Question Layout Preview')
        self.glw_layout.addWidget(self.game_layout_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.count = 1
        self.quest = 0
        for n in range(int(self.num_round.currentText())):
                self.gl_round_label = QLabel(f'Round {n + 1}')
                self.gl_round_label.setMaximumHeight(30)
                self.gl_round_label.setStyleSheet('font: bold 14px;')
                self.glw_layout.addWidget(self.gl_round_label, self.count, 0, 1, 1)
                self.count += 1
                self.gl_round_list = QListWidget()
                self.gl_round_list.setWordWrap(True)
                self.gl_round_list.setFixedWidth(300)
                self.gl_round_list.setStyleSheet('''border: none;
                                                    padding: 3px;
                                                    font: 14px;
                                                ''')
                self.gl_round_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
                self.glw_layout.addWidget(self.gl_round_list, self.count, 0, 1, 1)
                self.count += 1
                self.qcount = 1
                for i in range(int(self.qpr_num.currentText())):
                    shuffle(self.filtered_questions)
                    question = self.filtered_questions[self.quest]['question']
                    difficulty = self.filtered_questions[self.quest]['difficulty']
                    if i != int(self.qpr_num.currentText()) - 1:
                        self.gl_question_item = (f'{self.qcount}. {question}, {difficulty}')
                    else:
                        self.gl_question_item = QListWidgetItem(f'W. {question}, {difficulty}')
                    self.gl_round_list.addItem(self.gl_question_item)
                    self.qcount += 1
                    self.quest += 1
        self.game_layout_widget.setLayout(self.glw_layout)
        self.game_builder_tab_layout.addWidget(self.game_layout_widget, 4, 3, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.difficulty_level_label = QLabel('Max Difficulty:')
        self.filters_layout.addWidget(self.difficulty_level_label, 6, 1, 1, 1)
        self.difficulty_level_combo = QComboBox()
        self.difficulty_level_combo.addItems(self.diff)
        self.difficulty_level_combo.setMaximumWidth(40)
        self.filters_layout.addWidget(self.difficulty_level_combo, 6, 2, 1, 1)
        self.filter_button = QPushButton('Update')
        self.filter_button.clicked.connect(self.filter_questions)
        self.filters_layout.addWidget(self.filter_button, 7, 3, 1, 1)
        self.choose_question_label = QLabel('Choose Questions: ')
        self.filters_layout.addWidget(self.choose_question_label, 8, 0, 1, 1)
        self.auto_radio = QRadioButton('Automatically')
        self.auto_radio.clicked.connect(self.auto_question_generator)
        self.auto_radio.setChecked(True)
        self.filters_layout.addWidget(self.auto_radio, 8, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.manual_radio = QRadioButton('Manually')
        self.manual_radio.clicked.connect(self.manual_question_choice)
        self.filters_layout.addWidget(self.manual_radio, 8, 2, 1, 1)
        self.timer_config_label = QLabel('Question Timer')
        self.game_builder_tab_layout.addWidget(self.timer_config_label, 9, 0, 1, 1)
        self.time_set_widget = QWidget()
        self.time_set_widget.setMaximumWidth(125)
        self.time_set_layout = QHBoxLayout()
        self.time_set_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_set_widget.setLayout(self.time_set_layout)
        self.question_minutes = QComboBox()
        self.question_minutes.setMaximumWidth(60)
        self.question_minutes.addItems(self.min)
        self.question_minutes.setCurrentIndex(3)
        self.time_set_layout.addWidget(self.question_minutes)
        self.colon_label = QLabel(':')
        self.colon_label.setMaximumWidth(5)
        self.time_set_layout.addWidget(self.colon_label)
        self.question_seconds = QComboBox()
        self.question_seconds.setMaximumWidth(60)
        self.question_seconds.addItems(self.sec)
        self.time_set_layout.addWidget(self.question_seconds)
        self.game_builder_tab_layout.addWidget(self.time_set_widget, 9, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.create_game_button = QPushButton('Create Game')
        self.create_game_button.setFixedWidth(130)
        self.create_game_button.clicked.connect(self.create_game)
        self.game_builder_tab_layout.addWidget(self.create_game_button, 10, 0, 1, 2, Qt.AlignmentFlag.AlignRight)
        self.settings_tab.addTab(self.team_info_tab, 'Team Information')
        self.settings_tab.addTab(self.game_builder_tab, 'Game Information')
        self.tabWidget.addTab(self.settings_tab, 'Game Settings')
#Create the Game Control tab
        self.controller_tab = QWidget()
        self.game_control_layout = QGridLayout()
        self.controller_tab.setLayout(self.game_control_layout)
        self.scores_label = QLabel('Scores')
        self.scores_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_control_layout.addWidget(self.scores_label, 0, 0, 1, 3)
        self.player_screen_view_label = QLabel('Game Screen View')
        self.game_control_layout.addWidget(self.player_screen_view_label, 0, 3, 1, 2, Qt.AlignmentFlag.AlignCenter)
    #Create the Game section widget and game pages
        self.game_section = QStackedWidget()
        self.rules_page = Rules(self.rules)
        self.round_page = RoundScreen(self.round_counter)
        self.question_page = QLabel('This is the question page')
        self.answer_page = QLabel('This is the answer Page')
        self.score_page = Leaderboard(self.current_teams)
        self.wager_page = WagerRules()
        self.game_over = QLabel('Game Over')
    #add widgets to the game section widget
        self.game_section.addWidget(self.rules_page)
        self.game_section.addWidget(self.round_page)
        self.game_section.addWidget(self.question_page)
        self.game_section.addWidget(self.answer_page)
        self.game_section.addWidget(self.score_page)
        self.game_section.addWidget(self.wager_page)
        self.game_section.addWidget(self.game_over)
        self.game_section.setMinimumSize(550, 400)
        self.game_control_layout.addWidget(self.game_section, 1, 3, 1, 2)
    #Create the leaderboard section to hold the score widgets
        self.leader_widget = QWidget()
        self.leader_layout = QVBoxLayout()
        self.leader_widget.setLayout(self.leader_layout)
        self.leader_widget.setMinimumSize(600, 400)
        self.game_control_layout.addWidget(self.leader_widget, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
    #add buttons for game control
        self.player_screen_button = QPushButton('Show Player Screen')
        self.player_screen_button.setDisabled(True)
        self.player_screen_button.clicked.connect(self.toggle_player_screen)
        self.game_control_layout.addWidget(self.player_screen_button, 6, 3, 1, 1)
        self.start_button = QPushButton('Start Game')
        self.start_button.setDisabled(True)
        self.start_button.setStyleSheet('background-color: lightgreen;')
        self.start_button.setFixedHeight(50)
        self.start_button.clicked.connect(self.game_engine)
        self.game_control_layout.addWidget(self.start_button, 4, 3, 1, 2)
        self.leaderboard_button = QPushButton('Show Leaderboard')
        self.leaderboard_button.clicked.connect(self.show_leaderboard_toggle)
        self.game_control_layout.addWidget(self.leaderboard_button, 6, 4, 1, 1)
        self.show_answer_button = QPushButton('Show Answer')
        self.show_answer_button.setDisabled(True)
        self.show_answer_button.setFixedHeight(50)
        self.show_answer_button.clicked.connect(self.game_engine)
        self.show_answer_button.setStyleSheet('''background-color: red;
                                                ''')
        self.game_control_layout.addWidget(self.show_answer_button, 5, 3, 1, 2)
        self.rules_button = QPushButton('Show Rules')
        self.rules_button.clicked.connect(self.toggle_rules_page)
        self.game_control_layout.addWidget(self.rules_button, 7, 4, 1, 1)
    #add section for game master notes
        
        self.tabWidget.addTab(self.controller_tab, 'Game Controller')
        self.setCentralWidget(self.mainwidget)
        self.tabWidget.setCurrentIndex(0)
        

    def add_team(self):#adds team to current team list 
        self.team_name.setStyleSheet('background-color: white;')
        self.player_number.setStyleSheet('background-color: white;')
        self.bonus_pts.setStyleSheet('background-color: white;')

        if self.team_name.currentText() == '':
            self.team_name.setStyleSheet('background-color: red;')
            self.error_label.setText('*Please enter a team name*')
        elif self.player_number.text() == '':
            self.player_number.setStyleSheet('background-color: red;')
            self.error_label.setText('*Please enter how many players are on team*')
        elif self.player_number.text().isdigit() is False:
            self.player_number.setStyleSheet('background-color: red;')
            self.error_label.setText('*Please enter a valid number*')
        elif self.bonus_pts.text() == '':
            self.bonus_pts.setStyleSheet('background-color: red;')
            self.error_label.setText('*Please enter bonus points*')
        elif self.bonus_pts.text().isdigit() is False:
            self.bonus_pts.setStyleSheet('background-color: red;')
            self.error_label.setText('*Please enter a valid number*')
        elif len(self.bonus_pts.text()) > 1 and self.bonus_pts.text().startswith('0'):
            self.bonus_pts.setStyleSheet('background-color: red;')
            self.error_label.setText('*Number can\'t start with zero*')

        else:
                check = self.team_info_tab_layout.itemAtPosition(4, 0).widget()
                if check is not None:
                    self.team_info_tab_layout.removeWidget(check)
                    check.deleteLater()

                self.current_team_list = QWidget()
                self.current_team_list.setFixedWidth(500)
                self.current_team_list_layout = QVBoxLayout()
                self.current_team_list.setLayout(self.current_team_list_layout)
                self.team_info_tab_layout.addWidget(self.current_team_list, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

                self.error_label.setText('')
                current_team_name = self.team_name.currentText()
                players = self.player_number.text()
                bonus = self.bonus_pts.text()
                self.current_teams.append({'team': current_team_name, 'players': players, 'bonus': bonus, 'r1': '0', 'r2': '0', 'r3': '0', 'r4': '0', 'r5': '0', 'total': bonus})
                
                for i in self.current_teams:

                    index = self.current_teams.index(i)
                    name = i['team']
                    score = i['total']
                    self.team_widget = TeamWidget(index, name, score)
                    self.team_widget.remove_button.clicked.connect(self.remove_team)
                    self.current_team_list_layout.addWidget(self.team_widget)
                    
                
                self.team_name.setCurrentText('')
                self.player_number.clear()
                self.bonus_pts.setText('0')
        self.create_score_entry()

    def remove_team(self): #remove the team from game
        
        for w in self.current_team_list.children():
            for child in w.children():
                if child == self.sender():
                        team = w.children()[2].text()
        
        for i in self.current_teams:
            if i['team'] == team:
                self.current_teams.remove(i)
        
        check = self.team_info_tab_layout.itemAtPosition(4, 0).widget()
        if check is not None:
            self.team_info_tab_layout.removeWidget(check)
            check.deleteLater()

        self.current_team_list = QWidget()
        self.current_team_list.setFixedWidth(500)
        self.current_team_list_layout = QVBoxLayout()
        self.current_team_list.setLayout(self.current_team_list_layout)
        self.team_info_tab_layout.addWidget(self.current_team_list, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        for i in self.current_teams:

            index = self.current_teams.index(i)
            name = i['team']
            score = i['total']
            self.team_widget = TeamWidget(index, name, score)
            self.team_widget.remove_button.clicked.connect(self.remove_team)
            self.current_team_list_layout.addWidget(self.team_widget)

        self.create_score_entry()

#creates a widget with team name, and round scores, and option for adding or subtracting scores
# for the scores section in the game controller tab
    def create_score_entry(self):
        check = self.game_control_layout.itemAtPosition(1, 0).widget()
        if check is not None:
            self.game_control_layout.removeWidget(check)
            check.deleteLater()
        self.game_control_layout.itemAtPosition(1, 0)
        self.leader_widget = QWidget()
        self.leader_layout = QVBoxLayout()
        self.leader_widget.setLayout(self.leader_layout)
        self.leader_widget.setMinimumSize(600, 400)
        self.leader_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.game_control_layout.addWidget(self.leader_widget, 1, 0, 10, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        for t in self.current_teams:

            if t is '':
                pass
            else:
                index = self.current_teams.index(t)
                team = t['team']
                score = t['total']
                rounds = self.total_round_selection
                widget = ScoreWidget(team, index, score, rounds)
                self.leader_layout.addWidget(widget)

    def load_questions(self):# grab questions from the database
    #connect to the database
        conn = sqlite3.connect('trivia_questions.db')

    #Create a cursor
        c = conn.cursor()

    #query the mulitple choice database
        c.execute("SELECT * FROM MultipleChoiceQuestions")
        mc_list = c.fetchall() #layout: (id, main category, sub category, difficulty, notes, question, answer, distractor1, distractor2, distractor3)
        for i in mc_list:
            mc_dict = {'type': 'Multiple Choice', 'main_category': i[1], 'sub_category': i[2], 'difficulty': str(i[3]), 'notes': i[4], 'question': i[5], 'answer': i[6], 'distractor1': i[7], 'distractor2': i[8], 'distractor3': i[9]}
            if mc_dict not in self.questions:
                self.questions.append(mc_dict)
        c.execute("SELECT * FROM TrueFalseQuestions")
        tf_list = c.fetchall() #layout: (id, main category, sub category, difficulty, notes, question, answer)
        for i in tf_list:
            tf_dict = {'type': 'True or False', 'main_category': i[1], 'sub_category': i[2], 'difficulty': str(i[3]), 'notes': i[4], 'question': i[5], 'answer': i[6]}
            if tf_dict not in self.questions:
                self.questions.append(tf_dict)
        c.execute("SELECT * FROM FillInTheBlankQuestions")
        fib_list = c.fetchall() #layout: (id, main category, sub category, difficulty, notes, question, answer1, answer2, answer3)
        for i in fib_list:
            fib_dict = {'type': 'Fill in the Blank', 'main_category': i[1], 'sub_category': i[2], 'difficulty': str(i[3]), 'notes': i[4], 'question': i[5], 'answer1': i[6], 'answer2': i[7], 'answer3': i[8]}
            if fib_dict not in self.questions:
                self.questions.append(fib_dict)
    
        conn.commit()
    
        conn.close()
    #prints number of questions in database
    #not necessary for application to work
        for i in self.questions:
            if i['type'] not in self.types:
                self.types.append(i['type'])
            if i['main_category'] not in self.categories:
                self.categories.append(i['main_category'])
        print(len(self.questions), ' Questions Loaded')

    def filter_questions(self):#filters the available questions to the selected inputs when called
        checkboxes = []
        checked = []
        for i in self.type_widget.children():
            if i.isWidgetType() is True:
                checkboxes.append(i)
        for i in checkboxes:
            if i.isChecked() is True:
                checked.append(i.text())
        self.filters['types'] = checked
        self.filters['main_category'] = self.category_combo.currentText()
        self.filters['difficulty'] = self.difficulty_level_combo.currentText()
        self.filtered_questions = []
        for i in range(len(self.questions)):
                if self.questions[i]['type'] in self.filters['types']:
                    if self.filters['main_category'] == 'All':
                        if int(self.questions[i]['difficulty']) <= int(self.filters['difficulty']):
                            self.filtered_questions.append(self.questions[i])
                    if self.questions[i]['main_category'] == self.filters['main_category']:
                        if int(self.questions[i]['difficulty']) <= int(self.filters['difficulty']):
                            self.filtered_questions.append(self.questions[i])
        shuffle(self.filtered_questions)
        if self.auto_radio.isChecked():
            self.game_layout_preview()
            self.auto_question_generator()
        elif self.manual_radio.isChecked():
            self.manual_question_choice()


    def manual_question_choice(self):#creates a new widget containing filtered questions for manual selection using add and remove buttons
        check  = self.game_builder_tab_layout.itemAtPosition(6, 0)
        if check is not None:
            self.game_builder_tab_layout.removeItem(check)
            check.widget().deleteLater()
        self.man_question_widget = QWidget()
        self.man_question_widget_layout = QGridLayout()
        self.man_question_widget.setLayout(self.man_question_widget_layout)
        self.question_pool_label = QLabel('Question Pool')
        self.man_question_widget_layout.addWidget(self.question_pool_label, 0, 0, 1, 1)
        self.question_pool = QListWidget()
        self.question_pool.setFixedSize(400, 150)
        self.question_pool.setWordWrap(True)
        self.selected_category = self.category_combo.currentText()
        self.max_difficulty = self.difficulty_level_combo.currentText()

        if self.category_combo.currentIndex() is 0:
            for i in self.filtered_questions:
                question = i['question']
                difficulty = i['difficulty']
                self.question_pool.addItem(f'{question}, {difficulty}')
        else:
            for i in self.questions:
                if i['main_category'] == self.selected_category and int(i['difficulty']) <= int(self.max_difficulty):

                    question = i['question']
                    difficulty = i['difficulty']
                    self.question_pool.addItem(f'{question}, {difficulty}')

        self.man_question_widget_layout.addWidget(self.question_pool, 1, 0, 1, 1)
        self.add_remove_buttons = QWidget()
        self.arb_layout = QVBoxLayout()
        self.add_remove_buttons.setLayout(self.arb_layout)
        self.add_question_button = QPushButton('Add')
        self.add_question_button.setFixedWidth(70)
        self.add_question_button.clicked.connect(self.add_question)
        self.arb_layout.addWidget(self.add_question_button)
        self.remove_question_button = QPushButton('Remove')
        self.remove_question_button.setFixedWidth(70)
        self.remove_question_button.clicked.connect(self.remove_question)
        self.arb_layout.addWidget(self.remove_question_button)
        self.man_question_widget_layout.addWidget(self.add_remove_buttons, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.game_builder_tab_layout.addWidget(self.man_question_widget, 6, 0, 1, 2)

    def add_question(self):#transfers the selected question from the manual question list to the selected question in the game preview area when called
        item = self.question_pool.currentItem()
        if item is not None:
            new_question = item.text()
        current_index = None
        for widget in self.game_layout_widget.children(): 
            if type(widget) == QListWidget:
                for gw_item in widget.selectedItems():
                    if gw_item is not None:
                        current_index = widget.row(gw_item)
                        if current_index != int(self.qpr_num.currentText()) - 1:
                            gw_item.setText(f'{current_index + 1}. {new_question}')
                        else:
                            gw_item.setText(f'W. {new_question}')
                        widget.clearSelection()
        self.question_pool.clearSelection()

    def remove_question(self):#removes selected question from game preview area when called
        child_widgets = self.game_layout_widget.children()
        current_index = None
        for widget in child_widgets:
            if type(widget) == QListWidget:
                for gw_item in widget.selectedItems():
                    if gw_item is not None:
                        current_index = widget.row(gw_item)
                        if current_index != int(self.qpr_num.currentText()) - 1:
                            gw_item.setText(f'{current_index + 1}. (Empty)')
                        else:
                            gw_item.setText(f'W. (Empty)')
                        widget.clearSelection()
#automatically and randomly chooses questions for the selected number of rounds and questions per round and adds replaces the old
#questions in the game preview section
    def auto_question_generator(self):
        check  = self.game_builder_tab_layout.itemAt(6)
        if check is not None:
            self.game_builder_tab_layout.removeItem(check)
            check.widget().deleteLater()
        shuffle(self.filtered_questions)


    def game_layout_preview(self): #Create the game layout widget/section based on number of round and questions per round

        check = self.game_builder_tab_layout.itemAtPosition(4, 3)
        if check is not None:
            self.game_builder_tab_layout.removeWidget(check.widget())
        self.game_layout_widget = QWidget()
        self.glw_layout = QGridLayout()
        self.game_layout_label = QLabel('Question Layout Preview')
        self.game_layout_label.setMinimumHeight(75)
        self.glw_layout.addWidget(self.game_layout_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.count = 1
        self.quest = 0
        if (int(self.num_round.currentText()) * int(self.qpr_num.currentText())) > len(self.filtered_questions):
                    error_message = f'''Not Enough questions to fill the requested slots.
Slots Requested: {(int(self.num_round.currentText()) * int(self.qpr_num.currentText()))}\nAvailable Questions: {len(self.filtered_questions)}'''
                    error_label = QLabel(error_message)
                    error_label.setStyleSheet('font: 14px;')
                    self.glw_layout.addWidget(error_label, 1, 0, 1, 1)
        else:

            for n in range(int(self.num_round.currentText())):
                self.gl_round_label = QLabel(f'Round {n + 1}')
                self.gl_round_label.setMaximumHeight(30)
                self.glw_layout.addWidget(self.gl_round_label, self.count, 0, 1, 1)
                self.count += 1
                self.gl_round_list = QListWidget()
                self.gl_round_list.setWordWrap(True)
                self.gl_round_list.setFixedWidth(300)
                self.gl_round_list.setStyleSheet('''border: none;
                                                    padding: 3px; ''')
                self.glw_layout.addWidget(self.gl_round_list, self.count, 0, 1, 1)
                self.count += 1
                self.qcount = 1
                for i in range(int(self.qpr_num.currentText())):
                    question = self.filtered_questions[self.quest]['question']
                    difficulty = self.filtered_questions[self.quest]['difficulty']
                    self.quest += 1
                    if i < (int(self.qpr_num.currentText()) - 1):
                        self.gl_question_item = f'{self.qcount}. {question}, {difficulty}'
                        self.qcount += 1
                        
                    else:
                        self.gl_question_item = f'W. {question}, {difficulty}'
                    self.gl_round_list.addItem(self.gl_question_item)
        self.game_layout_widget.setLayout(self.glw_layout)
        self.game_builder_tab_layout.addWidget(self.game_layout_widget, 4, 3, 12, 1, Qt.AlignmentFlag.AlignCenter)

    def toggle_player_screen(self):#toggles a second screen when called

        if self.player_screen_toggle % 2:
            self.player_screen.hide()
            self.player_screen_button.setText('Show Player Screen')
            self.start_button.setDisabled(True)
            self.player_screen_toggle = self.player_screen_toggle + 1
        else:
            self.player_screen.show()
            self.player_screen_button.setText('Hide Player Screen')
            self.start_button.setDisabled(False)
            self.player_screen_toggle = self.player_screen_toggle + 1

    def create_game(self):  # applies setting selections to the game and creates the game.
        if self.create_game_toggle % 2:
        #Enable the player screen button
            self.player_screen_button.setDisabled(False)

        #Change the text of the create game button and startbutton
            self.create_game_button.setText('Edit Game Settings')
            self.start_button.setText('Start Game')
            self.question_type_selection = []
            for checkbox in self.type_widget.findChildren(QCheckBox):
                if checkbox.isChecked():
                    self.question_type_selection.append(checkbox.text())
            self.qpr_selection = int(self.qpr_num.currentText())
            self.total_round_selection = int(self.num_round.currentText())
            self.minute_selection = int(self.question_minutes.currentText())
            self.second_selection = int(self.question_seconds.currentText())
        #reset the round, question and stage counters to 1
            self.question_counter = 1
            self.round_counter = 1
            self.stage_counter = 1
            self.create_game_toggle += 1
        #Disable the widgets in the Game Settings/Game information tab
            self.category_combo.setDisabled(True)
            self.question_minutes.setDisabled(True)
            self.question_seconds.setDisabled(True)
            self.num_round.setDisabled(True)
            self.qpr_num.setDisabled(True)
            self.type_widget.setDisabled(True)
            self.filter_button.setDisabled(True)
            self.difficulty_level_combo.setDisabled(True)
            self.auto_radio.setDisabled(True)
            self.manual_radio.setDisabled(True)
            self.game_layout_widget.setDisabled(True)
        #Check to see if the manual question widget is on screen and then disables it if true
            if self.manual_radio.isChecked():
                self.man_question_widget.setDisabled(True)
        #Format the selected questions back to only the question and add them to the game question list
            child_widgets = self.game_layout_widget.children()
            for widget in child_widgets:
                gw_widget = widget
                gw_type = type(gw_widget)
                if gw_type == QListWidget:
                    for i in range(gw_widget.count()):
                        raw_question = gw_widget.item(i).text()
                        formatted_question = raw_question[3:][:-3]
                        self.game_questions.append(formatted_question)
            self.total_questions = len(self.game_questions)
            self.create_score_entry()
        else:
        #Disable the player screen button and hide the screen
            self.player_screen_button.setDisabled(True)
            self.player_screen.hide()
        #Change the text of the create game button
            self.create_game_button.setText('Create Game')
        #Enable the widgets in the Game Settings/Game information tab
            self.category_combo.setDisabled(False)
            self.question_minutes.setDisabled(False)
            self.question_seconds.setDisabled(False)
            self.num_round.setDisabled(False)
            self.qpr_num.setDisabled(False)
            self.type_widget.setDisabled(False)
            self.filter_button.setDisabled(False)
            self.difficulty_level_combo.setDisabled(False)
            self.auto_radio.setDisabled(False)
            self.manual_radio.setDisabled(False)
            self.game_layout_widget.setDisabled(False)
        # Enable the Manual question widget if it's on the screen
            if self.manual_radio.isChecked():
                self.man_question_widget.setDisabled(False)
            self.create_game_toggle += 1

# Moves between windows or "Stages" of the game when the start_pause_button and show_answer_button are clicked.
    def game_engine(self):
    # TODO: check to see if the start button's text is "End Game". if so game is over and the stats will be saved to a log file stored in folder called Previous games
    # the file will contain the teams that competed, total number of players they had for that game, and total score.
    # the file name should be labeled as follows: mm-dd-yyyy-location
        if self.leaderboard_button.text() == 'Hide Leaderboard':
            self.leaderboard_button.setText('Show Leaderboard')
        if self.leaderboard_toggle %2:
            pass
        else:
            self.leaderboard_toggle += 1
        if self.rules_button.text() == "Hide Rules":
            self.rules_button.setText('Show Rules')
        if self.rules_toggle %2:
            pass
        else:
            self.rules_toggle += 1

    # Check to see if the current round is less than or equal to the total rounds in the game
        if self.round_counter <= self.total_round_selection:
            if self.stage_counter is 1:
            #Change the selected round in the score widget automatically
                for widget in self.leader_widget.children():
                    if type(widget) is ScoreWidget:
                        for item in widget.children():
                            if type(item) is QPushButton:
                                if self.round_counter == 1 and widget.children().index(item) == (self.round_counter + 2):
                                    item.setChecked(True)
                                elif self.round_counter == 2  and widget.children().index(item) == (self.round_counter + 3):
                                    item.setChecked(True)
                                elif self.round_counter == 3  and widget.children().index(item) == (self.round_counter + 4):
                                    item.setChecked(True)
                                elif self.round_counter == 4  and widget.children().index(item) == (self.round_counter + 5):
                                    item.setChecked(True)
                                elif self.round_counter == 5  and widget.children().index(item) == (self.round_counter + 6):
                                    item.setChecked(True)
                                else:
                                    item.setChecked(False)
            #If its the final round, print final round, otherwise print the current round
                self.leaderboard_button.setDisabled(False)
                if self.round_counter == self.total_round_selection:
                    self.round_page.final_round()
                    self.player_screen.round_page.final_round()
                    self.game_section.setCurrentIndex(1)
                    self.player_screen.main_widget.setCurrentIndex(1)
                else:
                    self.round_page.round_label.setText(f'Round {self.round_counter}')
                    self.game_section.setCurrentIndex(1)
                    self.player_screen.round_page.round_label.setText(f'Round {self.round_counter}')
                    self.player_screen.main_widget.setCurrentIndex(1)
                self.stage_counter += 1
                self.start_button.setText('Show Question')
                
            elif self.stage_counter is 2:
            #if its the last question in the round, check to see what the current index is.
                self.leaderboard_button.setDisabled(False)
                if self.question_counter == self.qpr_selection:
                #if the current index is showing the wager questions, show the round's wager question
                    if self.game_section.currentIndex() is 5:
                        check = self.game_section.widget(2)
                        if check:
                            self.game_section.removeWidget(check)
                            check.deleteLater()
                        check2 = self.player_screen.main_widget.widget(2)
                        if check2:
                            self.player_screen.main_widget.removeWidget(check2)
                            check2.deleteLater()
                        self.question_idx = self.game_questions[self.question_index]
                    #check to see what type of question, respond with correct question widget
                        for i in self.questions:
                            if i['question'] == self.question_idx:
                                if i['type'] == 'Multiple Choice':
                                    self.question_widget = MultipleChoiceQuestion(i['question'], i['answer'], i['distractor1'], i['distractor2'], i['distractor3'], self.minute_selection, self.second_selection)
                                    self.ps_question_widget = MultipleChoiceQuestion(i['question'], i['answer'], i['distractor1'], i['distractor2'], i['distractor3'], self.minute_selection, self.second_selection)
                                    self.game_section.insertWidget(2, self.question_widget)
                                    self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                                elif i['type'] == 'True or False':
                                    self.question_widget = TrueFalseQuestion(i['question'], self.minute_selection, self.second_selection)
                                    self.ps_question_widget = TrueFalseQuestion(i['question'], self.minute_selection, self.second_selection)
                                    self.game_section.insertWidget(2, self.question_widget)
                                    self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                                elif i['type'] == 'Fill in the Blank':
                                    self.question_widget = FillInBlankQuestion(i['question'], self.minute_selection, self.second_selection)
                                    self.ps_question_widget = FillInBlankQuestion(i['question'], self.minute_selection, self.second_selection)
                                    self.game_section.insertWidget(2, self.question_widget)
                                    self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                        self.game_section.setCurrentIndex(2)
                        self.player_screen.main_widget.setCurrentIndex(2)
                        self.stage_counter += 1
                        self.start_button.setDisabled(True)
                        self.show_answer_button.setDisabled(False)
                #if the current index is showing the previous round's scores, show the wager rules
                    elif self.game_section.currentIndex() is 4:
                        self.game_section.setCurrentIndex(5)
                        self.player_screen.main_widget.setCurrentIndex(5)
                    elif self.game_section.currentIndex() is 1:
                        self.game_section.setCurrentIndex(5)
                        self.player_screen.main_widget.setCurrentIndex(5)
            #if not last question in the round, just show the question
                else:
                    check = self.game_section.widget(2)
                    if check:
                        self.game_section.removeWidget(check)
                        check.deleteLater()
                    check2 = self.player_screen.main_widget.widget(2)
                    if check2:
                        self.player_screen.main_widget.removeWidget(check2)
                        check2.deleteLater()
                    self.question_idx = self.game_questions[self.question_index]
            #check to see what type of question, respond with correct question widget
                    for i in self.questions:
                        if i['question'] == self.question_idx:
                            if i['type'] == 'Multiple Choice':
                                self.question_widget = MultipleChoiceQuestion(i['question'], i['answer'], i['distractor1'], i['distractor2'], i['distractor3'], self.minute_selection, self.second_selection)
                                self.ps_question_widget = MultipleChoiceQuestion(i['question'], i['answer'], i['distractor1'], i['distractor2'], i['distractor3'], self.minute_selection, self.second_selection)
                                self.game_section.insertWidget(2, self.question_widget)
                                self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                            elif i['type'] == 'True or False':
                                self.question_widget = TrueFalseQuestion(i['question'], self.minute_selection, self.second_selection)
                                self.ps_question_widget = TrueFalseQuestion(i['question'], self.minute_selection, self.second_selection)
                                self.game_section.insertWidget(2, self.question_widget)
                                self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                            elif i['type'] == 'Fill in the Blank':
                                self.question_widget = FillInBlankQuestion(i['question'], self.minute_selection, self.second_selection)
                                self.ps_question_widget = FillInBlankQuestion(i['question'], self.minute_selection, self.second_selection)
                                self.game_section.insertWidget(2, self.question_widget)
                                self.player_screen.main_widget.insertWidget(2, self.ps_question_widget)
                    self.game_section.setCurrentIndex(2)
                    self.player_screen.main_widget.setCurrentIndex(2)
                    self.stage_counter += 1
                    self.start_button.setDisabled(True)
                    self.show_answer_button.setDisabled(False)
        #show the question answer widget
            elif self.stage_counter is 3:
            #check to see if widgets already exist, and delete if so
                check = self.game_section.widget(3)
                if check:
                    self.game_section.removeWidget(check)
                    check.deleteLater()
                check2 = self.player_screen.main_widget.widget(3)
                if check2:
                    self.player_screen.main_widget.removeWidget(check2)
                    check2.deleteLater()
        #check to see what type of question, respond with correct answer widget
                for i in self.questions:
                    if i['question'] == self.question_idx:
                        if i['type'] == 'Multiple Choice':
                            self.answer_widget = MultipleChoiceAnswer(i['question'], i['answer'])
                            self.ps_answer_widget = MultipleChoiceAnswer(i['question'], i['answer'])
                            self.game_section.insertWidget(3, self.answer_widget)
                            self.player_screen.main_widget.insertWidget(3, self.ps_answer_widget)
                        elif i['type'] == 'True or False':
                            self.answer_widget = TrueFalseAnswer(i['question'], i['answer'])
                            self.ps_answer_widget = TrueFalseAnswer(i['question'], i['answer'])
                            self.game_section.insertWidget(3, self.answer_widget)
                            self.player_screen.main_widget.insertWidget(3, self.ps_answer_widget)
                        elif i['type'] == 'Fill in the Blank':
                            self.answer_widget = FillInBlankAnswer(i['question'], i['answer1'], i['answer2'], i['answer3'])
                            self.ps_answer_widget = FillInBlankAnswer(i['question'], i['answer1'], i['answer2'], i['answer3'])
                            self.game_section.insertWidget(3, self.answer_widget)
                            self.player_screen.main_widget.insertWidget(3, self.ps_answer_widget)
                self.game_section.setCurrentIndex(3)
                self.player_screen.main_widget.setCurrentIndex(3)
                self.question_counter += 1
                self.question_index += 1
                self.stage_counter += 1
                self.start_button.setText('Show Scores')
                self.start_button.setDisabled(False)
                self.show_answer_button.setDisabled(True)
        #show the leaderboard
            elif self.stage_counter is 4:
            #check to see if widgets exists, and if so, delete them
                self.leaderboard_button.setDisabled(True)
                check = self.game_section.widget(4)
                if check:
                    self.game_section.removeWidget(check)
                check2 = self.player_screen.main_widget.widget(4)
                if check2:
                    self.player_screen.main_widget.removeWidget(check2)
                self.update_score()
            #create new leaderboard objects and add them to index 4 of each screen
                self.leaderboard = Leaderboard(self.current_teams)
                self.game_section.insertWidget(4, self.leaderboard)
                self.ps_leaderboard = Leaderboard(self.current_teams)
                self.player_screen.main_widget.insertWidget(4, self.ps_leaderboard)
                self.game_section.setCurrentIndex(4)
                self.player_screen.main_widget.setCurrentIndex(4)
                if self.question_counter > self.qpr_selection:
                    self.round_counter += 1
                    self.question_counter = 1
                    self.stage_counter = 1
                    self.start_button.setText('Next Round')
                else:
                    self.start_button.setText('Next Question')
                    self.stage_counter = 2
        #if the current round is greater than the round selection, show the game over page.         
        else:
            self.leaderboard_button.setDisabled(False)
            self.game_section.setCurrentIndex(6)
            self.player_screen.main_widget.setCurrentIndex(6)
            self.start_button.setText('End and Save Game')
        
    def update_score(self):#grab the values from the buttons in the score widget, update them to the appropriate team in the self.current_teams list
        team = None
        score1 = '0'
        score2 = '0'
        score3 = '0'
        score4 = '0'
        score5 = '0'

        for widget in self.leader_widget.children():
            if type(widget) == ScoreWidget:
                for item in widget.children():
                    if widget.children().index(item) == 1:
                        team = item.text().split('. ')[1]
                        
                    if type(item) == QPushButton and widget.children().index(item) < len(widget.children()) - 2:
                        if widget.children().index(item) == 3:
                            score1 = item.text()
                        elif widget.children().index(item) == 5:
                            score2 = item.text()
                        elif widget.children().index(item) == 7:
                            score3 = item.text()
                        elif widget.children().index(item) == 9:
                            score4 = item.text()
                        elif widget.children().index(item) == 11:
                            score5 = item.text()
                
                    for i in self.current_teams:
                        if i['team'] == team:
                            i['r1'] = score1
                            i['r2'] = score2
                            i['r3'] = score3
                            i['r4'] = score4
                            i['r5'] = score5
                            i['total'] = int(i['bonus']) + int(i['r1']) + int(i['r2']) + int(i['r3']) + int(i['r4']) + int(i['r5'])

    
    def show_leaderboard_toggle(self):
        if self.rules_button.text() == "Hide Rules":
            self.rules_button.setText('Show Rules')
        if self.rules_toggle %2:
            pass
        else:
            self.rules_toggle += 1
    #update the scores
        self.update_score()
    #define lists to store teams and scores
        current_teams = self.current_teams
    #Create two leaderboard widgets and passing the current team list
        self.leaderboard = Leaderboard(current_teams)
        self.ps_leaderboard = Leaderboard(current_teams)
    #Check to see if there is a widget at the Leaderboard index
        check = self.game_section.widget(4)
        if check:
            self.game_section.removeWidget(check)
        check2 = self.player_screen.main_widget.widget(4)
        if check2:
            self.player_screen.main_widget.removeWidget(check2)
        self.game_section.insertWidget(4, self.leaderboard)
        self.player_screen.main_widget.insertWidget(4, self.ps_leaderboard)
    #create the toggle of the button
        if self.leaderboard_toggle %2:
            self.game_section.setCurrentIndex(4)
            self.player_screen.main_widget.setCurrentIndex(4)
            self.leaderboard_button.setText('Hide Leaderboard')
             
        else:
            if self.game_section.currentIndex() != 4:
                self.game_section.setCurrentIndex(self.stage_counter - 1)
                self.player_screen.main_widget.setCurrentIndex(self.stage_counter - 1)
            self.leaderboard_button.setText('Show Leaderboard')
        self.leaderboard_toggle +=1

    def toggle_rules_page(self):
        if self.leaderboard_button.text() == "Hide Leaderboard":
            self.leaderboard_button.setText('Show Leaderboard')
            self.leaderboard_toggle += 1
        if self.leaderboard_toggle %2:
            pass
        else:
            self.leaderboard_toggle += 1
        if self.rules_toggle %2:
            self.game_section.setCurrentIndex(0)
            self.player_screen.main_widget.setCurrentIndex(0)
            self.rules_button.setText('Hide Rules')
            self.rules_toggle += 1
        else:
            self.game_section.setCurrentIndex(self.stage_counter - 1)
            self.player_screen.main_widget.setCurrentIndex(self.stage_counter - 1)
            self.rules_button.setText('Show Rules')
            self.rules_toggle += 1

            
class PlayerScreen(QMainWindow):
    def __init__(self, teams, rules):
        super().__init__()
        self.rules = rules
        self.teams = teams
        self.setWindowTitle('Player Screen')
        self.main_widget = QStackedWidget()
        self.rules_page = Rules(self.rules)
        self.round_page = RoundScreen(1)
        self.question_page = QLabel('This is the question page')
        self.answer_page = QLabel('This is the answer Page')
        self.score_page = Leaderboard(self.teams)
        self.wager_page = WagerRules()
        self.game_over = QLabel('Game Over')
        self.main_widget.addWidget(self.rules_page)
        self.main_widget.addWidget(self.round_page)
        self.main_widget.addWidget(self.question_page)
        self.main_widget.addWidget(self.answer_page)
        self.main_widget.addWidget(self.score_page)
        self.main_widget.addWidget(self.wager_page)
        self.main_widget.addWidget(self.game_over)
        self.setCentralWidget(self.main_widget)

class TeamWidget(QWidget):
    def __init__(self, index, team, score):
        super().__init__()
        self.team_num = index + 1
        self.team = team
        self.score = score

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.index_label = QLabel(f'{self.team_num}.')
        self.index_label.setFixedWidth(30)
        self.team_label = QLabel(self.team)
        self.score_label = QLabel(f'Points: {self.score}')
        self.remove_button = QPushButton('X')
        self.remove_button.setFixedWidth(50)

        self.layout.addWidget(self.index_label)
        self.layout.addWidget(self.team_label)
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.remove_button)

class ScoreWidget(QWidget):
    def __init__(self, team, index, score, rounds):
        super().__init__()
        self.rounds = int(rounds)
        self.click_count = 1
        self.team = team
        self.index = index
        self.score = score
        self.setStyleSheet(''' QLabel { font: 16px;
                                        padding: 3px;
                                        }
                                QLineEdit { font: 16px;
                                            padding: 3px;
                                        }
                                QPushButton { font: 16px;
                                            padding: 3px;
                                        }
                    ''')
        self.layout = QHBoxLayout()
        self.team_name_label = QLabel(f'{self.index + 1}. {self.team}')
        self.layout.addWidget(self.team_name_label)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for n in range(self.rounds):
            self.round_num_label = QLabel(f'{n + 1}.')
            self.round_num_label.setFixedWidth(20)
            self.round_num_label.setMargin(0)
            self.round_score_button = QPushButton(f'{0}')
            self.round_score_button.setFixedWidth(40)
            self.round_score_button.setCheckable(True)
            self.button_group.addButton(self.round_score_button)
            self.layout.addWidget(self.round_num_label, Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.round_score_button, Qt.AlignmentFlag.AlignCenter)
        self.points_edit = QLineEdit()
        self.points_edit.setFixedSize(40, 30)
        self.layout.addWidget(self.points_edit, Qt.AlignmentFlag.AlignRight)
        self.add_points_button = QPushButton('+')
        self.add_points_button.clicked.connect(self.add_points)
        self.add_points_button.setFixedWidth(30)
        self.layout.addWidget(self.add_points_button, Qt.AlignmentFlag.AlignRight)
        self.subtract_points_button = QPushButton('-')
        self.subtract_points_button.setFixedWidth(30)
        self.subtract_points_button.clicked.connect(self.subtract_points)
        self.layout.addWidget(self.subtract_points_button, Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

    def add_points(self):

        if self.points_edit.text() == '':
            self.points_edit.setStyleSheet('background-color: red;')
        elif self.points_edit.text().isdigit() is False:
            self.points_edit.setStyleSheet('background-color: red;')
        else:
            points = int(self.points_edit.text())
            for widget in self.children():
                wtype = type(widget)
                if wtype == QPushButton:
                    if widget.isChecked():
                        current = int(widget.text())
                        self.new = current + points
                        widget.setText(str(self.new))
                        widget.setChecked(False)
                        team = self.layout.itemAt(0).widget().text().split('. ')[1]
                        
                        if self.layout.indexOf(widget) == 2:
                            print('Round 1', widget.text())
                        elif self.layout.indexOf(widget) == 4:
                            print('Round 2', widget.text())
                        elif self.layout.indexOf(widget) == 6:
                            print('Round 3', widget.text())
                        elif self.layout.indexOf(widget) == 8:
                            print('Round 4', widget.text())
                        elif self.layout.indexOf(widget) == 10:
                            print('Round 5', widget.text())
                        
            self.points_edit.clear()
            self.points_edit.setStyleSheet('background-color: white;')
        
    def subtract_points(self):
       
        if self.points_edit.text() == '':
            self.points_edit.setStyleSheet('background-color: red;')
        elif self.points_edit.text().isdigit() is False:
            self.points_edit.setStyleSheet('background-color: red;')
        else:
            points = int(self.points_edit.text())
            for widget in self.children():
                wtype = type(widget)
                if wtype == QPushButton:
                    if widget.isChecked():
                        current = int(widget.text())
                        self.new = current - points
                        widget.setText(str(self.new))
                        widget.setChecked(False)
            
            self.points_edit.clear()
            self.points_edit.setStyleSheet('background-color: white;')

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
        shuffle(answer_list)
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

class MultipleChoiceAnswer(QWidget):
    def __init__(self, question, correct_answer):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        main_layout = QGridLayout()
        self.question = QLabel(str(question))
        self.question.setWordWrap(True)
        main_layout.addWidget(self.question, 0, 0, 1, 1)
        self.a = QLabel(str(correct_answer))
        main_layout.addWidget(self.a, 1, 0, 1, 1)
        
        self.setLayout(main_layout)

class TrueFalseQuestion(QWidget):
    def __init__(self, question, minutes, seconds):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        self.timer = Timer(minutes, seconds)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'True or False: \n{question}')
        self.question.setWordWrap(True)
        
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.timer)
        
        
        
        self.setLayout(main_layout)

class TrueFalseAnswer(QWidget):
    def __init__(self, question, answer):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'True or False: \n{question}')
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
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'Fill in the Blank: \n{self.question}')
        self.question.setWordWrap(True)
        self.timer = Timer(minutes, seconds)
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.timer)
        
        
        self.setLayout(main_layout)

class FillInBlankAnswer(QWidget):
    def __init__(self, question, answer1, answer2, answer3):
        super().__init__()
        self.question = question
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.question = QLabel(f'Fill in the Blank: \n{self.question}')
        self.question.setWordWrap(True)
        
        if self.answer2 == '' and self.answer3 == '':
            self.answer_label = QLabel(f'{self.answer1}')
        elif self.answer3 == '':
            self.answer_label = QLabel(f'{self.answer1}, {self.answer2}')
        else:
            self.answer_label = QLabel(f'{self.answer1}, {self.answer2}, {self.answer3}')
    
        self.answer_label.setWordWrap(True)
        main_layout.addWidget(self.question)
        main_layout.addWidget(self.answer_label)
        
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
            
        
        self.setLayout(self.layout)
    
    
    def team_score(self):
        col = 0
        row = 0
        sorted_teams = sorted(self.teams, key=lambda x: x['total'], reverse=True)
        for t in sorted_teams:
            widget = QWidget()
            layout = QGridLayout()
            widget.setLayout(layout)
            
            name = QLabel(t['team'])
            layout.addWidget(name, row, 0, 1, 1)
            
            col += 1
            score = QLabel(str(t['total']))
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

if __name__ == "__main__":

    rules = ['Have Fun', 'Don\'t cheat']

    app = QApplication(sys.argv)
    window = GameDashboard(rules)
    window.show()
    app.exec()
