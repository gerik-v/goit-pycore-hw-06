from collections import UserDict
import re
from colorama import init, Fore

init(autoreset=True)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return bool(re.match(r"^\d{10}$", value))

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"{Fore.RED}Contact not found."
        except ValueError as ve:
            return f"{Fore.RED}{ve}"
        except IndexError:
            return f"{Fore.RED}Give me name and phone please."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

address_book = AddressBook()

@input_error
def add_contact(args):
    name, phone = args[0], args[1]
    if address_book.find(name):
        return f"{Fore.RED}Contact {name} already exists."
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"{Fore.GREEN}Contact added."

@input_error
def change_contact(args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = address_book.find(name)
    if not record:
        return f"{Fore.RED}Contact {name} not found."
    record.edit_phone(old_phone, new_phone)
    return f"{Fore.GREEN}Contact updated."

@input_error
def show_phone(args):
    name = args[0]
    record = address_book.find(name)
    if not record:
        return f"{Fore.RED}Contact {name} not found."
    return f"{Fore.BLUE}{record}"

def show_all():
    if not address_book:
        return f"{Fore.RED}No contacts found."
    return "\n".join([f"{Fore.BLUE}{str(record)}" for record in address_book.values()])

def main():
    print(f"{Fore.BLUE}Welcome to the assistant bot!")
    while True:
        user_input = input(f"{Fore.WHITE}Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit", "bye"]:
            print(f"{Fore.BLUE}Good bye!")
            break

        elif command in ["hello", "hi"]:
            print(f"{Fore.BLUE}How can I help you?")

        elif command == "add":
            if len(args) < 2:
                print(f"{Fore.RED}Invalid command. Usage: add [name] [phone]")
            else:
                print(add_contact(args))

        elif command == "change":
            if len(args) < 3:
                print(f"{Fore.RED}Invalid command. Usage: change [name] [old_phone] [new_phone]")
            else:
                print(change_contact(args))

        elif command == "phone":
            if len(args) < 1:
                print(f"{Fore.RED}Invalid command. Usage: phone [name]")
            else:
                print(show_phone(args))

        elif command == "all":
            print(show_all())

        else:
            print(f"{Fore.RED}Invalid command.")

if __name__ == "__main__":
    main()
