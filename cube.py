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

        self.u_face = SOLVED_STICKER_STATE[0:9]
        self.f_face = SOLVED_STICKER_STATE[9:18]
        self.r_face = SOLVED_STICKER_STATE[18:27]
        self.b_face = SOLVED_STICKER_STATE[27:36]
        self.l_face = SOLVED_STICKER_STATE[36:45]
        self.d_face = SOLVED_STICKER_STATE[45:54]
        self.tuple = ()  # initialized to nothing as only update_tuple will be used

    # exists for hashing, not to be used otherwise
    def update_tuple(self):
        self.tuple = (tuple(self.u_face), tuple(self.f_face), tuple(self.r_face),
                      tuple(self.b_face), tuple(self.l_face), tuple(self.d_face))
        return self.tuple

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
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        self.l_face[0:3] = temp_f
        self.b_face[0:3] = temp_l
        self.r_face[0:3] = temp_b
        self.f_face[0:3] = temp_r

        # face
        self.rotate_face(self.u_face)

        self.moves_applied.append("U")

    def u2_move(self):
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]

        self.l_face[0:3] = temp_r
        self.b_face[0:3] = temp_f
        self.r_face[0:3] = temp_l
        self.f_face[0:3] = temp_b

        self.rotate_face(self.u_face)
        self.rotate_face(self.u_face)

        self.moves_applied.append("U2")

    def u_prime_move(self):
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]

        self.l_face[0:3] = temp_b
        self.b_face[0:3] = temp_r
        self.r_face[0:3] = temp_f
        self.f_face[0:3] = temp_l

        self.rotate_face(self.u_face)
        self.rotate_face(self.u_face)
        self.rotate_face(self.u_face)

        self.moves_applied.append("U'")

    def f_move(self):

        # bars
        temp_u = self.u_face[8:5:-1]
        temp_r = self.r_face[6] + self.r_face[3] + self.r_face[0]
        temp_d = self.d_face[0:3]
        temp_l = self.l_face[2] + self.l_face[5] + self.l_face[8]

        self.u_face[8:5:-1] = temp_l
        self.d_face[0:3] = temp_r

        self.r_face[6] = temp_u[0]
        self.r_face[3] = temp_u[1]
        self.r_face[0] = temp_u[2]

        self.l_face[2] = temp_d[0]
        self.l_face[5] = temp_d[1]
        self.l_face[8] = temp_d[2]

        # face
        self.rotate_face(self.f_face)

        self.moves_applied.append("F")

    def f2_move(self):
        self.f_move()
        self.f_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("F2")

    def f_prime_move(self):
        self.f_move()
        self.f_move()
        self.f_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("F'")

    def r_move(self):

        # bars
        temp_u = self.u_face[2] + self.u_face[5] + self.u_face[8]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[2] + self.d_face[5] + self.d_face[8]
        temp_f = self.f_face[2] + self.f_face[5] + self.f_face[8]

        self.b_face[0] = temp_u[2]
        self.b_face[3] = temp_u[1]
        self.b_face[6] = temp_u[0]

        self.d_face[2] = temp_b[2]
        self.d_face[5] = temp_b[1]
        self.d_face[8] = temp_b[0]

        self.f_face[2] = temp_d[0]
        self.f_face[5] = temp_d[1]
        self.f_face[8] = temp_d[2]

        self.u_face[2] = temp_f[0]
        self.u_face[5] = temp_f[1]
        self.u_face[8] = temp_f[2]

        # face
        self.rotate_face(self.r_face)

        self.moves_applied.append("R")

    def r2_move(self):
        temp_u = self.u_face[8] + self.u_face[5] + self.u_face[2]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[8] + self.d_face[5] + self.d_face[2]
        temp_f = self.f_face[8] + self.f_face[5] + self.f_face[2]

        self.u_face[8] = temp_d[0]
        self.u_face[5] = temp_d[1]
        self.u_face[2] = temp_d[2]

        self.b_face[0] = temp_f[0]
        self.b_face[3] = temp_f[1]
        self.b_face[6] = temp_f[2]

        self.d_face[8] = temp_u[0]
        self.d_face[5] = temp_u[1]
        self.d_face[2] = temp_u[2]

        self.f_face[8] = temp_b[0]
        self.f_face[5] = temp_b[1]
        self.f_face[2] = temp_b[2]

        self.rotate_face(self.r_face)
        self.rotate_face(self.r_face)

        self.moves_applied.append("R2")

    def r_prime_move(self):
        self.r_move()
        self.r_move()
        self.r_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("R'")

    def b_move(self):

        # bars
        temp_u = self.u_face[2::-1]
        temp_l = self.l_face[0] + self.l_face[3] + self.l_face[6]
        temp_d = self.d_face[6:9]
        temp_r = self.r_face[8] + self.r_face[5] + self.r_face[2]

        self.u_face[2::-1] = temp_r
        self.l_face[0] = temp_u[0]
        self.l_face[3] = temp_u[1]
        self.l_face[6] = temp_u[2]

        self.d_face[6:9] = temp_l

        self.r_face[8] = temp_d[0]
        self.r_face[5] = temp_d[1]
        self.r_face[2] = temp_d[2]

        # face
        self.rotate_face(self.b_face)

        self.moves_applied.append("B")

    def b2_move(self):
        self.b_move()
        self.b_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("B2")

    def b_prime_move(self):
        self.b_move()
        self.b_move()
        self.b_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("B'")

    def l_move(self):
        # bars
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]

        self.u_face[0] = temp_b[0]
        self.u_face[3] = temp_b[1]
        self.u_face[6] = temp_b[2]

        self.f_face[0] = temp_u[0]
        self.f_face[3] = temp_u[1]
        self.f_face[6] = temp_u[2]

        self.d_face[0] = temp_f[0]
        self.d_face[3] = temp_f[1]
        self.d_face[6] = temp_f[2]

        self.b_face[8] = temp_d[0]
        self.b_face[5] = temp_d[1]
        self.b_face[2] = temp_d[2]

        # face
        self.rotate_face(self.l_face)

        self.moves_applied.append("L")

    def l2_move(self):
        self.l_move()
        self.l_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("L2")

    def l_prime_move(self):
        self.l_move()
        self.l_move()
        self.l_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("L'")

    def d_move(self):
        # bars
        temp_f = self.f_face[6:9]
        temp_r = self.r_face[6:9]
        temp_b = self.b_face[6:9]
        temp_l = self.l_face[6:9]

        self.r_face[6:9] = temp_f
        self.b_face[6:9] = temp_r
        self.l_face[6:9] = temp_b
        self.f_face[6:9] = temp_l

        # face
        self.rotate_face(self.d_face)

        self.moves_applied.append("D")

    def d2_move(self):
        self.d_move()
        self.d_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("D2")

    def d_prime_move(self):
        self.d_move()
        self.d_move()
        self.d_move()

        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.pop()
        self.moves_applied.append("D'")

    # takes a cube and returns a list of cubes with valid adjacent states
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
