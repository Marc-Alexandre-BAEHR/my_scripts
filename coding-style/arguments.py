## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
## EPITECH PROJECT - Sat, Mar, 2025                                                    ##
## Title           - scripts                                                           ##
## Description     -                                                                   ##
##     arguments                                                                       ##
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

from main import print_help, exit_with_error
from pdf_function import print_entire_pdf
from exclude import add_exclude

## ----------------------------------------------------------------------------------- ##

def setup_arguments(error_fixes):
    arglen = len(sys.argv)
    rlen = arglen - 1
    # ↓
    path = "."
    show_how_fix = 0
    conserve_file = 0
    conserve_file_name = ""
    exclude = []

    i = 1

    while i < arglen:

        if sys.argv[i] == "--help" or sys.argv[i] == "-h":
            print_help()

        if sys.argv[i] == "--pdf":
            print_entire_pdf(error_fixes)

        if (sys.argv[i] == "--path" or sys.argv[i] == "-p"):
            if i == rlen or sys.argv[i+1][0] == "-":
                exit_with_error("Wrong usage of --path", 1, 1)
            path = sys.argv[i+1]
            i+=2
            continue

        if (sys.argv[i] == "--show-fix" or sys.argv[i] == "-f"):
            show_how_fix = 1
            i+=1
            continue

        if (sys.argv[i] == "--conserve" or sys.argv[i] == "-c"):
            conserve_file = 1
            if i == rlen or sys.argv[i+1][0] == "-":
                conserve_file_name = "coding-style-reports.log"
                i+=1
                continue
            if i < rlen:
                conserve_file_name = sys.argv[i+1]
                i+=2
                continue
            else:
                exit_with_error("Wrong usage of --conserve", 1, 1)

        if (sys.argv[i] == "--exclude" or sys.argv[i] == "-e"):
            if i == rlen:
                exit_with_error("Wrong usage of --exclude: no rules was given", 1, 1)

            exclude = add_exclude(exclude, sys.argv[i+1])
            i+=2
            continue
        
        
        exit_with_error(f"invalid option -- [white]'{sys.argv[i]}'[/white]", 1, 1)

    return path, show_how_fix, conserve_file, conserve_file_name, exclude

