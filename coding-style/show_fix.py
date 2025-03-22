## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
## EPITECH PROJECT - Sat, Mar, 2025                                                    ##
## Title           - scripts                                                           ##
## Description     -                                                                   ##
##     help_handling                                                                   ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
##       _|_|_|_|  _|_|_|    _|_|_|  _|_|_|_|_|  _|_|_|_|    _|_|_|  _|    _|          ##
##       _|        _|    _|    _|        _|      _|        _|        _|    _|          ##
##       _|_|_|    _|_|_|      _|        _|      _|_|_|    _|        _|_|_|_|          ##
##       _|        _|          _|        _|      _|        _|        _|    _|          ##
##       _|_|_|_|  _|        _|_|_|      _|      _|_|_|_|    _|_|_|  _|    _|          ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##

import os
import subprocess
import sys
import time
import threading
from rich import *

## ----------------------------------------------------------------------------------- ##

def print_bar(bar):
    final = 3 + 4 + 2 + bar + 2 + 5 + 1
    print("▢", end='')
    for i in range(final):
        print("-", end='')
    print("▢")

def help_handling(error_code, error_found, show_how_fix, biggest_line, error_excluded):
    cpt = 0
    summary = 0

    for err in error_code:
        if err in error_found and err not in error_excluded:
            cpt += 1
        summary += 1

    if show_how_fix > 0 and len(error_found) > 0:
        print("|")
        print(f"| How to fix : {cpt}/{summary}")
        print("|")
        for err in error_code:
            if err in error_found and err not in error_excluded:
                print(f"| {err} => {error_code[err]}")
        print("|")
        print_bar(biggest_line)