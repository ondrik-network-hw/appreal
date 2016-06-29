#!/bin/bash

interface_file="interface.c"
interface_header="interface.h"
grammar_file="pcre.y"
new_grammar_file="pcre.gen.y"
painter_file="painter.cpp"
painter_header="painter.hpp"

rm -f $interface_file
rm -f $interface_header
rm -f $new_grammar_file
rm -f $painter_file
rm -f $painter_header

cp $grammar_file $new_grammar_file

# pripoji uvodni cast modulu painter
cp preambles/painter.cpp $painter_file
cp preambles/painter.hpp $painter_header

# pripoji uvodni cast interface souboru
cp preambles/interface.hpp $interface_header
cp preambles/interface.cpp $interface_file


echo "+-----------------------------------------------------------------------+"
echo "| Probehne:                                                             |"
echo "| - doplneni ladicich vypisu,                                           |"
echo "| - vytvoreni funkci ze vsech gramatickych pravidel                     |"
echo "| - jejich zavolani ze souboru s pravidly                               |"
echo "| - a vytvoreni modulu pro vykresleni derivacniho stromu.               |"
echo "+-----------------------------------------------------------------------+"

leva_strana="" # leva strana prepisovaciho pravidla
prava_strana="" # prava strana
kontext=""

predchozi=""

plonkovy_radek=1

pocet_funkci=0

IFS=$'\012' # novy radek
#for pravidlo in $(cat $grammar_file | awk '/^[a-z_]+:/,/^;$/') # prochazi pouze radky jednotlivych pravidel
for radek in $(cat $grammar_file)
do
	plonkovy_radek=1
	echo $radek | egrep '^[a-zA-Z_]+[:][\	]+([a-zA-Z0-9_\ ]+)[\	]+\{.*$' > /dev/null
	if [ "$?" -eq 0 ]; then
		pravidlo=$radek
		tmp=`echo $pravidlo | sed 's/^\([a-zA-Z_]*\):[\t]*\([a-zA-Z0-9_ ]*\).*$/\12\2/g' | sed 's/ $//g' | sed 's/ /|/g'`
		funkce=`echo $tmp | sed 's/|/_/g'`
		kontext=`echo $tmp | sed 's/2/ <<< /g' | sed 's/|/ /g'`
		leva_strana=`echo $tmp | sed 's/^\(.*\)2.*$/\1/g'`
		prava_strana=`echo $tmp | sed 's/^.*2\(.*\)$/\1/g'`
		if [ "$prava_strana" == "ASCII" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
		if [ "$prava_strana" == "INT" ]; then
			funkce_deklarace="$funkce(int i)"
			funkce_volani="$funkce((int)yylval)"
			debug="DEBUG(\"$kontext \" << (int)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (int)i << endl);"
		else
		if [ "$prava_strana" == "HEX" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << hex << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << hex << (char)c << endl);"
		else
		if [ "$prava_strana" == "CONTROLX" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
		if [ "$prava_strana" == "OCTAL" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
			funkce_deklarace="$funkce()"
			funkce_volani="$funkce()"
			debug="DEBUG(\"$kontext\" << endl);"
			debug_painter="DEBUG(\"$kontext\" << endl);"
		fi; fi; fi; fi; fi
		funkce_hlavicka="void $funkce_deklarace;"
		cat <<< $funkce_hlavicka >> $interface_header
		#cat <<< $funkce_hlavicka >> $painter_header
		zamena=`echo $pravidlo | sed 's/}/'$debug' '$funkce_volani';}/'`
		echo $radek | sed 's/'$radek'/'$zamena'/g' $new_grammar_file > $new_grammar_file.tmp
		cp $new_grammar_file.tmp $new_grammar_file
		plonkovy_radek=0
	fi

	echo $radek | egrep '^[a-zA-Z_]+[:][\	]+(/\* EMPTY \*/)[\	]+\{.*$' > /dev/null
	if [ "$?" -eq 0 ]; then
		pravidlo=$radek
		tmp=`echo $pravidlo | sed 's/^\([a-zA-Z_]*\):[\t]*.*$/\12EMPTY/g' | sed 's/ $//g' | sed 's/ /|/g'`
		funkce=`echo $tmp | sed 's/|/_/g'`
		kontext=`echo $tmp | sed 's/2/ <<< /g' | sed 's/|/-/g'`
		leva_strana=`echo $tmp | sed 's/^\(.*\)2.*$/\1/g'`
		prava_strana="EMPTY"
		funkce_deklarace="$funkce()"
		funkce_volani="$funkce()"
		funkce_hlavicka="void $funkce_deklarace;"
		debug="DEBUG(\"$kontext\" << endl);"
		debug_painter="DEBUG(\"$kontext\" << endl);"
		cat <<< $funkce_hlavicka >> $interface_header
		#cat <<< $funkce_hlavicka >> $painter_header
		zamena=`echo $pravidlo | sed 's/}/'$debug' '$funkce_volani';}/' | sed 's/\/\* EMPTY \*\//\t/g'`
		#echo $leva_strana
		#echo $zamena
		echo $radek | sed 's/^'$leva_strana'[^\n]*$/'$zamena'/g' $new_grammar_file > $new_grammar_file.tmp
		cp $new_grammar_file.tmp $new_grammar_file
		plonkovy_radek=0
	fi

	echo $radek | grep -E ^[\	]+[\|][\	]+[a-zA-Z0-9_\ ]+[\	]+\{.*$ > /dev/null
	if [ "$?" -eq 0 ]; then
		pravidlo=$radek
		#echo "$leva_strana $pravidlo"
		if [ "$leva_strana" == "" ]; then continue; fi
		tmp=`echo $pravidlo | sed 's/^[\t]*|[\t]*\([a-zA-Z0-9_ ]*\).*$/'$leva_strana'2\1/g' | sed 's/ $//g' |sed 's/ /|/g'`
		funkce=`echo $tmp | sed 's/|/_/g'`
		kontext=`echo $tmp | sed 's/2/ <<< /' | sed 's/|/-/'`
		prava_strana=`echo $tmp | sed 's/^.*2\(.*\)$/\1/'`
		if [ "$prava_strana" == "ASCII" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
		if [ "$prava_strana" == "INT" ]; then
			funkce_deklarace="$funkce(int i)"
			funkce_volani="$funkce((int)yylval)"
			debug="DEBUG(\"$kontext \" << (int)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (int)i << endl);"
		else
		if [ "$prava_strana" == "HEX" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << hex << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << hex << (char)c << endl);"
		else
		if [ "$prava_strana" == "CONTROLX" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
		if [ "$prava_strana" == "OCTAL" ]; then
			funkce_deklarace="$funkce(char c)"
			funkce_volani="$funkce((char)yylval)"
			debug="DEBUG(\"$kontext \" << (char)yylval << endl);"
			debug_painter="DEBUG(\"$kontext \" << (char)c << endl);"
		else
			funkce_deklarace="$funkce()"
			funkce_volani="$funkce()"
			debug="DEBUG(\"$kontext\" << endl);"
			debug_painter="DEBUG(\"$kontext\" << endl);"
		fi; fi; fi; fi; fi
		funkce_hlavicka="void $funkce_deklarace;"
		cat <<< $funkce_hlavicka >> $interface_header
		#cat <<< $funkce_hlavicka >> $painter_header
		zamena=`echo $pravidlo | sed 's/}/'$debug' '$funkce_volani';}/'`
		echo $pravidlo | sed 's/'$pravidlo'/'$zamena'/g' $new_grammar_file > $new_grammar_file.tmp
		cp $new_grammar_file.tmp $new_grammar_file
		plonkovy_radek=0
	fi

	# oddeli skupinu pravidel
	if [ "$radek" == ";" ]; then
		echo "" >> $interface_header
		#echo "" >> $painter_header
		echo ";" >> $new_grammar_file
		leva_strana=""
		prava_strana=""
		plonkovy_radek=0
		continue
	fi

	if [ "$prava_strana" != "" ]; then if [ "$leva_strana" != "" ]
	then
		pravidlo=$radek
		echo "// $kontext" >> $painter_file # nazev funkce
		echo "// $kontext" >> $interface_file
		echo $funkce_hlavicka | tr \; \{ >> $painter_file
		echo $funkce_hlavicka | tr \; \{ >> $interface_file

		echo $funkce_hlavicka
		let "pocet_funkci=$pocet_funkci+1"

		reverse=""
		oldifs=$IFS
		IFS='|'
		for pravidlo in $prava_strana; do
			reverse="$pravidlo|$reverse"
		done

		nonterm=0

		echo $prava_strana | grep -E ^[[:lower:][:space:]]+$ > /dev/null # na prave strane jsou pouze nonterminaly
		if [ "$?" -eq 0 ]; then
			echo "	nodes.push(++node); // vytvori prepisovany nonterminal" >> $painter_file
 			echo "" >> $painter_file
			nonterm=1
		fi

		for term in $reverse; do
			echo "	print_stack();" >> $painter_file
			echo "	$debug_painter" >> $painter_file
			echo $term | grep -E ^[[:upper:]0-9_]+$ > /dev/null # terminalni symboly jsou uppercase
			if [ "$?" -eq 0 ]; then
			#if [[ $term =~ [a-z]+ ]]; then
				echo "	node1 = ++node; // vytvori terminal $term" >> $painter_file
				if [ "$nonterm" -eq 0 ]; then
					echo "	node2 = ++node;  // vytvori nonterminal $leva_strana" >> $painter_file
					nonterm=1
				else
					echo "	node2 = nodes.top(); nodes.pop();  // vyzvedne nonterminal $leva_strana" >> $painter_file
				fi
			else
				if [ "$nonterm" -eq 0 ]; then
					echo "	node2 = ++node; // vytvori nonterminal $leva_strana" >> $painter_file
					nonterm=1
				else
					echo "	node2 = nodes.top(); nodes.pop(); // vyzvedne nonterminal $leva_strana" >> $painter_file
				fi
				echo "	node1 = nodes.top(); nodes.pop(); // vyzvedne nonterminal $term" >> $painter_file
			fi

			if [ "$prava_strana" == "ASCII" ]; then
				echo "	fprintf(graphFile, \"%d -> %d [label=\\\"ASCII %c\\\"]\n\", node2, node1, c);" >> $painter_file
			else
			if [ "$prava_strana" == "INT" ]; then
				echo "	fprintf(graphFile, \"%d -> %d [label=\\\"INT %i\\\"]\n\", node2, node1, i);" >> $painter_file
			else
			if [ "$prava_strana" == "HEX" ]; then
				echo "	fprintf(graphFile, \"%d -> %d [label=\\\"HEX %x\\\"]\n\", node2, node1, c);" >> $painter_file
			else
				echo "	fprintf(graphFile, \"%d -> %d\n\", node2, node1);" >> $painter_file
			fi
			fi
			fi
			echo "	fprintf(graphFile, \"%d [label=\\\"$leva_strana %d\\\"]\n\", node2, node2);" >> $painter_file
			echo "	fprintf(graphFile, \"%d [label=\\\"$term %d\\\"]\n\", node1, node1);" >> $painter_file
			echo "	nodes.push(node2);" >> $painter_file
			echo "" >> $painter_file
		done

		IFS=$oldifs
		echo "}" >> $painter_file
		echo "}" >> $interface_file
	fi
	fi

	#if [ "$plonkovy_radek" -eq 1 ]; then
		#cat <<< ''$radek'' >> $new_grammar_file
	#fi;
done

echo "#endif" >> $interface_header
echo "" >> $interface_header

echo "+-----------------------------------------------------------------------+"
echo "| Pocet gramatickych pravidel:     $pocet_funkci                        "
echo "| Pocet funkci:                    $pocet_funkci                        "
echo "+-----------------------------------------------------------------------+"
echo "| Vygenerované soubory:                                                 "
echo "| Interface:     $interface_header                                      "
echo "|                $interface_file                                        "
echo "| Modul painter: $painter_header                                        "
echo "|                $painter_file                                          "
echo "+-----------------------------------------------------------------------+"

rm -f $new_grammar_file.tmp

exit 0
