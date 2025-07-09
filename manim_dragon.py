from dragonlib import *
from manim import *
import numpy as np

def draw(instructions, step, initial_angle, left_angle, right_angle):
    """Return a VMobject representing the entire curve as one continuous path."""
    current_pos = ORIGIN
    current_angle = initial_angle
    path = VMobject()
    path.set_stroke(width=2)
    path.start_new_path(current_pos)

    for cmd in instructions:
        if cmd in "AB":
            dir_vec = np.array([
                np.cos(np.radians(current_angle)),
                np.sin(np.radians(current_angle)),
                0
            ])
            next_pos = current_pos + step * dir_vec
            path.add_line_to(next_pos)
            current_pos = next_pos
        elif cmd == "+":
            current_angle += left_angle
        elif cmd == "-":
            current_angle -= right_angle

    return path

class DragonCurveEvolution(Scene):
    def construct(self):        
        # parameter, feel free to change!
        length = 5 # length of zeroth generation
        generations = 15 # last generation
        left_angle = 90 
        right_angle = 90
        rule_A = "A+B"
        #rule_A = "A+B-A-B-A+B+A+B-A-B-A+B+A"

        # draw
        previous_curve = None
        initial_angle = 0
        command = "A"
        for gen in range(generations+1):
            # compute parameters for this generation
            x,y = end(rule_A, left_angle, right_angle)
            factor = np.sqrt(x**2 + y**2)**gen 
            step = length/factor 
            initial_angle = -np.degrees(np.arctan2(y,x)) * gen
            curve = draw(command, step, initial_angle, left_angle, right_angle)

            if previous_curve is None:
                self.play(Create(curve), run_time=1 + gen * 0.1)
            else:
                self.play(Transform(previous_curve, curve), run_time=1 + gen * 0.1)
                curve = previous_curve  

            previous_curve = curve
            command = folding_morphism(command, rule_A)
            
        self.wait(2)
