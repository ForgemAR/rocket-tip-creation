# this script will solve for the length of the cone so
# that we know the length of it for a given diameter.
from sympy.solvers import solve
from sympy import Symbol

a = 0.648148
b = 0.0
c = 0.75
x = Symbol('x')

cone_formula = a*(x - b)**c

def compute_cone_length(diameter):
    return solve(cone_formula - diameter / 2.0, x)[0]

def cone_at(x):
    return a*(x - b)**c

# all units are mm, unless specified otherwise

# strength of the MDF material used for milling
mdf_strength = 16.0
# outer diameter of the rocket
diameter = 118.00
# the alu-tip diameter, the cone is only
# created up until that.
alu_tip_diameter = 41.0
# slice_steps is the amount of steps / slice
slice_steps = 10.0
# render quality in scad
fn = 100

bottom_cone_length = compute_cone_length(diameter)
assert 380.0 < bottom_cone_length < 450.0
tip_cone_length = compute_cone_length(alu_tip_diameter)

assert tip_cone_length < bottom_cone_length
cone_length = bottom_cone_length - tip_cone_length

def slice_parameters():
    lower = tip_cone_length
    while lower < bottom_cone_length:
        yield lower, min(lower + mdf_strength, bottom_cone_length)
        lower += mdf_strength

def frange(start, end, step):
    while start < end:
        yield start
        start += step

cylinders = []

for slice_num, (lower, upper) in enumerate(slice_parameters()):
    step = (upper - lower) / slice_steps
    for i, f in enumerate(frange(lower, upper, step)):
        r1 = cone_at(f)
        r2 = cone_at(f + step)
        offset = i * step + mdf_strength * slice_num
        cylinders.append("translate([0, 0, %(offset)f]) cylinder(h=%(step)f, r1=%(r1)f, r2=%(r2)f, $fn=%(fn)i);" % dict(
            step=step,
            r1=r1,
            r2=r2,
            offset=offset,
            fn=fn
            ))

print "translate([0, 0, %(cone_length)f]) rotate([0, 180, 0]){" % dict(cone_length=cone_length)
print "\n".join(cylinders)
print "}"
