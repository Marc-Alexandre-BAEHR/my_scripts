#!/usr/bin/python3

import os
import subprocess
import sys
import time
import threading
from rich import *

from arguments import *
from show_fix import *
from launch_program import *


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
    "C1": f"Conditionnal branching, you must not have more than 3 indetations",
    "C2": f"The use of ternary operators is allowed as far as it is kept simple and readable",
    "C3": f"Usage of goto is forbidden",
    "H1": f"Header must only contain: function;type;struct;enum;global var;macros",
    "H2": f"Include guard, headers must be protected from double inclusion",
    "H3": f"Define must fit on only one line.",
    "A1": f"Constant pointers.",
    "A2": f"Prefer the most accurate types possible according to the use of the data.",
    "A3": f"File must end with a line break.",
    "A4": f"",
}

error_types = {
    "FATAL": ["GA"],
    "MAJOR": ["O1", "O2", "O3", "G4", "G5", "F3", "F4", "F5", "F6", "F7", "F9", "L1", "L5", "V2", "C1", "C2", "C3", "H1", "H2", "H3"],
    "MINOR": ["O4", "G1", "G2", "G3", "G6", "G7", "G8", "G9", "F1", "F2", "F8", "L2", "L3", "L4", "L6", "V1", "V3"],
    "INFOS": ["A1", "A2", "A3", "A4"]
}


def clear():
    subprocess.run("clear", shell=True)

def make_fclean():
    subprocess.run("make fclean", shell=True, capture_output=True)

def codingstyle(arg1, arg2):
    subprocess.run(["coding-style", arg1, arg2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def print_bar(bar):
    final = 3 + 4 + 2 + bar + 2 + 5 + 1
    print("▢", end='')
    for i in range(final):
        print("-", end='')
    print("▢")


def print_help():
    print(f"NAME:")
    print(f"\tcs - Coding Style checker for C projects during Epitech")
    print(f"")
    print(f"SYNOPSIS:")
    print(f"\tcs [OPTION]... [FLAGS]...")
    print(f"")
    print(f"DESCRIPTION:")
    print(f"\tCheck the coding style of a C project and render it the easier way to understand the errors")
    print(f"")

    print(f"\t[bold]-c, --conserve[/bold]")
    print(f"\t       Conserve the original file (default: 0)")
    print(f"\t       Usage: cs --conserve <file_name>(optionnal)")

    print(f"")

    print(f"\t[bold]-e, --exclude[/bold]")
    print(f"\t       Exclude a list of errors from the report (default: None)")
    print(f"\t       Usage: cs --exclude O1;O2;O3")

    print(f"")

    print(f"\t[bold]-f, --show-fix[/bold]")
    print(f"\t       Show or not how to fix the errors (default: None)")
    print(f"\t       Usage: cs --show-fix")

    print(f"")

    print(f"\t[bold]-h, --help[/bold]")
    print(f"\t       Display this help")

    print(f"")

    print(f"\t[bold]-p, --path[/bold]")
    print(f"\t       Path to the folder to check (default: current directory)")
    print(f"\t       Usage: cs --path <path>")
    
    print(f"")

    print(f"\t[bold]--pdf[/bold]")
    print(f"\t       Display the entire pdf rules")


    sys.exit(0)


def get_biggest_line():
    biggest_line = 0
    try:
        with open("coding-style-reports.log", "r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.split(":")
                path = parts[0]
                length = len(path)
                if length > biggest_line:
                    biggest_line = length
    except FileExistsError or FileNotFoundError:
        print(f"Error: coding-style-reports.log not found.")
        sys.exit(84)
    return biggest_line, lines


def get_cs_errors(lines, error_excluded):
    cs_err = [0, 0, 0, 0, 0]
    ex_cs_err = [0, 0, 0, 0, 0]

    for line in lines:
        parts = line.split(":")
        cs = parts[3][2:4]

        if "FATAL" in line:
            if cs not in error_excluded:
                cs_err[0] += 1
            else:
                ex_cs_err[0] += 1

        if "MAJOR" in line:
            if cs not in error_excluded:
                cs_err[1] += 1
            else:
                ex_cs_err[1] += 1

        if "MINOR" in line:
            if cs not in error_excluded:
                cs_err[2] += 1
            else:
                ex_cs_err[2] += 1

        if "INFO" in line:
            if cs not in error_excluded:
                cs_err[3] += 1
            else:
                ex_cs_err[3] += 1

    cs_err[-1] = sum(cs_err)
    ex_cs_err[-1] = sum(ex_cs_err)
    return cs_err, ex_cs_err


def display_percentage_bar(type, content):
    
    length = 10
    
    number = int(float(content) / length)
    remain = length - number

    string = "<"
    symbol_yes = "-"
    symbol_no = "-"
    end_string = ">"

    has_added = 0

    f = float(content) / length

    if (type == "fat"):
        if (f > length/2 and number != 10):
            has_added = 1
            string += f"[bold][grey30]{symbol_yes}[/grey30][bold]"
        for i in range(number):
            string += f"[bold][grey30]{symbol_yes}[/grey30][bold]"
        for i in range(remain - has_added):
            string += f"[bold][grey15]{symbol_no}[/grey15][bold]"
        return string + end_string
    if (type == "maj"):
        if (f > length/2 and number != 10):
            has_added = 1
            string += f"[bold][red]{symbol_yes}[/red][bold]"
        for i in range(number):
            string += f"[bold][red]{symbol_yes}[/red][bold]"
        for i in range(remain - has_added):
            string += f"[bold][grey15]{symbol_no}[/grey15][bold]"
        return string + end_string
    if (type == "min"):
        if (f > length/2 and number != 10):
            has_added = 1
            string += f"[bold][yellow]{symbol_yes}[/yellow][bold]"
        for i in range(number):
            string += f"[bold][yellow]{symbol_yes}[/yellow][bold]"
        for i in range(remain - has_added):
            string += f"[bold][grey15]{symbol_no}[/grey15][bold]"
        return string + end_string
    if (type == "inf"):
        if (f > length/2 and number != 10):
            has_added = 1
            string += f"[bold][green]{symbol_yes}[/green][bold]"
        for i in range(number):
            string += f"[bold][green]{symbol_yes}[/green][bold]"
        for i in range(remain - has_added):
            string += f"[bold][grey15]{symbol_no}[/grey15][bold]"
        return string + end_string






def display_result(cs_err, ex_cs_err, time_processing, biggest_line):
    fat, maj, min, inf, cs_total = cs_err
    ex_fat, ex_maj, ex_min, ex_inf, ex_total = ex_cs_err    
    
    if cs_total == 0 and ex_total == 0:
        print(f"▢  [bold]Coding style checked in [deep_sky_blue4]{time_processing:.3f}[/deep_sky_blue4]s[/bold]")
        print(f"|")
        print(f"|  No error found !")
        print(f"°")
        sys.exit(0)
    if cs_total == 0 and ex_total != 0:
        print(f"▢  [bold]Coding style checked in [deep_sky_blue4]{time_processing:.3f}[/deep_sky_blue4]s[/bold]")
        print(f"|")
        print(f"|  {ex_total} error(s) found but excluded")
        print(f"°")
        sys.exit(0)

    p_fat = (fat / cs_total) * 100
    p_maj = (maj / cs_total) * 100
    p_min = (min / cs_total) * 100
    p_inf = (inf / cs_total) * 100

    p_fat = f"{p_fat:.2f}%"
    p_maj = f"{p_maj:.2f}%"
    p_min = f"{p_min:.2f}%"
    p_inf = f"{p_inf:.2f}%"

    if p_fat[1] == ".":
        p_fat = '0' + p_fat
    if p_maj[1] == ".":
        p_maj = '0' + p_maj
    if p_min[1] == ".":
        p_min = '0' + p_min
    if p_inf[1] == ".":
        p_inf = '0' + p_inf


    bar_total = f"[bold][dodger_blue1]{"Total":<12}{cs_total:<5}[/dodger_blue1][/bold]"

    bar_fatal = f"[bold][grey30]{"Fatal":<7}{fat:<5}{p_fat:<8}[/grey30][/bold]{display_percentage_bar("fat", p_fat[:-1]):<15}"
    bar_major = f"[bold][red]{"Major":<7}{maj:<5}{p_maj:<8}[/red][/bold]{display_percentage_bar("maj", p_maj[:-1]):<15}"
    bar_minor = f"[bold][yellow]{"Minor":<7}{min:<5}{p_min:<8}[/yellow][/bold]{display_percentage_bar("min", p_min[:-1]):<15}"
    bar_infos = f"[bold][green]{"Infos":<7}{inf:<5}{p_inf:<8}[/green][/bold]{display_percentage_bar("inf", p_inf[:-1]):<15}"


    print(f"▢  [bold]Coding style checked in [dodger_blue1]{time_processing:.3f}[/dodger_blue1]s[/bold]")
    print(f"|")
    print(f"▢  {bar_total}")
    print(f"|")
    print(f"|  {bar_fatal}")
    print(f"|  {bar_major}")
    print(f"|  {bar_minor}")
    print(f"|  {bar_infos}")
    print(f"|")
    print_bar(biggest_line)


def display_line(str, cs, path, lined_at, biggest_line, error_excluded):
        
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

    if cs not in error_excluded:
        print(f"|  - {d_col}{cs}{fcol}   [deep_sky_blue4]{path_no_file}[/deep_sky_blue4][deep_sky_blue1]{parts[-1]}[/deep_sky_blue1][grey19]{string}[/grey19] [grey70]➟[/grey70]  {d_col}{lined_at:<3}{fcol} |")



def display_p(mode, lines, error_found, biggest_line, error_excluded):
    for line in lines:
        if mode in line:
            parts = line.split(":")
            path = parts[0]
            lined_at = parts[1]
            cs = parts[3][2:4]

            if parts[3][2:5] == "G10":
                cs = "GA"

            error_found.append(cs)
            display_line(mode, cs, path, lined_at, biggest_line, error_excluded)
    return error_found


def is_bar(where, cs_err, biggest_line):

    fat, maj, min, inf, total = cs_err

    if where == "FAT-MAJ":
        if fat > 0 and maj > 0 or fat > 0 and min > 0 or fat > 0 and inf > 0:
            print_bar(biggest_line)
    if where == "MAJ-MIN":
        if maj > 0 and min > 0 or maj > 0 and inf > 0:
            print_bar(biggest_line)
    if where == "MIN-INF":
        if min > 0 and inf > 0:
            print_bar(biggest_line)

def types_of_error_exclued(type, error_excluded, error_found):
    
    string = ""

    if type == "FATAL":
        for error in error_excluded:
            if error in error_types["FATAL"] and error in error_found:
                string += f" {error},"
    if type == "MAJOR":
        for error in error_excluded:
            if error in error_types["MAJOR"] and error in error_found:
                string += f" {error},"
    if type == "MINOR":
        for error in error_excluded:
            if error in error_types["MINOR"] and error in error_found:
                string += f" {error},"
    if type == "INFO":
        for error in error_excluded:
            if error in error_types["INFOS"] and error in error_found:
                string += f" {error},"

    string = string[1:-1]
    return string



def display_main_cs(cs_err, ex_cs_err, lines, error_found, biggest_line, error_excluded, error_types):
    error_found = display_p("FATAL",lines, error_found, biggest_line, error_excluded)
    is_bar("FAT-MAJ", cs_err, biggest_line)
    error_found = display_p("MAJOR",lines, error_found, biggest_line, error_excluded)
    is_bar("MAJ-MIN", cs_err, biggest_line)
    error_found = display_p("MINOR",lines, error_found, biggest_line, error_excluded)
    is_bar("MIN-INF", cs_err, biggest_line)
    error_found = display_p("INFO",lines, error_found, biggest_line, error_excluded)
    print_bar(biggest_line)


    if ex_cs_err[-1] > 0:

        fat_ex = types_of_error_exclued("FATAL", error_excluded, error_found)
        maj_ex = types_of_error_exclued("MAJOR", error_excluded, error_found)
        min_ex = types_of_error_exclued("MINOR", error_excluded, error_found)
        inf_ex = types_of_error_exclued("INFO", error_excluded, error_found)

        print(f"|")
        print(f"▢  [dodger_blue1]Excluded errors[/dodger_blue1]")
        print(f"|")
        print(f"|  [grey30]Fatal: {ex_cs_err[0]:<5}{fat_ex}[/grey30]")
        print(f"|  [red]Major: {ex_cs_err[1]:<5}{maj_ex}[/red]")
        print(f"|  [yellow]Minor: {ex_cs_err[2]:<5}{min_ex}[/yellow]")
        print(f"|  [green]Infos: {ex_cs_err[3]:<5}{inf_ex}[/green]")
        print(f"|")
        print_bar(biggest_line)
    return error_found



# def help_handling(error_code, error_found, show_how_fix, biggest_line):
#     cpt = 0
#     summary = 0


#     for error_code in error_fixes:
#         if error_code in error_found:
#             cpt += 1
#         summary += 1

#     if show_how_fix > 0 and len(error_fixes) > 0:
#         print("|")
#         print(f"| How to fix : {cpt}/{summary}")
#         print("|")
#         for error_code in error_fixes:
#             if error_code in error_found:
#                 print(f"| {error_code} => {error_fixes[error_code]}")
#         print("|")
#         print_bar(biggest_line)


def delete_file(conserve_file, conserve_file_name):
    if conserve_file:
        os.rename("coding-style-reports.log", conserve_file_name)
    else:
        os.remove("coding-style-reports.log")

if __name__=="__main__":

    error_found = []
    try:
        path, show_how_fix, conserve_file, conserve_file_name, error_excluded = setup_arguments(error_fixes)
        time_processing = launch_coding_style(path, error_excluded, error_types)
        biggest_line, lines = get_biggest_line()

        cs_err, ex_cs_err = get_cs_errors(lines, error_excluded)

        # fat, maj, min, inf, total, ex_fat, ex_maj, ex_min, ex_inf, ex_total = get_cs_errors(lines, error_excluded)
        clear()
        display_result(cs_err, ex_cs_err, time_processing, biggest_line)
        error_found = display_main_cs(cs_err, ex_cs_err, lines, error_found, biggest_line, error_excluded, error_types)
        help_handling(error_fixes, error_found, show_how_fix, biggest_line, error_excluded)
        delete_file(conserve_file, conserve_file_name)
        sys.exit(0)

    except KeyboardInterrupt:
        exit_with_error("Keyboard interrupt", 0, 84)