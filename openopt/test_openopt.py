from numpy import *
from openopt import *
 
coeff = 1e-8
 
f = lambda x: (x[0]-20)**2+(coeff * x[1] - 80)**2 # objFun
c = lambda x: (x[0]-14)**2-1 # non-lin ineq constraint(s) c(x) <= 0
# for the problem involved: f_opt =25, x_opt = [15.0, 8.0e9]
 
x0 = [-4,4]
# even modification of stop criteria can't help to achieve the desired solution:
someModifiedStopCriteria = {'gradtol': 1e-15,  'ftol': 1e-15,  'xtol': 1e-15}
 
# using default diffInt = 1e-7 is inappropriate:
p = NLP(f, x0, c=c, **someModifiedStopCriteria)
r = p.solve('ipopt')
print(r.ff,  r.xf) #  will print something like "6424.9999886000014 [ 15.0000005   4.       ]"
 
# for to improve the solution we will use
# changing either p.diffInt from default 1e-7 to [1e-7,  1]
# or p.scale from default None to [1,  1e-7]
 
# latter (using p.scale) is more recommended
# because it affects xtol for those solvers
# who use OO stop criteria
# (ralg, lincher, nsmm, nssolve and mb some others)
#  xtol will be compared to scaled x shift:
# is || (x[k] - x[k-1]) * scale || < xtol
 
# You can define scale and diffInt as
# numpy arrays, matrices, Python lists, tuples
 
p = NLP(f, x0, c=c, scale = [1,  coeff],  **someModifiedStopCriteria)
r = p.solve('ipopt')
print(r.ff,  r.xf) # "24.999996490694787 [  1.50000004e+01   8.00004473e+09]" - much better


"""
GLP (GLobal Problem from OpenOpt set) example for FuncDesigner model:
searching for global minimum of the func 
(x-1.5)**2 + sin(0.8 * y ** 2 + 15)**4 + cos(0.8 * z ** 2 + 15)**4 + (t-7.5)**4
subjected to some constraints
See http://openopt.org/GLP for more info and examples.
"""
from openopt import GLP
from FuncDesigner import *
 
x, y, z, t = oovars(4)
 
# define objective
f = (x-1.5)**2 + sin(0.8 * y ** 2 + 15)**4 + cos(0.8 * z ** 2 + 15)**4 + (t-7.5)**4
 
# define some constraints
constraints = [x<1, x>-1, y<1, y>-1, z<1, z>-1, t<1, t>-1, x+2*y>-1.5,  sinh(x)+cosh(z)+sinh(t) <2.0]
 
# add some more constraints via Python "for" cycle
M = 10
for i in xrange(M):
    func = i*x+(M-i)*y+sinh(z)+cosh(t)
    constraints.append(func < i+1)
 
# define start point. You can use variables with length > 1 as well
startPoint = {x:0, y:0, z:0, t:0}
 
# assign prob
p = GLP(f, startPoint, constraints=constraints,  maxIter = 1e3,  maxFunEvals = 1e5,  maxTime = 5,  maxCPUTime = 5)
 
#optional: graphic output
#p.plot = 1 or p.solve(..., plot=1) or p = GLP(..., plot=1)
 
# solve
r = p.solve('de') # try other solvers: galileo, pswarm
 
x_opt, y_opt, z_opt, t_opt = r(x, y, z, t)
# or 
# x_opt, y_opt, z_opt, t_opt = x(optPoint), y(optPoint), z(optPoint), t(optPoint)


# Example for NSP 
# |x[0]| + 1.2*|x[1]| + 1.44*|x[2]| + ... + 1.2^74*|x[74]| + |y-15| +|y+15| + y^2 +  -> min
# with some constraints
# coded in FuncDesigner
# all 1st derivatives are obtained via Automatic Differentiation,
# not to be confused with finite-difference derivatives approximation
 
from numpy import cos, arange
from FuncDesigner import *
from openopt import NSP
 
x, y = oovars('x y')
 
N = 75
koeffs = arange(1, N+1) ** 1.2 # 1, 1.2, 1.44, ..., 1.2^m, ..., 1.2^N
 
objective = sum(abs(x) * koeffs) + abs(y-15) + abs(y+15) + y**2
constraints = [(y-1)**2<1, abs(y) < 0.5]
constraints.append((x - 0.01*arange(N))**2 < 0.1*arange(1, N+1)) # (x_0-0)**2 < 0.1, (x_1-0.01)**2 < 0.2, (x_2-0.02)**2 < 0.3,...
startPoint = {x: cos(1+arange(N)), y:80}
 
p = NSP(objective, startPoint, maxIter = 1e5, constraints = constraints)
 
r = p.solve('ralg')
x_opt, y_opt = x(r), y(r)
print(max(abs(x_opt)), y_opt)
 
