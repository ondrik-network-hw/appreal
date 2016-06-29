#include "parse.h"
#include <stdio.h>

int parse(char *input_string)
{
	char input_tmp[262144];
	int j = 0;
	
	// set input string as input of LEX
	yy_scan_string (input_string);
	
	// parse input pattern
	int ret = yyparse();
	
	// destroy scaner, could start over in one instance of main program
	// nefunguje na merlinovi
	//yylex_destroy();
	
	// return value of parser: 0, 1, ...
	return ret;
}
