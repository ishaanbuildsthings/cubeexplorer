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


def rotate_face_ccw(face):
    # store temps
    temp0, temp1, temp2, temp3, temp5, temp6, temp7, temp8 = \
        face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8]
    # reassign
    face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8] = \
        temp2, temp5, temp8, temp1, temp7, temp0, temp3, temp6


def rotate_face_cw(face):
    # store temps
    temp0, temp1, temp2, temp3, temp5, temp6, temp7, temp8 = \
        face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8]
    # reassign
    face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8] = \
        temp6, temp3, temp0, temp7, temp1, temp8, temp5, temp2


def rotate_face_180(face):
    # store temps
    temp0, temp1, temp2, temp3, temp5, temp6, temp7, temp8 = \
        face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8]
    # reassign
    face[0], face[1], face[2], face[3], face[5], face[6], face[7], face[8] = \
        temp8, temp7, temp6, temp5, temp3, temp2, temp1, temp0


class Cube:
    def __init__(self):
        self.moves_applied = []
        self.parent_cube = None
        self.depth = 0
        self.allowed_moves_for_chain = []

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

    def u_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_f
        self.b_face[0:3] = temp_l
        self.r_face[0:3] = temp_b
        self.f_face[0:3] = temp_r
        # misc
        rotate_face_cw(self.u_face)
        self.moves_applied.append("U")

    def u2_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_r
        self.b_face[0:3] = temp_f
        self.r_face[0:3] = temp_l
        self.f_face[0:3] = temp_b
        # misc
        rotate_face_180(self.u_face)
        self.moves_applied.append("U2")

    def u_prime_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_b
        self.b_face[0:3] = temp_r
        self.r_face[0:3] = temp_f
        self.f_face[0:3] = temp_l
        # misc
        rotate_face_ccw(self.u_face)
        self.moves_applied.append("U'")

    def f_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:] = temp_l
        self.r_face[0] = temp_u[0]
        self.r_face[3] = temp_u[1]
        self.r_face[6] = temp_u[2]
        self.d_face[2::-1] = temp_r
        self.l_face[8] = temp_d[0]
        self.l_face[5] = temp_d[1]
        self.l_face[2] = temp_d[2]
        # misc
        rotate_face_cw(self.f_face)
        self.moves_applied.append("F")

    def f2_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:0] = temp_d
        self.r_face[0] = temp_l[0]
        self.r_face[3] = temp_l[1]
        self.r_face[6] = temp_l[2]
        self.d_face[2:-1:-1] = temp_u
        self.l_face[8] = temp_r[0]
        self.l_face[5] = temp_r[1]
        self.l_face[2] = temp_r[2]
        # misc
        rotate_face_180(self.f_face)
        self.moves_applied.append("F2")

    def f_prime_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:] = temp_r[0:3]
        self.r_face[0] = temp_d[0]
        self.r_face[3] = temp_d[1]
        self.r_face[6] = temp_d[2]
        self.d_face[2::-1] = temp_l[0:3]
        self.l_face[2] = temp_u[2]
        self.l_face[5] = temp_u[1]
        self.l_face[8] = temp_u[0]
        # misc
        rotate_face_ccw(self.f_face)
        self.moves_applied.append("F'")

    def r_move(self):
        # temps
        temp_u = self.u_face[2] + self.u_face[5] + self.u_face[8]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[2] + self.d_face[5] + self.d_face[8]
        temp_f = self.f_face[2] + self.f_face[5] + self.f_face[8]
        # assign bars
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
        # misc
        rotate_face_cw(self.r_face)
        self.moves_applied.append("R")

    def r2_move(self):
        # temps
        temp_u = self.u_face[8] + self.u_face[5] + self.u_face[2]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[8] + self.d_face[5] + self.d_face[2]
        temp_f = self.f_face[8] + self.f_face[5] + self.f_face[2]
        # assign bars
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
        # misc
        rotate_face_180(self.r_face)
        self.moves_applied.append("R2")

    def r_prime_move(self):
        # temps
        temp_u = self.u_face[2] + self.u_face[5] + self.u_face[8]
        temp_b = self.b_face[6] + self.b_face[3] + self.b_face[0]
        temp_d = self.d_face[2] + self.d_face[5] + self.d_face[8]
        temp_f = self.f_face[2] + self.f_face[5] + self.f_face[8]
        # assign bars
        self.u_face[2] = temp_b[0]
        self.u_face[5] = temp_b[1]
        self.u_face[8] = temp_b[2]
        self.f_face[2] = temp_u[0]
        self.f_face[5] = temp_u[1]
        self.f_face[8] = temp_u[2]
        self.d_face[2] = temp_f[0]
        self.d_face[5] = temp_f[1]
        self.d_face[8] = temp_f[2]
        self.b_face[6] = temp_d[0]
        self.b_face[3] = temp_d[1]
        self.b_face[0] = temp_d[2]
        # misc
        rotate_face_ccw(self.r_face)
        self.moves_applied.append("R'")

    def b_move(self):
        # temps
        temp_u = self.u_face[2::-1]
        temp_l = self.l_face[0] + self.l_face[3] + self.l_face[6]
        temp_d = self.d_face[6:]
        temp_r = self.r_face[8] + self.r_face[5] + self.r_face[2]
        # assign bars
        self.u_face[2::-1] = temp_r
        self.l_face[0] = temp_u[0]
        self.l_face[3] = temp_u[1]
        self.l_face[6] = temp_u[2]
        self.d_face[6:] = temp_l
        self.r_face[8] = temp_d[0]
        self.r_face[5] = temp_d[1]
        self.r_face[2] = temp_d[2]
        # misc
        rotate_face_cw(self.b_face)
        self.moves_applied.append("B")

    def b2_move(self):
        # temps
        temp_u = self.u_face[2::-1]
        temp_l = self.l_face[0] + self.l_face[3] + self.l_face[6]
        temp_d = self.d_face[6:]
        temp_r = self.r_face[8] + self.r_face[5] + self.r_face[2]
        # assign bars
        self.u_face[2::-1] = temp_d
        self.r_face[8] = temp_l[0]
        self.r_face[5] = temp_l[1]
        self.r_face[2] = temp_l[2]
        self.d_face[6:] = temp_u
        self.l_face[0] = temp_r[0]
        self.l_face[3] = temp_r[1]
        self.l_face[6] = temp_r[2]
        # misc
        rotate_face_180(self.b_face)
        self.moves_applied.append("B2")

    def b_prime_move(self):
        # temps
        temp_u = self.u_face[0:3]
        temp_l = self.l_face[6] + self.l_face[3] + self.l_face[0]
        temp_d = self.d_face[-1:5:-1]
        temp_r = self.r_face[2] + self.r_face[5] + self.r_face[8]
        # assign bars
        self.u_face[0:3] = temp_l
        self.r_face[2] = temp_u[0]
        self.r_face[5] = temp_u[1]
        self.r_face[8] = temp_u[2]
        self.d_face[-1:5:-1] = temp_r
        self.l_face[6] = temp_d[0]
        self.l_face[3] = temp_d[1]
        self.l_face[0] = temp_d[2]
        # misc
        rotate_face_ccw(self.b_face)
        self.moves_applied.append("B'")

    def l_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
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
        # misc
        rotate_face_cw(self.l_face)
        self.moves_applied.append("L")

    def l2_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
        self.u_face[0] = temp_d[0]
        self.u_face[3] = temp_d[1]
        self.u_face[6] = temp_d[2]
        self.f_face[0] = temp_b[0]
        self.f_face[3] = temp_b[1]
        self.f_face[6] = temp_b[2]
        self.d_face[0] = temp_u[0]
        self.d_face[3] = temp_u[1]
        self.d_face[6] = temp_u[2]
        self.b_face[8] = temp_f[0]
        self.b_face[5] = temp_f[1]
        self.b_face[2] = temp_f[2]
        # misc
        rotate_face_180(self.l_face)
        self.moves_applied.append("L2")

    def l_prime_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
        self.u_face[0] = temp_f[0]
        self.u_face[3] = temp_f[1]
        self.u_face[6] = temp_f[2]
        self.b_face[2] = temp_u[2]
        self.b_face[5] = temp_u[1]
        self.b_face[8] = temp_u[0]
        self.d_face[6] = temp_b[2]
        self.d_face[3] = temp_b[1]
        self.d_face[0] = temp_b[0]
        self.f_face[6] = temp_d[2]
        self.f_face[3] = temp_d[1]
        self.f_face[0] = temp_d[0]
        # misc
        rotate_face_ccw(self.l_face)
        self.moves_applied.append("L'")

    def d_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.r_face[6:] = temp_f
        self.b_face[6:] = temp_r
        self.l_face[6:] = temp_b
        self.f_face[6:] = temp_l
        # misc
        rotate_face_cw(self.d_face)
        self.moves_applied.append("D")

    def d2_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.f_face[6:] = temp_b
        self.r_face[6:] = temp_l
        self.b_face[6:] = temp_f
        self.l_face[6:] = temp_r
        # misc
        rotate_face_180(self.d_face)
        self.moves_applied.append("D2")

    def d_prime_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.f_face[6:] = temp_r
        self.l_face[6:] = temp_f
        self.b_face[6:] = temp_l
        self.r_face[6:] = temp_b
        # misc
        rotate_face_ccw(self.d_face)
        self.moves_applied.append("D'")

    def s_move(self):
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_l
        self.r_face[1] = temp_u[0]
        self.r_face[4] = temp_u[1]
        self.r_face[7] = temp_u[2]
        self.d_face[5:2:-1] = temp_r
        self.l_face[7] = temp_d[0]
        self.l_face[4] = temp_d[1]
        self.l_face[1] = temp_d[2]
        # moves applied
        self.moves_applied.append("S")

    def s_prime_move(self):
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_r
        self.r_face[1] = temp_d[0]
        self.r_face[4] = temp_d[1]
        self.r_face[7] = temp_d[2]
        self.d_face[5:2:-1] = temp_l
        self.l_face[1] = temp_u[2]
        self.l_face[4] = temp_u[1]
        self.l_face[7] = temp_u[0]
        # moves applied
        self.moves_applied.append("S'")

    def s2_move(self):
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_d
        self.r_face[1] = temp_l[0]
        self.r_face[4] = temp_l[1]
        self.r_face[7] = temp_l[2]
        self.d_face[5:2:-1] = temp_u
        self.l_face[7] = temp_r[0]
        self.l_face[4] = temp_r[1]
        self.l_face[1] = temp_r[2]
        # moves applied
        self.moves_applied.append("S2")
    
    def e_move(self):
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_l
        self.r_face[3:6] = temp_f
        self.b_face[3:6] = temp_r
        self.l_face[3:6] = temp_b
        # moves applied
        self.moves_applied.append("E")
        
    def e2_move(self):
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_b
        self.r_face[3:6] = temp_l
        self.b_face[3:6] = temp_f
        self.l_face[3:6] = temp_r
        # moves applied
        self.moves_applied.append("E2")
        
    def e_prime_move(self):
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_r
        self.r_face[3:6] = temp_b
        self.b_face[3:6] = temp_l
        self.l_face[3:6] = temp_f
        # moves applied
        self.moves_applied.append("E'")
        
    def m_move(self):
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_b[0]
        self.u_face[4] = temp_b[1]
        self.u_face[7] = temp_b[2]
        self.f_face[1] = temp_u[0]
        self.f_face[4] = temp_u[1]
        self.f_face[7] = temp_u[2]
        self.d_face[1] = temp_f[0]
        self.d_face[4] = temp_f[1]
        self.d_face[7] = temp_f[2]
        self.b_face[7] = temp_d[0]
        self.b_face[4] = temp_d[1]
        self.b_face[1] = temp_d[2]
        # moves applied
        self.moves_applied.append("M")

    def m_prime_move(self):
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_f[0]
        self.u_face[4] = temp_f[1]
        self.u_face[7] = temp_f[2]
        self.f_face[1] = temp_d[0]
        self.f_face[4] = temp_d[1]
        self.f_face[7] = temp_d[2]
        self.d_face[1] = temp_b[0]
        self.d_face[4] = temp_b[1]
        self.d_face[7] = temp_b[2]
        self.b_face[7] = temp_u[0]
        self.b_face[4] = temp_u[1]
        self.b_face[1] = temp_u[2]
        # moves applied
        self.moves_applied.append("M'")

    def m2_move(self):
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_d[0]
        self.u_face[4] = temp_d[1]
        self.u_face[7] = temp_d[2]
        self.f_face[1] = temp_b[0]
        self.f_face[4] = temp_b[1]
        self.f_face[7] = temp_b[2]
        self.d_face[1] = temp_u[0]
        self.d_face[4] = temp_u[1]
        self.d_face[7] = temp_u[2]
        self.b_face[7] = temp_f[0]
        self.b_face[4] = temp_f[1]
        self.b_face[1] = temp_f[2]
        # moves applied
        self.moves_applied.append("M2")

    def u_wide_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_f
        self.b_face[0:3] = temp_l
        self.r_face[0:3] = temp_b
        self.f_face[0:3] = temp_r
        # misc
        rotate_face_cw(self.u_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_r
        self.r_face[3:6] = temp_b
        self.b_face[3:6] = temp_l
        self.l_face[3:6] = temp_f
        # moves applied
        self.moves_applied.append("u")

    def u2_wide_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_r
        self.b_face[0:3] = temp_f
        self.r_face[0:3] = temp_l
        self.f_face[0:3] = temp_b
        # misc
        rotate_face_180(self.u_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_b
        self.r_face[3:6] = temp_l
        self.b_face[3:6] = temp_f
        self.l_face[3:6] = temp_r
        # moves applied
        self.moves_applied.append("u2")

    def u_prime_wide_move(self):
        # temps
        temp_f = self.f_face[0:3]
        temp_r = self.r_face[0:3]
        temp_b = self.b_face[0:3]
        temp_l = self.l_face[0:3]
        # assign bars
        self.l_face[0:3] = temp_b
        self.b_face[0:3] = temp_r
        self.r_face[0:3] = temp_f
        self.f_face[0:3] = temp_l
        # misc
        rotate_face_ccw(self.u_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_l
        self.r_face[3:6] = temp_f
        self.b_face[3:6] = temp_r
        self.l_face[3:6] = temp_b
        # moves applied
        self.moves_applied.append("u'")

    def d_wide_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.r_face[6:] = temp_f
        self.b_face[6:] = temp_r
        self.l_face[6:] = temp_b
        self.f_face[6:] = temp_l
        # misc
        rotate_face_cw(self.d_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_l
        self.r_face[3:6] = temp_f
        self.b_face[3:6] = temp_r
        self.l_face[3:6] = temp_b
        # moves applied
        self.moves_applied.append("d")

    def d2_wide_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.f_face[6:] = temp_b
        self.r_face[6:] = temp_l
        self.b_face[6:] = temp_f
        self.l_face[6:] = temp_r
        # misc
        rotate_face_180(self.d_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_b
        self.r_face[3:6] = temp_l
        self.b_face[3:6] = temp_f
        self.l_face[3:6] = temp_r
        # moves applied
        self.moves_applied.append("d2")

    def d_prime_wide_move(self):
        # temps
        temp_f = self.f_face[6:]
        temp_r = self.r_face[6:]
        temp_b = self.b_face[6:]
        temp_l = self.l_face[6:]
        # assign bars
        self.f_face[6:] = temp_r
        self.l_face[6:] = temp_f
        self.b_face[6:] = temp_l
        self.r_face[6:] = temp_b
        # misc
        rotate_face_ccw(self.d_face)
        # temps
        temp_f = self.f_face[3:6]
        temp_r = self.r_face[3:6]
        temp_b = self.b_face[3:6]
        temp_l = self.l_face[3:6]
        # assign strips
        self.f_face[3:6] = temp_r
        self.r_face[3:6] = temp_b
        self.b_face[3:6] = temp_l
        self.l_face[3:6] = temp_f
        # moves applied
        self.moves_applied.append("d'")



    def r_wide_move(self):
        # temps
        temp_u = self.u_face[2] + self.u_face[5] + self.u_face[8]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[2] + self.d_face[5] + self.d_face[8]
        temp_f = self.f_face[2] + self.f_face[5] + self.f_face[8]
        # assign bars
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
        # misc
        rotate_face_cw(self.r_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_f[0]
        self.u_face[4] = temp_f[1]
        self.u_face[7] = temp_f[2]
        self.f_face[1] = temp_d[0]
        self.f_face[4] = temp_d[1]
        self.f_face[7] = temp_d[2]
        self.d_face[1] = temp_b[0]
        self.d_face[4] = temp_b[1]
        self.d_face[7] = temp_b[2]
        self.b_face[7] = temp_u[0]
        self.b_face[4] = temp_u[1]
        self.b_face[1] = temp_u[2]
        self.moves_applied.append("r")

    def r_prime_wide_move(self):
        # temps
        temp_u = self.u_face[2] + self.u_face[5] + self.u_face[8]
        temp_b = self.b_face[6] + self.b_face[3] + self.b_face[0]
        temp_d = self.d_face[2] + self.d_face[5] + self.d_face[8]
        temp_f = self.f_face[2] + self.f_face[5] + self.f_face[8]
        # assign bars
        self.u_face[2] = temp_b[0]
        self.u_face[5] = temp_b[1]
        self.u_face[8] = temp_b[2]
        self.f_face[2] = temp_u[0]
        self.f_face[5] = temp_u[1]
        self.f_face[8] = temp_u[2]
        self.d_face[2] = temp_f[0]
        self.d_face[5] = temp_f[1]
        self.d_face[8] = temp_f[2]
        self.b_face[6] = temp_d[0]
        self.b_face[3] = temp_d[1]
        self.b_face[0] = temp_d[2]
        # misc
        rotate_face_ccw(self.r_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_b[0]
        self.u_face[4] = temp_b[1]
        self.u_face[7] = temp_b[2]
        self.f_face[1] = temp_u[0]
        self.f_face[4] = temp_u[1]
        self.f_face[7] = temp_u[2]
        self.d_face[1] = temp_f[0]
        self.d_face[4] = temp_f[1]
        self.d_face[7] = temp_f[2]
        self.b_face[7] = temp_d[0]
        self.b_face[4] = temp_d[1]
        self.b_face[1] = temp_d[2]
        # moves applied
        self.moves_applied.append("r2")

    def r2_wide_move(self):
        # temps
        temp_u = self.u_face[8] + self.u_face[5] + self.u_face[2]
        temp_b = self.b_face[0] + self.b_face[3] + self.b_face[6]
        temp_d = self.d_face[8] + self.d_face[5] + self.d_face[2]
        temp_f = self.f_face[8] + self.f_face[5] + self.f_face[2]
        # assign bars
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
        # misc
        rotate_face_180(self.r_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_d[0]
        self.u_face[4] = temp_d[1]
        self.u_face[7] = temp_d[2]
        self.f_face[1] = temp_b[0]
        self.f_face[4] = temp_b[1]
        self.f_face[7] = temp_b[2]
        self.d_face[1] = temp_u[0]
        self.d_face[4] = temp_u[1]
        self.d_face[7] = temp_u[2]
        self.b_face[7] = temp_f[0]
        self.b_face[4] = temp_f[1]
        self.b_face[1] = temp_f[2]
        self.moves_applied.append("r2")

    def l_wide_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
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
        # misc
        rotate_face_cw(self.l_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_b[0]
        self.u_face[4] = temp_b[1]
        self.u_face[7] = temp_b[2]
        self.f_face[1] = temp_u[0]
        self.f_face[4] = temp_u[1]
        self.f_face[7] = temp_u[2]
        self.d_face[1] = temp_f[0]
        self.d_face[4] = temp_f[1]
        self.d_face[7] = temp_f[2]
        self.b_face[7] = temp_d[0]
        self.b_face[4] = temp_d[1]
        self.b_face[1] = temp_d[2]
        self.moves_applied.append("l")

    def l_prime_wide_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
        self.u_face[0] = temp_f[0]
        self.u_face[3] = temp_f[1]
        self.u_face[6] = temp_f[2]
        self.b_face[2] = temp_u[2]
        self.b_face[5] = temp_u[1]
        self.b_face[8] = temp_u[0]
        self.d_face[6] = temp_b[2]
        self.d_face[3] = temp_b[1]
        self.d_face[0] = temp_b[0]
        self.f_face[6] = temp_d[2]
        self.f_face[3] = temp_d[1]
        self.f_face[0] = temp_d[0]
        # misc
        rotate_face_ccw(self.l_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_f[0]
        self.u_face[4] = temp_f[1]
        self.u_face[7] = temp_f[2]
        self.f_face[1] = temp_d[0]
        self.f_face[4] = temp_d[1]
        self.f_face[7] = temp_d[2]
        self.d_face[1] = temp_b[0]
        self.d_face[4] = temp_b[1]
        self.d_face[7] = temp_b[2]
        self.b_face[7] = temp_u[0]
        self.b_face[4] = temp_u[1]
        self.b_face[1] = temp_u[2]
        self.moves_applied.append("l'")

    def l2_wide_move(self):
        # temps
        temp_u = self.u_face[0] + self.u_face[3] + self.u_face[6]
        temp_f = self.f_face[0] + self.f_face[3] + self.f_face[6]
        temp_d = self.d_face[0] + self.d_face[3] + self.d_face[6]
        temp_b = self.b_face[8] + self.b_face[5] + self.b_face[2]
        # assign bars
        self.u_face[0] = temp_d[0]
        self.u_face[3] = temp_d[1]
        self.u_face[6] = temp_d[2]
        self.f_face[0] = temp_b[0]
        self.f_face[3] = temp_b[1]
        self.f_face[6] = temp_b[2]
        self.d_face[0] = temp_u[0]
        self.d_face[3] = temp_u[1]
        self.d_face[6] = temp_u[2]
        self.b_face[8] = temp_f[0]
        self.b_face[5] = temp_f[1]
        self.b_face[2] = temp_f[2]
        # misc
        rotate_face_180(self.l_face)
        # temps
        temp_u = self.u_face[1] + self.u_face[4] + self.u_face[7]
        temp_f = self.f_face[1] + self.f_face[4] + self.f_face[7]
        temp_d = self.d_face[1] + self.d_face[4] + self.d_face[7]
        temp_b = self.b_face[7] + self.b_face[4] + self.b_face[1]
        # assign strips
        self.u_face[1] = temp_d[0]
        self.u_face[4] = temp_d[1]
        self.u_face[7] = temp_d[2]
        self.f_face[1] = temp_b[0]
        self.f_face[4] = temp_b[1]
        self.f_face[7] = temp_b[2]
        self.d_face[1] = temp_u[0]
        self.d_face[4] = temp_u[1]
        self.d_face[7] = temp_u[2]
        self.b_face[7] = temp_f[0]
        self.b_face[4] = temp_f[1]
        self.b_face[1] = temp_f[2]
        self.moves_applied.append("l2")

    def f_wide_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:] = temp_l
        self.r_face[0] = temp_u[0]
        self.r_face[3] = temp_u[1]
        self.r_face[6] = temp_u[2]
        self.d_face[2::-1] = temp_r
        self.l_face[8] = temp_d[0]
        self.l_face[5] = temp_d[1]
        self.l_face[2] = temp_d[2]
        # misc
        rotate_face_cw(self.f_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_l
        self.r_face[1] = temp_u[0]
        self.r_face[4] = temp_u[1]
        self.r_face[7] = temp_u[2]
        self.d_face[5:2:-1] = temp_r
        self.l_face[7] = temp_d[0]
        self.l_face[4] = temp_d[1]
        self.l_face[1] = temp_d[2]
        # moves applied
        self.moves_applied.append("f")

    def f_prime_wide_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:] = temp_r[0:3]
        self.r_face[0] = temp_d[0]
        self.r_face[3] = temp_d[1]
        self.r_face[6] = temp_d[2]
        self.d_face[2::-1] = temp_l[0:3]
        self.l_face[2] = temp_u[2]
        self.l_face[5] = temp_u[1]
        self.l_face[8] = temp_u[0]
        # misc
        rotate_face_ccw(self.f_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_r
        self.r_face[1] = temp_d[0]
        self.r_face[4] = temp_d[1]
        self.r_face[7] = temp_d[2]
        self.d_face[5:2:-1] = temp_l
        self.l_face[1] = temp_u[2]
        self.l_face[4] = temp_u[1]
        self.l_face[7] = temp_u[0]
        # moves applied
        self.moves_applied.append("f'")

    def f2_wide_move(self):
        # temps
        temp_u = self.u_face[6:]
        temp_r = self.r_face[0] + self.r_face[3] + self.r_face[6]
        temp_d = self.d_face[2::-1]
        temp_l = self.l_face[8] + self.l_face[5] + self.l_face[2]
        # assign bars
        self.u_face[6:] = temp_d
        self.r_face[0] = temp_l[0]
        self.r_face[3] = temp_l[1]
        self.r_face[6] = temp_l[2]
        self.d_face[2::-1] = temp_u
        self.l_face[8] = temp_r[0]
        self.l_face[5] = temp_r[1]
        self.l_face[2] = temp_r[2]
        # misc
        rotate_face_180(self.f_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_d
        self.r_face[1] = temp_l[0]
        self.r_face[4] = temp_l[1]
        self.r_face[7] = temp_l[2]
        self.d_face[5:2:-1] = temp_u
        self.l_face[7] = temp_r[0]
        self.l_face[4] = temp_r[1]
        self.l_face[1] = temp_r[2]
        # moves applied
        self.moves_applied.append("f2")

    def b_wide_move(self):
        # temps
        temp_u = self.u_face[2::-1]
        temp_l = self.l_face[0] + self.l_face[3] + self.l_face[6]
        temp_d = self.d_face[6:]
        temp_r = self.r_face[8] + self.r_face[5] + self.r_face[2]
        # assign bars
        self.u_face[2::-1] = temp_r
        self.l_face[0] = temp_u[0]
        self.l_face[3] = temp_u[1]
        self.l_face[6] = temp_u[2]
        self.d_face[6:] = temp_l
        self.r_face[8] = temp_d[0]
        self.r_face[5] = temp_d[1]
        self.r_face[2] = temp_d[2]
        # misc
        rotate_face_cw(self.b_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_r
        self.r_face[1] = temp_d[0]
        self.r_face[4] = temp_d[1]
        self.r_face[7] = temp_d[2]
        self.d_face[5:2:-1] = temp_l
        self.l_face[1] = temp_u[2]
        self.l_face[4] = temp_u[1]
        self.l_face[7] = temp_u[0]
        # moves applied
        self.moves_applied.append("b")

    def b_prime_wide_move(self):
        # temps
        temp_u = self.u_face[0:3]
        temp_l = self.l_face[6] + self.l_face[3] + self.l_face[0]
        temp_d = self.d_face[-1:5:-1]
        temp_r = self.r_face[2] + self.r_face[5] + self.r_face[8]
        # assign bars
        self.u_face[0:3] = temp_l
        self.r_face[2] = temp_u[0]
        self.r_face[5] = temp_u[1]
        self.r_face[8] = temp_u[2]
        self.d_face[-1:5:-1] = temp_r
        self.l_face[6] = temp_d[0]
        self.l_face[3] = temp_d[1]
        self.l_face[0] = temp_d[2]
        # misc
        rotate_face_ccw(self.b_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_l
        self.r_face[1] = temp_u[0]
        self.r_face[4] = temp_u[1]
        self.r_face[7] = temp_u[2]
        self.d_face[5:2:-1] = temp_r
        self.l_face[7] = temp_d[0]
        self.l_face[4] = temp_d[1]
        self.l_face[1] = temp_d[2]
        # moves applied
        self.moves_applied.append("b'")

    def b2_wide_move(self):
        # temps
        temp_u = self.u_face[2::-1]
        temp_l = self.l_face[0] + self.l_face[3] + self.l_face[6]
        temp_d = self.d_face[6:]
        temp_r = self.r_face[8] + self.r_face[5] + self.r_face[2]
        # assign bars
        self.u_face[2::-1] = temp_d
        self.r_face[8] = temp_l[0]
        self.r_face[5] = temp_l[1]
        self.r_face[2] = temp_l[2]
        self.d_face[6:] = temp_u
        self.l_face[0] = temp_r[0]
        self.l_face[3] = temp_r[1]
        self.l_face[6] = temp_r[2]
        # misc
        rotate_face_180(self.b_face)
        # temps
        temp_u = self.u_face[3:6]
        temp_r = self.r_face[1] + self.r_face[4] + self.r_face[7]
        temp_d = self.d_face[5:2:-1]
        temp_l = self.l_face[7] + self.l_face[4] + self.l_face[1]
        # assign strips
        self.u_face[3:6] = temp_d
        self.r_face[1] = temp_l[0]
        self.r_face[4] = temp_l[1]
        self.r_face[7] = temp_l[2]
        self.d_face[5:2:-1] = temp_u
        self.l_face[7] = temp_r[0]
        self.l_face[4] = temp_r[1]
        self.l_face[1] = temp_r[2]
        # moves applied
        self.moves_applied.append("b2")

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
            cube_f.f_move()
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

        if "S" in self.allowed_moves_for_chain and "S" != simplified_last_move:
            cube_s = deepcopy(self)
            cube_s.s_move()
            cube_s2 = deepcopy(self)
            cube_s2.s2_move()
            cube_s_prime = deepcopy(self)
            cube_s_prime.s_prime_move()
            adj_list.extend([cube_s, cube_s2, cube_s_prime])

        if "M" in self.allowed_moves_for_chain and "M" != simplified_last_move:
            cube_m = deepcopy(self)
            cube_m.m_move()
            cube_m2 = deepcopy(self)
            cube_m2.m2_move()
            cube_m_prime = deepcopy(self)
            cube_m_prime.m_prime_move()
            adj_list.extend([cube_m, cube_m2, cube_m_prime])
            
        if "E" in self.allowed_moves_for_chain and "E" != simplified_last_move:
            cube_e = deepcopy(self)
            cube_e.e_move()
            cube_e2 = deepcopy(self)
            cube_e2.e2_move()
            cube_e_prime = deepcopy(self)
            cube_e_prime.e_prime_move()
            adj_list.extend([cube_e, cube_e2, cube_e_prime])

        if "u" in self.allowed_moves_for_chain and "u" != simplified_last_move:
            cube_u_wide = deepcopy(self)
            cube_u_wide.u_wide_move()
            cube_u2_wide = deepcopy(self)
            cube_u2_wide.u2_wide_move()
            cube_u_prime_wide = deepcopy(self)
            cube_u_prime_wide.u_prime_wide_move()
            adj_list.extend([cube_u_wide, cube_u2_wide, cube_u_prime_wide])

        if "d" in self.allowed_moves_for_chain and "d" != simplified_last_move:
            cube_d_wide = deepcopy(self)
            cube_d_wide.d_wide_move()
            cube_d2_wide = deepcopy(self)
            cube_d2_wide.d2_wide_move()
            cube_d_prime_wide = deepcopy(self)
            cube_d_prime_wide.d_prime_wide_move()
            adj_list.extend([cube_d_wide, cube_d2_wide, cube_d_prime_wide])
            
        if "f" in self.allowed_moves_for_chain and "f" != simplified_last_move:
            cube_f_wide = deepcopy(self)
            cube_f_wide.f_wide_move()
            cube_f2_wide = deepcopy(self)
            cube_f2_wide.f2_wide_move()
            cube_f_prime_wide = deepcopy(self)
            cube_f_prime_wide.f_prime_wide_move()
            adj_list.extend([cube_f_wide, cube_f2_wide, cube_f_prime_wide])
            
        if "b" in self.allowed_moves_for_chain and "b" != simplified_last_move:
            cube_b_wide = deepcopy(self)
            cube_b_wide.b_wide_move()
            cube_b2_wide = deepcopy(self)
            cube_b2_wide.b2_wide_move()
            cube_b_prime_wide = deepcopy(self)
            cube_b_prime_wide.b_prime_wide_move()
            adj_list.extend([cube_b_wide, cube_b2_wide, cube_b_prime_wide])
            
        if "r" in self.allowed_moves_for_chain and "r" != simplified_last_move:
            cube_r_wide = deepcopy(self)
            cube_r_wide.r_wide_move()
            cube_r2_wide = deepcopy(self)
            cube_r2_wide.r2_wide_move()
            cube_r_prime_wide = deepcopy(self)
            cube_r_prime_wide.r_prime_wide_move()
            adj_list.extend([cube_r_wide, cube_r2_wide, cube_r_prime_wide])
            
        if "l" in self.allowed_moves_for_chain and "l" != simplified_last_move:
            cube_l_wide = deepcopy(self)
            cube_l_wide.l_wide_move()
            cube_l2_wide = deepcopy(self)
            cube_l2_wide.l2_wide_move()
            cube_l_prime_wide = deepcopy(self)
            cube_l_prime_wide.l_prime_wide_move()
            adj_list.extend([cube_l_wide, cube_l2_wide, cube_l_prime_wide])

        return adj_list
