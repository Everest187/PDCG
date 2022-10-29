import sys
import requests, json, random, string, os, time, argparse, socket, ssl
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
        self.time_start = 0
        self.time_end = 0
        self.byte = 2046
        self.codes = []
        self.valid_codes = []
        self.threads = []
        self.payload = []
        self.response = []

    def recv(self):
        self.log(f"* Sent {pregen_amount} requests in {self.time_end - self.time_start:.2f}ms")
        for sentpayloads in self.payload:
            receive = ss.recv(self.byte).decode('utf-8')

            if "Dear me" not in receive:
                self.log(f"+ {sentpayloads['pdcode']} is active")
                self.valid_codes.append(sentpayloads["pdcode"])
            else:
                self.log(f"- {sentpayloads['pdcode']} inactive")

        print(f"Active PD Codes: {len(self.valid_codes)}")

    @staticmethod
    def send(reqpayload):
        ss.send(reqpayload)

    def create(self):
        for pdcode in self.codes:
            self.payload.append({"pdcode": pdcode, "pdpayload": bytes(f"GET /student/{pdcode} HTTP/1.1\r\nHost: app.peardeck.com\r\nCookie: PEARDECK_AUTH={self.token}; G_ENABLED_IDPS=google\r\n\r\n","utf-8",)})

    def load_cookies(self):
        with open(self.cookies_filename) as file:
            self.cookies = json.load(file)
            self.token = self.cookies["PEARDECK_AUTH"]

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
        self.log(f"{cookieinfo[0]} / Cookie expiration: {datetime.fromtimestamp(cookieinfo[1]).strftime('%B %d %Y %I:%M:%S')}\n\n* Generating Payload")
        

        self.create()
        self.log("* Starting Threads")
        self.time_start = time.time()
        for reqpayload in self.payload:
            if len(self.threads) > self.MAX_THREADS:
                for thread in self.threads:  # wait for all threads to complete
                    thread.join()

            thread = Thread(target=GenCodes.send, args=(reqpayload["pdpayload"],))
            thread.start()
            self.threads.append(thread)

            self.checked_codes += 1
            GenCodes.set_title(f"Checked Codes: {self.checked_codes} / {pregen_amount}")
        self.time_end = time.time()
        self.recv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='# of peardeck codes to generate')
    parser.add_argument('pre_gen', metavar='pre_gen', type=int, help='enter # of codes to generate')
    args = parser.parse_args()
    pregen_amount = args.pre_gen
    checker = GenCodes()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.connect(('app.peardeck.com', 443))
    ss = ssl.create_default_context().wrap_socket(sock, server_hostname='app.peardeck.com')
    checker.start_checker()