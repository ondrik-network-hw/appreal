#!/bin/sh

#Name of a PA
pa="*"
#Name of a NFA (for storing results)
name="*.reduced"
#NFA file
nfa="*.reduced.fa"
#Reduce path
reduce="*"

echo "Experiment with a PA ${pa}.fa"

touch tacas18/${name}-${pa}.log

file_labels="tacas18/${name}-${pa}-labels.log"
echo "Computing state labels"
(time python tools/subautomaton_weight.py -p ../experiments/tacas18/learning/${pa}.fa -a ../experiments/tacas18/${nfa} -m weight) &>> ${file_labels}

for i in {0..10..1}; do
   number="0.${i}"
   if [ $i -eq 10 ]; then
      number="1.0"
   fi

   file="tacas18/${name}-${pa}.log"

   echo "Reduction experiment: ${i}"
   (time python reduction.py -p ../experiments/tacas18/learning/${pa}.fa -a ../experiments/tacas18/${nfa} -d tacas18/${name}-${pa}-${number}.dot -o tacas18/${name}-${pa}-${number}.fa -t sl -m k -r ${number}) &>> ${file}

   echo " -- Converting to BA and VTF format"
   python tools/to_format.py -i tacas18/${name}-${pa}-${number}.fa -f fa -o tacas18/${name}-${pa}-${number}.ba -t ba
   python tools/to_format.py -i tacas18/${name}-${pa}-${number}.fa -f fa -o tacas18/${name}-${pa}-${number}.vtf -t vtf

   echo " -- Reduction using Rabit&Reduce"
   (time java -jar ${reduce} tacas18/${name}-${pa}-${number}.ba 12 -finite -o tacas18/${name}-${pa}-${number}.rabit.ba) &>> ${file}
   python tools/to_format.py -i tacas18/${name}-${pa}-${number}.rabit.ba -f ba -o tacas18/${name}-${pa}-${number}.reduced.fa -t fa
   python tools/to_format.py -i tacas18/${name}-${pa}-${number}.rabit.ba -f ba -o tacas18/${name}-${pa}-${number}.reduced.vtf -t vtf

   echo " -- Exact distance computation"
   (time python probabilistic_distance.py -p ../experiments/tacas18/learning/${pa}.fa -a ../experiments/tacas18/${name}.fa -b tacas18/${name}-${pa}-${number}.reduced.fa) &>> ${file}

   echo " -- Transforming to png"
   dot -Tpng tacas18/${name}-${pa}-${number}.dot -o tacas18/${name}-${pa}-${number}.png
done

