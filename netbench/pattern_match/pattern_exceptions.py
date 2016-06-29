###############################################################################
#  pattern_exceptions.py: Module for PATTERN MATCH - Module of all pattern
#                                                    match exceptions
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

"""
    This module groups all exceptions of Netbench - Pattern Match.
"""

import b_symbol
import b_state

###############################################################################
# General exceptions.                                                         #
###############################################################################
class general_pattern_exception(Exception):
    """
        Base class for all exceptions defined in pattern match part of the Netbench.
    """
    pass

class general_not_implemented(general_pattern_exception):
    """
        Class for raising general NOT IMPLEMENTED Exceptions. This exception
        should be used when some method, class, function or feature is defined
        but not implemented yet.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """
    def __init__(self, msg = ""):
        """
            Constructor of general_not_implemented class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: NOT IMPLEMENTED: This feature is not implemented!"

    def __str__(self):
        """
            Returns string containing text description of general_not_implemented.

            :returns: Text description.
            :rtype: string
        """
        dsc = self.text
        if len(self.msg) != 0:
            dsc += self.text + "\nDescription: " + self.msg
        return dsc

class general_unsupported_type(general_pattern_exception):
    """
        Class for raising exception if unsuported data typy was pased to method.

        :param method: String with name of method which raised the exception.
        :type method: string
        :param name: Name of object which caused the exception.
        :type name: string
        :param obj: Object which caused the exception.
        :type obj: Any type
        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """
    def __init__(self, method, name, obj, msg = ""):
        """
            Constructor of symbol_id_collision class.

            :param method: String with name of method which raised the exception.
            :type method: string
            :param name: Name of object which caused the exception.
            :type name: string
            :param obj: Object which caused the exception.
            :type obj: Any type
            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string
        """
        self.msg = msg
        self.method = method
        self.name = name
        self.obj = obj
        self.text = "ERROR: Unsupported type " + str(type(self.obj)) + " of " + self.name + " pased to method " + self.method

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        dsc = "\n  "
        if len(self.msg) != 0:
            dsc += self.text + "\n  Description: " + self.msg
        return dsc
###############################################################################
# Symbol specific exceptions.                                                 #
###############################################################################

class symbol_accept_exception(general_pattern_exception):
    """
        Class for raising symbol acception Exceptions.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """
    def __init__(self, msg = ""):
        """
            Constructor of symbol_accept_exception class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: Symbol accept exception: Symbol not matched in the beginning of the string!"

    def __str__(self):
        """
            Returns string containing text description of symbol_accept_description.

            :returns: Text description.
            :rtype: string
        """
        dsc = self.text
        if len(self.msg) != 0:
            dsc += self.text + "\nDescription: " + self.msg
        return dsc

class symbol_string_to_short(general_pattern_exception):
    """
        Class for raising symbol exception if the passed string to accept method is shorter than length of the symbol.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """
    def __init__(self, msg = ""):
        """
            Constructor of symbol_string_to_short class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: Symbol accept exception: String passed to the accept method is shorter than length of the symbol!"

    def __str__(self):
        """
            Returns string containing text description of symbol_string_to_short.

            :returns: Text description.
            :rtype: string
        """
        dsc = self.text
        if len(self.msg) != 0:
            dsc += self.text + "\nDescription: " + self.msg
        return dsc

class symbol_import_exception(general_pattern_exception):
    """
        Class for raising symbol exception if the detected type of class in import string doesn't corespond to the class of the symbol.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """
    def __init__(self, msg = ""):
        """
            Constructor of symbol_import_exception class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: Symbol import exception: Detected type of class in import string doesn't corespond to the class of the symbol!"

    def __str__(self):
        """
            Returns string containing text description of symbol_import_exception.

            :returns: Text description.
            :rtype: string
        """
        dsc = self.text
        if len(self.msg) != 0:
            dsc += self.text + "\nDescription: " + self.msg
        return dsc

class symbol_resolve_collision_exception(general_pattern_exception):
    """
        Class for raising symbol exception if collision cannot be resolved. Neither symbol is able to resolve collision with other symbol.

        :param ftype: Class of the first symbol.
        :type ftype: int
        :param stype: Class of the second symbol.
        :type stype: int
    """
    def __init__(self, ftype, stype):
        """
            Constructor of symbol_resolve_collision_exception class.

            :param ftype: Class of the first symbol.
            :type ftype: int
            :param stype: Class of the second symbol.
            :type stype: int
        """
        self.text = "ERROR: Symbol resolve collision exception: Collision between symbol of type " + b_symbol.io_reverse_mapper[ftype] + " and symbol of type " + b_symbol.io_reverse_mapper[ftype] + " cannot be resolved!"

    def __str__(self):
        """
            Returns string containing text description of symbol_resolve_collision_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class symbol_equality_exception(general_pattern_exception):
    """
        Class for raising symbol exception if symbol equality cannot be resolved. Neither symbol is able to resolve equality with other symbol.

        :param ftype: Class of the first symbol.
        :type ftype: int
        :param stype: Class of the second symbol.
        :type stype: int
    """
    def __init__(self, ftype, stype):
        """
            Constructor of symbol_equality_exception class.

            :param ftype: Class of the first symbol.
            :type ftype: int
            :param stype: Class of the second symbol.
            :type stype: int
        """
        self.text = "ERROR: Symbol equality exception: Equality between symbol of type " + b_symbol.io_reverse_mapper[ftype] + " and symbol of type " + b_symbol.io_reverse_mapper[ftype] + " cannot be determinated!"

    def __str__(self):
        """
            Returns string containing text description of symbol_resolve_collision_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class symbol_double_stride_exception(general_pattern_exception):
    """
        Class for raising symbol exception if double stride cannot be resolved. Neither symbol is able to compute double stride with other symbol.

        :param ftype: Class of the first symbol.
        :type ftype: int
        :param stype: Class of the second symbol.
        :type stype: int
    """
    def __init__(self, ftype, stype):
        """ Constructor of symbol_double_stride_exception class.

            :param ftype: Class of the first symbol.
            :type ftype: int
            :param stype: Class of the second symbol.
            :type stype: int
        """
        self.text = "ERROR: Symbol double stride exception: Double stride with first symbol of type " + b_symbol.io_reverse_mapper[ftype] + " and second symbol of type " + b_symbol.io_reverse_mapper[ftype] + " cannot be resolved!"

    def __str__(self):
        """
            Returns string containing text description of symbol_resolve_collision_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

###############################################################################
# State specific exceptions.                                                  #
###############################################################################
class state_join_exception(general_pattern_exception):
    """
        Class for raising state exception if join cannot be resolved. Neither state is able to compute join with other symbol.

        :param ftype: Class of the first state.
        :type ftype: int
        :param stype: Class of the second state.
        :type stype: int
    """
    def __init__(self, ftype, stype):
        """ Constructor of state_join_exception class.

            :param ftype: Class of the first state.
            :type ftype: int
            :param stype: Class of the second state.
            :type stype: int
        """
        self.text = "ERROR: State join exception: Join with first state of type " + b_state.reverse_types[ftype] + " and second state of type " + b_state.reverse_types[stype] + " cannot be resolved!"

    def __str__(self):
        """
            Returns string containing text description of state_join_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class state_colour_operation_not_supported_exception(general_pattern_exception):
    """
        Class for raising state exception if unsupported join colour operation is required.

        :param operation: Requested operation.
        :type operation: string
    """
    def __init__(self, operation):
        """
            Constructor of state_colour_operation_not_supported_exception class.

            :param operation: Requested operation.
            :type operation: string
        """
        self.text = "ERROR: Usupported colour join operation:" + operation + ". Only union, intersection, difference and symmetric_difference are supported"

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

###############################################################################
# nfa_data specific exceptions.                                               #
###############################################################################
class nfa_data_import_exception(general_pattern_exception):
    """
        Class for raising symbol exception if the detected type of class in import string doesn't corespond to any class of the symbol.

        :param msg: String containing the detected type of class in import string.
        :type msg: string
    """
    def __init__(self, msg):
        """
            Constructor of nfa_data_import_exception class.

            :param msg: String containing the detected type of class in import string.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: nfa_data.ImportFromFsm(): Unknown symbol string type (" + msg + "), coresponding class can not be determinated."

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class symbol_not_found(general_pattern_exception):
    """
        Class for raising symbol exception if symbol have not been found in alphabet during retrival of its alphabet id.

        :param msg: String containing string description of the symbol.
        :type msg: string
    """
    def __init__(self, msg):
        """
            Constructor of symbol_not_found class.

            :param msg: String containing string description of the symbol.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: nfa_data.get_symbol_id(): Symbol (" + msg + ") have not been found in alphabet so its id coudn't be determinated."

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class state_id_collision(general_pattern_exception):
    """
        Class for raising state exception if state id collision in automaton occured.

        :param state_id: Id of the state, which caused the collision.
        :type state_id: int
    """
    def __init__(self, state_id):
        """
            Constructor of state_id_collision class.

            :param state_id: Id of the state, which caused the collision.
            :type state_id: int
        """
        self.state_id = state_id
        self.text = "ERROR: nfa_data.add_states(): State with id (" + str(state_id) + ") have caused state id collision in automaton."

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class symbol_id_collision(general_pattern_exception):
    """
        Class for raising symbol exception if symbol id collision in automaton occured.

        :param symbol_id: Id of the symbol, which caused the collision.
        :type symbol_id: int
    """
    def __init__(self, symbol_id):
        """
            Constructor of symbol_id_collision class.

            :param symbol_id: Id of the symbol, which caused the collision.
            :type symbol_id: int
        """
        self.symbol_id = symbol_id
        self.text = "ERROR: nfa_data.add_symbols(): Symbol with id (" + str(symbol_id) + ") have caused symbol id collision in automaton."

    def __str__(self):
        """
            Returns string containing text description of nfa_data_import_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class COMPUTE_ERROR(general_pattern_exception):
    """
        Class for raising COMPUTE_ERROR exception if something happen with variable self._compute of automaton. For example, does not exist or has unexpected value.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """

    def __init__(self, msg = ""):
        """
            Constructor of COMPUTE_ERROR class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string.
        """

        self.msg = msg
        self.text = "ERROR: COMPUTE_ERROR"

class ALPHABET_COLLISION_FREE_ERROR(general_pattern_exception):
    """
        Class for raising ALPHABET_COLLISION_FREE_ERROR exception if something happen with "Alphabet collision free" flag of automaton. For example, does not exist or has unexpected value.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """

    def __init__(self, msg = ""):
        """
            Constructor of ALPHABET_COLLISION_FREE_ERROR class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string.
        """

        self.msg = msg
        self.text = "ERROR: ALPHABET_COLLISION_FREE_ERROR"

class DETERMINISTIC_ERROR(general_pattern_exception):
    """
        Class for raising DETERMINISTIC_ERROR exception if something happen with "Deterministic" flag of automaton. For example, does not exist or has unexpected value.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """

    def __init__(self, msg = ""):
        """
            Constructor of DETERMINISTIC_ERROR class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string.
        """

        self.msg = msg
        self.text = "ERROR: DETERMINISTIC_ERROR"

class MINIMAL_ERROR(general_pattern_exception):
    """
        Class for raising MINIMAL_ERROR exception if something happen with "Minimal" flag of automaton. For example, does not exist or has unexpected value.

        :param msg: Optional string describing the cause of the exception. Defaults to empty string.
        :type msg: string
    """

    def __init__(self, msg = ""):
        """
            Constructor of MINIMAL_ERROR class.

            :param msg: Optional string describing the cause of the exception. Defaults to empty string.
            :type msg: string.
        """

        self.msg = msg
        self.text = "ERROR: MINIMAL_ERROR"


class not_strided_exception(general_pattern_exception):
    """
        Class for raising exception if automaton is not strided.
    """
    def __init__(self):
        """
            Constructor of not_strided_exception class.
        """
        self.text = "ERROR: Automaton is not strided."

    def __str__(self):
        """
            Returns string containing text description of not_strided_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class empty_automaton_exception(general_pattern_exception):
    """
        Class for raising exception if automaton is empty.
    """
    def __init__(self):
        """
            Constructor of empty_automaton_exception class.
        """
        self.text = "ERROR: Automaton is empty."

    def __str__(self):
        """
            Returns string containing text description of empty_automaton_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class not_epsilon_free_automaton_exception(general_pattern_exception):
    """
        Class for raising exception if automaton is empty.
    """
    def __init__(self):
        """
            Constructor of not_epsilon_free_automaton_exception class.
        """
        self.text = "ERROR: Automaton is not epsilon free."

    def __str__(self):
        """
            Returns string containing text description of not_epsilon_free_automaton_exception.

            :returns: Text description.
            :rtype: string
        """
        return self.text
        
class not_a_timbuk_file(general_pattern_exception):
    """
        Class for raising symbol exception if file is not a timbuk formated file.

        :param msg: String containing the detected type of class in import string.
        :type msg: string
    """
    def __init__(self, msg):
        """
            Constructor of not_a_timbuk_file class.

            :param msg: String containing the file name.
            :type msg: string
        """
        self.msg = msg
        self.text = "ERROR: load_from_timbuk(): File " + msg + " is not in timbuk format or original file was not generated by Netbench."

    def __str__(self):
        """
            Returns string containing text description of not_a_timbuk_file.

            :returns: Text description.
            :rtype: string
        """
        return self.text

###############################################################################
# Algorithms specific exceptions.                                             #
###############################################################################

###############################################################################
# Environment specific exceptions.                                            #
###############################################################################
class no_netbench_path_variable(general_pattern_exception):
    """
        Class for raising exception if environment variable NETBENCHPATH is not set.
    """
    def __init__(self):
        """
            Constructor of empty_automaton_exception class.
        """
        self.text = "ERROR: Environment variable NETBENCHPATH is not set. Run the setup.sh script and then add the environment variable NETBENCHPATH into your .bashrc."

    def __str__(self):
        """
            Returns string containing text description of no_netbench_path_variable.

            :returns: Text description.
            :rtype: string
        """
        return self.text

class pcre_parser_failure(general_pattern_exception):
    """
        Class for raising exception if pcre parser C-based implementation can not be run or compiled. Version for PCRE parser.
    """
    def __init__(self):
        """
            Constructor of pcre_parser_failure class.
        """
        self.text = "ERROR: PCRE C-based parser failure. Check if gcc, g++, flex and bison are installed. Try run make clean; make parser manually in pcre_parser directory of Netbench:PatternMatch. Test if compiled parser (pcre_parser/parser) can be run."

    def __str__(self):
        """
            Returns string containing text description of pcre_parser_failure.

            :returns: Text description.
            :rtype: string
        """
        return self.text
        
###############################################################################
# Parser specific exceptions.                                                 #
###############################################################################
class unknown_parser(general_pattern_exception):
    """
        Class for raising unknown parser exception. This exception
        is used when unknown parser class name is passed to parser mataclass for wrapping any parser under single interface.

        :param msg: Name of the class that caused this exception.
        :type msg: string
    """
    def __init__(self, msg = ""):
        """
            Constructor of unknown_parser class.

            :param msg: Name of the class that caused this exception.
            :type msg: string
        """
        self.text = "ERROR: Parser class named " + msg + " is unknown! Check spelling of the name or pass the parser object directly."

    def __str__(self):
        """
            Returns string containing text description of general_not_implemented.

            :returns: Text description.
            :rtype: string
        """
        return self.text
###############################################################################
# End of file pattern_exceptions.py                                           #
###############################################################################
