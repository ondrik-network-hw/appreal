/**
 * Modul Painter
 * - modul vykreslí vytvořený derivační strom
 * - derivační strom je uložen do souboru config.outputDotFile ve formátu DOT
 *
 * @date 2010-12-12
 * @author Milan Pála (xpalam00@stud.fit.vutbr.cz)
 */

#include <stdio.h>
#include <string.h>
#include "interface.h"
#include "painter.hpp"
#include "debug.hpp"

#define DEBUG_HEADER "painter"
extern int debug;

#include <stack>
using namespace std;

FILE *graphFile;

int node = 0;
int node1=0, node2=0;

stack<int> nodes;

void module_init(T_CONFIG config)
{
	graphFile = fopen(config.outputDotFile, "w");

	fprintf(graphFile, "digraph PCRE {\n");
	fprintf(graphFile, "label = \"%s\"\n", config.inputPattern);
	//painter("node [shape=solid];\n");
}

void module_exit(int ret)
{
	fprintf(graphFile, "}\n");

	fclose(graphFile);
}

void print_stack()
{
	//printf("Velikost zasobniku: %d\n", nodes.size());
	/*for(int i=0; i<stack.size(); i++)
	{
		cout << stack
	}*/
}

