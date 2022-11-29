import alg_handler
import copy


# takes a cube as the input and prints a 2d representation in the console
def cube_to_visual(cube):
    tuple = cube.update_tuple()
    print(f"        {tuple[0][0]}{tuple[0][1]}{tuple[0][2]}")
    print(f"        {tuple[0][3]}{tuple[0][4]}{tuple[0][5]}")
    print(f"        {tuple[0][6]}{tuple[0][7]}{tuple[0][8]}")

    print(
        f"{tuple[4][0]}{tuple[4][1]}{tuple[4][2]} {tuple[1][0]}{tuple[1][1]}{tuple[1][2]} {tuple[2][0]}{tuple[2][1]}{tuple[2][2]} {tuple[3][0]}{tuple[3][1]}{tuple[3][2]}")
    print(
        f"{tuple[4][3]}{tuple[4][4]}{tuple[4][5]} {tuple[1][3]}{tuple[1][4]}{tuple[1][5]} {tuple[2][3]}{tuple[2][4]}{tuple[2][5]} {tuple[3][3]}{tuple[3][4]}{tuple[3][5]}")
    print(
        f"{tuple[4][6]}{tuple[4][7]}{tuple[4][8]} {tuple[1][6]}{tuple[1][7]}{tuple[1][8]} {tuple[2][6]}{tuple[2][7]}{tuple[2][8]} {tuple[3][6]}{tuple[3][7]}{tuple[3][8]}")

    print(f"        {tuple[5][0]}{tuple[5][1]}{tuple[5][2]}")
    print(f"        {tuple[5][3]}{tuple[5][4]}{tuple[5][5]}")
    print(f"        {tuple[5][6]}{tuple[5][7]}{tuple[5][8]}")


# prints n line(s) for spacing purposes
def print_line(n=1):
    for x in range(n):
        print("__________________________________")


# prints the depth of moves applied to a given cube from the initial state
def print_depth(cube):
    print(f"Depth: {cube.depth}")


# prints the moves applied to a given cube relative to the initial state
def print_moves(cube):
    print(" ".join(cube.moves_applied))


# prints if a cube state already exists in a given hashtype, usually the opposite type in the
# bidirectional search, which is either solved or scrambled
def exists_in_hash(hashtype):
    print(f"This state already exists in the {hashtype} hash, solution found!")


# takes a list containing list solutions and prints each one
def solutions_to_string(solutions_list):
    for solution in solutions_list:
        print(" ".join(solution))
