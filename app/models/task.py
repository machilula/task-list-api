from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import date

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[date] = mapped_column(nullable=True)

    def check_completion(self):
        if not self.completed_at:
            return False
        return self.completed_at
    
    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.check_completion()
            )


