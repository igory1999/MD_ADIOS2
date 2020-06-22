#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager
import os
import os.path
import subprocess
import sys

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
PYTHON = "/home/igor/.conda/envs/MD_ADIOS/bin/python"

run = sys.argv[1]

current_dir = os.getcwd()
run_dir = f'{current_dir}/run_{run}'
ADIOS_XML = f'{current_dir}/adios.xml'

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
    t.name = "aggregator"
    t.executable = PYTHON
    t.arguments = [f'{current_dir}/aggregator.py', current_dir, run_dir]
    subprocess.getstatusoutput(f'mkdir -p {run_dir}/aggregator')
    s.add_tasks(t)
    p.add_stages(s)
    
    pipelines.append(p)

    appman = AppManager(hostname=hostname, port=port)

    res_dict = {
        'resource': 'local.localhost',
        'walltime': 10,
        'cpus': 6,
        'gpus': 1
    }

    appman.resource_desc = res_dict
    appman.workflow = set(pipelines)
    appman.run()
