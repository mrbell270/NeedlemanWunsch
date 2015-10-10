# coding=utf-8
__author__ = 'Lenovo'

from collections import namedtuple

MatrixCell = namedtuple('MatrixCell', 'score up_gap_length left_gap_length')


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
            print('{:2}'.format(seq[0][i - 1])),
        for j in range(len(m[i])):
            print('{:4}'.format(m[i][j])),
        print


def gap_line(gap, length):
    if length > 0:
        return gap[0] + (length - 1) * gap[1]
    else:
        return 0


def horizontal_max(f_matrix, i, j, gap):
    scores = []
    for k in range(1, j):
        scores.append(f_matrix[i][j-k].score + gap_line(gap, k))
    if not len(scores):
        return 0
    return max(scores)


def vertical_matrix(f_matrix, i, j, gap):
    scores = []
    for k in range(1, i):
        scores.append(f_matrix[i-k][j].score + gap_line(gap, k))
    if not len(scores):
        return 0
    return max(scores)


def max_matrix(f_matrix):
    s_max = f_matrix[0][0].score
    i_max = 0
    j_max = 0
    for i in range(len(f_matrix)):
        for j in range(len(f_matrix[i])):
            if f_matrix[i][j].score >= s_max:
                s_max = f_matrix[i][j].score
                i_max = i
                j_max = j
    return s_max, i_max, j_max


def matrix_filling_SW(seq, s_matrix, gap):
    """
    Filling matrix according to Smith-Waterman algorithm
    :param seq: [2]string
    :param s_matrix: dict( char -> dict( char -> int))
    :param gap: [2]int
    :return:  [2]string, int
    """
    f_matrix = []  # Crating F-matrix, init with 0s
    for x in range(len(seq[0]) + 1):
        f_matrix.append([MatrixCell(0, 0, 0) for x in range(len(seq[1]) + 1)])

    print(f_matrix)
    for i in range(1, len(f_matrix)):  # Filling all other cells
        for j in range(1, len(f_matrix[i])):
            delta = s_matrix[seq[0][i - 1]][seq[1][j - 1]]
            diag = f_matrix[i - 1][j - 1].score + delta
            h_max = horizontal_max(f_matrix, i, j, gap)
            v_max = vertical_matrix(f_matrix, i, j, gap)
            score = max(0, diag, h_max, v_max)  # Choosing max of variants
            if score == 0 or f_matrix[i][j].score == diag:
                u_gap = 0
                l_gap = 0
            elif score == h_max:
                u_gap = 0
                l_gap = f_matrix[i][j - 1].left_gap_length + 1
            elif score == v_max:
                u_gap = f_matrix[i - 1][j].up_gap_length + 1
                l_gap = 0
            f_matrix[i][j] = MatrixCell(score, u_gap, l_gap)
    print_matrix(f_matrix, seq)
    return result_seq(f_matrix, seq, s_matrix, gap)


def result_seq(f_matrix, seq, s_matrix, gap):
    """
    Finding trace in F matrix and getting resulting sequences
    :param f_matrix: [][]MatrixCell
    :param seq: [2]string
    :param s_matrix: dict( char -> dict( char -> int))
    :param gap: [2]int
    :return:  [2]string, int
    """
    res1 = ""
    res2 = ""
    score, i, j = max_matrix(f_matrix)
    while f_matrix[i][j] > 0:
        if i > 0 and j > 0 and f_matrix[i][j].score == f_matrix[i - 1][j - 1].score + s_matrix[seq[0][i - 1]][seq[1][j - 1]]:
            i -= 1
            j -= 1
            res1 = seq[0][i] + res1
            res2 = seq[1][j] + res2
        elif i > 0 and f_matrix[i][j].score == f_matrix[i - 1][j].score + gap_line(gap, 1):
            i -= 1
            res1 = seq[0][i] + res1
            res2 = "-" + res2
        else:
            j -= 1
            res1 = "-" + res1
            res2 = seq[1][j] + res2
    return res1, res2, score
