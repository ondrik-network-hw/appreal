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
pcre:	modif_front pattern modif_rear	{DEBUG("pcre <<< modif_front pattern modif_rear" << endl); pcre2modif_front_pattern_modif_rear();}
;

/*	pcre_delim
	front modificators
*/
modif_front:	pcre_delim				{DEBUG("modif_front <<< pcre_delim" << endl); modif_front2pcre_delim();}
	|		modif_front_ext pcre_delim	{DEBUG("modif_front <<< modif_front_ext-pcre_delim" << endl); modif_front2modif_front_ext_pcre_delim();}
;

modif_front_ext:	modif_front_unit				{DEBUG("modif_front_ext <<< modif_front_unit" << endl); modif_front_ext2modif_front_unit();}
	|			modif_front_unit modif_front_ext	{DEBUG("modif_front_ext <<< modif_front_unit-modif_front_ext" << endl); modif_front_ext2modif_front_unit_modif_front_ext();}
;

/*	(*UTF8)	enable UTF-8 option
	(*UCP)	enable UCP option
*/
modif_front_unit:	UTF8	{DEBUG("modif_front_unit <<< UTF8" << endl); modif_front_unit2UTF8();}
	|				UCP		{DEBUG("modif_front_unit <<< UCP" << endl); modif_front_unit2UCP();}
;

modif_rear:	pcre_delim					{DEBUG("modif_rear <<< pcre_delim" << endl); modif_rear2pcre_delim();}
	|		pcre_delim modif_rear_ext	{DEBUG("modif_rear <<< pcre_delim-modif_rear_ext" << endl); modif_rear2pcre_delim_modif_rear_ext();}
;

modif_rear_ext:	modif_rear_unit					{DEBUG("modif_rear_ext <<< modif_rear_unit" << endl); modif_rear_ext2modif_rear_unit();}
	|			modif_rear_unit modif_rear_ext	{DEBUG("modif_rear_ext <<< modif_rear_unit-modif_rear_ext" << endl); modif_rear_ext2modif_rear_unit_modif_rear_ext();}
;

/* optional options
	i	for PCRE_CASELESS
	m	for PCRE_MULTILINE
	s	for PCRE_DOTALL
	x	for PCRE_EXTENDED
	R	for R option
*/
modif_rear_unit:	MODIF_CASELESS		{DEBUG("modif_rear_unit <<< MODIF_CASELESS" << endl); modif_rear_unit2MODIF_CASELESS();}
	|				MODIF_MULTILINE		{DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
	|				MODIF_DOTALL		{DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
	|				MODIF_EXTENDED		{DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
	|				MODIF_UNGREEDY		{DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
	|				MODIF_R				{DEBUG("modif_rear_unit <<< MODIF_R" << endl); modif_rear_unit2MODIF_R();}
	|				MODIF_O				{DEBUG("modif_rear_unit <<< MODIF_O" << endl); modif_rear_unit2MODIF_O();}
	|				MODIF_P				{DEBUG("modif_rear_unit <<< MODIF_P" << endl); modif_rear_unit2MODIF_P();}
	|				MODIF_B				{DEBUG("modif_rear_unit <<< MODIF_B" << endl); modif_rear_unit2MODIF_B();}
;

pcre_delim:	SLASH	{DEBUG("pcre_delim <<< SLASH" << endl); pcre_delim2SLASH();}
;

pattern:	newlinespec inslash		{DEBUG("pattern <<< newlinespec inslash" << endl); pattern2newlinespec_inslash();}
	|		inslash					{DEBUG("pattern <<< inslash" << endl); pattern2inslash();}
;

/*
	/pcre_pattern/
*/
inslash:	rv			{DEBUG("inslash <<< rv" << endl); inslash2rv();}
	|		bol rv		{DEBUG("inslash <<< bol-rv" << endl); inslash2bol_rv();}
	|		rv eol		{DEBUG("inslash <<< rv-eol" << endl); inslash2rv_eol();}
	|		bol rv eol	{DEBUG("inslash <<< bol-rv|eol" << endl); inslash2bol_rv_eol();}
;

rv:		ext_exp			{DEBUG("rv <<< ext_exp" << endl); rv2ext_exp();}
	|	rv or rv		{DEBUG("rv <<< rv-or|rv" << endl); rv2rv_or_rv();}
	|	or rv			{DEBUG("rv <<< or-rv" << endl); rv2or_rv();}
	|	rv or			{DEBUG("rv <<< rv-or" << endl); rv2rv_or();}
;

ext_exp:	exp			{DEBUG("ext_exp <<< exp" << endl); ext_exp2exp();}
	|		bol exp		{DEBUG("ext_exp <<< bol-exp" << endl); ext_exp2bol_exp();}
	|		exp eol		{DEBUG("ext_exp <<< exp-eol" << endl); ext_exp2exp_eol();}
	|		bol exp eol	{DEBUG("ext_exp <<< bol-exp|eol" << endl); ext_exp2bol_exp_eol();}
;

bol:	BOL	{DEBUG("bol <<< BOL" << endl); bol2BOL();}
;

eol:	EOL	{DEBUG("eol <<< EOL" << endl); eol2EOL();}
;

exp:	ext_unit		{DEBUG("exp <<< ext_unit" << endl); exp2ext_unit();}
	|	ext_unit exp	{DEBUG("exp <<< ext_unit-exp" << endl); exp2ext_unit_exp();}
;

/* extended unit
	unit (ASCII etc.)
	unit quantify (ASCII? etc.)
*/
ext_unit:	unit			{DEBUG("ext_unit <<< unit" << endl); ext_unit2unit();}
	|		quantify_unit	{DEBUG("ext_unit <<< quantify_unit" << endl); ext_unit2quantify_unit();}
;

quantify_unit:	unit quantify	{DEBUG("quantify_unit <<< unit quantify" << endl); quantify_unit2unit_quantify();}
;

quantify:	quantifier				{DEBUG("quantify <<< quantifier" << endl); quantify2quantifier();}
	|		quantifier possessive	{DEBUG("quantify <<< quantifier-possessive" << endl); quantify2quantifier_possessive();}
	|		quantifier lazy			{DEBUG("quantify <<< quantifier-lazy" << endl); quantify2quantifier_lazy();}
;

/*
	?		0 or 1, greedy
	*		0 or more, greedy
	+		1 or more, greedy
	{n,m}	...
*/
quantifier:	ZEROMORE	{DEBUG("quantifier <<< ZEROMORE" << endl); quantifier2ZEROMORE();}
	|		ZEROONE		{DEBUG("quantifier <<< ZEROONE" << endl); quantifier2ZEROONE();}
	|		ONEMORE		{DEBUG("quantifier <<< ONEMORE" << endl); quantifier2ONEMORE();}
	|		repeating	{DEBUG("quantifier <<< repeating" << endl); quantifier2repeating();}
;

possessive:	ONEMORE	{DEBUG("possessive <<< ONEMORE" << endl); possessive2ONEMORE();}
;

lazy:	ZEROONE	{DEBUG("lazy <<< ZEROONE" << endl); lazy2ZEROONE();}
;

/* group branch */
or:	OR	{DEBUG("or <<< OR" << endl); or2OR();}
;

/* unit
	element
	capturing
	option INTERNAL OPTION SETTING
*/
unit:	element		{DEBUG("unit <<< element" << endl); unit2element();}
	|	capturing	{DEBUG("unit <<< capturing" << endl); unit2capturing();}
	|	option		{DEBUG("unit <<< option" << endl); unit2option();}
	|	chal		{DEBUG("unit <<< chal" << endl); unit2chal();}
	|	class		{DEBUG("unit <<< class" << endl); unit2class();}
;

/* INTERNAL OPTION SETTING
	OPTION option_set RBRA (?imsx)
	OPTION option_unset RBRA (?-imsx)
	OPTION option_set option_unset_group RBRA (?imsx-imsx)
*/
option:	optionStart option_set optionEnd						{DEBUG("option <<< optionStart option_set optionEnd" << endl); option2optionStart_option_set_optionEnd();}
	|	optionStart option_unset_group optionEnd				{DEBUG("option <<< optionStart-option_unset_group|optionEnd" << endl); option2optionStart_option_unset_group_optionEnd();}
	|	optionStart option_set option_unset_group optionEnd		{DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl); option2optionStart_option_set_option_unset_group_optionEnd();}
;

optionStart:	OPTION	{DEBUG("optionStart <<< OPTION" << endl); optionStart2OPTION();}
;

optionEnd:	RBRA	{DEBUG("optionEnd <<< RBRA" << endl); optionEnd2RBRA();}
;

/*
	DASH option_unset
*/
option_unset_group:	dash option_unset	{DEBUG("option_unset_group <<< dash option_unset" << endl); option_unset_group2dash_option_unset();}
;

option_set:	option_set_unit				{DEBUG("option_set <<< option_set_unit" << endl); option_set2option_set_unit();}
	|		option_set_unit option_set	{DEBUG("option_set <<< option_set_unit-option_set" << endl); option_set2option_set_unit_option_set();}
;

option_set_unit:	MODIF_CASELESS		{DEBUG("option_set_unit <<< MODIF_CASELESS" << endl); option_set_unit2MODIF_CASELESS();}
	|				MODIF_DOTALL		{DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
	|				MODIF_EXTENDED		{DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
	|				MODIF_MULTILINE		{DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
	|				MODIF_DUPNAMES		{DEBUG("option_set_unit <<< MODIF_DUPNAMES" << endl); option_set_unit2MODIF_DUPNAMES();}
	|				MODIF_UNGREEDY		{DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
;

option_unset:	option_unset_unit				{DEBUG("option_unset <<< option_unset_unit" << endl); option_unset2option_unset_unit();}
	|			option_unset_unit option_unset	{DEBUG("option_unset <<< option_unset_unit-option_unset" << endl); option_unset2option_unset_unit_option_unset();}
;

option_unset_unit:	MODIF_CASELESS		{DEBUG("option_unset_unit <<< MODIF_CASELESS" << endl); option_unset_unit2MODIF_CASELESS();}
	|				MODIF_DOTALL		{DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
	|				MODIF_EXTENDED		{DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
	|				MODIF_MULTILINE		{DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
	|				MODIF_DUPNAMES		{DEBUG("option_set_unit <<< MODIF_DUPNAMES" << endl); option_set_unit2MODIF_DUPNAMES();}
	|				MODIF_UNGREEDY		{DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
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
element:	ASCII			{DEBUG("element <<< ASCII " << (char)yylval << endl); element2ASCII((char)yylval);}
	|		ANY				{DEBUG("element <<< ANY" << endl); element2ANY();}
	|		SPACE			{DEBUG("element <<< SPACE" << endl); element2SPACE();}
	|		hex				{DEBUG("element <<< hex" << endl); element2hex();}
	|		TAB				{DEBUG("element <<< TAB" << endl); element2TAB();}
	|		CR				{DEBUG("element <<< CR" << endl); element2CR();}
	|		LF				{DEBUG("element <<< LF" << endl); element2LF();}
	|		FF				{DEBUG("element <<< FF" << endl); element2FF();}
	|		BEL				{DEBUG("element <<< BEL" << endl); element2BEL();}
	|		ESC				{DEBUG("element <<< ESC" << endl); element2ESC();}
	|		CONTROLX		{DEBUG("element <<< CONTROLX " << (char)yylval << endl); element2CONTROLX((char)yylval);}
	|		BSR				{DEBUG("element <<< BSR" << endl); element2BSR();}
	|		RESET			{DEBUG("element <<< RESET" << endl); element2RESET();}
	|		assertions		{DEBUG("element <<< assertions" << endl); element2assertions();}
	|		ONEBYTE			{DEBUG("element <<< ONEBYTE" << endl); element2ONEBYTE();}
	|		OCTAL			{DEBUG("element <<< OCTAL " << (char)yylval << endl); element2OCTAL((char)yylval);}
	|		backreference	{DEBUG("element <<< backreference" << endl); element2backreference();}
	|		subroutine		{DEBUG("element <<< subroutine" << endl); element2subroutine();}
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
assertions:	WORDBOUNDARY	{DEBUG("assertions <<< WORDBOUNDARY" << endl); assertions2WORDBOUNDARY();}
	|		NWORDBOUNDARY	{DEBUG("assertions <<< NWORDBOUNDARY" << endl); assertions2NWORDBOUNDARY();}
	|		STARTSUBJECT	{DEBUG("assertions <<< STARTSUBJECT" << endl); assertions2STARTSUBJECT();}
	|		ENDSUBJECT		{DEBUG("assertions <<< ENDSUBJECT" << endl); assertions2ENDSUBJECT();}
	|		OENDSUBJECT		{DEBUG("assertions <<< OENDSUBJECT" << endl); assertions2OENDSUBJECT();}
	|		FIRSTPOSITION	{DEBUG("assertions <<< FIRSTPOSITION" << endl); assertions2FIRSTPOSITION();}
;

hex:	HEX	{DEBUG("hex <<< HEX " << hex << (char)yylval << endl); hex2HEX((char)yylval);}
;

/* new line convention specify */
newlinespec:	newlinespec_unit			{DEBUG("newlinespec <<< newlinespec_unit" << endl); newlinespec2newlinespec_unit();}
	|		newlinespec_unit newlinespec	{DEBUG("newlinespec <<< newlinespec_unit-newlinespec" << endl); newlinespec2newlinespec_unit_newlinespec();}
;

newlinespec_unit:	OPT_CR			{DEBUG("newlinespec_unit <<< OPT_CR" << endl); newlinespec_unit2OPT_CR();}
	|				OPT_LF			{DEBUG("newlinespec_unit <<< OPT_LF" << endl); newlinespec_unit2OPT_LF();}
	|				OPT_CRLF		{DEBUG("newlinespec_unit <<< OPT_CRLF" << endl); newlinespec_unit2OPT_CRLF();}
	|				OPT_ANYCRLF		{DEBUG("newlinespec_unit <<< OPT_ANYCRLF" << endl); newlinespec_unit2OPT_ANYCRLF();}
	|				OPT_ANY_NEWLINE	{DEBUG("newlinespec_unit <<< OPT_ANY_NEWLINE" << endl); newlinespec_unit2OPT_ANY_NEWLINE();}
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
capturing:	startCapturing rv endCapturing									{DEBUG("capturing <<< startCapturing rv endCapturing" << endl); capturing2startCapturing_rv_endCapturing();}
	|		capturingNamed capturingName capturingNameEnd rv endCapturing	{DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl); capturing2capturingNamed_capturingName_capturingNameEnd_rv_endCapturing();}
	|		capturingNon rv endCapturing									{DEBUG("capturing <<< capturingNon-rv|endCapturing" << endl); capturing2capturingNon_rv_endCapturing();}
	|		capturingNonreset rv endCapturing								{DEBUG("capturing <<< capturingNonreset-rv|endCapturing" << endl); capturing2capturingNonreset_rv_endCapturing();}
	|		capturingAtomic rv endCapturing									{DEBUG("capturing <<< capturingAtomic-rv|endCapturing" << endl); capturing2capturingAtomic_rv_endCapturing();}
	|		capturingComment rv endCapturing								{DEBUG("capturing <<< capturingComment-rv|endCapturing" << endl); capturing2capturingComment_rv_endCapturing();}
	|		capturingPosahead rv endCapturing								{DEBUG("capturing <<< capturingPosahead-rv|endCapturing" << endl); capturing2capturingPosahead_rv_endCapturing();}
	|		capturingNegahead rv endCapturing								{DEBUG("capturing <<< capturingNegahead-rv|endCapturing" << endl); capturing2capturingNegahead_rv_endCapturing();}
	|		capturingPosbehind rv endCapturing								{DEBUG("capturing <<< capturingPosbehind-rv|endCapturing" << endl); capturing2capturingPosbehind_rv_endCapturing();}
	|		capturingNegbehind rv endCapturing								{DEBUG("capturing <<< capturingNegbehind-rv|endCapturing" << endl); capturing2capturingNegbehind_rv_endCapturing();}
;

/* name of named capturing */
capturingNamed:	CAPTURING_NAMED	{DEBUG("capturingNamed <<< CAPTURING_NAMED" << endl); capturingNamed2CAPTURING_NAMED();}
;

capturingName:	capturingNameAdd				{DEBUG("capturingName <<< capturingNameAdd" << endl); capturingName2capturingNameAdd();}
	|			capturingNameAdd capturingName	{DEBUG("capturingName <<< capturingNameAdd-capturingName" << endl); capturingName2capturingNameAdd_capturingName();}
;

capturingNameAdd:	ASCII	{DEBUG("capturingNameAdd <<< ASCII " << (char)yylval << endl); capturingNameAdd2ASCII((char)yylval);}
;

capturingNon:	CAPTURING_NON	{DEBUG("capturingNon <<< CAPTURING_NON" << endl); capturingNon2CAPTURING_NON();}
;

capturingNonreset:	CAPTURING_NONRESET	{DEBUG("capturingNonreset <<< CAPTURING_NONRESET" << endl); capturingNonreset2CAPTURING_NONRESET();}
;

capturingAtomic:	CAPTURING_ATOMIC	{DEBUG("capturingAtomic <<< CAPTURING_ATOMIC" << endl); capturingAtomic2CAPTURING_ATOMIC();}
;

capturingComment:	CAPTURING_COMMENT	{DEBUG("capturingComment <<< CAPTURING_COMMENT" << endl); capturingComment2CAPTURING_COMMENT();}
;

capturingPosahead:	CAPTURING_POSAHEAD	{DEBUG("capturingPosahead <<< CAPTURING_POSAHEAD" << endl); capturingPosahead2CAPTURING_POSAHEAD();}
;

capturingNegahead:	CAPTURING_NEGAHEAD	{DEBUG("capturingNegahead <<< CAPTURING_NEGAHEAD" << endl); capturingNegahead2CAPTURING_NEGAHEAD();}
;

capturingPosbehind:	CAPTURING_POSBEHIND	{DEBUG("capturingPosbehind <<< CAPTURING_POSBEHIND" << endl); capturingPosbehind2CAPTURING_POSBEHIND();}
;

capturingNegbehind:	CAPTURING_NEGBEHIND	{DEBUG("capturingNegbehind <<< CAPTURING_NEGBEHIND" << endl); capturingNegbehind2CAPTURING_NEGBEHIND();}
;



/* end of name of capture */
capturingNameEnd:	CAPTURING_NAMED_END	{DEBUG("capturingNameEnd <<< CAPTURING_NAMED_END" << endl); capturingNameEnd2CAPTURING_NAMED_END();}
;

/* mark beginnig of grouping */
startCapturing:	LPAR	{DEBUG("startCapturing <<< LPAR" << endl); startCapturing2LPAR();}
;

endCapturing:	RPAR	{DEBUG("endCapturing <<< RPAR" << endl); endCapturing2RPAR();}
;

/* {} number of iterations */
repeating:	startRepeating interval endRepeating	{DEBUG("repeating <<< startRepeating interval endRepeating" << endl); repeating2startRepeating_interval_endRepeating();}
;

startRepeating:	LBRA	{DEBUG("startRepeating <<< LBRA" << endl); startRepeating2LBRA();}
;

endRepeating:	RBRA	{DEBUG("endRepeating <<< RBRA" << endl); endRepeating2RBRA();}
;

/* {} inside repeating
	x
	x,
	x,y
	,y	is not allowed!
*/
interval:	minimum intervalDelim maximum	{DEBUG("interval <<< minimum intervalDelim maximum" << endl); interval2minimum_intervalDelim_maximum();}
	|		minimum intervalDelim			{DEBUG("interval <<< minimum-intervalDelim" << endl); interval2minimum_intervalDelim();}
	|		maximum							{DEBUG("interval <<< maximum" << endl); interval2maximum();}
;

minimum:	INT	{DEBUG("minimum <<< INT " << (int)yylval << endl); minimum2INT((int)yylval);}
;

maximum:	INT	{DEBUG("maximum <<< INT " << (int)yylval << endl); maximum2INT((int)yylval);}
;

intervalDelim:	COMMA	{DEBUG("intervalDelim <<< COMMA" << endl); intervalDelim2COMMA();}
;

/* [], [^] or \w\W\s\S\d\D class of characters
	[...]
	[^...]
	\w\W\s\S\d\D
	posix class
*/
class:	classStart inclass classEnd	{DEBUG("class <<< classStart inclass classEnd" << endl); class2classStart_inclass_classEnd();}
	|	slashcharclass				{DEBUG("class <<< slashcharclass" << endl); class2slashcharclass();}
	|	posix_class					{DEBUG("class <<< posix_class" << endl); class2posix_class();}
;

classStart:	LBOX	{DEBUG("classStart <<< LBOX" << endl); classStart2LBOX();}
;

classEnd:	RBOX	{DEBUG("classEnd <<< RBOX" << endl); classEnd2RBOX();}
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
slashcharclass:	DECDIGIT		{DEBUG("slashcharclass <<< DECDIGIT" << endl); slashcharclass2DECDIGIT();}
	|			NDECDIGIT		{DEBUG("slashcharclass <<< NDECDIGIT" << endl); slashcharclass2NDECDIGIT();}
	|			HWHITESPACE		{DEBUG("slashcharclass <<< HWHITESPACE" << endl); slashcharclass2HWHITESPACE();}
	|			NHWHITESPACE	{DEBUG("slashcharclass <<< NHWHITESPACE" << endl); slashcharclass2NHWHITESPACE();}
	|			WHITESPACE		{DEBUG("slashcharclass <<< WHITESPACE" << endl); slashcharclass2WHITESPACE();}
	|			NWHITESPACE		{DEBUG("slashcharclass <<< NWHITESPACE" << endl); slashcharclass2NWHITESPACE();}
	|			VWHITESPACE		{DEBUG("slashcharclass <<< VWHITESPACE" << endl); slashcharclass2VWHITESPACE();}
	|			NVWHITESPACE	{DEBUG("slashcharclass <<< NVWHITESPACE" << endl); slashcharclass2NVWHITESPACE();}
	|			WORDCHAR		{DEBUG("slashcharclass <<< WORDCHAR" << endl); slashcharclass2WORDCHAR();}
	|			NWORDCHAR		{DEBUG("slashcharclass <<< NWORDCHAR" << endl); slashcharclass2NWORDCHAR();}
;

/** inside class
	class unit
	negate class
	alternate in class 	|	inclass or inclass		{}
*/
inclass:	inclass_ext_unit		{DEBUG("inclass <<< inclass_ext_unit" << endl); inclass2inclass_ext_unit();}
	|		bol inclass_ext_unit	{DEBUG("inclass <<< bol-inclass_ext_unit" << endl); inclass2bol_inclass_ext_unit();}
;

/* class unit
	one class unit
	more class units
*/
inclass_ext_unit:	inclass_unit			{DEBUG("inclass_ext_unit <<< inclass_unit" << endl); inclass_ext_unit2inclass_unit();}
	|		inclass_unit inclass_ext_unit	{DEBUG("inclass_ext_unit <<< inclass_unit-inclass_ext_unit" << endl); inclass_ext_unit2inclass_unit_inclass_ext_unit();}
;

inclass_unit:	inclass_element	{DEBUG("inclass_unit <<< inclass_element" << endl); inclass_unit2inclass_element();}
	|			rangechars		{DEBUG("inclass_unit <<< rangechars" << endl); inclass_unit2rangechars();}
	|			chal			{DEBUG("inclass_unit <<< chal" << endl); inclass_unit2chal();}
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
inclass_element:	ASCII			{DEBUG("element <<< ASCII " << (char)yylval << endl); element2ASCII((char)yylval);}
	|				posix_class		{DEBUG("inclass_element <<< posix_class" << endl); inclass_element2posix_class();}
	|				slashcharclass	{DEBUG("inclass_element <<< slashcharclass" << endl); inclass_element2slashcharclass();}
	|				hex				{DEBUG("inclass_element <<< hex" << endl); inclass_element2hex();}
	|				TAB				{DEBUG("inclass_element <<< TAB" << endl); inclass_element2TAB();}
	|				CR				{DEBUG("inclass_element <<< CR" << endl); inclass_element2CR();}
	|				LF				{DEBUG("inclass_element <<< LF" << endl); inclass_element2LF();}
	|				FF				{DEBUG("inclass_element <<< FF" << endl); inclass_element2FF();}
	|				BEL				{DEBUG("inclass_element <<< BEL" << endl); inclass_element2BEL();}
	|				ESC				{DEBUG("inclass_element <<< ESC" << endl); inclass_element2ESC();}
	|				CONTROLX		{DEBUG("inclass_element <<< CONTROLX " << (char)yylval << endl); inclass_element2CONTROLX((char)yylval);}
	|				RESET			{DEBUG("inclass_element <<< RESET" << endl); inclass_element2RESET();}
	|				OCTAL			{DEBUG("inclass_element <<< OCTAL " << (char)yylval << endl); inclass_element2OCTAL((char)yylval);}
	|				DASH			{DEBUG("inclass_element <<< DASH" << endl); inclass_element2DASH();}
;

/* Rozsah znaků (např. a-z, 0-9) */
rangechars:		INT		{DEBUG("rangechars <<< INT " << (int)yylval << endl); rangechars2INT((int)yylval);}
;

dash:	DASH		{DEBUG("dash <<< DASH" << endl); dash2DASH();}
;

/* Posixové třídy znaků */
posix_class:	P_ALNUM			{DEBUG("posix_class <<< P_ALNUM" << endl); posix_class2P_ALNUM();}
	|			P_ALPHA			{DEBUG("posix_class <<< P_ALPHA" << endl); posix_class2P_ALPHA();}
	|			P_ASCII			{DEBUG("posix_class <<< P_ASCII" << endl); posix_class2P_ASCII();}
	|			P_BLANK			{DEBUG("posix_class <<< P_BLANK" << endl); posix_class2P_BLANK();}
	|			P_CNTRL			{DEBUG("posix_class <<< P_CNTRL" << endl); posix_class2P_CNTRL();}
	|			P_DIGIT			{DEBUG("posix_class <<< P_DIGIT" << endl); posix_class2P_DIGIT();}
	|			P_GRAPH			{DEBUG("posix_class <<< P_GRAPH" << endl); posix_class2P_GRAPH();}
	|			P_LOWER			{DEBUG("posix_class <<< P_LOWER" << endl); posix_class2P_LOWER();}
	|			P_PRINT			{DEBUG("posix_class <<< P_PRINT" << endl); posix_class2P_PRINT();}
	|			P_PUNCT			{DEBUG("posix_class <<< P_PUNCT" << endl); posix_class2P_PUNCT();}
	|			P_SPACE			{DEBUG("posix_class <<< P_SPACE" << endl); posix_class2P_SPACE();}
	|			P_UPPER			{DEBUG("posix_class <<< P_UPPER" << endl); posix_class2P_UPPER();}
	|			P_WORD			{DEBUG("posix_class <<< P_WORD" << endl); posix_class2P_WORD();}
	|			P_XDIGIT		{DEBUG("posix_class <<< P_XDIGIT" << endl); posix_class2P_XDIGIT();}
	|			posix_class_neg	{DEBUG("posix_class <<< posix_class_neg" << endl); posix_class2posix_class_neg();}
;

posix_class_neg:	NP_ALNUM	{DEBUG("posix_class_neg <<< NP_ALNUM" << endl); posix_class_neg2NP_ALNUM();}
	|				NP_ALPHA	{DEBUG("posix_class_neg <<< NP_ALPHA" << endl); posix_class_neg2NP_ALPHA();}
	|				NP_ASCII	{DEBUG("posix_class_neg <<< NP_ASCII" << endl); posix_class_neg2NP_ASCII();}
	|				NP_BLANK	{DEBUG("posix_class_neg <<< NP_BLANK" << endl); posix_class_neg2NP_BLANK();}
	|				NP_CNTRL	{DEBUG("posix_class_neg <<< NP_CNTRL" << endl); posix_class_neg2NP_CNTRL();}
	|				NP_DIGIT	{DEBUG("posix_class_neg <<< NP_DIGIT" << endl); posix_class_neg2NP_DIGIT();}
	|				NP_GRAPH	{DEBUG("posix_class_neg <<< NP_GRAPH" << endl); posix_class_neg2NP_GRAPH();}
	|				NP_LOWER	{DEBUG("posix_class_neg <<< NP_LOWER" << endl); posix_class_neg2NP_LOWER();}
	|				NP_PRINT	{DEBUG("posix_class_neg <<< NP_PRINT" << endl); posix_class_neg2NP_PRINT();}
	|				NP_PUNCT	{DEBUG("posix_class_neg <<< NP_PUNCT" << endl); posix_class_neg2NP_PUNCT();}
	|				NP_SPACE	{DEBUG("posix_class_neg <<< NP_SPACE" << endl); posix_class_neg2NP_SPACE();}
	|				NP_UPPER	{DEBUG("posix_class_neg <<< NP_UPPER" << endl); posix_class_neg2NP_UPPER();}
	|				NP_WORD		{DEBUG("posix_class_neg <<< NP_WORD" << endl); posix_class_neg2NP_WORD();}
	|				NP_XDIGIT	{DEBUG("posix_class_neg <<< NP_XDIGIT" << endl); posix_class_neg2NP_XDIGIT();}
;

/* Remove special meaning */
chal:	chalStart inchal chalEnd	{DEBUG("chal <<< chalStart inchal chalEnd" << endl); chal2chalStart_inchal_chalEnd();}
;

chalStart:	CHALSTART	{DEBUG("chalStart <<< CHALSTART" << endl); chalStart2CHALSTART();}
;

chalEnd:	CHALEND		{DEBUG("chalEnd <<< CHALEND" << endl); chalEnd2CHALEND();}
;

inchal:		inchalExtUnit			{DEBUG("inchal <<< inchalExtUnit" << endl); inchal2inchalExtUnit();}
	|		inchalExtUnit inchal	{DEBUG("inchal <<< inchalExtUnit-inchal" << endl); inchal2inchalExtUnit_inchal();}
;

inchalExtUnit:	inchalUnit	{DEBUG("inchalExtUnit <<< inchalUnit" << endl); inchalExtUnit2inchalUnit();}
;

inchalUnit:		ASCII	{DEBUG("inchalUnit <<< ASCII " << (char)yylval << endl); inchalUnit2ASCII((char)yylval);}
;

backreference:	BACKREFERENCE			{DEBUG("backreference <<< BACKREFERENCE" << endl); backreference2BACKREFERENCE();}
	|			named_back_reference	{DEBUG("backreference <<< named_back_reference" << endl); backreference2named_back_reference();}
;

named_back_reference:	nbrStart inNbr nbrEnd	{DEBUG("named_back_reference <<< nbrStart inNbr nbrEnd" << endl); named_back_reference2nbrStart_inNbr_nbrEnd();}
;

nbrStart:	NAMED_BACKREFERENCE	{DEBUG("nbrStart <<< NAMED_BACKREFERENCE" << endl); nbrStart2NAMED_BACKREFERENCE();}
;

nbrEnd:	NAMED_BACKREFERENCE_END	{DEBUG("nbrEnd <<< NAMED_BACKREFERENCE_END" << endl); nbrEnd2NAMED_BACKREFERENCE_END();}
;

inNbr:	inNbrUnit		{DEBUG("inNbr <<< inNbrUnit" << endl); inNbr2inNbrUnit();}
	|	inNbrUnit inNbr	{DEBUG("inNbr <<< inNbrUnit-inNbr" << endl); inNbr2inNbrUnit_inNbr();}
;

inNbrUnit:	ASCII	{DEBUG("inNbrUnit <<< ASCII " << (char)yylval << endl); inNbrUnit2ASCII((char)yylval);}
;

subroutine:		SUBROUTINE_ALL		{DEBUG("subroutine <<< SUBROUTINE_ALL" << endl); subroutine2SUBROUTINE_ALL();}
	|			SUBROUTINE_ABSOLUTE	{DEBUG("subroutine <<< SUBROUTINE_ABSOLUTE" << endl); subroutine2SUBROUTINE_ABSOLUTE();}
	|			SUBROUTINE_RELATIVE	{DEBUG("subroutine <<< SUBROUTINE_RELATIVE" << endl); subroutine2SUBROUTINE_RELATIVE();}
	|			named_subroutine	{DEBUG("subroutine <<< named_subroutine" << endl); subroutine2named_subroutine();}
;

named_subroutine:	nsrStart inNsr nsrEnd	{DEBUG("named_subroutine <<< nsrStart inNsr nsrEnd" << endl); named_subroutine2nsrStart_inNsr_nsrEnd();}
;

nsrStart:	SUBROUTINE_NAME	{DEBUG("nsrStart <<< SUBROUTINE_NAME" << endl); nsrStart2SUBROUTINE_NAME();}
;

nsrEnd:	SUBROUTINE_NAME_END	{DEBUG("nsrEnd <<< SUBROUTINE_NAME_END" << endl); nsrEnd2SUBROUTINE_NAME_END();}
;

inNsr:	inNsrUnit		{DEBUG("inNsr <<< inNsrUnit" << endl); inNsr2inNsrUnit();}
	|	inNsrUnit inNsr	{DEBUG("inNsr <<< inNsrUnit-inNsr" << endl); inNsr2inNsrUnit_inNsr();}
;

inNsrUnit:	ASCII	{DEBUG("inNsrUnit <<< ASCII " << (char)yylval << endl); inNsrUnit2ASCII((char)yylval);}
;

%%
//! standard lex error function
void yyerror(char *s) {
	warnx("Terminating current pcre: %s", s);
}
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
