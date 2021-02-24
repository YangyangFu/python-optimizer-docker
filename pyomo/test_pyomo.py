# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

import shutil
import sys
import os.path

from pyomo.environ import *


"""def objfunc(x):
  
min  f = -x[0]*x[1]*x[2]
s.t.
  x[0] + 2.*x[1] + 2.*x[2] - 72.0 <= 0
  -x[0] - 2.*x[1] - 2.*x[2] <= 0
  0 <= xi <=42

  x*=[42,21,21], f*= -3456
"""

model = ConcreteModel()

def indices_rule(model):
  return xrange(1,4)
model.indices = Set(initialize=indices_rule, within=PositiveIntegers)

# declare decision variables
model.x = Var(model.indices, within=Reals)

# declare constraints
def bound_x_rule(model, i):
  return (0.0, model.x[i], 42.0)
model.bound_x = Constraint(model.indices, rule=bound_x_rule)

model.g1 = Constraint(expr = model.x[1]+2*model.x[2]+2*model.x[3] <= 72)
model.g2 = Constraint(expr = model.x[1]+2*model.x[2]+2*model.x[3] >= 0)

# declare objective
model.objective= Objective(
    expr = -model.x[1]*model.x[2]*model.x[3],
    sense = minimize)

# solve
SolverFactory('ipopt').solve(model).write()

print("obj = ", model.objective())
print("g1 = ", model.g1())
print("x1 = ", model.x[1]())
print("x2 = ", model.x[2]())
print("x3 = ", model.x[3]())