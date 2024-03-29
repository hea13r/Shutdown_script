#!/usr/bin/env python3
import time
import subprocess

def ipCheck(x):
    pingCheck = subprocess.run(['ping', x, '-c 1', '-W 1'], stdout=subprocess.DEVNULL)
    if "returncode=0" in str(pingCheck):
        return x
    else:
        pass

def ipChecker(x):
    shutdownList = []
    for i in x:
        shutdownList.append(ipCheck(i))
    return(shutdownList)

doubleCheck = input("Are you sure you want to shut everything down? [yes to continue] ")
if doubleCheck.lower() != "yes":
    exit(0)

ipList = [] #enter your ip list here

answer = "no"
while answer.lower() == "no":
    print("Checking for active endpoints...")
    shutdownList = ipChecker(ipList)
    shutdownList = shutdownList[::-1]
    answer = input(f"Are these the IPs you expect to see active? [type no to rescan] \n{shutdownList}\n")

checkAgain = input(f"Do you want to begin shutting down these IPs? [type yes to continue] \n{shutdownList}\n")
if checkAgain.lower() != 'yes':
    exit(0)

while len(shutdownList) != 0:
    for i in shutdownList:
        if i == None: #Sometimes the ipChecker will return a None value which breaks this loop, this fixes that
            shutdownList.remove(None)
            continue
        print(f"Attempting to shutdown {shutdownList[i]}...")
        subprocess.run(['ssh', i, 'shutdown -h now'], stdout=subprocess.DEVNULL)
        time.sleep(10) #Gives time for the IP to shutdown
        if not ipCheck(i): #Checks to make sure IP is shutdown before removing from list
            shutdownList.remove(i)

print("One final check to make sure everything is off...")
finalCheck = ipChecker(ipList)
finalAnswer = input(f"These are the IPs I found still active: {finalCheck}.\nIf blank or [None] type yes to continue, otherwise consider starting over.\n")
if finalAnswer.lower() != 'yes':
    exit(0)

print("I will now shutdown the control-plane...")
subprocess.run(['ssh', 'ip', 'shutdown -h now'], stdout=subprocess.DEVNULL) #you must enter the ip
time.sleep(10) #gives time for it to shutdown before shutting down your machine
               #also gives you time to remember your machine is about to be shutdown

print("I will now shut myself down...")
subprocess.run(['shutdown', '-h', 'now'])
