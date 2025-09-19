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
        self.tags = tags if tags else []
        
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
    
    def mark_as_finished(self):
        self.finished = True
        self.finished_at = datetime.now()

    def mark_as_unfinished(self):
        self.finished = False
        self.finished_at = None
        
    def is_overdue(self):
        if self.deadline and not self.finished:
            return datetime.now() > self.deadline
        return False
    
    def __str__(self):
        status = "Done" if self.finished else "Undone"
        overdue = " (Overdue)" if self.is_overdue() else ""
        deadline_str = self.deadline.strftime("%Y-%m-%d %H:%M") if self.deadline else "No deadline"
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        return (f"[{self.id}] {self.title} - {status}{overdue}\n"
                f"Description: {self.description}\n"
                f"Tags: {tags_str}\n"
                f"Deadline: {deadline_str}\n"
                f"Created at: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n")
    
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
    