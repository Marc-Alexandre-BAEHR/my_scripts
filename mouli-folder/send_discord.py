#!/usr/bin/python3

import os
import subprocess
import sys
import time
import datetime
import ast
import discord
import asyncio

from token_uid import DISCORD_BOT_TOKEN, USER_ID


async def send_message_to_user(project, prerequis, percent, total_passed, total_tests, test_value, hour, mins, sec, dd, mm, yy, now_timestmp):



    client = discord.Client(intents=discord.Intents.default())
    @client.event
    async def on_ready():
        print("BOT OK")
        try:
            user = await client.fetch_user(USER_ID)

            print(f"{user.name}")

            embed = discord.Embed(title=f"{project}",
                description=f"**Status**\n> {prerequis}\n**Percentage**\n> {percent}%\n**Tests**\n> {total_passed}/{total_tests}  ({test_value:.2f}%)\n",
                colour=0x7b3d40,
                timestamp=datetime.datetime.now())

            embed.set_author(name="Epitech",
                url="https://intra.epitech.eu/",
                icon_url="https://companieslogo.com/img/orig/epitech-eu-28fcad28.png?t=1720244494")

            embed.set_footer(text=f"{hour}h{mins}.{sec} on {dd}/{mm}/{yy}",
                icon_url="https://companieslogo.com/img/orig/epitech-eu-28fcad28.png?t=1720244494")

            await user.send(embed=embed)
            time.sleep(5)

        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")
        finally:
            await client.close()

    await client.start(DISCORD_BOT_TOKEN)

def send_message(project, prerequis, percent, total_passed, total_tests, test_value, hour, mins, sec, dd, mm, yy, now_timestmp):
    """Point d'entrée pour envoyer un message."""
    asyncio.run(send_message_to_user(project, prerequis, percent, total_passed, total_tests, test_value, hour, mins, sec, dd, mm, yy, now_timestmp))


def parse_test_data_from_string(data_string):

    test_data = ast.literal_eval(data_string)
    total_tests = 0
    total_passed = 0

    for stats in test_data.values():
        total_tests += stats['count']
        total_passed += stats['passed']

    if (total_tests > 0) :
        test_value = 100 / total_tests
    else:
        test_value = 0

    return total_tests, total_passed, test_value

def display_difference(diff_seconds):
    

    diff_ms = diff_seconds // 60
    diff_hs = diff_seconds // 3600
    diff_ds = diff_seconds // 86400

    if diff_seconds < 60:
        return f"{int(diff_seconds)}s ago"

    elif diff_seconds < 3600:
        return f"{int(diff_ms)}m {int(diff_seconds)%60}s ago"
    
    elif diff_seconds < 86400:
        return f"{int(diff_hs)}h {int(diff_ms)%60}m ago"
    
    elif diff_seconds < 86400*7:
        return f"{int(diff_ds)}d {int(diff_hs)%24}h ago"
    
    else:
        return f"{int(diff_ds)}d ago"

    return 0


def check_if_diff_from_last(old, new):
    
    percent_total = 0

    for i in range(len(new)):


        if (new[i] not in old):
            print(f"{old[i]}\n{new[i]}")
            
            parts = new[i].split("$")
            
            project = parts[0]

            percent = float(parts[1][:-1])
            percent_total += percent
            percent = round(percent, 2)


            hour = int(parts[2][-9:-7])
            mins = parts[2][-6:-4]
            sec = parts[2][-3:-1]
            requis = parts[3]

            total_tests, total_passed, test_value = parse_test_data_from_string(parts[5])

            dd = int(parts[2][8:10])
            mm = int(parts[2][5:7])
            yy = int(parts[2][2:4])+2000

            datetime_str = f"{yy}-{mm}-{dd} {hour}:{mins}:{sec}"
            datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            mouli_timestmp = datetime_obj.timestamp()

            now_timestmp = time.time()
            diff_stmp = now_timestmp - mouli_timestmp


            if mouli_timestmp > 1730026800:
                add_hour = 1
                diff_stmp -= 3600
            else:
                add_hour = 2
                diff_stmp -= 7200

            hour += add_hour
            if hour == 24:
                hour = 0
                dd += 1

            diff_time = display_difference(diff_stmp)



            yy = yy - 2000

        

            nb = float(percent/10)
            progress_bar = "▬"
            for i in range(1, int(nb)):
                progress_bar += "▬"


            requis = float(requis)
            prerequis = ""
            if requis == 2:
                prerequis = f"Prerequisites Met"
            if requis == 1.5:
                prerequis = f"Crashed"
            if requis == 1: 
                prerequis = f"No Test Passed"
            if requis == 0.5:
                prerequis = f"Delivery Error"
            if requis == 0.0:
                prerequis = f"Banned Function Used"

            send_message(project, prerequis, percent, total_passed, total_tests, test_value, hour, mins, sec, dd, mm, yy, now_timestmp)


            msg = f"`{project}`\n"
            msg += f"> {prerequis}\n"
            msg += f"> **{percent:.2f}**%\n"
            msg += f"> \n"
            msg += f"> **Tests:** {total_passed}/{total_tests}  ({test_value:.2f}%)\n"
            msg += f"> -# {hour:0}h{mins}.{sec} on {dd}/{mm}/{yy} <t:{now_timestmp:.0f}:R>"
    
    return