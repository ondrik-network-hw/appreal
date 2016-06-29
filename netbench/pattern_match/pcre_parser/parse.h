#include "pcre.tab.h"
#include "interface.h"

extern int yyparse();
extern int yylex();
extern void yylex_destroy();
extern int yy_scan_string(const char *);


int parse(char *);
