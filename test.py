from subprocess import call, Popen, PIPE


class Process:
    def __init__(self, ext=None, player=None, timeLimit=None):
        # lis = ["stdbuf", "-o0", "-i0", "-e0"]
        # lis = lis + ["./Bots/player" + str(player)]
        self.memLimit = 21340
        lis = self.getArgList(ext, player)
        self.proc = Popen(args=lis, stdin=PIPE, stdout=PIPE)
        call(
            [
                "prlimit",
                "--nofile=5",
                "--nproc=500",
                "--as=" + str(self.memLimit),
                "-p",
                str(self.proc.pid),
            ]
        )
        # self.pollObj = poll()
        # self.pollObj.register(self.proc.stdout.fileno(), POLLIN)

    def getArgList(self, exType, p):
        # This function returns a list of terminal commands (depending on type of bot) needed for running the bot
        lis = []
        lis = ["stdbuf", "-o0", "-i0", "-e0"]
        if exType == "cpp" or exType == "c":
            lis = lis + ["./" + "Bots/" + "player" + str(p + 1)]
        elif exType == "py":
            lis = lis + ["python", "Bots/" + "player" + str(p + 1) + ".py"]
            # self.memLimit = 32740
            # self.plist[3] = "--as=30000000"  # "--as=32740"
        return lis


c = Process(ext="cpp", player=0)
# b = Process(ext="py", player=1)
"""bot1 = Popen(["./Bots/player1"], stdin=PIPE, stdout=PIPE)
bot2 = Popen(["./Bots/player2"], stdin=PIPE, stdout=PIPE)

call(["prlimit", "--as=21460", "-p", str(bot1.pid)])
call(["prlimit", "--as=21460", "-p", str(bot2.pid)])

bot1.stdin.write(b"0\n")
bot2.stdin.write(b"1\n")"""
a = input()
