from cube import Cube
from visualizer import *
from alg_handler import *


cube = Cube()
apply_alg(["R", "M'", 'U', "R'", "U'", "M", "U", "R", "U'", "R'"], cube)
cube_to_visual(cube)

#R M' U R' U' M U R U' R'


