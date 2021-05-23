import re
from data_model import Base, engine, db_session, Insult
from sqlalchemy.sql.functions import random

def get_arguments(command: str) -> set[str]:
    args = set()
    if '--' in command:
        args |= set(re.findall(pattern='([-]{2}\\w*)', string=command))
    if '-' in command:
        args |= set(re.findall(pattern='(-{1}\\w{1}(?![\\w]))', string=command))
    return args


def process_input(command: str) -> (str, set[str]):
    if not command:
        raise ValueError('Command is required')

    command = re.sub(pattern='([/]\\w*)', repl='', string=command, count=1)
    args = get_arguments(command)
    if args:
        for arg in args:
            command = command.replace(arg, '')

    validate_input(command)
    value = command.strip().capitalize()
    return value, args


def validate_input(command: str) -> None:
    if command is None or len(command) == 0:
        raise ValueError('No input given')


def check_data_model():
    for table_name in Base.metadata.tables:
        if engine.has_table(table_name=table_name):
            pass
        else:
            return False
    return True


# Should only be run one time to build the schema
def create_data_model():
    Base.metadata.create_all(bind=engine)


# Drop all tables if you want to rebuild the data-model
def drop_all_tables(confirmed):
    if confirmed:
        Base.metadata.drop_all(bind=engine)


def get_random_insult(victim: str) -> str:
    session = db_session()
    insult = session.query(Insult).order_by(random()).first().insult
    insult = victim + ' ' + insult
    return insult.lower()
