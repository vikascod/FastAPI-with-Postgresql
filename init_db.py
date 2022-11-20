from database import Base, engine
from models import Task


Base.metadata.create_all(engine)