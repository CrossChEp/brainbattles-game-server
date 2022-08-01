from sqlalchemy.orm import Session

from core.middlewares.database_session import generate_session
from core.store.db_model import TaskTable


def get_task_by_id(task_id: int) -> TaskTable:
    session: Session = next(generate_session())
    task = session.query(TaskTable).filter_by(id=task_id).first()
    return task
