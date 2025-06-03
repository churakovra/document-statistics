from sqlalchemy import text
from sqlalchemy.orm import Session


class AppRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def connect_to_db(self):
        try:
            with self.db_session as session:
                session.execute(text("select 1;"))
            return True
        except Exception:
            return False
