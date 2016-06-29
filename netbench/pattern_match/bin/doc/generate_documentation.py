###############################################################################
#  generate_documentation.py: Generate documentation for specific module
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

import commands
import sys
import re

def help():
    print "Usage: python generate_documentation.py param modules"
    print "Where:"
    print "    param: help       to invoke this help"
    print "           html       to make standalone HTML files"
    print "           dirhtml    to make HTML files named index.html in directories"
    print "           singlehtml to make a single large HTML file"
    print "           pickle     to make pickle files"
    print "           json       to make JSON files"
    print "           htmlhelp   to make HTML files and a HTML help project"
    print "           qthelp     to make HTML files and a qthelp project"
    print "           devhelp    to make HTML files and a Devhelp project"
    print "           epub       to make an epub"
    print "           latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
    print "           latexpdf   to make LaTeX files and run them through pdflatex"
    print "           text       to make text files"
    print "           man        to make manual pages"
    print "           changes    to make an overview of all changed/added/deprecated items"
    print "           linkcheck  to check all external links for integrity"
    print "           doctest    to run all doctests embedded in the documentation (if enabled)"
    print "    modules: Names of the modules for which the documentation is generated."
    print "             Do not use the '.py' suffix. If module is in subdirectory, "
    print "             use same syntax as when importing Netbench module (Eg. algorithms.clark_nfa.clark_nfa)."
    print "            Do not use the prefix 'netbench.pattern_match' in module name."
    
def write_file(file_name, module_name):
    f = open(file_name, "w");
    text  = "The :mod:`" + module_name + "` Module\n"
    text += "----------------------"
    for i in xrange(0, len(module_name)):
        text += "-"
    text += "\n"
    text += ".. automodule:: netbench.pattern_match." + module_name + "\n"
    text += "   :members:\n"
    text += "   :undoc-members:\n"
    text += "   :show-inheritance:\n"
    f.write(text)
    f.close()

def write_template(args):
    f = open("index.tmpl", "r")
    blob = f.read()
    f.close()
    
    g = open("index.rst", "w")
    tmp = re.split("%\$%", blob)
    data = ""
    for module in args:
        data += "   auto_" + module + "\n"
    result = tmp[0] + data + tmp[1]
    g.write(result)
    g.close()
    

if len(sys.argv) < 3: 
    help()
else:
    commands.getstatusoutput("rm auto_*.rst")
    for i in xrange(2, len(sys.argv)):
        write_file("auto_" + sys.argv[i] +".rst", sys.argv[i])
    write_template(sys.argv[2:len(sys.argv)])
    res = commands.getstatusoutput("make " + sys.argv[1])
    print(res[1])
    