from sqlalchemy.ext.declarative import declarative_base
from ORM_models import Base,Player  # Assuming Player is defined in models.py
from sql_functions import get_engine_alchemy

# Create the engine to connect to the database
engine = get_engine_alchemy()

# Create all tables defined by the ORM models (this will create tables for all ORM models)
Base.metadata.create_all(engine)

print("Database and tables created successfully!")