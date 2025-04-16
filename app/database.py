from sqlalchemy import create_engine

from app.models.base_db_model import Base
from app.config.preferences import DATABASE_URL


engine = create_engine(url=DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
