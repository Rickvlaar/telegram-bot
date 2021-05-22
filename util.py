import re


def get_arguments(command: str) -> set[str]:
    args = set()
    if '--' in command:
        args |= set(re.findall(pattern='([-]{2}\\w*)', string=command))
    if '-' in command:
        args |= set(re.findall(pattern='(-{1}\\w{1}(?![\\w]))', string=command))
    return args


def clean_input(command: str, args: set[str]) -> str:
    if command:
        if args:
            for arg in args:
                command = command.replace(arg, '')
        return command.strip().capitalize()
