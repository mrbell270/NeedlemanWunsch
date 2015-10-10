# coding=utf-8
__author__ = 'Lenovo'


def horizontal_max(f_matrix, i, j, gap):
    scores = []
    for k in range(1, j):
        scores.append(f_matrix[i][j-k] + k * gap)
    if not len(scores):
        return 0
    return max(scores)


def vertical_matrix(f_matrix, i, j, gap):
    scores = []
    for k in range(1, i):
        scores.append(f_matrix[i-k][j] + k * gap)
    if not len(scores):
        return 0
    return max(scores)


def max_matrix(f_matrix):
    s_max = f_matrix[0][0]
    i_max = 0
    j_max = 0
    for i in range(len(f_matrix)):
        for j in range(len(f_matrix[i])):
            if f_matrix[i][j] >= s_max:
                s_max = f_matrix[i][j]
                i_max = i
                j_max = j
    return s_max, i_max, j_max


def matrix_filling(seq, s_matrix, gap):
    """
    Filling matrix according to Needleman-Wunsch algorithm
    :param seq: [2]string
    :param s_matrix: dict( char -> dict( char -> int))
    :param gap: int
    :return: [][]int
    """
    f_matrix = [[0 for x in range(len(seq[1]) + 1)] for x in range(len(seq[0]) + 1)]  # Crating F-matrix, init with 0s

    for i in range(len(f_matrix)):  # Filling first row and column
        if i:
            f_matrix[i][0] = 0
    for j in range(len(f_matrix[0])):
        if j:
            f_matrix[0][j] = 0
    for i in range(len(f_matrix)):  # Filling all other cells
        if not i:
            continue
        for j in range(len(f_matrix[i])):
            if not j:
                continue
            delta = s_matrix[seq[0][i - 1]][seq[1][j - 1]]
            f_matrix[i][j] = max(0,  # Choosing max of variants
                                 f_matrix[i - 1][j - 1] + delta,
                                 horizontal_max(f_matrix, i, j, gap),
                                 vertical_matrix(f_matrix, i, j, gap))
    return f_matrix


def result_seq(f_matrix, seq, s_matrix, gap):
    """
    Finding trace in F matrix and getting resulting sequences
    :param f_matrix: [][]int
    :param seq: [2]string
    :param s_matrix: dict( char -> dict( char -> int))
    :param gap: int
    :return: [2]string
    """
    res1 = ""
    res2 = ""
    score, i, j = max_matrix(f_matrix)
    print(i,j)
    while i > 0 and j > 0 and f_matrix[i][j] > 0:
        print(i, j, res1, res2)
        if i > 0 and j > 0 and f_matrix[i][j] == f_matrix[i - 1][j - 1] + s_matrix[seq[0][i - 1]][seq[1][j - 1]]:
            i -= 1
            j -= 1
            res1 = seq[0][i] + res1
            res2 = seq[1][j] + res2
        elif i > 0 and f_matrix[i][j] == f_matrix[i - 1][j] + gap:
            i -= 1
            res1 = seq[0][i] + res1
            res2 = "-" + res2
        else:
            j -= 1
            res1 = "-" + res1
            res2 = seq[1][j] + res2
    return res1, res2, score
