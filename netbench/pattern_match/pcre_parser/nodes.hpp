/*
 * File:   nodes.hpp
 * Author: milan
 *
 * Created on 14. květen 2011, 19:41
 */

#ifndef NODES_HPP
#define	NODES_HPP

#include <stack>
#include <list>

#include "symbols.hpp"

using namespace std;

struct fanode;

/**
 * Operace, podle kterých se řídí další zpracování automatů
*/
typedef enum operace
{
	zeromore,	// *
	onemore,	// +
	zeroone,	// ?
	repeating	// {x,y}
} T_OPERACE;

/**
 * Uzel v seznamu sousedu jednoho uzlu
*/
typedef struct seznamSouseduNode
{
	T_SYMBOL_TABLE_ROW * symbolTableRow; /**< symbol, se kterym se prechazi */
	fanode * soused; /**< odkaz do seznamu sousedu */
} T_SEZNAM_SOUSEDU_NODE;

/**
 * Uzel výsledného automatu
 * - obsahuje identifikátor
 * - obsahuje seznam sousedů
 */
typedef struct fanode
{
	unsigned id; // identifikátor uzlu
	list<T_SEZNAM_SOUSEDU_NODE> seznamSousedu;
	bool visited; /**< příznak, zda již byl při průchodu grafem uzel navštíven */
} T_FANODE;


// reprezentace FA: pocatecni a koncovy uzel
typedef struct farepre
{
	T_FANODE *start;	// pocatecni uzel automatu
	T_FANODE *end;	// koncovy uzel automatu
} T_FA;

// seznam sousedu jednoho uzlu NFA
typedef list<T_FANODE>::iterator strStackIterator; // ukazatel na uzel NFA
typedef list<T_FANODE> FAnodeList; // uzel NFA

typedef vector<T_FANODE*> T_SEZNAM_SOUSEDU;
extern T_SEZNAM_SOUSEDU seznamSousedu; // seznam sousedu

// id zlu
extern unsigned noveIdUzlu;

/**
 * Vytvoří nový uzel NFA
 */
T_FANODE *vytvorUzel();

ostream & operator << (ostream &os, T_SEZNAM_SOUSEDU &seznamSousedu);

/**
 * Spojí hranou dva uzly
 * @param node1 Počáteční uzel
 * @param node2 Koncový uzel
 * @param s Symbol, se kterým se přejde mezi uzly
 */
void spojHranou(T_FANODE *node1, T_FANODE *node2, T_SYMBOL_TABLE_ROW *str);

void spojHranou(T_FANODE *node1, T_FANODE *node2, T_SPECIALNI s);

/**
 * Spojí dva automaty do nového, který vrátí
 * @param T_FA* fa1 První automat
 * @param T_FA* fa2 Druhý automat
 * @return T_FA* Nový automat
 */
T_FA *spoj_automaty(T_FA *fa1, T_FA *fa2);

typedef struct opakovani
{
	int minimum;
	int maximum;
} T_OPAKOVANI;

extern T_OPAKOVANI opakovani;

typedef struct prevedenyUzel
{
	T_FANODE * staryUzel;
	T_FANODE * novyUzel;
} T_PREVEDENY_UZEL;

/**
 * Duplikuje uzel včetně seznamu sousedů
 * - posledni uzel urcuje zarazku, až po který uzel se má kopírovat seznam sousedů
 * @param T_FANODE* stary
 * @param T_FANODE* posledni
 * @return T_FANODE* Duplikovaný uzel
 */
T_FANODE * duplikujNode(T_FANODE* stary, T_FANODE* posledni);

void odstranNode(T_FANODE * node);

void odstranFA(T_FA *fa);

/**
 * Duplikuje konečný automat včetně všech jeho uzlů
 * @param Konečný automat určený k duplikování
 * @return Duplikovaný konečný automat
 */
T_FA * duplikujFA(T_FA *fa);

/**
 * Zopakuje předaný automat podle předané opakovací operace
 * @param fa Automat, který má být opakován
 * @param operace Operace opakování
 * @return Nový automat
 */
T_FA * vytvorOpakovani(T_FA *fa, T_OPERACE operace);

string osetriVystup(string s);

#endif	/* NODES_HPP */

