import visualizer  # for testing
from cube import Cube
from visualizer import *
import alg_handler
from bfs_system import BfsSystem
from queue import Queue

# creating cubes
solved_cube = Cube()
input_algorithm = input("What's your scramble?").split(" ")
scrambled_cube = Cube()
alg_handler.apply_alg(input_algorithm, scrambled_cube)
scrambled_cube.moves_applied = []
allowed_moves = input("What move types are allowed?").split(" ")
scrambled_cube.allowed_moves_for_chain = allowed_moves
solved_cube.allowed_moves_for_chain = allowed_moves


print(f"Here are your cubes:")
cube_to_visual(solved_cube)
print("Solved Cube")
print_line()
cube_to_visual(scrambled_cube)
print("Scrambled Cube")
print_line()
print_line()
print_line()

solved_hash = {}
scrambled_hash = {}

solved_queue = Queue()
scrambled_queue = Queue()

solved_queue.put(solved_cube)
scrambled_queue.put(scrambled_cube)

counter = 0
merges = []

for x in range(3000):
    print(x)
    got_cube = solved_queue.get()  # get cube in queue

    adj_list = got_cube.create_adj_list()  # R R2 R' U U2 U'

    for cube in adj_list:
        cube.parent_cube = got_cube
        cube.depth = got_cube.depth + 1
        cube.allowed_moves_for_chain = cube.parent_cube.allowed_moves_for_chain

        print(f"Started from solved cube")
        cube_to_visual(cube)
        counter += 1
        print(f"Count: {counter}")
        print_depth(cube)
        print_moves(cube)

        if cube.tuple not in solved_hash:
            print("This cube state hasn't been reached from the solved end before, hashing now...")
            solved_hash[cube.tuple] = [cube.moves_applied]

        elif cube.tuple in solved_hash:
            print(
                "This cube state has already been reached from the solved end before, adding another moveset to hash now...")
            solved_hash[cube.tuple].append(cube.moves_applied)

        if cube.tuple in scrambled_hash:
            print("This cube state has been reached from the scrambled end before! Intersection found.")
            print("Here are the ways we reached this state from the scrambled end:")

            for solution in scrambled_hash[cube.tuple]:
                good_solution = alg_handler.reverse_and_invert_move_list(alg_handler.clean_up_intersection(cube.moves_applied,
                                                                                               alg_handler.reverse_and_invert_move_list(
                                                                                                   solution)))
                print(solution)  # the ways we can reach this state from the scrambled end
                if good_solution not in merges:
                    merges.append(good_solution)

        print_line()
        solved_queue.put(cube)

    ####################
    scrambled_got_cube = scrambled_queue.get()  # get cube in queue
    scrambled_adj_list = scrambled_got_cube.create_adj_list()  # R R2 R' U U2 U'

    for scramble_count_cube in scrambled_adj_list:
        scramble_count_cube.parent_cube = scrambled_got_cube
        scramble_count_cube.depth = scrambled_got_cube.depth + 1
        scramble_count_cube.allowed_moves_for_chain = scramble_count_cube.parent_cube.allowed_moves_for_chain

        print(f"Started from solved cube")
        cube_to_visual(scramble_count_cube)
        counter += 1
        print(f"Count: {counter}")
        print_depth(scramble_count_cube)
        print_moves(scramble_count_cube)

        if scramble_count_cube.tuple not in scrambled_hash:
            print("This cube state hasn't been reached from the solved end before, hashing now...")
            scrambled_hash[scramble_count_cube.tuple] = [scramble_count_cube.moves_applied]

        elif scramble_count_cube.tuple in scrambled_hash:
            print("This cube state has already been reached from the solved end before, adding another moveset "
                  "to hash now...")
            scrambled_hash[scramble_count_cube.tuple].append(scramble_count_cube.moves_applied)

        if scramble_count_cube.tuple in solved_hash:
            print("This cube state has been reached from the scrambled end before! Intersection found.")
            print("Here are the ways we reached this state from the scrambled end:")

            for solution in solved_hash[scramble_count_cube.tuple]:
                good_solution = alg_handler.clean_up_intersection(scramble_count_cube.moves_applied,
                                                      alg_handler.reverse_and_invert_move_list(solution))
                print(solution)  # the ways we can reach this state from the scrambled end
                if good_solution not in merges:
                    merges.append(good_solution)

        print_line()
        scrambled_queue.put(scramble_count_cube)

# for cube_tuple in solved_hash:
#     print(solved_hash[cube_tuple])

merges_to_string(merges)
