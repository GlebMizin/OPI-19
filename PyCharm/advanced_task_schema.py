#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jsonschema
import json
import sys
from jsonschema import validate

schema = {
    "type": "object",
    "title": "MySchema",
    "required": [
        "s_b_a",
        "b_a",
        "t_a"
    ],
    "properties": {
        "s_b_a": {"type": "number"},
        "b_a": {"type": "number"},
        "t_a": {"type": "number"}
    },
}


def validating(check_data):
    try:
        validate(instance=check_data, schema=schema)
    except jsonschema.exceptions.ValidationError:
        err = "JSON data is not correct"
        return False, err

    message = "JSON data is correct"
    return True, message


def get_bank_acc():
    """
    Request for bank account details with verification
    """
    while True:
        s_b_a = input("Enter the sender's bank account: ")
        if len(s_b_a) != 20 or not s_b_a.isdigit():
            print("Incorrect bank account!")
        else:
            break

    while True:
        b_a = input("Enter the beneficiary's account: ")
        if len(b_a) != 20 or not b_a.isdigit():
            print("Incorrect bank account!")
        else:
            break

    t_a = input("Enter transfer amount in ₽: ")

    return {
        "s_b_a": s_b_a,
        "b_a": b_a,
        "t_a": t_a,
    }


def display_acc(accounts):
    """"
    Display of entered bank accounts
    """
    if accounts:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 2,
            '-' * 25,
            '-' * 25,
            '-' * 10
        )
        print(line)
        print(
            '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                "№",
                "Sender bank account",
                "beneficiary account",
                "Amount",
            )
        )
        print(line)

        for ind, requisite in enumerate(accounts, 1):
            print(
                '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                    ind,
                    requisite.get('s_b_a'),
                    requisite.get('b_a'),
                    requisite.get('t_a'),
                )
            )
            print(line)
    else:
        print("You have no bank accounts for now!")


def sum_check(requisites, account):
    """"
    Amount of all money withdrawn
    """
    full_summa = 0
    for sender_req in requisites:

        if int(sender_req.get("s_b_a")) == int(account):
            full_summa += float(sender_req.get("t_a"))

    if full_summa == 0:
        print("This bank account does not exist")
    else:
        print(full_summa)


def save_workers(file_name, accounts):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(accounts, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def help_me():
    print("Command List:\n")
    print("add - Add bank account;")
    print("list - Display a list of bank accounts;")
    print("select <bank account> -", end=" ")
    print("The withdrawn amount from account;")
    print("help - Display Help;")
    print("exit - End the program.")
    print("\n")


def invalid_com():
    print('\n')
    print(f"Invalid command use help", file=sys.stderr)


def main():
    """
    Main function
    """
    requisites = []
    while True:

        command = input("Enter Command: ").lower()
        if command == "exit":
            break

        elif command == "add":
            requisite = get_bank_acc()
            requisites.append(requisite)

            if len(requisites) > 1:
                requisites.sort(key=lambda item: item.get("s_b_a", ""))

        elif command == "list":
            display_acc(requisites)

        elif command.startswith("select "):
            parts = command.split(" ", maxsplit=1)
            bank_acc = parts[1]
            sum_check(requisites, bank_acc)

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_workers(file_name, requisites)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            check_req = load_workers(file_name)

            for smt in check_req:
                check, announce = validating(smt)
                if check:
                    requisites = load_workers(file_name)
                else:
                    print(announce)
                    break

        elif command == 'help':
            help_me()

        else:
            invalid_com()


if __name__ == '__main__':
    main()
