from dragonlib import *

def draw(command, step, initial_angle, left_angle, right_angle):
    right(initial_angle)
    for cmd in command:
        if cmd in "AB":
            forward(step)
        elif cmd == "-":
            right(right_angle)
        elif cmd == "+":
            left(left_angle)

def main():
    # Parameters, feel free to change!
    generation = 1 # 18 seems to be the limit on my computer
    length = 1000 # length of zeroth generation
    left_angle = 90
    right_angle = 90
    #left_angle = 180-17*180/32
    #right_angle = 180-17*180/32
    rule_A = "A+B" # Heighway's dragon
    #rule_A = "A-B-A+B+A+B-A+B-A" # example of symmetric 9-fold
    #rule_A = "A+B-A-B-A+B+A+B-A-B-A+B+A" # example of a asymmetric 13-fold
    #rule_A = "A+B+A" # example of self-intersecting dragon

    # Calculate instructions and parameters
    command = "A"
    for _ in range(generation): command = folding_morphism(command, rule_A)
    x,y = end(rule_A, left_angle, right_angle)
    factor = np.sqrt(x**2 + y**2)**generation   
    step = length/factor 
    initial_angle = np.degrees(np.arctan2(y,x)) * generation

    # Setup turtle
    speed(0)
    penup()
    goto(-450, -180)
    pendown()
    tracer(False)  # Disable animation
    draw(command, step, initial_angle, left_angle, right_angle)
    update()       # Render all at once
    done()

if __name__ == "__main__":
    main()