from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import date

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[date] = mapped_column(nullable=True)

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
        )

    def check_completion(self):
        if not self.completed_at:
            return False
        return True
    
    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.check_completion()
            )


