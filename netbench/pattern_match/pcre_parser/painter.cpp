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

// pcre <<< modif_front pattern modif_rear
void pcre2modif_front_pattern_modif_rear(){
	print_stack();
	DEBUG("pcre <<< modif_front pattern modif_rear" << endl);
	node2 = ++node; // vytvori nonterminal pcre
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pcre %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_rear %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("pcre <<< modif_front pattern modif_rear" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pattern
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pcre %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"pattern %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("pcre <<< modif_front pattern modif_rear" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pcre %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_front %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front <<< pcre_delim
void modif_front2pcre_delim(){
	print_stack();
	DEBUG("modif_front <<< pcre_delim" << endl);
	node2 = ++node; // vytvori nonterminal modif_front
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre_delim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"pcre_delim %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front <<< modif_front_ext-pcre_delim
void modif_front2modif_front_ext_pcre_delim(){
	print_stack();
	DEBUG("modif_front <<< modif_front_ext-pcre_delim" << endl);
	node2 = ++node; // vytvori nonterminal modif_front
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre_delim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"pcre_delim %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("modif_front <<< modif_front_ext-pcre_delim" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front_ext
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_front_ext %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front_ext <<< modif_front_unit
void modif_front_ext2modif_front_unit(){
	print_stack();
	DEBUG("modif_front_ext <<< modif_front_unit" << endl);
	node2 = ++node; // vytvori nonterminal modif_front_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_front_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front_ext <<< modif_front_unit-modif_front_ext
void modif_front_ext2modif_front_unit_modif_front_ext(){
	print_stack();
	DEBUG("modif_front_ext <<< modif_front_unit-modif_front_ext" << endl);
	node2 = ++node; // vytvori nonterminal modif_front_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front_ext
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_front_ext %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("modif_front_ext <<< modif_front_unit-modif_front_ext" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_front_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_front_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front_unit <<< UTF8
void modif_front_unit2UTF8(){
	print_stack();
	DEBUG("modif_front_unit <<< UTF8" << endl);
	node1 = ++node; // vytvori terminal UTF8
	node2 = ++node;  // vytvori nonterminal modif_front_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"UTF8 %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_front_unit <<< UCP
void modif_front_unit2UCP(){
	print_stack();
	DEBUG("modif_front_unit <<< UCP" << endl);
	node1 = ++node; // vytvori terminal UCP
	node2 = ++node;  // vytvori nonterminal modif_front_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_front_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"UCP %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear <<< pcre_delim
void modif_rear2pcre_delim(){
	print_stack();
	DEBUG("modif_rear <<< pcre_delim" << endl);
	node2 = ++node; // vytvori nonterminal modif_rear
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre_delim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"pcre_delim %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear <<< pcre_delim-modif_rear_ext
void modif_rear2pcre_delim_modif_rear_ext(){
	print_stack();
	DEBUG("modif_rear <<< pcre_delim-modif_rear_ext" << endl);
	node2 = ++node; // vytvori nonterminal modif_rear
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear_ext
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_rear_ext %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("modif_rear <<< pcre_delim-modif_rear_ext" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pcre_delim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"pcre_delim %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_ext <<< modif_rear_unit
void modif_rear_ext2modif_rear_unit(){
	print_stack();
	DEBUG("modif_rear_ext <<< modif_rear_unit" << endl);
	node2 = ++node; // vytvori nonterminal modif_rear_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_ext <<< modif_rear_unit-modif_rear_ext
void modif_rear_ext2modif_rear_unit_modif_rear_ext(){
	print_stack();
	DEBUG("modif_rear_ext <<< modif_rear_unit-modif_rear_ext" << endl);
	node2 = ++node; // vytvori nonterminal modif_rear_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear_ext
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_rear_ext %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("modif_rear_ext <<< modif_rear_unit-modif_rear_ext" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear_ext
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_ext %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_CASELESS
void modif_rear_unit2MODIF_CASELESS(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_CASELESS" << endl);
	node1 = ++node; // vytvori terminal MODIF_CASELESS
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_CASELESS %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_MULTILINE
void modif_rear_unit2MODIF_MULTILINE(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl);
	node1 = ++node; // vytvori terminal MODIF_MULTILINE
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_MULTILINE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_DOTALL
void modif_rear_unit2MODIF_DOTALL(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl);
	node1 = ++node; // vytvori terminal MODIF_DOTALL
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_DOTALL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_EXTENDED
void modif_rear_unit2MODIF_EXTENDED(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl);
	node1 = ++node; // vytvori terminal MODIF_EXTENDED
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_EXTENDED %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_UNGREEDY
void modif_rear_unit2MODIF_UNGREEDY(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl);
	node1 = ++node; // vytvori terminal MODIF_UNGREEDY
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_UNGREEDY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_R
void modif_rear_unit2MODIF_R(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_R" << endl);
	node1 = ++node; // vytvori terminal MODIF_R
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_R %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_O
void modif_rear_unit2MODIF_O(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_O" << endl);
	node1 = ++node; // vytvori terminal MODIF_O
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_O %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_P
void modif_rear_unit2MODIF_P(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_P" << endl);
	node1 = ++node; // vytvori terminal MODIF_P
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_P %d\"]\n", node1, node1);
	nodes.push(node2);

}
// modif_rear_unit <<< MODIF_B
void modif_rear_unit2MODIF_B(){
	print_stack();
	DEBUG("modif_rear_unit <<< MODIF_B" << endl);
	node1 = ++node; // vytvori terminal MODIF_B
	node2 = ++node;  // vytvori nonterminal modif_rear_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"modif_rear_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_B %d\"]\n", node1, node1);
	nodes.push(node2);

}
// pcre_delim <<< SLASH
void pcre_delim2SLASH(){
	print_stack();
	DEBUG("pcre_delim <<< SLASH" << endl);
	node1 = ++node; // vytvori terminal SLASH
	node2 = ++node;  // vytvori nonterminal pcre_delim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pcre_delim %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SLASH %d\"]\n", node1, node1);
	nodes.push(node2);

}
// pattern <<< newlinespec inslash
void pattern2newlinespec_inslash(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("pattern <<< newlinespec inslash" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pattern
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pattern %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("pattern <<< newlinespec inslash" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pattern
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal newlinespec
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pattern %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"newlinespec %d\"]\n", node1, node1);
	nodes.push(node2);

}
// pattern <<< inslash
void pattern2inslash(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("pattern <<< inslash" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal pattern
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"pattern %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inslash <<< rv
void inslash2rv(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inslash <<< rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inslash <<< bol-rv
void inslash2bol_rv(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inslash <<< bol-rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inslash <<< bol-rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inslash <<< rv-eol
void inslash2rv_eol(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inslash <<< rv-eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal eol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"eol %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inslash <<< rv-eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inslash <<< bol-rv|eol
void inslash2bol_rv_eol(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inslash <<< bol-rv|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal eol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"eol %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inslash <<< bol-rv|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inslash <<< bol-rv|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inslash
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inslash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node1, node1);
	nodes.push(node2);

}
// rv <<< ext_exp
void rv2ext_exp(){
	print_stack();
	DEBUG("rv <<< ext_exp" << endl);
	node2 = ++node; // vytvori nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node1, node1);
	nodes.push(node2);

}
// rv <<< rv-or|rv
void rv2rv_or_rv(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("rv <<< rv-or|rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("rv <<< rv-or|rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal or
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"or %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("rv <<< rv-or|rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

}
// rv <<< or-rv
void rv2or_rv(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("rv <<< or-rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("rv <<< or-rv" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal or
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"or %d\"]\n", node1, node1);
	nodes.push(node2);

}
// rv <<< rv-or
void rv2rv_or(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("rv <<< rv-or" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal or
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"or %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("rv <<< rv-or" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_exp <<< exp
void ext_exp2exp(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("ext_exp <<< exp" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_exp <<< bol-exp
void ext_exp2bol_exp(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("ext_exp <<< bol-exp" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("ext_exp <<< bol-exp" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_exp <<< exp-eol
void ext_exp2exp_eol(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("ext_exp <<< exp-eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal eol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"eol %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("ext_exp <<< exp-eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_exp <<< bol-exp|eol
void ext_exp2bol_exp_eol(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("ext_exp <<< bol-exp|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal eol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"eol %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("ext_exp <<< bol-exp|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("ext_exp <<< bol-exp|eol" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node1, node1);
	nodes.push(node2);

}
// bol <<< BOL
void bol2BOL(){
	print_stack();
	DEBUG("bol <<< BOL" << endl);
	node1 = ++node; // vytvori terminal BOL
	node2 = ++node;  // vytvori nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"BOL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// eol <<< EOL
void eol2EOL(){
	print_stack();
	DEBUG("eol <<< EOL" << endl);
	node1 = ++node; // vytvori terminal EOL
	node2 = ++node;  // vytvori nonterminal eol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"eol %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"EOL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// exp <<< ext_unit
void exp2ext_unit(){
	print_stack();
	DEBUG("exp <<< ext_unit" << endl);
	node2 = ++node; // vytvori nonterminal exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ext_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// exp <<< ext_unit-exp
void exp2ext_unit_exp(){
	print_stack();
	DEBUG("exp <<< ext_unit-exp" << endl);
	node2 = ++node; // vytvori nonterminal exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("exp <<< ext_unit-exp" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal exp
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"exp %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ext_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_unit <<< unit
void ext_unit2unit(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("ext_unit <<< unit" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal ext_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// ext_unit <<< quantify_unit
void ext_unit2quantify_unit(){
	print_stack();
	DEBUG("ext_unit <<< quantify_unit" << endl);
	node2 = ++node; // vytvori nonterminal ext_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"ext_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"quantify_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantify_unit <<< unit quantify
void quantify_unit2unit_quantify(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("quantify_unit <<< unit quantify" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("quantify_unit <<< unit quantify" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantify <<< quantifier
void quantify2quantifier(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("quantify <<< quantifier" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantify <<< quantifier-possessive
void quantify2quantifier_possessive(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("quantify <<< quantifier-possessive" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal possessive
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"possessive %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("quantify <<< quantifier-possessive" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantify <<< quantifier-lazy
void quantify2quantifier_lazy(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("quantify <<< quantifier-lazy" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal lazy
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"lazy %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("quantify <<< quantifier-lazy" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantify
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantify %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantifier <<< ZEROMORE
void quantifier2ZEROMORE(){
	print_stack();
	DEBUG("quantifier <<< ZEROMORE" << endl);
	node1 = ++node; // vytvori terminal ZEROMORE
	node2 = ++node;  // vytvori nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ZEROMORE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantifier <<< ZEROONE
void quantifier2ZEROONE(){
	print_stack();
	DEBUG("quantifier <<< ZEROONE" << endl);
	node1 = ++node; // vytvori terminal ZEROONE
	node2 = ++node;  // vytvori nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ZEROONE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantifier <<< ONEMORE
void quantifier2ONEMORE(){
	print_stack();
	DEBUG("quantifier <<< ONEMORE" << endl);
	node1 = ++node; // vytvori terminal ONEMORE
	node2 = ++node;  // vytvori nonterminal quantifier
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ONEMORE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// quantifier <<< repeating
void quantifier2repeating(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("quantifier <<< repeating" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal quantifier
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal repeating
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"quantifier %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"repeating %d\"]\n", node1, node1);
	nodes.push(node2);

}
// possessive <<< ONEMORE
void possessive2ONEMORE(){
	print_stack();
	DEBUG("possessive <<< ONEMORE" << endl);
	node1 = ++node; // vytvori terminal ONEMORE
	node2 = ++node;  // vytvori nonterminal possessive
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"possessive %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ONEMORE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// lazy <<< ZEROONE
void lazy2ZEROONE(){
	print_stack();
	DEBUG("lazy <<< ZEROONE" << endl);
	node1 = ++node; // vytvori terminal ZEROONE
	node2 = ++node;  // vytvori nonterminal lazy
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"lazy %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ZEROONE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// or <<< OR
void or2OR(){
	print_stack();
	DEBUG("or <<< OR" << endl);
	node1 = ++node; // vytvori terminal OR
	node2 = ++node;  // vytvori nonterminal or
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"or %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// unit <<< element
void unit2element(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("unit <<< element" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node1, node1);
	nodes.push(node2);

}
// unit <<< capturing
void unit2capturing(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("unit <<< capturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node1, node1);
	nodes.push(node2);

}
// unit <<< option
void unit2option(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("unit <<< option" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node1, node1);
	nodes.push(node2);

}
// unit <<< chal
void unit2chal(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("unit <<< chal" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chal
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"chal %d\"]\n", node1, node1);
	nodes.push(node2);

}
// unit <<< class
void unit2class(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("unit <<< class" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option <<< optionStart option_set optionEnd
void option2optionStart_option_set_optionEnd(){
	print_stack();
	DEBUG("option <<< optionStart option_set optionEnd" << endl);
	node2 = ++node; // vytvori nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart option_set optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart option_set optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option <<< optionStart-option_unset_group|optionEnd
void option2optionStart_option_unset_group_optionEnd(){
	print_stack();
	DEBUG("option <<< optionStart-option_unset_group|optionEnd" << endl);
	node2 = ++node; // vytvori nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart-option_unset_group|optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset_group
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset_group %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart-option_unset_group|optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option <<< optionStart-option_set|option_unset_group|optionEnd
void option2optionStart_option_set_option_unset_group_optionEnd(){
	print_stack();
	DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl);
	node2 = ++node; // vytvori nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset_group
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset_group %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal optionStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"optionStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// optionStart <<< OPTION
void optionStart2OPTION(){
	print_stack();
	DEBUG("optionStart <<< OPTION" << endl);
	node1 = ++node; // vytvori terminal OPTION
	node2 = ++node;  // vytvori nonterminal optionStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"optionStart %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPTION %d\"]\n", node1, node1);
	nodes.push(node2);

}
// optionEnd <<< RBRA
void optionEnd2RBRA(){
	print_stack();
	DEBUG("optionEnd <<< RBRA" << endl);
	node1 = ++node; // vytvori terminal RBRA
	node2 = ++node;  // vytvori nonterminal optionEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"optionEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RBRA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_group <<< dash option_unset
void option_unset_group2dash_option_unset(){
	print_stack();
	DEBUG("option_unset_group <<< dash option_unset" << endl);
	node2 = ++node; // vytvori nonterminal option_unset_group
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_group %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option_unset_group <<< dash option_unset" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset_group
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal dash
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_group %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"dash %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set <<< option_set_unit
void option_set2option_set_unit(){
	print_stack();
	DEBUG("option_set <<< option_set_unit" << endl);
	node2 = ++node; // vytvori nonterminal option_set
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set <<< option_set_unit-option_set
void option_set2option_set_unit_option_set(){
	print_stack();
	DEBUG("option_set <<< option_set_unit-option_set" << endl);
	node2 = ++node; // vytvori nonterminal option_set
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option_set <<< option_set_unit-option_set" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_CASELESS
void option_set_unit2MODIF_CASELESS(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_CASELESS" << endl);
	node1 = ++node; // vytvori terminal MODIF_CASELESS
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_CASELESS %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_DOTALL
void option_set_unit2MODIF_DOTALL(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_DOTALL" << endl);
	node1 = ++node; // vytvori terminal MODIF_DOTALL
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_DOTALL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_EXTENDED
void option_set_unit2MODIF_EXTENDED(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_EXTENDED" << endl);
	node1 = ++node; // vytvori terminal MODIF_EXTENDED
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_EXTENDED %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_MULTILINE
void option_set_unit2MODIF_MULTILINE(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_MULTILINE" << endl);
	node1 = ++node; // vytvori terminal MODIF_MULTILINE
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_MULTILINE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_DUPNAMES
void option_set_unit2MODIF_DUPNAMES(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_DUPNAMES" << endl);
	node1 = ++node; // vytvori terminal MODIF_DUPNAMES
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_DUPNAMES %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_set_unit <<< MODIF_UNGREEDY
void option_set_unit2MODIF_UNGREEDY(){
	print_stack();
	DEBUG("option_set_unit <<< MODIF_UNGREEDY" << endl);
	node1 = ++node; // vytvori terminal MODIF_UNGREEDY
	node2 = ++node;  // vytvori nonterminal option_set_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_set_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_UNGREEDY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset <<< option_unset_unit
void option_unset2option_unset_unit(){
	print_stack();
	DEBUG("option_unset <<< option_unset_unit" << endl);
	node2 = ++node; // vytvori nonterminal option_unset
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset <<< option_unset_unit-option_unset
void option_unset2option_unset_unit_option_unset(){
	print_stack();
	DEBUG("option_unset <<< option_unset_unit-option_unset" << endl);
	node2 = ++node; // vytvori nonterminal option_unset
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("option_unset <<< option_unset_unit-option_unset" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_CASELESS
void option_unset_unit2MODIF_CASELESS(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_CASELESS" << endl);
	node1 = ++node; // vytvori terminal MODIF_CASELESS
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_CASELESS %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_DOTALL
void option_unset_unit2MODIF_DOTALL(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_DOTALL" << endl);
	node1 = ++node; // vytvori terminal MODIF_DOTALL
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_DOTALL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_EXTENDED
void option_unset_unit2MODIF_EXTENDED(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_EXTENDED" << endl);
	node1 = ++node; // vytvori terminal MODIF_EXTENDED
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_EXTENDED %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_MULTILINE
void option_unset_unit2MODIF_MULTILINE(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_MULTILINE" << endl);
	node1 = ++node; // vytvori terminal MODIF_MULTILINE
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_MULTILINE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_DUPNAMES
void option_unset_unit2MODIF_DUPNAMES(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_DUPNAMES" << endl);
	node1 = ++node; // vytvori terminal MODIF_DUPNAMES
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_DUPNAMES %d\"]\n", node1, node1);
	nodes.push(node2);

}
// option_unset_unit <<< MODIF_UNGREEDY
void option_unset_unit2MODIF_UNGREEDY(){
	print_stack();
	DEBUG("option_unset_unit <<< MODIF_UNGREEDY" << endl);
	node1 = ++node; // vytvori terminal MODIF_UNGREEDY
	node2 = ++node;  // vytvori nonterminal option_unset_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"option_unset_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"MODIF_UNGREEDY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< ASCII
void element2ASCII(char c){
	print_stack();
	DEBUG("element <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< ANY
void element2ANY(){
	print_stack();
	DEBUG("element <<< ANY" << endl);
	node1 = ++node; // vytvori terminal ANY
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ANY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< SPACE
void element2SPACE(){
	print_stack();
	DEBUG("element <<< SPACE" << endl);
	node1 = ++node; // vytvori terminal SPACE
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< hex
void element2hex(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("element <<< hex" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal hex
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"hex %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< TAB
void element2TAB(){
	print_stack();
	DEBUG("element <<< TAB" << endl);
	node1 = ++node; // vytvori terminal TAB
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"TAB %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< CR
void element2CR(){
	print_stack();
	DEBUG("element <<< CR" << endl);
	node1 = ++node; // vytvori terminal CR
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< LF
void element2LF(){
	print_stack();
	DEBUG("element <<< LF" << endl);
	node1 = ++node; // vytvori terminal LF
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"LF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< FF
void element2FF(){
	print_stack();
	DEBUG("element <<< FF" << endl);
	node1 = ++node; // vytvori terminal FF
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"FF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< BEL
void element2BEL(){
	print_stack();
	DEBUG("element <<< BEL" << endl);
	node1 = ++node; // vytvori terminal BEL
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"BEL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< ESC
void element2ESC(){
	print_stack();
	DEBUG("element <<< ESC" << endl);
	node1 = ++node; // vytvori terminal ESC
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ESC %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< CONTROLX
void element2CONTROLX(char c){
	print_stack();
	DEBUG("element <<< CONTROLX " << (char)c << endl);
	node1 = ++node; // vytvori terminal CONTROLX
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CONTROLX %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< BSR
void element2BSR(){
	print_stack();
	DEBUG("element <<< BSR" << endl);
	node1 = ++node; // vytvori terminal BSR
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"BSR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< RESET
void element2RESET(){
	print_stack();
	DEBUG("element <<< RESET" << endl);
	node1 = ++node; // vytvori terminal RESET
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RESET %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< assertions
void element2assertions(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("element <<< assertions" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< ONEBYTE
void element2ONEBYTE(){
	print_stack();
	DEBUG("element <<< ONEBYTE" << endl);
	node1 = ++node; // vytvori terminal ONEBYTE
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ONEBYTE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< OCTAL
void element2OCTAL(char c){
	print_stack();
	DEBUG("element <<< OCTAL " << (char)c << endl);
	node1 = ++node; // vytvori terminal OCTAL
	node2 = ++node;  // vytvori nonterminal element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OCTAL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< backreference
void element2backreference(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("element <<< backreference" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal backreference
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"backreference %d\"]\n", node1, node1);
	nodes.push(node2);

}
// element <<< subroutine
void element2subroutine(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("element <<< subroutine" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal subroutine
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"subroutine %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< WORDBOUNDARY
void assertions2WORDBOUNDARY(){
	print_stack();
	DEBUG("assertions <<< WORDBOUNDARY" << endl);
	node1 = ++node; // vytvori terminal WORDBOUNDARY
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"WORDBOUNDARY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< NWORDBOUNDARY
void assertions2NWORDBOUNDARY(){
	print_stack();
	DEBUG("assertions <<< NWORDBOUNDARY" << endl);
	node1 = ++node; // vytvori terminal NWORDBOUNDARY
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NWORDBOUNDARY %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< STARTSUBJECT
void assertions2STARTSUBJECT(){
	print_stack();
	DEBUG("assertions <<< STARTSUBJECT" << endl);
	node1 = ++node; // vytvori terminal STARTSUBJECT
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"STARTSUBJECT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< ENDSUBJECT
void assertions2ENDSUBJECT(){
	print_stack();
	DEBUG("assertions <<< ENDSUBJECT" << endl);
	node1 = ++node; // vytvori terminal ENDSUBJECT
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ENDSUBJECT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< OENDSUBJECT
void assertions2OENDSUBJECT(){
	print_stack();
	DEBUG("assertions <<< OENDSUBJECT" << endl);
	node1 = ++node; // vytvori terminal OENDSUBJECT
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OENDSUBJECT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// assertions <<< FIRSTPOSITION
void assertions2FIRSTPOSITION(){
	print_stack();
	DEBUG("assertions <<< FIRSTPOSITION" << endl);
	node1 = ++node; // vytvori terminal FIRSTPOSITION
	node2 = ++node;  // vytvori nonterminal assertions
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"assertions %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"FIRSTPOSITION %d\"]\n", node1, node1);
	nodes.push(node2);

}
// hex <<< HEX
void hex2HEX(char c){
	print_stack();
	DEBUG("hex <<< HEX " << hex << (char)c << endl);
	node1 = ++node; // vytvori terminal HEX
	node2 = ++node;  // vytvori nonterminal hex
	fprintf(graphFile, "%d -> %d [label=\"HEX %x\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"hex %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"HEX %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec <<< newlinespec_unit
void newlinespec2newlinespec_unit(){
	print_stack();
	DEBUG("newlinespec <<< newlinespec_unit" << endl);
	node2 = ++node; // vytvori nonterminal newlinespec
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec <<< newlinespec_unit-newlinespec
void newlinespec2newlinespec_unit_newlinespec(){
	print_stack();
	DEBUG("newlinespec <<< newlinespec_unit-newlinespec" << endl);
	node2 = ++node; // vytvori nonterminal newlinespec
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal newlinespec
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"newlinespec %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("newlinespec <<< newlinespec_unit-newlinespec" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal newlinespec
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec_unit <<< OPT_CR
void newlinespec_unit2OPT_CR(){
	print_stack();
	DEBUG("newlinespec_unit <<< OPT_CR" << endl);
	node1 = ++node; // vytvori terminal OPT_CR
	node2 = ++node;  // vytvori nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPT_CR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec_unit <<< OPT_LF
void newlinespec_unit2OPT_LF(){
	print_stack();
	DEBUG("newlinespec_unit <<< OPT_LF" << endl);
	node1 = ++node; // vytvori terminal OPT_LF
	node2 = ++node;  // vytvori nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPT_LF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec_unit <<< OPT_CRLF
void newlinespec_unit2OPT_CRLF(){
	print_stack();
	DEBUG("newlinespec_unit <<< OPT_CRLF" << endl);
	node1 = ++node; // vytvori terminal OPT_CRLF
	node2 = ++node;  // vytvori nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPT_CRLF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec_unit <<< OPT_ANYCRLF
void newlinespec_unit2OPT_ANYCRLF(){
	print_stack();
	DEBUG("newlinespec_unit <<< OPT_ANYCRLF" << endl);
	node1 = ++node; // vytvori terminal OPT_ANYCRLF
	node2 = ++node;  // vytvori nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPT_ANYCRLF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// newlinespec_unit <<< OPT_ANY_NEWLINE
void newlinespec_unit2OPT_ANY_NEWLINE(){
	print_stack();
	DEBUG("newlinespec_unit <<< OPT_ANY_NEWLINE" << endl);
	node1 = ++node; // vytvori terminal OPT_ANY_NEWLINE
	node2 = ++node;  // vytvori nonterminal newlinespec_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"newlinespec_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OPT_ANY_NEWLINE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< startCapturing rv endCapturing
void capturing2startCapturing_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< startCapturing rv endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< startCapturing rv endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< startCapturing rv endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal startCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"startCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing
void capturing2capturingNamed_capturingName_capturingNameEnd_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNameEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNameEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingName
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingName %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNamed
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNamed %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingNon-rv|endCapturing
void capturing2capturingNon_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingNon-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNon-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNon-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNon
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNon %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingNonreset-rv|endCapturing
void capturing2capturingNonreset_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingNonreset-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNonreset-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNonreset-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNonreset
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNonreset %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingAtomic-rv|endCapturing
void capturing2capturingAtomic_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingAtomic-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingAtomic-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingAtomic-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingAtomic
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingAtomic %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingComment-rv|endCapturing
void capturing2capturingComment_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingComment-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingComment-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingComment-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingComment
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingComment %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingPosahead-rv|endCapturing
void capturing2capturingPosahead_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingPosahead-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingPosahead-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingPosahead-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingPosahead
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingPosahead %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingNegahead-rv|endCapturing
void capturing2capturingNegahead_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingNegahead-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNegahead-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNegahead-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNegahead
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNegahead %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingPosbehind-rv|endCapturing
void capturing2capturingPosbehind_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingPosbehind-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingPosbehind-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingPosbehind-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingPosbehind
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingPosbehind %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturing <<< capturingNegbehind-rv|endCapturing
void capturing2capturingNegbehind_rv_endCapturing(){
	print_stack();
	DEBUG("capturing <<< capturingNegbehind-rv|endCapturing" << endl);
	node2 = ++node; // vytvori nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNegbehind-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rv
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rv %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturing <<< capturingNegbehind-rv|endCapturing" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturing
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNegbehind
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNegbehind %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNamed <<< CAPTURING_NAMED
void capturingNamed2CAPTURING_NAMED(){
	print_stack();
	DEBUG("capturingNamed <<< CAPTURING_NAMED" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NAMED
	node2 = ++node;  // vytvori nonterminal capturingNamed
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNamed %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NAMED %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingName <<< capturingNameAdd
void capturingName2capturingNameAdd(){
	print_stack();
	DEBUG("capturingName <<< capturingNameAdd" << endl);
	node2 = ++node; // vytvori nonterminal capturingName
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNameAdd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingName %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNameAdd %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingName <<< capturingNameAdd-capturingName
void capturingName2capturingNameAdd_capturingName(){
	print_stack();
	DEBUG("capturingName <<< capturingNameAdd-capturingName" << endl);
	node2 = ++node; // vytvori nonterminal capturingName
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingName
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingName %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingName %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("capturingName <<< capturingNameAdd-capturingName" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingName
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal capturingNameAdd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingName %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"capturingNameAdd %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNameAdd <<< ASCII
void capturingNameAdd2ASCII(char c){
	print_stack();
	DEBUG("capturingNameAdd <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal capturingNameAdd
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"capturingNameAdd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNon <<< CAPTURING_NON
void capturingNon2CAPTURING_NON(){
	print_stack();
	DEBUG("capturingNon <<< CAPTURING_NON" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NON
	node2 = ++node;  // vytvori nonterminal capturingNon
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNon %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NON %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNonreset <<< CAPTURING_NONRESET
void capturingNonreset2CAPTURING_NONRESET(){
	print_stack();
	DEBUG("capturingNonreset <<< CAPTURING_NONRESET" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NONRESET
	node2 = ++node;  // vytvori nonterminal capturingNonreset
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNonreset %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NONRESET %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingAtomic <<< CAPTURING_ATOMIC
void capturingAtomic2CAPTURING_ATOMIC(){
	print_stack();
	DEBUG("capturingAtomic <<< CAPTURING_ATOMIC" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_ATOMIC
	node2 = ++node;  // vytvori nonterminal capturingAtomic
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingAtomic %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_ATOMIC %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingComment <<< CAPTURING_COMMENT
void capturingComment2CAPTURING_COMMENT(){
	print_stack();
	DEBUG("capturingComment <<< CAPTURING_COMMENT" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_COMMENT
	node2 = ++node;  // vytvori nonterminal capturingComment
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingComment %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_COMMENT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingPosahead <<< CAPTURING_POSAHEAD
void capturingPosahead2CAPTURING_POSAHEAD(){
	print_stack();
	DEBUG("capturingPosahead <<< CAPTURING_POSAHEAD" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_POSAHEAD
	node2 = ++node;  // vytvori nonterminal capturingPosahead
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingPosahead %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_POSAHEAD %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNegahead <<< CAPTURING_NEGAHEAD
void capturingNegahead2CAPTURING_NEGAHEAD(){
	print_stack();
	DEBUG("capturingNegahead <<< CAPTURING_NEGAHEAD" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NEGAHEAD
	node2 = ++node;  // vytvori nonterminal capturingNegahead
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNegahead %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NEGAHEAD %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingPosbehind <<< CAPTURING_POSBEHIND
void capturingPosbehind2CAPTURING_POSBEHIND(){
	print_stack();
	DEBUG("capturingPosbehind <<< CAPTURING_POSBEHIND" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_POSBEHIND
	node2 = ++node;  // vytvori nonterminal capturingPosbehind
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingPosbehind %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_POSBEHIND %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNegbehind <<< CAPTURING_NEGBEHIND
void capturingNegbehind2CAPTURING_NEGBEHIND(){
	print_stack();
	DEBUG("capturingNegbehind <<< CAPTURING_NEGBEHIND" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NEGBEHIND
	node2 = ++node;  // vytvori nonterminal capturingNegbehind
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNegbehind %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NEGBEHIND %d\"]\n", node1, node1);
	nodes.push(node2);

}
// capturingNameEnd <<< CAPTURING_NAMED_END
void capturingNameEnd2CAPTURING_NAMED_END(){
	print_stack();
	DEBUG("capturingNameEnd <<< CAPTURING_NAMED_END" << endl);
	node1 = ++node; // vytvori terminal CAPTURING_NAMED_END
	node2 = ++node;  // vytvori nonterminal capturingNameEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"capturingNameEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CAPTURING_NAMED_END %d\"]\n", node1, node1);
	nodes.push(node2);

}
// startCapturing <<< LPAR
void startCapturing2LPAR(){
	print_stack();
	DEBUG("startCapturing <<< LPAR" << endl);
	node1 = ++node; // vytvori terminal LPAR
	node2 = ++node;  // vytvori nonterminal startCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"startCapturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"LPAR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// endCapturing <<< RPAR
void endCapturing2RPAR(){
	print_stack();
	DEBUG("endCapturing <<< RPAR" << endl);
	node1 = ++node; // vytvori terminal RPAR
	node2 = ++node;  // vytvori nonterminal endCapturing
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"endCapturing %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RPAR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// repeating <<< startRepeating interval endRepeating
void repeating2startRepeating_interval_endRepeating(){
	print_stack();
	DEBUG("repeating <<< startRepeating interval endRepeating" << endl);
	node2 = ++node; // vytvori nonterminal repeating
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal endRepeating
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"repeating %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"endRepeating %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("repeating <<< startRepeating interval endRepeating" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal repeating
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal interval
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"repeating %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("repeating <<< startRepeating interval endRepeating" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal repeating
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal startRepeating
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"repeating %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"startRepeating %d\"]\n", node1, node1);
	nodes.push(node2);

}
// startRepeating <<< LBRA
void startRepeating2LBRA(){
	print_stack();
	DEBUG("startRepeating <<< LBRA" << endl);
	node1 = ++node; // vytvori terminal LBRA
	node2 = ++node;  // vytvori nonterminal startRepeating
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"startRepeating %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"LBRA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// endRepeating <<< RBRA
void endRepeating2RBRA(){
	print_stack();
	DEBUG("endRepeating <<< RBRA" << endl);
	node1 = ++node; // vytvori terminal RBRA
	node2 = ++node;  // vytvori nonterminal endRepeating
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"endRepeating %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RBRA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// interval <<< minimum intervalDelim maximum
void interval2minimum_intervalDelim_maximum(){
	print_stack();
	DEBUG("interval <<< minimum intervalDelim maximum" << endl);
	node2 = ++node; // vytvori nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal maximum
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"maximum %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("interval <<< minimum intervalDelim maximum" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal intervalDelim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"intervalDelim %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("interval <<< minimum intervalDelim maximum" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal minimum
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"minimum %d\"]\n", node1, node1);
	nodes.push(node2);

}
// interval <<< minimum-intervalDelim
void interval2minimum_intervalDelim(){
	print_stack();
	DEBUG("interval <<< minimum-intervalDelim" << endl);
	node2 = ++node; // vytvori nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal intervalDelim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"intervalDelim %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("interval <<< minimum-intervalDelim" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal minimum
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"minimum %d\"]\n", node1, node1);
	nodes.push(node2);

}
// interval <<< maximum
void interval2maximum(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("interval <<< maximum" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal interval
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal maximum
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"interval %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"maximum %d\"]\n", node1, node1);
	nodes.push(node2);

}
// minimum <<< INT
void minimum2INT(int i){
	print_stack();
	DEBUG("minimum <<< INT " << (int)i << endl);
	node1 = ++node; // vytvori terminal INT
	node2 = ++node;  // vytvori nonterminal minimum
	fprintf(graphFile, "%d -> %d [label=\"INT %i\"]\n", node2, node1, i);
	fprintf(graphFile, "%d [label=\"minimum %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"INT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// maximum <<< INT
void maximum2INT(int i){
	print_stack();
	DEBUG("maximum <<< INT " << (int)i << endl);
	node1 = ++node; // vytvori terminal INT
	node2 = ++node;  // vytvori nonterminal maximum
	fprintf(graphFile, "%d -> %d [label=\"INT %i\"]\n", node2, node1, i);
	fprintf(graphFile, "%d [label=\"maximum %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"INT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// intervalDelim <<< COMMA
void intervalDelim2COMMA(){
	print_stack();
	DEBUG("intervalDelim <<< COMMA" << endl);
	node1 = ++node; // vytvori terminal COMMA
	node2 = ++node;  // vytvori nonterminal intervalDelim
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"intervalDelim %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"COMMA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// class <<< classStart inclass classEnd
void class2classStart_inclass_classEnd(){
	print_stack();
	DEBUG("class <<< classStart inclass classEnd" << endl);
	node2 = ++node; // vytvori nonterminal class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal classEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"classEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("class <<< classStart inclass classEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("class <<< classStart inclass classEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal classStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"classStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// class <<< slashcharclass
void class2slashcharclass(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("class <<< slashcharclass" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node1, node1);
	nodes.push(node2);

}
// class <<< posix_class
void class2posix_class(){
	print_stack();
	DEBUG("class <<< posix_class" << endl);
	node2 = ++node; // vytvori nonterminal class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node1, node1);
	nodes.push(node2);

}
// classStart <<< LBOX
void classStart2LBOX(){
	print_stack();
	DEBUG("classStart <<< LBOX" << endl);
	node1 = ++node; // vytvori terminal LBOX
	node2 = ++node;  // vytvori nonterminal classStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"classStart %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"LBOX %d\"]\n", node1, node1);
	nodes.push(node2);

}
// classEnd <<< RBOX
void classEnd2RBOX(){
	print_stack();
	DEBUG("classEnd <<< RBOX" << endl);
	node1 = ++node; // vytvori terminal RBOX
	node2 = ++node;  // vytvori nonterminal classEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"classEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RBOX %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< DECDIGIT
void slashcharclass2DECDIGIT(){
	print_stack();
	DEBUG("slashcharclass <<< DECDIGIT" << endl);
	node1 = ++node; // vytvori terminal DECDIGIT
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"DECDIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< NDECDIGIT
void slashcharclass2NDECDIGIT(){
	print_stack();
	DEBUG("slashcharclass <<< NDECDIGIT" << endl);
	node1 = ++node; // vytvori terminal NDECDIGIT
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NDECDIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< HWHITESPACE
void slashcharclass2HWHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< HWHITESPACE" << endl);
	node1 = ++node; // vytvori terminal HWHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"HWHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< NHWHITESPACE
void slashcharclass2NHWHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< NHWHITESPACE" << endl);
	node1 = ++node; // vytvori terminal NHWHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NHWHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< WHITESPACE
void slashcharclass2WHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< WHITESPACE" << endl);
	node1 = ++node; // vytvori terminal WHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"WHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< NWHITESPACE
void slashcharclass2NWHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< NWHITESPACE" << endl);
	node1 = ++node; // vytvori terminal NWHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NWHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< VWHITESPACE
void slashcharclass2VWHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< VWHITESPACE" << endl);
	node1 = ++node; // vytvori terminal VWHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"VWHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< NVWHITESPACE
void slashcharclass2NVWHITESPACE(){
	print_stack();
	DEBUG("slashcharclass <<< NVWHITESPACE" << endl);
	node1 = ++node; // vytvori terminal NVWHITESPACE
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NVWHITESPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< WORDCHAR
void slashcharclass2WORDCHAR(){
	print_stack();
	DEBUG("slashcharclass <<< WORDCHAR" << endl);
	node1 = ++node; // vytvori terminal WORDCHAR
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"WORDCHAR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// slashcharclass <<< NWORDCHAR
void slashcharclass2NWORDCHAR(){
	print_stack();
	DEBUG("slashcharclass <<< NWORDCHAR" << endl);
	node1 = ++node; // vytvori terminal NWORDCHAR
	node2 = ++node;  // vytvori nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NWORDCHAR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass <<< inclass_ext_unit
void inclass2inclass_ext_unit(){
	print_stack();
	DEBUG("inclass <<< inclass_ext_unit" << endl);
	node2 = ++node; // vytvori nonterminal inclass
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_ext_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass <<< bol-inclass_ext_unit
void inclass2bol_inclass_ext_unit(){
	print_stack();
	DEBUG("inclass <<< bol-inclass_ext_unit" << endl);
	node2 = ++node; // vytvori nonterminal inclass
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_ext_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inclass <<< bol-inclass_ext_unit" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal bol
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"bol %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_ext_unit <<< inclass_unit
void inclass_ext_unit2inclass_unit(){
	print_stack();
	DEBUG("inclass_ext_unit <<< inclass_unit" << endl);
	node2 = ++node; // vytvori nonterminal inclass_ext_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_ext_unit <<< inclass_unit-inclass_ext_unit
void inclass_ext_unit2inclass_unit_inclass_ext_unit(){
	print_stack();
	DEBUG("inclass_ext_unit <<< inclass_unit-inclass_ext_unit" << endl);
	node2 = ++node; // vytvori nonterminal inclass_ext_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_ext_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inclass_ext_unit <<< inclass_unit-inclass_ext_unit" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_ext_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_unit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_ext_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_unit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_unit <<< inclass_element
void inclass_unit2inclass_element(){
	print_stack();
	DEBUG("inclass_unit <<< inclass_element" << endl);
	node2 = ++node; // vytvori nonterminal inclass_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_unit <<< rangechars
void inclass_unit2rangechars(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inclass_unit <<< rangechars" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal rangechars
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"rangechars %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_unit <<< chal
void inclass_unit2chal(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inclass_unit <<< chal" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_unit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chal
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_unit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"chal %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< ASCII
void inclass_element2ASCII(char c){
	print_stack();
	DEBUG("inclass_element <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< posix_class
void inclass_element2posix_class(){
	print_stack();
	DEBUG("inclass_element <<< posix_class" << endl);
	node2 = ++node; // vytvori nonterminal inclass_element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< slashcharclass
void inclass_element2slashcharclass(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inclass_element <<< slashcharclass" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal slashcharclass
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"slashcharclass %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< hex
void inclass_element2hex(){
	nodes.push(++node); // vytvori prepisovany nonterminal

	print_stack();
	DEBUG("inclass_element <<< hex" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inclass_element
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal hex
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"hex %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< TAB
void inclass_element2TAB(){
	print_stack();
	DEBUG("inclass_element <<< TAB" << endl);
	node1 = ++node; // vytvori terminal TAB
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"TAB %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< CR
void inclass_element2CR(){
	print_stack();
	DEBUG("inclass_element <<< CR" << endl);
	node1 = ++node; // vytvori terminal CR
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CR %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< LF
void inclass_element2LF(){
	print_stack();
	DEBUG("inclass_element <<< LF" << endl);
	node1 = ++node; // vytvori terminal LF
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"LF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< FF
void inclass_element2FF(){
	print_stack();
	DEBUG("inclass_element <<< FF" << endl);
	node1 = ++node; // vytvori terminal FF
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"FF %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< BEL
void inclass_element2BEL(){
	print_stack();
	DEBUG("inclass_element <<< BEL" << endl);
	node1 = ++node; // vytvori terminal BEL
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"BEL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< ESC
void inclass_element2ESC(){
	print_stack();
	DEBUG("inclass_element <<< ESC" << endl);
	node1 = ++node; // vytvori terminal ESC
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ESC %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< CONTROLX
void inclass_element2CONTROLX(char c){
	print_stack();
	DEBUG("inclass_element <<< CONTROLX " << (char)c << endl);
	node1 = ++node; // vytvori terminal CONTROLX
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CONTROLX %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< RESET
void inclass_element2RESET(){
	print_stack();
	DEBUG("inclass_element <<< RESET" << endl);
	node1 = ++node; // vytvori terminal RESET
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"RESET %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< OCTAL
void inclass_element2OCTAL(char c){
	print_stack();
	DEBUG("inclass_element <<< OCTAL " << (char)c << endl);
	node1 = ++node; // vytvori terminal OCTAL
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"OCTAL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inclass_element <<< DASH
void inclass_element2DASH(){
	print_stack();
	DEBUG("inclass_element <<< DASH" << endl);
	node1 = ++node; // vytvori terminal DASH
	node2 = ++node;  // vytvori nonterminal inclass_element
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inclass_element %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"DASH %d\"]\n", node1, node1);
	nodes.push(node2);

}
// rangechars <<< INT
void rangechars2INT(int i){
	print_stack();
	DEBUG("rangechars <<< INT " << (int)i << endl);
	node1 = ++node; // vytvori terminal INT
	node2 = ++node;  // vytvori nonterminal rangechars
	fprintf(graphFile, "%d -> %d [label=\"INT %i\"]\n", node2, node1, i);
	fprintf(graphFile, "%d [label=\"rangechars %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"INT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// dash <<< DASH
void dash2DASH(){
	print_stack();
	DEBUG("dash <<< DASH" << endl);
	node1 = ++node; // vytvori terminal DASH
	node2 = ++node;  // vytvori nonterminal dash
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"dash %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"DASH %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_ALNUM
void posix_class2P_ALNUM(){
	print_stack();
	DEBUG("posix_class <<< P_ALNUM" << endl);
	node1 = ++node; // vytvori terminal P_ALNUM
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_ALNUM %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_ALPHA
void posix_class2P_ALPHA(){
	print_stack();
	DEBUG("posix_class <<< P_ALPHA" << endl);
	node1 = ++node; // vytvori terminal P_ALPHA
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_ALPHA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_ASCII
void posix_class2P_ASCII(){
	print_stack();
	DEBUG("posix_class <<< P_ASCII" << endl);
	node1 = ++node; // vytvori terminal P_ASCII
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_BLANK
void posix_class2P_BLANK(){
	print_stack();
	DEBUG("posix_class <<< P_BLANK" << endl);
	node1 = ++node; // vytvori terminal P_BLANK
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_BLANK %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_CNTRL
void posix_class2P_CNTRL(){
	print_stack();
	DEBUG("posix_class <<< P_CNTRL" << endl);
	node1 = ++node; // vytvori terminal P_CNTRL
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_CNTRL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_DIGIT
void posix_class2P_DIGIT(){
	print_stack();
	DEBUG("posix_class <<< P_DIGIT" << endl);
	node1 = ++node; // vytvori terminal P_DIGIT
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_DIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_GRAPH
void posix_class2P_GRAPH(){
	print_stack();
	DEBUG("posix_class <<< P_GRAPH" << endl);
	node1 = ++node; // vytvori terminal P_GRAPH
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_GRAPH %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_LOWER
void posix_class2P_LOWER(){
	print_stack();
	DEBUG("posix_class <<< P_LOWER" << endl);
	node1 = ++node; // vytvori terminal P_LOWER
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_LOWER %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_PRINT
void posix_class2P_PRINT(){
	print_stack();
	DEBUG("posix_class <<< P_PRINT" << endl);
	node1 = ++node; // vytvori terminal P_PRINT
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_PRINT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_PUNCT
void posix_class2P_PUNCT(){
	print_stack();
	DEBUG("posix_class <<< P_PUNCT" << endl);
	node1 = ++node; // vytvori terminal P_PUNCT
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_PUNCT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_SPACE
void posix_class2P_SPACE(){
	print_stack();
	DEBUG("posix_class <<< P_SPACE" << endl);
	node1 = ++node; // vytvori terminal P_SPACE
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_SPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_UPPER
void posix_class2P_UPPER(){
	print_stack();
	DEBUG("posix_class <<< P_UPPER" << endl);
	node1 = ++node; // vytvori terminal P_UPPER
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_UPPER %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_WORD
void posix_class2P_WORD(){
	print_stack();
	DEBUG("posix_class <<< P_WORD" << endl);
	node1 = ++node; // vytvori terminal P_WORD
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_WORD %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< P_XDIGIT
void posix_class2P_XDIGIT(){
	print_stack();
	DEBUG("posix_class <<< P_XDIGIT" << endl);
	node1 = ++node; // vytvori terminal P_XDIGIT
	node2 = ++node;  // vytvori nonterminal posix_class
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"P_XDIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class <<< posix_class_neg
void posix_class2posix_class_neg(){
	print_stack();
	DEBUG("posix_class <<< posix_class_neg" << endl);
	node2 = ++node; // vytvori nonterminal posix_class
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_ALNUM
void posix_class_neg2NP_ALNUM(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_ALNUM" << endl);
	node1 = ++node; // vytvori terminal NP_ALNUM
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_ALNUM %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_ALPHA
void posix_class_neg2NP_ALPHA(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_ALPHA" << endl);
	node1 = ++node; // vytvori terminal NP_ALPHA
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_ALPHA %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_ASCII
void posix_class_neg2NP_ASCII(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_ASCII" << endl);
	node1 = ++node; // vytvori terminal NP_ASCII
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_BLANK
void posix_class_neg2NP_BLANK(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_BLANK" << endl);
	node1 = ++node; // vytvori terminal NP_BLANK
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_BLANK %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_CNTRL
void posix_class_neg2NP_CNTRL(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_CNTRL" << endl);
	node1 = ++node; // vytvori terminal NP_CNTRL
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_CNTRL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_DIGIT
void posix_class_neg2NP_DIGIT(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_DIGIT" << endl);
	node1 = ++node; // vytvori terminal NP_DIGIT
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_DIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_GRAPH
void posix_class_neg2NP_GRAPH(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_GRAPH" << endl);
	node1 = ++node; // vytvori terminal NP_GRAPH
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_GRAPH %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_LOWER
void posix_class_neg2NP_LOWER(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_LOWER" << endl);
	node1 = ++node; // vytvori terminal NP_LOWER
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_LOWER %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_PRINT
void posix_class_neg2NP_PRINT(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_PRINT" << endl);
	node1 = ++node; // vytvori terminal NP_PRINT
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_PRINT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_PUNCT
void posix_class_neg2NP_PUNCT(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_PUNCT" << endl);
	node1 = ++node; // vytvori terminal NP_PUNCT
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_PUNCT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_SPACE
void posix_class_neg2NP_SPACE(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_SPACE" << endl);
	node1 = ++node; // vytvori terminal NP_SPACE
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_SPACE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_UPPER
void posix_class_neg2NP_UPPER(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_UPPER" << endl);
	node1 = ++node; // vytvori terminal NP_UPPER
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_UPPER %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_WORD
void posix_class_neg2NP_WORD(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_WORD" << endl);
	node1 = ++node; // vytvori terminal NP_WORD
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_WORD %d\"]\n", node1, node1);
	nodes.push(node2);

}
// posix_class_neg <<< NP_XDIGIT
void posix_class_neg2NP_XDIGIT(){
	print_stack();
	DEBUG("posix_class_neg <<< NP_XDIGIT" << endl);
	node1 = ++node; // vytvori terminal NP_XDIGIT
	node2 = ++node;  // vytvori nonterminal posix_class_neg
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"posix_class_neg %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NP_XDIGIT %d\"]\n", node1, node1);
	nodes.push(node2);

}
// chal <<< chalStart inchal chalEnd
void chal2chalStart_inchal_chalEnd(){
	print_stack();
	DEBUG("chal <<< chalStart inchal chalEnd" << endl);
	node2 = ++node; // vytvori nonterminal chal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chalEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"chal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"chalEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("chal <<< chalStart inchal chalEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchal
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"chal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inchal %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("chal <<< chalStart inchal chalEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal chalStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"chal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"chalStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// chalStart <<< CHALSTART
void chalStart2CHALSTART(){
	print_stack();
	DEBUG("chalStart <<< CHALSTART" << endl);
	node1 = ++node; // vytvori terminal CHALSTART
	node2 = ++node;  // vytvori nonterminal chalStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"chalStart %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CHALSTART %d\"]\n", node1, node1);
	nodes.push(node2);

}
// chalEnd <<< CHALEND
void chalEnd2CHALEND(){
	print_stack();
	DEBUG("chalEnd <<< CHALEND" << endl);
	node1 = ++node; // vytvori terminal CHALEND
	node2 = ++node;  // vytvori nonterminal chalEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"chalEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"CHALEND %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inchal <<< inchalExtUnit
void inchal2inchalExtUnit(){
	print_stack();
	DEBUG("inchal <<< inchalExtUnit" << endl);
	node2 = ++node; // vytvori nonterminal inchal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchalExtUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inchal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inchalExtUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inchal <<< inchalExtUnit-inchal
void inchal2inchalExtUnit_inchal(){
	print_stack();
	DEBUG("inchal <<< inchalExtUnit-inchal" << endl);
	node2 = ++node; // vytvori nonterminal inchal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchal
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inchal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inchal %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inchal <<< inchalExtUnit-inchal" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchal
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchalExtUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inchal %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inchalExtUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inchalExtUnit <<< inchalUnit
void inchalExtUnit2inchalUnit(){
	print_stack();
	DEBUG("inchalExtUnit <<< inchalUnit" << endl);
	node2 = ++node; // vytvori nonterminal inchalExtUnit
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inchalUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inchalExtUnit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inchalUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inchalUnit <<< ASCII
void inchalUnit2ASCII(char c){
	print_stack();
	DEBUG("inchalUnit <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal inchalUnit
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"inchalUnit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// backreference <<< BACKREFERENCE
void backreference2BACKREFERENCE(){
	print_stack();
	DEBUG("backreference <<< BACKREFERENCE" << endl);
	node1 = ++node; // vytvori terminal BACKREFERENCE
	node2 = ++node;  // vytvori nonterminal backreference
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"backreference %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"BACKREFERENCE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// backreference <<< named_back_reference
void backreference2named_back_reference(){
	print_stack();
	DEBUG("backreference <<< named_back_reference" << endl);
	node2 = ++node; // vytvori nonterminal backreference
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_back_reference
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"backreference %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"named_back_reference %d\"]\n", node1, node1);
	nodes.push(node2);

}
// named_back_reference <<< nbrStart inNbr nbrEnd
void named_back_reference2nbrStart_inNbr_nbrEnd(){
	print_stack();
	DEBUG("named_back_reference <<< nbrStart inNbr nbrEnd" << endl);
	node2 = ++node; // vytvori nonterminal named_back_reference
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal nbrEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_back_reference %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"nbrEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("named_back_reference <<< nbrStart inNbr nbrEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_back_reference
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNbr
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_back_reference %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNbr %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("named_back_reference <<< nbrStart inNbr nbrEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_back_reference
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal nbrStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_back_reference %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"nbrStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// nbrStart <<< NAMED_BACKREFERENCE
void nbrStart2NAMED_BACKREFERENCE(){
	print_stack();
	DEBUG("nbrStart <<< NAMED_BACKREFERENCE" << endl);
	node1 = ++node; // vytvori terminal NAMED_BACKREFERENCE
	node2 = ++node;  // vytvori nonterminal nbrStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"nbrStart %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NAMED_BACKREFERENCE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// nbrEnd <<< NAMED_BACKREFERENCE_END
void nbrEnd2NAMED_BACKREFERENCE_END(){
	print_stack();
	DEBUG("nbrEnd <<< NAMED_BACKREFERENCE_END" << endl);
	node1 = ++node; // vytvori terminal NAMED_BACKREFERENCE_END
	node2 = ++node;  // vytvori nonterminal nbrEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"nbrEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"NAMED_BACKREFERENCE_END %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNbr <<< inNbrUnit
void inNbr2inNbrUnit(){
	print_stack();
	DEBUG("inNbr <<< inNbrUnit" << endl);
	node2 = ++node; // vytvori nonterminal inNbr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNbrUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNbr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNbrUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNbr <<< inNbrUnit-inNbr
void inNbr2inNbrUnit_inNbr(){
	print_stack();
	DEBUG("inNbr <<< inNbrUnit-inNbr" << endl);
	node2 = ++node; // vytvori nonterminal inNbr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNbr
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNbr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNbr %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inNbr <<< inNbrUnit-inNbr" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNbr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNbrUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNbr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNbrUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNbrUnit <<< ASCII
void inNbrUnit2ASCII(char c){
	print_stack();
	DEBUG("inNbrUnit <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal inNbrUnit
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"inNbrUnit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
// subroutine <<< SUBROUTINE_ALL
void subroutine2SUBROUTINE_ALL(){
	print_stack();
	DEBUG("subroutine <<< SUBROUTINE_ALL" << endl);
	node1 = ++node; // vytvori terminal SUBROUTINE_ALL
	node2 = ++node;  // vytvori nonterminal subroutine
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SUBROUTINE_ALL %d\"]\n", node1, node1);
	nodes.push(node2);

}
// subroutine <<< SUBROUTINE_ABSOLUTE
void subroutine2SUBROUTINE_ABSOLUTE(){
	print_stack();
	DEBUG("subroutine <<< SUBROUTINE_ABSOLUTE" << endl);
	node1 = ++node; // vytvori terminal SUBROUTINE_ABSOLUTE
	node2 = ++node;  // vytvori nonterminal subroutine
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SUBROUTINE_ABSOLUTE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// subroutine <<< SUBROUTINE_RELATIVE
void subroutine2SUBROUTINE_RELATIVE(){
	print_stack();
	DEBUG("subroutine <<< SUBROUTINE_RELATIVE" << endl);
	node1 = ++node; // vytvori terminal SUBROUTINE_RELATIVE
	node2 = ++node;  // vytvori nonterminal subroutine
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SUBROUTINE_RELATIVE %d\"]\n", node1, node1);
	nodes.push(node2);

}
// subroutine <<< named_subroutine
void subroutine2named_subroutine(){
	print_stack();
	DEBUG("subroutine <<< named_subroutine" << endl);
	node2 = ++node; // vytvori nonterminal subroutine
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_subroutine
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"named_subroutine %d\"]\n", node1, node1);
	nodes.push(node2);

}
// named_subroutine <<< nsrStart inNsr nsrEnd
void named_subroutine2nsrStart_inNsr_nsrEnd(){
	print_stack();
	DEBUG("named_subroutine <<< nsrStart inNsr nsrEnd" << endl);
	node2 = ++node; // vytvori nonterminal named_subroutine
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal nsrEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"nsrEnd %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("named_subroutine <<< nsrStart inNsr nsrEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_subroutine
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNsr
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNsr %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("named_subroutine <<< nsrStart inNsr nsrEnd" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal named_subroutine
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal nsrStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"named_subroutine %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"nsrStart %d\"]\n", node1, node1);
	nodes.push(node2);

}
// nsrStart <<< SUBROUTINE_NAME
void nsrStart2SUBROUTINE_NAME(){
	print_stack();
	DEBUG("nsrStart <<< SUBROUTINE_NAME" << endl);
	node1 = ++node; // vytvori terminal SUBROUTINE_NAME
	node2 = ++node;  // vytvori nonterminal nsrStart
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"nsrStart %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SUBROUTINE_NAME %d\"]\n", node1, node1);
	nodes.push(node2);

}
// nsrEnd <<< SUBROUTINE_NAME_END
void nsrEnd2SUBROUTINE_NAME_END(){
	print_stack();
	DEBUG("nsrEnd <<< SUBROUTINE_NAME_END" << endl);
	node1 = ++node; // vytvori terminal SUBROUTINE_NAME_END
	node2 = ++node;  // vytvori nonterminal nsrEnd
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"nsrEnd %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"SUBROUTINE_NAME_END %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNsr <<< inNsrUnit
void inNsr2inNsrUnit(){
	print_stack();
	DEBUG("inNsr <<< inNsrUnit" << endl);
	node2 = ++node; // vytvori nonterminal inNsr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNsrUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNsr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNsrUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNsr <<< inNsrUnit-inNsr
void inNsr2inNsrUnit_inNsr(){
	print_stack();
	DEBUG("inNsr <<< inNsrUnit-inNsr" << endl);
	node2 = ++node; // vytvori nonterminal inNsr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNsr
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNsr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNsr %d\"]\n", node1, node1);
	nodes.push(node2);

	print_stack();
	DEBUG("inNsr <<< inNsrUnit-inNsr" << endl);
	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNsr
	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal inNsrUnit
	fprintf(graphFile, "%d -> %d\n", node2, node1);
	fprintf(graphFile, "%d [label=\"inNsr %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"inNsrUnit %d\"]\n", node1, node1);
	nodes.push(node2);

}
// inNsrUnit <<< ASCII
void inNsrUnit2ASCII(char c){
	print_stack();
	DEBUG("inNsrUnit <<< ASCII " << (char)c << endl);
	node1 = ++node; // vytvori terminal ASCII
	node2 = ++node;  // vytvori nonterminal inNsrUnit
	fprintf(graphFile, "%d -> %d [label=\"ASCII %c\"]\n", node2, node1, c);
	fprintf(graphFile, "%d [label=\"inNsrUnit %d\"]\n", node2, node2);
	fprintf(graphFile, "%d [label=\"ASCII %d\"]\n", node1, node1);
	nodes.push(node2);

}
