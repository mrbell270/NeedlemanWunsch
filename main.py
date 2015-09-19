__author__ = 'Lenovo'
import NeedlemanWunsch


def print_matrix(m, seq):
    """
    Printing sequences and matrix
    :param m: [][]int
    :param seq: [2]string
    :return:
    """
    print('{:10}'.format("")),
    for char in seq[0]:
        print('{:4}'.format(char)),
    print
    for i in range(len(m)):
        if not i:
            print('{:2}'.format("")),
        else:
            print('{:2}'.format(seq[1][i-1])),
        for j in range(len(m[i])):
            print('{:4}'.format(m[i][j])),
        print


def main():
    seq = []
    scores = [0, 0, 0]

    filename = raw_input('File with sequences: ')   # Input path to file, containing 2 sequences
    if filename == '':
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

    scores[0] = -1   # mismatch
    scores[1] = 1    # match
    scores[2] = -1   # gap
    print('Default scores:\nMismatch {}\nMatch {}\nGap {}\n'.format(scores[0], scores[1], scores[2]))
    flag = raw_input('Do you want to change it? (y/n) ')
    if flag == 'y':
        scores[0] = int(raw_input('Mismatch score: '))   #
        scores[1] = int(raw_input('Match score: '))      # Scores input
        scores[2] = int(raw_input('Indel/gap score: '))  #
    elif flag == 'n':
        print('Working with default')

    f_matrix = NeedlemanWunsch.matrix_filling(seq, scores)

    seq[0], seq[1] = NeedlemanWunsch.result_seq(f_matrix, seq, scores)
    print('\nResult sequences:\n{}\n{}'.format(seq[0], seq[1]))
    print('Score {}'.format(f_matrix.pop().pop()))

if __name__ == '__main__':
    main()
