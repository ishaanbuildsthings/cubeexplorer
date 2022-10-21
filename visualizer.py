import alg_handler
import copy


def cube_to_visual(cube):
    tuple = cube.tuple
    print(f"        {tuple[0][0]}{tuple[0][1]}{tuple[0][2]}")
    print(f"        {tuple[0][3]}{tuple[0][4]}{tuple[0][5]}")
    print(f"        {tuple[0][6]}{tuple[0][7]}{tuple[0][8]}")

    print(
        f"{tuple[4][0]}{tuple[4][1]}{tuple[4][2]} {tuple[1][0]}{tuple[1][1]}{tuple[1][2]} {tuple[2][0]}{tuple[2][1]}{tuple[2][2]}")
    print(
        f"{tuple[4][3]}{tuple[4][4]}{tuple[4][5]} {tuple[1][3]}{tuple[1][4]}{tuple[1][5]} {tuple[2][3]}{tuple[2][4]}{tuple[2][5]}")
    print(
        f"{tuple[4][6]}{tuple[4][7]}{tuple[4][8]} {tuple[1][6]}{tuple[1][7]}{tuple[1][8]} {tuple[2][6]}{tuple[2][7]}{tuple[2][8]}")

    print(f"        {tuple[5][0]}{tuple[5][1]}{tuple[5][2]}")
    print(f"        {tuple[5][3]}{tuple[5][4]}{tuple[5][5]}")
    print(f"        {tuple[5][6]}{tuple[5][7]}{tuple[5][8]}")


def print_line():
    print("__________________________________")


def print_depth(cube):
    print(f"Depth: {cube.depth}")


def print_moves(cube):
    print(" ".join(cube.moves_applied))


def exists_in_hash(hashtype):
    print(f"This state already exists in the {hashtype} hash, solution found!")


def print_solution(bfs_system, cube, cube_state, opposite_state):
    print(f"These moves should bring us to the current state from the {cube_state} cube: "
          f"{cube.moves_applied}")

    print(f"These moves are how we reached the state from the {opposite_state} cube:"
          f"{bfs_system.hash[cube.get_tuple()]}")

    if cube_state == "scrambled":
        list_to_be_conversed = copy.deepcopy(bfs_system.hash[cube.get_tuple()])
        list_to_be_conversed = alg_handler.reverse_and_invert_move_list(list_to_be_conversed)
        final_solution = alg_handler.clean_up_intersection(cube.moves_applied, list_to_be_conversed)
    elif cube_state == "solved":
        list_to_be_conversed = copy.deepcopy(cube.moves_applied)
        list_to_be_conversed = alg_handler.reverse_and_invert_move_list(list_to_be_conversed)
        final_solution = alg_handler.clean_up_intersection(bfs_system.hash[cube.get_tuple()], list_to_be_conversed)
    else:
        return print("Error, invalid cube state")

    print(f"The final solution is {final_solution}")

    return final_solution


def merges_to_string(merge):
    for solution in merge:
        print(" ".join(solution))
