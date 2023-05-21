import sys

class Display:
    def banner():
        print(f"""
          _    _      _ ______ _           _           
         | |  | |    | |  ____(_)         | |          
         | |  | |_ __| | |__   _ _ __   __| | ___ _ __ 
         | |  | | '__| |  __| | | '_ \ / _` |/ _ \ '__|
         | |__| | |  | | |    | | | | | (_| |  __/ |   
          \____/|_|  |_|_|    |_|_| |_|\__,_|\___|_|   \x1b[0m\x1b[3m by Ruulian\x1b[0m

        \x1b[4mVersion\x1b[0m: 1.0
        """)

    def display_url(status_code, url):
        if status_code < 200 or (300 <= status_code and status_code < 400):
            color = 33
        elif 200 <= status_code and status_code < 300:
            color = 32
        else:
            color = 31
            
        print(f"[\x1b[{color}m{status_code}\x1b[0m] {url}")

    def error(message=""):
        print(f"[\x1b[91mERROR\x1b[0m] {message}")