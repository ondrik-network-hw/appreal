/***************************************************************************
############################################################################
#  history_fa.c: Algorithm for History based FA (transit through automat)
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
 *  history_fa.c  ver. 0.9
 *
 *  Algorithm for History based FA (transit through automat)
 *  ========================================================
 *
 *  Jaroslav Suchodol,  August 2010
 *
 */

#include <stdio.h>
#include <stdlib.h>

# define false 0
# define true 1

typedef unsigned int u_i;

// FLAGS
// 0 >= counter, -2 = set, -3 = must be set, -4 = reset, -5 = muset be reset

// Transition for History based FA.
typedef struct t_h_t {
  u_i *c;   // transition char(s)
  u_i c_c;  // count char for transition
  u_i d;    // destination state of transition
  u_i n_c;  // needed flag count
  int *n_f; // needed flag
  u_i *n_i; // needed flag index
  u_i a_c;  // after transition count
  int *a_f; // after flag
  u_i *a_i; // after flag index
} T_H_T;

// State for History based FA.
typedef struct t_h_s {
  T_H_T *t; // transitions for state
  u_i t_c;  // t_c=trans_count
  u_i f;    // mark of the final state
} T_H_S;

// History based FA.
typedef struct t_h {
  T_H_S *s;   // states of HFA
  u_i s_c;    // states count
  u_i s_s;    // start state
} T_H;      // T_HISTORY_FA

// Counter.
typedef struct t_c {
  u_i c;  // count
  u_i a;  // activation (true, false)
  u_i f;  // flag asociated with counter
} T_C;

// global variables
T_H h;        // History automat
u_i *flag;    // flags
u_i flag_c;   // flags count
T_C *ctr;     // counters
u_i ctr_c;    // counters count

// Parse input file (first argument of program) and 
// make structure from it for later use.
void parse_file(char *FileName)
{
  FILE *fr;
  u_i i, j, k;

  // open parse file
  if ((fr = fopen(FileName, "r")) == NULL) {
    fprintf(stderr, "Error: file \"%s\" could not be open for reading!\n",
    FileName);
    exit(1);
  }
  // fill data structures
  // parse COUNT OF STATES
  fscanf(fr, "%u\n", &h.s_c);
  h.s = (T_H_S *) malloc(h.s_c * sizeof(T_H_S));
  if (h.s == NULL) {
    fprintf(stderr, "Error: not enough memory!\n");
    exit(1);
  }
  // parse STARTING STATE
  fscanf(fr, "%u\n", &h.s_s);
  // parse TRANSITIONS between states
  for (i = 0; i < h.s_c; i++) {
    // count transitions for given state
    fscanf(fr, "t_c: %u\n", &h.s[i].t_c);
    h.s[i].t = (T_H_T *) malloc(h.s[i].t_c * sizeof(T_H_T));
    if (h.s[i].t == NULL) {
      fprintf(stderr, "Error: not enough memory!\n");
      exit(1);
    }
    // fill chars, count chars, destination state
    for (j = 0; j < h.s[i].t_c; j++) {
      fscanf(fr, "c_c: %u, d: %u\n", &h.s[i].t[j].c_c, &h.s[i].t[j].d);
      h.s[i].t[j].c = (u_i *) malloc(h.s[i].t[j].c_c * sizeof(u_i));
      if (h.s[i].t[j].c == NULL) {
        fprintf(stderr, "Error: not enough memory!\n");
        exit(1);
      }
      for (k = 0; k < h.s[i].t[j].c_c; k++) {
        fscanf(fr, "%u|", &h.s[i].t[j].c[k]);
      }
      fscanf(fr, "\n");
      // fill conditions for transition
      fscanf(fr, "n_c: %u, a_c: %u\n", &h.s[i].t[j].n_c, &h.s[i].t[j].a_c);
      h.s[i].t[j].n_f = (int *) malloc(h.s[i].t[j].n_c * sizeof(int));
      h.s[i].t[j].n_i = (u_i *) malloc(h.s[i].t[j].n_c * sizeof(u_i));
      h.s[i].t[j].a_f = (int *) malloc(h.s[i].t[j].a_c * sizeof(int));
      h.s[i].t[j].a_i = (u_i *) malloc(h.s[i].t[j].a_c * sizeof(u_i));
      if (h.s[i].t[j].n_f == NULL || h.s[i].t[j].n_i == NULL ||
        h.s[i].t[j].a_f == NULL || h.s[i].t[j].a_i == NULL) {
        fprintf(stderr, "Error: not enough memory!\n");
        exit(1);
      }
      for (k = 0; k < h.s[i].t[j].n_c; k++) {
        fscanf(fr, "%d->%u|", &h.s[i].t[j].n_f[k], &h.s[i].t[j].n_i[k]);
      }
      fscanf(fr, "\n");
      for (k = 0; k < h.s[i].t[j].a_c; k++) {
        fscanf(fr, "%d->%u|", &h.s[i].t[j].a_f[k], &h.s[i].t[j].a_i[k]);
      }
      fscanf(fr, "\n");
    }
  }
  // parse FINAL STATES
  u_i s_f_c;
  fscanf(fr, "%u\n", &s_f_c);
  for (i = 0; i < s_f_c; i++) {
    fscanf(fr, "%u|", &j);
    h.s[j].f = true;
  }
  fscanf(fr, "\n");
  // parse count of flags and counters
  fscanf(fr, "flags: %u\ncounters: %u\n", &flag_c, &ctr_c);
  flag = (u_i *) malloc(flag_c * sizeof(u_i));
  ctr = (T_C *) malloc(ctr_c * sizeof(T_C));
  if (flag == NULL || ctr == NULL) {
    fprintf(stderr, "Error: not enough memory!\n");
    exit(1);
  }
  // parse flag acociated with counter
  for (i = 0; i < ctr_c; i++) {
    fscanf(fr, "%u|", &ctr[i].f);
  }
  fscanf(fr, "\n");
  // initialize flags and counters
  // set all flags to false meaning they are not set
  for (i = 0; i < flag_c; i++) {
    flag[i] = false;
  }
  // set all counters to -1 meaning they are not set
  for (i = 0; i < ctr_c; i++) {
    ctr[i].c = -1;
    ctr[i].a = false; // inactive counter
  }
  // close parse file
  if (fclose(fr) == EOF) {
    fprintf(stderr, "Error: file \"%s\" could not be closed!\n", FileName);
  }
}

// Passing through automat with chars from file
// which is second argument of program.
void passing_automat(char *FileName)
{
  FILE *fr;
  int c;            // one input char from file
  u_i c_s = h.s_s;  // current state
  u_i i, j, k, aux; // helpful variables
  int *p_n_f;       // helpful pointer
  u_i *p_n_i;       // helpful pointer

  // open data file
  if ((fr = fopen(FileName, "rb")) == NULL) {
    fprintf(stderr, "Error: file \"%s\" could not be open for reading!\n",
    FileName);
    exit(1);
  }
  // Follow algorithm for way through automat.
  next_char:
  while ((c = getc(fr)) != EOF) {
    // decrement activated counters
    for (i = 0; i < ctr_c; i++) {
      if (ctr[i].a == true) {
        if (ctr[i].c > 0) {
          ctr[i].c = ctr[i].c - 1;
        }
        else {
          // deactivate counter + flag
          ctr[i].a = false;
          flag[ctr[i].f] = false;
        }
      }
    }
    // in current state try all transitions
    for (i = 0; i < h.s[c_s].t_c; i++) {
      for (j = 0; j < h.s[c_s].t[i].c_c; j++) {
        aux = true;
        // found transition for working char
        if (c == h.s[c_s].t[i].c[j]) {
          // check for needed properties
          for (p_n_f = h.s[c_s].t[i].n_f, p_n_i = h.s[c_s].t[i].n_i;
              p_n_i < h.s[c_s].t[i].n_i + h.s[c_s].t[i].n_c;
              p_n_f++, p_n_i++) {
            // check counter
            if (*p_n_f == 0) {
              if (ctr[*p_n_i].c != 0) {
                aux = false;
                break;
              }
            }
            // check set flag
            else if (*p_n_f == -3 && flag[*p_n_i] != true) {
              aux = false;
              break;
            }
            // check reset flag
            else if (*p_n_f == -5 && flag[*p_n_i] != false) {
              aux = false;
              break;
            }
          }
          // everythink all right
          if (aux) {
            // do after properties
            for (k = 0; k < h.s[c_s].t[i].a_c; k++) {
              // set counter
              if (h.s[c_s].t[i].a_f[k] > 0) {
                ctr[h.s[c_s].t[i].a_i[k]].c = h.s[c_s].t[i].a_f[k];
                // activate counter
                ctr[h.s[c_s].t[i].a_i[k]].a = true;
              }
              // reset counter
              else if (h.s[c_s].t[i].a_f[k] == 0) {
                ctr[h.s[c_s].t[i].a_i[k]].c = h.s[c_s].t[i].a_f[k];
                // deactivate counter
                ctr[h.s[c_s].t[i].a_i[k]].a = false;
              }
              else {
                // set up flag
                if (h.s[c_s].t[i].a_f[k] == -2) 
                  flag[h.s[c_s].t[i].a_i[k]] = true;
                // reset flag
                else if (h.s[c_s].t[i].a_f[k] == -4) 
                  flag[h.s[c_s].t[i].a_i[k]] = false;
              }
            }
            // move to destinaton state
            c_s = h.s[c_s].t[i].d;
            // check for final state
            if (h.s[c_s].f == true) {
              printf("\n*** Result: match ***\n\n");
              goto finish_after_match;
            }
            goto next_char;
          }
        }
      }
    }
  }
  // algorithm was NOT anytime in finite state
  printf("\n*** Result: NOT match ***\n\n");
  finish_after_match:
  // close data file
  if (fclose(fr) == EOF) {
    fprintf(stderr, "Error: file \"%s\" could not be closed!\n", FileName);
  }
}

// Main function.
int main(int argc, char *argv[])
{
  if (argc == 3) {
    parse_file(argv[1]);
    passing_automat(argv[2]);
  } else {
    fprintf(stderr, "Error: bad arguments!\n");
    fprintf(stderr, "Example: ./history_fa parse_file data_file\n");
    exit(1);
  }
  return 0;
}

