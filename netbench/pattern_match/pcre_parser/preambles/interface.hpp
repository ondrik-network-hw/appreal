/**
 * Rozhraní aplikace parseru PCRE
 *
 * @date 2011-06-18
 * @author Milan Pála (xpalam00@stud.fit.vutbr.cz)
 */

#ifndef __INTERFACE_HEADER
#define __INTERFACE_HEADER

/**
 * Struktura obsahující konfigurační direktivy zadané uživatelem při spuštění
 */
typedef struct configStruct
{
	char inputPattern[262144];	/**< vstupní vzor PCRE */
	char outputMsfmFile[1024];	/**< výstupní soubor s NFA automatem formátu MSFM */
	char outputDotFile[1024];	/**< výstupní soubor grafu tvořeného automatu ve formátu DOT */
	char charExport[4];			/**< výstupní formát při exportu symbolů (dec, hex) */
	unsigned strict;			/**< zapne varovaní, pokud je chování parseru odlišné od PCRE specifikace */
	unsigned lowAscii;			/**< pouze spodní polovina ASCII tabulky */
	unsigned ccSymbols;			/**< mají se counting-constraints předat jako symbol, nebo rozgenerovat */
	unsigned eofExport;			/**< má se pro výraz /a$/ exportovat přechod se symbolem EOF */
} T_CONFIG;

/**
 * Procedura provádějící inicializaci před začátkem parsování vzoru
 * @param T_CONFIG Struktura obsahujicí konfigurační direktivy pro parser
 */
void module_init(T_CONFIG);

/**
 * Procedura provádějící post-operece po skončení práce parseru
 * @param int Návratová hodnota funkce parse
 */
void module_exit(int);
