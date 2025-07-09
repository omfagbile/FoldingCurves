import numpy as np
import sys

sys.setrecursionlimit(10000) # Increase recursion limit (just in case, not strictly needed here)

def switch(word):
    """ switching involution on words over {A,B,+,-}"""
    rules = {"A":"B", "B":"A", "+":"-","-":"+"}
    return "".join(rules.get(c, c) for c in word)

def reverse(word):
    """reversing involution"""
    return word[::-1]

def folding_morphism(word, rule_A):
    """return P_0 applied to word over {A,B,+,-} given P_0(A)"""
    rules = {"A":rule_A, "B":switch(reverse(rule_A))}
    word = "".join(rules.get(c, c) for c in word)
    return word

def end(rule_A, left_angle, right_angle):
    """ Simulates a turtle walk over the instruction string `rule_A`:
    Each 'A' or 'B' represents a forward move of unit length,
    '+' turns left 90 degrees, '-' turns right 90 degrees.
    Returns the final (x, y) position after executing all commands."""
    x, y = 0, 0
    angle = 0  # initial direction facing right
    for cmd in rule_A:
        if cmd in "AB":
            x += np.cos(np.radians(angle))
            y += np.sin(np.radians(angle))
        elif cmd == "-":
            angle -= right_angle
        elif cmd == "+":
            angle += left_angle
    return (x, y)
