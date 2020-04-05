from subprocess import Popen, PIPE

objpy = Popen(args=["python", "child.py"], stdout=PIPE, stdin=PIPE)
objcpp = Popen(args=["./a.out"], stdout=PIPE, stdin=PIPE)
msg = "hellofromparent\n"

objcpp.stdin.write(str.encode(msg))
objcpp.stdin.flush()
outcpp = objcpp.stdout.read()
msg = outcpp.decode()
print(msg)

msg = msg + '\n'

objpy.stdin.write(str.encode(msg))
objpy.stdin.flush()
outpy = objpy.stdout.read()
msg = outpy.decode()
print(msg)
# print(obj.poll())

# print(out.decode())
