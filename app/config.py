import os


DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rpg.db")
