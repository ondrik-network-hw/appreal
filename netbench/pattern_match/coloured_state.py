###############################################################################
#  colored_state.py: Module for PATTERN MATCH - state with asociated colors
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
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

from b_state import b_State, types
import pattern_exceptions
import copy

class ColouredState(b_State):
    """
        State class with asociated colours.

        :param mid: State unique identification number.
        :type mid: int
        :param rnum: Set of regular expression numbres. If set is empty the state is not final. The set of regular expression numbers identify which RE are matched in particular final state. 
        :type rnum: set(int)
        :param colours: State colours.
        :type colours: set(int)
        :param join_method: Method of merging colours during join operation. Supported values: union, intersection, difference and symmetric_difference. NOTE: In automaton should be used only one method for all coloured states, as colour operation is determinated only by first state in join operation.
        :type join_method: string
    """

    def __init__(self, mid, rnum, colours, join_method = "union"):
        """
            Class constructor.

            :param mid: State unique identification number.
            :type mid: int
            :param rnum: Set of regular expression numbres. If set is empty the state is not final. The set of regular expression numbers identify which RE are matched in particular final state. 
            :type rnum: set(int)
            :param colours: State colours.
            :type colours: set(int)
            :param join_method: Method of merging colours during join operation. Supported values: union, intersection, difference and symmetric_difference. NOTE: In automaton should be used only one method for all coloured states, as colour operation is determinated only by first state in join operation.
            :type join_method: string
        """
        b_State.__init__(self, mid, rnum)
        self.colours = colours
        self.join_method = join_method
        self.ctype  = types["ColouredState"]
        self.stypes = [types["b_State"], types["ColouredState"]]

    def get_text(self):
        """
            Returns text description for graph representation.
            
            :returns: Text description of state
            :rtype: string
        """
        text = ""
        for colour in self.colours:
            text += "~" + str(colour) 
        return '"' + str(self._id) + text + '"'

    def get_colours(self):
        """
            Returns colours of state.
            
            :returns: Colours of state.
            :rtype: set(int)
        """
        
        return copy.copy(self.colours)

    def set_colours(self, colours):
        """
            Sets colours of state.
            
            :param colours: New colours of state.
            :type colours: set(int)
        """
        
        self.colours = colours
        
    def get_join_method(self):
        """
            Returns join method of state.
            
            :returns: Join method of state.
            :rtype: string
        """
        
        return self.join_method

    def set_join_method(self, join_method):
        """
            Sets join method of state.
            
            :param join_method: New join method of state.
            :type join_method: string
        """
        
        self.join_method = join_method

    def compute_join(self, other):
        """
            Computes join of two states. Note that new state ID must be set after. Default value is -2.
            
            :param other: Second state.
            :type other: b_State
            
            :returns: Joined state.
            :rtype: ColouredState
            
            :raises: state_colour_operation_not_supported_exception if unsupported join method is set.
        """
        if other.get_type() == types["b_State"]:
            colours_other = set()
        else:
            colours_other = other.get_colours()
        colours_new = set()
        
        if self.join_method == "union":
            colours_new = self.get_colours() | colours_other
        elif self.join_method == "intersection":
            colours_new = self.get_colours() & colours_other
        elif self.join_method == "difference":
            colours_new = self.get_colours() - colours_other
        elif self.join_method == "symmetric_difference":
            colours_new = self.get_colours() ^ colours_other
        else:
            raise pattern_exceptions.state_colour_operation_not_supported_exception(self.join_method) 
            
        return ColouredState(-2, self.get_regexp_number() | other.get_regexp_number(), colours_new, self.join_method)

    def __str__(self):
        """
            Returns state identification value as string.
        
            :returns: Text description of state
            :rtype: string
        """
        return str(self._id) + ", " + str(self.colours)

    def __repr__(self):
        """ 
            Returns representation of state identification value, regular expression number and colours.
            
            :returns: Text description of state
            :rtype: string
        """
        return "<" + str(self._id) + ", " + str(self._rnum) + ", " + str(self.colours) + ">"