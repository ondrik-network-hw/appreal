%option nounput
%option outfile="pcre.yy.c"

%{
#include "debug.hpp"
#include "interface.h"
#include "pcre.tab.h"

#define DEBUG_HEADER "lex"
extern int debug;

using namespace std;

%}

INT	(0|[1-9][0-9]*)
STRING	[a-zA-Z0-9_-]+
HEX	[a-fA-F0-9][a-fA-F0-9]

%x times
%x class class_first
%x esc
%x exp
%x modif_front
%x modif_rear
%x opt
%x capturing_named_perl1 capturing_named_perl2 capturing_named_python
%x chal chal_class
%x nb_perl1 nb_perl2 nb_perl3 nb_dotnet nb_python
%x srn_perl srn_oniguruma1 srn_oniguruma2 srn_python

%%

<modif_front>"*UTF8)" {
	DEBUG("*UTF8" << endl);
	return UTF8;
}
<modif_front>"*UCP)" {
		DEBUG("*UCP" << endl);
		return UCP;
	}
<modif_front,INITIAL>"/"	{	// pattern s úvodním modifikátorem, začátek výrazu
		DEBUG("modif_front: SLASH" << endl);
		BEGIN(exp);
		return SLASH;
	}
<modif_front>.	{
	DEBUG("modif_front: ASCII: " << yytext << endl);
	return ASCII;
}

<exp>"{"	{ // start of quantifiing
		DEBUG("LBRA" << endl);
		BEGIN(times);
		return LBRA;
	}
<times>"}"	{ // end of quantifiing
		DEBUG("RBRA" << endl);
		BEGIN(exp);
		return RBRA;
	}
<times>{INT}	{
		DEBUG("INT" << endl);
		yylval = atoi(yytext);
		return INT;
}
<times>,	{
		DEBUG("COMMA" << endl);
		return COMMA;
}
<times>.	{
	DEBUG("times: ASCII: " << yytext << endl);
	return ASCII;
}
<exp,class>"\\d"	{
	DEBUG("DECDIGIT" << endl);
	return DECDIGIT;
}
<exp,class>"\\D"	{
	DEBUG("NDECDIGIT" << endl);
	return NDECDIGIT;
}
<exp,class>"\\h"	{
	DEBUG("HWHITESPACE" << endl);
	return HWHITESPACE;
}
<exp,class>"\\H"	{
	DEBUG("NHWHITESPACE" << endl);
	return NHWHITESPACE;
}
<exp,class>"\\s"	{
	DEBUG("WHITESPACE" << endl);
	return WHITESPACE;
}
<exp,class>"\\S"	{
	DEBUG("NWHITESPACE" << endl);
	return NWHITESPACE;
}
<exp,class>"\\v"	{
	DEBUG("VWHITESPACE" << endl);
	return VWHITESPACE;
}
<exp,class>"\\V"	{
	DEBUG("NVWHITESPACE" << endl);
	return NVWHITESPACE;
}
<exp,class>"\\w"	{
	DEBUG("WORDCHAR" << endl);
	return WORDCHAR;
}
<exp,class>"\\W"	{
	DEBUG("NWORDCHAR" << endl);
	return NWORDCHAR;
}
<exp>\\\$ {
	yylval = '$';
	DEBUG("ASCII $" << endl);
	return ASCII;
}
<exp>\\[\\/\^.\[|()?*+{]	{ /* speciální znaky \/^$.[|()?*+{ jako ASCII mimo třídu znaků */
	yylval = yytext[1];
	DEBUG("ASCII " << (char)yylval << endl);
	return ASCII;
}
<exp,class>\\x{HEX}	{
	if( sscanf(yytext, "\\x%x", &yylval) == 1 )
	{
		DEBUG("HEX " << yytext << endl);
		return HEX;
	}
}
<exp,class>\\x\{{HEX}\}	{
	if( sscanf(yytext, "\\x{%x}", &yylval) == 1 )
	{
		DEBUG("HEX " << yytext << endl);
		return HEX;
	}
}
<exp,class>"\\x"	{ // PCRE: the  initial  \x  will  be interpreted as ... zero
	yylval = 0x00;
	DEBUG("HEX \\x" << endl);
	return HEX;
}
<exp,class>\\[c].	{ // \cx "control-x", where x is any character
	yylval = yytext[2];
	DEBUG("CONTROLX " << (char)yylval << endl);
	return CONTROLX;
}
<exp,class>"\\t"	{ // \t
	DEBUG("TAB" << endl);
	return TAB;
}
<exp,class>"\\n"	{ // \n
	DEBUG("LF" << endl);
	return LF;
}
<exp,class>"\\r"	{ // \r
	DEBUG("CR" << endl);
	return CR;
}
<exp,class>"\\f"	{ // \f
	DEBUG("FF" << endl);
	return FF;
}
<exp,class>"\\e"	{ // \e escape (hex 1B)
	DEBUG("ESC" << endl);
	return ESC;
}
<exp,class>"\\a"	{ // \a alarm, that is, the BEL character (hex 07)
	DEBUG("BEL" << endl);
	return BEL;
}
<exp,class>"\\R"	{ // backslash R = BSR
	DEBUG("BSR" << endl);
	return BSR;
}
<exp,class>"\\K"	{ // RESET
	DEBUG("RESET" << endl);
	return RESET;
}
<exp>"\\b"	{ // \b	matches at a word boundary
	DEBUG("WORDBOUNDARY" << endl);
	return WORDBOUNDARY;
}
<exp>"\\B"	{ // \B	matches when not at a word boundary
	DEBUG("NWORDBOUNDARY" << endl);
	return NWORDBOUNDARY;
}
<exp>"\\A"	{ // \A	matches at the start of the subject
	DEBUG("STARTSUBJECT" << endl);
	return STARTSUBJECT;
}
<exp>"\\Z"	{ // \Z	matches at the end of the subject
	DEBUG("ENDSUBJECT" << endl);
	return ENDSUBJECT;
}
<exp>"\\z"	{ // \z	matches only at the end of the subject
	DEBUG("OENDSUBJECT" << endl);
	return OENDSUBJECT;
}
<exp>"\\G"	{ // \G	matches at the first matching position in the subject
	DEBUG("FIRSTPOSITION" << endl);
	return FIRSTPOSITION;
}
<exp>"\\C"	{ // MATCHING A SINGLE BYTE \C
	DEBUG("ONEBYTE " << (char)yylval << endl);
	return ONEBYTE;

}
<exp>"\\Q"	{ // \Q start of removing special meaning
	DEBUG("CHALSTART" << endl);
	BEGIN(chal);
	return CHALSTART;
}
<chal>"\\E"	{ // \E end of special meaning
	DEBUG("CHALEND" << endl);
	BEGIN(exp);
	return CHALEND;
}
<class>"\\Q"	{ // \Q start of removing special meaning
	DEBUG("CHALSTART" << endl);
	BEGIN(chal_class);
	return CHALSTART;
}
<chal_class>"\\E"	{ // \E end of special meaning
	DEBUG("CHALEND" << endl);
	BEGIN(class);
	return CHALEND;
}
<chal,chal_class>.	{
	DEBUG("ASCII " << yytext << endl);
	yylval = yytext[0];
	return ASCII;
}
<exp>\\[0-9]	{	// back reference
	if( sscanf(yytext, "\\%d", &yylval) == 1 )
	{
		DEBUG("BACKREFERENCE" << endl);
		return BACKREFERENCE;
	}
}
<exp>\\g-?[0-9]	{	// back reference
	if( sscanf(yytext, "\\g%d", &yylval) == 1 )
	{
		DEBUG("BACKREFERENCE" << endl);
		return BACKREFERENCE;
	}
}
<exp>\\g\{-?[0-9]\}	{	// back reference
	if( sscanf(yytext, "\\g{%d}", &yylval) == 1 )
	{
		DEBUG("BACKREFERENCE" << endl);
		return BACKREFERENCE;
	}
}
<exp>\\k\<	{	// named back reference
	DEBUG("NAMED_BACKREFERENCE" << endl);
	BEGIN(nb_perl1);
	return NAMED_BACKREFERENCE;
}
<exp>\\k\'	{	// named back reference
	DEBUG("NAMED_BACKREFERENCE" << endl);
	BEGIN(nb_perl2);
	return NAMED_BACKREFERENCE;
}
<exp>\\g\{	{	// named back reference
	DEBUG("NAMED_BACKREFERENCE" << endl);
	BEGIN(nb_perl3);
	return NAMED_BACKREFERENCE;
}
<exp>\\k\{	{	// named back reference
	DEBUG("NAMED_BACKREFERENCE" << endl);
	BEGIN(nb_dotnet);
	return NAMED_BACKREFERENCE;
}
<exp>"(?P="	{	// named back reference
	DEBUG("NAMED_BACKREFERENCE" << endl);
	BEGIN(nb_python);
	return NAMED_BACKREFERENCE;
}
<nb_perl1>">"	{	// named back reference end
	DEBUG("NAMED_BACKREFERENCE_END" << endl);
	BEGIN(exp);
	return NAMED_BACKREFERENCE_END;
}
<nb_perl2>"'"	{	// named back reference end
	DEBUG("NAMED_BACKREFERENCE_END" << endl);
	BEGIN(exp);
	return NAMED_BACKREFERENCE_END;
}
<nb_perl3>"}"	{	// named back reference end
	DEBUG("NAMED_BACKREFERENCE_END" << endl);
	BEGIN(exp);
	return NAMED_BACKREFERENCE_END;
}
<nb_dotnet>"}"	{	// named back reference end
	DEBUG("NAMED_BACKREFERENCE_END" << endl);
	BEGIN(exp);
	return NAMED_BACKREFERENCE_END;
}
<nb_python>")"	{	// named back reference end
	DEBUG("NAMED_BACKREFERENCE_END" << endl);
	BEGIN(exp);
	return NAMED_BACKREFERENCE_END;
}
<nb_perl1,nb_perl2,nb_perl3,nb_dotnet,nb_python>[a-z]	{ // name of back reference
	yylval = yytext[1];
	DEBUG("ASCII " << yylval << endl);
	return ASCII;
}
<exp,class>\\0[0-9]{1,2}	{ // PCRE: After  \0  up  to two further octal digits are read.
	if( sscanf(yytext, "\\%o", &yylval) == 1 )
	{
		DEBUG("OCTAL " << yytext << endl);
		return OCTAL;
	}
}
<exp>"["	{ // start of character class
		DEBUG("LBOX" << endl);
		BEGIN(class);
		return LBOX;
}
<class>"^"	{ // negate class
		DEBUG("BOL" << endl);
		return BOL;
}
<class>\\[\\\-\[\]]	{ // speciální znaky \^-[] jako ASCII ve třídě znaků
			yylval = yytext[1];
			DEBUG("class: ASCII " << yylval << endl);
			return ASCII;
}
<class>"]"	{ // end of class
	DEBUG("RBOX" << endl);
	BEGIN(exp);
	return RBOX;
}
<class>\\x{HEX}-\\x{HEX} {
	DEBUG("CHARCLASS2VALUE HEX-HEX" << endl);
	// return 2 values - high and low boundary - shifted <<8
	unsigned int high, low;
	if(sscanf(yytext, "\\x%x-\\x%x", &low, &high) != 2)
		printf("character class error %s", yytext);
	if(low >= high)
		printf("character class error %s", yytext);

	yylval = (high << 8) + low;
	DEBUG((char)yylval << "-" << (char)(yylval >> 8) << endl);
	return INT;
}

<class>[^\]]-\\x{HEX} {
	DEBUG("CHARCLASS2VALUE char-HEX" << endl);
	// return 2 values - high and low boundary - shifted <<8
	char low;
	unsigned int high;
	if(sscanf(yytext, "%c-\\x%x", &low, &high) != 2)
		printf("character class error %s", yytext);
	if(low >= high)
		printf("character class error %s", yytext);

	yylval = (high << 8) + low;
	DEBUG((char)yylval << "-" << (char)(yylval >> 8) << endl);
	return INT;
}

<class>\\x{HEX}-[^-\]]	{
	DEBUG("CHARCLASS2VALUE HEX-char" << endl);
	// return 2 values - high and low boundary - shifted <<8
	char high;
	unsigned int low;
	if(sscanf(yytext, "\\x%x-%c", &low, &high) != 2)
		printf("character class error %s", yytext);
	if(low >= high)
		printf("character class error %s", yytext);

	yylval = (high << 8) + low;
	DEBUG((char)yylval << "-" << (char)(yylval >> 8) << endl);
	return INT;
}

<class>[^\]]-[^-\]]	{
	DEBUG("CHARCLASS2VALUE char-char" << endl);
	// return 2 values - high and low boundary - shifted <<8
	char high, low;
	if(sscanf(yytext, "%c-%c", &low, &high) != 2)
		printf("character class error %s", yytext);
	if(low >= high)
		printf("character class error %s", yytext);

	yylval = (high << 8) + low;
	DEBUG((char)yylval << "-" << (char)(yylval >> 8) << endl);
	return INT;
}
<class>"-"	{
		DEBUG("class: DASH" << endl);
		return DASH;
}
<exp,class>"[:alnum:]"	{
	DEBUG("P_ALNUM" << endl);
	return P_ALNUM;
}
<exp,class>"[:alpha:]"	{
	DEBUG("P_ALPHA" << endl);
	return P_ALPHA;
}
<exp,class>"[:ascii:]"	{
	DEBUG("P_ASCII" << endl);
	return P_ASCII;
}
<exp,class>"[:blank:]"	{
	DEBUG("P_BLANK" << endl);
	return P_BLANK;
}
<exp,class>"[:cntrl:]"	{
	DEBUG("P_CNTRL" << endl);
	return P_CNTRL;
}
<exp,class>"[:digit:]"	{
	DEBUG("P_DIGIT" << endl);
	return P_DIGIT;
}
<exp,class>"[:graph:]"	{
	DEBUG("P_GRAPH" << endl);
	return P_GRAPH;
}
<exp,class>"[:lower:]"	{
	DEBUG("P_LOWER" << endl);
	return P_LOWER;
}
<exp,class>"[:print:]"	{
	DEBUG("P_PRINT" << endl);
	return P_PRINT;
}
<exp,class>"[:punct:]"	{
	DEBUG("P_PUNCT" << endl);
	return P_PUNCT;
}
<exp,class>"[:space:]"	{
	DEBUG("P_SPACE" << endl);
	return P_SPACE;
}
<exp,class>"[:upper:]"	{
	DEBUG("P_UPPER" << endl);
	return P_UPPER;
}
<exp,class>"[:word:]"	{
	DEBUG("P_WORD" << endl);
	return P_WORD;
}
<exp,class>"[:xdigit:]"	{
	DEBUG("P_XDIGIT" << endl);
	return P_XDIGIT;
}
<exp,class>"[:^alnum:]"	{
	DEBUG("NP_ALNUM" << endl);
	return NP_ALNUM;
}
<exp,class>"[:^alpha:]"	{
	DEBUG("NP_ALPHA" << endl);
	return NP_ALPHA;
}
<exp,class>"[:^ascii:]"	{
	DEBUG("NP_ASCII" << endl);
	return NP_ASCII;
}
<exp,class>"[:^blank:]"	{
	DEBUG("NP_BLANK" << endl);
	return NP_BLANK;
}
<exp,class>"[:^cntrl:]"	{
	DEBUG("NP_CNTRL" << endl);
	return NP_CNTRL;
}
<exp,class>"[:^digit:]"	{
	DEBUG("NP_DIGIT" << endl);
	return NP_DIGIT;
}
<exp,class>"[:^graph:]"	{
	DEBUG("NP_GRAPH" << endl);
	return NP_GRAPH;
}
<exp,class>"[:^lower:]"	{
	DEBUG("NP_LOWER" << endl);
	return NP_LOWER;
}
<exp,class>"[:^print:]"	{
	DEBUG("NP_PRINT" << endl);
	return NP_PRINT;
}
<exp,class>"[:^punct:]"	{
	DEBUG("NP_PUNCT" << endl);
	return NP_PUNCT;
}
<exp,class>"[:^space:]"	{
	DEBUG("NP_SPACE" << endl);
	return NP_SPACE;
}
<exp,class>"[:^upper:]"	{
	DEBUG("NP_UPPER" << endl);
	return NP_UPPER;
}
<exp,class>"[:^word:]"	{
	DEBUG("NP_WORD" << endl);
	return NP_WORD;
}
<exp,class>"[:^xdigit:]"	{
	DEBUG("NP_XDIGIT" << endl);
	return NP_XDIGIT;
}
<class>.	{
		yylval = yytext[0];
		DEBUG("class: ASCII " << (char)yylval << endl);
		return ASCII;
	}
<exp>"/"	{
		DEBUG("SLASH" << endl);
		BEGIN(modif_rear);
		return SLASH;
	}
<modif_rear>i|m|s|x|.	{ // přepínače nakonci výrazu (a ostatní možnosti .)
	switch(yytext[0])
	{
		case 'i':
			return MODIF_CASELESS;
			break;
		case 'm':
			return MODIF_MULTILINE;
			break;
		case 's':
			return MODIF_DOTALL;
			break;
		case 'x':
			return MODIF_EXTENDED;
			break;
		case 'U':
			return MODIF_UNGREEDY;
			break;
		case 'R':
			return MODIF_R;
			break;
		case 'O':
			return MODIF_O;
			break;
		case 'P':
			return MODIF_P;
			break;
		case 'B':
			return MODIF_B;
			break;
		default:
			yylval = yytext[0];
			return ASCII;
	}
}
<exp>"(?R)"	{
	return SUBROUTINE_ALL;
}
<exp>\(\?[0-9]\)	{	// subroutine
	if( sscanf(yytext, "(?%d)", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_ABSOLUTE" << endl);
		return SUBROUTINE_ABSOLUTE;
	}
}
<exp>\\g<[0-9]>	{	// subroutine
	if( sscanf(yytext, "\\g<%d>", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_ABSOLUTE" << endl);
		return SUBROUTINE_ABSOLUTE;
	}
}
<exp>\\g\'[0-9]\'	{	// subroutine
	if( sscanf(yytext, "\\g'%d'", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_ABSOLUTE" << endl);
		return SUBROUTINE_ABSOLUTE;
	}
}
<exp>\(\?(\+|-)[0-9]\)	{	// subroutine
	if( sscanf(yytext, "(?%d)", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_RELATIVE" << endl);
		return SUBROUTINE_RELATIVE;
	}
}
<exp>\\g<(\+|-)[0-9]>	{	// subroutine
	if( sscanf(yytext, "\\g<%d>", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_RELATIVE" << endl);
		return SUBROUTINE_RELATIVE;
	}
}
<exp>"(?&"	{	// subroutine
	DEBUG("SUBROUTINE_NAME" << endl);
	BEGIN(srn_perl);
	return SUBROUTINE_NAME;
}
<exp>"(?P>"	{	// subroutine
	DEBUG("SUBROUTINE_NAME" << endl);
	BEGIN(srn_python);
	return SUBROUTINE_NAME;
}
<exp>"\g<"	{	// subroutine
	DEBUG("SUBROUTINE_NAME" << endl);
	BEGIN(srn_oniguruma1);
	return SUBROUTINE_NAME;
}
<exp>"\g'"	{	// subroutine
	DEBUG("SUBROUTINE_NAME" << endl);
	BEGIN(srn_oniguruma2);
	return SUBROUTINE_NAME;
}
<exp>\\g\'(\+|-)[0-9]\'	{	// subroutine
	if( sscanf(yytext, "\\g'%d'", &yylval) == 1 )
	{
		DEBUG("SUBROUTINE_RELATIVE" << endl);
		return SUBROUTINE_RELATIVE;
	}
}
<srn_perl,srn_python>")"	{
	BEGIN(exp);
	DEBUG("SUBROUTINE_NAME_END" << endl);
	return SUBROUTINE_NAME_END;
}
<srn_oniguruma1>">"	{
	BEGIN(exp);
	DEBUG("SUBROUTINE_NAME_END" << endl);
	return SUBROUTINE_NAME_END;
}
<srn_oniguruma2>">"	{
	BEGIN(exp);
	DEBUG("SUBROUTINE_NAME_END" << endl);
	return SUBROUTINE_NAME_END;
}
<srn_perl,srn_python,srn_oniguruma1,srn_oniguruma2>[a-z]	{
	DEBUG("ASCII" << endl);
	return ASCII;
}
<exp>"(?="	{
	return CAPTURING_POSAHEAD;
}
<exp>"(?!"	{
	return CAPTURING_NEGAHEAD;
}
<exp>"(?<="	{
	return CAPTURING_POSBEHIND;
}
<exp>"(?<!"	{
	return CAPTURING_NEGBEHIND;
}
<exp>"(?:"	{
	return CAPTURING_NON;
}
<exp>"(?|"	{
	return CAPTURING_NONRESET;
}
<exp>"(?>"	{
	return CAPTURING_ATOMIC;
}
<exp>"(?#"	{
	return CAPTURING_COMMENT;
}
<exp>"(?<"	{
	BEGIN(capturing_named_perl1);
	DEBUG("CAPTURING_NAMED" << endl);
	return CAPTURING_NAMED;
}
<exp>"(?'"	{
	BEGIN(capturing_named_perl2);
	DEBUG("CAPTURING_NAMED" << endl);
	return CAPTURING_NAMED;
}
<exp>"(?P<"	{
	BEGIN(capturing_named_python);
	DEBUG("CAPTURING_NAMED" << endl);
	return CAPTURING_NAMED;
}
<capturing_named_perl1,capturing_named_perl2,capturing_named_python>[a-z0-9]	{
	yylval = yytext[0];
	return ASCII;
}
<capturing_named_perl1,capturing_named_python>">"	{
	BEGIN(exp);
	return CAPTURING_NAMED_END;
}
<capturing_named_perl2>"'"	{
	BEGIN(exp);
	return CAPTURING_NAMED_END;
}
<exp>"(?"	{
	BEGIN(opt);
	DEBUG("OPTION" << endl);
	return OPTION;
}
<opt>i|m|s|x|\-|\)|.	{ // přepínače uprostřed výrazu (a ostatní možnosti .)
	switch(yytext[0])
	{
		case 'i':
			DEBUG("MODIF_CASELESS" << endl);
			return MODIF_CASELESS;
			break;
		case 'm':
			DEBUG("MODIF_MULTILINE" << endl);
			return MODIF_MULTILINE;
			break;
		case 's':
			DEBUG("MODIF_DOTALL" << endl);
			return MODIF_DOTALL;
			break;
		case 'x':
			DEBUG("MODIF_EXTENDED" << endl);
			return MODIF_EXTENDED;
			break;
		case 'J':
			DEBUG("MODIF_DUPNAMES" << endl);
			return MODIF_DUPNAMES;
			break;
		case 'U':
			DEBUG("MODIF_UNGREEDY" << endl);
			return MODIF_UNGREEDY;
			break;
		case '-':
			DEBUG("DASH" << endl);
			return DASH;
			break;
		case ')':
			BEGIN(exp);
			DEBUG("RBRA" << endl);
			return RBRA;
			break;
		default:
			yylval = yytext[0];
			DEBUG("ASCII " << (char)yylval << endl);
			return ASCII;
	}
}
<exp>"(*CR)"	{
		DEBUG("OPT_CR" << endl);
		return OPT_CR;
	}
<exp>"(*LF)"	{
		DEBUG("OPT_LF" << endl);
		return OPT_LF;
	}
<exp>"(*CRLF)"	{
		DEBUG("OPT_CRLF" << endl);
		return OPT_CRLF;
	}
<exp>"(*ANYCRLF)"	{
		DEBUG("OPT_ANYCRLF" << endl);
		return OPT_ANYCRLF;
	}
<exp>"(*ANY)"	{
		DEBUG("OPT_ANY_NEWLINE" << endl);
		return OPT_ANY_NEWLINE;
	}
<exp>"("	{
		DEBUG("LPAR" << endl);
		return LPAR;
	}
<exp>")"	{
		DEBUG("RPAR" << endl);
		return RPAR;
	}
<exp>"."	{
		DEBUG("ANY" << endl);
		return ANY;
	}
<exp>"?"	{
		DEBUG("ZEROONE" << endl);
		return ZEROONE;
	}
<exp>"+"	{
		DEBUG("ONEMORE" << endl);
		return ONEMORE;
	}
<exp>"*"	{
		DEBUG("ZEROMORE" << endl);
		return ZEROMORE;
	}
<exp>"|"	{
		DEBUG("OR" << endl);
		return OR;
	}
<exp>"$"	{
		DEBUG("EOL" << endl);
		return EOL;
	}
<exp>"^"	{
		DEBUG("BOL" << endl);
		return BOL;
	}
<exp>[[:space:]]	{
		DEBUG("ASCII SPACE" << yytext << endl);
		yylval = yytext[0];
		return SPACE;
	}
<exp>"]"	{ // outside class is ASCII
		yylval = yytext[0];
		DEBUG("ASCII " << (char)yylval << endl);
		return ASCII;
	}
<exp>.	{
		yylval = yytext[0];
		DEBUG("ASCII " << (char)yylval << endl);
		return ASCII;
	}
"("	{	/* úvodní modifikátory tvaru (modif)/pcre/ */
		DEBUG("(" << endl);
		BEGIN(modif_front);
	}
"/"	{	// pattern bez úvodního modifikátoru /pcre/
		DEBUG("SLASH" << endl);
		BEGIN(exp);
		return SLASH;
	}
.	{
		DEBUG("ASCII " << yytext << endl);
		yylval = yytext[0];
		return ASCII;
	}
%%

void flexReset() {
	BEGIN(INITIAL);
}
