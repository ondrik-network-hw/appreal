BIN_PARSER=parser
BIN_PAINTER=painter
BIN_TESTER=tester
BIN=$(BIN_PARSER) $(BIN_PAINTER) $(BIN_TESTER)
CCFLAGS=-g -lrt # -lrt modif for time.h include
CC=g++

all: parser
flex: pcre.yy.c
bison: pcre.tab.c

$(BIN_PARSER): symbols.o nodes.o nfa.o pcre.tab.o pcre.yy.o parse.o parser.o
	${CC} -o $(BIN_PARSER) nfa.o nodes.o symbols.o pcre.yy.o pcre.tab.o parse.o parser.o -lfl ${CCFLAGS}

$(BIN_PAINTER): painter.o pcre.tab.o pcre.yy.o parse.o parser.o
	${CC} -o $(BIN_PAINTER) painter.o pcre.yy.o pcre.tab.o parse.o parser.o -lfl ${CCFLAGS}

$(BIN_TESTER): interface.o pcre.tab.o pcre.yy.o parse.o parser.o
	${CC} -o $(BIN_TESTER) interface.o pcre.yy.o pcre.tab.o parse.o parser.o -lfl ${CCFLAGS}

# generate grammar
# -d switch to produce pcre.tab.h to connect bison with lex
pcre.tab.c: pcre.gen.y
	bison -r all -d pcre.gen.y -o pcre.tab.c

# compile grammar
pcre.tab.o: pcre.tab.c pcre.y
	${CC} -c pcre.tab.c -o pcre.tab.o ${CCFLAGS}

# generate lexical analysator
pcre.yy.c: pcre.l
	flex pcre.l

# compile lexical analysator
pcre.yy.o: pcre.yy.c
	${CC} -c pcre.yy.c -o pcre.yy.o ${CCFLAGS}

parse.o: parse.c
	${CC} -c parse.c -o parse.o ${CCFLAGS}

parser.o: parser.c
	${CC} -c parser.c -o parser.o ${CCFLAGS}

interface.o: interface.c pcre.tab.c
	${CC} -c interface.c -o interface.o ${CCFLAGS}

painter.o: painter.cpp pcre.tab.c
	${CC} -c painter.cpp -o painter.o ${CCFLAGS}

nfa.o: nfa.cpp nfa.hpp symbols.hpp nodes.hpp
	${CC} -c nfa.cpp -o nfa.o ${CCFLAGS}

symbols.o: symbols.cpp symbols.hpp nodes.hpp
	${CC} -c symbols.cpp -o symbols.o ${CCFLAGS}

nodes.o: nodes.cpp nodes.hpp symbols.hpp
	${CC} -c nodes.cpp -o nodes.o ${CCFLAGS}

graph:
	dot -Tpng graph.dot -o graf.png
	eog graf.png 2> /dev/null

doxy:
	doxygen ./doxy/config

test: ${BIN_PARSER} ${BIN_TESTER}
	cd tests && ./test.sh

clean:
	rm -f pcre.yy.* pcre.tab.* *.o *~ *.dot ${BIN} *.png *.msfm *.output tests/nfa.msfm
	rm -f -r ./tests/test/
