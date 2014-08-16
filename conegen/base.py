# this script will solve for the length of the cone so
# that we know the length of it for a given diameter.
import argparse
import solid

from sympy.solvers import solve
from sympy import Symbol

EPSILON = 1e-10

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
# size of the center notch to align the parts on
center_notch = 10.0
# diameter of the milling tool
tool_radius = 3.0

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


def feq(v):
    return abs(v) < EPSILON

def frange(start, end, step):
    while not feq(start - end):
        yield start
        start += step

def produce_slice(lower, upper, outer_offset=0.0):
    res = []
    step = (upper - lower) / slice_steps
    for i, f in enumerate(frange(lower, upper, step)):
        r1 = cone_at(f)
        r2 = cone_at(f + step)
        offset = i * step + outer_offset
        res.append(
            solid.translate([0, 0, offset])(
                solid.cylinder(h=step, r1=r1, r2=r2)
                )
        )
    return res


def scaffold(length, color=[0, 0, 1, 1]):
    h = solid.translate([diameter / 2.0, 0, length / 2.0])(
        solid.scale([diameter, diameter, length])(
            solid.cube(center=True)
            )
    ) + solid.translate([0, 0, length / 2.0])(
        solid.scale([center_notch + tool_radius * 2,
                     center_notch, length])(
            solid.cube(center=True)
            )
    )
    # scale & move in Z to ensure overlap
    h = solid.translate([0, 0, -(length * .1)/2.0])(solid.scale([1, 1, 1.1])(h))
    return solid.color(color)(h)


def full_cone():
    cylinders = []
    for slice_num, (lower, upper) in enumerate(slice_parameters()):
        cylinders.extend(produce_slice(lower, upper, mdf_strength * slice_num))

    return solid.translate([0, 0, cone_length])(
        solid.rotate([0, 180, 0])(
            solid.union()(*cylinders)
            )
        )


def single_slice(index):
    for slice_num, (lower, upper) in enumerate(slice_parameters()):
        if slice_num == index:
            return solid.translate([0, 0, upper - lower])(
                solid.rotate([0, 180, 0])(
                    solid.union()(*produce_slice(lower, upper))
                    ))
    raise Exception("Non-existent slice %i, max: %i!" % (index, slice_num))


def preamble():
    print "$fn=%s;" % fn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slice", type=int)
    parser.add_argument("-s", "--sub-scaffold", action="store_true")
    args = parser.parse_args()

    if args.slice is not None:
        sl = single_slice(args.slice)
        if args.sub_scaffold:
            sl = sl - scaffold(mdf_strength)
        preamble()
        print solid.scad_render(sl)
    else:
        preamble()
        print solid.scad_render(full_cone() - scaffold(cone_length))
        #print solid.scad_render(scaffold())
