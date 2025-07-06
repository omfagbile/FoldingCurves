from turtle import *
import sys

# Increase recursion limit (just in case, not strictly needed here)
sys.setrecursionlimit(10000)

def koch_instruction(order):
    axiom = "F"
    rules = {"F": "F+F--F+F"}

    sequence = axiom
    for _ in range(order):
        sequence = "".join(rules.get(c, c) for c in sequence)
    return sequence

def draw_instruction(sequence, step):
    for cmd in sequence:
        if cmd == "F":
            forward(step)
        elif cmd == "+":
            left(60)
        elif cmd == "-":
            right(60)

# Parameters, feel free to change!
order = 5        
size = 3 

# Generate instructions
instructions = koch_instruction(order)

# Setup turtle
speed(0)
penup()
goto(-300, 0)
pendown()
tracer(False)  # Disable animation
draw_instruction(instructions, size)
update()       # Render all at once
done()
