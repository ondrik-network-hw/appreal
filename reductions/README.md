# Approximate Reduction of Automata

Prototype tool for approximate reduction of NFAs used in network traffic
filtering writen in Python. The tool provides the reduction of NFAs using the pruning reduction
and the self-loop reduction. The tool provides also the computation of the
probabilistic distance. Moreover, scripts for better utilization in the context of network
monitoring, s.t., preparation of a PA learning, evaluation of the error on the
traffic and scripts for handling with larger automata, are included.

## Installation
The prototype tool is written in Python 2.7. Required Python libraries:
 - **NumPy** for linear algebra operations,
 - **PuLP** for solving (integer) linear programming problems,
 - **FAdo** for operations with finite automata,
 - **Scapy** for operations with PCAP files.

 For the learning PAs, the [Treba](https://code.google.com/archive/p/treba) tool
 is needed. The executable binary file of Treba must be placed in the folder
 *learning*.

## Automata Format
NFAs are specified using the **FA format**, which is given as follows.
```
<initial state>\n
:(<symbol in hexa> )*\n
(<source state> <destination state> <symbol in hexa>\n)*
(<final state>\n)*
```
An example of the content of a FA file.
```
0
:0x61 0x62
0 1 0x61
1 2 0x61
2 3 0x62
3 4 0x62
4 0 0x61
2
3
4
```

PAs are specified using the Treba format, which given as follows. The initial
state is implicitly the state 0.
```
<source state> <destination state> <symbol in dec> <probability>\n)*
(<final state> <probability>\n)*
```
An example of the content of a Treba file.
```
0 0 97 0.5
0 0 98 0.4
0 0.1
```

## Example of Usage
The probabilistic distance can be computed using the following script.
```
$ ./probabilistic_distance.py -p pa.fa -a nfa1.fa -b nfa2.fa
```
The reduction is provided by the script *reduction.py*.
```
$ ./reduction.py -p pa.fa -a nfa.fa -o out.fa --type=sl --mode=eps --restriction=0.5
```

## Contributors
- Vojtěch Havlena <xhavle03[at]stud.fit.vutbr.cz>
