import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                            'telegram-bot.db')


def ready_env():
    if not os.path.exists(basedir + '/pleepapier.txt'):
        plee = open('pleepapier.txt', 'w')
        plee.close()

    if not os.path.exists(basedir + '/reservelijst.txt'):
        plee = open('reservelijst.txt', 'w')
        plee.close()
