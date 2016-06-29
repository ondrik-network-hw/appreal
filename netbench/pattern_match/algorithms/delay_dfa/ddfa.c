/***************************************************************************
############################################################################
#  ddfa.c: Algorithm for Delay DFA (transit through automat)
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol
############################################################################
#
#  LICENSE TERMS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. All advertising materials mentioning features or use of this software
#     or firmware must display the following acknowledgement:
#
#       This product includes software developed by the University of
#       Technology, Faculty of Information Technology, Brno and its
#       contributors.
#
#  4. Neither the name of the Company nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
#  In no event shall the company or contributors be liable for any
#  direct, indirect, incidental, special, exemplary, or consequential
#  damages (including, but not limited to, procurement of substitute
#  goods or services; loss of use, data, or profits; or business
#  interruption) however caused and on any theory of liability, whether
#  in contract, strict liability, or tort (including negligence or
#  otherwise) arising in any way out of the use of this software, even
#  if advised of the possibility of such damage.
#
#  $Id$
***************************************************************************/

/*
 *  ddfa.c    ver. 1.0
 *
 *  Algorithm for Delay DFA (transit through automat)
 *  =================================================
 *
 *  Jaroslav Suchodol,  July 2010
 *
 */

#include <stdio.h>
#include <stdlib.h>

typedef unsigned int u_i;

/* definition of global variables */
u_i count_states, start_state, alp_count_trans, alphabet_length;
u_i count_final_states;
u_i *alphabet;      /* array of transitions chars (alphabet),
                     * index to this array is in 'alp_in_begin/end' */
u_i *alp_in_begin; /* array of indexes where begin char(s) for transition,
                    * index to this array is structure T_STATE.trans_char */
u_i *alp_in_end;  /* array of indexes where end char(s) for transition, 
                   * index to this array is structure T_STATE.trans_char */
u_i *final_states;  /* array of final states */

// Structure for representing one state in automat
typedef struct t_state {
  int def_trans;    /* default transition */
  u_i trans_count;  /* count of transitions for current state */
  u_i *trans_char;  /* index transition char(s) */
  u_i *trans_dest;  /* destination state */
} T_STATE;
T_STATE *state;

/* Free dynamically allocated memory. */
void free_memory()
{
  u_i i;
  free(alphabet); alphabet = NULL;
  free(alp_in_begin); alp_in_begin = NULL;
  free(alp_in_end); alp_in_end = NULL;
  free(final_states); final_states = NULL;
  for (i = 0; i < count_states; i++) {
    free(state[i].trans_char);
    free(state[i].trans_dest);
  }
  free(state); state = NULL;
}

/* Parse input file (first argument of program) and 
 * make structure from it for later use. */
void parse_file(char *FileName)
{
  FILE *fr;
  u_i i, j;

  if ((fr = fopen(FileName, "r")) == NULL) {
    fprintf(stderr, "Error: file \"%s\" could not be open for reading!\n",
        FileName);
    exit(1);
  }
  /* parse COUNT OF STATES */
  fscanf(fr, "%u\n", &count_states);
  state = (T_STATE *) malloc(count_states * sizeof(T_STATE));
  /* parse ALPHABET */
  // first parse indexes
  fscanf(fr, "%u\n", &alp_count_trans);
  alp_in_begin = (u_i *) malloc(alp_count_trans * sizeof(u_i));
  alp_in_end = (u_i *) malloc(alp_count_trans * sizeof(u_i));
  if (alp_in_begin == NULL || alp_in_end == NULL || state == NULL) {
    fprintf(stderr, "Error: not enough memory!\n");
    free(state); free(alp_in_begin); free(alp_in_end);
    exit(1);
  }
  for (i = 0; i < alp_count_trans; i++) {
    fscanf(fr, "%u->%u|", &alp_in_begin[i], &alp_in_end[i]);
  }
  // second parse chars
  fscanf(fr, "%u->", &alphabet_length);
  alphabet = (u_i *) malloc(alphabet_length * sizeof(u_i));
  if (alphabet == NULL) {
    fprintf(stderr, "Error: not enough memory!\n");
    free(state); free(alp_in_begin); free(alp_in_end); free(alphabet);
    exit(1);
  }
  for (i = 0; i < alphabet_length; i++) {
    fscanf(fr, "%u|", &alphabet[i]);
  }
  /* parse STARTING STATE */
  fscanf(fr, "%u", &start_state);
  /* parse TRANSITIONS */
  // first parse count transitions for each state
  for (i = 0; i < count_states; i++) {
    fscanf(fr, "%u|", &state[i].trans_count);
  }
  // second parse transition char with destination state
  for (i = 0; i < count_states; i++) {
    state[i].trans_char = (u_i *) malloc(state[i].trans_count * sizeof(u_i));
    state[i].trans_dest = (u_i *) malloc(state[i].trans_count * sizeof(u_i));
    if (state[i].trans_char == NULL || state[i].trans_dest == NULL) {
      fprintf(stderr, "Error: not enough memory!\n");
      for (j = 0; j <= i; j++) {
        free(state[j].trans_char); free(state[j].trans_dest);
      }
      free(state); free(alp_in_begin); free(alp_in_end); free(alphabet);
      exit(1);
    }
    for (j = 0; j < state[i].trans_count; j++) {
      fscanf(fr, "%u->%u|", &state[i].trans_char[j], &state[i].trans_dest[j]);
    }
  }
  /* parse FINAL STATES */
  fscanf(fr, "%u", &count_final_states);
  final_states = (u_i *) malloc(count_final_states * sizeof(u_i));
  if (final_states == NULL) {
    fprintf(stderr, "Error: not enough memory!\n");
    free_memory();
    exit(1);
  }
  for (i = 0; i < count_final_states; i++) {
    fscanf(fr, "%u|", &final_states[i]);
  }
  /* parse DEFAULT TRANSITIONS */
  for (i = 0; i < count_states; i++) {
    fscanf(fr, "%d|", &state[i].def_trans);
  }
  // close parse file
  if (fclose(fr) == EOF) {
    fprintf(stderr, "Error: file \"%s\" could not be closed!\n", FileName);
    // do not exit here, just continue with error printed
  }
}

/* Passing through automat with chars from file
   which is second argument of program. */
void passing_automat(char *FileName)
{
  FILE *fr;
  u_i finite_state = 0;       /* indication automat about in finite state */
  int c;                      /* one input char from file */
  u_i cur_state = start_state;/* current state */
  u_i i, j, k, flag;          /* helpful variables */
  u_i num_char = 0;           /* number of actual char in file */
  u_i num_tran = 0;    /* number of actually executed transitions */
  u_i num_def_tran = 0;/* number of actually executed default transitions */

  // open dafa file
  if ((fr = fopen(FileName, "rb")) == NULL) {
    fprintf(stderr, "Error: file \"%s\" could not be open for reading!\n",
        FileName);
    free_memory();
    exit(1);
  }
  // Follow algorithm for way through automat.
  while ((c = getc(fr)) != EOF) {
    ++num_char;
    flag = 0;
    // in current state try all transitions
    process_char:
    for (j = 0; j < state[cur_state].trans_count; j++) {
      for (k = alp_in_begin[state[cur_state].trans_char[j]];
         k <= alp_in_end[state[cur_state].trans_char[j]]; k++) {
        // found transition for actual working char ->
        if (c == alphabet[k]) {
          ++num_tran;
          // -> move to next state
          cur_state = state[cur_state].trans_dest[j];
          flag = 1;
          break;
        }
      }
      // found transition for actual working char ->
      if (flag) {
        // -> skip working on other transitions
        break;
      }
    }
    // was NOT found any transition for actual working char
    if (!flag) {
      ++num_tran;
      // unknown char for current state and do not exist default
      // transition from this state -> go to start state
      if (state[cur_state].def_trans == -1) {
        if (cur_state != start_state) {
          cur_state = start_state;
        } else {
          // we are in start state and have not transition for
          // working char -> skip looking for finite state and
          // immediately move to next char
          continue;
        }
      } else {
        // default transition
        ++num_def_tran;
        cur_state = state[cur_state].def_trans;
        goto process_char;
      }
    }
    // algorithm is in any finite state of automat
    for (i = 0; i < count_final_states; i++) {
      if (cur_state == final_states[i]) {
        printf("*** match on char %u, state %u ***\n", num_char, cur_state);
        finite_state = 1;
        break;
      }
    }
  }
  free_memory();
  // algorithm was NOT anytime in finite state
  if (!finite_state) {
    printf("\n*** Result: NOT match ***\n\n");
  }
  // print number of executed def. tran.
  printf("Number of OVERALL executed transitions: %u\n", num_tran);
  printf("Number of executed DEFAULT transitions: %u\n", num_def_tran);
  // close data file
  if (fclose(fr) == EOF) {
    fprintf(stderr, "Error: file \"%s\" could not be closed!\n", FileName);
    // do not exit here, just continue with error printed
  }
}

/* MAIN function */
int main(int argc, char *argv[])
{
  if (argc == 3) {
    parse_file(argv[1]);
    passing_automat(argv[2]);
  } else {
    fprintf(stderr, "Error: bad arguments!\n");
    fprintf(stderr, "Example: ./ddfa parse_file data_file\n");
    exit(1);
  }
  return 0;
}

