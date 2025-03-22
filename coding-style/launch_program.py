## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
## EPITECH PROJECT - Sun, Mar, 2025                                                    ##
## Title           - scripts                                                           ##
## Description     -                                                                   ##
##     launch_program                                                                  ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
##             ███████╗██████╗ ██╗████████╗███████╗ ██████╗██╗  ██╗                    ##
##             ██╔════╝██╔══██╗██║╚══██╔══╝██╔════╝██╔════╝██║  ██║                    ##
##             █████╗  ██████╔╝██║   ██║   █████╗  ██║     ███████║                    ##
##             ██╔══╝  ██╔═══╝ ██║   ██║   ██╔══╝  ██║     ██╔══██║                    ##
##             ███████╗██║     ██║   ██║   ███████╗╚██████╗██║  ██║                    ##
##             ╚══════╝╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝                    ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##


import os
import subprocess
import sys
import time
import threading
from rich import *

## ----------------------------------------------------------------------------------- ##

def exit_with_error(string, help, code):
    print(f"cs: {string}")
    if help:
        print(f"Try 'cs --help' for more information")

    
    sys.exit(code)


def clear():
    subprocess.run("clear", shell=True)

def make_fclean():
    subprocess.run("make fclean", shell=True, capture_output=True)

def codingstyle(arg1, arg2):
    subprocess.run(["coding-style", arg1, arg2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def display_timer(start_time, stop_event):

    while not stop_event.is_set():

        elapsed_time = time.time() - start_time

        sec = int(elapsed_time)
        mil = elapsed_time - sec

        mil = str(mil)
        mil = mil[2:5]
        if sec < 60:
            print(f"▢➜  [deep_sky_blue1]{sec}[grey46]s[/grey46]{mil}[grey46]ms[/grey46][/deep_sky_blue1]", end="\r")
        else:
            mit = sec//60
            nsc = sec%60
            print(f"▢➜  [deep_sky_blue1]{mit}[grey46]:[/grey46]{nsc}[grey46]s[/grey46]{mil}[grey46]ms[/grey46][/deep_sky_blue1]", end="\r")

def launch_coding_style(path, error_excluded, error_types):
    start_time = time.time()
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=display_timer, args=(start_time, stop_event))
    timer_thread.daemon = True
    make_fclean()


    if os.path.isdir(path):
        os.chdir(path)
        print(f".")
        print(f"| - Path selected : [green]{os.getcwd()}[/green]")
    else:
        exit_with_error(f"invalid path: {path} is not a valid path.", 1, 84)
    
    
    if error_excluded:

        string_err = f"| - Error(s) excluded : [ "

        for error in error_excluded:
            if error in error_types["FATAL"]:
                string_err += f"[grey30]{error}[/grey30] - "
            elif error in error_types["MAJOR"]:
                string_err += f"[red]{error}[/red] - "
            elif error in error_types["MINOR"]:
                string_err += f"[yellow]{error}[/yellow] - "
            elif error in error_types["INFOS"]:
                string_err += f"[green]{error}[/green] - "
        string_err = string_err[:-3]
        string_err += f" ]"
        print(f"{string_err}")

    print(f"|")
    print(f"| Checking [cyan]coding style[/cyan] errors, please wait a few seconds")
    print(f"|")
    timer_thread.start()


    codingstyle(".", ".")
    
    
    time_processing = time.time() - start_time   

    
    
    stop_event.set()
    timer_thread.join()
    return time_processing