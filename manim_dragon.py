from manim import *
import numpy as np

def end(word, left_angle, right_angle):
        x, y = 0, 0
        angle = 0  # initial direction facing right
        for cmd in word:
            if cmd in "AB":
                x += np.cos(np.radians(angle))
                y += np.sin(np.radians(angle))
            elif cmd == "-":
                angle += left_angle
            elif cmd == "+":
                angle -= right_angle
        return (x, y)

def folding_morphism(word, rule_A):
    invert = {"A": "B", "B": "A", "+":"-", "-":"+"}
    rule_B = ''.join(invert[ch] for ch in reversed(rule_A))
    rules = {"A": rule_A, "B": rule_B}
    return "".join(rules.get(c, c) for c in word)

def manim_draw(instructions, step, initial_angle, left_angle, right_angle):
    """Return a VMobject representing the entire curve as one continuous path."""
    current_pos = ORIGIN + DOWN + 2*LEFT
    current_angle = initial_angle
    path = VMobject()
    path.set_stroke(width=2)
    path.set_color(BLACK)
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
        elif cmd == "-":
            current_angle += left_angle
        elif cmd == "+":
            current_angle -= right_angle

    return path

class DragonCurveEvolution(Scene):
    def construct(self):       
        self.camera.background_color = WHITE 
        # parameter, feel free to change!
        length = 5 # length of zeroth generation
        generations = 15 # last generation
        left_angle = 90 
        right_angle = 90
        rule_A = "A+B"
        #rule_A = "A+B-A-B-A+B+A+B-A-B-A+B+A"

        x,y = end(rule_A, left_angle, right_angle)
        factor = np.sqrt(x**2 + y**2)

        # draw
        previous_curve = None
        initial_angle = 0
        command = "A"
        for gen in range(generations+1):
            # compute parameters for this generation
    
            initial_angle = -np.degrees(np.arctan2(y,x)) * gen
            curve = manim_draw(command, length, initial_angle, left_angle, right_angle)

            if previous_curve is None:
                self.play(Create(curve), run_time=1 + gen * 0.1)
            else:
                self.play(Transform(previous_curve, curve), run_time=1 + gen * 0.1)
                curve = previous_curve  

            previous_curve = curve
            command = folding_morphism(command, rule_A)
            length = length/factor 
            
        self.wait(2)
