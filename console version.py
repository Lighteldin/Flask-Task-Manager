####################################################################################
#                           FOR TEXT-CONSOLE PROGRAM                               #
####################################################################################

import taskpy

tp = taskpy.TaskPy()

############################
# Operations Interacting #
############################


def interact_add():
    print("\nYou've chosen to ADD TASK.")
    new_task = input("New task:")
    tp.add_task(new_task)
        
def interact_mark():
    print("\nYou've chosen to MARK TASK.")
    if tp.show_tasks() == 1:
        while True:
            try:
                task_number = int(input("\n Mark task number:"))
                if task_number in range(len(tp.tasks["undone"])): 
                    tp.mark_task(task_number)
                    return 0
            except ValueError:
                print("!Invalid! Choose a number corresponding to the task.") 
                
def interact_show():
    print("\nYou've chosen to SHOW TASKS.")
    tp.show_tasks()

def interact_clear():
    print("\nYou've chosen to CLEAR TASKS.")
    confirm = input("Are you sure? (y/n): ").lower()
    if confirm in ['y','t','1','yes','true','confirm']:
        tp.clear_tasks()
    else:
         print("Clear cancelled.")

def interact_exit():
    print("\nYou've chosen to EXIT.")
    quit()
        
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
            if operation in [tp.EXIT, tp.ADD_TASK, tp.MARK_TASK, tp.SHOW_TASKS, tp.CLEAR_TASKS]:
                return operation
            else:
                print(error_message)        
        except ValueError:
            print(error_message) 

def perform_operation(operation):
    if operation == tp.ADD_TASK: 
        interact_add()
    elif operation == tp.MARK_TASK: 
        interact_mark()
    elif operation == tp.SHOW_TASKS: 
        interact_show()
    elif operation == tp.CLEAR_TASKS:  
        interact_clear()
    elif operation == tp.EXIT:
        interact_exit()


if __name__ == "__main__":
    while True:
        show_options()
        chosen_operation = take_input()
        perform_operation(chosen_operation)