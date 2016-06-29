/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* Copy the first part of user declarations.  */
#line 5 "pcre.gen.y" /* yacc.c:339  */

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


#line 86 "pcre.tab.c" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* In a future release of Bison, this section will be replaced
   by #include "pcre.tab.h".  */
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

/* Copy the second part of user declarations.  */

#line 254 "pcre.tab.c" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  9
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   657

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  117
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  89
/* YYNRULES -- Number of rules.  */
#define YYNRULES  238
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  288

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   371

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    46,    46,    52,    53,    56,    57,    63,    64,    67,
      68,    71,    72,    82,    83,    84,    85,    86,    87,    88,
      89,    90,    93,    96,    97,   103,   104,   105,   106,   109,
     110,   111,   112,   115,   116,   117,   118,   121,   124,   127,
     128,   135,   136,   139,   142,   143,   144,   153,   154,   155,
     156,   159,   162,   166,   174,   175,   176,   177,   178,   186,
     187,   188,   191,   194,   200,   203,   204,   207,   208,   209,
     210,   211,   212,   215,   216,   219,   220,   221,   222,   223,
     224,   246,   247,   248,   249,   250,   251,   252,   253,   254,
     255,   256,   257,   258,   259,   260,   261,   262,   263,   276,
     277,   278,   279,   280,   281,   284,   288,   289,   292,   293,
     294,   295,   296,   314,   315,   316,   317,   318,   319,   320,
     321,   322,   323,   327,   330,   331,   334,   337,   340,   343,
     346,   349,   352,   355,   358,   364,   368,   371,   375,   378,
     381,   390,   391,   392,   395,   398,   401,   410,   411,   412,
     415,   418,   433,   434,   435,   436,   437,   438,   439,   440,
     441,   442,   450,   451,   458,   459,   462,   463,   464,   483,
     484,   485,   486,   487,   488,   489,   490,   491,   492,   493,
     494,   495,   496,   500,   503,   507,   508,   509,   510,   511,
     512,   513,   514,   515,   516,   517,   518,   519,   520,   521,
     524,   525,   526,   527,   528,   529,   530,   531,   532,   533,
     534,   535,   536,   537,   541,   544,   547,   550,   551,   554,
     557,   560,   561,   564,   567,   570,   573,   574,   577,   580,
     581,   582,   583,   586,   589,   592,   595,   596,   599
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 0
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "LBRA", "RBRA", "INT", "COMMA", "LBOX",
  "RBOX", "SLASH", "LPAR", "RPAR", "ANY", "ZEROONE", "ONEMORE", "ZEROMORE",
  "DASH", "OR", "ASCII", "CHARCLASS2VALUE", "EOL", "BOL", "SPACE", "UTF8",
  "UCP", "MODIF_CASELESS", "MODIF_MULTILINE", "MODIF_DOTALL",
  "MODIF_EXTENDED", "OPTION", "MODIF_DUPNAMES", "MODIF_UNGREEDY",
  "MODIF_R", "MODIF_O", "MODIF_P", "MODIF_B", "OPT_CR", "OPT_LF",
  "OPT_CRLF", "OPT_ANYCRLF", "OPT_ANY_NEWLINE", "DECDIGIT", "NDECDIGIT",
  "HWHITESPACE", "NHWHITESPACE", "WHITESPACE", "NWHITESPACE",
  "VWHITESPACE", "NVWHITESPACE", "WORDCHAR", "NWORDCHAR", "P_ALNUM",
  "P_ALPHA", "P_ASCII", "P_BLANK", "P_CNTRL", "P_DIGIT", "P_GRAPH",
  "P_LOWER", "P_PRINT", "P_PUNCT", "P_SPACE", "P_UPPER", "P_WORD",
  "P_XDIGIT", "NP_ALNUM", "NP_ALPHA", "NP_ASCII", "NP_BLANK", "NP_CNTRL",
  "NP_DIGIT", "NP_GRAPH", "NP_LOWER", "NP_PRINT", "NP_PUNCT", "NP_SPACE",
  "NP_UPPER", "NP_WORD", "NP_XDIGIT", "HEX", "OCTAL", "TAB", "CR", "LF",
  "FF", "ESC", "BEL", "CONTROLX", "BSR", "RESET", "ONEBYTE",
  "WORDBOUNDARY", "NWORDBOUNDARY", "STARTSUBJECT", "ENDSUBJECT",
  "OENDSUBJECT", "FIRSTPOSITION", "CAPTURING_NON", "CAPTURING_NONRESET",
  "CAPTURING_ATOMIC", "CAPTURING_COMMENT", "CAPTURING_NEGBEHIND",
  "CAPTURING_POSBEHIND", "CAPTURING_NEGAHEAD", "CAPTURING_POSAHEAD",
  "CAPTURING_NAMED", "CAPTURING_NAMED_END", "CHALSTART", "CHALEND",
  "BACKREFERENCE", "NAMED_BACKREFERENCE", "NAMED_BACKREFERENCE_END",
  "SUBROUTINE_ALL", "SUBROUTINE_NAME", "SUBROUTINE_NAME_END",
  "SUBROUTINE_ABSOLUTE", "SUBROUTINE_RELATIVE", "$accept", "pcre",
  "modif_front", "modif_front_ext", "modif_front_unit", "modif_rear",
  "modif_rear_ext", "modif_rear_unit", "pcre_delim", "pattern", "inslash",
  "rv", "ext_exp", "bol", "eol", "exp", "ext_unit", "quantify_unit",
  "quantify", "quantifier", "possessive", "lazy", "or", "unit", "option",
  "optionStart", "optionEnd", "option_unset_group", "option_set",
  "option_set_unit", "option_unset", "option_unset_unit", "element",
  "assertions", "hex", "newlinespec", "newlinespec_unit", "capturing",
  "capturingNamed", "capturingName", "capturingNameAdd", "capturingNon",
  "capturingNonreset", "capturingAtomic", "capturingComment",
  "capturingPosahead", "capturingNegahead", "capturingPosbehind",
  "capturingNegbehind", "capturingNameEnd", "startCapturing",
  "endCapturing", "repeating", "startRepeating", "endRepeating",
  "interval", "minimum", "maximum", "intervalDelim", "class", "classStart",
  "classEnd", "slashcharclass", "inclass", "inclass_ext_unit",
  "inclass_unit", "inclass_element", "rangechars", "dash", "posix_class",
  "posix_class_neg", "chal", "chalStart", "chalEnd", "inchal",
  "inchalExtUnit", "inchalUnit", "backreference", "named_back_reference",
  "nbrStart", "nbrEnd", "inNbr", "inNbrUnit", "subroutine",
  "named_subroutine", "nsrStart", "nsrEnd", "inNsr", "inNsrUnit", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371
};
# endif

#define YYPACT_NINF -169

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-169)))

#define YYTABLE_NINF -146

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
      36,  -169,  -169,  -169,     3,   152,    39,    16,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,    39,  -169,    44,  -169,   259,
      30,   366,  -169,   259,    53,  -169,    27,  -169,  -169,  -169,
     259,    72,  -169,    47,   259,   259,   259,   259,   259,   259,
     259,   259,   259,  -169,   467,  -169,  -169,  -169,  -169,    56,
    -169,  -169,    57,  -169,  -169,    75,  -169,  -169,  -169,    92,
    -169,  -169,   259,    44,   366,    30,  -169,  -169,    45,  -169,
    -169,  -169,  -169,  -169,    59,  -169,    65,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,    90,    26,     7,    61,  -169,  -169,
    -169,   -10,    47,    52,    52,    52,    52,    52,    52,    52,
      52,    52,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,   550,  -169,  -169,    89,  -169,   550,
    -169,  -169,  -169,  -169,  -169,     5,    56,  -169,  -169,   -13,
      57,  -169,    -9,    75,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,    92,    45,  -169,    30,  -169,  -169,
    -169,  -169,  -169,   110,   111,   116,  -169,  -169,  -169,  -169,
      90,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,    61,
    -169,   259,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,   124,  -169,  -169,    52,  -169,  -169,  -169
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,    22,     7,     8,     0,     0,     0,     5,     3,     1,
     150,   136,    82,    53,    81,    37,    83,    62,   108,   109,
     110,   111,   112,   152,   153,   154,   155,   156,   157,   158,
     159,   160,   161,   185,   186,   187,   188,   189,   190,   191,
     192,   193,   194,   195,   196,   197,   198,   200,   201,   202,
     203,   204,   205,   206,   207,   208,   209,   210,   211,   212,
     213,   105,    96,    85,    86,    87,    88,    90,    89,    91,
      92,    93,    95,    99,   100,   101,   102,   103,   104,   127,
     128,   129,   130,   134,   133,   132,   131,   123,   215,   221,
     224,   229,   234,   230,   231,     0,    24,    25,    29,     0,
      33,    39,    42,     0,    41,    56,     0,    54,    94,    84,
       0,   106,    55,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    58,     0,   148,   149,   199,    57,     0,
      97,   222,     0,    98,   232,     0,     4,     6,     2,     9,
      38,    27,    32,    26,     0,    33,    35,    40,    31,   139,
      48,    49,    47,    43,    44,    50,     0,   184,    67,    70,
      68,    69,    71,    72,     0,     0,    65,     0,    23,   107,
     126,     0,   124,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   183,   182,   169,   181,   173,   174,   175,   176,
     178,   177,   179,   180,     0,   172,   171,     0,   162,   164,
     166,   167,   170,   168,   220,     0,   217,   219,   228,     0,
     226,   238,     0,   236,    13,    14,    15,    16,    17,    18,
      19,    20,    21,    10,    11,    30,    28,    34,    35,    52,
      51,    45,    46,   144,     0,     0,   143,    63,    60,    59,
       0,    66,    75,    78,    76,    77,    79,    80,    64,    73,
     135,     0,   125,   137,   115,   116,   117,   118,   119,   120,
     121,   122,   113,   163,   151,   147,   165,   216,   214,   218,
     225,   223,   227,   235,   233,   237,    12,    36,   140,   138,
     146,   142,    61,    74,     0,   145,   141,   114
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -169,  -169,  -169,   123,  -169,  -169,   -92,  -169,     8,  -169,
      23,   -98,  -169,    -3,   -96,   -73,  -169,  -169,  -169,  -169,
    -169,  -169,   -97,  -169,  -169,  -169,  -138,   -31,   -30,  -169,
    -114,  -169,  -169,  -169,  -109,    28,  -169,  -169,  -169,   -35,
    -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,  -169,
    -169,  -168,  -169,  -169,  -169,  -169,  -169,  -143,  -169,  -169,
    -169,  -169,   -99,  -169,  -158,  -169,  -169,  -169,  -169,   -95,
    -169,   -93,  -169,  -169,   -66,  -169,  -169,  -169,  -169,  -169,
    -169,   -69,  -169,  -169,  -169,  -169,  -169,   -71,  -169
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     4,     5,     6,     7,   138,   223,   224,     8,    95,
      96,    97,    98,   144,   141,   100,   101,   102,   153,   154,
     231,   232,   103,   104,   105,   106,   238,   164,   165,   166,
     248,   249,   107,   108,   109,   110,   111,   112,   113,   171,
     172,   114,   115,   116,   117,   118,   119,   120,   121,   251,
     122,   254,   155,   156,   279,   234,   235,   236,   281,   123,
     124,   265,   125,   197,   198,   199,   200,   201,   167,   126,
     127,   128,   129,   268,   205,   206,   207,   130,   131,   132,
     271,   209,   210,   133,   134,   135,   274,   212,   213
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
     142,   143,    99,     9,   146,   148,   255,   256,   257,   258,
     259,   260,   261,   262,   136,   195,   173,   174,   175,   176,
     177,   178,   179,   180,   181,   196,   145,   239,   147,   202,
     237,   203,   158,   159,   160,   161,   263,   162,   163,     2,
       3,   266,   157,   157,   225,     1,   142,   226,     1,   228,
     140,   142,   158,   159,   160,   161,   149,   162,   163,     2,
       3,    13,    13,   253,   140,   170,   150,   151,   152,    13,
     233,   227,   229,   230,   204,   208,   142,   142,   142,   142,
     142,   142,   142,   142,   142,   195,   242,   243,   244,   245,
     195,   246,   247,   211,   237,   196,   250,   264,   270,   202,
     196,   203,   282,   139,   202,   273,   203,    99,    18,    19,
      20,    21,    22,   267,  -145,   278,   287,   214,   215,   216,
     217,   194,   280,   218,   219,   220,   221,   222,   142,   285,
     137,   277,   276,   168,   240,   283,   241,   252,   286,   169,
     269,   272,   275,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,   284,     0,     0,     0,     0,     0,    10,
       0,     0,    11,     0,    12,     0,     0,     0,     0,    13,
      14,     0,     0,    15,    16,     0,     0,     0,     0,     0,
       0,    17,     0,     0,     0,     0,     0,   142,    18,    19,
      20,    21,    22,    23,    24,    25,    26,    27,    28,    29,
      30,    31,    32,    33,    34,    35,    36,    37,    38,    39,
      40,    41,    42,    43,    44,    45,    46,    47,    48,    49,
      50,    51,    52,    53,    54,    55,    56,    57,    58,    59,
      60,    61,    62,    63,    64,    65,    66,    67,    68,    69,
      70,    71,    72,    73,    74,    75,    76,    77,    78,    79,
      80,    81,    82,    83,    84,    85,    86,    87,     0,    88,
       0,    89,    90,     0,    91,    92,    10,    93,    94,    11,
       0,    12,     0,     0,     0,     0,    13,    14,     0,     0,
      15,    16,     0,     0,     0,     0,     0,     0,    17,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      23,    24,    25,    26,    27,    28,    29,    30,    31,    32,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
      63,    64,    65,    66,    67,    68,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,     0,    88,     0,    89,    90,
       0,    91,    92,    10,    93,    94,    11,     0,    12,     0,
       0,     0,     0,     0,    14,     0,     0,     0,    16,     0,
       0,     0,     0,     0,     0,    17,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,    23,    24,    25,
      26,    27,    28,    29,    30,    31,    32,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,    65,
      66,    67,    68,    69,    70,    71,    72,    73,    74,    75,
      76,    77,    78,    79,    80,    81,    82,    83,    84,    85,
      86,    87,   182,    88,     0,    89,    90,     0,    91,    92,
       0,    93,    94,   183,     0,   184,     0,     0,    15,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,   185,   186,   187,
     188,   189,   190,   191,   192,   182,   193,     0,     0,     0,
       0,     0,     0,     0,     0,     0,   183,     0,   184,     0,
       0,     0,     0,     0,    88,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,    23,    24,    25,    26,    27,    28,    29,    30,    31,
      32,    33,    34,    35,    36,    37,    38,    39,    40,    41,
      42,    43,    44,    45,    46,    47,    48,    49,    50,    51,
      52,    53,    54,    55,    56,    57,    58,    59,    60,    61,
     185,   186,   187,   188,   189,   190,   191,   192,     0,   193,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,    88
};

static const yytype_int16 yycheck[] =
{
      97,    99,     5,     0,   100,   103,   174,   175,   176,   177,
     178,   179,   180,   181,     6,   124,   114,   115,   116,   117,
     118,   119,   120,   121,   122,   124,    99,   165,   101,   124,
       4,   124,    25,    26,    27,    28,   194,    30,    31,    23,
      24,   199,    16,    16,   142,     9,   143,   143,     9,   145,
      20,   148,    25,    26,    27,    28,     3,    30,    31,    23,
      24,    17,    17,    11,    20,    18,    13,    14,    15,    17,
       5,   144,    13,    14,    18,    18,   173,   174,   175,   176,
     177,   178,   179,   180,   181,   194,    25,    26,    27,    28,
     199,    30,    31,    18,     4,   194,   106,     8,   111,   194,
     199,   194,   240,    95,   199,   114,   199,   110,    36,    37,
      38,    39,    40,   108,     4,     4,   284,    25,    26,    27,
      28,   124,     6,    31,    32,    33,    34,    35,   225,     5,
       7,   227,   224,   110,   165,   249,   166,   172,   281,   111,
     206,   210,   213,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,   251,    -1,    -1,    -1,    -1,    -1,     7,
      -1,    -1,    10,    -1,    12,    -1,    -1,    -1,    -1,    17,
      18,    -1,    -1,    21,    22,    -1,    -1,    -1,    -1,    -1,
      -1,    29,    -1,    -1,    -1,    -1,    -1,   284,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    46,    47,
      48,    49,    50,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    61,    62,    63,    64,    65,    66,    67,
      68,    69,    70,    71,    72,    73,    74,    75,    76,    77,
      78,    79,    80,    81,    82,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,    93,    94,    95,    96,    97,
      98,    99,   100,   101,   102,   103,   104,   105,    -1,   107,
      -1,   109,   110,    -1,   112,   113,     7,   115,   116,    10,
      -1,    12,    -1,    -1,    -1,    -1,    17,    18,    -1,    -1,
      21,    22,    -1,    -1,    -1,    -1,    -1,    -1,    29,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      41,    42,    43,    44,    45,    46,    47,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,    66,    67,    68,    69,    70,
      71,    72,    73,    74,    75,    76,    77,    78,    79,    80,
      81,    82,    83,    84,    85,    86,    87,    88,    89,    90,
      91,    92,    93,    94,    95,    96,    97,    98,    99,   100,
     101,   102,   103,   104,   105,    -1,   107,    -1,   109,   110,
      -1,   112,   113,     7,   115,   116,    10,    -1,    12,    -1,
      -1,    -1,    -1,    -1,    18,    -1,    -1,    -1,    22,    -1,
      -1,    -1,    -1,    -1,    -1,    29,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    41,    42,    43,
      44,    45,    46,    47,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    66,    67,    68,    69,    70,    71,    72,    73,
      74,    75,    76,    77,    78,    79,    80,    81,    82,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,    93,
      94,    95,    96,    97,    98,    99,   100,   101,   102,   103,
     104,   105,     5,   107,    -1,   109,   110,    -1,   112,   113,
      -1,   115,   116,    16,    -1,    18,    -1,    -1,    21,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    41,    42,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
      63,    64,    65,    66,    67,    68,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,     5,    89,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    16,    -1,    18,    -1,
      -1,    -1,    -1,    -1,   107,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    41,    42,    43,    44,    45,    46,    47,    48,    49,
      50,    51,    52,    53,    54,    55,    56,    57,    58,    59,
      60,    61,    62,    63,    64,    65,    66,    67,    68,    69,
      70,    71,    72,    73,    74,    75,    76,    77,    78,    79,
      80,    81,    82,    83,    84,    85,    86,    87,    -1,    89,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,   107
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     9,    23,    24,   118,   119,   120,   121,   125,     0,
       7,    10,    12,    17,    18,    21,    22,    29,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    46,    47,
      48,    49,    50,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    61,    62,    63,    64,    65,    66,    67,
      68,    69,    70,    71,    72,    73,    74,    75,    76,    77,
      78,    79,    80,    81,    82,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,    93,    94,    95,    96,    97,
      98,    99,   100,   101,   102,   103,   104,   105,   107,   109,
     110,   112,   113,   115,   116,   126,   127,   128,   129,   130,
     132,   133,   134,   139,   140,   141,   142,   149,   150,   151,
     152,   153,   154,   155,   158,   159,   160,   161,   162,   163,
     164,   165,   167,   176,   177,   179,   186,   187,   188,   189,
     194,   195,   196,   200,   201,   202,   125,   120,   122,   125,
      20,   131,   139,   128,   130,   132,   131,   132,   128,     3,
      13,    14,    15,   135,   136,   169,   170,    16,    25,    26,
      27,    28,    30,    31,   144,   145,   146,   185,   127,   152,
      18,   156,   157,   128,   128,   128,   128,   128,   128,   128,
     128,   128,     5,    16,    18,    80,    81,    82,    83,    84,
      85,    86,    87,    89,   130,   151,   179,   180,   181,   182,
     183,   184,   186,   188,    18,   191,   192,   193,    18,   198,
     199,    18,   204,   205,    25,    26,    27,    28,    31,    32,
      33,    34,    35,   123,   124,   128,   131,   132,   131,    13,
      14,   137,   138,     5,   172,   173,   174,     4,   143,   143,
     144,   145,    25,    26,    27,    28,    30,    31,   147,   148,
     106,   166,   156,    11,   168,   168,   168,   168,   168,   168,
     168,   168,   168,   181,     8,   178,   181,   108,   190,   191,
     111,   197,   198,   114,   203,   204,   123,   131,     4,   171,
       6,   175,   143,   147,   128,     5,   174,   168
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   117,   118,   119,   119,   120,   120,   121,   121,   122,
     122,   123,   123,   124,   124,   124,   124,   124,   124,   124,
     124,   124,   125,   126,   126,   127,   127,   127,   127,   128,
     128,   128,   128,   129,   129,   129,   129,   130,   131,   132,
     132,   133,   133,   134,   135,   135,   135,   136,   136,   136,
     136,   137,   138,   139,   140,   140,   140,   140,   140,   141,
     141,   141,   142,   143,   144,   145,   145,   146,   146,   146,
     146,   146,   146,   147,   147,   148,   148,   148,   148,   148,
     148,   149,   149,   149,   149,   149,   149,   149,   149,   149,
     149,   149,   149,   149,   149,   149,   149,   149,   149,   150,
     150,   150,   150,   150,   150,   151,   152,   152,   153,   153,
     153,   153,   153,   154,   154,   154,   154,   154,   154,   154,
     154,   154,   154,   155,   156,   156,   157,   158,   159,   160,
     161,   162,   163,   164,   165,   166,   167,   168,   169,   170,
     171,   172,   172,   172,   173,   174,   175,   176,   176,   176,
     177,   178,   179,   179,   179,   179,   179,   179,   179,   179,
     179,   179,   180,   180,   181,   181,   182,   182,   182,   183,
     183,   183,   183,   183,   183,   183,   183,   183,   183,   183,
     183,   183,   183,   184,   185,   186,   186,   186,   186,   186,
     186,   186,   186,   186,   186,   186,   186,   186,   186,   186,
     187,   187,   187,   187,   187,   187,   187,   187,   187,   187,
     187,   187,   187,   187,   188,   189,   190,   191,   191,   192,
     193,   194,   194,   195,   196,   197,   198,   198,   199,   200,
     200,   200,   200,   201,   202,   203,   204,   204,   205
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     3,     1,     2,     1,     2,     1,     1,     1,
       2,     1,     2,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     2,     1,     1,     2,     2,     3,     1,
       3,     2,     2,     1,     2,     2,     3,     1,     1,     1,
       2,     1,     1,     2,     1,     2,     2,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     3,
       3,     4,     1,     1,     2,     1,     2,     1,     1,     1,
       1,     1,     1,     1,     2,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     2,     1,     1,
       1,     1,     1,     3,     5,     3,     3,     3,     3,     3,
       3,     3,     3,     1,     1,     2,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     3,     1,
       1,     3,     2,     1,     1,     1,     1,     3,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     2,     1,     2,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     1,     1,     1,     2,     1,
       1,     1,     1,     3,     1,     1,     1,     2,     1,     1,
       1,     1,     1,     3,     1,     1,     1,     2,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:
#line 46 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("pcre <<< modif_front pattern modif_rear" << endl); pcre2modif_front_pattern_modif_rear();}
#line 1681 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 3:
#line 52 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front <<< pcre_delim" << endl); modif_front2pcre_delim();}
#line 1687 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 4:
#line 53 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front <<< modif_front_ext-pcre_delim" << endl); modif_front2modif_front_ext_pcre_delim();}
#line 1693 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 5:
#line 56 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front_ext <<< modif_front_unit" << endl); modif_front_ext2modif_front_unit();}
#line 1699 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 6:
#line 57 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front_ext <<< modif_front_unit-modif_front_ext" << endl); modif_front_ext2modif_front_unit_modif_front_ext();}
#line 1705 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 7:
#line 63 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front_unit <<< UTF8" << endl); modif_front_unit2UTF8();}
#line 1711 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 8:
#line 64 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_front_unit <<< UCP" << endl); modif_front_unit2UCP();}
#line 1717 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 9:
#line 67 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear <<< pcre_delim" << endl); modif_rear2pcre_delim();}
#line 1723 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 10:
#line 68 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear <<< pcre_delim-modif_rear_ext" << endl); modif_rear2pcre_delim_modif_rear_ext();}
#line 1729 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 11:
#line 71 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_ext <<< modif_rear_unit" << endl); modif_rear_ext2modif_rear_unit();}
#line 1735 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 12:
#line 72 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_ext <<< modif_rear_unit-modif_rear_ext" << endl); modif_rear_ext2modif_rear_unit_modif_rear_ext();}
#line 1741 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 13:
#line 82 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_CASELESS" << endl); modif_rear_unit2MODIF_CASELESS();}
#line 1747 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 14:
#line 83 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
#line 1753 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 15:
#line 84 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
#line 1759 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 16:
#line 85 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
#line 1765 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 17:
#line 86 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
#line 1771 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 18:
#line 87 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_R" << endl); modif_rear_unit2MODIF_R();}
#line 1777 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 19:
#line 88 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_O" << endl); modif_rear_unit2MODIF_O();}
#line 1783 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 20:
#line 89 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_P" << endl); modif_rear_unit2MODIF_P();}
#line 1789 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 21:
#line 90 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_B" << endl); modif_rear_unit2MODIF_B();}
#line 1795 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 22:
#line 93 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("pcre_delim <<< SLASH" << endl); pcre_delim2SLASH();}
#line 1801 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 23:
#line 96 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("pattern <<< newlinespec inslash" << endl); pattern2newlinespec_inslash();}
#line 1807 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 24:
#line 97 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("pattern <<< inslash" << endl); pattern2inslash();}
#line 1813 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 25:
#line 103 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inslash <<< rv" << endl); inslash2rv();}
#line 1819 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 26:
#line 104 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inslash <<< bol-rv" << endl); inslash2bol_rv();}
#line 1825 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 27:
#line 105 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inslash <<< rv-eol" << endl); inslash2rv_eol();}
#line 1831 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 28:
#line 106 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inslash <<< bol-rv|eol" << endl); inslash2bol_rv_eol();}
#line 1837 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 29:
#line 109 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("rv <<< ext_exp" << endl); rv2ext_exp();}
#line 1843 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 30:
#line 110 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("rv <<< rv-or|rv" << endl); rv2rv_or_rv();}
#line 1849 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 31:
#line 111 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("rv <<< or-rv" << endl); rv2or_rv();}
#line 1855 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 32:
#line 112 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("rv <<< rv-or" << endl); rv2rv_or();}
#line 1861 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 33:
#line 115 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_exp <<< exp" << endl); ext_exp2exp();}
#line 1867 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 34:
#line 116 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_exp <<< bol-exp" << endl); ext_exp2bol_exp();}
#line 1873 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 35:
#line 117 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_exp <<< exp-eol" << endl); ext_exp2exp_eol();}
#line 1879 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 36:
#line 118 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_exp <<< bol-exp|eol" << endl); ext_exp2bol_exp_eol();}
#line 1885 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 37:
#line 121 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("bol <<< BOL" << endl); bol2BOL();}
#line 1891 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 38:
#line 124 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("eol <<< EOL" << endl); eol2EOL();}
#line 1897 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 39:
#line 127 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("exp <<< ext_unit" << endl); exp2ext_unit();}
#line 1903 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 40:
#line 128 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("exp <<< ext_unit-exp" << endl); exp2ext_unit_exp();}
#line 1909 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 41:
#line 135 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_unit <<< unit" << endl); ext_unit2unit();}
#line 1915 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 42:
#line 136 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("ext_unit <<< quantify_unit" << endl); ext_unit2quantify_unit();}
#line 1921 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 43:
#line 139 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantify_unit <<< unit quantify" << endl); quantify_unit2unit_quantify();}
#line 1927 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 44:
#line 142 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantify <<< quantifier" << endl); quantify2quantifier();}
#line 1933 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 45:
#line 143 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantify <<< quantifier-possessive" << endl); quantify2quantifier_possessive();}
#line 1939 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 46:
#line 144 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantify <<< quantifier-lazy" << endl); quantify2quantifier_lazy();}
#line 1945 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 47:
#line 153 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantifier <<< ZEROMORE" << endl); quantifier2ZEROMORE();}
#line 1951 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 48:
#line 154 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantifier <<< ZEROONE" << endl); quantifier2ZEROONE();}
#line 1957 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 49:
#line 155 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantifier <<< ONEMORE" << endl); quantifier2ONEMORE();}
#line 1963 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 50:
#line 156 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("quantifier <<< repeating" << endl); quantifier2repeating();}
#line 1969 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 51:
#line 159 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("possessive <<< ONEMORE" << endl); possessive2ONEMORE();}
#line 1975 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 52:
#line 162 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("lazy <<< ZEROONE" << endl); lazy2ZEROONE();}
#line 1981 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 53:
#line 166 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("or <<< OR" << endl); or2OR();}
#line 1987 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 54:
#line 174 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("unit <<< element" << endl); unit2element();}
#line 1993 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 55:
#line 175 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("unit <<< capturing" << endl); unit2capturing();}
#line 1999 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 56:
#line 176 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("unit <<< option" << endl); unit2option();}
#line 2005 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 57:
#line 177 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("unit <<< chal" << endl); unit2chal();}
#line 2011 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 58:
#line 178 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("unit <<< class" << endl); unit2class();}
#line 2017 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 59:
#line 186 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option <<< optionStart option_set optionEnd" << endl); option2optionStart_option_set_optionEnd();}
#line 2023 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 60:
#line 187 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option <<< optionStart-option_unset_group|optionEnd" << endl); option2optionStart_option_unset_group_optionEnd();}
#line 2029 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 61:
#line 188 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option <<< optionStart-option_set|option_unset_group|optionEnd" << endl); option2optionStart_option_set_option_unset_group_optionEnd();}
#line 2035 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 62:
#line 191 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("optionStart <<< OPTION" << endl); optionStart2OPTION();}
#line 2041 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 63:
#line 194 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("optionEnd <<< RBRA" << endl); optionEnd2RBRA();}
#line 2047 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 64:
#line 200 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_unset_group <<< dash option_unset" << endl); option_unset_group2dash_option_unset();}
#line 2053 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 65:
#line 203 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_set <<< option_set_unit" << endl); option_set2option_set_unit();}
#line 2059 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 66:
#line 204 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_set <<< option_set_unit-option_set" << endl); option_set2option_set_unit_option_set();}
#line 2065 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 67:
#line 207 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_set_unit <<< MODIF_CASELESS" << endl); option_set_unit2MODIF_CASELESS();}
#line 2071 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 68:
#line 208 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
#line 2077 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 69:
#line 209 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
#line 2083 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 70:
#line 210 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
#line 2089 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 71:
#line 211 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_set_unit <<< MODIF_DUPNAMES" << endl); option_set_unit2MODIF_DUPNAMES();}
#line 2095 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 72:
#line 212 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
#line 2101 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 73:
#line 215 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_unset <<< option_unset_unit" << endl); option_unset2option_unset_unit();}
#line 2107 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 74:
#line 216 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_unset <<< option_unset_unit-option_unset" << endl); option_unset2option_unset_unit_option_unset();}
#line 2113 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 75:
#line 219 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_unset_unit <<< MODIF_CASELESS" << endl); option_unset_unit2MODIF_CASELESS();}
#line 2119 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 76:
#line 220 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_DOTALL" << endl); modif_rear_unit2MODIF_DOTALL();}
#line 2125 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 77:
#line 221 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_EXTENDED" << endl); modif_rear_unit2MODIF_EXTENDED();}
#line 2131 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 78:
#line 222 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_MULTILINE" << endl); modif_rear_unit2MODIF_MULTILINE();}
#line 2137 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 79:
#line 223 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("option_set_unit <<< MODIF_DUPNAMES" << endl); option_set_unit2MODIF_DUPNAMES();}
#line 2143 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 80:
#line 224 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("modif_rear_unit <<< MODIF_UNGREEDY" << endl); modif_rear_unit2MODIF_UNGREEDY();}
#line 2149 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 81:
#line 246 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< ASCII " << (char)yylval << endl); element2ASCII((char)yylval);}
#line 2155 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 82:
#line 247 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< ANY" << endl); element2ANY();}
#line 2161 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 83:
#line 248 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< SPACE" << endl); element2SPACE();}
#line 2167 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 84:
#line 249 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< hex" << endl); element2hex();}
#line 2173 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 85:
#line 250 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< TAB" << endl); element2TAB();}
#line 2179 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 86:
#line 251 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< CR" << endl); element2CR();}
#line 2185 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 87:
#line 252 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< LF" << endl); element2LF();}
#line 2191 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 88:
#line 253 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< FF" << endl); element2FF();}
#line 2197 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 89:
#line 254 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< BEL" << endl); element2BEL();}
#line 2203 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 90:
#line 255 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< ESC" << endl); element2ESC();}
#line 2209 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 91:
#line 256 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< CONTROLX " << (char)yylval << endl); element2CONTROLX((char)yylval);}
#line 2215 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 92:
#line 257 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< BSR" << endl); element2BSR();}
#line 2221 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 93:
#line 258 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< RESET" << endl); element2RESET();}
#line 2227 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 94:
#line 259 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< assertions" << endl); element2assertions();}
#line 2233 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 95:
#line 260 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< ONEBYTE" << endl); element2ONEBYTE();}
#line 2239 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 96:
#line 261 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< OCTAL " << (char)yylval << endl); element2OCTAL((char)yylval);}
#line 2245 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 97:
#line 262 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< backreference" << endl); element2backreference();}
#line 2251 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 98:
#line 263 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< subroutine" << endl); element2subroutine();}
#line 2257 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 99:
#line 276 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< WORDBOUNDARY" << endl); assertions2WORDBOUNDARY();}
#line 2263 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 100:
#line 277 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< NWORDBOUNDARY" << endl); assertions2NWORDBOUNDARY();}
#line 2269 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 101:
#line 278 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< STARTSUBJECT" << endl); assertions2STARTSUBJECT();}
#line 2275 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 102:
#line 279 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< ENDSUBJECT" << endl); assertions2ENDSUBJECT();}
#line 2281 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 103:
#line 280 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< OENDSUBJECT" << endl); assertions2OENDSUBJECT();}
#line 2287 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 104:
#line 281 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("assertions <<< FIRSTPOSITION" << endl); assertions2FIRSTPOSITION();}
#line 2293 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 105:
#line 284 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("hex <<< HEX " << hex << (char)yylval << endl); hex2HEX((char)yylval);}
#line 2299 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 106:
#line 288 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec <<< newlinespec_unit" << endl); newlinespec2newlinespec_unit();}
#line 2305 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 107:
#line 289 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec <<< newlinespec_unit-newlinespec" << endl); newlinespec2newlinespec_unit_newlinespec();}
#line 2311 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 108:
#line 292 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec_unit <<< OPT_CR" << endl); newlinespec_unit2OPT_CR();}
#line 2317 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 109:
#line 293 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec_unit <<< OPT_LF" << endl); newlinespec_unit2OPT_LF();}
#line 2323 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 110:
#line 294 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec_unit <<< OPT_CRLF" << endl); newlinespec_unit2OPT_CRLF();}
#line 2329 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 111:
#line 295 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec_unit <<< OPT_ANYCRLF" << endl); newlinespec_unit2OPT_ANYCRLF();}
#line 2335 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 112:
#line 296 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("newlinespec_unit <<< OPT_ANY_NEWLINE" << endl); newlinespec_unit2OPT_ANY_NEWLINE();}
#line 2341 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 113:
#line 314 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< startCapturing rv endCapturing" << endl); capturing2startCapturing_rv_endCapturing();}
#line 2347 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 114:
#line 315 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingNamed-capturingName|capturingNameEnd|rv|endCapturing" << endl); capturing2capturingNamed_capturingName_capturingNameEnd_rv_endCapturing();}
#line 2353 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 115:
#line 316 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingNon-rv|endCapturing" << endl); capturing2capturingNon_rv_endCapturing();}
#line 2359 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 116:
#line 317 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingNonreset-rv|endCapturing" << endl); capturing2capturingNonreset_rv_endCapturing();}
#line 2365 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 117:
#line 318 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingAtomic-rv|endCapturing" << endl); capturing2capturingAtomic_rv_endCapturing();}
#line 2371 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 118:
#line 319 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingComment-rv|endCapturing" << endl); capturing2capturingComment_rv_endCapturing();}
#line 2377 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 119:
#line 320 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingPosahead-rv|endCapturing" << endl); capturing2capturingPosahead_rv_endCapturing();}
#line 2383 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 120:
#line 321 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingNegahead-rv|endCapturing" << endl); capturing2capturingNegahead_rv_endCapturing();}
#line 2389 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 121:
#line 322 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingPosbehind-rv|endCapturing" << endl); capturing2capturingPosbehind_rv_endCapturing();}
#line 2395 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 122:
#line 323 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturing <<< capturingNegbehind-rv|endCapturing" << endl); capturing2capturingNegbehind_rv_endCapturing();}
#line 2401 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 123:
#line 327 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNamed <<< CAPTURING_NAMED" << endl); capturingNamed2CAPTURING_NAMED();}
#line 2407 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 124:
#line 330 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingName <<< capturingNameAdd" << endl); capturingName2capturingNameAdd();}
#line 2413 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 125:
#line 331 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingName <<< capturingNameAdd-capturingName" << endl); capturingName2capturingNameAdd_capturingName();}
#line 2419 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 126:
#line 334 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNameAdd <<< ASCII " << (char)yylval << endl); capturingNameAdd2ASCII((char)yylval);}
#line 2425 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 127:
#line 337 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNon <<< CAPTURING_NON" << endl); capturingNon2CAPTURING_NON();}
#line 2431 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 128:
#line 340 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNonreset <<< CAPTURING_NONRESET" << endl); capturingNonreset2CAPTURING_NONRESET();}
#line 2437 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 129:
#line 343 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingAtomic <<< CAPTURING_ATOMIC" << endl); capturingAtomic2CAPTURING_ATOMIC();}
#line 2443 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 130:
#line 346 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingComment <<< CAPTURING_COMMENT" << endl); capturingComment2CAPTURING_COMMENT();}
#line 2449 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 131:
#line 349 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingPosahead <<< CAPTURING_POSAHEAD" << endl); capturingPosahead2CAPTURING_POSAHEAD();}
#line 2455 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 132:
#line 352 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNegahead <<< CAPTURING_NEGAHEAD" << endl); capturingNegahead2CAPTURING_NEGAHEAD();}
#line 2461 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 133:
#line 355 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingPosbehind <<< CAPTURING_POSBEHIND" << endl); capturingPosbehind2CAPTURING_POSBEHIND();}
#line 2467 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 134:
#line 358 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNegbehind <<< CAPTURING_NEGBEHIND" << endl); capturingNegbehind2CAPTURING_NEGBEHIND();}
#line 2473 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 135:
#line 364 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("capturingNameEnd <<< CAPTURING_NAMED_END" << endl); capturingNameEnd2CAPTURING_NAMED_END();}
#line 2479 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 136:
#line 368 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("startCapturing <<< LPAR" << endl); startCapturing2LPAR();}
#line 2485 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 137:
#line 371 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("endCapturing <<< RPAR" << endl); endCapturing2RPAR();}
#line 2491 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 138:
#line 375 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("repeating <<< startRepeating interval endRepeating" << endl); repeating2startRepeating_interval_endRepeating();}
#line 2497 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 139:
#line 378 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("startRepeating <<< LBRA" << endl); startRepeating2LBRA();}
#line 2503 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 140:
#line 381 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("endRepeating <<< RBRA" << endl); endRepeating2RBRA();}
#line 2509 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 141:
#line 390 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("interval <<< minimum intervalDelim maximum" << endl); interval2minimum_intervalDelim_maximum();}
#line 2515 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 142:
#line 391 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("interval <<< minimum-intervalDelim" << endl); interval2minimum_intervalDelim();}
#line 2521 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 143:
#line 392 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("interval <<< maximum" << endl); interval2maximum();}
#line 2527 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 144:
#line 395 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("minimum <<< INT " << (int)yylval << endl); minimum2INT((int)yylval);}
#line 2533 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 145:
#line 398 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("maximum <<< INT " << (int)yylval << endl); maximum2INT((int)yylval);}
#line 2539 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 146:
#line 401 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("intervalDelim <<< COMMA" << endl); intervalDelim2COMMA();}
#line 2545 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 147:
#line 410 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("class <<< classStart inclass classEnd" << endl); class2classStart_inclass_classEnd();}
#line 2551 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 148:
#line 411 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("class <<< slashcharclass" << endl); class2slashcharclass();}
#line 2557 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 149:
#line 412 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("class <<< posix_class" << endl); class2posix_class();}
#line 2563 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 150:
#line 415 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("classStart <<< LBOX" << endl); classStart2LBOX();}
#line 2569 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 151:
#line 418 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("classEnd <<< RBOX" << endl); classEnd2RBOX();}
#line 2575 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 152:
#line 433 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< DECDIGIT" << endl); slashcharclass2DECDIGIT();}
#line 2581 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 153:
#line 434 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< NDECDIGIT" << endl); slashcharclass2NDECDIGIT();}
#line 2587 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 154:
#line 435 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< HWHITESPACE" << endl); slashcharclass2HWHITESPACE();}
#line 2593 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 155:
#line 436 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< NHWHITESPACE" << endl); slashcharclass2NHWHITESPACE();}
#line 2599 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 156:
#line 437 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< WHITESPACE" << endl); slashcharclass2WHITESPACE();}
#line 2605 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 157:
#line 438 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< NWHITESPACE" << endl); slashcharclass2NWHITESPACE();}
#line 2611 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 158:
#line 439 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< VWHITESPACE" << endl); slashcharclass2VWHITESPACE();}
#line 2617 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 159:
#line 440 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< NVWHITESPACE" << endl); slashcharclass2NVWHITESPACE();}
#line 2623 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 160:
#line 441 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< WORDCHAR" << endl); slashcharclass2WORDCHAR();}
#line 2629 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 161:
#line 442 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("slashcharclass <<< NWORDCHAR" << endl); slashcharclass2NWORDCHAR();}
#line 2635 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 162:
#line 450 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass <<< inclass_ext_unit" << endl); inclass2inclass_ext_unit();}
#line 2641 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 163:
#line 451 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass <<< bol-inclass_ext_unit" << endl); inclass2bol_inclass_ext_unit();}
#line 2647 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 164:
#line 458 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_ext_unit <<< inclass_unit" << endl); inclass_ext_unit2inclass_unit();}
#line 2653 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 165:
#line 459 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_ext_unit <<< inclass_unit-inclass_ext_unit" << endl); inclass_ext_unit2inclass_unit_inclass_ext_unit();}
#line 2659 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 166:
#line 462 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_unit <<< inclass_element" << endl); inclass_unit2inclass_element();}
#line 2665 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 167:
#line 463 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_unit <<< rangechars" << endl); inclass_unit2rangechars();}
#line 2671 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 168:
#line 464 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_unit <<< chal" << endl); inclass_unit2chal();}
#line 2677 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 169:
#line 483 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("element <<< ASCII " << (char)yylval << endl); element2ASCII((char)yylval);}
#line 2683 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 170:
#line 484 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< posix_class" << endl); inclass_element2posix_class();}
#line 2689 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 171:
#line 485 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< slashcharclass" << endl); inclass_element2slashcharclass();}
#line 2695 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 172:
#line 486 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< hex" << endl); inclass_element2hex();}
#line 2701 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 173:
#line 487 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< TAB" << endl); inclass_element2TAB();}
#line 2707 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 174:
#line 488 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< CR" << endl); inclass_element2CR();}
#line 2713 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 175:
#line 489 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< LF" << endl); inclass_element2LF();}
#line 2719 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 176:
#line 490 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< FF" << endl); inclass_element2FF();}
#line 2725 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 177:
#line 491 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< BEL" << endl); inclass_element2BEL();}
#line 2731 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 178:
#line 492 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< ESC" << endl); inclass_element2ESC();}
#line 2737 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 179:
#line 493 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< CONTROLX " << (char)yylval << endl); inclass_element2CONTROLX((char)yylval);}
#line 2743 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 180:
#line 494 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< RESET" << endl); inclass_element2RESET();}
#line 2749 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 181:
#line 495 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< OCTAL " << (char)yylval << endl); inclass_element2OCTAL((char)yylval);}
#line 2755 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 182:
#line 496 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inclass_element <<< DASH" << endl); inclass_element2DASH();}
#line 2761 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 183:
#line 500 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("rangechars <<< INT " << (int)yylval << endl); rangechars2INT((int)yylval);}
#line 2767 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 184:
#line 503 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("dash <<< DASH" << endl); dash2DASH();}
#line 2773 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 185:
#line 507 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_ALNUM" << endl); posix_class2P_ALNUM();}
#line 2779 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 186:
#line 508 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_ALPHA" << endl); posix_class2P_ALPHA();}
#line 2785 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 187:
#line 509 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_ASCII" << endl); posix_class2P_ASCII();}
#line 2791 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 188:
#line 510 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_BLANK" << endl); posix_class2P_BLANK();}
#line 2797 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 189:
#line 511 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_CNTRL" << endl); posix_class2P_CNTRL();}
#line 2803 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 190:
#line 512 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_DIGIT" << endl); posix_class2P_DIGIT();}
#line 2809 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 191:
#line 513 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_GRAPH" << endl); posix_class2P_GRAPH();}
#line 2815 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 192:
#line 514 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_LOWER" << endl); posix_class2P_LOWER();}
#line 2821 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 193:
#line 515 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_PRINT" << endl); posix_class2P_PRINT();}
#line 2827 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 194:
#line 516 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_PUNCT" << endl); posix_class2P_PUNCT();}
#line 2833 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 195:
#line 517 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_SPACE" << endl); posix_class2P_SPACE();}
#line 2839 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 196:
#line 518 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_UPPER" << endl); posix_class2P_UPPER();}
#line 2845 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 197:
#line 519 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_WORD" << endl); posix_class2P_WORD();}
#line 2851 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 198:
#line 520 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< P_XDIGIT" << endl); posix_class2P_XDIGIT();}
#line 2857 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 199:
#line 521 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class <<< posix_class_neg" << endl); posix_class2posix_class_neg();}
#line 2863 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 200:
#line 524 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_ALNUM" << endl); posix_class_neg2NP_ALNUM();}
#line 2869 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 201:
#line 525 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_ALPHA" << endl); posix_class_neg2NP_ALPHA();}
#line 2875 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 202:
#line 526 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_ASCII" << endl); posix_class_neg2NP_ASCII();}
#line 2881 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 203:
#line 527 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_BLANK" << endl); posix_class_neg2NP_BLANK();}
#line 2887 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 204:
#line 528 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_CNTRL" << endl); posix_class_neg2NP_CNTRL();}
#line 2893 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 205:
#line 529 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_DIGIT" << endl); posix_class_neg2NP_DIGIT();}
#line 2899 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 206:
#line 530 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_GRAPH" << endl); posix_class_neg2NP_GRAPH();}
#line 2905 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 207:
#line 531 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_LOWER" << endl); posix_class_neg2NP_LOWER();}
#line 2911 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 208:
#line 532 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_PRINT" << endl); posix_class_neg2NP_PRINT();}
#line 2917 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 209:
#line 533 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_PUNCT" << endl); posix_class_neg2NP_PUNCT();}
#line 2923 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 210:
#line 534 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_SPACE" << endl); posix_class_neg2NP_SPACE();}
#line 2929 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 211:
#line 535 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_UPPER" << endl); posix_class_neg2NP_UPPER();}
#line 2935 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 212:
#line 536 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_WORD" << endl); posix_class_neg2NP_WORD();}
#line 2941 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 213:
#line 537 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("posix_class_neg <<< NP_XDIGIT" << endl); posix_class_neg2NP_XDIGIT();}
#line 2947 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 214:
#line 541 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("chal <<< chalStart inchal chalEnd" << endl); chal2chalStart_inchal_chalEnd();}
#line 2953 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 215:
#line 544 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("chalStart <<< CHALSTART" << endl); chalStart2CHALSTART();}
#line 2959 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 216:
#line 547 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("chalEnd <<< CHALEND" << endl); chalEnd2CHALEND();}
#line 2965 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 217:
#line 550 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inchal <<< inchalExtUnit" << endl); inchal2inchalExtUnit();}
#line 2971 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 218:
#line 551 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inchal <<< inchalExtUnit-inchal" << endl); inchal2inchalExtUnit_inchal();}
#line 2977 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 219:
#line 554 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inchalExtUnit <<< inchalUnit" << endl); inchalExtUnit2inchalUnit();}
#line 2983 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 220:
#line 557 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inchalUnit <<< ASCII " << (char)yylval << endl); inchalUnit2ASCII((char)yylval);}
#line 2989 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 221:
#line 560 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("backreference <<< BACKREFERENCE" << endl); backreference2BACKREFERENCE();}
#line 2995 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 222:
#line 561 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("backreference <<< named_back_reference" << endl); backreference2named_back_reference();}
#line 3001 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 223:
#line 564 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("named_back_reference <<< nbrStart inNbr nbrEnd" << endl); named_back_reference2nbrStart_inNbr_nbrEnd();}
#line 3007 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 224:
#line 567 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("nbrStart <<< NAMED_BACKREFERENCE" << endl); nbrStart2NAMED_BACKREFERENCE();}
#line 3013 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 225:
#line 570 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("nbrEnd <<< NAMED_BACKREFERENCE_END" << endl); nbrEnd2NAMED_BACKREFERENCE_END();}
#line 3019 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 226:
#line 573 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNbr <<< inNbrUnit" << endl); inNbr2inNbrUnit();}
#line 3025 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 227:
#line 574 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNbr <<< inNbrUnit-inNbr" << endl); inNbr2inNbrUnit_inNbr();}
#line 3031 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 228:
#line 577 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNbrUnit <<< ASCII " << (char)yylval << endl); inNbrUnit2ASCII((char)yylval);}
#line 3037 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 229:
#line 580 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("subroutine <<< SUBROUTINE_ALL" << endl); subroutine2SUBROUTINE_ALL();}
#line 3043 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 230:
#line 581 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("subroutine <<< SUBROUTINE_ABSOLUTE" << endl); subroutine2SUBROUTINE_ABSOLUTE();}
#line 3049 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 231:
#line 582 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("subroutine <<< SUBROUTINE_RELATIVE" << endl); subroutine2SUBROUTINE_RELATIVE();}
#line 3055 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 232:
#line 583 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("subroutine <<< named_subroutine" << endl); subroutine2named_subroutine();}
#line 3061 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 233:
#line 586 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("named_subroutine <<< nsrStart inNsr nsrEnd" << endl); named_subroutine2nsrStart_inNsr_nsrEnd();}
#line 3067 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 234:
#line 589 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("nsrStart <<< SUBROUTINE_NAME" << endl); nsrStart2SUBROUTINE_NAME();}
#line 3073 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 235:
#line 592 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("nsrEnd <<< SUBROUTINE_NAME_END" << endl); nsrEnd2SUBROUTINE_NAME_END();}
#line 3079 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 236:
#line 595 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNsr <<< inNsrUnit" << endl); inNsr2inNsrUnit();}
#line 3085 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 237:
#line 596 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNsr <<< inNsrUnit-inNsr" << endl); inNsr2inNsrUnit_inNsr();}
#line 3091 "pcre.tab.c" /* yacc.c:1646  */
    break;

  case 238:
#line 599 "pcre.gen.y" /* yacc.c:1646  */
    {DEBUG("inNsrUnit <<< ASCII " << (char)yylval << endl); inNsrUnit2ASCII((char)yylval);}
#line 3097 "pcre.tab.c" /* yacc.c:1646  */
    break;


#line 3101 "pcre.tab.c" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 602 "pcre.gen.y" /* yacc.c:1906  */

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
