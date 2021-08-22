import re
from typing import Optional
from data_model import Base, engine, db_session, Insult
from sqlalchemy.sql.functions import random


# FIXME: multi-word command values should be in quotes (")
# FIXME: keyword only arguments fail
# TODO: get command-value in more reliable manner
class Command:

    def __init__(self, command_string: str) -> None:
        self.command_string: str = command_string
        self.command: Optional[str] = None
        self.value: Optional[str] = None
        self.value_list: Optional[list[str]] = None
        self.arguments: dict[str, Command.Argument] = {}
        self.separate_command_and_value()
        self.get_arguments()

    # The regular expressions separate the argument and its values
    def get_arguments(self) -> None:
        word_arg_regex = '((?<=[-]{2})\\w*)(.+?(?:(?=(\\s-)|[\\n\\r])|$))'
        letter_arg_regex = '((?<=-{1})\\w{1}(?![\\w]))(.+?(?:(?=(\\s-)|[\\n\\r])|$))'

        match_set = set(re.findall(pattern=word_arg_regex, string=self.command_string))
        match_set |= set(re.findall(pattern=letter_arg_regex, string=self.command_string))

        for match in match_set:
            arg_str = match[0]
            val = match[1].strip()
            arg = self.Argument(argument=arg_str, value=val)
            self.arguments[arg_str] = arg

    def separate_command_and_value(self) -> None:
        match = re.findall(pattern='((?<=[/!])\\w+)(.+?(?:(?=(\\s-)|[\\n\\r])|$))', string=self.command_string)[0]
        command = match[0]
        value = match[1].strip()
        self.command = command
        self.value = value
        self.value_list = value.split(',').strip() if ',' in value else [value]

    def has_args(self) -> bool:
        return len(self.arguments) > 0

    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[0] != '_'}

    class Argument:

        def __init__(self, argument: str, value: str) -> None:
            self.argument = argument
            self.value = value

        def __repr__(self):
            return self.attributes()

        def __str__(self):
            return str(self.attributes())

        def attributes(self):
            return {key: value for key, value in self.__dict__.items() if key[0] != '_'}


def process_input(command_string: str) -> Command:
    validate_input(command_string)
    return Command(command_string=command_string)


def get_insultee_name(command: str):
    match = re.match(pattern='[/!](\\w+)', string=command)
    return match.group(1)


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


def upsert_records(records: list[object]) -> None:
    session = db_session(expire_on_commit=False)
    for record in records:
        session.add(record)
    session.commit()
    session.expunge_all()
    session.close()


def delete_records(records: list[object]) -> None:
    session = db_session()
    for record in records:
        session.delete(record)
    session.commit()
    session.close()


def get_random_insult(victim: str) -> str:
    session = db_session()
    insult = session.query(Insult).order_by(random()).first().insult
    insult = victim + ' ' + insult
    return insult.capitalize()
