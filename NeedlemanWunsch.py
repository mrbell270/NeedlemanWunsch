# coding=utf-8
__author__ = 'Lenovo'


def matrix_filling(seq, scores):
    """
    Filling matrix according to Needleman-Wunsch algorithm
    :param seq: [2]string
    :param scores: [3]int
    :return: [][]int
    """
    f_matrix = [[0 for x in range(len(seq[1]) + 1)] for x in range(len(seq[0]) + 1)]  # Crating F-matrix, init with 0s
    gap = scores[2]

    for i in range(len(f_matrix)):  # Filling first row and column
        if i:
            f_matrix[i][0] = f_matrix[i - 1][0] + gap
    for j in range(len(f_matrix[0])):
        if j:
            f_matrix[0][j] = f_matrix[0][j - 1] + gap

    for i in range(len(f_matrix)):  # Filling all other cells
        if not i:
            continue
        for j in range(len(f_matrix[i])):
            if not j:
                continue
            delta = scores[int(seq[0][i - 1] == seq[1][j - 1])]
            f_matrix[i][j] = max(f_matrix[i - 1][j - 1] + delta,  #
                                 f_matrix[i][j - 1] + gap,        # Choosing max of variants
                                 f_matrix[i - 1][j] + gap)        #
    return f_matrix


def result_seq(f_matrix, seq, scores):
    """
    Finding trace in F matrix and getting resulting sequences
    :param f_matrix: [][]int
    :param seq: [2]string
    :param scores: [3]int
    :return: [2]string
    """
    res1 = ""
    res2 = ""
    i = len(seq[0])
    j = len(seq[1])
    while i > 0 or j > 0:
        if i > 0 and j > 0 and f_matrix[i][j] == f_matrix[i - 1][j - 1] + scores[int(seq[0][i - 1] == seq[1][j - 1])]:
            res1 = seq[0][i - 1] + res1
            res2 = seq[1][j - 1] + res2
            i -= 1
            j -= 1
        elif i > 0 and f_matrix[i][j] == f_matrix[i - 1][j] + scores[2]:
            res1 = seq[0][i - 1] + res1
            res2 = "-" + res2
            i -= 1
        else:
            res1 = "-" + res1
            res2 = seq[1][j - 1] + res2
            j -= 1
    return res1, res2
