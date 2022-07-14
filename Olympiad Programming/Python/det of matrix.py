# Determine matrix program
# [1 2 3]
# [4 5 6]
# [7 8 9]
#
# det a = 1*5*9 + 4*3*8 + 7*2*6 - (3*5*7 + 1*8*6 + 2*4*9)
# det a = 45 + 96 + 84 - (105 + 48 + 72)
# det a = 225 - 225 = 0

# standard matrix
matrix = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# input new matrix
def input_matrix(matrix):
    for i in range(len(matrix)):
        matrix[i] = int(input("Enter num[{}]:".format(i+1)))

# calculate det for new matrix
def det(matrix):
    # 1, 5, 9
    sum1 = matrix[0] * matrix[4] * matrix[8]
    # 3, 4, 8
    sum2 = matrix[2] * matrix[3] * matrix[7]
    # 2, 6, 7
    sum3 = matrix[1] * matrix[5] * matrix[6]
    # 3, 5, 7
    usum1 = matrix[2] * matrix[4] * matrix[6]
    # 1, 6, 8
    usum2 = matrix[0] * matrix[5] * matrix[7]
    # 2, 4, 9
    usum3 = matrix[1] * matrix[3] * matrix[8] 

    res = sum1 + sum2 + sum3 - (usum1 + usum2 + usum3)
    print("Answer")
    print("det a =", res)
    print("")

def show(matrix):
    print("")
    print("Matrix:")
    print(matrix[0], matrix[4], matrix[8])
    print(matrix[2], matrix[3], matrix[7])
    print(matrix[1], matrix[5], matrix[6])
    print("")

input_matrix(matrix)
show(matrix)
det(matrix)
