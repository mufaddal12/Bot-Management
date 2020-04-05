# coding = UTF-8

from subprocess import call, Popen, PIPE
from select import poll, POLLIN
from signal import signal, alarm, SIGALRM, SIGPIPE, SIG_DFL
from sys import exit, argv
from time import sleep
# argv = ["newBm.py", "#extension of 1", "#extension of 2", "#log file name", "True or False if swap or no"]

print(argv)
(bot1Ext, bot2Ext, logFile, isP2) = (argv[1], argv[2], argv[3], argv[4])

botFile = "Bots/"
time_limits = {
    "cpp": 3,
    "c": 3,
    "py": 6,
}
bot1Time = time_limits[bot1Ext]
bot2Time = time_limits[bot2Ext]

call("g++ -o val val.cpp".split())

plist1 = ["prlimit", "-p", ""]
plist2 = ["prlimit", "-p", ""]


def processWrite(proc, string):
    proc.stdin.write(str.encode(string))
    proc.stdin.flush()


def processRead(proc, poll=None):
    sleep(1)
    ret = proc.stdout.readline()
    ret = ret.decode().strip()
    # print(ret)
    return ret


def giveAndTakeInput(string, proc):
    processWrite(proc, string)
    return processRead(proc)


def end_code(exit_code):
    if bot1.poll() is None:
        bot1.kill()
    if bot2.poll() is None:
        bot2.kill()
    if val.poll() is None:
        val.kill()
    exit(exit_code)


def getArgList(exType, p):
    lis = ["stdbuf", "-o0", "-i0", "-e0"]
    # lis = []
    if exType == "cpp" or exType == "c":
        lis = lis + ["./" + botFile + "player" + str(p)]
        plist1.extend(("--nofile=5", "--nproc=500", "--as=21460"))
    else:
        lis = lis + ["python", botFile + "player" + str(p) + ".py"]
        plist1.extend(("--nofile=5", "--nproc=500", "--as=32740"))
    return lis


bot1 = Popen(args=getArgList(bot1Ext, 1), stdin=PIPE, stdout=PIPE)
bot1Poll = poll()
bot1Poll.register(bot1.stdout.fileno(), POLLIN)

bot2 = Popen(args=getArgList(bot2Ext, 2), stdin=PIPE, stdout=PIPE)
bot2Poll = poll()
bot2Poll.register(bot2.stdout.fileno(), POLLIN)

val = Popen(args=["./val"], stdin=PIPE, stdout=PIPE)

plist1[2] = str(bot1.pid)
plist2[2] = str(bot2.pid)

# call(plist1)  # dont know this
# call(plist2)

if isP2 == "True":
    (bot1, bot2) = (bot2, bot1)
    (bot1Time, bot2Time) = (bot2Time, bot1Time)

msg = "0\n"
processWrite(bot1, "0\n")

msg = "1\n"
processWrite(bot2, "1\n")

while True:
    move = processRead(bot1)
    # print(move)
    move = move + "\n"

    validity = giveAndTakeInput(move, val)
    print(validity)

    if validity.strip() == move.strip():

        if not bot2.poll():

            move = giveAndTakeInput(move, bot2)
            move = move + "\n"

            validity = giveAndTakeInput(move, val)
            print(validity)

            if validity.strip() == move.strip():

                if not bot1.poll():
                    processWrite(bot1, move)

            else:
                print("bot1 won")
                end_code(101)  # weird thing dont know as of now

    else:
        print("bot2 won")
        end_code(102)  # weird thing dont know as of now
        break
end_code(101)
