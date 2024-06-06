import importlib 
import sys
import json
import os
import signal

programs = {"chameleon", "float_operation", 
            "linpack", "matmul", "pyaes", "image_processing"}

unsupported = {"mapreduce", "model_serving", "model_training"}

if len(sys.argv) != 3:
    print("usage: run.py <program-name> <json>")
    exit()

prog = sys.argv[1]
json_string = sys.argv[2]

json_req = json.loads(json_string)

if prog not in programs:
    print(f"error: {prog} not in {programs}")
    exit() 

# chameleon and pyaes are already py libraries; use modules from the directories instead
if prog == "chameleon" or prog == "pyaes":
    prog += "1"

main = importlib.import_module(prog + ".main")

for i in range(10):
    print(main.function_handler(json_req))

os.kill(os.getpid(), signal.SIGSTOP)

print(main.function_handler(json_req))

os.kill(os.getpid(), signal.SIGSTOP)



