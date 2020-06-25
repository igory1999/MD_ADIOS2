* There are N simulations running, at each time step sending its data to the aggregator via adios
* The communication is blocking: simulation cannot proceed to the next time step until its output is read by the aggregator
* Each simulation and the aggregator run in its own pipeline. 
* The pipeline has 1 Stage with one Task.
* When a stage finishes, another stage is started via post_exec
* To set the environment:
  ```source env_local.sh```
  or
  ```source env_summit.sh```
* Notice that in both cases Anaconda environment is used in which Radical and Adios are installed.
* To run
  ```make```
* To clean
  ```make clean```
* Current problem: it runs fine on an ubuntu laptop, however, on summit the first pipeline starts and than blocks waiting to communicate with 
