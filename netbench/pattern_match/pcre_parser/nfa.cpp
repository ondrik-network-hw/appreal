/**
 * Aplikace parseru PCRE - tvorba NFA
 *
 * @date 2011-04-27
 * @author Milan Pála (xpalam00@stud.fit.vutbr.cz)
 */

#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string.h>
#include <sys/time.h>

#define NFA_FAIL 3

#include "interface.h"
#include "symbols.hpp"
#include "nodes.hpp"
#include "nfa.hpp"

#include <stack>
#include <vector>
#include <list>

using namespace std;

FILE *graphFile;

extern int debug;
extern int silent; /***< Potlaci vsechny vystupy na STDOUT krome vynuceneho vystupu do MSFM */

T_CONFIG config;

T_OPTIONS_STACK optionsStack;

static struct timespec cas;
unsigned int startTime, stopTime, diffTime;

void NOT_IMPLEMENTED()
{
	if( !silent ) cerr << "ERROR: Not implemented." << endl;
	exit(NFA_FAIL);
}

void EMPTY_IMPLEMENTATION(string what)
{
	if( !silent && config.strict ) cerr << "WARNING: Implementation of " << what << " is empty." << endl;
}

void SEMANTICS_ERROR(string error = NULL)
{
	if(error.empty()) cerr << "ERROR: semantics error" << endl;
	else cerr << "ERROR: " << error << endl;
	exit(NFA_FAIL);
}

/**
 * Zásobník na operace prováděné s automaty
*/
stack<T_OPERACE> operaceStack;

/**
 * Zásobník pro automaty
 */
stack<T_FA*> fas;

// automaty používané v programu
T_FA *fa1 = new T_FA;
T_FA *fa2 = new T_FA;
T_FA *fa = new T_FA;

// uzly používané v aplikaci
T_FANODE *fanode1 = new T_FANODE;
T_FANODE *fanode2 = new T_FANODE;

T_FA* FAstackTopPop()
{
	if( !fas.empty() )
	{
		T_FA *fa;
		fa = fas.top();
		fas.pop();
		return fa;
	}
	else
	{
		if( !silent ) cerr << "Doslo k chybe pry vyberu automatu ze zasobniku." << endl;
		exit(NFA_FAIL);
	}
}

/**
 *      FORMAT of Automata file (MSFM)
      - Number of the States in the automaton
      - Number of the transition in the automaton
      - Line with identifikator of the startState
      - Each transition is represenetd by one line in the file. Line
        is in format Source_State|Symbol|Target_State|Epsilon
      - End of the transition table is represented by line of #
      - Number of the end states
      - Line with identifikator of the endState. Every endstate is
        folowed by , (coma)
      - End of endState section is represented by line of #
      - Number of the symbols in symbol table
      - Every symbol is stored on its own line and it is represented
        as Symbol_Number:Character1|Character2|
      - End of the file
 */
void generujMSFM(ostream &os)
{
	fa = FAstackTopPop();

	// - Number of the States in the automaton
	os << dec << seznamSousedu.size() << endl;

	// - Number of the transition in the automaton
	int pocetPrechodu = 0;
	T_SEZNAM_SOUSEDU::iterator it = seznamSousedu.begin();
	list<T_SEZNAM_SOUSEDU_NODE>::iterator it2;
	while( it != seznamSousedu.end() )
	{
		pocetPrechodu += (**it).seznamSousedu.size();
		it++;
	}
	os << dec << pocetPrechodu << endl;

	// - Line with identifikator of the startState
	os << dec << fa->start->id << endl;

	// - Each transition is represenetd by one line in the file. Line
	//   is in format Source_State|Symbol|Target_State|Epsilon
	it = seznamSousedu.begin();
	while( it != seznamSousedu.end() )
	{
		it2 = (**it).seznamSousedu.begin();
		while( it2 != (**it).seznamSousedu.end() )
		{
			if( *((*it2).symbolTableRow->nazev) == "epsilon" )
			{
				os << (**it).id << "|" << 0 << "|" << (*it2).soused->id << "|1" << endl;
			}
			else
			{
				os << (**it).id << "|" << (*it2).symbolTableRow->printId << "|" << (*it2).soused->id << "|0" << endl;
			}
			it2++;
		}
		it++;
	}

	//- End of the transition table is represented by line of #
	os << "######################################################################################" << endl;

	// - Number of the end states
	os << 1 << endl;
	// - Line with identifikator of the endState. Every endstate is
     //   folowed by , (coma)
	os << dec << fa->end->id << "," << endl;
     // - End of endState section is represented by line of #
	os << "######################################################################################" << endl;

	// - Number of the symbols in symbol table
	//os << symbolTable.size() << endl; // bere i neaktivni radky
	vector<T_SYMBOL_TABLE_ROW*>::iterator it3 = symbolTable.begin();
	unsigned pocetSymbolu = 0;
	while( it3 != symbolTable.end() )
	{
		if( *((*it3)->nazev) == "epsilon" ) { it3++; continue; }
		if( (*it3)->pouzity == false ) { it3++; continue; }
		pocetSymbolu++;
		it3++;
	}
	os << pocetSymbolu << endl;

	// - Every symbol is stored on its own line and it is represented
	//   as Symbol_Number:Character1|Character2|
	// nesmí se přeskakovat symboly, protože by vznikla prázdná reference z tabulky přechodů
	it3 = symbolTable.begin();
	while( it3 != symbolTable.end() )
	{
		//if( *((*it3)->nazev) == "epsilon" ) { it3++; continue; }

		if( (*it3)->pouzity == false ) { it3++; continue; }

		os << (**it3).printId << ":";
		vector<unsigned char>::iterator it4 = (**it3).symbol.znaky.begin();

		// export cc-symbolů
		if( config.ccSymbols == true && ((**it3).symbol.minimum != -1 || (**it3).symbol.maximum != -1) )
		{
			os << "#";
			if( (**it3).symbol.minimum != -1 ) os << (**it3).symbol.minimum; else os << "";
			os << "#";
			if( (**it3).symbol.maximum != -1 ) os << (**it3).symbol.maximum; else os << "";
			os << "#";
		}
		if(config.eofExport == true && (*(*it3)->nazev) == "EOI" ) os << "EOF|";
		// export vlastních symbolů
		while( it4 != (**it3).symbol.znaky.end() )
		{
			if( strcmp( config.charExport, "dec") == 0 ) os << *it4 << "|";
			else
			{
				os << "0x"; os.width(2); os.fill('0'); os << hex << (int)*it4;
				os << "|" << dec;
			}
			it4++;
		}
		os << endl;
		it3++;
	}

	// - End of the file

	fas.push(fa);
}

void module_init(T_CONFIG configuration)
{
	config = configuration;

	// počáteční konfigurace
	options.caseless = false;
	options.multiline = false;
	options.extended = false;
	options.newline = CR;
	options.editable = true;
	optionsStack.push_front(options);

	// nalezení přepínačů na konci výrazu
	char c;
	for(size_t i=0; i<strlen(config.inputPattern); i++)
	{
		c = config.inputPattern[strlen(config.inputPattern)-i];
		if(c == '/') break; // konec vlastního výrazu
		if(c == 'x') setOption(true, "extended"); // PCRE_EXTENDED
		if(c == 'i') setOption(true, "caseless"); // PCRE_CASELESS
		if(c == 'm') setOption(true, "multiline"); // PCRE_CASELESS
	}
	optionsStack.front().editable = false;

	abeceda += (string)"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

	posixClasses.lower += "abcdefghijklmnopqrstuvwxyz";
	posixClasses.upper += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	posixClasses.alpha += posixClasses.lower;
	posixClasses.alpha += posixClasses.upper;
	posixClasses.digit += "0123456789";
	posixClasses.alnum += posixClasses.alpha;
	posixClasses.alnum += posixClasses.digit;
	for(int i=0; i<128; i++) { posixClasses.ascii += (char)i; }
	posixClasses.blank += (char)0x20; // SP
	posixClasses.blank += (char)0x09; // HT
	for(int i=0; i<32; i++) { posixClasses.cntrl += (char)i; }
	posixClasses.cntrl += (char)0x127; // del
	for(int i=33; i<127; i++) { posixClasses.graph += (char)i; }
	for(int i=32; i<127; i++) { posixClasses.print += (char)i; }
	posixClasses.punct += "[!\"#$%&'()*+,\\-./:;<=>?@[\\]^_`{|}~]";
	posixClasses.xdigit += "abcdefABCDEF0123456789";

	backslashClasses.digit += posixClasses.digit;
	vytvorDoplnek(backslashClasses.Ndigit, backslashClasses.digit);

	// HT, CR, SP
	backslashClasses.hWhitespace += (char)0x09;
	backslashClasses.vWhitespace += (char)chCR;
	backslashClasses.hWhitespace += (char)0x20;
	vytvorDoplnek(backslashClasses.NhWhitespace, backslashClasses.hWhitespace);

	// VT, LF, FF
	backslashClasses.vWhitespace += (char)0x0b;
	backslashClasses.vWhitespace += (char)chLF;
	backslashClasses.vWhitespace += (char)0x0c;
	vytvorDoplnek(backslashClasses.NvWhitespace, backslashClasses.vWhitespace);

	// PCRE: HT  (9), LF (10), FF (12), CR (13), and space (32)
	backslashClasses.whitespace += (char)0x09;
	backslashClasses.whitespace += (char)chLF;
	backslashClasses.whitespace += (char)0x0c;
	backslashClasses.whitespace += (char)chCR;
	backslashClasses.whitespace += (char)0x20;
	vytvorDoplnek(backslashClasses.Nwhitespace, backslashClasses.whitespace);

	backslashClasses.wordchar += '_';
	backslashClasses.wordchar += backslashClasses.digit;
	backslashClasses.wordchar += posixClasses.alpha;
	vytvorDoplnek(backslashClasses.Nwordchar, backslashClasses.wordchar);

	posixClasses.word = backslashClasses.wordchar;

	// PCRE: HT (9), LF (10), VT (11), FF (12), CR (13), and space (32)
	posixClasses.space += backslashClasses.whitespace;
	posixClasses.space += (char)0x0b;

	clock_gettime(CLOCK_REALTIME, &cas);
	startTime = cas.tv_nsec;
}

/**
 * Normalizuje výsledný KA.
 * - přečísluje čísla stavů tak, aby počáteční měl číslo 0, dále podle DFS
 */
void normalizujFA()
{
	if(fas.empty()) return;

	T_FA *fa = fas.top();

	unsigned cisloUzlu = 0;

	stack<T_FANODE*> fanodes;

	T_FANODE * fanode;

	fanodes.push(fa->start);

	while(!fanodes.empty())
	{
		fanode = fanodes.top(); fanodes.pop();

		fanode->id = cisloUzlu++;
		fanode->visited = true;
		list<T_SEZNAM_SOUSEDU_NODE>::iterator it = fanode->seznamSousedu.begin();
		//fanode->seznamSousedu.sort();
		while(it != fanode->seznamSousedu.end())
		{
			if( it->soused->visited == false ) fanodes.push(it->soused);
			it->soused->visited = true;
			it++;
		}
	}
}

void module_exit(int ret)
{
	// vypocet delky trvani prevodu - konec
	clock_gettime(CLOCK_REALTIME, &cas);
	stopTime = cas.tv_nsec;
	diffTime = stopTime - startTime;

	normalizujFA();
	optimizeSymbolTable();

	if( !silent )
	{
		cout << "+"; for(int i=0; i<78; i++) cout << "-"; cout << "+" << endl;
		cout << "| Pattern: " << config.inputPattern << endl;
		if( ret == 0 )
		{
			cout << "| => parsed succesfly" << endl;
			cout << "| MSFM output in: " << osetriVystup(config.outputMsfmFile) << endl;
			if( strcmp(config.outputDotFile, "") != 0 ) cout << "| DOT output in: " << osetriVystup(config.outputDotFile) << endl;
		}
		else if( ret == 1 ) cout << "| => could not parsed: SYNTAX ERROR" << endl;
		else cout << "| => could not parsed: MEMORY EXHAUSTION" << endl;

		cout.precision(4);
		cout << "| Elapsed time: " << fixed << (float)diffTime/1000000.0 << " ms" << endl;
		cout << "+"; for(int i=0; i<78; i++) cout << "-"; cout << "+" << endl;
	}

	if( debug ) cout << symbolTable;
	//cout << seznamSousedu;

	if( strcmp(config.outputDotFile, "") != 0 )
	{
		ofstream graf;
		graf.open (config.outputDotFile, ios::trunc);
		graf << seznamSousedu;
		graf.close();
	}

	if( ret == 0 )
	{
		if( !strcmp(config.outputMsfmFile, "STDOUT") ) { generujMSFM(cout); }
		else
		{
			ofstream nfaFile;
			nfaFile.open(config.outputMsfmFile, ios::trunc);
			generujMSFM(nfaFile);
			nfaFile.close();
		}
	}

	if( debug && strcmp(config.outputMsfmFile, "STDOUT") ) generujMSFM(cout);
}

// pcre <<< modif_front pattern modif_rear
void pcre2modif_front_pattern_modif_rear(){
}
// modif_front <<< pcre_delim
void modif_front2pcre_delim(){
}
// modif_front <<< modif_front_ext pcre_delim
void modif_front2modif_front_ext_pcre_delim(){
}
// modif_front_ext <<< modif_front_unit
void modif_front_ext2modif_front_unit(){
}
// modif_front_ext <<< modif_front_unit-modif_front_ext
void modif_front_ext2modif_front_unit_modif_front_ext(){
}
// modif_front_unit <<< UTF8
void modif_front_unit2UTF8(){
	NOT_IMPLEMENTED();
}
// modif_front_unit <<< UCP
void modif_front_unit2UCP(){
	NOT_IMPLEMENTED();
}
// modif_rear <<< pcre_delim
void modif_rear2pcre_delim(){
}
// modif_rear <<< pcre_delim modif_rear_ext
void modif_rear2pcre_delim_modif_rear_ext(){
}
// modif_rear_ext <<< modif_rear_unit
void modif_rear_ext2modif_rear_unit(){
}
// modif_rear_ext <<< modif_rear_unit-modif_rear_ext
void modif_rear_ext2modif_rear_unit_modif_rear_ext(){
}
// modif_rear_unit <<< MODIF_CASELESS
void modif_rear_unit2MODIF_CASELESS(){
	// nastaveni provedeno v konstruktoru parseru
	//options.caseless = true;
	//caseInsesitive(symbolTable);
}
// modif_rear_unit <<< MODIF_MULTILINE
void modif_rear_unit2MODIF_MULTILINE(){
	//options.multiline = true;
	if( options.assertStart == true )
	{
		T_FANODE *node1 = vytvorUzel();
		T_FANODE *node2 = vytvorUzel();

		T_FA *fa = FAstackTopPop();

		//spojHranou(node1, node1, any);
		//spojHranou(node1, node2, bs_whitesp);
		//spojHranou(node2, fa->start, epsilon);
		spojHranou(node1, fa->start, epsilon);
		spojHranou(node1, node2, epsilon);
		spojHranou(node2, node2, all);
		
		T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)chCR);
		symbol->symbol += chLF;
		*(symbol->nazev) = "["+*(symbol->nazev)+"0x0a]";
		spojHranou(node2, fa->start, symbol);
		fa->start = node1;
		fas.push(fa);
	}
	/*if( options.assertEnd == true )
	{
		T_FANODE *node1 = vytvorUzel();
		T_FANODE *node2 = vytvorUzel();

		T_FA *fa = FAstackTopPop();

		spojHranou(node2, node2, any);
		spojHranou(node1, node2, bs_whitesp);
		spojHranou(node1, node1, bs_whitesp);
		spojHranou(fa->end, node1, epsilon);
		fa->end = node2;
		fas.push(fa);
	}*/
}
// modif_rear_unit <<< MODIF_DOTALL
void modif_rear_unit2MODIF_DOTALL(){
	dotAll(symbolTable);
}
// modif_rear_unit <<< MODIF_EXTENDED
void modif_rear_unit2MODIF_EXTENDED(){
	// nastaveni provedeno v init fázi
}
// modif_rear_unit <<< MODIF_UNGREEDY
void modif_rear_unit2MODIF_UNGREEDY(){
	EMPTY_IMPLEMENTATION("ungreedy modificator");
}
// modif_rear_unit <<< MODIF_R
void modif_rear_unit2MODIF_R(){
	EMPTY_IMPLEMENTATION("R modificator");
}
// modif_rear_unit <<< MODIF_O
void modif_rear_unit2MODIF_O(){
	EMPTY_IMPLEMENTATION("O modificator");
}
// modif_rear_unit <<< MODIF_P
void modif_rear_unit2MODIF_P(){
	EMPTY_IMPLEMENTATION("P modificator");
}
// modif_rear_unit <<< MODIF_B
void modif_rear_unit2MODIF_B(){
	EMPTY_IMPLEMENTATION("B modificator");
}
// pcre_delim <<< SLASH
void pcre_delim2SLASH(){
}
// pattern <<< newlinespec inslash
void pattern2newlinespec_inslash(){
}
// pattern <<< inslash
void pattern2inslash(){
}
// inslash <<< rv
void inslash2rv(){
	fa = FAstackTopPop();

	// vytvoří počáteční iteraci
	fanode1 = vytvorUzel();
	spojHranou(fanode1, fanode1, all);
	spojHranou(fanode1, fa->start, epsilon);
	fa->start = fanode1;

	// poznámka od ikosar: pro RV typu /rv/implementovat chování jako by to byl výraz /rv$/, cyklení v koncovém stavu je pro naše účely zbytečné
	// připojí koncovou iteraci
	/*fanode2 = vytvorUzel();
	spojHranou(fanode2, fanode2, any);
	spojHranou(fa->end, fanode2, epsilon);
	fa->end = fanode2;*/

	fas.push(fa);
}
// inslash <<< bol-rv
void inslash2bol_rv(){
	options.assertStart = true;
	// poznámka od ikosar: pro RV typu /rv/implementovat chování jako by to byl výraz /rv$/, cyklení v koncovém stavu je pro naše účely zbytečné
	/*
	fa = FAstackTopPop();

	// připojí koncovou iteraci
	fanode2 = vytvorUzel();
	spojHranou(fanode2, fanode2, any);
	spojHranou(fa->end, fanode2, epsilon);
	fa->end = fanode2;

	fas.push(fa);*/
}
// inslash <<< rv-eol
void inslash2rv_eol(){
	options.assertEnd = true;
	fa = FAstackTopPop();

	// vytvoří počáteční iteraci
	fanode1 = vytvorUzel();
	spojHranou(fanode1, fanode1, any);
	spojHranou(fanode1, fa->start, epsilon);
	fa->start = fanode1;

	// připojí koncový přechod s koncem vstupu
	fanode1 = vytvorUzel();
	spojHranou(fa->end, fanode1, eoi);
	fa->end = fanode1;

	fas.push(fa);
}
// inslash <<< bol-rv|eol
void inslash2bol_rv_eol(){
	options.assertEnd = true;
	options.assertStart = true;

	fa = FAstackTopPop();

	// připojí koncový přechod s koncem vstupu
	fanode1 = vytvorUzel();
	spojHranou(fa->end, fanode1, eoi);
	fa->end = fanode1;

	fas.push(fa);
}
// bol <<< BOL
void bol2BOL(){
}
// eol <<< EOL
void eol2EOL(){
}
// pcreDelim <<< SLASH
void pcreDelim2SLASH(){
}
// rv <<< exp
void rv2ext_exp(){
	if( optionsStack.size() > 1 ) optionsStack.pop_front();
}
// rv <<< ext_exp or ext_exp
void rv2rv_or_rv(){
	fa2 = FAstackTopPop();
	fa1 = FAstackTopPop();

	fanode1 = vytvorUzel();
	fanode2 = vytvorUzel();

	spojHranou(fanode1, fa1->start, epsilon);
	spojHranou(fanode1, fa2->start, epsilon);

	spojHranou(fa1->end, fanode2, epsilon);
	spojHranou(fa2->end, fanode2, epsilon);

	fa = new T_FA;
	fa->start = fanode1;
	fa->end = fanode2;

	fas.push(fa);
}
// rv <<< or ext_exp
void rv2or_rv(){
	fa1 = FAstackTopPop();

	fanode1 = vytvorUzel();
	fanode2 = vytvorUzel();

	spojHranou(fanode1, fa1->start, epsilon);
	spojHranou(fa1->end, fanode2, epsilon);

	spojHranou(fanode1, fanode2, epsilon);

	fa->start = fanode1;
	fa->end = fanode2;
	fas.push(fa);
}
// rv <<< ext_exp or
void rv2rv_or(){
	fa1 = FAstackTopPop();

	fanode1 = vytvorUzel();
	fanode2 = vytvorUzel();

	spojHranou(fanode1, fa1->start, epsilon);
	spojHranou(fa1->end, fanode2, epsilon);

	spojHranou(fanode1, fanode2, epsilon);

	fa->start = fanode1;
	fa->end = fanode2;
	fas.push(fa);
}
// inslash <<< rv
void ext_exp2exp(){
}
// inslash <<< bol-rv
void ext_exp2bol_exp(){
}
// inslash <<< rv-eol
void ext_exp2exp_eol(){
	fa = FAstackTopPop();

	// připojí koncový přechod s koncem vstupu
	fanode1 = vytvorUzel();
	spojHranou(fa->end, fanode1, eoi);
	fa->end = fanode1;

	fas.push(fa);
}
// inslash <<< bol-rv|eol
void ext_exp2bol_exp_eol(){
	fa = FAstackTopPop();

	// připojí koncový přechod s koncem vstupu
	fanode1 = vytvorUzel();
	spojHranou(fa->end, fanode1, eoi);
	fa->end = fanode1;

	fas.push(fa);
}
// exp <<< ext_unit
void exp2ext_unit(){
}
// exp <<< ext_unit-exp
void exp2ext_unit_exp(){
	if( fas.size() < 2 ) NOT_IMPLEMENTED();
	fa2 = FAstackTopPop();
	fa1 = FAstackTopPop();
	fa = spoj_automaty(fa1, fa2);
	fas.push(fa);
}
// ext_unit <<< unit
void ext_unit2unit(){
}
// ext_unit <<< quantify_unit
void ext_unit2quantify_unit(){
	fa1 = FAstackTopPop();
	if( operaceStack.empty() ) NOT_IMPLEMENTED();
	T_OPERACE operace = operaceStack.top(); operaceStack.pop();
	fa = vytvorOpakovani(fa1, operace);
	fas.push(fa);
}
// quantify_unit <<< unit quantify
void quantify_unit2unit_quantify(){
}
// quantify <<< quantifier
void quantify2quantifier(){
}
// quantify <<< quantifier-possessive
void quantify2quantifier_possessive(){
}
// quantify <<< quantifier-lazy
void quantify2quantifier_lazy(){
}
// quantifier <<< ZEROMORE
void quantifier2ZEROMORE(){
	operaceStack.push(zeromore);
}
// quantifier <<< ZEROONE
void quantifier2ZEROONE(){
	operaceStack.push(zeroone);
}
// quantifier <<< ONEMORE
void quantifier2ONEMORE(){
	operaceStack.push(onemore);
}
// quantifier <<< repeating
void quantifier2repeating(){
    operaceStack.push(repeating);
}
// possessive <<< ONEMORE
void possessive2ONEMORE(){
	EMPTY_IMPLEMENTATION("possessive quantifier");
}
// lazy <<< ZEROONE
void lazy2ZEROONE(){
	EMPTY_IMPLEMENTATION("lazy quantifier");
}
// or <<< OR
void or2OR(){
}
// unit <<< element
void unit2element(){
	if( strStack.empty() ) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * symbol = strStack.top();
	strStack.pop();
	T_FA *fa = new T_FA;
	if( *symbol->nazev == "nop" )
	{
		fanode1 = vytvorUzel();
		fa->start = fanode1;
		fa->end = fanode1;
	}
	else
	{
		fanode1 = vytvorUzel();
		fanode2 = vytvorUzel();

		spojHranou(fanode1, fanode2, symbol);
		fa->start = fanode1;
		fa->end = fanode2;
	}

	fas.push(fa);
}
// unit <<< capturing
void unit2capturing(){
}
// unit <<< option
void unit2option(){
	setOption(false, "editable");

	T_FA *fa = new T_FA;
	fanode1 = vytvorUzel();
	fa->start = fanode1;
	fa->end = fanode1;
	fas.push(fa);
}
// unit <<< alternate
void unit2alternate(){
}
// option <<< optionStart option_set optionEnd
void option2optionStart_option_set_optionEnd(){
}
// option <<< optionStart-option_unset_group|optionEnd
void option2optionStart_option_unset_group_optionEnd(){
}
// option <<< optionStart-option_set|option_unset_group|optionEnd
void option2optionStart_option_set_option_unset_group_optionEnd(){
}
// optionStart <<< OPTION
void optionStart2OPTION(){
}
// optionEnd <<< RBRA
void optionEnd2RBRA(){
}
// option_unset_group <<< dash option_unset
void option_unset_group2dash_option_unset(){
}
// option_set <<< option_set_unit
void option_set2option_set_unit(){
}
// option_set <<< option_set_unit-option_set
void option_set2option_set_unit_option_set(){
}
// option_set_unit <<< MODIF_CASELESS
void option_set_unit2MODIF_CASELESS(){
	setOption(true, "caseless");
}
// option_set_unit <<< MODIF_DOTALL
void option_set_unit2MODIF_DOTALL(){
	NOT_IMPLEMENTED();
}
// option_set_unit <<< MODIF_EXTENDED
void option_set_unit2MODIF_EXTENDED(){
	setOption(true, "extended");
}
// option_set_unit <<< MODIF_MULTILINE
void option_set_unit2MODIF_MULTILINE(){
	NOT_IMPLEMENTED();
}
// option_set_unit <<< MODIF_DUPNAMES
void option_set_unit2MODIF_DUPNAMES(){
	NOT_IMPLEMENTED();
}
// option_set_unit <<< MODIF_UNGREEDY
void option_set_unit2MODIF_UNGREEDY(){
	EMPTY_IMPLEMENTATION("ungreedy modificator");
}
// option_unset <<< option_unset_unit
void option_unset2option_unset_unit(){
}
// option_unset <<< option_unset_unit-option_unset
void option_unset2option_unset_unit_option_unset(){
}
// option_unset_unit <<< MODIF_CASELESS
void option_unset_unit2MODIF_CASELESS(){
	setOption(false, "caseless");
}
// option_unset_unit <<< MODIF_DOTALL
void option_unset_unit2MODIF_DOTALL(){
	NOT_IMPLEMENTED();
}
// option_unset_unit <<< MODIF_EXTENDED
void option_unset_unit2MODIF_EXTENDED(){
	NOT_IMPLEMENTED();
}
// option_unset_unit <<< MODIF_MULTILINE
void option_unset_unit2MODIF_MULTILINE(){
	NOT_IMPLEMENTED();
}
// option_unset_unit <<< MODIF_DUPNAMES
void option_unset_unit2MODIF_DUPNAMES(){
	NOT_IMPLEMENTED();
}
// option_unset_unit <<< MODIF_UNGREEDY
void option_unset_unit2MODIF_UNGREEDY(){
	EMPTY_IMPLEMENTATION("ungreedy modificator");
}
// element <<< ASCII
void element2ASCII(char c){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(c);
	strStack.push(symbol);
}
// element <<< ANY
void element2ANY(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(any);
	strStack.push(symbol);
}
// element <<< SPACE
void element2SPACE(){
	T_SYMBOL_TABLE_ROW * symbol = NULL;
	if( options.extended == true ) symbol = addToSymbolTable(nop);
	else symbol = addToSymbolTable(space);

	strStack.push(symbol);
}
// element <<< newlinespec
void element2newlinespec(){
}
// element <<< hex
void element2hex(){
}
// element <<< TAB
void element2TAB(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)0x09);
	*symbol->nazev = "TAB";
	strStack.push(symbol);
}
// element <<< CR
void element2CR(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)chCR);
	*symbol->nazev = "CR";
	strStack.push(symbol);
}
// element <<< LF
void element2LF(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)chLF);
	*symbol->nazev = "LF";
	strStack.push(symbol);
}
// element <<< FF
void element2FF(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)0x0c);
	*symbol->nazev = "FF";
	strStack.push(symbol);
}
// element <<< BEL
void element2BEL(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)0x07);
	*symbol->nazev = "BEL";
	strStack.push(symbol);
}
// element <<< ESC
void element2ESC(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)0x1b);
	*symbol->nazev = "ESC";
	strStack.push(symbol);
}
// element <<< CONTROLX
void element2CONTROLX(char c){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)(c^32));
	*symbol->nazev = "CONTROLX";
	strStack.push(symbol);
}
// element <<< BSR
void element2BSR(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bsr);
	strStack.push(symbol);
}
// element <<< RESET
void element2RESET(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(nop);
	strStack.push(symbol);
}
// element <<< assertions
void element2assertions(){
}
// element <<< ONEBYTE
void element2ONEBYTE(){
}
// element <<< OCTAL
void element2OCTAL(char c){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)c);
	strStack.push(symbol);
}
// unit <<< chal
void unit2chal(){
}
// unit <<< class
void unit2class(){
	unit2element();
}
// element <<< backreference
void element2backreference(){
	NOT_IMPLEMENTED();
}
// element <<< subroutine
void element2subroutine(){
	NOT_IMPLEMENTED();
}
// assertions <<< WORDBOUNDARY
void assertions2WORDBOUNDARY(){
	NOT_IMPLEMENTED();
}
// assertions <<< NWORDBOUNDARY
void assertions2NWORDBOUNDARY(){
	NOT_IMPLEMENTED();
}
// assertions <<< STARTSUBJECT
void assertions2STARTSUBJECT(){
	NOT_IMPLEMENTED();
}
// assertions <<< ENDSUBJECT
void assertions2ENDSUBJECT(){
	NOT_IMPLEMENTED();
}
// assertions <<< OENDSUBJECT
void assertions2OENDSUBJECT(){
	NOT_IMPLEMENTED();
}
// assertions <<< FIRSTPOSITION
void assertions2FIRSTPOSITION(){
	NOT_IMPLEMENTED();
}
// hex <<< HEX
void hex2HEX(char c){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable((char)c);
	strStack.push(symbol);
}
// newlinespec <<< newlinespec_unit
void newlinespec2newlinespec_unit(){
}
// newlinespec <<< newlinespec_unit-newlinespec
void newlinespec2newlinespec_unit_newlinespec(){
}
// newlinespec_unit <<< OPT_CR
void newlinespec_unit2OPT_CR(){
	options.newline = CR;
}
// newlinespec_unit <<< OPT_LF
void newlinespec_unit2OPT_LF(){
	optionsStack.front().newline = LF;
}
// newlinespec_unit <<< OPT_CRLF
void newlinespec_unit2OPT_CRLF(){
	optionsStack.front().newline = CRLF;
}
// newlinespec_unit <<< OPT_ANYCRLF
void newlinespec_unit2OPT_ANYCRLF(){
	optionsStack.front().newline = ANYCRLF;
}
// newlinespec_unit <<< OPT_ANY_NEWLINE
void newlinespec_unit2OPT_ANY_NEWLINE(){
	optionsStack.front().newline = ANY;
}

// capturing <<< startCapturing rv endCapturing
void capturing2startCapturing_rv_endCapturing(){
}
// capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing
void capturing2capturingNamed_capturingName_capturingNameEnd_rv_endCapturing(){
}
// capturing <<< capturingNon-rv|endCapturing
void capturing2capturingNon_rv_endCapturing(){
}
// capturing <<< capturingNonreset-rv|endCapturing
void capturing2capturingNonreset_rv_endCapturing(){
}
// capturing <<< capturingAtomic-rv|endCapturing
void capturing2capturingAtomic_rv_endCapturing(){
}
// capturing <<< capturingComment-rv|endCapturing
void capturing2capturingComment_rv_endCapturing(){
	fa = FAstackTopPop();
	odstranFA(fa);
	T_FANODE * fa1;

	fa1 = vytvorUzel();
	fa->start = fa1;
	fa->end = fa1;

	fas.push(fa);
}
// capturing <<< capturingPosahead-rv|endCapturing
void capturing2capturingPosahead_rv_endCapturing(){
	NOT_IMPLEMENTED();
}
// capturing <<< capturingNegahead-rv|endCapturing
void capturing2capturingNegahead_rv_endCapturing(){
	NOT_IMPLEMENTED();
}
// capturing <<< capturingPosbehind-rv|endCapturing
void capturing2capturingPosbehind_rv_endCapturing(){
	NOT_IMPLEMENTED();
}
// capturing <<< capturingNegbehind-rv|endCapturing
void capturing2capturingNegbehind_rv_endCapturing(){
	NOT_IMPLEMENTED();
}
// capturingNamed <<< CAPTURING_NAMED
void capturingNamed2CAPTURING_NAMED(){
}
// capturingName <<< capturingNameAdd
void capturingName2capturingNameAdd(){
}
// capturingName <<< capturingNameAdd-capturingName
void capturingName2capturingNameAdd_capturingName(){
}
// capturingNameAdd <<< ASCII
void capturingNameAdd2ASCII(char c){
}
// capturingNon <<< CAPTURING_NON
void capturingNon2CAPTURING_NON(){
}
// capturingNonreset <<< CAPTURING_NONRESET
void capturingNonreset2CAPTURING_NONRESET(){
}
// capturingAtomic <<< CAPTURING_ATOMIC
void capturingAtomic2CAPTURING_ATOMIC(){
}
// capturingComment <<< CAPTURING_COMMENT
void capturingComment2CAPTURING_COMMENT(){
}
// capturingPosahead <<< CAPTURING_POSAHEAD
void capturingPosahead2CAPTURING_POSAHEAD(){
}
// capturingNegahead <<< CAPTURING_NEGAHEAD
void capturingNegahead2CAPTURING_NEGAHEAD(){
}
// capturingPosbehind <<< CAPTURING_POSBEHIND
void capturingPosbehind2CAPTURING_POSBEHIND(){
}
// capturingNegbehind <<< CAPTURING_NEGBEHIND
void capturingNegbehind2CAPTURING_NEGBEHIND(){
}
// capturingNameEnd <<< CAPTURING_NAMED_END
void capturingNameEnd2CAPTURING_NAMED_END(){
}
// startCapturing <<< LPAR
void startCapturing2LPAR(){
}
// endCapturing <<< RPAR
void endCapturing2RPAR(){
}
// repeating <<< startRepeating interval endRepeating
void repeating2startRepeating_interval_endRepeating(){
}
// startRepeating <<< LBRA
void startRepeating2LBRA(){
}
// endRepeating <<< RBRA
void endRepeating2RBRA(){
}
// interval <<< minimum intervalDelim maximum
void interval2minimum_intervalDelim_maximum(){
}
// interval <<< minimum-intervalDelim
void interval2minimum_intervalDelim(){
	opakovani.maximum = -1;
}
// interval <<< maximum
void interval2maximum(){
	opakovani.minimum = opakovani.maximum;
}
// minimum <<< INT
void minimum2INT(int i){
    opakovani.minimum = i;
}
// maximum <<< INT
void maximum2INT(int i){
    opakovani.maximum = i;
}
// intervalDelim <<< COMMA
void intervalDelim2COMMA(){
}
// class <<< classStart inclass classEnd
void class2classStart_inclass_classEnd(){
	// výstup z podstromu zpracování třídy znaků
	if( strStack.empty() ) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * symbol = strStack.top(); strStack.pop();
	*symbol->nazev = "[" + *symbol->nazev + "]";
	strStack.push(symbol);
}
// class <<< slashcharclass
void class2slashcharclass(){
}
// class <<< posix_class
void class2posix_class(){
}
// classStart <<< LBOX
void classStart2LBOX(){
}
// negateClassStart <<< NEGATECLASSSTART
void negateClassStart2NEGATECLASSSTART(){
}
// classEnd <<< RBOX
void classEnd2RBOX(){
}
// negateClass <<< NEGATE
void negateClass2NEGATE(){
}
// slashcharclass <<< DECDIGIT
void slashcharclass2DECDIGIT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_digit);
	strStack.push(symbol);
}
// slashcharclass <<< NDECDIGIT
void slashcharclass2NDECDIGIT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_ndigit);
	strStack.push(symbol);
}
// slashcharclass <<< HWHITESPACE
void slashcharclass2HWHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_whitesp);
	strStack.push(symbol);
}
// slashcharclass <<< NHWHITESPACE
void slashcharclass2NHWHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_whitesp);
	strStack.push(symbol);
}
// slashcharclass <<< WHITESPACE
void slashcharclass2WHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_whitesp);
	strStack.push(symbol);
}
// slashcharclass <<< NWHITESPACE
void slashcharclass2NWHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_nwhitesp);
	strStack.push(symbol);
}
// slashcharclass <<< VWHITESPACE
void slashcharclass2VWHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_vwhitesp);
	strStack.push(symbol);
}
// slashcharclass <<< NVWHITESPACE
void slashcharclass2NVWHITESPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_nvwhitesp);
	strStack.push(symbol);
}
// slashcharclass <<< WORDCHAR
void slashcharclass2WORDCHAR(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_wordchar);
	strStack.push(symbol);
}
// slashcharclass <<< NWORDCHAR
void slashcharclass2NWORDCHAR(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(bs_nwordchar);
	strStack.push(symbol);
}
// inclass <<< inclass_ext_unit
void inclass2inclass_ext_unit(){
}
// inclass <<< bol-inclass_ext_unit
void inclass2bol_inclass_ext_unit(){
	if( strStack.empty() ) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * symbol = strStack.top(); strStack.pop();
	T_SYMBOL_TABLE_ROW * novy = duplikujStr(symbol);
	novy->symbol.znaky.clear();
	vytvorDoplnek(novy->symbol, symbol->symbol);
	*novy->nazev = "^" + *novy->nazev;
	symbol->pouzity = false;
	strStack.push(novy);
}
// inclass_ext_unit <<< inclass_unit
void inclass_ext_unit2inclass_unit(){
}
// inclass_ext_unit <<< inclass_unit-inclass_ext_unit
void inclass_ext_unit2inclass_unit_inclass_ext_unit(){
	T_SYMBOL_TABLE_ROW * novySymbol;
	T_SYMBOL_TABLE_ROW * symbol;

	if( strStack.empty() ) NOT_IMPLEMENTED();
	symbol = strStack.top(); strStack.pop();
	novySymbol = strStack.top(); strStack.pop();

	*novySymbol += *symbol;
	symbol->pouzity = false;
	strStack.push(novySymbol);
}
// inclass_unit <<< inclass_element
void inclass_unit2inclass_element(){
}
// inclass_unit <<< chal
void inclass_unit2chal(){
}
// inclass_unit <<< rangechars
void inclass_unit2rangechars(){
}
// inclass_unit <<< ASCII
void inclass_element2ASCII(char c){
	element2ASCII(c);
}
// inclass_unit <<< posix_class
void inclass_element2posix_class(){
}
// inclass_unit <<< slashcharclass
void inclass_element2slashcharclass(){
}
// inclass_unit <<< hex
void inclass_element2hex(){
}
// inclass_unit <<< TAB
void inclass_element2TAB(){
	element2TAB();
}
// inclass_unit <<< CR
void inclass_element2CR(){
	element2CR();
}
// inclass_unit <<< LF
void inclass_element2LF(){
	element2LF();
}
// inclass_unit <<< FF
void inclass_element2FF(){
	element2FF();
}
// inclass_unit <<< BEL
void inclass_element2BEL(){
	element2BEL();
}
// inclass_unit <<< ESC
void inclass_element2ESC(){
	element2ESC();
}
// inclass_unit <<< DASH
void inclass_element2DASH(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable('-');
	strStack.push(symbol);
}
// inclass_unit <<< CONTROLX
void inclass_element2CONTROLX(char c){
	element2CONTROLX(c);
}
// inclass_unit <<< RESET
void inclass_element2RESET(){
}
// inclass_unit <<< OCTAL
void inclass_element2OCTAL(char c){
	element2OCTAL(c);
}
// inclass_unit <<< chal
void inclass_element2chal(){
}
// rangechars <<< range_unit dash range_unit
void rangechars2range_unit_dash_range_unit(){
	if( strStack.size() < 2) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * end = strStack.top(); strStack.pop();
	if( strStack.size() < 1 ) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * start = strStack.top(); strStack.pop();

	T_SYMBOL_TABLE_ROW * novy = rozsahSymbolu(start, end);

	strStack.push(novy);
}
// dash <<< DASH
void dash2DASH(){
}
// rangechars <<< CHARCLASS <<< VALUE
void rangechars2INT(int i){
	unsigned char low, high;
	// extract 2 values from yylval
	low = (unsigned char)i;
	high = (unsigned char)(i >> 8);

	if(high < low) SEMANTICS_ERROR("Range out of order in character class.");

	T_SYMBOL_TABLE_ROW * start = addToSymbolTable((char)low);
	T_SYMBOL_TABLE_ROW * end = addToSymbolTable((char)high);

	T_SYMBOL_TABLE_ROW * novy = rozsahSymbolu(start, end);
	start->pouzity = false;
	end->pouzity = false;
	strStack.push(novy);
}
// posix_class <<< P_ALNUM
void posix_class2P_ALNUM(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_alnum);
	strStack.push(symbol);
}
// posix_class <<< P_ALPHA
void posix_class2P_ALPHA(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_alpha);
	strStack.push(symbol);
}
// posix_class <<< P_ASCII
void posix_class2P_ASCII(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_ascii);
	strStack.push(symbol);
}
// posix_class <<< P_BLANK
void posix_class2P_BLANK(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_blank);
	strStack.push(symbol);
}
// posix_class <<< P_CNTRL
void posix_class2P_CNTRL(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_cntrl);
	strStack.push(symbol);
}
// posix_class <<< P_DIGIT
void posix_class2P_DIGIT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_digit);
	strStack.push(symbol);
}
// posix_class <<< P_GRAPH
void posix_class2P_GRAPH(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_graph);
	strStack.push(symbol);
}
// posix_class <<< P_LOWER
void posix_class2P_LOWER(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_lower);
	strStack.push(symbol);
}
// posix_class <<< P_PRINT
void posix_class2P_PRINT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_print);
	strStack.push(symbol);
}
// posix_class <<< P_PUNCT
void posix_class2P_PUNCT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_punct);
	strStack.push(symbol);
}
// posix_class <<< P_SPACE
void posix_class2P_SPACE(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_space);
	strStack.push(symbol);
}
// posix_class <<< P_UPPER
void posix_class2P_UPPER(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_upper);
	strStack.push(symbol);
}
// posix_class <<< P_WORD
void posix_class2P_WORD(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_word);
	strStack.push(symbol);
}
// posix_class <<< P_XDIGIT
void posix_class2P_XDIGIT(){
	T_SYMBOL_TABLE_ROW * symbol = addToSymbolTable(p_xdigit);
	strStack.push(symbol);
}
// posix_class <<< posix_class_neg
void posix_class2posix_class_neg(){
	if( strStack.empty() ) NOT_IMPLEMENTED();
	T_SYMBOL_TABLE_ROW * symbol = strStack.top(); strStack.pop();
	T_SYMBOL_TABLE_ROW * novy = duplikujStr(symbol);
	vytvorDoplnek(novy->symbol, symbol->symbol);
	symbol->pouzity = false;
	*novy->nazev = "[:^" + novy->nazev->substr(2);
	strStack.push(novy);
}
// posix_class_neg <<< NP_ALNUM
void posix_class_neg2NP_ALNUM(){
	posix_class2P_ALNUM();
}
// posix_class_neg <<< NP_ALPHA
void posix_class_neg2NP_ALPHA(){
	posix_class2P_ALPHA();
}
// posix_class_neg <<< NP_ASCII
void posix_class_neg2NP_ASCII(){
	posix_class2P_ASCII();
}
// posix_class_neg <<< NP_BLANK
void posix_class_neg2NP_BLANK(){
	posix_class2P_BLANK();
}
// posix_class_neg <<< NP_CNTRL
void posix_class_neg2NP_CNTRL(){
	posix_class2P_CNTRL();
}
// posix_class_neg <<< NP_DIGIT
void posix_class_neg2NP_DIGIT(){
	posix_class2P_DIGIT();
}
// posix_class_neg <<< NP_GRAPH
void posix_class_neg2NP_GRAPH(){
	posix_class2P_GRAPH();
}
// posix_class_neg <<< NP_LOWER
void posix_class_neg2NP_LOWER(){
	posix_class2P_LOWER();
}
// posix_class_neg <<< NP_PRINT
void posix_class_neg2NP_PRINT(){
	posix_class2P_PRINT();
}
// posix_class_neg <<< NP_PUNCT
void posix_class_neg2NP_PUNCT(){
	posix_class2P_PUNCT();
}
// posix_class_neg <<< NP_SPACE
void posix_class_neg2NP_SPACE(){
	posix_class2P_SPACE();
}
// posix_class_neg <<< NP_UPPER
void posix_class_neg2NP_UPPER(){
	posix_class2P_UPPER();
}
// posix_class_neg <<< NP_WORD
void posix_class_neg2NP_WORD(){
	posix_class2P_WORD();
}
// posix_class_neg <<< NP_XDIGIT
void posix_class_neg2NP_XDIGIT(){
	posix_class2P_XDIGIT();
}
// chal <<< chalStart inchal chalEnd
void chal2chalStart_inchal_chalEnd(){
}
// chalStart <<< CHALSTART
void chalStart2CHALSTART(){
}
// chalEnd <<< CHALEND
void chalEnd2CHALEND(){
}
// inchal <<< inchalExtUnit
void inchal2inchalExtUnit(){
}
// inchal <<< inchalExtUnit-inchal
void inchal2inchalExtUnit_inchal(){
}
// inchalExtUnit <<< inchalUnit
void inchalExtUnit2inchalUnit(){
}
// inchalUnit <<< ASCII
void inchalUnit2ASCII(char c){
	element2ASCII(c);
}
// backreference <<< BACKREFERENCE
void backreference2BACKREFERENCE(){
}
// backreference <<< named_back_reference
void backreference2named_back_reference(){
}
// named_back_reference <<< nbrStart inNbr nbrEnd
void named_back_reference2nbrStart_inNbr_nbrEnd(){
}
// nbrStart <<< NAMED_BACKREFERENCE
void nbrStart2NAMED_BACKREFERENCE(){
}
// nbrEnd <<< NAMED_BACKREFERENCE_END
void nbrEnd2NAMED_BACKREFERENCE_END(){
}
// inNbr <<< inNbrUnit
void inNbr2inNbrUnit(){
}
// inNbr <<< inNbrUnit-inNbr
void inNbr2inNbrUnit_inNbr(){
}
// inNbrUnit <<< ASCII
void inNbrUnit2ASCII(char c){
}
// subroutine <<< SUBROUTINE_ALL
void subroutine2SUBROUTINE_ALL(){
}
// subroutine <<< SUBROUTINE_ABSOLUTE
void subroutine2SUBROUTINE_ABSOLUTE(){
}
// subroutine <<< SUBROUTINE_RELATIVE
void subroutine2SUBROUTINE_RELATIVE(){
}
// subroutine <<< named_subroutine
void subroutine2named_subroutine(){
}
// named_subroutine <<< nsrStart inNsr nsrEnd
void named_subroutine2nsrStart_inNsr_nsrEnd(){
}
// nsrStart <<< SUBROUTINE_NAME
void nsrStart2SUBROUTINE_NAME(){
}
// nsrEnd <<< SUBROUTINE_NAME_END
void nsrEnd2SUBROUTINE_NAME_END(){
}
// inNsr <<< inNsrUnit
void inNsr2inNsrUnit(){
}
// inNsr <<< inNsrUnit-inNsr
void inNsr2inNsrUnit_inNsr(){
}
// inNsrUnit <<< ASCII
void inNsrUnit2ASCII(char c){
}
