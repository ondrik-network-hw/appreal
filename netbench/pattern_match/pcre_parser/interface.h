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
void pcre2modif_front_pattern_modif_rear();

void modif_front2pcre_delim();
void modif_front2modif_front_ext_pcre_delim();

void modif_front_ext2modif_front_unit();
void modif_front_ext2modif_front_unit_modif_front_ext();

void modif_front_unit2UTF8();
void modif_front_unit2UCP();

void modif_rear2pcre_delim();
void modif_rear2pcre_delim_modif_rear_ext();

void modif_rear_ext2modif_rear_unit();
void modif_rear_ext2modif_rear_unit_modif_rear_ext();

void modif_rear_unit2MODIF_CASELESS();
void modif_rear_unit2MODIF_MULTILINE();
void modif_rear_unit2MODIF_DOTALL();
void modif_rear_unit2MODIF_EXTENDED();
void modif_rear_unit2MODIF_UNGREEDY();
void modif_rear_unit2MODIF_R();
void modif_rear_unit2MODIF_O();
void modif_rear_unit2MODIF_P();
void modif_rear_unit2MODIF_B();

void pcre_delim2SLASH();

void pattern2newlinespec_inslash();
void pattern2inslash();

void inslash2rv();
void inslash2bol_rv();
void inslash2rv_eol();
void inslash2bol_rv_eol();

void rv2ext_exp();
void rv2rv_or_rv();
void rv2or_rv();
void rv2rv_or();

void ext_exp2exp();
void ext_exp2bol_exp();
void ext_exp2exp_eol();
void ext_exp2bol_exp_eol();

void bol2BOL();

void eol2EOL();

void exp2ext_unit();
void exp2ext_unit_exp();

void ext_unit2unit();
void ext_unit2quantify_unit();

void quantify_unit2unit_quantify();

void quantify2quantifier();
void quantify2quantifier_possessive();
void quantify2quantifier_lazy();

void quantifier2ZEROMORE();
void quantifier2ZEROONE();
void quantifier2ONEMORE();
void quantifier2repeating();

void possessive2ONEMORE();

void lazy2ZEROONE();

void or2OR();

void unit2element();
void unit2capturing();
void unit2option();
void unit2chal();
void unit2class();

void option2optionStart_option_set_optionEnd();
void option2optionStart_option_unset_group_optionEnd();
void option2optionStart_option_set_option_unset_group_optionEnd();

void optionStart2OPTION();

void optionEnd2RBRA();

void option_unset_group2dash_option_unset();

void option_set2option_set_unit();
void option_set2option_set_unit_option_set();

void option_set_unit2MODIF_CASELESS();
void option_set_unit2MODIF_DOTALL();
void option_set_unit2MODIF_EXTENDED();
void option_set_unit2MODIF_MULTILINE();
void option_set_unit2MODIF_DUPNAMES();
void option_set_unit2MODIF_UNGREEDY();

void option_unset2option_unset_unit();
void option_unset2option_unset_unit_option_unset();

void option_unset_unit2MODIF_CASELESS();
void option_unset_unit2MODIF_DOTALL();
void option_unset_unit2MODIF_EXTENDED();
void option_unset_unit2MODIF_MULTILINE();
void option_unset_unit2MODIF_DUPNAMES();
void option_unset_unit2MODIF_UNGREEDY();

void element2ASCII(char c);
void element2ANY();
void element2SPACE();
void element2hex();
void element2TAB();
void element2CR();
void element2LF();
void element2FF();
void element2BEL();
void element2ESC();
void element2CONTROLX(char c);
void element2BSR();
void element2RESET();
void element2assertions();
void element2ONEBYTE();
void element2OCTAL(char c);
void element2backreference();
void element2subroutine();

void assertions2WORDBOUNDARY();
void assertions2NWORDBOUNDARY();
void assertions2STARTSUBJECT();
void assertions2ENDSUBJECT();
void assertions2OENDSUBJECT();
void assertions2FIRSTPOSITION();

void hex2HEX(char c);

void newlinespec2newlinespec_unit();
void newlinespec2newlinespec_unit_newlinespec();

void newlinespec_unit2OPT_CR();
void newlinespec_unit2OPT_LF();
void newlinespec_unit2OPT_CRLF();
void newlinespec_unit2OPT_ANYCRLF();
void newlinespec_unit2OPT_ANY_NEWLINE();

void capturing2startCapturing_rv_endCapturing();
void capturing2capturingNamed_capturingName_capturingNameEnd_rv_endCapturing();
void capturing2capturingNon_rv_endCapturing();
void capturing2capturingNonreset_rv_endCapturing();
void capturing2capturingAtomic_rv_endCapturing();
void capturing2capturingComment_rv_endCapturing();
void capturing2capturingPosahead_rv_endCapturing();
void capturing2capturingNegahead_rv_endCapturing();
void capturing2capturingPosbehind_rv_endCapturing();
void capturing2capturingNegbehind_rv_endCapturing();

void capturingNamed2CAPTURING_NAMED();

void capturingName2capturingNameAdd();
void capturingName2capturingNameAdd_capturingName();

void capturingNameAdd2ASCII(char c);

void capturingNon2CAPTURING_NON();

void capturingNonreset2CAPTURING_NONRESET();

void capturingAtomic2CAPTURING_ATOMIC();

void capturingComment2CAPTURING_COMMENT();

void capturingPosahead2CAPTURING_POSAHEAD();

void capturingNegahead2CAPTURING_NEGAHEAD();

void capturingPosbehind2CAPTURING_POSBEHIND();

void capturingNegbehind2CAPTURING_NEGBEHIND();

void capturingNameEnd2CAPTURING_NAMED_END();

void startCapturing2LPAR();

void endCapturing2RPAR();

void repeating2startRepeating_interval_endRepeating();

void startRepeating2LBRA();

void endRepeating2RBRA();

void interval2minimum_intervalDelim_maximum();
void interval2minimum_intervalDelim();
void interval2maximum();

void minimum2INT(int i);

void maximum2INT(int i);

void intervalDelim2COMMA();

void class2classStart_inclass_classEnd();
void class2slashcharclass();
void class2posix_class();

void classStart2LBOX();

void classEnd2RBOX();

void slashcharclass2DECDIGIT();
void slashcharclass2NDECDIGIT();
void slashcharclass2HWHITESPACE();
void slashcharclass2NHWHITESPACE();
void slashcharclass2WHITESPACE();
void slashcharclass2NWHITESPACE();
void slashcharclass2VWHITESPACE();
void slashcharclass2NVWHITESPACE();
void slashcharclass2WORDCHAR();
void slashcharclass2NWORDCHAR();

void inclass2inclass_ext_unit();
void inclass2bol_inclass_ext_unit();

void inclass_ext_unit2inclass_unit();
void inclass_ext_unit2inclass_unit_inclass_ext_unit();

void inclass_unit2inclass_element();
void inclass_unit2rangechars();
void inclass_unit2chal();

void inclass_element2ASCII(char c);
void inclass_element2posix_class();
void inclass_element2slashcharclass();
void inclass_element2hex();
void inclass_element2TAB();
void inclass_element2CR();
void inclass_element2LF();
void inclass_element2FF();
void inclass_element2BEL();
void inclass_element2ESC();
void inclass_element2CONTROLX(char c);
void inclass_element2RESET();
void inclass_element2OCTAL(char c);
void inclass_element2DASH();

void rangechars2INT(int i);

void dash2DASH();

void posix_class2P_ALNUM();
void posix_class2P_ALPHA();
void posix_class2P_ASCII();
void posix_class2P_BLANK();
void posix_class2P_CNTRL();
void posix_class2P_DIGIT();
void posix_class2P_GRAPH();
void posix_class2P_LOWER();
void posix_class2P_PRINT();
void posix_class2P_PUNCT();
void posix_class2P_SPACE();
void posix_class2P_UPPER();
void posix_class2P_WORD();
void posix_class2P_XDIGIT();
void posix_class2posix_class_neg();

void posix_class_neg2NP_ALNUM();
void posix_class_neg2NP_ALPHA();
void posix_class_neg2NP_ASCII();
void posix_class_neg2NP_BLANK();
void posix_class_neg2NP_CNTRL();
void posix_class_neg2NP_DIGIT();
void posix_class_neg2NP_GRAPH();
void posix_class_neg2NP_LOWER();
void posix_class_neg2NP_PRINT();
void posix_class_neg2NP_PUNCT();
void posix_class_neg2NP_SPACE();
void posix_class_neg2NP_UPPER();
void posix_class_neg2NP_WORD();
void posix_class_neg2NP_XDIGIT();

void chal2chalStart_inchal_chalEnd();

void chalStart2CHALSTART();

void chalEnd2CHALEND();

void inchal2inchalExtUnit();
void inchal2inchalExtUnit_inchal();

void inchalExtUnit2inchalUnit();

void inchalUnit2ASCII(char c);

void backreference2BACKREFERENCE();
void backreference2named_back_reference();

void named_back_reference2nbrStart_inNbr_nbrEnd();

void nbrStart2NAMED_BACKREFERENCE();

void nbrEnd2NAMED_BACKREFERENCE_END();

void inNbr2inNbrUnit();
void inNbr2inNbrUnit_inNbr();

void inNbrUnit2ASCII(char c);

void subroutine2SUBROUTINE_ALL();
void subroutine2SUBROUTINE_ABSOLUTE();
void subroutine2SUBROUTINE_RELATIVE();
void subroutine2named_subroutine();

void named_subroutine2nsrStart_inNsr_nsrEnd();

void nsrStart2SUBROUTINE_NAME();

void nsrEnd2SUBROUTINE_NAME_END();

void inNsr2inNsrUnit();
void inNsr2inNsrUnit_inNsr();

void inNsrUnit2ASCII(char c);

#endif

