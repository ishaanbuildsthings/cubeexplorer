from flask import Flask, request
from flask_cors import CORS
from main import solve
from collections import defaultdict
from threading import Thread
import json
import uuid

app = Flask(__name__)
CORS(app)

txn_ids = set()
id_to_solns = defaultdict(list)

# Given a scramble, max_depth, and move_types, handle_solve() spawns a thread
# that computes the solve. Returns a txn_id that is used to fetch the results
@app.route("/solve", methods=["GET"])
def handle_solve():
    scramble = request.args.get("scramble")
    max_depth = request.args.get("max-depth")
    move_types = request.args.get("move-types")
    if scramble == None or max_depth == None or move_types == None:
        return "Please provide scramble, max_depth, and move_types", 400
    
    id = str(uuid.uuid4())
    while id in txn_ids:
        id = str(uuid.uuid4())
    txn_ids.add(id)

    soln_list = []
    id_to_solns[id] = soln_list
    t = Thread(target=solve, args=(scramble, move_types, max_depth, id, txn_ids, soln_list,))
    t.start()

    return json.dumps(id)

# Given a txn-id, returns the current generated solutions
@app.route("/solve-update", methods=["GET"])
def solve_update():
    txn_id = request.args.get("txn-id")
    if txn_id == None:
        return json.dumps([])

    cur_solns = id_to_solns[txn_id][:]
    # TODO: watch out for the edge case where a user starts a requests but never finishes it
    #       id_to_solns will have a stale entry
    id_to_solns[txn_id].clear()
    return json.dumps(cur_solns)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)