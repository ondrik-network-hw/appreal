/**
 * Testovací aplikace parseru PCRE
 * - aplikace čte ze stdin a načtené řetězce předává parseru
 * - aplikace odstraňuje znaky konce nových řádků z konce načtených vstupů
 *
 * @date 2010-12-12
 * @author Milan Pála (xpalam00@stud.fit.vutbr.cz)
 */

#include <stdio.h>
#include <string.h>
#include "parse.h"
#include "interface.h"
#include <getopt.h>

#define PROGRAM_ERR 4;

int debug = 0;
int silent = 0;

void help()
{
	printf("Usage: parser [-hdsotfera]\n");
	printf("- Parse PCRE pattern from STDIN\n");
	printf("\t-h print this help\n");
	printf("\t-d debug mode\n");
	printf("\t-s silent mode\n");
	printf("\t-o output MSFM file (e.g. STDOUT; default nfa.msfm)\n");
	printf("\t-t output DOT file (e.g. graph.dot; default OFF)\n");
	printf("\t-f specify file as input, default STDIN\n");
	printf("\t-e export format of symbols: hex (default), dec\n");
	printf("\t-r PCRE strict mode, show warning if diferent then PCRE behavior\n");
	printf("\t-a ASCII means 0-127\n");
	printf("\t-c counting constraints are code into symbols\n");
	printf("\t-E do not export EOF on /a$/ pattern\n");
}

int main(int argc, char ** argv)
{
	FILE *input;
	int ret = 0;

	input = stdin;

	T_CONFIG config;
	strcpy(config.outputDotFile, "");
	strcpy(config.outputMsfmFile, "nfa.msfm");
	strcpy(config.charExport, "hex");
	config.strict = 0;
	config.lowAscii = 0;
	config.ccSymbols = 0;
	config.eofExport = 1;

	char c;
	// process parameters
	while ((c = getopt(argc, argv, "hdso:t:e:f:racE")) != -1)
	{
		switch (c)
		{
		case 'h':
			help();
			return 0;
		case 'd':
			debug = 1;
			break;
		case 's':
			silent = 1;
			break;
		case 'o':
			strcpy(config.outputMsfmFile, optarg);
			break;
		case 't':
			strcpy(config.outputDotFile, optarg);
			break;
		case 'f':
			input = fopen(optarg, "r");
			break;
		case 'e':
			if( strcmp("dec", optarg) == 0 ) strcpy(config.charExport, "dec");
			break;
		case 'r':
			config.strict = 1;
			break;
		case 'a':
			config.lowAscii = 1;
			break;
		case 'c':
			config.ccSymbols = 1;
			break;
		case 'E':
			config.eofExport = 0;
			break;
		case '?':
			if (optopt == 'c') fprintf (stderr, "Option -%c requires an argument.\n", optopt);
			return PROGRAM_ERR;
		default:
			fprintf(stderr, "Unknown argument -%c\n", optopt);
			return PROGRAM_ERR;
		}
	}

	if(input == NULL)
	{
		fprintf(stderr, "Input could not open.\n");
		return PROGRAM_ERR;
	}


	while( fgets(config.inputPattern, 262143 , input) != NULL )
	{
		// odstraním znak nového řádku z konce regulárního výrazu
		if( config.inputPattern[strlen(config.inputPattern)-1] == '\n' ) config.inputPattern[strlen(config.inputPattern)-1] = '\0';
		module_init(config);
		ret += parse(config.inputPattern);
		module_exit(ret);
	}

	return ret;
}
