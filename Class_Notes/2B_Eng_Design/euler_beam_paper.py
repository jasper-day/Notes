import numpy as np
import matplotlib.pyplot as plt
import pint

ureg = pint.UnitRegistry()

def mass_cylinder(diam, length, rolls):
    # one sheet of A4 paper weighs 5g
    m = 5 * ureg.g
    # area of one sheet of A4 is 
    a = 210 * 297 * ureg.Quantity("mm^2")
    rho = m / a
    cylinder_area = diam * np.pi * length * rolls
    cylinder_mass = rho * cylinder_area
    return cylinder_mass

def get_moment_force(max_force, length):
    # force in Newtons, acting on the end of the cylinder
    force = np.arange(0,max_force,0.1) * ureg.N
    Moment = force * length
    return Moment, force

def section_properties(diam, t):
    r = diam/2
    # second moment of area for thin walled cylinder
    I_x = np.pi * r**3 * t
    # section modulus of cylinder
    C = I_x / r
    return I_x, C


def tip_deflection(force, length, E, I_x): 
    return (force * length**3 / (3 * E * I_x)).to("mm")


def main():

    diam = int(input("Input the diameter of the paper beam (mm): ")) * ureg.mm
    length = int(input("Input the length of the beam (mm): ")) * ureg.mm
    rolls = int(input("Input the thickness of the beam in sheets of paper: "))
    max_force = int(input("Input the maximum force expected on the structure: "))
    cylinder_mass = mass_cylinder(diam, length, rolls)

    # thickness of sheet of paper
    t = 0.1 * ureg.mm * rolls

    # Young's modulus for paper ~ 2 GPa
    E = 2 * ureg.Quantity("GPa")

    M, force = get_moment_force(max_force, length)
    I_x, C = section_properties(diam, t)
    
    sg_max = (M/I_x * diam/2).to("Pa")

    deflect = tip_deflection(force, length, E, I_x)

    print(f""" Cylinder stats:
    Mass:                                   {cylinder_mass:_.0f}
    Second moment of area:                  {I_x:_.0f}
    Section modulus:                        {C:_.0f}
    Maximum stress due to bending:          {max(sg_max):_.0f}
    Maximum tip deflection due to load:   {max(deflect):_.2f}
    """)
    
if __name__ == "__main__":
    main()