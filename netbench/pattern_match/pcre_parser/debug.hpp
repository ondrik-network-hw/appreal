#include <iostream>

#ifndef DEBUG
#ifndef ALLDEBUG
	// separate debug and debug_header in each source file
	#define DEBUG(str)    if (debug) cout << DEBUG_HEADER << "\t: " << str
#else
	#define DEBUG(str)    if (debug) cout << str
#endif
	#define DEBUG_CONT(str)    if (debug) cout << str
#endif