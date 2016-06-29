###############################################################################
#  b_state.py: Module for PATTERN MATCH - base state class
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

import pattern_exceptions

types = {"b_State":'0', "ColouredState":'1'}
""" Maps class name to coresponding class specification char. For testing if object is of specified state class this dictionary have to be used. """
reverse_types = {'0':"b_State", '1':"ColouredState"}

class b_State:
    """
        A base class for state representation.


        :param mid: State unique identification number
        :type mid: int
        :param rnum: Set of regular expression numbres. If set is empty the state is not final. The set of regular expression numbers identify which RE are matched in particular final state.
        :type rnum: set(int)
    """
    def __init__(self, mid = 0, rnum = set()):
        """ Class constructor.

            :param mid: State unique identification number
            :type mid: int
            :param rnum: Set of regular expression numbres. If set is empty the state is not final. The set of regular expression numbers identify which RE are matched in particular final state.
            :type rnum: set(int)
        """
        self._id    = mid;   # State identification value
        self._rnum  = rnum;  # Regular expression numbers (final state), set value
        self.ctype  = types["b_State"]
        self.stypes = [types["b_State"]]

    def get_text(self):
        """
            Returns text description for graph representation.

            :returns: Text description of state
            :rtype: string
        """
        return str(self._id)

    def get_id(self):
        """
            Returns state identification number.

            :returns: State identification number
            :rtype: int
        """
        return self._id

    def set_id(self, new_id):
        """ Sets the id of state to new_id.

            :param new_id: New unique state  identification number.
            :type new_id: int
        """
        self._id = new_id

    def is_final(self):
        """
            Returns true if the state is a final state.

            :returns: True if the state is a final state, False otherwise.
            :rtype: boolean
        """
        return self._rnum != set()

    def get_regexp_number(self):
        """
            Returns set of indexes of regular expression, which corresponds to the
            final state. If empty set value is returned the state is not final and
            do not represent any regular expression.

            :returns: Set of regular expression numbres coresponding to the state
            :rtype: set(int)
        """
        return self._rnum;

    def set_regexp_number(self, new_rnum):
        """
            Sets set of indexes of regular expression, which corresponds to the
            final state. If empty set is set the state is not final and
            do not represent any regular expression.

            :param new_rnum: New set of regular expression numbres
            :type new_rnum: Set of Int
        """
        self._rnum = new_rnum

    def get_type(self):
        """
            Returns type of state.

            :returns: Returns type of state.
            :rtype: int
        """

        return self.ctype

    def get_support_type(self):
        """
            Returns supported types of states for current type of state.

            :returns: Returns supported types of states for current type of state.
            :rtype: list(int)
        """
        return self.stypes

    def join(self, other):
        """
            Joins using self and other state. Creates new state.

            :param other: Other state.
            :type other: b_State
            :returns: New joined state.
            :rtype: b_State
            :raises: state_join_exception() if join can't be computed.
        """
        if other.get_type() in self.get_support_type():
            return self.compute_join(other)
        elif self.get_type() in other.get_support_type():
            return other.compute_join(self)
        else:
            raise pattern_exceptions.state_join_exception(self.get_type(), other.get_type())

    def compute_join(self, other):
        """
            Computes join of two states. Note that new state ID must be set after. Default value is -2.

            :param other: Second state.
            :type other: b_State
            :returns: Joined states.
            :rtype: b_State
        """
        return b_State(-2, self.get_regexp_number() | other.get_regexp_number())

    def __str__(self):
        """
            Returns state identification value as string.

            :returns: Text description of state
            :rtype: string
        """
        return str(self._id)

    def __repr__(self):
        """
            Returns representation of state identification value and regular expression numeber.

            :returns: Text description of state
            :rtype: string
        """
        return "<" + str(self._id) + ", " + str(self._rnum) + ">"


###############################################################################
# End of File b_state.py                                                      #
###############################################################################
