#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def get_bank_acc(accounts, s_b_a, b_a, t_a):
    """
    Request for bank account details with verification
    """
    accounts.append(
        {
            "s_b_a": s_b_a,
            "b_a": b_a,
            "t_a": t_a
        }
    )

    return accounts


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


def main(command_line=None):
    """
    Main function
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("BankAcc")
    parser.add_argument(
        "--version",
        action="store",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add new BankAcc"
    )
    add.add_argument(
        "-s",
        "--s_b_a",
        action="store",
        required=True,
        help="Sender bank account"
    )
    add.add_argument(
        "-b",
        "--s_b",
        action="store",
        required=True,
        help="Receivers bank account"
    )
    add.add_argument(
        "-t",
        "--t_a",
        action="store",
        required=True,
        help="transfer summ"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all bank accs"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select sum of choosen bank acc"
    )
    select.add_argument(
        "-c",
        "--choose",
        action="store",
        type=int,
        required=True,
        help="Sum of choosen bank acc"
    )

    args = parser.parse_args(command_line)
    is_dirty = False
    if os.path.exists(args.filename):
        requisites = load_workers(args.filename)
    else:
        requisites = []

    if args.command == "add":
        requisites = get_bank_acc(
            requisites,
            args.s_b_a,
            args.b_a,
            args.t_a
        )
        is_dirty = True

    elif args.command == "display":
        display_acc(requisites)

    elif args.command == "select":
        sum_check(requisites, args.choose)
        display_acc(selected)

    elif is_dirty:
        save_workers(args.filename, requisites)


if __name__ == '__main__':
    main()
