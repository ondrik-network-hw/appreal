/*
 * File:   symbols.hpp
 * Author: milan
 *
 * Created on 13. květen 2011, 22:48
 */

#ifndef SYMBOLS_HPP
#define	SYMBOLS_HPP

#include <stdio.h>
#include <iostream>
#include <list>
#include <vector>
#include <string>
#include <stack>

#define chLF 0x0a
#define chCR 0x0d

#define LOW_ASCII 127 // interval <0;LOW_ASCII>
#define HIGH_ASCII 255 // interval <0;HIGH_ASCII>

using namespace std;

/**
 * Speciální symboly se kterými se přechází mezi stavy
*/
typedef enum specialni
{
	epsilon,
	any,
	space,
	p_alnum,
	p_alpha,
	p_lower,
	p_upper,
	p_digit,
	p_ascii,
	p_blank,
	p_space,
	p_word,
	p_cntrl,
	p_graph,
	p_print,
	p_punct,
	p_xdigit,
	bs_digit,
	bs_ndigit,
	bs_hwhitesp,
	bs_nhwhitesp,
	bs_vwhitesp,
	bs_nvwhitesp,
	bs_whitesp,
	bs_nwhitesp,
	bs_wordchar,
	bs_nwordchar,
	bsr,
	nop,
	cr,
	lf,
	eoi,
	all
} T_SPECIALNI;

typedef enum newline
{
	CR,
	LF,
	CRLF,
	ANYCRLF,
	ANY
} T_NEWLINE;

typedef struct options
{
    bool caseless;
    bool multiline;
    bool assertStart;	/**< Příznak, zda výraz začíná se začátkem vstupu */
    bool assertEnd;	/**< Příznak, zda výraz končí s koncem vstupu */
	bool extended; /**< Příznak, zda je výraz zkompilován s volbou PCRE_EXTENDED */
	T_NEWLINE newline; /**< Nastavení nových řádků, default LF, možné CR, LF, CRLF, ANYCRLF, ANY */
	bool editable; /**< Příznak, zda je možné změnit nastavení sady přepínačů */
} T_OPTIONS;

extern T_OPTIONS options;

typedef list<T_OPTIONS> T_OPTIONS_STACK;

extern T_OPTIONS_STACK optionsStack;

/**
 * Nastavi aktualni konfiguraci PCRE
 * Ohlida si, zda je na zasobniku editovatelna konfigurace
 * @param bool hodnota Nová hodnota klice
 * @param string klic Nazev klice, kteremu se ma zmenithodnota
 * @return void
 */
void setOption(bool hodnota, string klic);

/**
 * Z menšího písmena udělá větší a obráceně
 * @param c
 * @return invertované písmeno
 */
char invertujPismeno(char c);

/**
 * Množina symbolů, se kterými se může přecházet nad hranou
 */
typedef struct symboly
{
	vector<unsigned char> znaky; /**< Znaky symbolu */
	int minimum;
	int maximum;
} T_SYMBOL;

extern T_SYMBOL abeceda;

/**
 * POSIX třídy znaků
 */
typedef struct posixClasses
{
    T_SYMBOL alnum;
    T_SYMBOL alpha;
    T_SYMBOL lower;
    T_SYMBOL upper;
    T_SYMBOL digit;
    T_SYMBOL ascii;
    T_SYMBOL blank;
    T_SYMBOL space;
    T_SYMBOL word;
    T_SYMBOL cntrl;
    T_SYMBOL graph;
    T_SYMBOL print;
    T_SYMBOL punct;
    T_SYMBOL xdigit;
} T_POSIX_CLASSES;

extern T_POSIX_CLASSES posixClasses;

/**
 * Backslash třídy znaků
 */
typedef struct backslashClasses
{
    T_SYMBOL digit;
    T_SYMBOL Ndigit;
    T_SYMBOL hWhitespace;
    T_SYMBOL NhWhitespace;
    T_SYMBOL whitespace;
    T_SYMBOL Nwhitespace;
    T_SYMBOL vWhitespace;
    T_SYMBOL NvWhitespace;
    T_SYMBOL wordchar;
    T_SYMBOL Nwordchar;
} T_BACKSLASH_CLASSES;

extern T_BACKSLASH_CLASSES backslashClasses;

/**
 * Vloží symbol do množiny symbolů nad jednou hranou
 * @param os Symbol, do kterého se má přidat znak
 * @param c Znak, který se má vložit
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &os, char c);

/**
 * Vloží znaky řetězce do množiny symbolů nad jednou hranou
 * @param os Symbol, do kterého se má přidat znak
 * @param s Řetězec symbolů, který se má vložit
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &os, string s);

/**
 * Vloží jeden symbol do druhého: provede spojení dvou symbolů
 * @param novy Symbol, do kterého se má vložit další symbol
 * @param stary Symbol, který se má vkládat
 * @return T_SYMBOL
 */
T_SYMBOL & operator +=(T_SYMBOL &novy, T_SYMBOL &stary);

/**
 * Symboly, se kterými se může přecházet mezi stavy
*/
typedef struct symbolTableRow
{
	unsigned id;		/**< Číselné ID symbolu */
	string *nazev;		/**< Název symbolu, např. nad přechod mezi stavy */
	T_SYMBOL symbol;	/**< Vlastní množina znaků */
	bool pouzity;		/**< Příznak, zda je řádek tabulky použivaný, či nikoli */
	unsigned printId;	/**< Číselné ID symbolu určené pro zveřejnění. */
} T_SYMBOL_TABLE_ROW;

/**
 * Vypíše řádek tabulky symbolů do streamu
 * @param os Stream, do kterého se má vypsat
 * @param str Řádek tabulky symbolů, který se má vypsat
 * @return ostream
 */
ostream & operator << (ostream &os, T_SYMBOL_TABLE_ROW &str);

/**
 * Datový typ tabulky symbolů
 */
typedef vector<T_SYMBOL_TABLE_ROW*> T_TABULKA_SYMBOLU;

/**
 * Tabulka symbolů
*/
extern T_TABULKA_SYMBOLU symbolTable; // tabulka symbolu
extern stack<T_SYMBOL_TABLE_ROW*> strStack; // zasobnik symbolu pro převod z derivačního stromu

/**
 * Výpis tabulky symbolů
 * @param os
 * @param symbolTable
 * @return
 */
ostream & operator << (ostream &os, T_TABULKA_SYMBOLU &symbolTable);

/**
 * Nové ID symbolu tabulky, inkrementované po každém vložení do tabulky
 */
extern unsigned noveIdSymbolu;

/**
 * Vloží symbol do tabulky symbolů
 * @param T_SPECIALNI s Symbol, se kterým se přechází
 * @return T_SYMBOL_TABLE_ROW reference na nově vytvořený symbol
 */
T_SYMBOL_TABLE_ROW *addToSymbolTable(T_SPECIALNI s);

/**
 * Vloží symbol do tabulky symbolů
 */
T_SYMBOL_TABLE_ROW *addToSymbolTable(char c);

T_SYMBOL_TABLE_ROW *addToSymbolTable(int i);

T_SYMBOL_TABLE_ROW & operator += (T_SYMBOL_TABLE_ROW &novy, T_SYMBOL_TABLE_ROW &stary);

/**
 * Vytvoří rozsah symbolů mezi startovním a koncovým symbolem
 * @param start
 * @param end
 * @return
 */
T_SYMBOL_TABLE_ROW * rozsahSymbolu(T_SYMBOL_TABLE_ROW * start, T_SYMBOL_TABLE_ROW * end);

void vytvorDoplnek(T_SYMBOL &, T_SYMBOL &);

T_SYMBOL_TABLE_ROW * duplikujStr(T_SYMBOL_TABLE_ROW *stary);

void caseInsesitive(T_TABULKA_SYMBOLU &);
void dotAll(T_TABULKA_SYMBOLU &);

ostream & operator << (ostream &os, T_OPTIONS &options);
ostream & operator << (ostream &os, T_NEWLINE &nl);

void optimizeSymbolTable();

#endif	/* SYMBOLS_HPP */
