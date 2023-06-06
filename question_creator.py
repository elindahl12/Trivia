#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ethan Lindahl"
__version__ = "0.1.0"
__license__ = "Private"

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from QuestionAnswerWidgets import *
import sqlite3

question_types = ['True/False', 'Multiple Choice', 'Fill in the Blank']
main_categories = ['', 'Movies & T.V.', 'Science', 'Music', 'Nature', 'U.S. History', 'National Parks']
sub_categories = ['', 'None']
difficulty_levels = ['1', '2', '3', '4', '5']

#Create a database or connect to one
conn = sqlite3.connect('trivia_questions.db')
#create a cursor
cursor = conn.cursor()

#define tables for each question type
multiple_choice_table_query = '''CREATE TABLE IF NOT EXISTS MultipleChoiceQuestions(
                                    id INTEGER PRIMARY KEY,
                                    main_category TEXT,
                                    sub_category TEXT,
                                    difficulty INTEGER,
                                    question_notes TEXT,
                                    question TEXT,
                                    answer TEXT,
                                    distractor1 TEXT,
                                    distractor2 TEXT,
                                    distractor3 TEXT
                                    )'''
true_false_table_query = '''CREATE TABLE IF NOT EXISTS TrueFalseQuestions(
                                    id INTEGER PRIMARY KEY,
                                    main_category TEXT,
                                    sub_category TEXT,
                                    difficulty INTEGER,
                                    question_notes TEXT,
                                    question TEXT,
                                    answer TEXT
                                )'''
fill_in_blank_table_query = '''CREATE TABLE IF NOT EXISTS FillInTheBlankQuestions(
                                    id INTEGER PRIMARY KEY,
                                    main_category TEXT,
                                    sub_category TEXT,
                                    difficulty INTEGER,
                                    question_notes TEXT,
                                    question TEXT,
                                    answer1 TEXT,
                                    answer2 TEXT,
                                    answer3 TEXT
                                        )'''

#execute sql command to create tables
cursor.execute(multiple_choice_table_query)
cursor.execute(true_false_table_query)
cursor.execute(fill_in_blank_table_query)

#commit the changes
conn.commit()

#Close the connection
conn.close()


class QuestionCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.question = None
        self.type = None
        self.answer = None
        self.answer2 = None
        self.answer3 = None
        self.distractor1 = None
        self.distractor2 = None
        self.distractor3 = None
        self.main_category = None
        self.sub_category = None
        self.difficulty = None
        self.notes = None

        self.setWindowTitle("Trivia Question Creator")
        mainwidget = QWidget()
        main_layout = QVBoxLayout()
        widget_1 = QWidget()

        self.creator_layout = QGridLayout()
        self.creator_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.creator_layout.setContentsMargins(5, 5, 5, 5)

        self.type_label = QLabel('Question Type')
        self.type_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.type_label, 0, 0, 1, 1)

        self.question_label = QLabel('Question')
        self.question_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.question_label, 0, 1, 1, 1)

        self.correct_label = QLabel('Correct Answer w/ Optional Elaboration')
        self.correct_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.correct_label, 0, 2, 1, 1)

        self.question_type_combo = QComboBox()
        self.question_type_combo.addItems(question_types)
        self.question_type_combo.currentTextChanged.connect(self.question_check)
        self.creator_layout.addWidget(self.question_type_combo, 1, 0, 1, 1)

        self.question_edit = QTextEdit()
        self.question_edit.setMaximumHeight(55)
        self.creator_layout.addWidget(self.question_edit, 1, 1, 1, 1)

        self.correct_answer = QTextEdit()
        self.correct_answer.setMaximumHeight(55)
        self.creator_layout.addWidget(self.correct_answer, 1, 2, 1, 1)

        self.cat_label = QLabel('Main Category')
        self.cat_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.cat_label, 2, 0, 1, 1)

        self.sub_cat_label = QLabel('Sub Category')
        self.sub_cat_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.sub_cat_label, 2, 1, 1, 1)

        self.difficulty_label = QLabel('Difficulty Level')
        self.difficulty_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.difficulty_label, 2, 2, 1, 1)

        self.notes_label = QLabel('Notes for the Game Master')
        self.notes_label.setFixedHeight(50)
        self.creator_layout.addWidget(self.notes_label, 2, 3, 1, 1)

        
        self.main_category_combo = QComboBox()
        self.main_category_combo.setEditable(True)
        self.main_category_combo.addItems(main_categories)
        self.creator_layout.addWidget(self.main_category_combo, 3, 0, 1, 1)

        self.sub_category_combo = QComboBox()
        self.sub_category_combo.setEditable(True)
        self.sub_category_combo.addItems(sub_categories)
        self.creator_layout.addWidget(self.sub_category_combo, 3, 1, 1, 1)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(difficulty_levels)
        self.creator_layout.addWidget(self.difficulty_combo, 3, 2, 1, 1)

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setMaximumBlockCount(255)
        self.notes_edit.setPlaceholderText('Ex. Play a certain song for this question\nList other acceptable answers\nElaboration of answer')
        self.creator_layout.addWidget(self.notes_edit, 3, 3, 1, 1)

        widget_2 = QWidget()

        self.preview_layout = QGridLayout(widget_2)
        self.preview_layout.setContentsMargins(0, 0, 0, 0)

        
        self.add_button = QPushButton('Save')
        self.add_button.clicked.connect(self.save_question)
        self.add_button.setMaximumSize(QSize(150, 75))
        self.preview_layout.addWidget(self.add_button, 1, 1, 1, 1)

        self.preview_button = QPushButton('Show Preview')
        self.preview_button.clicked.connect(self.display_preview)
        self.preview_button.setMaximumSize(150, 75)
        self.preview_layout.addWidget(self.preview_button, 1, 0, 1, 1)

        self.quest_layout_label = QLabel('Question Layout Widget Here')
        

        self.answer_layout_label = QLabel('Answer layout Widget Here')
        

        widget_1.setLayout(self.creator_layout)
        widget_2.setLayout(self.preview_layout)
       
        main_layout.addWidget(widget_1)
        main_layout.addWidget(widget_2)
        mainwidget.setLayout(main_layout)
        self.setCentralWidget(mainwidget)
        

    def display_preview(self):
        question = self.question_edit.toPlainText()
        

        if self.preview_layout.itemAt(2) is None:
            self.preview_button.setText('Hide Preview')
            if self.question_type_combo.currentText() == 'True/False':
                tf_answer = self.correct_answer.toPlainText()
                self.quest_layout = TrueFalseQuestion(question)
                self.answer_layout = TrueFalseAnswer(question, tf_answer)
            elif self.question_type_combo.currentText() == 'Multiple Choice':
                mc_answer = self.correct_edit.text()
                distractor1 = self.other1.text()
                distractor2 = self.other2.text()
                distractor3 = self.other3.text()
                self.quest_layout = MultipleChoiceQuestion(question, mc_answer, distractor1, distractor2, distractor3)
                self.answer_layout = MultipleChoiceAnswer(question, mc_answer)
            else:
                self.quest_layout = FillInBlankQuestion()
                self.answer_layout = FillInBlankAnswer()
            self.preview_layout.addWidget(self.quest_layout, 2, 0, 1, 1)
            self.preview_layout.addWidget(self.answer_layout, 2, 1, 1, 1)
        else:
            self.preview_button.setText('Show Preview')
            self.preview_layout.removeWidget(self.quest_layout)
            self.preview_layout.removeWidget(self.answer_layout)

    def save_question(self): #save to the database

        #Create a database or connect to one
        conn = sqlite3.connect('trivia_questions.db')
        #create a cursor
        cursor = conn.cursor()
        #get total number of items in each table
        mc_count_query = 'SELECT COUNT(*) FROM MultipleChoiceQuestions'
        cursor.execute(mc_count_query)
        total_mc = cursor.fetchone()[0]
        tf_count_query = 'SELECT COUNT(*) FROM TrueFalseQuestions'
        cursor.execute(tf_count_query)
        total_tf = cursor.fetchone()[0]
        fib_count_query = 'SELECT COUNT(*) FROM FillInTheBlankQuestions'
        cursor.execute(fib_count_query)
        total_fib = cursor.fetchone()[0]

        print(f'there are {total_mc} multiple choice quesitons in the database')
        print(f'there are {total_tf} true or false quesitons in the database')
        print(f'there are {total_fib} fill in the blank quesitons in the database')



        self.question = self.question_edit.toPlainText()
        self.type = self.question_type_combo.currentText()
        self.main_category = self.main_category_combo.currentText()
        self.sub_category = self.sub_category_combo.currentText()
        self.difficulty = self.difficulty_combo.currentText()
        self.notes = self.notes_edit.toPlainText()

        if self.type == 'Multiple Choice':
            self.mc_id = int(total_mc) + 1   
            self.mc_answer = self.correct_edit.text()
            self.distractor1 = self.other1.text()
            self.distractor2 = self.other2.text()
            self.distractor3 = self.other3.text()
            self.mc_item = (self.mc_id, self.main_category, self.sub_category, self.difficulty, self.notes, self.question, self.mc_answer, self.distractor1, self.distractor2, self.distractor3)
            self.insert_mc = '''INSERT INTO MultipleChoiceQuestions (
                                            id, main_category, sub_category, difficulty, question_notes, question, answer, distractor1, distractor2, distractor3)
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(self.insert_mc, self.mc_item)
            print(f'{self.mc_id},{self.type},{self.question},{self.mc_answer},{self.distractor1},{self.distractor2},{self.distractor3},{self.main_category},{self.sub_category},{self.difficulty},{self.notes}')
            self.other1.clear()
            self.other2.clear()
            self.other3.clear()
            self.correct_edit.clear()

        elif self.type == 'True/False':
            self.tf_id = int(total_tf) + 1   
            self.answer = self.correct_answer.toPlainText()
            self.tf_item = (self.tf_id, self.main_category, self.sub_category, self.difficulty, self.notes, self.question, self.answer)
            self.insert_tf = '''INSERT INTO TrueFalseQuestions (id, main_category, sub_category, difficulty, question_notes, question, answer)
                                VALUES (?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(self.insert_tf, self.tf_item)
            print(f'{self.tf_id},{self.type},{self.question},{self.answer},{self.main_category},{self.sub_category},{self.difficulty},{self.notes}')
            self.correct_answer.clear()

        elif self.type == 'Fill in the Blank':
            self.fib_id = total_fib + 1
            self.answer1 = self.fib_answer1.text()
            self.answer2 = self.fib_answer2.text()
            self.answer3 = self.fib_answer3.text()
            
            self.fib_item = (self.fib_id, self.main_category, self.sub_category, self.difficulty, self.notes, self.question, self.answer1, self.answer2, self.answer3)
            self.insert_fib = '''INSERT INTO FillInTheBlankQuestions (id, main_category, sub_category, difficulty, question_notes, question, answer1, answer2, answer3)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(self.insert_fib, self.fib_item)
            print(f'{self.fib_id},{self.type},{self.question},{self.answer1},{self.answer2},{self.answer3},{self.main_category},{self.sub_category},{self.difficulty},{self.notes}')
            self.fib_answer1.clear()
            self.fib_answer2.clear()
            self.fib_answer3.clear()
        

        self.question_edit.clear()
        self.main_category_combo.setCurrentIndex(0)
        self.sub_category_combo.setCurrentIndex(0)
        self.difficulty_combo.setCurrentIndex(0)
        self.notes_edit.clear()

        #commit the changes
        conn.commit()

        #Close the connection
        conn.close()
        

    def question_check(self):
        if self.question_type_combo.currentText() == 'Multiple Choice':
            try: 
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.correct_answer)
                self.correct_answer.deleteLater()
            except:
                pass

            try:
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.fib_widget)
                self.fib_widget.deleteLater()
            except:
                pass

            self.correct_label = QLabel('Correct Answer')
            self.creator_layout.addWidget(self.correct_label, 0, 2, 1, 1)

            self.correct_edit = QLineEdit()
            self.correct_edit.setMaxLength(255)
            self.creator_layout.addWidget(self.correct_edit, 1, 2, 1, 1)

            self.other_option_label = QLabel('Distractors')
            self.creator_layout.addWidget(self.other_option_label, 0, 3, 1, 1)
            
            self.other_edit = QWidget()
            self.other_edit_layout = QVBoxLayout()
            self.other_edit_layout.setContentsMargins(0, 0, 0, 0)
            self.other_edit_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.other1 = QLineEdit()
            self.other1.setMaxLength(255)
            self.other2 = QLineEdit()
            self.other2.setMaxLength(255)
            self.other3 = QLineEdit()
            self.other3.setMaxLength(255)
            self.other_edit_layout.addWidget(self.other1)
            self.other_edit_layout.addWidget(self.other2)
            self.other_edit_layout.addWidget(self.other3)
            self.other_edit.setLayout(self.other_edit_layout)
            self.creator_layout.addWidget(self.other_edit, 1, 3, 1, 1)

        elif self.question_type_combo.currentText() == 'Fill in the Blank':
        
            try:
                self.creator_layout.removeWidget(self.other_option_label)
                self.other_option_label.deleteLater()
                self.creator_layout.removeWidget(self.other_edit)
                self.other_edit.deleteLater()
            except:
                pass
            try:
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.correct_edit)
                self.correct_edit.deleteLater()
                
            except:
                pass
            try:
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.correct_answer)
                self.correct_answer.deleteLater()
                
            except:
                pass

            self.correct_label = QLabel("Correct Answers")
            self.creator_layout.addWidget(self.correct_label, 0, 2, 1, 1)
            self.fib_widget = QWidget()
            self.fib_layout = QHBoxLayout()
            self.fib_answer1 = QLineEdit()
            self.fib_answer2 = QLineEdit()
            self.fib_answer3 = QLineEdit()
            self.fib_layout.addWidget(self.fib_answer1)
            self.fib_layout.addWidget(self.fib_answer2)
            self.fib_layout.addWidget(self.fib_answer3)
            self.fib_widget.setLayout(self.fib_layout)
            self.creator_layout.addWidget(self.fib_widget, 1, 2, 1, 3)
            
        elif self.question_type_combo.currentText() == 'True/False':
            
            try:
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.correct_edit)
                self.correct_edit.deleteLater()
                self.creator_layout.removeWidget(self.other_option_label)
                self.other_option_label.deleteLater()
                self.creator_layout.removeWidget(self.other_edit)
                self.other_edit.deleteLater()
            except:
                pass

            try:
                self.creator_layout.removeWidget(self.correct_label)
                self.correct_label.deleteLater()
                self.creator_layout.removeWidget(self.fib_widget)
                self.fib_widget.deleteLater()
            except:
                pass

            self.correct_label = QLabel('Correct Answer w/ Optional Elaboration')
            self.creator_layout.addWidget(self.correct_label, 0, 2, 1, 1)
            self.correct_answer = QTextEdit()
            self.correct_answer.setFixedHeight(55)
            self.creator_layout.addWidget(self.correct_answer, 1, 2, 1, 1)
    


if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    window = QuestionCreator()
    window.show()

    app.exec()
