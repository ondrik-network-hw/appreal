PCAP-Ex-Tractor
===============
Extracts payloads from packets within a PCAP file and writes them into a text
file.  There are two text file formats to choose from.

Text hexa format
----------------
The format contains packets, one per line, each expressed using hexadecimal
codes of the bytes, separated by a space, e.g.,
```
3A 2F 2F 77 77 77 2E 79 61 68 6F 6F 2E 63
6F 6D 2F 65 78 74
2F 6D 73 66 69 6E 64 66 61 73 74 2F 69 6E 64 65 78 32 2E 68 74 6D 6C 22 20 4E 41 4D 45 3D 22 72 69 67 68 74 22 20 4E 4F 52 45 53 49 5A 45 20 53 43 52 4F 4C 4C 49 4E 47 3D 4E 4F 3E 0D 0A 09 09 09 3C 46 52 41 4D 45 20 4D 41 52 47 49 4E 57 49 44 54 48 3D 22 30 22 20 4D 41 52 47 49 4E 48 45
```

SPiCe format
------------
This format is used in the [SPiCe competition](http://spice.lif.univ-mrs.fr).
The first line contains two fields: the number of samples and the size of the alphabet, separated by a whitespace.
The body of the file has a line for every packet.
Each line of the body starts with the length of the packet, followed by a sequence of numbers (base-10) from the range \[0, alphabet size-1\].
Example:
```
2 256
9 1 2 3 4 5 6 7 8 7
4 42 0 255 3
```


Prerequisities
==============
Needs
```
libpcap0.8-dev
g++
make
```

Compiling
=========
Run
```
make
```

Running
=======
Run
```
./pcap-ex-tractor [-t|-s] INPUT.pcap > OUTPUT.txt
```
