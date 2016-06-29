/**
 * Rozhraní aplikace parseru PCRE
 * 
 * @date 2011-06-18
 * @author Milan Pála (xpalam00@stud.fit.vutbr.cz)
 */

#include "interface.h"

void module_init(T_CONFIG config)
{
}
void module_exit(int ret)
{
}
// pcre <<< modif_front pattern modif_rear
void pcre2modif_front_pattern_modif_rear(){
}
// modif_front <<< pcre_delim
void modif_front2pcre_delim(){
}
// modif_front <<< modif_front_ext-pcre_delim
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
}
// modif_front_unit <<< UCP
void modif_front_unit2UCP(){
}
// modif_rear <<< pcre_delim
void modif_rear2pcre_delim(){
}
// modif_rear <<< pcre_delim-modif_rear_ext
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
}
// modif_rear_unit <<< MODIF_MULTILINE
void modif_rear_unit2MODIF_MULTILINE(){
}
// modif_rear_unit <<< MODIF_DOTALL
void modif_rear_unit2MODIF_DOTALL(){
}
// modif_rear_unit <<< MODIF_EXTENDED
void modif_rear_unit2MODIF_EXTENDED(){
}
// modif_rear_unit <<< MODIF_UNGREEDY
void modif_rear_unit2MODIF_UNGREEDY(){
}
// modif_rear_unit <<< MODIF_R
void modif_rear_unit2MODIF_R(){
}
// modif_rear_unit <<< MODIF_O
void modif_rear_unit2MODIF_O(){
}
// modif_rear_unit <<< MODIF_P
void modif_rear_unit2MODIF_P(){
}
// modif_rear_unit <<< MODIF_B
void modif_rear_unit2MODIF_B(){
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
}
// inslash <<< bol-rv
void inslash2bol_rv(){
}
// inslash <<< rv-eol
void inslash2rv_eol(){
}
// inslash <<< bol-rv|eol
void inslash2bol_rv_eol(){
}
// rv <<< ext_exp
void rv2ext_exp(){
}
// rv <<< rv-or|rv
void rv2rv_or_rv(){
}
// rv <<< or-rv
void rv2or_rv(){
}
// rv <<< rv-or
void rv2rv_or(){
}
// ext_exp <<< exp
void ext_exp2exp(){
}
// ext_exp <<< bol-exp
void ext_exp2bol_exp(){
}
// ext_exp <<< exp-eol
void ext_exp2exp_eol(){
}
// ext_exp <<< bol-exp|eol
void ext_exp2bol_exp_eol(){
}
// bol <<< BOL
void bol2BOL(){
}
// eol <<< EOL
void eol2EOL(){
}
// exp <<< ext_unit
void exp2ext_unit(){
}
// exp <<< ext_unit-exp
void exp2ext_unit_exp(){
}
// ext_unit <<< unit
void ext_unit2unit(){
}
// ext_unit <<< quantify_unit
void ext_unit2quantify_unit(){
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
}
// quantifier <<< ZEROONE
void quantifier2ZEROONE(){
}
// quantifier <<< ONEMORE
void quantifier2ONEMORE(){
}
// quantifier <<< repeating
void quantifier2repeating(){
}
// possessive <<< ONEMORE
void possessive2ONEMORE(){
}
// lazy <<< ZEROONE
void lazy2ZEROONE(){
}
// or <<< OR
void or2OR(){
}
// unit <<< element
void unit2element(){
}
// unit <<< capturing
void unit2capturing(){
}
// unit <<< option
void unit2option(){
}
// unit <<< chal
void unit2chal(){
}
// unit <<< class
void unit2class(){
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
}
// option_set_unit <<< MODIF_DOTALL
void option_set_unit2MODIF_DOTALL(){
}
// option_set_unit <<< MODIF_EXTENDED
void option_set_unit2MODIF_EXTENDED(){
}
// option_set_unit <<< MODIF_MULTILINE
void option_set_unit2MODIF_MULTILINE(){
}
// option_set_unit <<< MODIF_DUPNAMES
void option_set_unit2MODIF_DUPNAMES(){
}
// option_set_unit <<< MODIF_UNGREEDY
void option_set_unit2MODIF_UNGREEDY(){
}
// option_unset <<< option_unset_unit
void option_unset2option_unset_unit(){
}
// option_unset <<< option_unset_unit-option_unset
void option_unset2option_unset_unit_option_unset(){
}
// option_unset_unit <<< MODIF_CASELESS
void option_unset_unit2MODIF_CASELESS(){
}
// option_unset_unit <<< MODIF_DOTALL
void option_unset_unit2MODIF_DOTALL(){
}
// option_unset_unit <<< MODIF_EXTENDED
void option_unset_unit2MODIF_EXTENDED(){
}
// option_unset_unit <<< MODIF_MULTILINE
void option_unset_unit2MODIF_MULTILINE(){
}
// option_unset_unit <<< MODIF_DUPNAMES
void option_unset_unit2MODIF_DUPNAMES(){
}
// option_unset_unit <<< MODIF_UNGREEDY
void option_unset_unit2MODIF_UNGREEDY(){
}
// element <<< ASCII
void element2ASCII(char c){
}
// element <<< ANY
void element2ANY(){
}
// element <<< SPACE
void element2SPACE(){
}
// element <<< hex
void element2hex(){
}
// element <<< TAB
void element2TAB(){
}
// element <<< CR
void element2CR(){
}
// element <<< LF
void element2LF(){
}
// element <<< FF
void element2FF(){
}
// element <<< BEL
void element2BEL(){
}
// element <<< ESC
void element2ESC(){
}
// element <<< CONTROLX
void element2CONTROLX(char c){
}
// element <<< BSR
void element2BSR(){
}
// element <<< RESET
void element2RESET(){
}
// element <<< assertions
void element2assertions(){
}
// element <<< ONEBYTE
void element2ONEBYTE(){
}
// element <<< OCTAL
void element2OCTAL(char c){
}
// element <<< backreference
void element2backreference(){
}
// element <<< subroutine
void element2subroutine(){
}
// assertions <<< WORDBOUNDARY
void assertions2WORDBOUNDARY(){
}
// assertions <<< NWORDBOUNDARY
void assertions2NWORDBOUNDARY(){
}
// assertions <<< STARTSUBJECT
void assertions2STARTSUBJECT(){
}
// assertions <<< ENDSUBJECT
void assertions2ENDSUBJECT(){
}
// assertions <<< OENDSUBJECT
void assertions2OENDSUBJECT(){
}
// assertions <<< FIRSTPOSITION
void assertions2FIRSTPOSITION(){
}
// hex <<< HEX
void hex2HEX(char c){
}
// newlinespec <<< newlinespec_unit
void newlinespec2newlinespec_unit(){
}
// newlinespec <<< newlinespec_unit-newlinespec
void newlinespec2newlinespec_unit_newlinespec(){
}
// newlinespec_unit <<< OPT_CR
void newlinespec_unit2OPT_CR(){
}
// newlinespec_unit <<< OPT_LF
void newlinespec_unit2OPT_LF(){
}
// newlinespec_unit <<< OPT_CRLF
void newlinespec_unit2OPT_CRLF(){
}
// newlinespec_unit <<< OPT_ANYCRLF
void newlinespec_unit2OPT_ANYCRLF(){
}
// newlinespec_unit <<< OPT_ANY_NEWLINE
void newlinespec_unit2OPT_ANY_NEWLINE(){
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
}
// capturing <<< capturingPosahead-rv|endCapturing
void capturing2capturingPosahead_rv_endCapturing(){
}
// capturing <<< capturingNegahead-rv|endCapturing
void capturing2capturingNegahead_rv_endCapturing(){
}
// capturing <<< capturingPosbehind-rv|endCapturing
void capturing2capturingPosbehind_rv_endCapturing(){
}
// capturing <<< capturingNegbehind-rv|endCapturing
void capturing2capturingNegbehind_rv_endCapturing(){
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
}
// interval <<< maximum
void interval2maximum(){
}
// minimum <<< INT
void minimum2INT(int i){
}
// maximum <<< INT
void maximum2INT(int i){
}
// intervalDelim <<< COMMA
void intervalDelim2COMMA(){
}
// class <<< classStart inclass classEnd
void class2classStart_inclass_classEnd(){
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
// classEnd <<< RBOX
void classEnd2RBOX(){
}
// slashcharclass <<< DECDIGIT
void slashcharclass2DECDIGIT(){
}
// slashcharclass <<< NDECDIGIT
void slashcharclass2NDECDIGIT(){
}
// slashcharclass <<< HWHITESPACE
void slashcharclass2HWHITESPACE(){
}
// slashcharclass <<< NHWHITESPACE
void slashcharclass2NHWHITESPACE(){
}
// slashcharclass <<< WHITESPACE
void slashcharclass2WHITESPACE(){
}
// slashcharclass <<< NWHITESPACE
void slashcharclass2NWHITESPACE(){
}
// slashcharclass <<< VWHITESPACE
void slashcharclass2VWHITESPACE(){
}
// slashcharclass <<< NVWHITESPACE
void slashcharclass2NVWHITESPACE(){
}
// slashcharclass <<< WORDCHAR
void slashcharclass2WORDCHAR(){
}
// slashcharclass <<< NWORDCHAR
void slashcharclass2NWORDCHAR(){
}
// inclass <<< inclass_ext_unit
void inclass2inclass_ext_unit(){
}
// inclass <<< bol-inclass_ext_unit
void inclass2bol_inclass_ext_unit(){
}
// inclass_ext_unit <<< inclass_unit
void inclass_ext_unit2inclass_unit(){
}
// inclass_ext_unit <<< inclass_unit-inclass_ext_unit
void inclass_ext_unit2inclass_unit_inclass_ext_unit(){
}
// inclass_unit <<< inclass_element
void inclass_unit2inclass_element(){
}
// inclass_unit <<< rangechars
void inclass_unit2rangechars(){
}
// inclass_unit <<< chal
void inclass_unit2chal(){
}
// inclass_element <<< ASCII
void inclass_element2ASCII(char c){
}
// inclass_element <<< posix_class
void inclass_element2posix_class(){
}
// inclass_element <<< slashcharclass
void inclass_element2slashcharclass(){
}
// inclass_element <<< hex
void inclass_element2hex(){
}
// inclass_element <<< TAB
void inclass_element2TAB(){
}
// inclass_element <<< CR
void inclass_element2CR(){
}
// inclass_element <<< LF
void inclass_element2LF(){
}
// inclass_element <<< FF
void inclass_element2FF(){
}
// inclass_element <<< BEL
void inclass_element2BEL(){
}
// inclass_element <<< ESC
void inclass_element2ESC(){
}
// inclass_element <<< CONTROLX
void inclass_element2CONTROLX(char c){
}
// inclass_element <<< RESET
void inclass_element2RESET(){
}
// inclass_element <<< OCTAL
void inclass_element2OCTAL(char c){
}
// inclass_element <<< DASH
void inclass_element2DASH(){
}
// rangechars <<< INT
void rangechars2INT(int i){
}
// dash <<< DASH
void dash2DASH(){
}
// posix_class <<< P_ALNUM
void posix_class2P_ALNUM(){
}
// posix_class <<< P_ALPHA
void posix_class2P_ALPHA(){
}
// posix_class <<< P_ASCII
void posix_class2P_ASCII(){
}
// posix_class <<< P_BLANK
void posix_class2P_BLANK(){
}
// posix_class <<< P_CNTRL
void posix_class2P_CNTRL(){
}
// posix_class <<< P_DIGIT
void posix_class2P_DIGIT(){
}
// posix_class <<< P_GRAPH
void posix_class2P_GRAPH(){
}
// posix_class <<< P_LOWER
void posix_class2P_LOWER(){
}
// posix_class <<< P_PRINT
void posix_class2P_PRINT(){
}
// posix_class <<< P_PUNCT
void posix_class2P_PUNCT(){
}
// posix_class <<< P_SPACE
void posix_class2P_SPACE(){
}
// posix_class <<< P_UPPER
void posix_class2P_UPPER(){
}
// posix_class <<< P_WORD
void posix_class2P_WORD(){
}
// posix_class <<< P_XDIGIT
void posix_class2P_XDIGIT(){
}
// posix_class <<< posix_class_neg
void posix_class2posix_class_neg(){
}
// posix_class_neg <<< NP_ALNUM
void posix_class_neg2NP_ALNUM(){
}
// posix_class_neg <<< NP_ALPHA
void posix_class_neg2NP_ALPHA(){
}
// posix_class_neg <<< NP_ASCII
void posix_class_neg2NP_ASCII(){
}
// posix_class_neg <<< NP_BLANK
void posix_class_neg2NP_BLANK(){
}
// posix_class_neg <<< NP_CNTRL
void posix_class_neg2NP_CNTRL(){
}
// posix_class_neg <<< NP_DIGIT
void posix_class_neg2NP_DIGIT(){
}
// posix_class_neg <<< NP_GRAPH
void posix_class_neg2NP_GRAPH(){
}
// posix_class_neg <<< NP_LOWER
void posix_class_neg2NP_LOWER(){
}
// posix_class_neg <<< NP_PRINT
void posix_class_neg2NP_PRINT(){
}
// posix_class_neg <<< NP_PUNCT
void posix_class_neg2NP_PUNCT(){
}
// posix_class_neg <<< NP_SPACE
void posix_class_neg2NP_SPACE(){
}
// posix_class_neg <<< NP_UPPER
void posix_class_neg2NP_UPPER(){
}
// posix_class_neg <<< NP_WORD
void posix_class_neg2NP_WORD(){
}
// posix_class_neg <<< NP_XDIGIT
void posix_class_neg2NP_XDIGIT(){
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
