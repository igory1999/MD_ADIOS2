* There are N simulations running, at each time step sending data to the aggregator via ADIOS
* The communication is blocking: a simulation cannot proceed to the next time step until its output is read by the aggregator
* Each simulation and the aggregator runs in its own Pipeline. 
* Each Pipeline has one Stage with one Task.
* When a Stage finishes, another Stage is started via post_exec
* To set the environment:
  ```source env_local.sh```
  or
  ```source env_summit.sh```
* Notice that in both cases Anaconda environment is used into which Radical and ADIOS are installed.
* To run
  ```make```
* To clean
  ```make clean```
* Current problem: it runs fine on an Ubuntu laptop, however, on Summit the first Pipeline starts and then blocks forever 
  waiting to communicate with the aggregator which is never started (and neither are other simulations), 
  so apparently Pipelines are running sequentially and not in parallel on Summit. 
