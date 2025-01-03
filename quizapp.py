

import csv
import re


# Function to load CSV data
def load_csv(file_name):
    data = []
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    return data


# Function to write data to CSV
def write_csv(file_name, data):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# Function to validate password strength
def is_valid_password(password):
    """Validates password according to basic security standards."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # At least one uppercase letter
        return False
    if not re.search(r'\d', password):  # At least one digit
        return False
    if not re.search(r'[@#$%^&+=!]', password):  # At least one special character
        return False
    return True


# Function to check if username is unique
def is_unique_username(username, file_name):
    """Checks if the username already exists in the specified CSV file."""
    data = load_csv(file_name)
    for user in data:
        if user[0] == username:
            return False  # Username already exists
    return True


# Admin Functions
def add_new_user():
    username = input("Enter Username: ")

    # Check if username is unique
    if not is_unique_username(username, "users.csv"):
        print("Username already exists. Try again.")
        return

    password = input("Enter Password: ")

    # Validate password
    if not is_valid_password(password):
        print(
            "Password must be at least 8 characters long, include at least one uppercase letter, one digit, and one special character.")
        return

    # Add new user to CSV
    users = load_csv("users.csv")
    users.append([username, password, "0%"])
    write_csv("users.csv", users)
    print(f"User {username} added successfully.")


def add_update_question():
    question_text = input("Enter Question Text: ")
    question_id = len(load_csv("questions.csv")) + 1  # Auto increment ID
    questions = load_csv("questions.csv")
    questions.append([str(question_id), question_text])

    # Add options
    print("Enter 4 options (A, B, C, D):")
    options = []
    for option in ['A', 'B', 'C', 'D']:
        option_text = input(f"{option}: ")
        options.append(option_text)

    # Ensure exactly 4 options
    if len(options) != 4:
        print("Error: You must provide exactly 4 options.")
        return

    # Add correct answer
    correct_answer = input("Enter correct answer (A, B, C, or D): ").upper()

    # Validate correct answer
    if correct_answer not in ['A', 'B', 'C', 'D']:
        print("Error: The correct answer must be one of A, B, C, or D.")
        return

    # Mark the correct answer with []
    options_dict = {'A': options[0], 'B': options[1], 'C': options[2], 'D': options[3]}
    options_line = [str(question_id)] #+ options_dict.values()

    # Ensure only one correct answer
    options_line = [f"[{opt}]" if opt == correct_answer else opt for opt in options_line]
    write_csv("questions.csv", questions)
    write_csv("options.csv", [options_line])
    print("Question and options added/updated successfully.")


def view_participant_results():
    users = load_csv("users.csv")
    print("Participant Results:")
    for user in users:
        print(f"{user[0]} - Score: {user[2]}")


# Participant Functions
def participant_login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Load users and validate login
    users = load_csv("users.csv")
    for user in users:
        if user[0] == username:
            if user[1] == password:
                print("Login successful!")
                return username
            else:
                print("Wrong Password. Please enter the correct password.")
                return None
    print("Please ask the administrator for registration.")
    return None


def take_quiz(username):
    questions = load_csv("questions.csv")
    options = load_csv("options.csv")
    score = 0

    for i, question in enumerate(questions[1:], start=1):  # Skipping header row
        print(f"Question {i}: {question[1]}")
        option_line = options[i]
        print(f"A: {option_line[1]}")
        print(f"B: {option_line[2]}")
        print(f"C: {option_line[3]}")
        print(f"D: {option_line[4]}")

        answer = input("Enter your answer (A/B/C/D): ").upper()

        # Validate the answer (A/B/C/D)
        if answer not in ['A', 'B', 'C', 'D']:
            print("Invalid answer. Please enter A, B, C, or D.")
            continue

        # Validate the entered answer against correct options
        correct_answer = option_line[1:].index(f"[{answer}]")  # Find the correct answer
        if answer == option_line[correct_answer + 1]:
            score += 1
            print("Correct!")
        else:
            print("Wrong answer.")

    total_questions = len(questions) - 1
    percentage = (score / total_questions) * 100
    result = f"{percentage}%"
    print(f"Your result: {result} Passed.")

    # Save score in the users.csv file
    users = load_csv("users.csv")
    for user in users:
        if user[0] == username:
            user[2] = result
    write_csv("users.csv", users)


# Main Program
def main():
    while True:
        print("\n1. Admin Login")
        print("2. Participant Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            # Admin login and functionalities
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")

            # Validate admin credentials (hardcoded for now)
            if admin_username == "admin" and admin_password == "admin123":
                while True:
                    print("\nAdmin Menu:")
                    print("1. Add New User")
                    print("2. Add/Update Questions")
                    print("3. View Participant Results")
                    print("4. Exit")
                    admin_choice = input("Choose an option: ")

                    if admin_choice == '1':
                        add_new_user()
                    elif admin_choice == '2':
                        add_update_question()
                    elif admin_choice == '3':
                        view_participant_results()
                    elif admin_choice == '4':
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid admin credentials.")

        elif choice == '2':
            username = participant_login()
            if username:
                take_quiz(username)

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()















        
    
