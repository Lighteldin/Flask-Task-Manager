import json
import os

class TaskJSON:
    JFILE = 'data.json'

    def __init__(self):
        self.tasks = {
            "latest_id": 0,
            "tags": [],
            "daily": [],
            "overall": []
        }
        self._setup_json() 

    # ============================== Internal helpers (file + count) ==============================
        
    def _setup_json(self): # creates the json file if it doesn't exist
        try:
            if not os.path.exists(self.JFILE):
                self._update_json()
            else:
                with open(self.JFILE, 'r') as jf:
                    self.tasks = json.load(jf)
        except Exception as e:
            print("Error:", e)
            
    def _update_json(self): # updates the json file with current tasks
        with open(self.JFILE, 'w') as jf:
            json.dump(self.tasks, jf, indent=4)
             
    def _increment_id(self): # increments the task id and returns the new id
        self.tasks['latest_id'] += 1
        return self.tasks['latest_id']
    
    def _add_tags(self, new_tags: list):
        for tag in new_tags:
            if tag and tag not in self.tasks['tags']:
                self.tasks['tags'].append(tag)
        self._update_json()
    
    
    # ============================== Task operations ==============================
    
    def add_task(self, new_task: dict, task_type: str):
        if not self.is_new_task_unique(new_task, task_type):
            return

        id = self._increment_id()
        new_task['id'] = id
        self.tasks[task_type].append(new_task)

        self._add_tags(new_task['tags'])
        self._update_json()

    def edit_task(self, edited_task: dict, task_type: str):
        for i, task in enumerate(self.tasks[task_type]):
            if task['id'] == edited_task['id']:
                self.tasks[task_type][i] = edited_task
                self._add_tags(edited_task['tags'])
                self._update_json()
                return

    def delete_task(self, task_id: int, task_type: str):
        for i, task in enumerate(self.tasks[task_type]):
            if task['id'] == task_id:
                del self.tasks[task_type][i]
                self._update_json()
                return

    # ============================== Reset operations ==============================
    
    def reset_tasks(self, task_type: str):
        if task_type == 'daily':
            self.tasks["daily"].clear()
        elif task_type == 'overall':
            self.tasks["overall"].clear()
        self._update_json()

    def reset_tags(self):
        self.tasks["tags"].clear()
        for task_type in ['daily', 'overall']:
            for task in self.tasks[task_type]:
                task['tags'].clear()
        self._update_json()

    
   # ============================== Getters ==============================
    
    def get_next_id(self):
        return self.tasks['latest_id'] + 1

    def get_tags(self): 
        return self.tasks['tags']

    def get_tasks(self, task_type: str): # returns list of tasks of given type
        task_type = task_type.lower().strip()
        if task_type in ['daily', 'overall']:
            return self.tasks[task_type]

    def get_task_by_id(self, task_id: int): # returns "task dict" and "task_type" by id
        for task_type in ['daily', 'overall']:
            for task in self.tasks[task_type]:
                if task['id'] == task_id:
                    return task, task_type
        return None

    def is_new_task_unique(self, new_task: dict, task_type: str):
        for task in self.tasks[task_type]:
            if task['title'] == new_task['title'] or task['id'] == new_task['id']:
                return False
        return True

