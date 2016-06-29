#!/usr/bin/env python2

# Uses FAdo (python2):
#
#   doc: http://pythonhosted.org/FAdo/
#   git: https://github.com/Glavin001/FAdo
#
# To install:
#
# $ pip install FAdo

from FAdo.fa import *

m3 = NFA()
m3.setSigma(['0'])
m3.addState(0)
m3.addTransition(0, '0', 0)
print(m3)
