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
    def _update_jfile(self):
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