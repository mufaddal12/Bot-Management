Things left to do:
1. process address space limit or poll() class object time limit problem
2. address space has been increased to 20MB for cpp bots and 40 MB for python for time being but has to be reduced(problem above)

Running the bm:
argv is a list of arguments passed along with the command to call this program
argv[0] : Name of Source file (here "newBm.py")
argv[1] : Extension of bot 1 : "c" or "cpp" or "py"
gv[2] : Extension of bot 2 : "c" or "cpp" or "py"
argv[3] : Name of file in which logs are to be written
argv[4] : If bot1 is playing as player 2 or not : "True" or "False"

python newBM.py cpp py logFileName True

player1 has cpp bot
player2 has py bot
logs will be stored in file named logFileName
True: player2 will player first
