## parseCLA.py
# Primary Owner: Andrew Downie

from . import logger
import sys

hostClientDefault = '104.196.166.63'  # IP of the server
hostServerDefault = ''
portDefault = 12345                   # The same port as used by the server

###
### (Helper) ParsePort
###
def ParsePort(port):
    try:
        return int(port)
    except Exception as e:
        print("\nInvalid -p parameter: " + str(e) + "\n")
        quit()


###
### (Helper) PrevCurNextItem
###
def PrevCurNextItem(array, index):
    prevItem = None
    curItem = None
    nextItem = None

    arrayLen = len(array)
    if(index - 1 > 0 and index - 1 < arrayLen):
        prevItem = array[index - 1]

    if(index > 0 and index < arrayLen):
        curItem = array[index]

    if(index + 1 > 0 and index + 1 < arrayLen):
        nextItem = array[index + 1]

    return prevItem, curItem, nextItem


#####
##### HostPortDatalist
#####
# Gives the user the option to over ride default host and port, using -h and -p flags
# Arguments not preceeded by a -h or a -p will be added to a list, and returned as the 3rd parameter
def HostPortDatalist():
    host = hostClientDefault
    port = portDefault
    data = []

    args = sys.argv
    argc = len(args)

    for i in range(1, argc):
        prevArg, curArg, nextArg = PrevCurNextItem(args, i)

        if(curArg == "-h"):
            host = nextArg
        elif(curArg == "-p"):
            port = ParsePort(nextArg)
        elif(prevArg != "-h" and prevArg != "-p"):
            data.append(curArg)

    ###
    ### Show the settings the user has selected
    ###
    print("\nHost(-h) set to: " + host)
    print("Port(-p) set to: " + str(port))
    print("Other args set to: " + str(data) + "\n")

    return host, port, data

#####
##### HostPortData
#####
# Gives the user the option to over ride default host and port, using -h and -p flags
# The last argument not preceeded by a -h or a -p will be returned as the third return value
# Unused args will be printed to command line, as ignored args
def HostPortData(dataName="CLA input"):
    host = hostClientDefault
    port = portDefault
    data = ""
    ignoredArgs = []

    args = sys.argv
    argc = len(args)

    for i in range(1, argc):
        prevArg, curArg, nextArg = PrevCurNextItem(args, i)

        if(curArg == "-h"):
            host = nextArg
        elif(curArg == "-p"):
            port = ParsePort(nextArg)
        elif(prevArg != "-h" and prevArg != "-p"):
            ignoredArgs.append(curArg)
            data = curArg

    if(len(ignoredArgs) > 0):
        del ignoredArgs[-1]

    ###
    ### Show the settings the user has selected
    ###
    print("\nHost set to: " + str(host))
    print("Port set to: " + str(port))
    print(dataName + " set to: " + str(data))
    print("Ignored args are: " + ", ".join(ignoredArgs) + "\n")

    return host, port, data

#####
##### Server_HostPort
#####
def Server_HostPort():
    host = hostServerDefault
    port = portDefault
    ignoredArgs = []

    args = sys.argv
    argc = len(args)

    for i in range(1, argc):
        prevArg, curArg, nextArg = PrevCurNextItem(args, i)

        if(curArg == "-h"):
            host = nextArg
        elif(curArg == "-p"):
            port = ParsePort(nextArg)
        elif(prevArg != "-h" and prevArg != "-p"):
            ignoredArgs.append(curArg)

    ###
    ### Show settings the server is being run with
    ###
    printHost = host
    if(printHost == ''):
        printHost = '(default host)'

    startMsg = "Starting Server -> "
    startMsg += "Host( " + printHost
    startMsg += " ), Port( " + str(port)
    startMsg += " ), Ignored args: " +  ", ".join(ignoredArgs)
    logger.PrintLog(startMsg)
    return host, port

