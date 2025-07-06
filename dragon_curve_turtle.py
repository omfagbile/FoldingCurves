from turtle import *
import sys

# Increase recursion limit (just in case, not strictly needed here)
sys.setrecursionlimit(10000)

def folding_instruction(order, rules):
    sequence = "A"
    for _ in range(order):
        sequence = "".join(rules.get(c, c) for c in sequence)
    return sequence.replace("A", "F").replace("B", "F")

def draw_instruction(sequence, step, left_angle=90, right_angle=90):
    for cmd in sequence:
        if cmd == "F":
            forward(step)
        elif cmd == "+":
            right(right_angle)
        elif cmd == "-":
            left(left_angle)

# Parameters, feel free to change!
order = 15 # 18 seems to be the limit on my computer
step = 3
angle = 90 # folding angle (angle between line segments)
rules = {"A": "A+B", "B": "A-B"} # Heighway's dragon
#rules = {"A": "A-B-A+B+A+B-A+B-A", "B": "B+A-B+A-B-A-B+A+B"} # Helena's dragon

# Generate instructions
instructions = folding_instruction(order, rules)
#print(instructions)

# Setup turtle
speed(0)
penup()
goto(-200, 200)
pendown()
tracer(False)  # Disable animation
draw_instruction(instructions, step, angle, angle)
update()       # Render all at once
done()