import json  
import os

#############
# Variables #
#############

tasks = {
        "undone":[],
        "done":[]
        }


#############
# Constants #
#############

JFILE = "data.json"

EXIT = -1
ADD_TASK = 0
MARK_TASK = 1
SHOW_TASKS = 2
CLEAR_TASKS = 3

#####################
# File Manipulation #
#####################

def update_jfile():
    with open(JFILE, 'w') as jf:
        json.dump(tasks, jf, indent=4)

def init() -> bool:
    global tasks
    try:
        if not os.path.exists(JFILE):
            update_jfile()
        else:
            with open(JFILE, 'r') as jf:
                tasks = json.load(jf)
        return True
    except Exception as e:
        print("Error:", e)
        return False

############################
# Operations Functionality #
############################

def add_task(task:str):
    tasks["undone"].append(task)
    print("\tAdded task successfully!")
    update_jfile()
        
def mark_task(task_number:int):
    tasks["done"].append(tasks["undone"][task_number])
    tasks["undone"].pop(task_number)
    print("\tMarked task successfully!")
    update_jfile()

def show_tasks() -> int:
    if len(tasks["undone"]) == 0:
        print("\tNo active tasks available.")
        return 0
    else:
        print(f"\tActive tasks:")
        for i in range(len(tasks["undone"])):
            print(f"\t\t{i}: {tasks['undone'][i]}")
        return 1
                
def clear_tasks():
    tasks["undone"].clear()
    tasks["done"].clear()
    print("Cleared tasks successfully!")
    update_jfile()

    ############################
    # Operations Interactivity #
    ############################

def interact_add():
    print("\nYou've chosen to ADD TASK.")
    new_task = input("New task:")
    add_task(new_task)
        
def interact_mark():
    print("\nYou've chosen to MARK TASK.")
    if show_tasks() == 1:
        while True:
            try:
                task_number = int(input("\n Mark task number:"))
                if task_number in range(len(tasks["undone"])): 
                    mark_task(task_number)
                    return 0
            except ValueError:
                print("!Invalid! Choose a number corresponding to the task.") 
                
def interact_show():
    print("\nYou've chosen to SHOW TASKS.")
    show_tasks()

def interact_clear():
    print("\nYou've chosen to CLEAR TASKS.")
    confirm = input("Are you sure? (y/n): ").lower()
    if confirm in ['y','t','1','yes','true','confirm']:
        clear_tasks()
    else:
        print("Clear cancelled.")

def interact_exit():
    print("\nYou've chosen to EXIT.")
#########
# Other #
#########

def show_options():
    print("\nPlease choose an operation:")
    print("\t-1 = Exit\n0 = Add Task\t1 = Mark Task\n2 = Show Tasks\t3 = Clear Tasks")

def take_input() -> int:
    error_message="!Invalid! Choose a number corresponding to the operation."
    while True:
        try:
            operation = int(input("TYPE HERE:"))
            if operation in [EXIT, ADD_TASK, MARK_TASK, SHOW_TASKS, CLEAR_TASKS]:
                return operation
            else:
                print(error_message)        
        except ValueError:
            print(error_message) 

def perform_operation(operation):
    if operation == ADD_TASK: 
        interact_add()
    elif operation == MARK_TASK: 
        interact_mark()
    elif operation == SHOW_TASKS: 
        interact_show()
    elif operation == CLEAR_TASKS:  
        interact_clear()
    elif operation == EXIT:
        interact_exit()
########
# Main #
########

def main():
    state = init()
    if not state:
        print("!! Found a problem whiles initializing !!")
        return
        
    while True:
        show_options()
        operation = take_input()
        perform_operation(operation)
        if operation == EXIT: 
            return


if __name__ == "__main__":
    main()