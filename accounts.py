import datetime

import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient import discovery

SPREADSHEET_ID = "1otVI0JgfuBDJw8jlW_l8vHXyfo5ufJiXOqshDixazZA"  # ALL-IN-ONE-LOG-2021


class Spreadsheet:
    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        self.sheet = self.get_all_in_one_log()

    def get_all_in_one_log(self):
        SERVICE_ACCOUNT_FILE = "credentials.json"
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = discovery.build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        return sheet

    def getSheet(self):
        return self.sheet


def list_last_five_trans():
    result = (
        sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Trans!B6:G").execute()
    )
    values = result.get("values", [])
    df = pd.DataFrame(
        values, columns=["Date", "Description", "Dummy", "Amount", "From A/c", "To A/c"]
    )
    df["Description"] = df["Description"].str.slice(0, 20)
    print(df.tail(5))
    return


def list_last_30_trans():
    result = (
        sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Trans!B6:G").execute()
    )
    values = result.get("values", [])
    df = pd.DataFrame(
        values, columns=["Date", "Description", "Dummy", "Amount", "From A/c", "To A/c"]
    )
    df["Description"] = df["Description"].str.slice(0, 20)
    print(df.tail(30))
    return


def check_balances():
    res2 = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range="Dashboard!B9:B19")
        .execute()
    )
    acc = res2.get("values", [])

    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range="Dashboard!P9:P19")
        .execute()
    )
    val = result.get("values", [])
    balances = np.array(val)
    balances = balances.flatten()
    balances[balances == "#N/A"] = "0"

    balances = list(map(float, balances))

    (
        C,
        K,
        Zer,
        Zer_Comm,
        Cams,
        Samrudhi,
        Citi,
        K_Fixed,
        Union,
        Z_Hold,
        Citi_Fixed,
    ) = balances
    print(f"Cash Balance~~~~~~~~~~~~~~~~~~~~~:{C:.2f}")
    print(
        f"Saving A/c Balance~~~~~~~~~~~~~~~:{(K+Citi):.2f} with (Kotak-{K:.2f} and Citi-{Citi:.2f})"
    )
    print(
        f"In FD (CB,Kotak,Union, Samruddhi):{(K_Fixed+Union+Citi_Fixed):.2f} with (K-{K_Fixed:.2f}, Citi-{Citi_Fixed:.2f})"
    )
    print(f"Unutilized in Shares~~~~~~~~~~~~~:{Zer:.2f}")
    print(f"In CAMS MF~~~~~~~~~~~~~~~~~~~~~~~:{Cams:.2f}")
    print(f"In shares~~~~~~~~~~~~~~~~~~~~~~~~:{Z_Hold:.2f}")

    return


def check_expenses():
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range="Dashboard!C46:C46")
        .execute()
    )
    values = result.get("values", [])
    print("Expenses for the year: " + values[0][0])
    return


class Account:
    def __init__(self, desc, amount, from_ac, to_ac):
        self.desc = desc
        self.amount = amount
        self.from_ac = from_ac
        self.to_ac = to_ac
        self.catg = "Adjustment"
        if self.from_ac == "C" or self.from_ac == "K":
            self.catg = "Expense"
        self.today = datetime.datetime.now()
        self.period = datetime.date.strftime(self.today, "%Y-%m")
        self.formatted_dt = datetime.date.strftime(self.today, "%m/%d/%Y")
        self.new_trans = [
            [
                self.formatted_dt,
                self.desc,
                "",
                self.amount,
                self.from_ac,
                self.to_ac,
                "",
                self.period,
                self.catg,
            ]
        ]

    def get_trans(self):
        return self.new_trans


def add_new_record():
    print("Adding new records, Enter description, amount, from a/c and to a/c")
    desc = input("description is: ")
    amount = input("trans amount: ")
    from_ac = input(" from account: ")
    to_ac = input(" to account: ")
    account = Account(desc, amount, from_ac, to_ac)
    print(" Transaction to be entered is: ", account.get_trans())
    conf = 0
    while conf != 1 and conf != 9:
        conf = int(input(" Enter 1 to confirm, 9 to erase: "))

    if conf == 9:
        print("Exiting adding new record, please re-enter your choice: ")
        return

    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Trans!B6:J",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": account.get_trans()},
    )
    response = request.execute()
    print("Added new record: ")
    print(response)
    return


class Choice:
    switcher = {
        1: add_new_record,
        4: list_last_30_trans,
        5: list_last_five_trans,
        6: check_balances,
        7: check_expenses,
    }

    def __init__(self, SpreadSheet):
        self._choice = 0
        self.exit = False
        self.Spreadsheet = Spreadsheet

    def is_exit(self):
        return self.exit

    def get_choice(self):
        print("~~~~~~ MAIN MENU ~~~~~~~")
        print("1:ADD, 4:LIST-30, 5:LIST-5, 6:CHECK-BALANCE, 7:.CHECK-EXPENSES  9: Quit")
        self._choice = int(input("Enter your choice : "))
        if self._choice == 9:
            self.exit = True
        return self._choice

    def switch_choice(self):
        func = self.switcher.get(self._choice, lambda: "Invalid choice")
        func()


if __name__ == "__main__":
    AccountSheet = Spreadsheet(SPREADSHEET_ID)
    sheet = AccountSheet.getSheet()
    # sheet = get_all_in_one_log()

    # list_last_five_trans()

    choice = Choice(AccountSheet)
    while choice.is_exit() == False:
        choice.get_choice()
        choice.switch_choice()

    print("Exiting out.. kind regards!")
