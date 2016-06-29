#!/bin/python
###############################################################################
#  b_ptrn_match.py: Module for PATTERN MATCH - base virtual pattern match class
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Vlastimil Kosar <ikosar@fit.vutbr.cz>
###############################################################################
#
#  LICENSE TERMS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. All advertising materials mentioning features or use of this software
#     or firmware must display the following acknowledgement:
#
#       This product includes software developed by the University of
#       Technology, Faculty of Information Technology, Brno and its
#       contributors.
#
#  4. Neither the name of the Company nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  This software or firmware is provided ``as is'', and any express or implied
#  warranties, including, but not limited to, the implied warranties of
#  merchantability and fitness for a particular purpose are disclaimed.
#  In no event shall the company or contributors be liable for any
#  direct, indirect, incidental, special, exemplary, or consequential
#  damages (including, but not limited to, procurement of substitute
#  goods or services; loss of use, data, or profits; or business
#  interruption) however caused and on any theory of liability, whether
#  in contract, strict liability, or tort (including negligence or
#  otherwise) arising in any way out of the use of this software, even
#  if advised of the possibility of such damage.
#
#  $Id$


class b_ptrn_match:
    """ 
        Base class for the pattern_match experiments. It defines only basic functions.
    """
    def __init__(self):
        """ 
            Constructor of the pattern_match experiments. It initializes the value for consumed memory and consumed logic. Every inherited approach has to set these two variables to valid values.
        """
        self._consumed_memory = 0;
        self._consumed_logic = 0;
        
    def report_memory(self):
        """ 
            Reports amount of the memory consumed by this algorithm. The returned number is in the bytes.
            
            :returns: Amount of the memory consumed/
            :rtype: int
        """
        return self._consumed_memory
    
    def report_logic(self):
        """ 
            Reports amount of logic consumed by the algorithm. The meaning of this value can differs depending on the approach (number of cores in multicore versus number of LUTs in FPGA. For specific information check the report function of the child.
            
            :returns: Amount of logic consumed by the algorithm.
            :rtype: Depends on the algorithm.
        """
        return self._consumed_logic
    
    def search(self, input_string):
        """
            This function will find patterns in the given string by the specified approach.
           
            :param input_string: String in which will be the patterns found.
            :type input_string: string
            :returns: Bitmap of matched patterns. Match is indicated by 1, mismatch by 0. Number of fields in this array is equal to the count of patterns.
            :rtype: list(int)
        """

###############################################################################
# End of File b_ptrn_match.py                                                 #
###############################################################################