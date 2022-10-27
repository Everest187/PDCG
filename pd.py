import sys
import requests, json, random, string, os, time, argparse
from os import system
from threading import Thread
from Scan.decrypt import decode
from datetime import datetime

class GenCodes:
    def __init__(self, cookies_filename: str="cookies.json", MAX_THREADS: int=50):
        self.cookies_filename = cookies_filename
        self.MAX_THREADS = MAX_THREADS

        self.cookies = {}
        self.token = ""
        self.checked_codes = 0
        self.codes = []
        self.valid_codes = []
        self.threads = []

    def load_cookies(self):
        with open(self.cookies_filename) as file:
            self.cookies = json.load(file)
            self.token = self.cookies["PEARDECK_AUTH"]

    def check_code(self, code: str) -> bool:
        response = requests.get(f"https://app.peardeck.com/student/{code}", cookies=self.cookies)
        response.raise_for_status()
        # code is invalid
        return "Dear me" not in response.text

    def validate_code(self, code):
        if self.check_code(code):
            self.log(f"{code} is active")
            self.valid_codes.append(code)
        else:
            self.log(f"{code} is inactive")

    @staticmethod
    def generate_code() -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(9))

    @staticmethod
    def set_title(title: str):
        if os.name == "nt":
            system(f"title {title}")
        else:
            system(f"echo -ne \"\033]0;{title}\007\"")

    @staticmethod
    def clear():
        if os.name == "nt":
            system("cls")
        else:
            system("clear")

    @staticmethod
    def log(text: str):
        print(text)

    def start_checker(self):
        self.load_cookies()
        cookieinfo = decode(self.token)
        GenCodes.clear()

        if pregen_amount >= 1500:
            exit()
        for _ in range(pregen_amount):
            self.codes.append(GenCodes.generate_code())
            GenCodes.set_title(f"PreGen Codes: {len(self.codes)} / {pregen_amount}")
        self.log(f"\n{cookieinfo[0]} / Cookie expiration: {datetime.fromtimestamp(cookieinfo[1]).strftime('%B %d %Y %I:%M:%S')}\nChecking Codes...")
        for code in self.codes:
            if len(self.threads) > self.MAX_THREADS:
                for thread in self.threads:  # wait for all threads to complete
                    thread.join()

            thread = Thread(target=self.validate_code, args=(code,))
            thread.start()
            self.threads.append(thread)

            self.checked_codes += 1
            GenCodes.set_title(f"Checked Codes: {self.checked_codes} / {pregen_amount}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='# of peardeck codes to generate')
    parser.add_argument('pre_gen', metavar='pre_gen', type=int, help='enter # of codes to generate')
    args = parser.parse_args()
    pregen_amount = args.pre_gen
    checker = GenCodes()
    checker.start_checker()