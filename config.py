import os
import secrets
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Webhook settings
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_TOKEN = secrets.token_urlsafe(32)
WEBHOOK_PATH = f"/webhook"

# Webserver settings
WEB_SERVER_HOST = '::'
WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT'))

# Database settings
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = f"mysql+aiomysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# SqlAlchemy initialize
engine = create_async_engine(DATABASE_URL, echo=True)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
