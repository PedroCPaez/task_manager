"""
This program helps the user to manage tasks.
Takes tasks.txt and user.txt as input files,
If they don't exist, it creates them.
The user has options such as:
    -Register a new user.
    -Add a new task.
    -View all tasks.
    -View my tasks (those of the user who is logged).
    -Edit some details of the tasks, such as the user assigned to task, 
        the due date or the completed status,
        as long as the task has not been completed or has passed the due date.
    And for the 'admin' user, to vizualize statistics and generate output reports.
    -Display the statistics on the screen.
    -Generate reports in output files.
"""


import os
from datetime import datetime, date
from tabulate import tabulate

DATETIME_STRING_FORMAT = "%d-%m-%Y"

def create_user_file_if_not_found():
    """
    Create a user file if not found.
    If the "user.txt" file does not exist, create it and add a default admin user.
    Parameters:    None
    Returns:    None
    """


    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding='utf-8') as default_file:
            default_file.write("admin;password")


def read_users_file():
    """
    Read users' data from the user file.
    Reads the usernames and passwords from the "user.txt" file.
    Parameters:    None
    Returns:    dict: A dictionary containing usernames as keys and passwords as values.
    """


    username_password = {}

    with open("user.txt", 'r', encoding='utf-8') as user_file:
        for line in user_file:
            username, password = line.strip().split(';')
            username_password[username] = password
    return username_password


def separate_line():
    """
    Print a separator line.
    Prints a separator line to improve readability.
    Parameters:    None
    Returns:    None
    """


    print("*-" * 30)


def initial_loggin(user, password):
    """
    Check login credentials.
    Checks if the provided username and password match any user in the system.
    Parameters:    user (str): The username entered by the user.
                    password (str): The password entered by the user.
    Returns:    bool: True if login successful, False otherwise.
    """


    logged_in = False

    username_password = read_users_file()

    if user in username_password:
        if username_password[user] == password:
            print("\n\033[92mSuccessful login!\033[0m\n")
            logged_in = True
        else:
            print("\033[91mIncorrect password.\033[0m")
    else:
        print("\033[91mUser doesn't exist or incorrect password.\033[0m")

    return logged_in


def validate_data_entry(data):
    """
    Validate general input data.
    Validates that the input is not empty.
    Parameters:    data (str): The input data to be validated.
    Returns:    bool: True if the input is valid, False otherwise.
    """


    while True:
        if not data:
            data = input("Plese entry valid data: ")
        else:
            return data


def validate_due_date_input():
    """
    Validate the due date input.
    Ensures that the due date is in the correct format.
    Returns:    datetime: The validated due date.
    """


    while True:
        try:
            task_due_date_str = validate_data_entry(input("Due date of task (DD-MM-YYYY): "))
            due_date_time = datetime.strptime(task_due_date_str, DATETIME_STRING_FORMAT)
            return due_date_time
        except ValueError:
            print("\033[91mInvalid date format. "
                  "Please enter the date in the format DD-MM-YYYY.\033[0m")


def display_main_menu(curr_user):
    """
    Display the main menu.
    Displays the main menu options based on the current user's privileges.
    Parameters:    curr_user (str): The username of the current user.
    Returns:    None
    """


    if curr_user == 'admin':
        options = [
            ["r",  "Register a user"],
            ["a",  "Add a task"],
            ["va", "View all tasks"],
            ["vm", "View my tasks"],
            ["gr", "Generate reports"],
            ["ds", "Display statistics"],
            ["e",  "Exit"]
        ]
        print(tabulate(options, headers=["Option", "Description"], tablefmt="grid"))
    else:
        options = [
            ["r",  "Register a user"],
            ["a",  "Add a task"],
            ["va", "View all tasks"],
            ["vm", "View my tasks"],
            ["e",  "Exit"]
        ]
        print(tabulate(options, headers=["Option", "Description"], tablefmt="grid"))


def registration_user_option(new_user, username_password):
    """
    Register a new user.
    Allows the admin to register a new user with a username and password.
    Parameters:    new_user (str): The username of the new user.
        username_password (dict): A dictionary containing usernames as keys and passwords as values.
    Returns:    None
    """


    while new_user in username_password:
        print("\nUser already exists.\n")
        new_user = validate_data_entry(input("Please enter a different username: "))

    new_password = validate_data_entry(input("New Password: "))
    confirm_password = validate_data_entry(input("Confirm Password: "))

    if new_password == confirm_password:
        print("\n\033[92mNew user added successfully!\033[0m\n")
        username_password[new_user] = new_password
        add_new_user_to_user_file(username_password)


def create_user_pass_dictionary():
    """
    Create a dictionary of usernames and passwords.
    Reads the usernames and passwords from the user file and returns them as a dictionary.
    Parameters:    None
    Returns:    dict: A dictionary containing usernames as keys and passwords as values.
    """


    username_password = read_users_file()
    return username_password


def add_new_user_to_user_file(username_password):
    """
    Add a new user to the user file.
    Writes the updated list of usernames and passwords to the user file.
    Parameters:    username_password (dict): A dictionary containing usernames as keys and passwords as values.
    Returns:    None
    """


    with open("user.txt", "w", encoding='utf-8') as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))


def read_tasks_file():
    """
    Read tasks data from the tasks file.
    Reads the task data from the "tasks.txt" file.
    Parameters:    None
    Returns:    list: A list of task data.
    """


    try:
        with open("tasks.txt", 'r+', encoding='utf-8') as task_file:
            task_data = task_file.read().split("\n")
            task_data = [t.split(";") for t in task_data if t]
    except FileNotFoundError:
        with open("tasks.txt", 'w', encoding='utf-8') as task_file:
            task_data = []

    return task_data


def create_task_list(task_data):
    """
    Create a list of tasks.
    Converts the task data into a list of dictionaries representing individual tasks.
    Parameters:    task_data (list): A list of task data.
    Returns:    list: A list of dictionaries representing tasks.
    """


    task_list = []
    for i, task_components in enumerate(task_data, start=1):
        curr_t = {}
        curr_t['number'] = i
        curr_t['username'] = task_components[1]
        curr_t['title'] = task_components[2]
        curr_t['description'] = task_components[3]
        curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[6] == "Yes" else False
        task_list.append(curr_t)
    return task_list


def assign_task_to_user(username):
    """
    Assign a task to a user.
    Allows the admin to assign a task to a specific user.
    Parameters:    username (str): The username of the user to whom the task will be assigned.
    Returns:    None
    """


    username_password = read_users_file()

    while username not in username_password:
        print("\033[91mUser doesn't exist.\033[0m")
        username = input("\033[91mPlease enter a valid user: \033[0m")


def validate_if_username_registered(task_username, username_password):
    """
    Validate if a username is registered.
    Checks if the provided username is registered in the system.
    Parameters:    task_username (str): The username to validate.
    username_password (dict): A dictionary containing usernames as keys and passwords as values.
    Returns:    str: The validated username.
    """


    while True:
        if task_username in username_password.keys():
            return task_username
        else:
            print("\033[91mUser does not exist.\033[0m")

        task_username = input("\033[91mPlease enter a username already registered: \033[0m")


def add_new_task_to_task_list(task_list, task_username, task_title, task_description, due_date_time, curr_date):
    """
    Add a new task to the task list.
    Creates a new task dictionary and appends it to the task list.
    Parameters:    task_list (list): A list of dictionaries representing tasks.
        task_username (str): The username of the user to whom the task is assigned.
        task_title (str): The title of the task.
        task_description (str): The description of the task.
        due_date_time (datetime): The due date and time of the task.
        curr_date (date): The current date.
    Returns:    list: The updated task list.
    """


    task_number = len(task_list) + 1

    new_task = {
        "number": task_number,
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)

    return task_list


def write_new_task_to_tasks_file(task_list):
    """
    Write new tasks to the tasks file.
    Writes the updated list of tasks to the "tasks.txt" file.
    Parameters:    task_list (list): A list of dictionaries representing tasks.
    Returns:    None
    """


    with open("tasks.txt", "w+", encoding='utf-8') as task_file:
        for i, task in enumerate(task_list, start=1):
            task_data = [
                str(i),
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            task_file.write(";".join(task_data) + "\n")

        print(f"\n\033[92mTask {i} successfully added to output file tasks.txt\033[0m\n")


def create_tasks_file_if_not_found():
    """
    Create tasks file if not found.
    If the "tasks.txt" file does not exist, create it.
    Parameters:    None
    Returns:    None
    """


    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding='utf-8'):
            pass


def view_all_tasks_option(task_list):
    """
    View all tasks.
    Displays all tasks stored in the system.
    Parameters:    task_list (list): A list of dictionaries representing tasks.
    Returns:    None
    """


    if not task_list:
        separate_line()
        print("\033[91mNo tasks available.\033[0m")
        separate_line()
        return

    separate_line()
    print("\033[93mAll Tasks:\033[0m")
    separate_line()
    for task in task_list:
        separate_line()
        task_number = task.get('number') or task.get('task_number')
        if task_number is not None:
            print(f"Task number:\t\t{task_number}")
        else:
            print("Task number:\t\tN/A")
        print(f"Assigned to:\t\t{task['username']}")
        print(f"Title:\t\t\t{task['title']}")
        print(f"Description:\t\t{task['description']}")
        print(f"Due Date:\t\t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Assigned Date:\t\t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed:\t\t{'Yes' if task['completed'] else 'No'}")
        print("")


def view_my_tasks_option(curr_user):
    """
    View tasks assigned to the current user.
    Displays tasks assigned to the current user.
    Parameters:    curr_user (str): The username of the current user.
    Returns:    list: A list of dictionaries representing tasks assigned to the current user.
    """


    task_data = read_tasks_file()
    task_list = create_task_list(task_data)

    found_tasks = False

    my_task_list = []

    separate_line()
    print("\033[93mYour tasks:\033[0m")
    separate_line()
    for i, task in enumerate(task_list, start=1):
        if task['username'] == curr_user:
            found_tasks = True
            separate_line()
            print(f"Task number:\t\t {task['number']}")
            print(f"Task assigned to:\t {task['username']}")
            print(f"Task title:\t\t {task['title']}")
            print(f"Task description:\t {task['description']}")
            print(f"Date assigned:\t\t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Due date:\t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: \t\t {'Yes' if task['completed'] else 'No'}")
            print()
            task['task_number'] = i
            my_task_list.append(task)

    if not found_tasks:
        print("\033[91mNo tasks assigned to you.\033[0m")

    return my_task_list


def edit_task_details(my_task_list, edit_specific_task):
    """
    Edit task details.
    Allows the user to edit specific details of a task.
    Parameters:    my_task_list (list): A list of dictionaries representing tasks assigned to the current user.
    specific_task (str): The number of the specific task to be edited.
    Returns:    list: The updated list of tasks.
    """


    try:
        edit_specific_task = int(edit_specific_task)
    except ValueError:
        print("\033[91mInvalid task number.\033[0m")
        return my_task_list

    task_found = False

    for task in my_task_list:
        if task['task_number'] == edit_specific_task:
            task_found = True
            separate_line()
            print("\033[93mTask details:\033[0m")
            separate_line()
            print(f"Task number:\t\t {task['task_number']}")
            print(f"Task assigned to:\t {task['username']}")
            print(f"Title:\t\t\t {task['title']}")
            print(f"Description:\t\t {task['description']}")
            print(f"Due Date:\t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Assign date:\t\t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed:\t\t {'Yes' if task['completed'] else 'No'}")
            print()

            current_date = datetime.today()

            if (task['completed'] is False) and (task['due_date'] > current_date):
                display_edit_or_complete_menu()
                field_to_edit = input("Please select an option: \n").lower()

                if field_to_edit == 'u':
                    username_password = read_users_file()
                    new_username = validate_data_entry(input("Enter the new username: "))
                    validate_if_username_registered(new_username, username_password)
                    task['username'] = new_username
                    print("\033[92mUsername successfully updated.\033[0m")
                    update_tasks_file(task)

                elif field_to_edit == 'd':
                    new_due_date = validate_due_date_input()
                    task['due_date'] = new_due_date
                    print("\033[92mDue date successfully updated.\033[0m")
                    update_tasks_file(task)

                elif field_to_edit == 'c':
                    new_completed = validate_data_entry(input("To change to completed enter 'Yes': ").lower())
                    if new_completed == "yes":
                        task['completed'] = True
                        print("\033[92mComplete status successfully updated.\033[0m")
                        update_tasks_file(task)
                    else:
                        print("\033[91mNo change made.\033[0m")

                elif field_to_edit == 'e':
                    break

                else:
                    print("\033[91mInvalid option.\033[0m")
                    return my_task_list
            else:
                print("\033[91mTask completed or overdue, can't be edited.\033[0m")
                break

    if not task_found:
        print("\033[91mInvalid task number.\033[0m")

    return my_task_list


def update_tasks_file(specific_task):
    """
    Update tasks file with edited task details.
    Updates the "tasks.txt" file with the edited details of a task.
    Parameters:    specific_task (dict): A dictionary representing the specific task to be updated.
    Returns:    None
    """


    with open("tasks.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        parts = line.split(";")
        if parts[0].strip() == str(specific_task['number']):
            lines[i] = (
                f"{specific_task['number']};"
                f"{specific_task['username']};"
                f"{specific_task['title']};"
                f"{specific_task['description']};"
                f"{specific_task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{specific_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{'Yes' if specific_task['completed'] else 'No'}\n"
            )
            break

    with open("tasks.txt", "w", encoding='utf-8') as file:
        file.writelines(lines)


def display_edit_or_complete_menu():
    """
    Display edit or complete menu.
    Displays the options for editing or completing a task.
    Parameters:    None
    Returns:    None
    """


    edit_options = [
        ["u", "Edit username"],
        ["d", "Edit due date"],
        ["c", "Complete task"],
        ["e", "Exit"]
    ]

    print(tabulate(edit_options, headers=["Opcion", "Description"], tablefmt="grid"))


def generate_reports_option():
    """
    Generate reports.
    Generates reports based on task data and user statistics.
    Parameters:    None
    Returns:    None
    """


    current_date = datetime.today()

    create_user_file_if_not_found()
    username_password = create_user_pass_dictionary()

    task_data = read_tasks_file()
    task_list = []
    total_tasks_completed = 0
    total_tasks_uncompleted = 0
    total_tasks_uncompleted_overdue = 0

    user_stats = {}

    for username in username_password:
        user_stats[username] = {
            'total_tasks_assigned': 0,
            'total_tasks_completed': 0,
            'total_tasks_uncompleted': 0,
            'total_tasks_uncompleted_overdue': 0,
        }

    for i, task_components in enumerate(task_data, start=1):
        curr_t = {
            'number': i,
            'username': task_components[1],
            'title': task_components[2],
            'description': task_components[3],
            'due_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            'assigned_date': datetime.strptime(task_components[5], DATETIME_STRING_FORMAT),
            'completed': task_components[6] == "Yes"
        }
        task_list.append(curr_t)

        if curr_t['completed']:
            total_tasks_completed += 1
            user_stats[curr_t['username']]['total_tasks_completed'] += 1
        else:
            total_tasks_uncompleted += 1
            user_stats[curr_t['username']]['total_tasks_uncompleted'] += 1
            if curr_t['due_date'] <= current_date:
                total_tasks_uncompleted_overdue += 1
                user_stats[curr_t['username']]['total_tasks_uncompleted_overdue'] += 1

        user_stats[curr_t['username']]['total_tasks_assigned'] += 1

    total_tasks = len(task_list)

    percentage_tasks_uncompleted = (total_tasks_uncompleted / total_tasks) * 100 if total_tasks > 0 else 0
    percentage_tasks_overdue = (total_tasks_uncompleted_overdue / total_tasks) * 100 if total_tasks > 0 else 0

    try:
        with open("task_overview.txt", "w", encoding='utf-8') as task_file:
            task_file.write("Task Overview\n\n")
            task_file.write(f"Total number of tasks: \t\t\t\t\t\t\t {total_tasks}\n")
            task_file.write(f"Total number of tasks completed: \t\t\t\t "
                            f"{total_tasks_completed}\n")
            task_file.write(f"Total number of tasks uncompleted: \t\t\t\t "
                            f"{total_tasks_uncompleted}\n")
            task_file.write(f"Percentage of tasks uncompleted: \t\t\t\t "
                            f"{int(percentage_tasks_uncompleted)}%\n")
            task_file.write(f"Total number of tasks uncompleted and overdue: \t "
                            f"{total_tasks_uncompleted_overdue}\n")
            task_file.write(f"Percentage of tasks overdue: \t\t\t\t\t "
                            f"{int(percentage_tasks_overdue)}%\n")
    except IOError:
        print("\033[91mError: It wasn't possible to write in file task_overview.txt\033[0m")

    try:
        with open("user_overview.txt", "w", encoding='utf-8') as user_file:
            user_file.write("User Statistics:\n\n")
            user_file.write(f"Total number of users: \t {len(username_password)}\n")
            user_file.write(f"Total number of tasks: \t {total_tasks}\n")
            for username, stats in user_stats.items():
                total_assigned = stats['total_tasks_assigned']
                total_completed = stats['total_tasks_completed']
                total_uncompleted = stats['total_tasks_uncompleted']
                total_uncompleted_overdue = stats['total_tasks_uncompleted_overdue']

                percentage_assigned = (
                    (total_assigned / total_tasks) * 100
                    if total_tasks > 0 else 0
                )
                percentage_assigned_completed = (
                    (total_completed / total_assigned) * 100
                    if total_assigned > 0 else 0
                )
                percentage_assigned_uncompleted = (
                    (total_uncompleted / total_assigned) * 100
                    if total_assigned > 0 else 0
                )
                percentage_assigned_uncompleted_overdue = (
                    (total_uncompleted_overdue / total_assigned) * 100
                if total_assigned > 0 else 0
                )

                user_file.write(f"\nUsername: \t\t\t\t\t\t\t\t\t\t\t\t"
                                f"{username}\n")
                user_file.write(f"Total tasks assigned: \t\t\t\t\t\t\t\t\t"
                                f"{total_assigned}\n")
                user_file.write(f"Percentage of tasks assigned: \t\t\t\t\t\t\t"
                                f"{int(percentage_assigned)}%\n")
                user_file.write(f"Total tasks completed: \t\t\t\t\t\t\t\t\t"
                                f"{total_completed}\n")
                user_file.write(f"Percentage of tasks assigned and completed: \t\t\t"
                                f"{int(percentage_assigned_completed)}%\n")
                user_file.write(f"Total tasks uncompleted: \t\t\t\t\t\t\t\t"
                                f"{total_uncompleted}\n")
                user_file.write(f"Percentage of tasks assigned and uncompleted: \t\t\t"
                                f"{int(percentage_assigned_uncompleted)}%\n")
                user_file.write(f"Total tasks uncompleted and overdue: \t\t\t\t\t"
                                f"{total_uncompleted_overdue}\n")
                user_file.write(f"Percentage of tasks assigned, uncompleted, and overdue: "
                                f"{int(percentage_assigned_uncompleted_overdue)}%\n")
    except IOError:
        print("\033[91mError: It wasn't possible to write in file user_overview.txt")

    print("\n\033[92mReports task_overview.txt & user_overview.txt"
          " successfully generated!\033[0m\n")


def display_stats_option():
    """
    Display statistics.
    Displays task overview and user statistics.
    Parameters:    None
    Returns:    None
    """


    current_date = datetime.today()

    create_user_file_if_not_found()
    username_password = create_user_pass_dictionary()

    task_data = read_tasks_file()
    task_list = []
    total_tasks_completed = 0
    total_tasks_uncompleted = 0
    total_tasks_uncompleted_overdue = 0

    user_stats = {}

    for username in username_password:
        user_stats[username] = {
            'total_tasks_assigned': 0,
            'total_tasks_completed': 0,
            'total_tasks_uncompleted': 0,
            'total_tasks_uncompleted_overdue': 0,
        }

    for i, task_components in enumerate(task_data, start=1):
        curr_t = {
            'number': i,
            'username': task_components[1],
            'title': task_components[2],
            'description': task_components[3],
            'due_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            'assigned_date': datetime.strptime(task_components[5], DATETIME_STRING_FORMAT),
            'completed': task_components[6] == "Yes"
        }
        task_list.append(curr_t)

        if curr_t['completed']:
            total_tasks_completed += 1
            user_stats[curr_t['username']]['total_tasks_completed'] += 1
        else:
            total_tasks_uncompleted += 1
            user_stats[curr_t['username']]['total_tasks_uncompleted'] += 1
            if curr_t['due_date'] <= current_date:
                total_tasks_uncompleted_overdue += 1
                user_stats[curr_t['username']]['total_tasks_uncompleted_overdue'] += 1

        user_stats[curr_t['username']]['total_tasks_assigned'] += 1

    total_tasks = len(task_list)

    percentage_tasks_uncompleted = (total_tasks_uncompleted / total_tasks) * 100 if total_tasks > 0 else 0
    percentage_tasks_overdue = (total_tasks_uncompleted_overdue / total_tasks) * 100 if total_tasks > 0 else 0

    print("")
    separate_line()
    print("\033[93mTask Overview\033[0m")
    separate_line()
    print(f"Total number of tasks: \t\t\t\t {total_tasks}")
    print(f"Total number of tasks completed: \t\t {total_tasks_completed}")
    print(f"Total number of tasks uncompleted: \t\t {total_tasks_uncompleted}")
    print(f"Percentage of tasks uncompleted: \t\t {int(percentage_tasks_uncompleted)}%")
    print(f"Total number of tasks uncompleted and overdue: \t {total_tasks_uncompleted_overdue}")
    print(f"Percentage of tasks overdue: \t\t\t {int(percentage_tasks_overdue)}%")
    print("")

    separate_line()
    print("\033[93mUser Statistics:\033[0m")
    separate_line()
    total_users = len(username_password)
    print(f"Total number of users: \t {total_users}")
    print(f"Total number of tasks: \t {total_tasks}")

    for username, stats in user_stats.items():
        total_assigned = stats['total_tasks_assigned']
        total_completed = stats['total_tasks_completed']
        total_uncompleted = stats['total_tasks_uncompleted']
        total_uncompleted_overdue = stats['total_tasks_uncompleted_overdue']

        percentage_assigned = (
            (total_assigned / total_tasks) * 100
            if total_tasks > 0 else 0
        )
        percentage_assigned_completed = (
            (total_completed / total_assigned) * 100
            if total_assigned > 0 else 0
        )
        percentage_assigned_uncompleted = (
            (total_uncompleted / total_assigned) * 100
            if total_assigned > 0 else 0
        )
        percentage_assigned_uncompleted_overdue = (
            (total_uncompleted_overdue / total_assigned) * 100
            if total_assigned > 0 else 0
        )

        separate_line()
        print(f"\nUsername: \t\t\t\t\t\t{username}")
        print(f"Total tasks assigned: \t\t\t\t\t{total_assigned}")
        print(f"Percentage of tasks assigned: \t\t\t\t{int(percentage_assigned)}%")
        print(f"Total tasks completed: \t\t\t\t\t{total_completed}")
        print(f"Percentage of tasks assigned and completed: \t\t{int(percentage_assigned_completed)}%")
        print(f"Total tasks uncompleted: \t\t\t\t{total_uncompleted}")
        print(f"Percentage of tasks assigned and uncompleted: \t\t{int(percentage_assigned_uncompleted)}%")
        print(f"Total tasks uncompleted and overdue: \t\t\t{total_uncompleted_overdue}")
        print(f"Percentage of tasks assigned, uncompleted, and overdue: "
              f"{int(percentage_assigned_uncompleted_overdue)}%")


def main():
    """
    Main function.
    The main function of the task management system.
    Parameters:    None
    Returns:    None
    """


    create_user_file_if_not_found()
    username_password = create_user_pass_dictionary()

    task_data = read_tasks_file()
    task_list = create_task_list(task_data)

    DATETIME_STRING_FORMAT = "%d-%m-%Y"

    user_option = ""
    edit_specific_task = ""

    while True:

        if user_option == "e":
            break

        print("")
        separate_line()
        print("\033[93mPlease LOGIN\033[0m")
        separate_line()
        curr_user = validate_data_entry(input("Username: "))
        curr_pass = validate_data_entry(input("Password: "))

        if initial_loggin(curr_user, curr_pass) is False:
            print("\033[91mVerify your data and try again.\033[0m")
            break

        while True:
            if edit_specific_task != "-1":
                display_main_menu(curr_user)

            user_option = validate_data_entry(input("Select an option from the main menu: ")).lower()

            if user_option == "r":
                new_username = validate_data_entry(input("New Username: "))
                registration_user_option(new_username, username_password)

            elif user_option == "a":
                task_username = input("Name of person assigned to task: ")
                validated_username = validate_if_username_registered(task_username, username_password)
                task_title = validate_data_entry(input("Title of Task: "))
                task_description = validate_data_entry(input("Description of Task: "))
                task_due_date = validate_due_date_input()
                curr_date = date.today()

                add_new_task_to_task_list(
                    task_list, validated_username, task_title, task_description,
                    task_due_date, curr_date
                    )

                write_new_task_to_tasks_file(task_list)

            elif user_option == "va":
                task_data = read_tasks_file()
                task_list = create_task_list(task_data)
                view_all_tasks_option(task_list)

            elif user_option == "vm":
                my_task_list = view_my_tasks_option(curr_user)

                edit_specific_task = validate_data_entry(input("\nIf you want to access to any of your tasks,"
                                    "Enter the task number, "
                                    "or enter -1 to go back to Main Menu: \n"))

                if edit_specific_task == "-1":
                    display_main_menu(curr_user)
                else:
                    edit_task_details(my_task_list, edit_specific_task)

            elif (user_option == "gr") and (curr_user == 'admin'):
                generate_reports_option()

            elif (user_option == "ds") and (curr_user == 'admin'):
                display_stats_option()

            elif user_option == "e":
                print("\033[91mGoodbye!!!\033[0m")
                break

            else:
                print("\033[91mInvalid option.\033[0m")

if __name__ == "__main__":
    main()
