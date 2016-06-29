#include "stdlib.h"
#include "map"
#include "nodes.hpp"
#include "interface.h"

#define NFA_FAIL 3

using namespace std;

extern stack<T_FA *> fas;

// id zlu
unsigned noveIdUzlu;

T_SEZNAM_SOUSEDU seznamSousedu;

T_OPAKOVANI opakovani;

vector<T_PREVEDENY_UZEL> prevodUzlu;

extern T_CONFIG config;

/**
 * Vytvoří nový uzel NFA
 */
T_FANODE *vytvorUzel()
{
	T_FANODE *uzel = new T_FANODE;
	uzel->id = noveIdUzlu;
	uzel->visited = false;
	noveIdUzlu++;
	seznamSousedu.push_back(uzel); // vloží uzel do tabulky
	return uzel;
}

string osetriVystup(string s)
{
	string str;
	for(int i=0; i<s.length(); i++)
	{
		if( s[i] == '\\' ) str.push_back('\\');
		if( s[i] == '$' ) str.push_back('\\');
		if( (int)s[i] < 32 ) { char buf[6]; sprintf(buf, "0x%02x", s[i]); str.append(buf); continue; }
		str.push_back(s[i]);
	}
	return str;
}

ostream & operator << (ostream &os, T_SEZNAM_SOUSEDU &seznamSousedu)
{
	if( fas.empty() ) return os;

	os << "digraph NFA {" << endl;
	os << "rankdir=LR;" << endl;
	os << "label=\"PCRE pattern: " << osetriVystup(config.inputPattern) << "\"" << endl;
	T_FA *fa = fas.top();
	os << "node [shape = doublecircle]; " << fa->end->id << endl;
	os << "node [shape = circle];" << endl;
	os << "-1 [style=invis]" << endl;
	os << "-1 -> " << fa->start->id << endl;
	for(unsigned i=0; i<seznamSousedu.size(); i++)
	{
		unsigned rodic = seznamSousedu[i]->id;
		for(list<T_SEZNAM_SOUSEDU_NODE>::iterator it = seznamSousedu[i]->seznamSousedu.begin(); it != seznamSousedu[i]->seznamSousedu.end(); it++)
		{
			if( config.ccSymbols == 1 && (it->symbolTableRow->symbol.minimum != -1 || it->symbolTableRow->symbol.maximum != -1) ) os << rodic << " -> " << it->soused->id << " [label=\"" << "#" << it->symbolTableRow->symbol.minimum << "#" << it->symbolTableRow->symbol.maximum << "#" << osetriVystup(*it->symbolTableRow->nazev) << "\"]" << endl;
			else os << rodic << " -> " << it->soused->id << " [label=\"" << osetriVystup(*it->symbolTableRow->nazev) << "\"]" << endl;
		}
	}
	os << "}" << endl;
	return os;
}

/**
 * Spojí hranou dva uzly
 * @param node1 Počáteční uzel
 * @param node2 Koncový uzel
 * @param s Symbol, se kterým se přejde mezi uzly
 */
void spojHranou(T_FANODE *node1, T_FANODE *node2, T_SYMBOL_TABLE_ROW *str)
{
	T_SEZNAM_SOUSEDU_NODE sousedni;
	sousedni.symbolTableRow = str;
	sousedni.soused = node2;

	node1->seznamSousedu.push_back(sousedni);
	// metoda vkládající seznamy sousedů podle abecedy
	/*list<T_SEZNAM_SOUSEDU_NODE>::iterator it = node1->seznamSousedu.begin();
	while(it != node1->seznamSousedu.end())
	{
		if( *it->symbolTableRow->nazev > *str->nazev ) break;
		it++;
	}
	node1->seznamSousedu.insert(it, sousedni);*/

	if( *str->nazev == "*" && (options.newline == ANYCRLF || options.newline == CRLF || options.newline == ANY) )
	{
		T_FANODE * node3 = vytvorUzel();
		spojHranou(node1, node3, cr);
		spojHranou(node3, node2, lf);
	}
}

void spojHranou(T_FANODE *node1, T_FANODE *node2, T_SPECIALNI s)
{
	// při vypnutém exportu EOF symbolů se nespojí pomocí EOF
	if( s == eoi && config.eofExport == false )
	{
		spojHranou(node1, node2, epsilon);
	}
	else
	{
		T_SYMBOL_TABLE_ROW * str = addToSymbolTable(s);
		spojHranou(node1, node2, str);
	}

	if( s == eoi && optionsStack.front().multiline == true )
	{
		T_FANODE *node3 = vytvorUzel();
		if( optionsStack.front().newline == CR )
		{
			spojHranou(node1, node3, cr);
			spojHranou(node3, node2, epsilon);
		}
		if( optionsStack.front().newline == LF )
		{
			spojHranou(node1, node3, lf);
			spojHranou(node3, node2, epsilon);
		}
		if( optionsStack.front().newline == CRLF )
		{
			spojHranou(node1, node3, cr);
			spojHranou(node3, node2, lf);
		}
	}

	/*if( s == any && (options.newline == ANYCRLF || options.newline == CRLF) )
	{
		T_FANODE * node3 = vytvorUzel();
		spojHranou(node1, node3, cr);
		spojHranou(node3, node2, lf);
	}*/
}

/**
 * Spojí dva automaty do nového, který vrátí
 * @param T_FA* fa1 První automat
 * @param T_FA* fa2 Druhý automat
 * @return T_FA* Nový automat
 */
T_FA *spoj_automaty(T_FA *fa1, T_FA *fa2)
{
	spojHranou(fa1->end, fa2->start, epsilon);

	T_FA * fa = new T_FA;

	fa->start = fa1->start;
	fa->end = fa2->end;

	return fa;
}

/**
 * Duplikuje uzel včetně seznamu sousedů
 * - posledni uzel urcuje zarazku, až po který uzel se má kopírovat seznam sousedů
 * @param T_FANODE* stary
 * @param T_FANODE* posledni
 * @return T_FANODE* Duplikovaný uzel
 */
T_FANODE * duplikujNode(T_FANODE* stary, T_FANODE* posledni)
{
	vector<T_PREVEDENY_UZEL>::iterator it = prevodUzlu.begin();
	T_FANODE * novy = NULL;
	while(it != prevodUzlu.end())
	{
	   if( it->staryUzel == stary )
	   {
		novy = it->novyUzel;
		  break;
	   }
	   it++;
	}
	if( novy == NULL )
	{
		novy = vytvorUzel();
		T_PREVEDENY_UZEL prevedenyUzel;
		prevedenyUzel.staryUzel = stary;
		prevedenyUzel.novyUzel = novy;
		prevodUzlu.push_back(prevedenyUzel);
		novy->seznamSousedu = stary->seznamSousedu;
		list<T_SEZNAM_SOUSEDU_NODE>::iterator it = novy->seznamSousedu.begin();
		while( it != novy->seznamSousedu.end() )
		{
			// pokud duplikuji poslední uzel a chtěl bych do seznamu sousedů přidat uzel až za posledním uzlem
			if( stary == posledni && it->soused->id <= stary->id || stary != posledni)
			{
				it->soused = duplikujNode(it->soused, posledni);
				it++;
			}
			else
			{
				it = novy->seznamSousedu.erase(it);
			}
		}
	}
	return novy;
}

void odstranNode(T_FANODE * node, map<int, bool> &prosle)
{
	if( node == NULL ) return;
	if( node->seznamSousedu.empty() ) { node = NULL; return; }

	prosle[node->id] = true;
	// odstraní se rekurzivně podčást automatu počínaje tímto uzlem dále
	list<T_SEZNAM_SOUSEDU_NODE>::iterator it = node->seznamSousedu.begin();
	while( it != node->seznamSousedu.end() )
	{
		if( it->soused->id == node->id ) { it++; continue; } // cyklus sám nad sebou
		if( prosle[it->soused->id] == true ) { it++; continue; } // již mazaný uzel
		odstranNode(it->soused, prosle);
		it++;
	}

	// smaže seznam sousedů uzlu
	vector<T_FANODE*>::iterator it2 = seznamSousedu.begin();
	while( it2 != seznamSousedu.end() )
	{
		if( (*it2)->id == node->id )
		{
			seznamSousedu.erase(it2);
			break;
		}
		it2++;
	}
	// smaže samotný uzel
	//delete node;
	node = NULL;
	return;
}

void odstranFA(T_FA *fa)
{
	map<int, bool> prosle;
	odstranNode(fa->start, prosle);
}

/**
 * Duplikuje konečný automat včetně všech jeho uzlů
 * @param Konečný automat určený k duplikování
 * @return Duplikovaný konečný automat
 */
T_FA * duplikujFA(T_FA *fa)
{
	prevodUzlu.clear();
	T_FA *novy = new T_FA;
	novy->start = duplikujNode(fa->start, fa->end);
	novy->end = duplikujNode(fa->end, fa->end);
	prevodUzlu.clear();
	return novy;
}

/**
 * Zopakuje předaný automat podle předané opakovací operace
 * @param fa Automat, který má být opakován
 * @param operace Operace opakování
 * @return Nový automat
 */
T_FA * vytvorOpakovani(T_FA *fa, T_OPERACE operace)
{
	switch(operace)
	{
		case zeromore:
		{
			T_FANODE * fanode1 = vytvorUzel();
			T_FANODE * fanode2 = vytvorUzel();
			spojHranou(fanode1, fa->start, epsilon);
			spojHranou(fa->end, fanode2, epsilon);
			spojHranou(fa->end, fa->start, epsilon);
			spojHranou(fanode1, fanode2, epsilon);
			fa->start = fanode1;
			fa->end = fanode2;
		}
		break;
		case onemore:
		{
			spojHranou(fa->end, fa->start, epsilon);
		}
		break;
		case zeroone:
		{
			spojHranou(fa->start, fa->end, epsilon);
		}
		break;
		case repeating:
		{
			T_FA * fa_skladany = new T_FA;
			T_FA * fa2;
			// automat obsahuje pouze 2 stavy a jeden přechod mezi nimi
			if( config.ccSymbols == 1 && fa->start->seznamSousedu.size() == 1 && fa->start->seznamSousedu.back().soused->id == fa->end->id )
			{
				fa->start->seznamSousedu.back().symbolTableRow->symbol.minimum = opakovani.minimum;
				fa->start->seznamSousedu.back().symbolTableRow->symbol.maximum = opakovani.maximum;
			}
			else
			{
				// opakování {0}, {0,}, {0,x}
				if( opakovani.minimum == 0 )
				{
					T_FANODE *node= vytvorUzel();
					fa_skladany->start = node;
					fa_skladany->end = node;
				}
				// opakování {2,}, {2,x} || {2}, {2,2}
				if( opakovani.minimum > 0 || opakovani.minimum == opakovani.maximum && opakovani.minimum != 0 || opakovani.maximum > 0 )
				{
					int opakovat = opakovani.maximum > opakovani.minimum ? opakovani.maximum : opakovani.minimum;
					for(int i=0; i<opakovat; i++)
					{
						fa2 = duplikujFA(fa);
						if( i >= opakovani.minimum ) spojHranou(fa2->start, fa2->end, epsilon);
						if( opakovani.minimum != 0 && i == 0 ) fa_skladany = fa2;
						else fa_skladany = spoj_automaty(fa_skladany, fa2);
					}
				}
				// opakování {x,}
				if( opakovani.maximum == -1 )
				{
                    T_FA * fa_3 = new T_FA;
                    T_FANODE * fanode1 = vytvorUzel();
                    
					fa2 = duplikujFA(fa);
					spojHranou(fa2->end, fa2->start, epsilon);
// 					spojHranou(fa2->start, fa2->end, epsilon);
// 					fa_skladany = spoj_automaty(fa_skladany, fa2);
                    spojHranou(fa_skladany->end, fa2->start, epsilon);
                    spojHranou(fa2->end, fanode1, epsilon);
                    fa2->end = fanode1;
                    spojHranou(fa_skladany->end, fa2->end, epsilon);
                    fa_3->start = fa_skladany->start;
                    fa_3->end = fa2->end;
                    fa_skladany = fa_3;
				}
				odstranFA(fa);
				fa->start = fa_skladany->start;
				fa->end = fa_skladany->end;
			}
		}
		break;
	}
	return fa;
}
