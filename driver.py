#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager
import radical.utils as ru
import os
import os.path
import subprocess
import sys

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
PYTHON = os.environ.get('PYTHON', '/home/igor/.conda/envs/MD_ADIOS/bin/python')

run = sys.argv[1]
RESOURCE = os.environ.get('RESOURCE', 'local.localhost')

current_dir = os.getcwd()
run_dir = f'{current_dir}/run_{run}'
ADIOS_XML = f'{current_dir}/adios.xml'

config = ru.read_json(f'{current_dir}/config.json')

for d in ["new", "running", "stopped", "all"]:
    subprocess.getstatusoutput(f"mkdir -p  {run_dir}/simulations/{d}")

npipelines = 5    

def generate_simulation_pipeline(i):
    def post_stage():
        if(not os.path.exists(f'{run_dir}/aggregator/stop.aggregator') ):
            nstages = len(p.stages)
            s = Stage()
            s.name = f"{nstages}"
            t = Task()
            t.cpu_reqs = {'processes':1, 'process_type': None, 'threads_per_process':1, 'thread_type': None}
            t.gpu_reqs = {'processes': 0, 'process_type': None, 'threads_per_process': 0, 'thread_type': None}
            t.name = f" {i}_{nstages} "
            t.executable = PYTHON
            t.arguments = [f'{current_dir}/simulation.py', f'{run_dir}/simulations/all/{i}_{nstages}', ADIOS_XML]
            subprocess.getstatusoutput(f'ln -s  {run_dir}/simulations/all/{i}_{nstages} {run_dir}/simulations/new/{i}_{nstages}')
            s.add_tasks(t)
            s.post_exec = post_stage
            p.add_stages(s)
    p = Pipeline()
    nstages = len(p.stages)
    p.name = f"{i}"
    s = Stage()
    s.name = f"{nstages}"
    t = Task()
    t.name = f" {i}_{nstages} "
    t.executable = PYTHON
    t.arguments = [f'{current_dir}/simulation.py', f'{run_dir}/simulations/all/{i}_{nstages}', ADIOS_XML]
    subprocess.getstatusoutput(f'ln -s  {run_dir}/simulations/all/{i}_{nstages} {run_dir}/simulations/new/{i}_{nstages}')
    s.add_tasks(t)
    s.post_exec = post_stage
    p.add_stages(s)
    print(f"In generate_simulation_pipelin({i}): {nstages}")
    print("="*20)
    print(p.to_dict())
    print("="*20)
    print('-'*15)
    print(s.to_dict())
    print('-'*15)
    print('_'*10)
    print(t.to_dict())
    print('_'*10)

    return p

if(__name__ == "__main__"):

    pipelines = []
    
    for i in range(npipelines):
        pipelines.append(generate_simulation_pipeline(i))

    p = Pipeline()
    p.name = "AggregationP"
    s = Stage()
    s.name = "AggregationS"
    t = Task()
    t.cpu_reqs = {'processes':1, 'process_type': None, 'threads_per_process':1, 'thread_type': None}
    t.gpu_reqs = {'processes': 0, 'process_type': None, 'threads_per_process': 0, 'thread_type': None}
    t.name = "aggregator"
    t.executable = PYTHON
    t.arguments = [f'{current_dir}/aggregator.py', current_dir, run_dir]
    subprocess.getstatusoutput(f'mkdir -p {run_dir}/aggregator')
    s.add_tasks(t)
    p.add_stages(s)
    
    pipelines.append(p)

    print("After creating an aggregation pipeline")
    print("="*20)
    print(p.to_dict())
    print("="*20)
    print('-'*15)
    print(s.to_dict())
    print('-'*15)
    print('_'*10)
    print(t.to_dict())
    print('_'*10)

    appman = AppManager(hostname=hostname, port=port)


    print(config)

    res_dict = {
        'resource': RESOURCE,
        'walltime': 30,
        'cpus': config[RESOURCE]['cores'],
        'gpus': config[RESOURCE]['gpus'],
	'project': config[RESOURCE]['project'],
	'schema': config[RESOURCE]['schema'],
	'queue' : config[RESOURCE]['queue']
    }

    appman.resource_desc = res_dict
    appman.workflow = set(pipelines)
    appman.run()
