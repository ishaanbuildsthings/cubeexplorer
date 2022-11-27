# imports
from copy import deepcopy
from alg_handler import simplify_move

# constants
SOLVED_STICKER_STATE = ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜',
                        '🟥', '🟥', '🟥', '🟥', '🟥', '🟥', '🟥', '🟥', '🟥',
                        '🟦', '🟦', '🟦', '🟦', '🟦', '🟦', '🟦', '🟦', '🟦',
                        '🟧', '🟧', '🟧', '🟧', '🟧', '🟧', '🟧', '🟧', '🟧',
                        '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩',
                        '🟨', '🟨', '🟨', '🟨', '🟨', '🟨', '🟨', '🟨', '🟨',
                        ]


class Cube:
    def __init__(self):
        self.moves_applied = []
        self.parent_cube = None
        self.depth = 0
        self.allowed_moves_for_chain = ["U", "F", "R", "B", "L", "D"]

        self.uFace = SOLVED_STICKER_STATE[0:9]
        self.fFace = SOLVED_STICKER_STATE[9:18]
        self.rFace = SOLVED_STICKER_STATE[18:27]
        self.bFace = SOLVED_STICKER_STATE[27:36]
        self.lFace = SOLVED_STICKER_STATE[36:45]
        self.dFace = SOLVED_STICKER_STATE[45:54]

        self.tuple = (tuple(self.uFace), tuple(self.fFace), tuple(self.rFace),
                      tuple(self.bFace), tuple(self.lFace), tuple(self.dFace))

    def update_tuple(self):
        self.tuple = (tuple(self.uFace), tuple(self.fFace), tuple(self.rFace),
                      tuple(self.bFace), tuple(self.lFace), tuple(self.dFace))

    def is_solved(self):
        return self.uFace + self.fFace + self.rFace + self.bFace + self.lFace + self.dFace == SOLVED_STICKER_STATE

    def reset_cube_state(self):

        self.uFace = SOLVED_STICKER_STATE[0:9]
        self.fFace = SOLVED_STICKER_STATE[9:18]
        self.rFace = SOLVED_STICKER_STATE[18:27]
        self.bFace = SOLVED_STICKER_STATE[27:36]
        self.lFace = SOLVED_STICKER_STATE[36:45]
        self.dFace = SOLVED_STICKER_STATE[45:54]

    def rotate_face(self, face):
        temp0 = face[0]
        temp1 = face[1]
        temp2 = face[2]
        temp3 = face[3]
        temp5 = face[5]
        temp6 = face[6]
        temp7 = face[7]
        temp8 = face[8]

        face[0] = temp6
        face[1] = temp3
        face[2] = temp0
        face[3] = temp7
        face[5] = temp1
        face[6] = temp8
        face[7] = temp5
        face[8] = temp2

    def u_move(self):

        # bars
        tempF = self.fFace[0:3]
        tempR = self.rFace[0:3]
        tempB = self.bFace[0:3]
        tempL = self.lFace[0:3]
        self.lFace[0:3] = tempF
        self.bFace[0:3] = tempL
        self.rFace[0:3] = tempB
        self.fFace[0:3] = tempR

        # face
        self.rotate_face(self.uFace)

        self.moves_applied.append("U")

        self.update_tuple()

    def u2_move(self):
        tempF = self.fFace[0:3]
        tempR = self.rFace[0:3]
        tempB = self.bFace[0:3]
        tempL = self.lFace[0:3]

        self.lFace[0:3] = tempR
        self.bFace[0:3] = tempF
        self.rFace[0:3] = tempL
        self.fFace[0:3] = tempB

        self.rotate_face(self.uFace)
        self.rotate_face(self.uFace)

        self.moves_applied.append("U2")

        self.update_tuple()

    def u_prime_move(self):
        tempF = self.fFace[0:3]
        tempR = self.rFace[0:3]
        tempB = self.bFace[0:3]
        tempL = self.lFace[0:3]

        self.lFace[0:3] = tempB
        self.bFace[0:3] = tempR
        self.rFace[0:3] = tempF
        self.fFace[0:3] = tempL

        self.rotate_face(self.uFace)
        self.rotate_face(self.uFace)
        self.rotate_face(self.uFace)

        self.moves_applied.append("U'")

        self.update_tuple()

    def f_move(self):

        # bars
        tempU = self.uFace[8:5:-1]
        tempR = self.rFace[6] + self.rFace[3] + self.rFace[0]
        tempD = self.dFace[0:3]
        tempL = self.lFace[2] + self.lFace[5] + self.lFace[8]

        self.uFace[8:5:-1] = tempL
        self.dFace[0:3] = tempR

        self.rFace[6] = tempU[0]
        self.rFace[3] = tempU[1]
        self.rFace[0] = tempU[2]

        self.lFace[2] = tempD[0]
        self.lFace[5] = tempD[1]
        self.lFace[8] = tempD[2]

        # face
        self.rotate_face(self.fFace)

        self.moves_applied.append("F")

        self.update_tuple()

    def f2_move(self):
        self.f_move()
        self.f_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("F2")

        self.update_tuple()

    def f_prime_move(self):
        self.f_move()
        self.f_move()
        self.f_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("F'")

        self.update_tuple()

    def r_move(self):

        # bars
        tempU = self.uFace[2] + self.uFace[5] + self.uFace[8]
        tempB = self.bFace[0] + self.bFace[3] + self.bFace[6]
        tempD = self.dFace[2] + self.dFace[5] + self.dFace[8]
        tempF = self.fFace[2] + self.fFace[5] + self.fFace[8]

        self.bFace[0] = tempU[2]
        self.bFace[3] = tempU[1]
        self.bFace[6] = tempU[0]

        self.dFace[2] = tempB[2]
        self.dFace[5] = tempB[1]
        self.dFace[8] = tempB[0]

        self.fFace[2] = tempD[0]
        self.fFace[5] = tempD[1]
        self.fFace[8] = tempD[2]

        self.uFace[2] = tempF[0]
        self.uFace[5] = tempF[1]
        self.uFace[8] = tempF[2]

        # face
        self.rotate_face(self.rFace)

        self.moves_applied.append("R")

        self.update_tuple()

    def r2_move(self):
        tempU = self.uFace[8] + self.uFace[5] + self.uFace[2]
        tempB = self.bFace[0] + self.bFace[3] + self.bFace[6]
        tempD = self.dFace[8] + self.dFace[5] + self.dFace[2]
        tempF = self.fFace[8] + self.fFace[5] + self.fFace[2]

        self.uFace[8] = tempD[0]
        self.uFace[5] = tempD[1]
        self.uFace[2] = tempD[2]

        self.bFace[0] = tempF[0]
        self.bFace[3] = tempF[1]
        self.bFace[6] = tempF[2]

        self.dFace[8] = tempU[0]
        self.dFace[5] = tempU[1]
        self.dFace[2] = tempU[2]

        self.fFace[8] = tempB[0]
        self.fFace[5] = tempB[1]
        self.fFace[2] = tempB[2]

        self.rotate_face(self.rFace)
        self.rotate_face(self.rFace)

        self.moves_applied.append("R2")

        self.update_tuple()

    def r_prime_move(self):
        self.r_move()
        self.r_move()
        self.r_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("R'")

        self.update_tuple()

    def b_move(self):

        # bars
        tempU = self.uFace[2::-1]
        tempL = self.lFace[0] + self.lFace[3] + self.lFace[6]
        tempD = self.dFace[6:9]
        tempR = self.rFace[8] + self.rFace[5] + self.rFace[2]

        self.uFace[2::-1] = tempR
        self.lFace[0] = tempU[0]
        self.lFace[3] = tempU[1]
        self.lFace[6] = tempU[2]

        self.dFace[6:9] = tempL

        self.rFace[8] = tempD[0]
        self.rFace[5] = tempD[1]
        self.rFace[2] = tempD[2]

        # face
        self.rotate_face(self.bFace)

        self.moves_applied.append("B")

        self.update_tuple()

    def b2_move(self):
        self.b_move()
        self.b_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("B2")

        self.update_tuple()

    def b_prime_move(self):
        self.b_move()
        self.b_move()
        self.b_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("B'")

        self.update_tuple()

    def l_move(self):
        # bars
        tempU = self.uFace[0] + self.uFace[3] + self.uFace[6]
        tempF = self.fFace[0] + self.fFace[3] + self.fFace[6]
        tempD = self.dFace[0] + self.dFace[3] + self.dFace[6]
        tempB = self.bFace[8] + self.bFace[5] + self.bFace[2]

        self.uFace[0] = tempB[0]
        self.uFace[3] = tempB[1]
        self.uFace[6] = tempB[2]

        self.fFace[0] = tempU[0]
        self.fFace[3] = tempU[1]
        self.fFace[6] = tempU[2]

        self.dFace[0] = tempF[0]
        self.dFace[3] = tempF[1]
        self.dFace[6] = tempF[2]

        self.bFace[8] = tempD[0]
        self.bFace[5] = tempD[1]
        self.bFace[2] = tempD[2]

        # face
        self.rotate_face(self.lFace)

        self.moves_applied.append("L")

        self.update_tuple()

    def l2_move(self):
        self.l_move()
        self.l_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("L2")

        self.update_tuple()

    def l_prime_move(self):
        self.l_move()
        self.l_move()
        self.l_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("L'")

        self.update_tuple()

    def d_move(self):
        # bars
        tempF = self.fFace[6:9]
        tempR = self.rFace[6:9]
        tempB = self.bFace[6:9]
        tempL = self.lFace[6:9]

        self.rFace[6:9] = tempF
        self.bFace[6:9] = tempR
        self.lFace[6:9] = tempB
        self.fFace[6:9] = tempL

        # face
        self.rotate_face(self.dFace)

        self.moves_applied.append("D")

        self.update_tuple()

    def d2_move(self):
        self.d_move()
        self.d_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("D2")

        self.update_tuple()

    def d_prime_move(self):
        self.d_move()
        self.d_move()
        self.d_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("D'")

        self.update_tuple()

    # takes a cube and returns valid adjacent states
    def create_adj_list(self):

        adj_list = []

        if len(self.moves_applied) != 0:
            simplified_last_move = simplify_move(self.moves_applied[-1])
        else:
            simplified_last_move = ""

        if "R" in self.allowed_moves_for_chain and "R" != simplified_last_move:
            cube_r = deepcopy(self)
            cube_r.r_move()
            cube_r2 = deepcopy(self)
            cube_r2.r2_move()
            cube_r_prime = deepcopy(self)
            cube_r_prime.r_prime_move()
            adj_list.extend([cube_r, cube_r2, cube_r_prime])

        if "U" in self.allowed_moves_for_chain and "U" != simplified_last_move:
            cube_u = deepcopy(self)
            cube_u.u_move()
            cube_u2 = deepcopy(self)
            cube_u2.u2_move()
            cube_u_prime = deepcopy(self)
            cube_u_prime.u_prime_move()
            adj_list.extend([cube_u, cube_u2, cube_u_prime])

        if "F" in self.allowed_moves_for_chain and "F" != simplified_last_move:
            cube_f = deepcopy(self)
            cube_f.f_prime_move()
            cube_f2 = deepcopy(self)
            cube_f2.f2_move()
            cube_f_prime = deepcopy(self)
            cube_f_prime.f_prime_move()
            adj_list.extend([cube_f, cube_f2, cube_f_prime])

        if "B" in self.allowed_moves_for_chain and "B" != simplified_last_move:
            cube_b = deepcopy(self)
            cube_b.b_move()
            cube_b2 = deepcopy(self)
            cube_b2.b2_move()
            cube_b_prime = deepcopy(self)
            cube_b_prime.b_prime_move()
            adj_list.extend([cube_b, cube_b2, cube_b_prime])

        if "L" in self.allowed_moves_for_chain and "L" != simplified_last_move:
            cube_l = deepcopy(self)
            cube_l.l_move()
            cube_l2 = deepcopy(self)
            cube_l2.l2_move()
            cube_l_prime = deepcopy(self)
            cube_l_prime.l_prime_move()
            adj_list.extend([cube_l, cube_l2, cube_l_prime])

        if "D" in self.allowed_moves_for_chain and "D" != simplified_last_move:
            cube_d = deepcopy(self)
            cube_d.d_move()
            cube_d2 = deepcopy(self)
            cube_d2.d2_move()
            cube_d_prime = deepcopy(self)
            cube_d_prime.d_prime_move()
            adj_list.extend([cube_d, cube_d2, cube_d_prime])

        return adj_list
