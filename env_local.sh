module load adios2/2.5.0-gcc750
module load Anaconda3/2020.02
source activate MD_ADIOS

export RADICAL_PILOT_DBURL="mongodb://localhost/RP1"
export RADICAL_PILOT_VERBOSE="DEBUG"
export RADICAL_PILOT_LOG_LVL="DEBUG"
export RADICAL_VERBOSE=DEBUG
export RADICAL_LOG_TGT=r.log
export PYTHON=`which python`
export RESOURCE="local.localhost"
