#!/usr/bin/python3

import os
import subprocess
import sys
import time
import threading
from rich import *


# Error codes and fixes dictionary
error_fixes = {
    "O1": f"Repo must not contain .o or .a files",
    "O2": f"The C program must have either .c or .h file extensions.",
    "O3": f"Ensure the file contains 10 functions: 5 static and 5 non-static.",
    "O4": f"Ensure that files and folders are named logically and consistently.",
    "G1": f"Header is missing.",
    "G2": f"Functions should be separated by exactly one empty line.",
    "G3": f"Preprocessor directives must be properly indented.",
    "G4": f"Global variables should be declared at the top.",
    "G5": f"Only include .h files.",
    "G6": f"Lines of code should never end with a backslash.",
    "G7": f"No spaces allowed at the end of the line.",
    "G8": f"Avoid leading empty lines and ensure no more than one trailing empty line.",
    "G9": f"Constant values should be defined using appropriate constants.",
    "GA": f"Ensure inline assembly code is used properly.",
    "F1": f"Functions should maintain logical coherence.",
    "F2": f"Function names must be descriptive and concise.",
    "F3": f"The line is too long (80 characters maximum).",
    "F4": f"The function is too long (20 lines of code maximum).",
    "F5": f"The function have too much parameters (4 parameters maximum).",
    "F6": f"Functions without parameters should be used where appropriate.",
    "F7": f"Structures can be passed as parameters to functions.",
    "F8": f"Ensure comments inside functions are present and useful.",
    "F9": f"Avoid nested functions.",
    "L1": f"Each line of code within a function should be concise.",
    "L2": f"Indentation in the line is wrong.",
    "L3": f"Spaces should be used appropriately.",
    "L4": f"Curly brackets should be placed correctly.",
    "L5": f"Variable declarations should be clear and placed at the beginning.",
    "L6": f"Blank lines should be used to separate logical blocks of code.",
    "V1": f"Naming identifiers",
    "V2": f"",
    "V3": f"Wrong placement of pointer(s)",
    "C1": f"",
    "C2": f"",
    "C3": f"Usage of goto is forbidden",
    "H1": f"Header must only contain: function;type;struct;enum;global var;macros",
    "H2": f"",
    "H3": f"",
    "A1": f"",
    "A2": f"",
    "A3": f"File must end with a line break.",
    "A4": f"",
}


## Functions declared:
def clear():
    subprocess.run("clear", shell=True)

def codingstyle(arg1, arg2):
    subprocess.run(["coding-style", arg1, arg2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def display_timer(start_time):
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
        # time.sleep(0.065)



def print_bar(bar):
    final = 3 + 4 + 2 + bar + 2 + 5 + 1
    print("▢", end='')
    for i in range(final):
        print("-", end='')
    print("▢")


## Default or Custom Variable:
arglen = len(sys.argv)
# ↓
path = "."
show_how_fix = 1

if arglen > 1:
    for i in range(1, arglen):
        if sys.argv[i] == "--path" and i < arglen:
            path = sys.argv[i+1]
        if sys.argv[i] == "--show-fix" and i < arglen:
            show_how_fix = int(sys.argv[i+1])





# Start the timer in a separate thread
start_time = time.time()
stop_event = threading.Event()
timer_thread = threading.Thread(target=display_timer, args=(start_time,))
timer_thread.daemon = True



if os.path.isdir(path):
    print(f".")
    print(f"| [green]{path}[/green] has been selected.")
    print(f"| Checking [cyan]coding style[/cyan] errors, please wait a few seconds")
    print(f"|")
    timer_thread.start()
    codingstyle(path, ".")
else:
    print(f".")
    print(f"| No valid path has been selected. Current folder taken as path [green]successfully[/green].")
    print(f"| Checking [cyan]coding style[/cyan] errors, please wait a few seconds")
    print(f"|")
    timer_thread.start()
    codingstyle(".", ".")
time_processing = time.time() - start_time
   
stop_event.set()
timer_thread.join()



biggest_line = 0
with open("coding-style-reports.log", "r") as f:
    lines = f.readlines()


    for line in lines:
        parts = line.split(":")
        path = parts[0]
        length = len(path)
        if length > biggest_line:
            biggest_line = length




fat = sum(1 for line in lines if "FATAL" in line)
maj = sum(1 for line in lines if "MAJOR" in line)
mim = sum(1 for line in lines if "MINOR" in line)
inf = sum(1 for line in lines if "INFO" in line)
total = fat + maj + mim + inf

clear()





if maj == 0 and mim == 0 and inf == 0:
    os.remove("coding-style-reports.log")
    print(f"▢  [bold]Coding style checked in [deep_sky_blue4]{time_processing:.3f}[/deep_sky_blue4]s[/bold]")
    print(f"|")
    print(f"|  No error found !")
    print(f"°")
    sys.exit(0)


p_fat = (fat / total) * 100
p_maj = (maj / total) * 100
p_mim = (mim / total) * 100
p_inf = (inf / total) * 100

# Display the results
bar_text = f"[bold][dodger_blue1]Total[/dodger_blue1]\t[grey30]Fatal[/grey30]\t[red]Major\t[/red][yellow]Minor\t[/yellow][green]Infos[/green][/bold]"
bar_dgts = f"[dodger_blue1]{total:<5}[/dodger_blue1]\t[grey30]{fat:<5}[/grey30]\t[red]{maj:<5}[/red]\t[yellow]{mim:<5}[/yellow]\t[green]{inf:<5}[/green]"
bar_prct = f"\t\t[grey30]{p_fat:.2f}%[/grey30]\t[red]{p_maj:.2f}%[/red]\t[yellow]{p_mim:.2f}%[/yellow]\t[green]{p_inf:.2f}%[/green]"


print(f"▢  [bold]Coding style checked in [dodger_blue1]{time_processing:.3f}[/dodger_blue1]s[/bold]")
print(f"|")
print(f"▢  {bar_text}")
print(f"|  {bar_dgts}")
print(f"|")
print(f"|  {bar_prct:}")
print(f"|")
print_bar(biggest_line)


def display_line(str, cs, path, lined_at):
        
    if str == "FATAL":
        col = f"grey30"
    elif str == "MAJOR":
        col = f"red"
    elif str == "MINOR":
        col = f"yellow"
    elif str == "INFO":
        col = f"green"
    d_col = f"[{col}]"
    fcol = f"[/{col}]"


    parts = path.split("/")
    path_no_file = ""
    for i in range(len(parts)-1):
        path_no_file += parts[i]
        path_no_file += "/"


    comble = biggest_line - len(path)
    string = ""
    for i in range(comble):
        string += "✗"

    print(f"|  - {d_col}{cs}{fcol}   [deep_sky_blue4]{path_no_file}[/deep_sky_blue4][deep_sky_blue1]{parts[-1]}[/deep_sky_blue1][grey19]{string}[/grey19] [grey70]➟[/grey70]  {d_col}{lined_at:<3}{fcol} |")

error_found = []




def display_p(mode):
    for line in lines:
        if mode in line:
            parts = line.split(":")
            path = parts[0]
            lined_at = parts[1]
            cs = parts[3][2:4]

            if parts[3][2:5] == "G10":
                cs = "GA"

            error_found.append(cs)
            display_line(mode, cs, path, lined_at)


def is_bar(where):
    if where == "FAT-MAJ":
        if fat > 0 and maj > 0 or fat > 0 and mim > 0 or fat > 0 and inf > 0:
            print_bar(biggest_line)
    if where == "MAJ-MIN":
        if maj > 0 and mim > 0 or maj > 0 and inf > 0:
            print_bar(biggest_line)
    if where == "MIN-INF":
        if mim > 0 and inf > 0:
            print_bar(biggest_line)




display_p("FATAL")
is_bar("FAT-MAJ")
display_p("MAJOR")
is_bar("MAJ-MIN")
display_p("MINOR")
is_bar("MIN-INF")
display_p("INFO")




print_bar(biggest_line)

cpt = 0
summary = 0

for error_code in error_fixes:
    if error_code in error_found:
        cpt += 1
    summary += 1


if show_how_fix > 0 and len(error_fixes) > 0:
    print("|")
    print(f"| How to fix : {cpt}/{summary}")
    print("|")
    for error_code in error_fixes:
        if error_code in error_found:
            print(f"| {error_code} => {error_fixes[error_code]}")
    print("|")
    print_bar(biggest_line)



os.remove("coding-style-reports.log")
