# AppReAL - Approximate Reduction of Automata and Languages

This repository contains a tool for (language non-preserving) reduction of non-deterministic finite automata (NFAs) wrt a probabilistic model (see the [technical report](https://arxiv.org/abs/1710.08647)) for more details.
The particular setting considered here is the reduction of NFAs obtained from PCREs (Perl compatible regular expressions) that occur in [Snort](https://www.snort.org) rules.

## Contents of directories

* `experiments/` - the setting of our experiments
* `netbench/` - the Netbench tool that we use to transform PCREs into NFAs
* `preproc/` - a bunch of small programs used for pre-processing network traffic PCAP files
* `reduce/` - the tool performing the reduction itself
* `regexps/` - regular expressions that we have collected

## Authors

* Milan Češka     :email: `<ceskam (at) fit.vutbr.cz>`
* **Vojtěch Havlena :email: `<ihavlena (at) fit.vutbr.cz>` (corresponding author)**
* Lukáš Holík     :email: `<holik (at) fit.vutbr.cz>`
* Ondřej Lengál   :email: `<lengal (at) fit.vutbr.cz>`
* Tomáš Vojnar    :email: `<vojnar (at) fit.vutbr.cz>`
