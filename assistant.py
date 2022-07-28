import sys
import re

phone_pattern = "\+?[-\s]?(?:\d{2,3})?[-\s]?(?:\([-\s]?\d{2,3}[-\s]?\)|\d{2,3})?[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3}"

phone_book = {
}


errors = {
    "not_found": lambda *_: "Sorry I can't understand you. Use 'help' to see what I can.",
    "missing_name": lambda *_: "It seems that you missed the name of contact. Please, try again.",
    "missing_number": lambda *_: """Sorry, I can't identify a valid phone number.
Try 'help' command to see allowed formats.""",
    "name_exists": lambda x: "Contact '{}' already exists. Try 'change' command to rewrite it.".format(x),
    "name_not_found": lambda x: "Contact '{}' does not exist. Try 'add' command to create a new contact.".format(x),
    "invalid_number": lambda x: "It seems that '{}' is not a valid phone number. Please, try again"
                                " or type 'help' to know more about supported formats of phone number. ".format(x),
    "invalid_contact": lambda x: "Contact '{}' does not exist. Try 'add' him to your phone book.".format(x),
    "name_number": lambda x: "'{}' expects name and phone number as keys.".format(x),
}


def find_name_number(text: str):  # return tuple of name and number
    pattern = re.compile(phone_pattern)
    only_name = text
    if not pattern.findall(text):
        return find_name(text), ""
    for x in pattern.findall(text):
        only_name = only_name.replace(x, "")
    return find_name(only_name), str(pattern.findall(text)[0]).strip().replace(" ", "").replace("", ""),


def find_name(text: str):  # converts text into name. Should be used only after the numer has been extracted.
    return text.strip().lower().title()


def log_decorator(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Exception):
            return result
        errcode = result[0] if type(result) == tuple else result
        if errcode in errors.keys():
            return errors[errcode](result[1] if type(result) == tuple else " ")
        else:
            return result
    return inner


@log_decorator
def show_all(*_):
    try:
        out = ""
        if not phone_book:
            return "Your phone book is empty."
        for name in phone_book.keys():
            out += name + ": " + phone_book[name] + "\n"
        return out
    except Exception as err:
        return err


@log_decorator
def add(data: str):
    try:
        name, number = find_name_number(data)
        if not name:
            return "missing_name", "add"
        if name in phone_book.keys():
            return "name_exists", name
        if not number:
            return "missing_number"
        else:
            phone_book[name] = number
            return f"Contact '{name}': '{number}' has been added to your phone book."
    except Exception as err:
        return err


@log_decorator
def change(data: str):
    try:
        name, number = find_name_number(data)
        if not name:
            return "missing_name", "add"
        if name not in phone_book.keys():
            return "name_not_found", name
        if not number:
            return "missing_number"
        else:
            phone_book.update({name: number})
            return f"Contact '{name}' has been changed to '{number}'."
    except Exception as err:
        return err


@log_decorator
def phone(data: str):
    try:
        name = find_name(data)
        if not name:
            return "missing_name"
        if name not in phone_book.keys():
            return "invalid_contact", name
        else:
            return str(phone_book[name])
    except Exception as err:
        return err


def help_me(*_):
    return f'''\t\t\thello -- replies to the console "How can I help you?".
            add 'name' 'number' -- create a new contact 'name' with phone number 'number'. 
            change 'name' 'number' -- change phone number of 'name' to 'phone number'.
            phone 'name' -- show phone number of contact 'name'.
            show all -- show all contacts.
            
            * 'name' can be more that one word and must contain at least one letter.
            'name' will be saved in title format (e.g. Musfer Adzhymambetov). 
            
            ** popular allowed phone numer formats:
                +38 093 12 34 456
                    093 12 344 56
                        123 44 56
                 38 093 12 34 456
                +38 (093) 12 34 456
            hyphens instead of spaces are allowed
            General format using regular expressions:
            '{phone_pattern}'
            
            
            use '.', 'good bye', 'close', or 'exit' to shut down the assistant. '''


commands = {
    "e": lambda *_: sys.exit(),
    "g": lambda *_: (print("Good bye!"), sys.exit()),
    "h": lambda *_: "How can I help you?",
    "a": add,
    "c": change,
    "p": phone,
    "s": show_all,
    "help": help_me,
    "empty": lambda *_: errors['not_found'](),
    0: lambda *_: errors['not_found'](),
}


@log_decorator
def def_mod(string: str):  # returns tuple of mod (user command) and other data (name and phone numer)
    try:
        mods = {
            "hello": "h",
            ".": "e",
            "change": "c",
            "phone": "p",
            "show all": "s",
            "good bye": "g",
            "close": "g",
            "exit": "g",
            "help": "help",
            "add": "a",
        }
        if not string:
            return "empty", ""
        for key_word in mods.keys():
            if key_word in string:
                return mods[key_word], string.replace(key_word, "")
        return 0, ""
    except Exception as err:
        return err


def main():
    print("Welcome to your personal Python assistant!")
    print("What can I do for you today?")
    while True:
        command = input()
        mod, data = def_mod(command)
        print(commands.get(mod)(data))


if __name__ == "__main__":
    main()
