import importlib 
import sys
import json
import os
import signal

default_jsons = {
    "chameleon": '{"num_of_rows": 3, "num_of_cols": 4}',
    "float_operation": '{"N": 300}',
    "linpack": '{"N": 300}',
    "matmul": '{"N": 300}',
    "pyaes": '{"length_of_message": 20, "num_of_iterations": 3}',
    "image_processing": '{"path": "~/serverless-faas-workbench/dataset/image/animal-dog.jpg"}'
}

if len(sys.argv) < 2:
    print("usage: run.py <program-name> <optional: json>")
    exit()

prog = sys.argv[1]

if prog not in default_jsons:
    print(f"error: {prog} not in {default_jsons.keys()}")
    exit() 

json_string = default_jsons[prog]
if len(sys.argv) == 3:
    json_string = sys.argv[2]

json_req = json.loads(json_string)

# chameleon and pyaes are already py libraries; use modules from the directories instead
if prog == "chameleon" or prog == "pyaes":
    prog += "1"

main = importlib.import_module(f"cpu-memory.{prog}.main")

for i in range(10):
    print(main.function_handler(json_req))

os.kill(os.getpid(), signal.SIGSTOP)

print(main.function_handler(json_req))

os.kill(os.getpid(), signal.SIGSTOP)



