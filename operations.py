import psycopg2
import psycopg2.extras
import re
from cryptography.fernet import Fernet
import random
import matplotlib.pyplot as plt
import numpy as np
import datetime

from pandas.core.common import not_none

#Encription log
key = "ex-un4oLEmt7TrN4i3iHyDXCtT_uNg8-A40MFMPSy4A="
fernet = Fernet(key)

#DB Connection log
connection = psycopg2.connect(
    host="localhost",
    database="TriviaDB",
    user="postgres",  # postgres
    password="admin",
    port="5559" #ATTENTION!!! If you're inspecting this project
    #you might have to change the port!!!
)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

#Here are functions that check the users' input
def tryInt(num):
    try:
        newInt = int(num)
        return newInt
    except:
        _num = input("Enter a valid number ")
        return tryInt(_num)


def usernameCheck():
    """Check that the username doesn't exist in the database"""
    _username = input("Enter a username ")
    cursor.execute(f"SELECT checkUsername('{_username}')")
    ans = cursor.fetchall()[0][0]
    if ans:
        print("This username is taken ",end='\n\n')
        usernameCheck()
    else:
        return _username

def emailCheck():
    """Checking that the email format is valid and doesn't exist in the database"""
    _email = input("Enter your email ")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',_email):
        print("This is not a valid Email ", end='\n\n')
        emailCheck()
    cursor.execute(f"SELECT checkEmail('{_email}')")
    ans = cursor.fetchall()[0][0]
    if ans:
        print("This email is taken ", end='\n\n')
        emailCheck()
    else:
        return _email

def ageCheck():
    """Checking that the age is valid"""
    try:
        age = int(input("Enter your age "))
        if age <= 0:
            print("Enter a real age ")
            ageCheck()
        elif age >= 100:
            print("Aren't you too old to play this ? never mind...")
            return age
        else:
            return age
    except:
        print("You need to enter a number ")
        ageCheck()


def passwordCheck(password: str):
    """Checking that the password was entered correctly used"""
    rePassword = input("Enter the password again ")
    if rePassword == password:
        return
    else:
        print("You entered a different password ",end="\n\n")
        mainMenuInterface()

#----------------------------------------------------------------

#Main Menu Functions
#Main menu number 1
def userSignup():
    """Signing up new user"""
    _username = usernameCheck()
    _email = emailCheck()
    _age = ageCheck()
    _password = input("Enter a password ")
    passwordCheck(_password)
    EncryptedPassword = fernet.encrypt(_password.encode())
    cursor.execute(f"CALL addUser('{_username}','{_email}','{_age}','{EncryptedPassword.decode()}')")
    print("User added successfully !",end='\n\n')


#Main menu number 2
def userLogin():
    """Logging in as an existing user"""
    _username = input("Enter your User name ")
    cursor.execute(f"SELECT checkUsername('{_username}')")
    ans = cursor.fetchall()[0][0]
    if ans:
        _password = input("Enter your password ")
        #_password = fernet.encrypt(_password.encode())
        cursor.execute(f"SELECT password FROM players WHERE username = '{_username}'")
        encryptedPassword = cursor.fetchall()[0][0]
        decryptedPassword = fernet.decrypt(encryptedPassword)
        if _password == decryptedPassword.decode():
            cursor.execute(f"SELECT user_login('{_username}', '{encryptedPassword}')")
            loginAns = cursor.fetchall()[0][0]
            if loginAns == 0:
                print("The password didn't match inside \n")
                mainMenuInterface()
            else:
                preGame(loginAns)
        else:
            print("The password didn't match \n")
            mainMenuInterface()
    else:
        print("This username doesn't exist \n")
        mainMenuInterface()


#Main menu number 3
def gameStats(_id: int = 0):
    """This is displaying the game statistics interface"""
    print("Statistics menu\n")
    print("Type 1 to show how many players played")
    print("Type 2 to show the question that the most players answered correctly ")
    print("Type 3 to show the question that the fewest players answered correctly ")
    print("Type 4 to display the players in order by the number of questions they answered correctly.")
    print("Type 5 to display the players in order by the number of questions they answered totally (Including wrong question).")

    #Including the bonus pie chart
    print("Type 6 to enter a players id to view all of the questions he answered")

    #Bonus + bonus graph
    print("Type 7 to view question stats \n")
    print("Type 8 to go back to the main menu \n")
    action = input('')
    action = tryInt(action)
    getAction(action, 'S')


#The game function
def preGame(_id: int):
    """This function is displaying pregame interface"""
    cursor.execute(f"SELECT username FROM players WHERE player_id = {_id}")
    _username = cursor.fetchall()[0][0]
    print(f"Welcome {_username}")
    cursor.execute(f"SELECT questions_solved FROM players WHERE player_id = '{_id}'")
    ans = cursor.fetchall()[0][0]
    if ans == 0:
        print("Starting a new game! ")
        print("Type 'q' to return to the main menu,\n"
              "Type 's' to display your amount of correct and incorrect answers,\n"
              "Type 'a', 'b', 'c' or 'd' to answer the question \n")
        game(_id)
    elif ans == 20:
        print("You have finished the game, do you wish to play again ? (yes/no) - ")
        while True:
            ansFinish = input('').lower()
            if ansFinish != "yes" and ansFinish != "no":
                print("Type a valid answer ")
            else:
                break
        if ansFinish == 'yes':
            print("Great have fun! ")
            print("Resetting scores...")
            print("Starting a new game! ")
            print("Type 'q' to return to the main menu,\n"
                  "Type 's' to display your amount of correct and incorrect answers,\n"
                  "Type 'a', 'b', 'c' or 'd' to answer the question \n")
            cursor.execute(f"CALL reset_solved({_id})")
            game(_id)
        elif ansFinish == 'no':
            print("OK, your loss I guess...")
            mainMenuInterface(_id)

    else:
        print("Do you wish to restart the game or continue from the point you stopped? ")
        print("Type 1 to restart, 2 to continue \n")

        while True:
            ansFinish = input('').lower()
            if ansFinish != '1' and ansFinish != '2':
                print("Type a valid answer ")
            else:
                break
        if ansFinish == '1':
            print("Alright! ")
            print("Resetting scores...")
            print("Starting a new game! ")
            print("Type 'q' to return to the main menu,\n"
                  "Type 's' to display your amount of correct and incorrect answers,\n"
                  "Type 'a', 'b', 'c' or 'd' to answer the question \n")
            cursor.execute(f"CALL reset_solved({_id})")
            game(_id)
        elif ansFinish == '2':
            print("Alright! ")
            print("Continuing the game... ")
            print("Type 'q' to return to the main menu,\n"
              "Type 's' to display your amount of correct and incorrect answers,\n"
              "Type 'a', 'b', 'c' or 'd' to answer the question \n")
            game(_id)


def unanswered_questions(_id: int):
    """This function returns all unanswered questions by player id"""
    cursor.execute(f"SELECT answered_questions({_id})")
    answered = cursor.fetchall()[0][0]
    unanswered = [i for i in range(1, 21)]
    for i in answered:
        unanswered.remove(i)
    return unanswered


def initQuestion(q_id: int):
    """This function formats the question"""
    cursor.execute(
        f"select question_text, answer_a, answer_b, answer_c, answer_d FROM questions WHERE question_id = {q_id}")
    question = cursor.fetchall()[0]
    questionFormated =(f"{question[0]}\n\n"
                       f"A. {question[1]}\n"
                       f"B. {question[2]}\n"
                       f"C. {question[3]}\n"
                       f"D. {question[4]}\n")
    return questionFormated


def question_interface(player_id: int, question_id: int, question: str):
    """This function is the interface of the question in the game"""
    cursor.execute(f"SELECT correct_answer FROM questions WHERE question_id = {question_id}")
    correct_answer = cursor.fetchall()[0][0]
    print(question, '\n ')
    answer = input("Type answer here - ").lower()
    possibleAnswers = ['a', 'b', 'c', 'd']
    print("\n")
    if answer not in possibleAnswers:
        if answer == 'q':
            return mainMenuInterface(player_id)
        elif answer == 's':
            cursor.execute(f"SELECT answers_amount({player_id})")
            answers = cursor.fetchall()[0][0]
            print(f"You have in total \n{answers[0]} correct answers, and {answers[1]} incorrect answers\n")
            return question_interface(player_id, question_id, question)
        else:
            print("Enter a valid answer please \n")
            return question_interface(player_id, question_id, question)
    else:
        if answer == correct_answer:
            print("Correct! \n")
        else:
            print(f"Incorrect, the correct answer is {correct_answer}")
        print("Next question...\n")
        cursor.execute(f"INSERT INTO player_answers (player_id, question_id, selected_answer, is_correct)"
                       f" VALUES ({player_id}, {question_id}, '{answer}', {answer == correct_answer})")
        return game(player_id)

def game(_id: int):
    """This function is activating the game and sending a RANDOM (BONUS) question id to initiation"""
    unanswered = unanswered_questions(_id)
    if len(unanswered) > 0:
        randomQID = random.choice(unanswered)
        question = initQuestion(randomQID)
        question_interface(_id, randomQID, question)
    else:
        print("You have finished the game! ")
        #update high scores
        high_scores_insert(_id)
        mainMenuInterface(_id)




def high_scores_insert(_id):
    cursor.execute(f"SELECT count(is_correct) FROM players JOIN player_answers pa USING (player_id) "
                   f"WHERE player_id = {_id} AND is_correct = true GROUP BY username")
    solved = cursor.fetchall()
    if len(solved) > 0:
        solved = solved[0][0]
        cursor.execute(f"INSERT INTO high_scores (score_id, player_id) VALUES"
                       f"({solved}, {_id}) "
                       f"ON CONFLICT (score_id)"
                       f"DO UPDATE SET player_id = EXCLUDED.player_id, achieved_at = '{datetime.datetime.now()}'")
    cursor.execute(f"SELECT hs.score_id, p.username, hs.achieved_at FROM players p join high_scores hs using (player_id) ORDER BY score_id DESC")
    ans = cursor.fetchall()
    print(f"\nHIGH SCORES\n")
    print("SCORE   PLAYER   DATE\n")
    for i in ans:
        print(f"{i[0]}   {i[1]}   {str(i[2])[:-7]}")
        print("-----------------------")
def getAction(actSelected, interface: chr, _id: int = 0):
    """This function is the control center of each menu choices
    M- stands for Main menu choices
    S - stands for Statistics choices
    G - stands for the game choices"""
    if interface == 'M':
        match actSelected:
            case 1:
                #User Sign up
                userSignup()
                mainMenuInterface(_id)
            case 2:
                if _id == 0:
                    return userLogin()
                else:
                    return preGame(_id)
            case 3:
                #Statistics menu
                gameStats(_id)
            case 4:
                #Exiting the game
                print("Have a good day! ")
                print('Closing connection...')
                connection.commit()
                cursor.close()
                connection.close()
                print('Connection closed !')
                return
            case _:
                print("This option doesn't exist")
                mainMenuInterface(_id)
    elif interface == 'S':
        match actSelected:
            case 1:
                #Printing the amount of players that played
                cursor.execute("SELECT players_played()")
                print()
                print(cursor.fetchall()[0][0],'players have played so far \n')
                gameStats(_id)
            case 2:
                cursor.execute("select easiest_question()")
                questions = cursor.fetchall()[0][0]
                for i in questions:
                    print(initQuestion(i),'\n')
                gameStats(_id)
            case 3:
                cursor.execute("select hardest_question()")
                questions = cursor.fetchall()[0][0]
                for i in questions:
                    print(initQuestion(i), '\n')
                gameStats(_id)
            case 4:
                cursor.execute("SELECT * FROM most_answered_correctly_view")
                print(cursor.fetchall(), '\n')
                gameStats(_id)
            case 5:
                cursor.execute("SELECT * FROM most_answered_totally_view")
                print(cursor.fetchall(), '\n')
                gameStats(_id)
            case 6:
                while True:
                    try:
                        player_id = int(input("Enter the players id \n"))
                        while True:
                            cursor.execute(f"SELECT player_id from players where player_id = {player_id}")
                            res = cursor.fetchall()[0][0]
                            cursor.execute(f"SELECT questions_solved from players where player_id = {player_id}")
                            solved = cursor.fetchall()[0][0]
                            if res == player_id and solved > 0:
                                cursor.execute(f"SELECT question_text, is_correct FROM questions JOIN player_answers pa USING (question_id) WHERE player_id = {player_id}")
                                print("\nTrue for a correct answer, False for an incorrect answer ")
                                ans = cursor.fetchall()
                                print(ans,'\n')

                                # Bonus part matplotlib

                                cursor.execute(f"select question_pie({player_id})")
                                ansplt = cursor.fetchall()[0][0]
                                # Data
                                labels = ['Unanswered', 'Correct', 'Wrong']
                                sizes = [ansplt[0], ansplt[1], ansplt[2]]
                                colors = ['yellowgreen', 'red', 'gold']
                                explode = (0.1, 0, 0)  # To "explode" the first slice

                                # Create a pie chart
                                fig, ax = plt.subplots()
                                ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                                       shadow=True, startangle=90)

                                # Equal aspect ratio ensures that the pie chart is drawn as a circle.
                                ax.axis('equal')

                                # Add a headline
                                ax.set_title("Distribution of answers")

                                # Show the plot
                                plt.show()

                                return gameStats(_id)

                            else:
                                print("This player didn't play yet \n")
                                while True:
                                    try:
                                        player_id = int(input("Enter the players id \n"))
                                        break
                                    except:
                                        print("This players id doesn't exist \n")
                    except:
                        print("This players id doesn't exist \n")

            case 7:
                cursor.execute("SELECT * FROM question_stats")
                ans = cursor.fetchall()
                for i in ans:
                    print(f'Question: {i[0]}, Total answers: {i[1]}, Correct answers: {i[2]}, Incorrect answers: {i[3]}')
                print()
                # Data for the histogram
                questions = np.arange(1, 21)  # Questions from 1 to 20
                cursor.execute("SELECT * FROM question_stats")
                ansplt = cursor.fetchall()
                answered = []
                correct = []
                incorrect = []
                a = 0
                c = 0
                w = 0
                for i in ansplt:
                    a = i[1]
                    c = i[2]
                    w = i[3]
                    answered.append(i[1])
                    if c is None:
                        c = 0
                    correct.append(c)
                    if w is None:
                        w = 0
                    incorrect.append(w)
                # Create the histogram
                bar_width = 0.2
                r1 = np.arange(len(questions))
                r2 = [x + bar_width for x in r1]
                r3 = [x + bar_width for x in r2]

                plt.bar(r1, answered, color='blue', width=bar_width, edgecolor='grey', label='Answered')
                plt.bar(r2, correct, color='green', width=bar_width, edgecolor='grey', label='Correct')
                plt.bar(r3, incorrect, color='red', width=bar_width, edgecolor='grey', label='Wrong')

                # Add labels and title
                plt.xlabel('Questions', fontweight='bold')
                plt.ylabel('Number of Responses', fontweight='bold')
                plt.title('Responses to Questions 1-20: Answered, Correct, and Wrong')
                plt.xticks([r + bar_width for r in range(len(questions))], questions)
                plt.yticks(np.arange(0, max(answered) + 1, 1))
                # Show the legend
                plt.legend()

                # Display the graph
                plt.tight_layout()
                plt.show()
                return gameStats(_id)
            case 8:
                return mainMenuInterface(_id)
            case _:
                print("This option doesn't exist")
                gameStats()


def mainMenuInterface(_id: int = 0):
    """This function is displaying the main menu interface"""
    print("\n\n\nHello and welcome to my humble trivia game! ")
    print("The game includes 20 trivia questions ")
    print("Type 1 to sign up as a new player")
    print("Type 2 to log in as an existing player, or start the game if you already logged in")
    print("Type 3 to display statistics")
    print("Type 4 to exit the game")
    action = input('')
    action = tryInt(action)
    getAction(action, 'M', _id)











