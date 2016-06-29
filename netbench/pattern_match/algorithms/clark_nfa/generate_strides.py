###############################################################################
#  generate_strides.py: Generating multistrided Clark NFAs
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Denis Matousek <imatousekd@fit.vutbr.cz>
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

import re
import time

from netbench.pattern_match import parser
from netbench.pattern_match.algorithms.clark_nfa import clark_nfa

"""
    This module generates multistrided Clark NFAs in specified configurations
"""

if __name__ == '__main__':

    rulesets_prefix = '../../rules/'
    rulesets = ['L7/great', 'L7/great-good', '100g/hanic']
    rulesets_suffix = '.pcre'
    strides = [1, 2, 4, 8, 16, 32, 64]

    report = open('report.txt', 'w')
    report.write('ruleset stride LUTs FFs BRAMs states ND-states transitions time\n')

    # Clark mapping method without support for char classes

    for ruleset in rulesets:
        for stride in strides:

            ruleset_filename = rulesets_prefix + ruleset + rulesets_suffix
            # remove any non-alphanumeric character
            ruleset_abc = re.sub('[\W_]', '', ruleset)

            print('Generating (%s,%d)...' % (ruleset_filename, stride))

            start = time.time()

            # Create clark_nfa object
            cn = clark_nfa.clark_nfa(True, stride)
            # Create parser - use default parser
            Test0 = parser.parser("pcre_parser")
            # Load RE file
            Test0.load_file(ruleset_filename)
            # Parse RE and create NFA
            cn.create_by_parser(Test0)
            # Call the compute method
            cn.compute()
            # Get number of used LUTs and FFs
            logic = cn.report_logic()

            stop = time.time()

            report.write('%s %d %d %d %d %d %d %d %f\n' % (ruleset_abc,
                stride, logic[0], logic[1], logic[2], cn.get_state_num(),
                len(cn.get_set_of_nondeterministic_states()),
                cn.get_trans_num(), stop - start))
            report.flush()

            # Save VHDL implementation
            vhd = open('clark_nfa_%s_%02d.vhd' % (ruleset_abc, stride), 'w')
            vhd.write(cn.get_HDL())
            vhd.close()

    report.close()
