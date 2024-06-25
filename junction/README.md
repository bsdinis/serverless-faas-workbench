# FunctionBench on Junction 
## Setting up the Environment 
### External Library Installation
All the necessary Python libraries for running the functions can be installed with the `setup_venv.sh` script.
```
cd serverless-faas-workbench/junction
./setup_venv.sh
```
## Running on Junction 
```
build/junction/junction_run <config_file> --ld_preload -- <repo_path>/junction/venv/bin/python3 <repo_path>/junction/run.py <function_name>
```
The function will warm up and stop itself. Run junction-ctl to interact with the tracer and send signals. For example, 
```
build/junction-ctl/junction-ctl 192.168.230.10 
> start-trace 1 
> signal 1 SIGCONT
> stop-trace 1
> signal 1 SIGCONT
```

`function_name` can be any of the supported FunctionBench functions. Currently they include:
- `chameleon` 
- `float_operation`
- `linpack`
- `matmul`
- `pyaes`
- `image_processing`
- `rnn_serving`
- `json_serdes`
- `video_processing`
- `lr_training`
- `cnn_serving`
