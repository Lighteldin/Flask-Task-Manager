#                            TASK MANAGER JSON DATABASE (v1.0.0)

import json
import os
from datetime import datetime

class TaskJSON:
    JFILE = './task_data/data.json'

    def __init__(self):
        self.tasks = {
            "latest_id": 0,
            "tags": [],
            "daily": [],
            "overall": []
        }
        self._setup_json() 

    # ==================================================================
    # Internal helpers (file + count)
    #                           Functions:
    # _setup_json() -> Creates the json file if it doesn't exist and loads the tasks from it.
    # _update_json() -> Saves the tasks to the json file.
    # _increment_id() -> Returns the next available id.
    # _add_tags() -> Adds new tags to the list of tags.
    # ==================================================================
        
    def _setup_json(self):
        """Creates the json file if it doesn't exist and loads the tasks from it."""
        
        try:
            if not os.path.exists(self.JFILE):
                self._update_json()
            else:
                with open(self.JFILE, 'r') as jf:
                    self.tasks = json.load(jf)
        except Exception as e:
            print("Error:", e)
            
            
    def _update_json(self):
        """Saves the tasks to the json file."""
        
        with open(self.JFILE, 'w') as jf:
            json.dump(self.tasks, jf, indent=4)
        
             
    def _increment_id(self):
        """Returns the next available id."""
        
        self.tasks['latest_id'] += 1
        return self.tasks['latest_id']
    
    
    def _add_tags(self, new_tags: list):
        """Adds new tags to the list of tags."""
        
        for tag in new_tags:
            if tag and tag not in self.tasks['tags']:
                self.tasks['tags'].append(tag)
        self._update_json()
    
    
    # ==================================================================
    # Task Operations
    #                           Functions:
    # add_task() -> Adds a new task to the list of tasks.
    # edit_task() -> Edits an existing task in the list of tasks.
    # delete_task() -> Deletes a task from the list of tasks.
    # toggle_task_finished() -> Toggles the finished status of a task.
    # ==================================================================
    
    def add_task(self, new_task: dict, task_type: str):
        """Adds a new task to the list of tasks."""
        
        if not self.is_new_task_unique(new_task, task_type):
            return

        id = self._increment_id()
        new_task['id'] = id
        self.tasks[task_type].append(new_task)

        self._add_tags(new_task['tags'])
        self._update_json()


    def edit_task(self, edited_task: dict, task_type: str):
        """Edits an existing task in the list of tasks."""
        
        for i, task in enumerate(self.tasks[task_type]):
            if task['id'] == edited_task['id']:
                self.tasks[task_type][i] = edited_task
                self._add_tags(edited_task['tags'])
                self._update_json()
                return


    def delete_task(self, task_id: int, task_type: str):
        """Deletes a task from the list of tasks."""
        
        for i, task in enumerate(self.tasks[task_type]):
            if task['id'] == task_id:
                del self.tasks[task_type][i]
                self._update_json()
                return
            
            
    def toggle_task_finished(self, task_id: int, task_type: str):
        """Toggles the finished status of a task."""
        
        for task in self.tasks[task_type]:
            if task['id'] == task_id:
                task['finished'] = not task['finished']
                if task['finished']:
                    task['finished_at'] = datetime.now().strftime("%Y-%m-%dT%H:%M")
                else:
                    task['finished_at'] = None
                self._update_json()
                return
    
            
    # ==================================================================
    # Reset Operations
    #                           Functions:
    # reset_tasks() -> Resets all tasks of a given type (daily/overall) to empty list.
    # reset_tags() -> Resets all tags to empty list.
    # ==================================================================
    
    def reset_tasks(self, task_type: str):
        """Resets all tasks of a given type (daily/overall) to empty list."""
        
        if task_type == 'daily':
            self.tasks["daily"].clear()
        elif task_type == 'overall':
            self.tasks["overall"].clear()
        self._update_json()


    def reset_tags(self):
        """Resets all tags to empty list."""
        
        self.tasks["tags"].clear()
        for task_type in ['daily', 'overall']:
            for task in self.tasks[task_type]:
                task['tags'].clear()
        self._update_json()
        
    def reset_daily_finished(self):
        """Resets all daily tasks that were finished before today."""
        
        today = datetime.now().date()
        tasks_reset = False  # Track if anything changed

        for task in self.tasks['daily']:
            if task['finished'] and task.get('finished_at'):
                finished_at = datetime.strptime(task['finished_at'], "%Y-%m-%dT%H:%M")
                
                # If task was finished on a previous day
                if finished_at.date() < today:
                    task['finished'] = False
                    task['finished_at'] = None
                    tasks_reset = True

        if tasks_reset:
            self._update_json()


    # ==================================================================
    # Getters/Checkers
    #                           Functions:
    # get_next_id() -> Returns the next available id.
    # get_tags() -> Returns the list of tags.
    # get_tasks_count() -> Returns the number of tasks of a given type.
    # get_tasks_by_type() -> Returns the list of tasks of a given type.
    # get_task_by_id() -> Returns the task with the given id.
    # is_new_task_unique() -> Checks if the new task is unique.
    # is_task_type_empty() -> Checks if the task type is empty.
    # does_task_exist() -> Checks if the task exists.
    # ==================================================================
    
    def get_next_id(self):
        """Returns the next available id."""
        
        return self.tasks['latest_id'] + 1


    def get_tags(self):
        """Returns the list of tags."""
        
        return self.tasks['tags']


    def get_tasks_count(self, task_type: str):
        """Returns the number of tasks of a given type."""
        
        return len(self.tasks[task_type])


    def get_tasks_by_type(self, task_type: str): 
        """Returns the list of tasks of a given type."""
        
        task_type = task_type.lower().strip()
        if task_type in ['daily', 'overall']:
            return self.tasks[task_type]


    def get_task_by_id(self, task_id: int):
        """Returns the task with the given id."""
        
        for task_type in ['daily', 'overall']:
            for task in self.tasks[task_type]:
                if task['id'] == task_id:
                    return task, task_type
        return None


    def is_new_task_unique(self, new_task: dict, task_type: str):
        """Checks if a new task is unique (title or id)."""
        
        for task in self.tasks[task_type]:
            if task['title'] == new_task['title'] or task['id'] == new_task['id']:
                return False
        return True
    
    
    def is_task_type_empty(self, task_type: str):
        """Checks if a task type is empty."""
        
        return len(self.tasks[task_type]) == 0
    
    
    def does_task_exist(self, task_id: int):
        """Checks if a task with the given id exists."""
        
        for task_type in ['daily', 'overall']:
            for task in self.tasks[task_type]:
                if task['id'] == task_id:
                    return True
        return False