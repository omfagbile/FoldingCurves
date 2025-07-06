from turtle import *
import sys

# Increase recursion limit (just in case, not strictly needed here)
sys.setrecursionlimit(10000)

def folding_instruction(order, rules):
    sequence = "A"
    for _ in range(order):
        sequence = "".join(rules.get(c, c) for c in sequence)
    return sequence.replace("A", "F").replace("B", "F")

def draw_instruction(sequence, step, angle=90):
    for cmd in sequence:
        if cmd == "F":
            forward(step)
        elif cmd == "+":
            left(180-angle)
        elif cmd == "-":
            right(180-angle)

# Parameters, feel free to change!
order = 11 # 18 seems to be the limit on my computer
step = 5
angle = 95 # folding angle (angle between line segments)
rules = {"A": "A+B", "B": "A-B"} # Heighway's dragon
#rules = {"A": "A-B-A+B+A+B-A+B-A", "B": "B+A-B+A-B-A-B+A+B"} # Helena's dragon

# Generate instructions
instructions = folding_instruction(order, rules)

# Setup turtle
speed(0)
penup()
goto(-100, -200)
pendown()
tracer(False)  # Disable animation
draw_instruction(instructions, step, angle)
update()       # Render all at once
done()