module load python/3.7.0-anaconda3-5.3.0   
module load gcc/7.4.0
module load zeromq/4.2.5  
module load libfabric/1.7.0
source activate T20

export RADICAL_PILOT_VERBOSE="DEBUG"
export RADICAL_PILOT_LOG_LVL="DEBUG"
export RADICAL_VERBOSE=DEBUG
export RADICAL_LOG_TGT=r.log
export PYTHON=`which python`
export RESOURCE="ornl.summit"
export RADICAL_PROFILE=True
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENTK_PROFILE=True
export RMQ_HOSTNAME=129.114.17.233
export RMQ_PORT=33239
export RADICAL_PILOT_DBURL=mongodb://hyperrct:h1p3rrc7@129.114.17.233:27017/hyperrct

