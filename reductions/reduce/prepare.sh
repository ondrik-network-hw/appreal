#!/bin/sh

#Name of an NFA
name="*"
#Reduce path
reduce="*"

echo "Converting to BA format"
python tools/to_format.py -i ../experiments/tacas18/${name}.fa -f fa -o ../experiments/tacas18/${name}.ba -t ba

echo "Reducing using Rabit&Reduce"
java -jar ${reduce} ../experiments/tacas18/${name}.ba 12 -finite -o ../experiments/tacas18/${name}.reduced.ba

echo "Converting to FA format"
python tools/to_format.py -i ../experiments/tacas18/${name}.reduced.ba -f ba -o ../experiments/tacas18/${name}.reduced.fa -t fa

echo "Converting to VTF format"
python tools/to_format.py -i ../experiments/tacas18/${name}.reduced.fa -f fa -o ../experiments/tacas18/${name}.reduced.vtf -t vtf

echo "Dividing automaton to subautomata"
python tools/subautomaton_weight.py -p ../experiments/tacas18/learning/http-protocol-prob.fa -a ../experiments/tacas18/${name}.reduced.fa -m divide
