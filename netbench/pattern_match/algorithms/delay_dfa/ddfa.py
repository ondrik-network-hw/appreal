############################################################################
#  ddfa.py: Module for PATTERN MATCH algorithm Delayed Input DFA
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol
############################################################################
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
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
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

"""Module for pattern match: algorithm for Delayed Input DFA."""

from netbench.pattern_match.pattern_exceptions import COMPUTE_ERROR, DETERMINISTIC_ERROR
from netbench.pattern_match import sym_char, sym_char_class, b_symbol, pattern_exceptions
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State

class DELAY_DFA(b_dfa):
    """
        Class for Delayed Input DFA automat.
        
        Based on:
            "Algorithms to accelerate multiple regular expressions matching 
            for deep packet inspection"
            ISBN: 1-59593-308-5
            URL: http://portal.acm.org/citation.cfm?id=1159952
            
        Delayed Input DFA substantially reduces space requirements as compared 
        to a DFA. DDFA is constructed by transforming a DFA via incrementally 
        replacing several transitions of the automaton with a single default
        transition. A DDFA represents reduces transitions by more than 95%.
    """

    def __init__(self):
        """
            Constructor - initializes object attribute:
            diameterBound - diameter bound, default 0 (no limit)
        """
        
        b_dfa.__init__(self)
        self.diameterBound = 0 # diameter bound, default 0 (no limit)

    def compute(self, c_dfa = True):
        """
            This method computes Delayed Input DFA automat.
            
            :param c_dfa: compute DFA(Delault is true,so compute() is called 
                          to create DFA)
            :type c_dfa: bool
            
            :raises: COMPUTE_ERROR
        """

        if c_dfa == True:
            b_dfa.compute(self)

            #Check if dfa was computed.
            if not self.get_compute():
                raise COMPUTE_ERROR

        self._make_ddfa()

    def _make_ddfa(self):
        """
            This method changes Deterministic FA into Delayed Input DFA to make
            default transitions.
            
            :raises: DETERMINISTIC_ERROR
        """
        automat = self._automaton

        # Check if the automat is deterministic.
        if not self.has_flag("Deterministic") \
           or self.get_flag("Deterministic") == False:
            raise DETERMINISTIC_ERROR

        # Creation of spanning trees.
        s_t = []
        s_t = self._create_spanning_trees(automat)
    
        # Selection of root nodes.
        # A root is a node which has the shortest way to all other states.
        roots = self._selection_of_roots(s_t)
        
        # Default transitions.
        self._def_trans = {} 
        
        # Compute default transitions in spanning trees.
        for tree in s_t:
            # Compute default transitions directed to root
            for n_s in tree.n_s[roots[s_t.index(tree)]]:
                self._def_trans[n_s] = roots[s_t.index(tree)]
            computed = [roots[s_t.index(tree)]]
            not_computed = tree.n_s[roots[s_t.index(tree)]]
            # Compute the other default transitions.
            while len(not_computed) != 0:
                computed += not_computed
                tmp = []
                for s in not_computed:
                    for n_s in tree.n_s[s]:
                        if n_s not in computed:
                            self._def_trans[n_s] = s
                            tmp.append(n_s)
                not_computed = tmp        
        
        # Add new symbol with text description "default" and symbol 
        # identification value a_l(alphabet length).
        a_l = len(automat.alphabet)
        automat.alphabet[a_l] = \
        b_symbol.DEF_SYMBOLS("default", a_l)
    
        # Sort transitions.
        sort_trans = {}
        for i in range(0, len(automat.states), 1):
            sort_trans[i] = []
        for trans in automat.transitions:
            sort_trans[trans[0]].append(trans[1:])
    
        # Replace the equal transitions with the default transitions.
        for s in self._def_trans:
            # Delete the equal transitions.
            for k in range(0, len(sort_trans[s]), 1):
                if sort_trans[s][k] in sort_trans[self._def_trans[s]]:
                    automat.transitions.remove  \
                    ((s, sort_trans[s][k][0], sort_trans[s][k][1]))
            # Replace the deleted transitions with default transition.
            automat.transitions.add((s, a_l, self._def_trans[s]))
        
        # Set automat flag.
        automat.Flags["Delay DFA"] = True
        self._compute = True

    def _create_spanning_trees(self, automat):
        """
            This method creates spanning trees from dfa.
            
            :param automat: The automat from which spanning trees are created.
            :type automat: b_dfa
            :returns: Array of spanning trees
            :rtype: array(SPANNING_TREE)
        """
        # Compute weight set.
        weight_set = self._compute_weight_set(automat)
        
        # States already added to spanning tree(s)
        a_s = []  
        
        # Spanning trees
        s_t = []
        
        for i in range(255, 0, -1):
            if i in weight_set:
                # Select edge from weight_set[i] which leads to the smallest 
                # growth in the diameter of the default tree.
                while len(weight_set[i]) != 0:
                    for_delete = []
                    # smallest growth diameter edge
                    small_edge = 0
                    # diameter of the smallest edge
                    small_edge_d = 0  
                    # tree in which the smallest edge is
                    small_edge_t = 0  
                    for edge in weight_set[i]:
                        new_tree = True
                        for tree in s_t:
                            # Check if states from the edge are already 
                            # in a tree.
                            if edge[0] in tree.s and edge[1] in tree.s:
                                # If condition is true, do not add the edge 
                                # to any tree and just skip it.
                                for_delete.append(edge)
                                new_tree = False
                                break
                            # Check if one state from edge exists in tree.
                            elif edge[0] in tree.s or edge[1] in tree.s:
                                new_tree = False
                                # Check if edge connects two trees.
                                if edge[0] in a_s and edge[1] in a_s:
                                    # Find second tree
                                    if edge[0] in tree.s:
                                        tree0 = tree
                                        for t in s_t:
                                            if edge[1] in t.s:
                                                tree1 = t
                                    else:
                                        tree1 = tree
                                        for t in s_t:
                                            if edge[0] in t.s:
                                                tree0 = t
                                    
                                    # Compute diameter.
                                    diameter0 = self._compute_diameter(tree0, edge)
                                    diameter1 = self._compute_diameter(tree1, edge)
                                    if diameter0 == 0 or diameter1 == 0:
                                        diameter = 0
                                    else:
                                        diameter = diameter0 + diameter1
                                # Edge joining two states in the same tree.
                                else :
                                    diameter = self._compute_diameter(tree, edge)

                                # Check if edge maintains diameter bound.
                                if diameter == 0:
                                    for_delete.append(edge)
                                    break
                                # Lowest diameter, immediately join edge to tree.
                                elif diameter == 1:
                                    if edge[0] in tree.s:
                                        tree.s.append(edge[1])
                                        tree.n_s[edge[0]].append(edge[1])
                                        tree.n_s[edge[1]] = [edge[0]]
                                        a_s.append(edge[1])
                                    else :
                                        tree.s.append(edge[0])
                                        tree.n_s[edge[1]].append(edge[0])
                                        tree.n_s[edge[0]] = [edge[1]]
                                        a_s.append(edge[0])
                                        for_delete.append(edge)
                                        break
                                # Check the smallest edge.
                                else :
                                    if small_edge_d == 0:
                                        small_edge_d = diameter
                                        small_edge = edge
                                        small_edge_t = s_t.index(tree)
                                    elif diameter < small_edge_d:
                                        small_edge_d = diameter
                                        small_edge = edge
                                        small_edge_t = s_t.index(tree)
                        
                        # There is no tree to which we can add current edge. 
                        # We create new tree.
                        if new_tree:
                            # Create new tree and add current edge to it 
                            s_t.append(SPANNING_TREE())
                            s_t[-1].s = [edge[0], edge[1]]
                            s_t[-1].n_s[edge[0]] = [edge[1]]
                            s_t[-1].n_s[edge[1]] = [edge[0]]
                            a_s.append(edge[0])
                            a_s.append(edge[1])
                            for_delete.append(edge)
                    
                    # Adding the smallest (in growth diameter) edge 
                    # in the tree.
                    if small_edge_d != 0:
                        # Check if the edge connects two trees.
                        if small_edge[0] in a_s and small_edge[1] in a_s:
                            # Find second tree
                            if small_edge[0] in s_t[small_edge_t].s:
                                tree0 = s_t[small_edge_t]
                                for t in s_t:
                                    if small_edge[1] in t.s:
                                        tree1 = t
                            else :
                                tree1 = s_t[small_edge_t]
                                for t in s_t:
                                    if small_edge[0] in t.s:
                                        tree0 = t
                                             
                            # Merger trees.           
                            tree0.s += tree1.s              
                            tree0.n_s.update(tree1.n_s)
                            s_t.remove(tree1)
                            tree0.n_s[small_edge[0]].append(small_edge[1])
                            tree0.n_s[small_edge[1]].append(small_edge[0])
                        # Connect the edge to the tree
                        else :
                            if small_edge[0] in s_t[small_edge_t].s:
                                s_t[small_edge_t].s.append(small_edge[1])
                                s_t[small_edge_t].n_s[small_edge[0]].append(small_edge[1])
                                s_t[small_edge_t].n_s[small_edge[1]] = [small_edge[0]]
                                a_s.append(small_edge[1])
                            else :
                                s_t[small_edge_t].s.append(small_edge[0])
                                s_t[small_edge_t].n_s[small_edge[1]].append(small_edge[0])
                                s_t[small_edge_t].n_s[small_edge[0]] = [small_edge[1]]
                                a_s.append(small_edge[0])
                        for_delete.append(small_edge)
                    
                    # Delete the marked edges.
                    for m_edge in for_delete:
                        weight_set[i].remove(m_edge)
        return s_t
    
    def _compute_weight_set(self, automat):
        """
            This method computes weight set in automat.
            
            :param automat: Automat in which weight set is computed.
            :type automat: b_dfa
            :returns: Set of arrays of pair states among which the weight 
                      is computed
            :rtype: set(array(int,int))
        """
        weight_set = {}
        
        # Sort transitions.
        sort_trans = {}
        for i in range(0, len(automat.states), 1):
            sort_trans[i] = []
        for trans in automat.transitions:
            sort_trans[trans[0]].append(trans[1:])
        
        # For each combination of 2 states compute their weight of reduction 
        # transitions
        for i in range(0, len(automat.states) - 1, 1):
            for j in range(i + 1, len(automat.states), 1):
                space_reduction = 0
                # Compute number of same transitions
                for k in range(0, len(sort_trans[i]), 1):
                    if sort_trans[i][k] in sort_trans[j]:
                        space_reduction += 1
                # Decrement by 1 because of default transition
                space_reduction = space_reduction - 1
                # Append combination of states i and j to weight_set,
                # if they got reduced
                if space_reduction > 0:
                    if space_reduction in weight_set:
                        weight_set[space_reduction].append((i,j))
                    else:
                        weight_set[space_reduction] = []
                        weight_set[space_reduction].append((i,j))
        return weight_set
            
    def _selection_of_roots(self, s_t):
        """
            This method selects root in each spanning tree.
            
            :param s_t: Array of spanning trees
            :type s_t: array(SPANNING_TREE)
            :returns: Array of roots
            :rtype: array(int)
            
            Root is node which has the shortest way to all others states.
        """        
        roots = [-1] * len(s_t)
        for tree in s_t:
            # Best state diameter
            best_state_d = 0  
            for s in tree.s:
                distance = 1
                diameter = 0
                computed = [s]
                not_computed = tree.n_s[s]
                while len(not_computed) != 0:
                    diameter += len(not_computed) * distance
                    distance += 1
                    computed += not_computed
                    tmp = []
                    for state in not_computed:
                        for x in tree.n_s[state]:
                            if x not in computed:
                                tmp.append(x)
                    not_computed = tmp
                if best_state_d == 0:
                    roots[s_t.index(tree)] = s
                    best_state_d = diameter
                elif diameter < best_state_d:
                    roots[s_t.index(tree)] = s
                    best_state_d = diameter
        return roots
  
    def set_bound(self, d_b = 0):
        """
            This method sets diameter bound. 
           
            :param d_b: diameter bound
            :type d_b: int
            
            Default is zero, which means no limit in construction of Delay DFA.
        """

        self.diameterBound = d_b

    def get_default_trans_num(self):
        """
            This method returns the number of default transitions 
            in Delay DFA automaton.
            
            :returns: number of default transitions
            :rtype: int
        """

        numberDefTrans = 0
        defaultSymbolID = -1

        for symbolID in self._automaton.alphabet:
            if isinstance(self._automaton.alphabet[symbolID], b_symbol.DEF_SYMBOLS):
                defaultSymbolID = symbolID
        if defaultSymbolID != -1:
            for t in self._automaton.transitions:
                if t[1] == defaultSymbolID:
                    numberDefTrans += 1
        return numberDefTrans

    def _compute_diameter(self, tree, edge):
        """
            This method computes the diameter of connecting edge to the tree.
            
            :param tree: spanning tree to be connect edge
            :type tree: SPANNING_TREE
            :param edge: edge for which compute diameter
            :type tree: array(int)
            :returns: diameter of edge
            :rtype: int
        """

        distance = 1
        diameter = 0

        if edge[0] in tree.s:
            s = edge[0]
        else :
            s = edge[1]
        computed = [s]
        not_computed = tree.n_s[s]
        while len(not_computed) != 0:
            diameter += len(not_computed) * distance
            # Check if edge maintain the diameter bound.
            if self.diameterBound != 0 and distance >= self.diameterBound:
                return 0
            distance += 1
            computed += not_computed
            tmp = []
            for state in not_computed:
                for x in tree.n_s[state]:
                    if x not in computed:
                        tmp.append(x)
            not_computed = tmp
        return diameter

    def search(self, input_string):
        """
            This function will find patterns in the given string.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """
        # Stack of states. State is list (tupple) consisting of state 
        # and unprocessed part of input string.
        Stack = list()
        # Set of actual states.
        ActState = set()

        # Create start state.
        ActState.add((self._automaton.start, input_string, False))
        # Add start state to stack.0
        Stack.append(ActState)

        # Create mapping between reg. exp. number and coresponding final 
        # states.
        sameFinal = dict()
        for fstate in self._automaton.final:
            rnums = self._automaton.states[fstate].get_regexp_number()
            for rnum in rnums:
                if rnum in sameFinal:
                    sameFinal[rnum].add(fstate)
                else:
                    sameFinal[rnum] = set()
                    sameFinal[rnum].add(fstate)

        # Compute number of reg. exp.
        rules = len(sameFinal)
        # dictionary is no longer needed.
        sameFinal = None

        # Init bitmap to zeros.
        bitmap = [0] * rules

        # If needed create mapping between states and outgoing transitions.
        _mapper = dict()
        for transition in self._automaton.transitions:
            if transition[0] in _mapper:
                _mapper[transition[0]].add((transition[1], transition[2]))
            else:
                _mapper[transition[0]] = set()
                _mapper[transition[0]].add((transition[1], transition[2]))

        # Until stack is empty, search
        while len(Stack) != 0:
            # Pop state from stack.
            ActState = Stack.pop()
            newActState = set()
            
            # Create new state. Accept char if possible and add state 
            # to new state.
            for state in ActState:
                if state[0] in _mapper:
                    unacc = 1
                    delay = False
                    for transition in _mapper[state[0]]:
                        # Delay transition
                        if state[0] in self._def_trans and self._def_trans[state[0]] == transition[1]:
                            delay = True
                            continue
                        else:
                            try:
                                # Handle strided automaton, add padding 
                                # characters if needed (when size of string 
                                # is smaller than size of stride)
                                astr = ""
                                if self._automaton.states[transition[1]].is_final():
                                    if self._automaton.Flags.has_key("Stride") and len(state[1]) < self._automaton.Flags["Stride"]:
                                        mod = len(state[1]) % self._automaton.Flags["Stride"]
                                        if mod != 0:
                                            for i in xrange(0, self._automaton.Flags["Stride"] - mod):
                                                astr += chr(0)
                                                    
                                res = self._automaton.alphabet[transition[0]].accept(state[1] + astr)
                            except pattern_exceptions.symbol_accept_exception:
                                unacc += 1
                            except:
                                pass
                            else:
                                newActState.add((transition[1],res,False))
                    if delay == True and len(_mapper[state[0]]) == unacc and len(state[1]) > 0:
                        newActState.add((self._def_trans[state[0]],state[1],True))
                # If in final state, set coresponding bitmap field to 1.
                if self._automaton.states[state[0]].is_final() == True and not state[2]:
                    for rnum in self._automaton.states[state[0]].get_regexp_number():
                        bitmap[rnum] = 1
            # If possible add new state to stack.
            if len(newActState) > 0:
                Stack.append(newActState)

        # Return bitmap.
        return bitmap

    def SaveToFile(self, FileName):
        """
            This method creates the file which represents the Delay DFA 
            automat. This file will be input into algorithm written 
            in C language.
            
            :param FileName: Name of file into which Delay DFA automat 
                             representation will be saved.
            :type FileName: string
        """

        a = self._automaton
        fw = open(FileName, 'w')

        # Write the number of states
        fw.write(str(len(a.states)) + '\n')
        
        # Write ALPHABET
        alphabet = ""
        length = ""
        pom_length = 0
        for index in range(0, len(a.alphabet), 1):
            if isinstance(a.alphabet[index], sym_char.b_Sym_char):
                alphabet += str(ord(str(a.alphabet[index]))) + '|'
                length += str(pom_length) + "->" + str(pom_length) + '|'
                pom_length += 1
            elif isinstance(a.alphabet[index], sym_char_class.b_Sym_char_class):
                for char in a.alphabet[index].charClass:
                    alphabet += str(ord(char)) + '|'
                length += str(pom_length) + "->" + str(pom_length + \
                    len(a.alphabet[index].charClass) - 1) + '|'
                pom_length += len(a.alphabet[index].charClass)
        fw.write(str(len(a.alphabet) - 1) + '\n' + length + '\n')
        length_alphabet = len(alphabet.split('|')) - 1
        fw.write(str(length_alphabet) + "->" + alphabet + '\n')
        
        # Write START STATE
        fw.write(str(a.start) + '\n')
        
        # Write TRANSITIONS
        # Sort transitions
        sort = {}
        for s in range(0, len(a.states)):
            sort[s] = []
        for t in a.transitions:
            if t[1] != 'def':
                sort[t[0]].append(t[1:])
        
        # Transitions in string
        t_str = ""
        # Count transitions for state
        c_t = ""  
        for s in range(0, len(a.states)):
            c_t += str(len(sort[s])) + '|'
            for i in range(0, len(sort[s])):
                t_str += str(sort[s][i][0]) + '->' + str(sort[s][i][1]) + '|'
        fw.write(c_t + '\n' + t_str + '\n')
        
        # Write FINAL STATES
        final = ""
        for x in list(a.final):
            final += str(x) + '|'
        fw.write(str(len(a.final)) + '\n' + final + '\n')
        
        # Write DEFAULT TRANSITIONS
        # Default transitions in string
        d_t = ""  
        for state in range(0, len(a.states), 1):
            if state in self._def_trans:
                d_t += str(self._def_trans[state]) + '|'
            else:
                d_t += str(-1) + '|'
        fw.write(d_t + '\n')

class SPANNING_TREE():
    """
        Class for representation one spanning tree, which are needed 
        for finding default transitions.
    """

    def __init__(self):
        """
            Constructor - construct basic items.
            s - states in tree
            n_s - neighbours states
        """

        self.s = []   # states in tree
        self.n_s = {} # neighbours states
