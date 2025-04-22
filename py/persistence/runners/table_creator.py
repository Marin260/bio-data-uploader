from ..db_connection import engine
from ..entities.base_model import Base

# Creates all tables in the db
Base.metadata.create_all(engine)
