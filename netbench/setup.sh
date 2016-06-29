#!/bin/sh
CURRENT_DIR=`pwd`
cd ..
NETBENCH_DIR=`pwd`
export PYTHONPATH=${PYTHONPATH}:${NETBENCH_DIR}
export NETBENCHPATH=${NETBENCH_DIR}
cd $CURRENT_DIR
echo "--------------------------------------------------------------------------"
echo "Path to NetBench common library was added into environment variable PYTHONPATH."
echo "Path to NetBench common library was added into environment variable NETBENCHPATH."
echo "The NETBENCHPATH variable is used internaly in Netbench."
echo
echo "Please add following line into your .bashrc:"
echo 'export PYTHONPATH=${PYTHONPATH}'":${NETBENCH_DIR}"
echo 'export NETBENCHPATH='"${NETBENCH_DIR}"
echo "--------------------------------------------------------------------------"
