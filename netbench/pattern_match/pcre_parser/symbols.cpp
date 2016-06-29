/*
 * File:   symbols.cpp
 * Author: xpalam00
 *
 * Created on 13. květen 2011, 22:48
 */

#include "symbols.hpp"
#include "nodes.hpp"
#include "interface.h"

T_SYMBOL abeceda;
T_TABULKA_SYMBOLU symbolTable; // tabulka symbolu
stack<T_SYMBOL_TABLE_ROW*> strStack; // zasobnik symbolu pro převod z derivačního stromu

T_OPTIONS options;
extern T_CONFIG config;

/**
 * Nové ID symbolu tabulky, inkrementované po každém vložení do tabulky
 */
unsigned noveIdSymbolu = 0;

T_POSIX_CLASSES posixClasses;
T_BACKSLASH_CLASSES backslashClasses;

/**
 * Vloží symbol do množiny symbolů nad jednou hranou.
 * Hlídá správné pořadí symbolů a nevkládá duplicitní symboly.
 * @param os Symbol, do kterého se má přidat znak
 * @param c Znak, který se má vložit
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &os, char c)
{
	vector<unsigned char>::iterator it = os.znaky.begin();
	while(it != os.znaky.end())
	{
		if((unsigned char)*it < (unsigned char)c) it++;
		else if((unsigned char)*it == (unsigned char)c) return os;
		else break;
	}
	os.znaky.insert(it, (unsigned char)c);
	return os;
}

/**
 * Vloží znaky řetězce do množiny symbolů nad jednou hranou
 * @param os Symbol, do kterého se má přidat znak
 * @param s Řetězec symbolů, který se má vložit
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &os, string s)
{
	for(int i=0; i<s.length(); i++)
	{
		os.znaky.push_back(s[i]);
	}
	return os;
}

/**
 * Vloží jeden symbol do druhého: provede spojení dvou symbolů
 * @param novy Symbol, do kterého se má vložit další symbol
 * @param stary Symbol, který se má vkládat
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &novy, T_SYMBOL &stary)
{
	for(int i=0; i<stary.znaky.size(); i++)
	{
		novy += stary.znaky[i];
	}
	return novy;
}

/**
 * Vypíše řádek tabulky symbolů do streamu
 * @param os Stream, do kterého se má vypsat
 * @param str Řádek tabulky symbolů, který se má vypsat
 * @return ostream
 */
ostream & operator << (ostream &os, T_SYMBOL_TABLE_ROW &str)
{
	os << str.id << ":" << str.printId << ":" << (str.pouzity ? "aktivni" : "neaktiv") << ":" << *str.nazev;
	return os;
}

/**
 * Výpis tabulky symbolů
 * @param os
 * @param symbolTable
 * @return
 */
ostream & operator << (ostream &os, T_TABULKA_SYMBOLU &symbolTable)
{
	os << "Symbol table" << " (Velikost " << symbolTable.size() << ")" << endl;
	os << "----------------------" << endl;
	for(unsigned i=0; i<symbolTable.size(); i++)
	{
		os << *symbolTable[i] << endl;
	}
	os << "----------------------" << endl;
	return os;
}

/**
 * Invertuje velikost písmene z ASCII
 * @param c písmeno, jehož velikost se má invertovat
 * @return invertované písmeno
 */
char invertujPismeno(char c)
{
	if(c >= 'a' && c <= 'z') return (char)((unsigned)c-32);
	else if(c >= 'A' && c <= 'Z') return (char)((unsigned)c+32);
	else return c;
}

/**
 * Vloží symbol do tabulky symbolů
 * @param T_SPECIALNI s Symbol, se kterým se přechází
 * @return T_SYMBOL_TABLE_ROW* ukazatel na nově vytvořený symbol
 */
T_SYMBOL_TABLE_ROW *addToSymbolTable(T_SPECIALNI s)
{
	vector<T_SYMBOL_TABLE_ROW*>::iterator it = symbolTable.begin();
	while(it != symbolTable.end())
	{
		if( s == epsilon && *((*it)->nazev) == "epsilon" ) return *it;
		if( s == any && *((*it)->nazev) == "*" ) return *it;
		if( s == space && *((*it)->nazev) == "[ ]" ) return *it;
		it++;
	}
	T_SYMBOL_TABLE_ROW *str = new T_SYMBOL_TABLE_ROW;
	str->id = noveIdSymbolu++;
	str->nazev = new string;
	str->pouzity = true;
	str->symbol.minimum = -1;
	str->symbol.maximum = -1;
	switch(s)
	{
		case epsilon:
		{
			*str->nazev = "epsilon";
			str->symbol += 'e';
			str->pouzity = false;
		} break;
		case any:
		{
			*str->nazev = "*";
			unsigned asciiEnd = HIGH_ASCII;
			if(config.lowAscii == 1) asciiEnd = LOW_ASCII; else asciiEnd = HIGH_ASCII;
			for(unsigned i=0; i<=asciiEnd; i++)
			{
				//if(i == 13) continue; // default: except DOTALL
				if(i == 13 || i == 10)
				{
					continue;
				}
				str->symbol.znaky.push_back(i);
			}
			if(options.newline == LF) str->symbol += chLF;
			if(options.newline == CR) str->symbol += chCR;
			if(options.newline == ANYCRLF) { str->symbol += chCR; str->symbol += chLF; }
			if(options.newline == ANY) { str->symbol += chCR; str->symbol += chLF; }
		} break;
		case space:
		{
			*str->nazev = "[ ]"; str->symbol += ' ';
		} break;
		case p_alnum:
		{
			*str->nazev = "[:alnum:]"; str->symbol = posixClasses.alnum;
		} break;
		case p_alpha:
		{
			*str->nazev = "[:alpha:]"; str->symbol = posixClasses.alpha;
		} break;
		case p_upper:
		{
			*str->nazev = "[:upper:]"; str->symbol = posixClasses.lower;
		} break;
		case p_lower:
		{
			*str->nazev = "[:lower:]"; str->symbol = posixClasses.upper;
		} break;
		case p_ascii:
		{
			*str->nazev = "[:ascii:]"; str->symbol = posixClasses.ascii;
		} break;
		case p_blank:
		{
			*str->nazev = "[:blank:]"; str->symbol = posixClasses.blank;
		} break;
		case p_space:
		{
			*str->nazev = "[:space:]"; str->symbol = posixClasses.space;
		} break;
		case p_word:
		{
			*str->nazev = "[:word:]"; str->symbol = posixClasses.word;
		} break;
		case p_cntrl:
		{
			*str->nazev = "[:cntrl:]"; str->symbol = posixClasses.cntrl;
		} break;
		case p_graph:
		{
			*str->nazev = "[:graph:]"; str->symbol = posixClasses.graph;
		} break;
		case p_punct:
		{
			*str->nazev = "[:punct:]"; str->symbol = posixClasses.punct;
		} break;
		case p_print:
		{
			*str->nazev = "[:print:]"; str->symbol = posixClasses.print;
		} break;
		case p_xdigit:
		{
			*str->nazev = "[:xdigit:]"; str->symbol = posixClasses.xdigit;
		} break;
		case bs_digit:
		{
			*str->nazev = "\\d"; str->symbol = backslashClasses.digit;
		} break;
		case bs_ndigit:
		{
			*str->nazev = "\\D"; str->symbol = backslashClasses.Ndigit;
		} break;
		case bs_hwhitesp:
		{
			*str->nazev = "\\h"; str->symbol = backslashClasses.hWhitespace;
		} break;
		case bs_nhwhitesp:
		{
			*str->nazev = "\\H"; str->symbol = backslashClasses.NhWhitespace;
		} break;
		case bs_vwhitesp:
		{
			*str->nazev = "\\v"; str->symbol = backslashClasses.vWhitespace;
		} break;
		case bs_nvwhitesp:
		{
			*str->nazev = "\\V"; str->symbol = backslashClasses.NvWhitespace;
		} break;
		case bs_whitesp:
		{
			*str->nazev = "\\s"; str->symbol = backslashClasses.whitespace;
		} break;
		case bs_nwhitesp:
		{
			*str->nazev = "\\S"; str->symbol = backslashClasses.Nwhitespace;
		} break;
		case bs_wordchar:
		{
			*str->nazev = "\\w"; str->symbol = backslashClasses.wordchar;
		} break;
		case bs_nwordchar:
		{
			*str->nazev = "\\W"; str->symbol = backslashClasses.Nwordchar;
		} break;
		case bsr:
		{
			*str->nazev = "BSR"; str->symbol += "\r\n\f"; str->symbol += (char)0x0b;
		} break;
		case nop:
		{
			*str->nazev = "nop";
			str->symbol += 'n';
		} break;
		case cr:
		{
			*str->nazev = "CR"; str->symbol += "\r";
		} break;
		case lf:
		{
			*str->nazev = "LF"; str->symbol += "\n";
		} break;
		case eoi:
		{
			*str->nazev = "EOI";
			str->symbol += "";
		} break;
		case all:
		{
			*str->nazev = "*";
			unsigned asciiEnd = HIGH_ASCII;
			if(config.lowAscii == 1) asciiEnd = LOW_ASCII; else asciiEnd = HIGH_ASCII;
			for(unsigned i=0; i<=asciiEnd; i++)
			{
				str->symbol.znaky.push_back(i);
			}
		} break;
	}
	symbolTable.push_back(str);
	return str;
}

/**
 * Vloží symbol do tabulky symbolů
 */
T_SYMBOL_TABLE_ROW *addToSymbolTable(char c)
{
	T_SYMBOL_TABLE_ROW *str = new T_SYMBOL_TABLE_ROW;
	str->id = noveIdSymbolu++;
	str->pouzity = true;
	str->symbol.minimum = -1;
	str->symbol.maximum = -1;
	str->nazev = new string;
	*str->nazev = c;
	str->symbol += c;
	if( optionsStack.front().caseless == true ) str->symbol += invertujPismeno(c);
	symbolTable.push_back(str);
	return str;
}

/**
 * Vloží symbol do tabulky symbolů
 */
T_SYMBOL_TABLE_ROW *addToSymbolTable(int i)
{
	T_SYMBOL_TABLE_ROW *str = new T_SYMBOL_TABLE_ROW;
	str->id = noveIdSymbolu++;
	str->pouzity = true;
	str->symbol.minimum = -1;
	str->symbol.maximum = -1;
	str->nazev = new string;
	char tmp[2];
	sprintf(tmp, "%i", i);
	*str->nazev = tmp;
	str->symbol += tmp[0];
	symbolTable.push_back(str);
	return str;
}

T_SYMBOL_TABLE_ROW * duplikujStr(T_SYMBOL_TABLE_ROW *stary)
{
	T_SYMBOL_TABLE_ROW *novy = new T_SYMBOL_TABLE_ROW;
	novy->id = noveIdSymbolu++;
	novy->nazev = new string(*stary->nazev);
	novy->symbol = stary->symbol;
	novy->pouzity = true;
	novy->symbol.minimum = stary->symbol.minimum;
	novy->symbol.maximum = stary->symbol.maximum;
	symbolTable.push_back(novy);
	return novy;
}

T_SYMBOL_TABLE_ROW & operator += (T_SYMBOL_TABLE_ROW &novy, T_SYMBOL_TABLE_ROW &stary)
{
	*novy.nazev += "|" + *stary.nazev;
	novy.symbol += stary.symbol;

	return novy;
}

T_SYMBOL_TABLE_ROW * rozsahSymbolu(T_SYMBOL_TABLE_ROW * start, T_SYMBOL_TABLE_ROW * end)
{
	T_SYMBOL_TABLE_ROW * novy = addToSymbolTable((char)start->symbol.znaky[0]);
	*novy->nazev += "-";
	unsigned int i=(unsigned char)start->symbol.znaky[0];
	for(i; i<=end->symbol.znaky[0]; i++ )
	{
		novy->symbol += i;
		if( optionsStack.front().caseless == true ) { novy->symbol += invertujPismeno(i); }
	}
	*novy->nazev += end->symbol.znaky[0];
	return novy;
}

void vytvorDoplnek(T_SYMBOL &novy, T_SYMBOL &stary)
{
	unsigned asciiEnd = HIGH_ASCII;
	if(config.lowAscii == 1) asciiEnd = LOW_ASCII; else asciiEnd = HIGH_ASCII;
	for(unsigned i=0; i<=asciiEnd; i++)
	{
		unsigned j;
		for(j=0; j<stary.znaky.size(); j++)
		{
			if( (unsigned)stary.znaky[j] == i ) break;
		}
		if( j == stary.znaky.size() )
		{
			novy.znaky.push_back((char)i);
		}
	}
}

void caseInsesitive(T_TABULKA_SYMBOLU &tabulka)
{
	for(unsigned i=0; i<tabulka.size(); i++)
	{
		if( tabulka[i]->pouzity == false ) continue;
		unsigned delka = tabulka.at(i)->symbol.znaky.size();
		for(unsigned j=0; j<delka; j++)
		{
			if(tabulka.at(i)->symbol.znaky[j] >= 'a' && tabulka.at(i)->symbol.znaky[j] <= 'z' || tabulka.at(i)->symbol.znaky[j] >= 'A' && tabulka.at(i)->symbol.znaky[j] <= 'Z')
			{
				tabulka.at(i)->symbol.znaky.push_back(invertujPismeno(tabulka.at(i)->symbol.znaky[j]));
			}
		}
	}
}

void dotAll(T_TABULKA_SYMBOLU &tabulka)
{
	for(unsigned i=0; i<tabulka.size(); i++)
	{
		if( tabulka[i]->pouzity == false ) continue;
		if(*(tabulka.at(i)->nazev) == "*" )
		{
			tabulka.at(i)->symbol += chCR;
			tabulka.at(i)->symbol += chLF;
		}
	}
}

void setOption(bool hodnota, string klic)
{
	// pokud poslední sada nastavení není v režimu nastavování, zkopíruje se hlavní sada přepínačů (z kořene stromu)
	if( optionsStack.front().editable == false )
	{
		optionsStack.push_front(optionsStack.back());
		optionsStack.front().editable = true;
	}

	if(klic == "caseless") optionsStack.front().caseless = hodnota;
	if(klic == "extended") optionsStack.front().extended = hodnota;
	if(klic == "multiline") optionsStack.front().multiline = hodnota;
	if(klic == "editable") optionsStack.front().editable = hodnota;
}

ostream & operator << (ostream &os, T_OPTIONS &options)
{
	os << "Config" << endl;
	os << "------" << endl;
	os << "- caseless=" << options.caseless << endl;
	os << "- multiline=" << options.multiline << endl;
	os << "- newline=" << options.newline << endl;
}

ostream & operator << (ostream &os, T_NEWLINE &nl)
{
	switch(nl)
	{
		case ANY:
			os << "ANY";
			break;
		case CR:
			os << "CR";
			break;
		case LF:
			os << "LF";
			break;
		case CRLF:
			os << "CRLF";
			break;
		case ANYCRLF:
			os << "ANYCRLFCR";
			break;
	}
}

void optimizeSymbolTable()
{
	unsigned id=0;
	for(unsigned i=0; i<symbolTable.size(); i++)
	{
		if( symbolTable[i]->pouzity == true ) symbolTable[i]->printId = id++;
		else symbolTable[i]->printId = 0;
	}
}
