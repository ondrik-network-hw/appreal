if [ $# != 2 ]; then
    echo "./simscript file.pcap output.flow"
    exit
fi

# Input file
PCAPFILE="file.pcap"
PCAPFILE=`pwd`/$1

# Output file
FLOWFILE="output.flow"
FLOWFILE=`pwd`/$2
 
# Temporary file
TRACEFILE="tmp.hdr"

# Size of cache
let CACHESIZE=16*1024

# Additional parameters
RANKNAME=""
RANK=0

cd ../../../flowcontext/flowsim/
cd $NETBENCHPATH/netbench/flowcontext/flowsim/
make
cd ..

# Convert pcap file into packet header file
./genheaders.py ${PCAPFILE} > ${TRACEFILE}

# Load packet header file, simulate policy, output flow records
./testsim.py ${TRACEFILE} "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" 0 ${CACHESIZE} ${RANK} ${FLOWFILE}.tmp

# Select columns of interest
cat ${FLOWFILE}.tmp | cut -d, -f1-5,8-9 > ${FLOWFILE}
