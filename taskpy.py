import json  
import os
class TaskPy:
    
    #############
    # Constants #
    #############
    JFILE = "data.json"

    EXIT = -1
    ADD_TASK = 0
    MARK_TASK = 1
    SHOW_TASKS = 2
    CLEAR_TASKS = 3
    
    #############
    # Variables #
    #############

    
        
    ##################
    # Initialization #
    ##################    
    def __init__(self):
        self.tasks = {"undone":[], "done":[]}
        try:
            # Create JSON file if it doesn't exist.
            if not os.path.exists(self.JFILE):
                self.update_jfile() 
            # Load in data from JSON file if it exists.
            else:
                with open(self.JFILE, 'r') as jf:
                    self.tasks = json.load(jf)
        
        except Exception as e:
            print("Error:", e)
        
        
    # Load dictionary into JSON
    def update_jfile(self):
        with open(self.JFILE, 'w') as jf:
            json.dump(self.tasks, jf, indent=4)
        
    ############################
    # Operations Functionality #
    ############################

    def add_task(self, task:str):
        self.tasks["undone"].append(task) # add to UNDONE
        print("\tAdded task successfully!")
        
        self.update_jfile() # Update
        
    def mark_task(self, task_number:int):
        self.tasks["done"].append(self.tasks["undone"][task_number])
        self.tasks["undone"].pop(task_number)
        print("\tMarked task successfully!")
        
        self.update_jfile() # Update

    def show_tasks(self) -> int:
        # If no task exists:
        if len(self.tasks["undone"]) == 0:
            print("\tNo active tasks available.")
            return 0
        
        # If a task exists:
        else:
            print(f"\tActive tasks:")
            for i in range(len(self.tasks["undone"])):
                print(f"\t\t{i}: {self.tasks['undone'][i]}")
            return 1
                
    def clear_tasks(self):
        self.tasks["undone"].clear() # Clear UNDONE
        self.tasks["done"].clear() # Clear DONE
        print("Cleared tasks successfully!")
        
        self.update_jfile() # Update


    ####################################################################################
    #                           FOR TEXT-CONSOLE PROGRAM                               #
    ####################################################################################
    
    ############################
    # Operations Interacting #
    ############################

    def interact_add(self):
        print("\nYou've chosen to ADD TASK.")
        new_task = input("New task:")
        self.add_task(new_task)
        
    def interact_mark(self):
        print("\nYou've chosen to MARK TASK.")
        if self.show_tasks() == 1:
            while True:
                try:
                    task_number = int(input("\n Mark task number:"))
                    if task_number in range(len(self.tasks["undone"])): 
                        self.mark_task(task_number)
                        return 0
                except ValueError:
                    print("!Invalid! Choose a number corresponding to the task.") 
                
    def interact_show(self):
        print("\nYou've chosen to SHOW TASKS.")
        self.show_tasks()

    def interact_clear(self):
        print("\nYou've chosen to CLEAR TASKS.")
        confirm = input("Are you sure? (y/n): ").lower()
        if confirm in ['y','t','1','yes','true','confirm']:
            self.clear_tasks()
        else:
            print("Clear cancelled.")

    def interact_exit(self):
        print("\nYou've chosen to EXIT.")
        
    #########
    # Other #
    #########

    def show_options(self):
        print("\nPlease choose an operation:")
        print("\t-1 = Exit\n0 = Add Task\t1 = Mark Task\n2 = Show Tasks\t3 = Clear Tasks")

    def take_input(self) -> int:
        error_message="!Invalid! Choose a number corresponding to the operation."
        while True:
            try:
                operation = int(input("TYPE HERE:"))
                if operation in [self.EXIT, self.ADD_TASK, self.MARK_TASK, self.SHOW_TASKS, self.CLEAR_TASKS]:
                    return operation
                else:
                    print(error_message)        
            except ValueError:
                print(error_message) 

    def perform_operation(self, operation):
        if operation == self.ADD_TASK: 
            self.interact_add()
        elif operation == self.MARK_TASK: 
            self.interact_mark()
        elif operation == self.SHOW_TASKS: 
            self.interact_show()
        elif operation == self.CLEAR_TASKS:  
            self.interact_clear()
        elif operation == self.EXIT:
            self.interact_exit()