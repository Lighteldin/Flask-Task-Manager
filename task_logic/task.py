from datetime import datetime
import sys

class Task:
    def __init__(self,
                type: str,
                id: int,
                title: str,
                description: str,
                tags: list | None = None,
                deadline: datetime | None = None
                ):
        self.type = type
        self.id = id
        self.title = title
        self.description = description if description is not None else ""
        self.tags = list({tag for tag in (tags or []) if tag}) # remove empty tags and duplicates
        
        if not deadline:
            self.deadline = None 
        else:
            if isinstance(deadline, str):
                self.deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            else:
                self.deadline = deadline  # already datetime
        
        self.created_at = datetime.now()
        self.finished = False
        self.finished_at = None
    
    # ==================================================================
    # Operations
    # ==================================================================

    def toggle_finished(self):
        """Toggles the finished status of a task."""
        
        if self.finished:
            self.finished = False
            self.finished_at = None
        else:
            self.finished = True
            self.finished_at = datetime.now()
        
    def add_tag(self, tag: str):
        """Adds a tag to the list of tags."""
        
        if tag not in self.tags:
            self.tags.append(tag)
            
    def remove_tag(self, tag: str):
        """Removes a tag from the list of tags."""
        
        if tag in self.tags:
            self.tags.remove(tag)
    
    def set_deadline(self, deadline: datetime | str):
        """Sets the deadline."""
        
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        else:
            self.deadline = deadline  # already datetime
    
    def remove_deadline(self):
        """Removes the deadline."""
        self.deadline = None
        
    # ==================================================================
    # Deadline related
    # ==================================================================
        
    def get_time_left(self):
        """Returns the time left until the deadline."""
        
        if not self.deadline:
            return None
        return self.deadline - datetime.now()
        
    def is_overdue(self):
        """Checks if the task is overdue."""
        
        if self.deadline and not self.finished:
            return datetime.now() > self.deadline
        return False
    
    # ==================================================================
    # Serialization
    # ==================================================================
        
    def to_dict(self):
        """Returns the task as a dictionary from a task object."""
        
        return {
            "type": self.type,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "deadline": self.deadline.strftime("%Y-%m-%dT%H:%M") if self.deadline else None,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M"),
            "finished": self.finished,
            "finished_at": self.finished_at.strftime("%Y-%m-%dT%H:%M") if self.finished else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Returns the task as a task object from a dictionary."""
        deadline = datetime.strptime(data["deadline"], "%Y-%m-%dT%H:%M") if data["deadline"] else None
        task = cls(
            type=data["type"],
            id=data["id"],
            title=data["title"],
            description=data["description"],
            tags=data["tags"],
            deadline=deadline
        )
        task.created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M")
        task.finished = data["finished"]
        if task.finished:
            task.finished_at = datetime.strptime(data["finished_at"], "%Y-%m-%dT%H:%M")
        else:
            task.finished_at = None
        return task
    
    