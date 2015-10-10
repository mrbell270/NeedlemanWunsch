__author__ = 'Lenovo'
import NeedlemanWunsch
import SmithWaterman
import re


def print_matrix(m, seq):
    """
    Printing sequences and matrix
    :param m: [][]int
    :param seq: [2]string
    :return:
    """
    print('{:10}'.format("")),
    for char in seq[1]:
        print('{:4}'.format(char)),
    print
    for i in range(len(m)):
        if not i:
            print('{:2}'.format("")),
        else:
            print('{:2}'.format(seq[0][i-1])),
        for j in range(len(m[i])):
            print('{:4}'.format(m[i][j])),
        print


def ask(question):
    answer = raw_input('{} (y/n)'.format(question))
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        ask(question)

def main():
    # TODO Add non-linear indel.
    seq = []
    filename = raw_input('File with sequences: ')   # Input path to file, containing 2 sequences.
    if filename == '':                              # If no input, open default.
        filename = r"file.txt"
    f = open(filename)
    line = f.readline()
    while line != '':   # Scanning file for sequences
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
        mismatch = -1   # default mismatch
        match = 1    # default match
        gap = -1   # default gap

        print('Default scores:\nMismatch {}\nMatch {}\nGap {}\n'.format(mismatch, match, gap))
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
                mismatch = int(raw_input('Mismatch score: '))  #
                match = int(raw_input('Match score: '))        # Scores input.
                gap = int(raw_input('Indel/gap score: '))      #
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
        gap = int(raw_input('Gap score: '))
        f = open(r"blosum62.txt")
        raw_matrix = [line.split() for line in f]
        f.close()
        raw_dicts = [0 for x in range(len(raw_matrix[0]))]
        for i in range(len(raw_matrix[0])):
            raw_dicts[i] = dict(zip(raw_matrix[0], map(int, raw_matrix[i+1])))

        s_matrix = dict()
        for i in range(len(raw_matrix[0])):
            s_matrix[raw_matrix[0][i]] = raw_dicts[i]

    flag = ask('Do you want to use global(y) or local(n) alignment?')
    if flag:
        f_matrix = NeedlemanWunsch.matrix_filling(seq, s_matrix, gap)  # Filling F-matrix, Needleman-Wunsch algorithm.
        print_matrix(f_matrix, seq)
        seq[0], seq[1], max_score = NeedlemanWunsch.result_seq(f_matrix, seq, s_matrix, gap)  # Getting results.
    else:
        f_matrix = SmithWaterman.matrix_filling(seq, s_matrix, gap)  # Filling F-matrix, Smith-Waterman algorithm.
        print_matrix(f_matrix, seq)
        seq[0], seq[1], max_score = SmithWaterman.result_seq(f_matrix, seq, s_matrix, gap)  # Getting results.

    print('\nResult sequences:\n{}\n{}\nScore {}'.format(seq[0], seq[1], max_score))

if __name__ == '__main__':
    main()
