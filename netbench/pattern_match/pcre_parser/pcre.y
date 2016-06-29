/**
 * Grammar and semantic analyzer for PCRE
 * - input for the bison utility, use: bison -d pcre.y
 */
%{
#include <iostream>
#include <fstream>
#include <sstream>
#include <err.h>
#include <stdio.h>
#include "debug.hpp"
#include "interface.h"

#define DEBUG_HEADER "yacc"
extern int debug;

using namespace std;

int yylex (void);
void yyerror(char *);
void yyrestart(FILE *);

%}

%token LBRA RBRA INT COMMA LBOX RBOX SLASH LPAR RPAR ANY ZEROONE ONEMORE
%token ZEROMORE DASH OR ASCII CHARCLASS2VALUE
%token EOL BOL SPACE
%token UTF8 UCP MODIF_CASELESS MODIF_MULTILINE MODIF_DOTALL MODIF_EXTENDED OPTION MODIF_DUPNAMES MODIF_UNGREEDY MODIF_R MODIF_O MODIF_P MODIF_B
%token OPT_CR OPT_LF OPT_CRLF OPT_ANYCRLF OPT_ANY_NEWLINE
%token DECDIGIT NDECDIGIT HWHITESPACE NHWHITESPACE WHITESPACE NWHITESPACE VWHITESPACE NVWHITESPACE WORDCHAR NWORDCHAR
%token P_ALNUM P_ALPHA P_ASCII P_BLANK P_CNTRL P_DIGIT P_GRAPH P_LOWER P_PRINT P_PUNCT P_SPACE P_UPPER P_WORD P_XDIGIT
%token NP_ALNUM NP_ALPHA NP_ASCII NP_BLANK NP_CNTRL NP_DIGIT NP_GRAPH NP_LOWER NP_PRINT NP_PUNCT NP_SPACE NP_UPPER NP_WORD NP_XDIGIT
%token HEX OCTAL
%token TAB CR LF FF ESC BEL CONTROLX BSR RESET ONEBYTE
%token WORDBOUNDARY NWORDBOUNDARY STARTSUBJECT ENDSUBJECT OENDSUBJECT FIRSTPOSITION
%token CAPTURING_NON CAPTURING_NONRESET CAPTURING_ATOMIC CAPTURING_COMMENT CAPTURING_NEGBEHIND CAPTURING_POSBEHIND CAPTURING_NEGAHEAD CAPTURING_POSAHEAD
%token CAPTURING_NAMED CAPTURING_NAMED_END
%token CHALSTART CHALEND
%token BACKREFERENCE NAMED_BACKREFERENCE NAMED_BACKREFERENCE_END
%token SUBROUTINE_ALL SUBROUTINE_NAME SUBROUTINE_NAME_END SUBROUTINE_ABSOLUTE SUBROUTINE_RELATIVE

%%
/* PCRE gramatics */

/* modif_front/PATTERN/modif_rear */
pcre:	modif_front pattern modif_rear	{}
;

/*	pcre_delim
	front modificators
*/
modif_front:	pcre_delim				{}
	|		modif_front_ext pcre_delim	{}
;

modif_front_ext:	modif_front_unit				{}
	|			modif_front_unit modif_front_ext	{}
;

/*	(*UTF8)	enable UTF-8 option
	(*UCP)	enable UCP option
*/
modif_front_unit:	UTF8	{}
	|				UCP		{}
;

modif_rear:	pcre_delim					{}
	|		pcre_delim modif_rear_ext	{}
;

modif_rear_ext:	modif_rear_unit					{}
	|			modif_rear_unit modif_rear_ext	{}
;

/* optional options
	i	for PCRE_CASELESS
	m	for PCRE_MULTILINE
	s	for PCRE_DOTALL
	x	for PCRE_EXTENDED
	R	for R option
*/
modif_rear_unit:	MODIF_CASELESS		{}
	|				MODIF_MULTILINE		{}
	|				MODIF_DOTALL		{}
	|				MODIF_EXTENDED		{}
	|				MODIF_UNGREEDY		{}
	|				MODIF_R				{}
	|				MODIF_O				{}
	|				MODIF_P				{}
	|				MODIF_B				{}
;

pcre_delim:	SLASH	{}
;

pattern:	newlinespec inslash		{}
	|		inslash					{}
;

/*
	/pcre_pattern/
*/
inslash:	rv			{}
	|		bol rv		{}
	|		rv eol		{}
	|		bol rv eol	{}
;

rv:		ext_exp			{}
	|	rv or rv		{}
	|	or rv			{}
	|	rv or			{}
;

ext_exp:	exp			{}
	|		bol exp		{}
	|		exp eol		{}
	|		bol exp eol	{}
;

bol:	BOL	{}
;

eol:	EOL	{}
;

exp:	ext_unit		{}
	|	ext_unit exp	{}
;

/* extended unit
	unit (ASCII etc.)
	unit quantify (ASCII? etc.)
*/
ext_unit:	unit			{}
	|		quantify_unit	{}
;

quantify_unit:	unit quantify	{}
;

quantify:	quantifier				{}
	|		quantifier possessive	{}
	|		quantifier lazy			{}
;

/*
	?		0 or 1, greedy
	*		0 or more, greedy
	+		1 or more, greedy
	{n,m}	...
*/
quantifier:	ZEROMORE	{}
	|		ZEROONE		{}
	|		ONEMORE		{}
	|		repeating	{}
;

possessive:	ONEMORE	{}
;

lazy:	ZEROONE	{}
;

/* group branch */
or:	OR	{}
;

/* unit
	element
	capturing
	option INTERNAL OPTION SETTING
*/
unit:	element		{}
	|	capturing	{}
	|	option		{}
	|	chal		{}
	|	class		{}
;

/* INTERNAL OPTION SETTING
	OPTION option_set RBRA (?imsx)
	OPTION option_unset RBRA (?-imsx)
	OPTION option_set option_unset_group RBRA (?imsx-imsx)
*/
option:	optionStart option_set optionEnd						{}
	|	optionStart option_unset_group optionEnd				{}
	|	optionStart option_set option_unset_group optionEnd		{}
;

optionStart:	OPTION	{}
;

optionEnd:	RBRA	{}
;

/*
	DASH option_unset
*/
option_unset_group:	dash option_unset	{}
;

option_set:	option_set_unit				{}
	|		option_set_unit option_set	{}
;

option_set_unit:	MODIF_CASELESS		{}
	|				MODIF_DOTALL		{}
	|				MODIF_EXTENDED		{}
	|				MODIF_MULTILINE		{}
	|				MODIF_DUPNAMES		{}
	|				MODIF_UNGREEDY		{}
;

option_unset:	option_unset_unit				{}
	|			option_unset_unit option_unset	{}
;

option_unset_unit:	MODIF_CASELESS		{}
	|				MODIF_DOTALL		{}
	|				MODIF_EXTENDED		{}
	|				MODIF_MULTILINE		{}
	|				MODIF_DUPNAMES		{}
	|				MODIF_UNGREEDY		{}
;

/* Basic elements
	ASCII
	. as any character
	SPACE
	TAB
	CR
	LF
	FF
	BEL
	ESC
	CONTROL-X
	RESET Resetting the match start
	assertions
	ONEBYTE
	OCTAL
	character as literal
	backreference
	subroutine
 */
element:	ASCII			{}
	|		ANY				{}
	|		SPACE			{}
	|		hex				{}
	|		TAB				{}
	|		CR				{}
	|		LF				{}
	|		FF				{}
	|		BEL				{}
	|		ESC				{}
	|		CONTROLX		{}
	|		BSR				{}
	|		RESET			{}
	|		assertions		{}
	|		ONEBYTE			{}
	|		OCTAL			{}
	|		backreference	{}
	|		subroutine		{}
;

/* Simple assertions
 * These assertions may not appear in character classes
	\b	matches at a word boundary
	\B	matches when not at a word boundary
	\A	matches at the start of the subject
	\Z	matches at the end of the subject
		also matches before a newline at the end of the subject
	\z	matches only at the end of the subject
	\G	matches at the first matching position in the subject
*/
assertions:	WORDBOUNDARY	{}
	|		NWORDBOUNDARY	{}
	|		STARTSUBJECT	{}
	|		ENDSUBJECT		{}
	|		OENDSUBJECT		{}
	|		FIRSTPOSITION	{}
;

hex:	HEX	{}
;

/* new line convention specify */
newlinespec:	newlinespec_unit			{}
	|		newlinespec_unit newlinespec	{}
;

newlinespec_unit:	OPT_CR			{}
	|				OPT_LF			{}
	|				OPT_CRLF		{}
	|				OPT_ANYCRLF		{}
	|				OPT_ANY_NEWLINE	{}
;

/* CAPTURING
	(...)		capturing group
	(?<name>...)	named capturing group (Perl)
	(?'name'...)	named capturing group (Perl)
	(?P<name>...)	named capturing group (Python)
	(?:...)		non-capturing group
	(?|...)         non-capturing group; reset group numbers for
                          capturing groups in each alternative
	(?>...)         atomic, non-capturing group
	(?#....)        comment (not nestable)
	(?=...)         positive look ahead
	(?!...)         negative look ahead
	(?<=...)        positive look behind
	(?<!...)        negative look behind
*/
capturing:	startCapturing rv endCapturing									{}
	|		capturingNamed capturingName capturingNameEnd rv endCapturing	{}
	|		capturingNon rv endCapturing									{}
	|		capturingNonreset rv endCapturing								{}
	|		capturingAtomic rv endCapturing									{}
	|		capturingComment rv endCapturing								{}
	|		capturingPosahead rv endCapturing								{}
	|		capturingNegahead rv endCapturing								{}
	|		capturingPosbehind rv endCapturing								{}
	|		capturingNegbehind rv endCapturing								{}
;

/* name of named capturing */
capturingNamed:	CAPTURING_NAMED	{}
;

capturingName:	capturingNameAdd				{}
	|			capturingNameAdd capturingName	{}
;

capturingNameAdd:	ASCII	{}
;

capturingNon:	CAPTURING_NON	{}
;

capturingNonreset:	CAPTURING_NONRESET	{}
;

capturingAtomic:	CAPTURING_ATOMIC	{}
;

capturingComment:	CAPTURING_COMMENT	{}
;

capturingPosahead:	CAPTURING_POSAHEAD	{}
;

capturingNegahead:	CAPTURING_NEGAHEAD	{}
;

capturingPosbehind:	CAPTURING_POSBEHIND	{}
;

capturingNegbehind:	CAPTURING_NEGBEHIND	{}
;



/* end of name of capture */
capturingNameEnd:	CAPTURING_NAMED_END	{}
;

/* mark beginnig of grouping */
startCapturing:	LPAR	{}
;

endCapturing:	RPAR	{}
;

/* {} number of iterations */
repeating:	startRepeating interval endRepeating	{}
;

startRepeating:	LBRA	{}
;

endRepeating:	RBRA	{}
;

/* {} inside repeating
	x
	x,
	x,y
	,y	is not allowed!
*/
interval:	minimum intervalDelim maximum	{}
	|		minimum intervalDelim			{}
	|		maximum							{}
;

minimum:	INT	{}
;

maximum:	INT	{}
;

intervalDelim:	COMMA	{}
;

/* [], [^] or \w\W\s\S\d\D class of characters
	[...]
	[^...]
	\w\W\s\S\d\D
	posix class
*/
class:	classStart inclass classEnd	{}
	|	slashcharclass				{}
	|	posix_class					{}
;

classStart:	LBOX	{}
;

classEnd:	RBOX	{}
;

/* generic character types
	\d	any decimal digit
	\D	any character that is not a decimal digit
	\h	any horizontal whitespace character
	\H	any character that is not a horizontal whitespace character
	\s	any whitespace character
	\S	any character that is not a whitespace character
	\v	any vertical whitespace character
	\V	any character that is not a vertical whitespace character
	\w	any "word" character
	\W	any "non-word" character
*/
slashcharclass:	DECDIGIT		{}
	|			NDECDIGIT		{}
	|			HWHITESPACE		{}
	|			NHWHITESPACE	{}
	|			WHITESPACE		{}
	|			NWHITESPACE		{}
	|			VWHITESPACE		{}
	|			NVWHITESPACE	{}
	|			WORDCHAR		{}
	|			NWORDCHAR		{}
;

/** inside class
	class unit
	negate class
	alternate in class 	|	inclass or inclass		{}
*/
inclass:	inclass_ext_unit		{}
	|		bol inclass_ext_unit	{}
;

/* class unit
	one class unit
	more class units
*/
inclass_ext_unit:	inclass_unit			{}
	|		inclass_unit inclass_ext_unit	{}
;

inclass_unit:	inclass_element	{}
	|			rangechars		{}
	|			chal			{}
;

/* Co všechno může obsahovat třída znaků [...]
	ASCII
	posix_class
	slashcharclass
	rangechars
	hex
	TAB
	CR
	LF
	FF
	BEL
	ESC
	CONTROL-X
	RESET Resetting the match start \K
	OCTAL
*/
inclass_element:	ASCII			{}
	|				posix_class		{}
	|				slashcharclass	{}
	|				hex				{}
	|				TAB				{}
	|				CR				{}
	|				LF				{}
	|				FF				{}
	|				BEL				{}
	|				ESC				{}
	|				CONTROLX		{}
	|				RESET			{}
	|				OCTAL			{}
	|				DASH			{}
;

/* Rozsah znaků (např. a-z, 0-9) */
rangechars:		INT		{}
;

dash:	DASH		{}
;

/* Posixové třídy znaků */
posix_class:	P_ALNUM			{}
	|			P_ALPHA			{}
	|			P_ASCII			{}
	|			P_BLANK			{}
	|			P_CNTRL			{}
	|			P_DIGIT			{}
	|			P_GRAPH			{}
	|			P_LOWER			{}
	|			P_PRINT			{}
	|			P_PUNCT			{}
	|			P_SPACE			{}
	|			P_UPPER			{}
	|			P_WORD			{}
	|			P_XDIGIT		{}
	|			posix_class_neg	{}
;

posix_class_neg:	NP_ALNUM	{}
	|				NP_ALPHA	{}
	|				NP_ASCII	{}
	|				NP_BLANK	{}
	|				NP_CNTRL	{}
	|				NP_DIGIT	{}
	|				NP_GRAPH	{}
	|				NP_LOWER	{}
	|				NP_PRINT	{}
	|				NP_PUNCT	{}
	|				NP_SPACE	{}
	|				NP_UPPER	{}
	|				NP_WORD		{}
	|				NP_XDIGIT	{}
;

/* Remove special meaning */
chal:	chalStart inchal chalEnd	{}
;

chalStart:	CHALSTART	{}
;

chalEnd:	CHALEND		{}
;

inchal:		inchalExtUnit			{}
	|		inchalExtUnit inchal	{}
;

inchalExtUnit:	inchalUnit	{}
;

inchalUnit:		ASCII	{}
;

backreference:	BACKREFERENCE			{}
	|			named_back_reference	{}
;

named_back_reference:	nbrStart inNbr nbrEnd	{}
;

nbrStart:	NAMED_BACKREFERENCE	{}
;

nbrEnd:	NAMED_BACKREFERENCE_END	{}
;

inNbr:	inNbrUnit		{}
	|	inNbrUnit inNbr	{}
;

inNbrUnit:	ASCII	{}
;

subroutine:		SUBROUTINE_ALL		{}
	|			SUBROUTINE_ABSOLUTE	{}
	|			SUBROUTINE_RELATIVE	{}
	|			named_subroutine	{}
;

named_subroutine:	nsrStart inNsr nsrEnd	{}
;

nsrStart:	SUBROUTINE_NAME	{}
;

nsrEnd:	SUBROUTINE_NAME_END	{}
;

inNsr:	inNsrUnit		{}
	|	inNsrUnit inNsr	{}
;

inNsrUnit:	ASCII	{}
;

%%
//! standard lex error function
void yyerror(char *s) {
	warnx("Terminating current pcre: %s", s);
}
