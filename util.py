import re
from data_model import Base, engine

def get_arguments(command: str) -> set[str]:
    args = set()
    if '--' in command:
        args |= set(re.findall(pattern='([-]{2}\\w*)', string=command))
    if '-' in command:
        args |= set(re.findall(pattern='(-{1}\\w{1}(?![\\w]))', string=command))
    return args


def clean_input(command: str, args: set[str] = None) -> str:
    if command:
        if args:
            for arg in args:
                command = command.replace(arg, '')
        return command.strip().capitalize()


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
