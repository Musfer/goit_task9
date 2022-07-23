import sys


min_len = 7  # minimal number of digits in phone number

phone_book = {
}


errors = {
    "not_found": lambda *_: "Sorry I can't understand you. Use 'help' to see what I can.",
    "missing_name": lambda *_: "It seems that you missed the name of contact. Please, try again.",
    "missing_number": lambda *_: "Phone number has not been detected.",
    "name_exists": lambda x: "Contact '{}' already exists. Try 'change' command to rewrite it.".format(x),
    "name_not_found": lambda x: "Contact '{}' does not exist. Try 'add' command to create a new contact.".format(x),
    "invalid_number": lambda x: "It seems that '{}' is not a valid phone number. Please, try again"
                                " or type 'help' to know more about supported formats of phone number. ".format(x),
    "invalid_contact": lambda x: "Contact '{}' does not exist. Try 'add' him to your phone book.".format(x),
    "name_number": lambda x: "'{}' expects name and phone number as keys.".format(x),
}


def log_decorator(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Exception):
            return result
        errcode = result[0] if type(result) == tuple else result
        if errcode in errors.keys():

            return "Warning: " + errors[errcode](result[1] if type(result) == tuple else " ")
        else:
            return result
    return inner


def not_a_phone_number(number: str):
    digits = 0
    non_digits = 0
    if number.count("+") > 1:
        return True
    elif number.count("+") == 1 and number[0] != "+":
        return True
    left_b = number.count("(")
    right_b = number.count(")")
    if not(left_b == right_b and (left_b == 1 or left_b == 0)):
        return True
    for i in number:
        if i.isdigit():
            digits += 1
        elif i not in ("-", " ", ")", "(", "+"):
            non_digits += 1
    if digits < min_len or non_digits > 0:
        return True
    return False


def not_a_name(name: str):
    for s in name:
        if s.isalpha():
            return False
    return True


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
def add(command: str):
    try:
        name = " ".join(command.split(" ")[1:-1]).lower().title()
        number = command.split(" ")[-1]
        if len(command.split()) < 3:
            return "name_number", "add"
        if not_a_name(name):
            return "missing_name"
        if not number:
            return "missing_number"
        if not_a_phone_number(number):
            return "invalid_number", number
        elif name in phone_book.keys():
            return "name_exists", name
        else:
            phone_book[name] = number
            return f"Contact '{name}': '{number}' has been added to your phone book."
    except Exception as err:
        return err


@log_decorator
def change(command: str):
    try:
        name = " ".join(command.split(" ")[1:-1]).lower().title()
        number = command.split(" ")[-1]
        if len(command.split()) < 3:
            return "name_number", 'change'
        if not_a_name(name):
            return "missing_name"
        if not number:
            return "missing_number"
        elif not not_a_phone_number(number) and name in phone_book.keys():
            phone_book.update({name: number})
            return f"Contact '{name}' has been changed to '{number}'."
        elif not (name in phone_book.keys()):
            return "name_not_found", name
        else:
            return "invalid_number", number
    except Exception as err:
        return err


@log_decorator
def phone(command: str):
    try:
        if len(command.split()) < 2:
            return "missing_name"
        name = " ".join(command.split(" ")[1:]).lower().title().strip()
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
            
            ** 'number' must contain at least {min_len} digits, not more that one pair of '(' ')' brackets and 
            may start with "+". All other characters except hyphens '-' are not allowed.
            
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
def def_mod(string: str):
    if "." in string:
        return "e"
    elif string.lower() == "hello":
        return "h"
    elif string.lower().startswith("add"):
        return "a"
    elif string.lower().startswith("change"):
        return "c"
    elif string.lower().startswith("phone"):
        return "p"
    elif string.lower().startswith("show all"):
        return "s"
    elif string.lower() in ["good bye", "close", "exit"]:
        return "g"
    elif string.lower() == "help":
        return "help"
    elif not string.strip():
        return "empty"
    else:
        return 0


def main():
    print("Welcome to your personal Python assistant!")
    while True:
        command = input()
        print(commands.get(def_mod(command))(command))


if __name__ == "__main__":
    main()
