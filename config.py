import os
from telegram.utils.request import Request
from telegram.ext import Defaults

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    HHPC_TOKEN = os.environ.get('HHPC_TOKEN')
    HHPC_CHAT_ID = os.environ.get('HHPC_TOKEN')
    MEMBERS = os.environ.get('HHPC_CHAT_ID')

    db_env_setting = os.environ.get('DATABASE_URL')
    if db_env_setting is not None and db_env_setting.startswith('postgres'):
        db_env_setting = db_env_setting.replace('postgres', 'postgresql')

    DATABASE_URL = db_env_setting or 'sqlite:///' + os.path.join(basedir, 'telegram-bot.db')

    DEFAULTS = Defaults(run_async=True)
    REQUEST = Request(con_pool_size=8)
