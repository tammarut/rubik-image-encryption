import numpy


def upshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shift = numpy.roll(col, -n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shift[i]


def downshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shift = numpy.roll(col, n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shift[i]


def rotate180(n):
    bits = "{0:b}".format(n)
    return int(bits[::-1], 2)
