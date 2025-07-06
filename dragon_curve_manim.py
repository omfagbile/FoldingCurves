from manim import *
import numpy as np

def folding_instruction(order, rules):
    sequence = "A"
    for _ in range(order):
        sequence = "".join(rules.get(c, c) for c in sequence)
    return sequence.replace("A", "F").replace("B", "F")

def draw_instruction(instructions, step, initial_angle, folding_angle):
    """Return a VMobject representing the entire curve as one continuous path."""
    current_pos = ORIGIN
    current_angle = initial_angle
    path = VMobject()
    path.set_stroke(width=2)
    path.start_new_path(current_pos)

    for cmd in instructions:
        if cmd == "F":
            dir_vec = np.array([
                np.cos(np.radians(current_angle)),
                np.sin(np.radians(current_angle)),
                0
            ])
            next_pos = current_pos + step * dir_vec
            path.add_line_to(next_pos)
            current_pos = next_pos
        elif cmd == "+":
            current_angle += folding_angle
        elif cmd == "-":
            current_angle -= folding_angle

    return path

class DragonCurveEvolution(Scene):
    def construct(self):        
        # parameter, feel free to change!
        length = 5 # length of zeroth generation
        order = 15 # last generation
        rules = {"A": "A+B", "B": "A-B"} # Heighway's dragon
        angle = 180 - 90 # folding angle

        # draw
        previous_curve = None
        initial_angle = 0
        for gen in range(order+1):
            # compute parameters for this generation
            factor = 1 / (2 * np.cos(np.radians(angle/ 2)))
            step = length * (factor**gen)
            instruction = folding_instruction(gen, rules)
            curve = draw_instruction(instruction, step, initial_angle, angle)

            if previous_curve is None:
                self.play(Create(curve), run_time=1 + gen * 0.1)
            else:
                self.play(Transform(previous_curve, curve), run_time=1 + gen * 0.1)
                curve = previous_curve  

            previous_curve = curve
            initial_angle -= angle/2
            
        self.wait(2)


