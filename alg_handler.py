import copy


# applies an algorithm to a cube
def apply_alg(algorithm, cube):
    move_dict = {"U": cube.u_move,
                 "U'": cube.u_prime_move,
                 "U2": cube.u2_move,
                 "R": cube.r_move,
                 "R2": cube.r2_move,
                 "R'": cube.r_prime_move,
                 "F": cube.f_move,
                 "F2": cube.f2_move,
                 "F'": cube.f_prime_move,
                 "B": cube.b_move,
                 "B2": cube.b2_move,
                 "B'": cube.b_prime_move,
                 "L": cube.l_move,
                 "L2": cube.l2_move,
                 "L'": cube.l_prime_move,
                 "D": cube.d_move,
                 "D2": cube.d2_move,
                 "D'": cube.d_prime_move,
                 "S": cube.s_move,
                 "S'": cube.s_prime_move,
                 "S2": cube.s2_move,
                 "M": cube.m_move,
                 "M'": cube.m_prime_move,
                 "M2": cube.m2_move,
                 "u": cube.u_wide_move,
                 "u2": cube.u2_wide_move,
                 "u'": cube.u_prime_wide_move,
                 "d": cube.d_wide_move,
                 "d2": cube.d2_wide_move,
                 "d'": cube.d_prime_wide_move,
                 "f": cube.f_wide_move,
                 "f'": cube.f_prime_wide_move,
                 "f2": cube.f2_wide_move,
                 "b": cube.b_wide_move,
                 "b2": cube.b2_wide_move,
                 "b'": cube.b_prime_wide_move,
                 "r": cube.r_wide_move,
                 "r2": cube.r2_wide_move,
                 "r'": cube.r_prime_wide_move,
                 "l": cube.l_wide_move,
                 "l2": cube.l2_wide_move,
                 "l'": cube.l_prime_wide_move,
                 "E": cube.e_move,
                 "E2": cube.e2_move,
                 "E'": cube.e_prime_move
                 }
    for move in algorithm:
        move_dict[move]()


# dependency of cube class
def simplify_move(move):
    if len(move) == 2:
        move = move[0:1]
    return move


# dependency of invert_move_list
def invert_move(move):
    if move[-1] == "'":
        move = move[0:1]
    elif move[-1] != "'" and move[-1] != "2":
        move += "'"
    return move


# parsing functions
def double_to_normal(move):
    return move[0:1]


def double_to_prime(move):
    return move[0:1] + "'"


def normal_to_double(move):
    return move + "2"


def prime_to_double(move):
    return move[0:1] + "2"


def invert_move_list(move_list):
    for i, move in enumerate(move_list):
        move_list[i] = invert_move(move)
    return move_list


def reverse_move_list(move_list):
    reversed_list = copy.deepcopy(move_list)
    reversed_list.reverse()
    return reversed_list


def reverse_and_invert_move_list(move_list):
    move_list = reverse_move_list(move_list)
    invert_move_list(move_list)
    return move_list


# connects the left and right ends of move lists correctly and returns the result
def clean_up_intersection(lista, listb):
    list1 = copy.deepcopy(lista)
    list2 = copy.deepcopy(listb)
    if not list1:
        return list2
    elif not list2:
        return list1
    elif list1[-1][0] != list2[0][0]:
        # print(f"list1: {list1} list2: {list2}")
        return list1 + list2
    else:
        if list1[-1][-1] == "'":
            if list2[0][-1] == "'":  # prime + prime = double
                list1[-1] = prime_to_double(list1[-1])
            elif list2[0][-1] == "2":  # prime + double = normal
                list1[-1] = invert_move(list1[-1])
            else:  # prime + normal = cancel
                list1 = list1[0:-1]

        elif list1[-1][-1] == "2":
            if list2[0][-1] == "'":  # double + prime = normal
                list1[-1] = double_to_normal(list1[-1])
            elif list2[0][-1] == "2":  # double + double = cancel
                list1 = list1[0:-1]
            else:  # double + normal = prime
                list1[-1] = double_to_prime(list1[-1])

        else:
            if list2[0][-1] == "'":  # normal + prime = cancel
                list1 = list1[0:-1]
            elif list2[0][-1] == "2":  # normal + double = prime
                list1[-1] = invert_move(list1[-1])
            else:  # normal + normal = double
                list1[-1] = normal_to_double(list1[-1])

        list2 = list2[1:]  # remove list2 starting element
        return clean_up_intersection(list1, list2)
