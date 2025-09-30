#                            TASK MANAGER COMMAND LINE INTERFACE APPLICATION

import sys
from datetime import datetime

from task_logic.task import Task
from task_logic.task_json import TaskJSON

database = TaskJSON()

# ============================== Input helpers ==============================

#                           Functions:
# ask_task_type(): Ask the user to pick between daily/overall
# ask_task_information(): Collect full task info from user input
# ask_for_task_id_and_validate(): Ask for a task ID and validate it exists

def ask_task_type():
    """Ask the user to pick between daily/overall."""
    while True:
        task_type = input("\nTask type (daily/overall): ").lower().strip()
        if task_type not in ["daily", "overall"]:
            print("\nInvalid task type. Try again.")
        else:
            return task_type

def ask_task_information(ask_type: bool = True, task_type: str | None = None):
    """Collect full task info from user input."""
    
    if ask_type:
        task_type = ask_task_type()
    elif task_type is None:
        raise ValueError("task_type must be provided if ask_type=False")

    task_id = database.get_next_id()
    task_title = input("Task title: ").strip()
    task_description = input("Task description: ").strip()
    task_tags = input("Task tags (comma separated): ").split(",")
    task_tags = [tag.strip() for tag in task_tags if tag.strip()]

    task_deadline = None
    if task_type == "overall":
        while True:
            try:
                task_deadline = input("Task deadline (ex: 2023-01-25 23:59): ").strip()
                task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d %H:%M")
                break
            except ValueError:
                print("\nInvalid date format. Try again.")

    return task_type, task_id, task_title, task_description, task_tags, task_deadline

def ask_for_task_id_and_validate():
    """Ask for a task ID and validate it exists."""
    while True:
        task_id = input("\nEnter task ID: ").strip()
        try:
            task_id = int(task_id)
            if database.does_task_exist(task_id):
                return task_id
            else:
                print("\nTask ID not found. Try again.")
        except ValueError:
            print("\nInvalid task id. Try again.")

# ============================== Task operations ==============================

#                           Functions:
# add_task(): Create and save a new task
# edit_task(): Edit a task
# show_all_tasks(): List tasks by type (daily/overall)
# show_task(): Show full task details by ID

def add_task():
    """Create and save a new task."""
    
    task = Task(*ask_task_information(ask_type=True))  # " *ask_task_information() " unpacks into individual arguments
    database.add_task(task.to_dict(), task.type)
    print("\nTask added successfully.")

def edit_task(task_id, task_type):
    """Edit a task."""
    
    print(f'\nEDITING TASK ID "{task_id}"')
    task = Task(*ask_task_information(ask_type=False, task_type=task_type))
    task.id = task_id 
    database.edit_task(task.to_dict(), task_type)
    

def show_all_tasks(task_type):
    """List tasks by type (daily/overall)."""
    
    tasks_list = database.get_tasks_by_type(task_type)
    
    if not tasks_list:
        print(f"\tNo {task_type} tasks found.")
        return
    
    print(f"\nAvailable {task_type} tasks:")
    print("\t(ID). (Title)")
    for task in tasks_list:
        print(f"\t{task['id']}. {task['title']}")

def show_task(task_id):
    """Show full task details by ID."""
    
    task, task_type = database.get_task_by_id(task_id)
    print(f'\nSHOWING TASK ID "{task["id"]}"')
    print(f"\tTASK TYPE: {task_type}")
    print(f"\tTITLE: {task['title']}")
    print(f"\tDESCRIPTION: {task['description']}")
    print(f"\tTAGS: {task['tags']}")
    print(f"\tCREATED AT: {task['created_at']}")
    print(f"\tDEADLINE: {task['deadline']}" if task['deadline'] else "\tDEADLINE: NO DEADLINE.")
    print(f"\tFINISHED: {task['finished']}")
    if task['finished']:
        print(f"\tFINISHED AT: {task['finished_at']}")

# ============================== Menus ==============================

#                           Functions:
# task_menu(): Submenu for showing tasks and performing operations on them
# single_task_menu(): Submenu for operations on a single task
# main(): Main application menu

def task_menu(task_type):
    """Submenu for showing tasks and performing operations on them."""
    show_all_tasks(task_type)

    print("\nAvailable operations:")
    print("\t0. BACK TO MAIN MENU")
    print("\t1. Show task information by ID")

    choice = input("Choose operation: ")

    if choice == "0": #Done
        return
    elif choice == "1": #Done
        task_id = ask_for_task_id_and_validate()
        single_task_menu(task_id)
    else: #Done
        print("\nInvalid option.")

def single_task_menu(task_id):
    """Submenu for operations on a single task."""
    show_task(task_id)

    task, task_type = database.get_task_by_id(task_id)

    print(f"\nAvailable operations for task {task_id}:")
    print("\t0. BACK TO MAIN MENU")
    print("\t1. Edit task")
    print("\t2. Delete task")
    print("\t3. Mark task as finished")

    choice = input("Choose operation: ")

    if choice == "0": #Done
        return
    elif choice == "1": #Done
        edit_task(task_id, task_type)
        print("\nTask edited successfully.")
    elif choice == "2": #Done
        database.delete_task(task_id, task_type)
        print("\nTask deleted.")
    elif choice == "3": #Done
        database.mark_task_finished(task_id, task_type)
        print("\nTask marked as finished.")
    else:
        print("\nInvalid option.")

def main():
    """Main application menu."""
    while True:
        count_daily_tasks = database.get_tasks_count("daily")
        count_overall_tasks = database.get_tasks_count("overall")
        print("\n========================")
        print(f"Main Menu: (Daily: {count_daily_tasks} - Overall: {count_overall_tasks})")
        print("\t0. Exit")
        print("\t1. Add task")
        print("\t2. Show tasks")
        print("\t3. Reset daily tasks")
        print("\t4. Reset overall tasks")
        print("\t5. Reset tags")
        choice = input("Choose operation: ")

        if choice == "0": #Done
            print("\nExiting program...")
            sys.exit(0)
        elif choice == "1": #Done
            add_task()
        elif choice == "2": #Done
            task_type = ask_task_type()
            if database.is_task_type_empty(task_type):
                print(f"\nNo {task_type} tasks available.")
            else:
                task_menu(task_type)
        elif choice == "3": #Done
            database.reset_tasks("daily")
            print("\nDaily tasks cleared.")
        elif choice == "4": #Done
            database.reset_tasks("overall")
            print("\nOverall tasks cleared.")
        elif choice == "5": #Done
            database.reset_tags()
            print("\nAll tags cleared.")
        else: #Done
            print("\nInvalid option.")

# ============================== Entry Point ==============================

if __name__ == "__main__":
    main()
