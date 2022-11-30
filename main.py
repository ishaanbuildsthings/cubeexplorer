# imports
from cube import Cube
from visualizer import *
from alg_handler import *
from queue import Queue
import math

# generates all possible solutions for a scramble, subject to the given
# move_types and max_depth.
# scramble and move_types must be delimited by ","
def solve(scramble, move_types, max_depth, id, txn_ids, solns):
    input_algorithm = scramble.split(",")
    allowed_moves = move_types.split(",")
    max_depth_allowed = int(max_depth)
    converted_max_depth_allowed = int(math.ceil((float(max_depth_allowed) / 2)))

    # create solved cube
    solved_cube = Cube()
    solved_cube.allowed_moves_for_chain = allowed_moves

    # create scrambled cube
    scrambled_cube = Cube()
    alg_handler.apply_alg(input_algorithm, scrambled_cube)
    scrambled_cube.moves_applied = []
    scrambled_cube.allowed_moves_for_chain = allowed_moves

    # setup for search algorithm
    solved_hash = {}
    solved_queue = Queue()
    solved_queue.put(solved_cube)

    scrambled_hash = {}
    scrambled_queue = Queue()
    scrambled_queue.put(scrambled_cube)

    num_cubes = 0
    depth_next_queued = 0
    final_solutions = set()

    # pruning
    odd_status = bool(max_depth_allowed % 2)

    # search algorithm
    while depth_next_queued < converted_max_depth_allowed:

        # take a cube from queue and make adjacency list
        got_cube = solved_queue.get()
        adj_list = got_cube.create_adj_list()

        for cube in adj_list:
            num_cubes += 1
            # set properties of adjacent cube
            cube.parent_cube = got_cube
            cube.depth = got_cube.depth + 1
            cube.allowed_moves_for_chain = cube.parent_cube.allowed_moves_for_chain

            # handles if the cube state has/hasn't been reached from the solved (same) end
            if cube.update_tuple() not in solved_hash:
                solved_hash[cube.update_tuple()] = [cube.moves_applied]
            else:
                solved_hash[cube.update_tuple()].append(cube.moves_applied)

            # handles if the cube state has been reached from the scrambled end
            if cube.update_tuple() in scrambled_hash:

                for scrambled_halfway in scrambled_hash[cube.update_tuple()]:
                    stage_1 = reverse_and_invert_move_list(scrambled_halfway)
                    stage_2 = clean_up_intersection(cube.moves_applied, stage_1)
                    stage_3 = reverse_and_invert_move_list(stage_2)
                    stage_3_s = ' '.join(stage_3)

                    if stage_3_s not in final_solutions:
                        final_solutions.add(stage_3_s)
                        solns.append(stage_3_s)

            # misc
            solved_queue.put(cube)

        # for while condition
        depth_next_queued = solved_queue.queue[0].depth

        # ____________________________________ SCRAMBLED SIDE ____________________________________ #

        scrambled_got_cube = scrambled_queue.get()

        # pruning
        if odd_status and (scrambled_got_cube.depth == converted_max_depth_allowed - 1):
            continue

        scrambled_adj_list = scrambled_got_cube.create_adj_list()

        for scramble_cube in scrambled_adj_list:
            num_cubes += 1
            # set properties of adjacent cube
            scramble_cube.parent_cube = scrambled_got_cube
            scramble_cube.depth = scrambled_got_cube.depth + 1
            scramble_cube.allowed_moves_for_chain = scramble_cube.parent_cube.allowed_moves_for_chain

            # handles if the cube state has/hasn't been reached from the scrambled (same) end
            if scramble_cube.update_tuple() not in scrambled_hash:
                scrambled_hash[scramble_cube.update_tuple()] = [scramble_cube.moves_applied]

            else:
                scrambled_hash[scramble_cube.update_tuple()].append(scramble_cube.moves_applied)

            # handles if the cube state has been reached from the solved end
            if scramble_cube.update_tuple() in solved_hash:
                for solved_halfway in solved_hash[scramble_cube.update_tuple()]:
                    stage_1 = reverse_and_invert_move_list(solved_halfway)
                    stage_2 = clean_up_intersection(scramble_cube.moves_applied, stage_1)

                    stage_2_s = ' '.join(stage_2)
                    if stage_2_s not in final_solutions:
                        final_solutions.add(stage_2_s)
                        solns.append(stage_2_s)

            # misc
            scrambled_queue.put(scramble_cube)

    # remove txn id from set
    solns.append('DONE')
    txn_ids.remove(id)

