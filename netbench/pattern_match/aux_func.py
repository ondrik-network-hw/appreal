###############################################################################
#  aux_func.py: Module for PATTERN MATCH - auxiliary functions
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

""" 
    Module containing auxiliary functions for classes, scripts, etc.
"""
import pattern_exceptions
import os
import sys
import subprocess
import uuid
import datetime

def create_temp_file_name(prefix = "temp", sufix = "tmp"):
    """
        Create temporary filename, should be very unique. The filename is created from prefix, timestamp, uuid and sufix. The file name will be: prefix_time_uuid.sufix. The time format is "%d%m%y_%H%M%S".
        
        :param prefix: Prefix of the file name. Defaults to temp.
        :type prefix: string
        :param sufix: Suffix of the file name. Defaults to tmp.
        :type sufix: string
        
        :returns: Unique file name.
        :rtype: string
    """
    time = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
    uuidd = str(uuid.uuid4())
    return prefix + "_" + time + "_" + uuidd + "." + sufix

def delete_temp_file(filename):
    """
        Delete temporary file.
        
        :param filename: Prefix of the file name. Defaults to temp.
        :type filename: string
    """
    try:
        os.remove(filename)
    except Exception:
        pass

def getPatternMatchDir():
    """ 
        Parses the NETBENCHPATH environment variable and returns path to pattern match.
        
        :raises: no_netbench_path_variable() if environment variable NETBENCHPATH doesn't exist.
        :returns: Path to Netbench base dir.
        :rtype: string
    """
    try:
        pypath = os.environ['NETBENCHPATH'].split(os.pathsep)

        for path in pypath:
                return path + "/netbench/pattern_match"
    except Exception:
        raise pattern_exceptions.no_netbench_path_variable()

def isPickle(fileName):
    """
        Acording to suffix of file name determinates if file is pickled object (.pkl) or ruleset.
        
        :param fileName: Name of input file
        :type fileName: string
        :returns: True if pickled object, otherwise return False.
        :rtype: boolean
    """
    
    parts = fileName.split('/')
    name = parts[len(parts) - 1]
    nameParts = name.rsplit('.', 1)
    if nameParts[1] == "pkl":
        return True
    else:
        return False
        
def deprecation_warning(element_type, old_name, new_name):
    """
        Prints deprecation warning on stderr.
        
        :param element_type: Type of deprecated element. Eg. module, class, method, function.
        :type element_type: string
        :param old_name: Name of deprecated element.
        :type old_name: string
        :param new_name: Name of new element.
        :type new_name: string
    """
    sys.stderr.write("WARNING: The " + element_type + " " + old_name + " is deprecated and may be removed in future versions of Netbench. Use the " + element_type + " " + new_name + ".\n")
    
def getstatusoutput(cmd, input_data):
    """
        Run command with arguments and return its output as a string.
        :param cmd: Command to run.
        :type cmd: string
        :param input_data: Data to be passed to stdin. If no data are being passes set this param to None.
        :type input_data: string
        :returns: Exit code and content of std_out and std_err.
        :rtype: tuple(int, string, string)
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = process.communicate(input_data)
    retcode = process.poll()
    # Remove trailing \n
    output = str(output)
    err = str(err)
    if len(output) > 0:
        if output[len(output) - 1] == '\n':
            output = output[0:len(output)-1]
    return [retcode, output, err]

###############################################################################
# End of File aux_func.py                                                     #
###############################################################################