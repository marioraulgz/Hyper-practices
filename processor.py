def create_matrix(matrix_by_order):
    matrix_dimensions = input('Enter size of{} matrix: '.format(matrix_by_order)).split()
    print('Enter{} matrix: '.format(matrix_by_order))
    a = [[int(i) if i.isdigit() else float(i) for i in input().split()] for j in range(int(matrix_dimensions[0]))]
    return a


def print_matrix(matrix):
    for i, _ in enumerate(matrix):
        print(" ".join(matrix[i]))


def matrix_sum(matrix_1, matrix_2):
    summed_matrix = []
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        return 'The operation cannot be performed.'
    else:
        for i, _ in enumerate(matrix_1):
            matrix_row_sum = [str(matrix_1[i][j] + matrix_2[i][j]) for j, _ in enumerate(matrix_1[0])]
            summed_matrix.append(matrix_row_sum)
        return summed_matrix


def scalar_multiplication(constant, matrix):
    scaled_matrix = []
    constant = to_num(constant)
    for i, _ in enumerate(matrix):
        matrix_row_scalar = [
            str(constant * matrix[i][j]) for j, _ in enumerate(matrix[0])]
        scaled_matrix.append(matrix_row_scalar)
    return scaled_matrix


def to_num(x):
    if type(x) != int and type(x) != float:
        if x.isdigit():
            x = int(x)
        else:
            x = float(x)
    return x


def matrix_multiplication(matrix_1, matrix_2):
    multiplied_matrix = []
    if len(matrix_1[0]) != len(matrix_2):
        return 'The operation cannot be performed.'
    else:
        for i, _ in enumerate(matrix_1):
            matrix_row_multiplication = [str(sum(
                [matrix_1[i][j] * matrix_2[j][k] for j, _ in
                 enumerate(matrix_2)])) for k, _ in enumerate(matrix_2[0])]
            multiplied_matrix.append(matrix_row_multiplication)
        return multiplied_matrix


def main_diagonal_transpose(matrix):
    transposed_matrix = [[str(matrix[j][i]) for j, _ in enumerate(matrix[0])] for i, _ in enumerate(matrix)]
    return transposed_matrix


def side_diagonal_transpose(matrix):
    matrix.reverse()
    columns = len(matrix[0])
    transposed_matrix = [[str(matrix_.pop()) for matrix_ in matrix] for j in range(columns)]
    return transposed_matrix


def vertical_transpose(matrix):
    matrix_new = matrix_to_str(matrix)
    for i, _ in enumerate(matrix_new):
        matrix_new[i].reverse()
    return matrix_new


def horizontal_transpose(matrix):
    matrix_new = matrix_to_str(matrix)
    matrix_new.reverse()
    return matrix_new


def check_validity(operated_matrix):
    if operated_matrix != 'The operation cannot be performed.':
        print('The result is:')
        print_matrix(operated_matrix)
        print()
    else:
        print(operated_matrix)


def matrix_to_str(matrix):
    new_matrix = [[str(i) for i in matrix[j]] for j, _ in enumerate(matrix)]
    return new_matrix


def matrix_to_number(matrix):
    new_matrix = [[int(i) if i.isdigit() else float(i) for i in matrix[j]] for j, _ in enumerate(matrix)]
    return new_matrix


def minors(matrix, i, j):
    return [[matrix[h][k] for k, _ in enumerate(matrix) if k != j] for h, _ in enumerate(matrix) if h != i]


def determinant(matrix, reference_row=0):
    if len(matrix) == 1:
        return matrix[0][0]
    else:
        det = 0
        for j, coef in enumerate(matrix[0]):
            minor = minors(matrix, reference_row, j)
            det += ((-1) ** (reference_row + j)) * coef * determinant(minor)
        return det


def matrix_inverse(matrix):
    if determinant(matrix) == 0:
        print("This matrix doesn't have an inverse.")
    else:
        cofactor_matrix = [[((-1) ** (i + j)) * determinant(minors(matrix, i, j)) for j, _ in enumerate(matrix[0])] for
                           i, _ in enumerate(matrix)]
        cofactor_matrix_str = main_diagonal_transpose(cofactor_matrix)
        cofactor_matrix_number = matrix_to_number(cofactor_matrix_str)
        return scalar_multiplication(1 / determinant(matrix), cofactor_matrix_number)


def menu_matrix():
    print("""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit """)
    return input("Your choice: ")


def menu_transposes():
    print("""1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
    return input("Your choice: ")


def matrix_transposes():
    while True:
        choice = menu_transposes()
        if choice == '1':
            matrix = create_matrix('')
            operated_matrix = main_diagonal_transpose(matrix)
            check_validity(operated_matrix)
        elif choice == '2':
            matrix = create_matrix('')
            operated_matrix = side_diagonal_transpose(matrix)
            check_validity(operated_matrix)
        elif choice == '3':
            matrix = create_matrix('')
            operated_matrix = vertical_transpose(matrix)
            check_validity(operated_matrix)
        elif choice == '4':
            matrix = create_matrix('')
            operated_matrix = horizontal_transpose(matrix)
            check_validity(operated_matrix)
        elif choice == '0':
            print()
            quit()


def matrix_operations():
    while True:
        choice = menu_matrix()

        if choice == '1':
            matrix_1 = create_matrix(' first')
            matrix_2 = create_matrix(' second')
            operated_matrix = matrix_sum(matrix_1, matrix_2)
            check_validity(operated_matrix)
        elif choice == '2':
            matrix = create_matrix('')
            constant = input('Enter constant: ')
            operated_matrix = scalar_multiplication(constant, matrix)
            check_validity(operated_matrix)
        elif choice == '3':
            matrix_1 = create_matrix(' first')
            matrix_2 = create_matrix(' second')
            operated_matrix = matrix_multiplication(matrix_1, matrix_2)
            check_validity(operated_matrix)
        elif choice == '4':
            print()
            matrix_transposes()
        elif choice == '5':
            matrix = create_matrix('')
            print("The result is:\n{}\n".format(determinant(matrix)))
        elif choice == '6':
            matrix = create_matrix('')
            operated_matrix = matrix_inverse(matrix)
            check_validity(operated_matrix)
        elif choice == '0':
            break


matrix_operations()
