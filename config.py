import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

    db_env_setting = os.environ.get('DATABASE_URL')
    if db_env_setting is not None and db_env_setting.startswith('postgres'):
        db_env_setting = db_env_setting.replace('postgres', 'postgresql')

    DATABASE_URL = db_env_setting or 'sqlite:///' + os.path.join(basedir, 'telegram-bot.db')
