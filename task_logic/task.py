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
    
    # ============================== Operations ==============================
    
    def mark_as_finished(self):
        self.finished = True
        self.finished_at = datetime.now()

    def mark_as_unfinished(self):
        self.finished = False
        self.finished_at = None
        
    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
            
    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
    
    def set_deadline(self, deadline: datetime | str):
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        else:
            self.deadline = deadline  # already datetime
    
    def remove_deadline(self):
        self.deadline = None
        
    # ============================== Deadline ==============================
        
    def get_time_left(self):
        if not self.deadline:
            return None
        return self.deadline - datetime.now()
        
    def is_overdue(self):
        if self.deadline and not self.finished:
            return datetime.now() > self.deadline
        return False
    
    # ============================== Serialization ==============================
        
    def to_dict(self):
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
    
    