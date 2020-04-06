"""
from subprocess import call, Popen, PIPE
from select import poll, POLLIN, POLLOUT
from signal import signal, alarm, SIGALRM, SIGPIPE, SIG_DFL
from sys import exit, argv
from time import sleep


# argv is a list of arguments passed along with the command to call this program
# argv[0] : Name of Source file (here "newBm.py")
# argv[1] : Extension of bot 1 : "c" or "cpp" or "py"
# argv[2] : Extension of bot 2 : "c" or "cpp" or "py"
# argv[3] : Name of file in which logs are to be written
# argv[4] : If bot1 is playing as player 2 or not : "True" or "False"
print(argv)
(bot1Ext, bot2Ext, logFile, isP2) = (argv[1], argv[2], argv[3], argv[4])

# botFile is where bots are kept
botFile = "Bots/"
# Time limit given to different types of bots
time_limits = {
    "cpp": 3000,
    "c": 3000,
    "py": 6000,
}

# Get the executable file of the validation code (in current directory)
call("g++ -o val val.cpp".split())

# Don't know the use of this as of now
plist1 = ["prlimit", "-p", ""]
plist2 = ["prlimit", "-p", ""]


def logWrite(msg):
    # Writing logs to logfile (name mentioned in argv[3])
    print(msg)



def processWrite(proc, string):
    # Writing string of bytes to process proc
    # str.encode(string) converts string to string of bytes
    proc.stdin.write(str.encode(string))
    proc.stdin.flush()


def processRead(proc, poll=None):
    # Reading output from given proc
    ret = proc.stdout.readline()
    ret = ret.decode().strip()
    return ret


def end_code(exit_code):
    # Return code to system tellling how the game ended and also killing any open processes
    # Program closes from here
    if bot1.poll() is None:
        bot1.kill()
    if bot2.poll() is None:
        bot2.kill()
    if val.poll() is None:
        val.kill()
    exit(exit_code)


def getArgList(exType, p):
    # Get the command depending on type of extension and return a list of terminal commands
    # example for running a python program, command is "python player1.py"
    # but player1.py named bot is in directory botFile, so command is "python " + botFile + "player1"
    # list is list of commands
    lis = []
    if exType == "cpp" or exType == "c":
        lis = lis + ["./" + botFile + "player" + str(p)]
        plist1.extend(("--nofile=5", "--nproc=500", "--as=21460"))
    elif exType == "py":
        lis = lis + ["python", botFile + "player" + str(p) + ".py"]
        plist1.extend(("--nofile=5", "--nproc=500", "--as=32740"))
    return lis


# Popen is for opening a process by passing command line arguments
# The input(stdin) and output(stdout) of these processes is changed to type PIPE
# By default input and ouput would've been to the computer screen,
# but with PIPE, the input and output are passed through a pipe to this process(parent)
bot1 = Popen(args=getArgList(bot1Ext, 1), stdin=PIPE, stdout=PIPE)
# poll classes is used to check if the process is ready to give output or not
bot1Poll = poll()
bot1Poll.register(bot1.stdout.fileno())
bot1Time = time_limits[bot1Ext]

bot2 = Popen(args=getArgList(bot2Ext, 2), stdin=PIPE, stdout=PIPE)
bot2Poll = poll()
bot2Poll.register(bot2.stdout.fileno())
bot2Time = time_limits[bot2Ext]

# The input and output from the bots will be passed through the validation process
val = Popen(args=["./val"], stdin=PIPE, stdout=PIPE)

# Dom't know this
plist1[2] = str(bot1.pid)
plist2[2] = str(bot2.pid)

# call(plist1)  # dont know this
# call(plist2)


if isP2 == "True":
    # If it was True in argv[4], then it means player 1 will play 2nd
    # and so swapping the corresponding values
    (bot1, bot2) = (bot2, bot1)
    (bot1Poll, bot2Poll) = (bot2Poll, bot1Poll)
    (bot1Time, bot2Time) = (bot2Time, bot1Time)

# bot1 starts first hence passing 0
msg = "0\n"
processWrite(bot1, "0\n")

# bot2 starts 2nd hence passing 1
msg = "1\n"
processWrite(bot2, "1\n")

while True:
    # poll().poll(time) waits for registered process to create an event(here give output to the PIPE)
    # within given input time - time
    # If an event is created wtihin time, then the output is read and temp is not empty
    # If temp is not empty then poll().poll(time) return a list of tuples saying if output is ready or no
    # so temp[0][1] is a POLLIN integer
    if not bot1.poll():
        temp = bot1Poll.poll(bot1Time)
        if temp:
            if temp[0][1] is POLLIN:
                move = processRead(bot1)
            else:
                logWrite("v,0,No IO recieved")
                end_code(102)
        else:
            logWrite("v,0,No IO recieved")
            end_code(102)
    else:
        logWrite("v,0,PREMATURE TERMINATION")
        end_code(102)

    move = move + "\n"

    processWrite(val, move)
    validity = processRead(val)

    # validity is the move if it was a valid move else it is INVALID

    if validity.strip() != move.strip():
        logWrite("v,0," + move.strip() + " " + validity.strip())
        end_code(102)
    print("v,0," + move.strip())

    if not bot2.poll():
        processWrite(bot2, move)
        temp = bot2Poll.poll(bot2Time)
        if temp:
            if temp[0][1] is POLLIN:
                move = processRead(bot2)
            else:
                logWrite("v,1,No IO recieved")
                end_code(101)
        else:
            logWrite("v,1,No IO recieved")
            end_code(101)

    else:
        logWrite("v,1,PREMATURE TERMINATION")
        end_code(101)

    move = move + "\n"

    processWrite(val, move)
    validity = processRead(val)

    if validity.strip() != move.strip():
        logWrite("v,1," + move.strip() + " " + validity.strip())
        end_code(101)
    print("v,1," + move.strip())

    if not bot1.poll():
        processWrite(bot1, move)

end_code(101)
"""


# new approach to the code

from subprocess import call, Popen, PIPE
from select import poll, POLLIN, POLLOUT
from signal import signal, alarm, SIGALRM, SIGPIPE, SIG_DFL
from sys import exit, argv
from time import sleep


# argv is a list of arguments passed along with the command to call this program
# argv[0] : Name of Source file (here "newBm.py")
# argv[1] : Extension of bot 1 : "c" or "cpp" or "py"
# argv[2] : Extension of bot 2 : "c" or "cpp" or "py"
# argv[3] : Name of file in which logs are to be written
# argv[4] : If bot1 is playing as player 2 or not : "True" or "False"
print(argv)
(bot1Ext, bot2Ext, logFile, isP2) = (argv[1], argv[2], argv[3], argv[4])

# botFile is where bots are kept
botFile = "Bots/"
# Time limit given to different types of bots
time_limits = {
    "cpp": 3000,
    "c": 3000,
    "py": 6000,
}

# Get the executable file of the validation code (in current directory)
call("g++ -o val val.cpp".split())

# Don't know the use of this as of now
plist1 = ["prlimit", "-p", ""]
plist2 = ["prlimit", "-p", ""]


def logWrite(msg):
    # Writing logs to logfile (name mentioned in argv[3])
    print(msg)


class Process:
    def __init__(self, ext=None, player=None, timeLimit=None, otherArgs=None):
        self.ext = ext
        self.player = player
        self.timeLimit = timeLimit
        if otherArgs is None:
            self.argList = self.getArgList(ext, player)

        else:
            self.argList = otherArgs

        self.proc = Popen(args=self.argList, stdin=PIPE, stdout=PIPE)
        self.pollObj = poll()
        self.pollObj.register(self.proc.stdout.fileno())

    def getArgList(self, exType, p):
        # lis = ["stdbuf", "-o0", "-i0", "-e0"]
        lis = []
        if exType == "cpp" or exType == "c":
            lis = lis + ["./" + botFile + "player" + str(p)]
            plist1.extend(("--nofile=5", "--nproc=500", "--as=21460"))
        elif exType == "py":
            lis = lis + ["python", botFile + "player" + str(p) + ".py"]
            plist1.extend(("--nofile=5", "--nproc=500", "--as=32740"))
        return lis

    def write(self, string):
        string = string + "\n"
        self.proc.stdin.write(str.encode(string))
        self.proc.stdin.flush()

    def read(self):
        temp = self.pollObj.poll(self.timeLimit)
        if temp:
            if temp[0][1] is POLLIN:
                ret = self.proc.stdout.readline()
                ret = ret.decode().strip()
                return ret
        return ""

    def writeAndRead(self, string=""):
        self.write(string)
        temp = self.pollObj.poll(self.timeLimit)
        if temp:
            if temp[0][1] is POLLIN:
                val = self.read()
                return val
        return ""
        # raise Exception  # make exception class and raise an exception object

    def isRunning(self):
        return self.proc.poll() is None

    def kill(self):
        self.proc.kill()


bot1 = Process(ext=bot1Ext, player=1, timeLimit=time_limits[bot1Ext])

bot2 = Process(ext=bot2Ext, player=2, timeLimit=time_limits[bot2Ext])

val = Process(timeLimit=1000, otherArgs="./val".split())


def end_code(exit_code):
    # Return code to system tellling how the game ended and also killing any open processes
    # Program closes from here
    if bot1.isRunning():
        bot1.kill()
    if bot2.isRunning():
        bot2.kill()
    if val.isRunning():
        val.kill()
    exit(exit_code)


if isP2 == "True":
    (bot1, bot2) = (bot2, bot1)

bot2.write("1")

move = "0"

while(1):
    if bot1.isRunning():
        # try
        move = bot1.writeAndRead(move.strip())
    else:
        logWrite("v,0,PREMATURE TERMINATION")
        end_code(102)

    #a = input()

    # If program reaches here means bot1 returned a string
    validity = val.writeAndRead(move.strip())
    if validity.strip() != move.strip():
        # print(validity)
        logWrite("v,0," + move + " " + validity)
        end_code(102)

    # If program reaches here means string returned by bot1 is valid
    logWrite("v,0," + move)

    if bot2.isRunning():
        move = bot2.writeAndRead(move.strip())
    else:
        logWrite("v,1,PREMATURE TERMINATION")
        end_code(101)

    # If program reaches here means bot2 returned a string
    validity = val.writeAndRead(move.strip())
    if validity.strip() != move.strip():
        # print(validity)
        logWrite("v,1," + move + " " + validity)
        end_code(101)

    # If program reaches here means string returned by bot2 is valid
    logWrite("v,1," + move)

a = input()
