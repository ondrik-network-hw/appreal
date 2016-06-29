/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_PCRE_TAB_H_INCLUDED
# define YY_YY_PCRE_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    LBRA = 258,
    RBRA = 259,
    INT = 260,
    COMMA = 261,
    LBOX = 262,
    RBOX = 263,
    SLASH = 264,
    LPAR = 265,
    RPAR = 266,
    ANY = 267,
    ZEROONE = 268,
    ONEMORE = 269,
    ZEROMORE = 270,
    DASH = 271,
    OR = 272,
    ASCII = 273,
    CHARCLASS2VALUE = 274,
    EOL = 275,
    BOL = 276,
    SPACE = 277,
    UTF8 = 278,
    UCP = 279,
    MODIF_CASELESS = 280,
    MODIF_MULTILINE = 281,
    MODIF_DOTALL = 282,
    MODIF_EXTENDED = 283,
    OPTION = 284,
    MODIF_DUPNAMES = 285,
    MODIF_UNGREEDY = 286,
    MODIF_R = 287,
    MODIF_O = 288,
    MODIF_P = 289,
    MODIF_B = 290,
    OPT_CR = 291,
    OPT_LF = 292,
    OPT_CRLF = 293,
    OPT_ANYCRLF = 294,
    OPT_ANY_NEWLINE = 295,
    DECDIGIT = 296,
    NDECDIGIT = 297,
    HWHITESPACE = 298,
    NHWHITESPACE = 299,
    WHITESPACE = 300,
    NWHITESPACE = 301,
    VWHITESPACE = 302,
    NVWHITESPACE = 303,
    WORDCHAR = 304,
    NWORDCHAR = 305,
    P_ALNUM = 306,
    P_ALPHA = 307,
    P_ASCII = 308,
    P_BLANK = 309,
    P_CNTRL = 310,
    P_DIGIT = 311,
    P_GRAPH = 312,
    P_LOWER = 313,
    P_PRINT = 314,
    P_PUNCT = 315,
    P_SPACE = 316,
    P_UPPER = 317,
    P_WORD = 318,
    P_XDIGIT = 319,
    NP_ALNUM = 320,
    NP_ALPHA = 321,
    NP_ASCII = 322,
    NP_BLANK = 323,
    NP_CNTRL = 324,
    NP_DIGIT = 325,
    NP_GRAPH = 326,
    NP_LOWER = 327,
    NP_PRINT = 328,
    NP_PUNCT = 329,
    NP_SPACE = 330,
    NP_UPPER = 331,
    NP_WORD = 332,
    NP_XDIGIT = 333,
    HEX = 334,
    OCTAL = 335,
    TAB = 336,
    CR = 337,
    LF = 338,
    FF = 339,
    ESC = 340,
    BEL = 341,
    CONTROLX = 342,
    BSR = 343,
    RESET = 344,
    ONEBYTE = 345,
    WORDBOUNDARY = 346,
    NWORDBOUNDARY = 347,
    STARTSUBJECT = 348,
    ENDSUBJECT = 349,
    OENDSUBJECT = 350,
    FIRSTPOSITION = 351,
    CAPTURING_NON = 352,
    CAPTURING_NONRESET = 353,
    CAPTURING_ATOMIC = 354,
    CAPTURING_COMMENT = 355,
    CAPTURING_NEGBEHIND = 356,
    CAPTURING_POSBEHIND = 357,
    CAPTURING_NEGAHEAD = 358,
    CAPTURING_POSAHEAD = 359,
    CAPTURING_NAMED = 360,
    CAPTURING_NAMED_END = 361,
    CHALSTART = 362,
    CHALEND = 363,
    BACKREFERENCE = 364,
    NAMED_BACKREFERENCE = 365,
    NAMED_BACKREFERENCE_END = 366,
    SUBROUTINE_ALL = 367,
    SUBROUTINE_NAME = 368,
    SUBROUTINE_NAME_END = 369,
    SUBROUTINE_ABSOLUTE = 370,
    SUBROUTINE_RELATIVE = 371
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_PCRE_TAB_H_INCLUDED  */
