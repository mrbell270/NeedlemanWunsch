__author__ = 'Lenovo'

import NeedlemanWunsch
import SmithWaterman
import re


def ask(question):
    answer = raw_input('{} (y/n)'.format(question))
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        ask(question)


def main():
    seq = []
    filename = raw_input('File with sequences: ')  # Input path to file, containing 2 sequences.
    if filename == '':  # If no input, open default.
        filename = r"file.txt"
    f = open(filename)
    line = f.readline()
    while line != '':  # Scanning file for sequences
        if line.startswith('>'):
            line = f.readline()
            tmp = ''
            while not line.startswith('>') and line != '':
                tmp += line.strip('\n')
                line = f.readline()
            seq.append(''.join(tmp.upper().split()))
            continue
        line = f.readline()
    f.close()
    print('Found sequences:\n{}\n{}\n'.format(seq[0], seq[1]))

    if re.search('[^AGTC]', seq[0]) is None:  # Get type of sequence by checking for presence of letters
        seq_type = 'DNA'
    else:
        seq_type = 'Protein'
    if seq_type == 'DNA':
        # match = 1  # default match
        # mismatch = -1  # default mismatch
        # gap = [-1, 0]  # default gap
        match = 10  # default match
        mismatch = -8  # default mismatch
        gap = [-10, -1]  # default gap

        print('Default scores:\nMatch {}\nMismatch {}\nGap start {}\nGap extension {}\n'.format(match, mismatch, gap[0],
                                                                                               gap[1]))
        flag = ask('Do you want to change it?')
        if flag:
            flag = ask('Do you want to rewrite whole matrix?')
            if flag:
                print('Rewriting whole matrix')
                letter_arr = ['A', 'G', 'C', 'T']
                s_matrix = dict(zip(letter_arr, [dict(), dict(), dict(), dict()]))
                for x in range(len(letter_arr)):
                    for y in range(x, len(letter_arr)):
                        tmp = int(raw_input('{}-{} score: '.format(letter_arr[x], letter_arr[y])))
                        s_matrix[letter_arr[x]][letter_arr[y]] = tmp
                        s_matrix[letter_arr[y]][letter_arr[x]] = tmp
            else:
                print('Rewriting only sores\n')
                match = int(raw_input('Match score: '))  # Scores input.
                mismatch = int(raw_input('Mismatch score: '))
                gap[0] = int(raw_input('Gap start score: '))
                gap[1] = int(raw_input('Gap extension score: '))
                s_matrix = {
                    'A': {'A': match, 'G': mismatch, 'C': mismatch, 'T': mismatch},
                    'G': {'A': mismatch, 'G': match, 'C': mismatch, 'T': mismatch},
                    'C': {'A': mismatch, 'G': mismatch, 'C': match, 'T': mismatch},
                    'T': {'A': mismatch, 'G': mismatch, 'C': mismatch, 'T': match}
                }
        else:
            s_matrix = {
                'A': {'A': match, 'G': mismatch, 'C': mismatch, 'T': mismatch},
                'G': {'A': mismatch, 'G': match, 'C': mismatch, 'T': mismatch},
                'C': {'A': mismatch, 'G': mismatch, 'C': match, 'T': mismatch},
                'T': {'A': mismatch, 'G': mismatch, 'C': mismatch, 'T': match}
            }
            print('Working with default')
    else:
        print('Aligning proteins. Using BLOSUM62 matrix')
        gap = [0, 0]
        gap[0] = int(raw_input('Gap start score: '))
        gap[1] = int(raw_input('Gap extension score: '))
        f = open(r"blosum62.txt")
        raw_matrix = [line.split() for line in f]
        f.close()
        raw_dicts = [0 for x in range(len(raw_matrix[0]))]
        for i in range(len(raw_matrix[0])):
            raw_dicts[i] = dict(zip(raw_matrix[0], map(int, raw_matrix[i + 1])))

        s_matrix = dict()
        for i in range(len(raw_matrix[0])):
            s_matrix[raw_matrix[0][i]] = raw_dicts[i]

    flag = ask('Do you want to use global(y) or local(n) alignment?')
    if flag:
        seq[0], seq[1], max_score = NeedlemanWunsch.matrix_filling_NW(seq, s_matrix, gap)  # Getting results.
    else:
        seq[0], seq[1], max_score = SmithWaterman.matrix_filling_SW(seq, s_matrix, gap)  # Getting results.

    char = [':', '|', ' ']
    align = ''
    for i in range(len(seq[0])):
        if seq[0][i] == '-' or seq[1][i] == '-':
            align += char[2]
            continue
        align += char[int(seq[0][i] == seq[1][i])]
    print('\nScore {}\nResult sequences:\n{}\n{}\n{}'.format(max_score, seq[0], align, seq[1]))


if __name__ == '__main__':
    main()
