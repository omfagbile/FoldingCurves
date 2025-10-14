import numpy as np
from turtle import *
import canvasvg
import io
from contextlib import redirect_stdout, redirect_stderr

SQUAREGRID_ALPHABET = ('A', 'B')
MIDGRID_ALPHABET = ('R', 'r', 'L', 'l', 'S', 's')

# Helpers for drawing
screen = Screen()
screen._root.withdraw()  # Hide the Tk window
canvas = screen.getcanvas()
ANGLE_90 = 90
FONTNAME = "Times New Roman"
FONTTYPE = "normal"
FONTSIZE = 12

# Helper to quietly save SVG (suppress stdout/stderr)
def save_canvas_svg(filename: str, reset_after: bool = True):
    update()
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with redirect_stdout(buf_out), redirect_stderr(buf_err):
        canvasvg.saveall(filename, canvas)
    if reset_after:
        clearscreen()

def _turtle_turn_right(radius: float, angle: float = 90.0) -> None:
    """
    Turn right by `angle` degrees. If `radius > 0`, draw a clockwise arc
    of that radius and extent instead of a sharp turn.
    """
    if radius and radius > 0:
        circle(-radius, extent=angle)  # clockwise arc
    else:
        right(angle)

def _turtle_turn_left(radius: float, angle: float = 90.0) -> None:
    """
    Turn left by `angle` degrees. If `radius > 0`, draw a counterclockwise arc
    of that radius and extent instead of a sharp turn.
    """
    if radius and radius > 0:
        circle(radius, extent=angle)   # counterclockwise arc
    else:
        left(angle)

def end_squaregrid_word(word: str) -> tuple[int, int]:
    """
    Compute the integer endpoint of a square-grid word over {A,B,+,-}.
    '+' = left 90°, '-' = right 90°, 'A'/'B' = step forward.
    Returns (x, y) as integers.
    """
    x, y = 0, 0
    dir = 0 # direction: 0 = West, 1 = North, 2 = East, 3 = South
    for cmd in word:
        if cmd in "AB":
            if dir == 0:   x += 1
            elif dir == 1: y += 1
            elif dir == 2: x -= 1
            else: y -= 1
        elif cmd == '+':
            dir = (dir - 1) % 4
        elif cmd == '-':
            dir = (dir + 1) % 4
    return x, y

def draw_sqauregrid_word(word: str, 
                                step: float,
                                initial_angle: float = 0.0,
                                rounded_corners: float = 0.2,
                                pen_colour: str = "black",
                                pen_width: float = 2.5,
                                arrow_head: bool = True,
                                label: bool = False) -> None:
    """Axis-aligned: 'A'/'B' forward, '+' left 90°, '-' right 90°."""
    tracer(0)         # no per-move repaint
    ht()              # hide turtle
    pencolor(pen_colour)
    pensize(pen_width)
    penup(); home(); setheading(initial_angle); pendown()

    radius = rounded_corners * step

    forward(radius)
    for ch in word:
        if ch == "A":
            forward(0.5 * (step - 2*radius))
            if label:
                write(ch, align = "center", font = (FONTNAME, FONTSIZE, FONTTYPE))
            forward(0.5 * (step - 2*radius))
        if ch == "B":
            forward(0.5 * (step - 2*radius))
            if label:
                write(ch, align = "right", font = (FONTNAME, FONTSIZE, FONTTYPE))
            forward(0.5 * (step - 2*radius))
        elif ch == "+":
            if label: 
                write(ch, align="left", font = (FONTNAME, FONTSIZE, FONTTYPE))
            _turtle_turn_right(radius=radius, angle=ANGLE_90)
        elif ch == "-":
            if label:
                write(ch, align="left", font = (FONTNAME, FONTSIZE, FONTTYPE))
            _turtle_turn_left(radius=radius, angle=ANGLE_90)

    forward(radius)

    if arrow_head: 
        st()


def draw_midgrid_word(word: str, 
                             step: float,
                             initial_angle: float,
                             rounded_corners: float = 0.2,
                             pen_colour: str = "black",
                             pen_width: float = 2.5,
                             arrow_head: bool = False,
                             label: bool = False) -> None:
    """
    Draw curve of word over {R,r,L,l,S,s}
    R / r  = half-step, right turn 90°, half-step;  L / l = half-step, left turn 90°, half-step; S/s = full step.
    Each diagonal segment has length √2 * step.
    """    
    tracer(0)         # no per-move repaint
    ht()              # hide turtle
    pencolor(pen_colour)
    pensize(pen_width)
    penup(); home(); setheading(initial_angle); pendown()

    full = step * np.sqrt(2.0)
    half = 0.5 * full
    radius =  rounded_corners * full

    # initial half step
    
    # interior
    for ch in word:
        if ch in ("R", "r"):
            forward(half-radius)
            if label:
                write(ch, font = (FONTNAME, FONTSIZE, FONTTYPE))
            _turtle_turn_right(radius=radius, angle=ANGLE_90)
            forward(half-radius)
        elif ch in ("L", "l"):
            forward(half-radius)
            if label:
                write(ch, font = (FONTNAME, FONTSIZE, FONTTYPE))
            _turtle_turn_left(radius=radius, angle=ANGLE_90)
            forward(half-radius)
        elif ch in ("S", "s"):
            forward(0.5*full)
            if label:
                write(ch, font = (FONTNAME, FONTSIZE, FONTTYPE))
            forward(0.5*full)

    if arrow_head: 
        st()


class FoldingSequence:
    def __init__(self, folding_sequence: str):
        self.folding_sequence = folding_sequence

    def inv_switch(self, w: str) -> str:
        table = str.maketrans({"A":"B", "B":"A", "+":"-","-":"+", "R":"L", "L":"R", "S":"S", "a":"a", "v":"v"})
        return w.translate(table)

    def inv_reverse(self, w: str) -> str:
        return w[::-1]

    def inv_invert(self, w: str) -> str:
        return self.inv_reverse(self.inv_switch(w))

    def folding_morphism(self, D2_word: str):
        m = len(self.folding_sequence)
        omega = ('A', 'B')
        rule_A = "A"
        for i in range(m):
            rule_A = rule_A + self.folding_sequence[i] + omega[(i+1) % 2]
        rule_B = self.inv_invert(rule_A)
        rules = {"A": rule_A, "B": rule_B}
        D2_word = "".join(rules.get(c, c) for c in D2_word)
        return D2_word
        
    # ---------------- Boundary algorithm (Verrill) ----------------
    # CreateLeft / CreateRight on {A,B,+,-}* -> intermediate {R,L,S,a,v}* (no S produced here)
    def create_left(self, D2_word: str) -> str:
        mapping = {"A": "R", "B": "R", "+": "a", "-": "v"}
        return "".join(mapping.get(c, c) for c in D2_word)

    def create_right(self, D2_word: str) -> str:
        mapping = {"A": "L", "B": "L", "+": "v", "-": "a"}
        return "".join(mapping.get(c, c) for c in D2_word)

    def _reduce_once(self, w: list) -> tuple[list, bool]:
        changed = False
        i = 0
        out = []
        while i < len(w):
            # 3-letter patterns X v Y
            if i+2 < len(w) and w[i+1] == "v" and w[i] in "RLS" and w[i+2] in "RLS":
                X, Y = w[i], w[i+2]
                # Map (X, v, Y)
                if X == "R" and Y == "R": out.append("S")
                elif X == "L" and Y == "L": out.append("S")
                elif X == "R" and Y == "L": out.append("v")
                elif X == "L" and Y == "R": out.append("v")
                elif X == "S" and Y == "R": out.append("L")
                elif X == "S" and Y == "L": out.append("R")
                elif X == "S" and Y == "S": out.append("v")
                elif X == "R" and Y == "S": out.append("L")
                elif X == "L" and Y == "S": out.append("R")
                else:
                    # should not happen, but keep safe
                    out.extend([w[i], w[i+1], w[i+2]])
                i += 3
                changed = True
                continue
            # 2-letter patterns of a/v
            if i+1 < len(w) and w[i] in "av" and w[i+1] in "av":
                pair = w[i] + w[i+1]
                if pair in ("vv", "aa"): out.append("a")
                else: out.append("v")  # "av" or "va"
                i += 2
                changed = True
                continue
            # default pass-through
            out.append(w[i])
            i += 1
        return out, changed

    def reduce_backtracking(self, w: str) -> str:
        # Input over {R,L,S,a,v}*
        arr = list(w)
        changed = True
        while changed:
            arr, changed = self._reduce_once(arr)
        # ensure no stray 'i' (not used), and return
        return "".join(arr)

    def remove_ai(self, w: str) -> str:
        return "".join(ch for ch in w if ch in "RLS")

    def alternate_cases(self, start_parity: int, base: str) -> str:
        # base over {R,L,S}*
        out = []
        p = start_parity  # 0 -> even (upper), 1 -> odd (lower)
        for ch in base:
            if p == 0:
                out.append(ch)  # uppercase already
            else:
                out.append({"R":"r","L":"l","S":"s"}[ch])
            # update parity
            if ch in "RL":
                p = 1 - p
            # if ch == 'S', parity unchanged
        return "".join(out)

    def initial_cases(self, P0A: str) -> tuple[int,int]:
        # p0 for R/L/S boundaries; p1 for r/l/s boundaries
        p0 = 0 if P0A[0] == "A" else 1
        p1 = 1 if P0A[-1] == "A" else 0
        return p0, p1

    def boundary_morphism(self, w: str) -> str:
        """
        Construct Verrill's boundary L-system map P1: Ω1* -> Ω1*,
        from the folding rule P0 encoded by self.folding_sequence.
        """
        # Step 0: P0(A)
        P0A = self.folding_morphism("A")
        # Step 1: CreateLeft / Right
        wR_tilde = self.create_left(P0A)
        wL_tilde = self.create_right(P0A)
        # Step 2: Reduce backtracking
        wR_red = self.reduce_backtracking(wR_tilde)
        wL_red = self.reduce_backtracking(wL_tilde)
        # Step 3: Remove a/v for base paths
        wR_base = self.remove_ai(wR_red)
        wL_base = self.remove_ai(wL_red)
        # Step 4: initial parities
        p0, p1 = self.initial_cases(P0A)
        # Step 5: R, L
        P1_R = self.alternate_cases(p0, wR_base)
        P1_L = self.alternate_cases(p0, wL_base)
        # Step 6: r, l via invert of opposite boundary
        w_r_base = self.remove_ai(self.inv_invert(wL_red))
        w_l_base = self.remove_ai(self.inv_invert(wR_red))
        P1_r = self.alternate_cases(p1, w_r_base)
        P1_l = self.alternate_cases(p1, w_l_base)
        # Step 7: S, s via Reduce(R v invert(L)) (and its odd variant)
        wS_tilde = self.reduce_backtracking(wR_red + "v" + self.inv_invert(wL_red))
        wS_base = self.remove_ai(wS_tilde)
        P1_S = self.alternate_cases(p0, wS_base)

        ws_tilde = self.reduce_backtracking(self.inv_invert(wL_red) + "v" + wR_red)
        ws_base = self.remove_ai(ws_tilde)
        P1_s = self.alternate_cases(p1, ws_base)

        table = str.maketrans({"R": P1_R, "L": P1_L, "S": P1_S, "r": P1_r, "l": P1_l, "s": P1_s})
    
        return w.translate(table)

    def boundary_morphism_adjacency_matrix(self, vertex_set: list = ['R', 'L', 'S', 's']):
        """
        Compute the adjacency matrix of the boundary morphism restricted to `vertex_set`,
        counting occurrences of each letter v or its invert (without double counting).
        """
        invert_map = {"R": "l", "L": "r", "S": "S", "s": "s",
                    "r": "L", "l": "R"} 
        k = len(vertex_set)
        M = np.zeros((k, k), dtype=int)

        for i, src in enumerate(vertex_set):
            img = self.boundary_morphism(src)
            for j, tgt in enumerate(vertex_set):
                tgt_inv = invert_map.get(tgt, tgt)
                # Count letters in img equal to tgt or its invert
                M[i, j] = sum(1 for ch in img if ch == tgt or ch == tgt_inv)

        return M

    def turtledraw_foldingcurve(self,
                    i: int,
                    step: float = 12.0,
                    filename: str = "folding.svg",
                    draw_curve: bool = True,
                    draw_boundary: bool = False,
                    curve_colour: str = "#000000",
                    left_colour: str = "#ff6b6b",
                    right_colour: str = "#1e90ff",
                    curve_width: float = 2.5,
                    boundary_width: float = 3.0,
                    arrow_head: bool = False,
                    rounded_corners: float = 0.2) -> None:
        """
        Render the ith square-grid folding curve generated by our folding sequence (L^{-n}C(P^n(A))) and (optionally) its
        right/left boundaries using Python turtle, then save to SVG via canvasvg.
        """
        # 1) Build P^n_σ(A)
        w = "A"
        for _ in range(i):
            w = self.folding_morphism(w)

        # 2) Iterate Verrill boundary map on seeds 'R' and 'L'
        def iterate_boundary(seed: str, n: int) -> str:
            b = seed
            for _ in range(n):
                b = self.boundary_morphism(b)
            return b

        br, bl = "", ""
        if draw_boundary:  
            br = iterate_boundary("R", i)
            bl = iterate_boundary("L", i) 

        # 5) Boundary start headings (SVG/turtle screen coords: +y is up in turtle)
        # Map JS Bdirs to turtle angles:
        #   NE: 45°,  NW: 135°,  SW: 225°,  SE: 315°   (turtle 0°=+x, CCW positive)
        starts_with_A = (w[0] == "A")
        if starts_with_A:
            base_R = 45.0    # NE for right boundary
            base_L = 315.0   # SE for left boundary
        else:
            base_R = 135.0   # NW
            base_L = 45.0    # NE

        (x,y) = end_squaregrid_word(self.folding_morphism("A"))
        factor = np.sqrt(x**2 + y**2)
        angle = np.arctan2(y,x) * 180/np.pi

        # 6) Draw in order: boundaries first
        if draw_boundary:
            draw_midgrid_word(word=br, step=step/(factor**i), initial_angle=base_R - i*angle, pen_colour=left_colour, pen_width=boundary_width, rounded_corners=rounded_corners)
            draw_midgrid_word(word=bl, step=step/(factor**i), initial_angle=base_L - i*angle, pen_colour=right_colour, pen_width=boundary_width, rounded_corners=rounded_corners)
        if draw_curve:
            draw_sqauregrid_word(word=w, step=step/(factor**i), initial_angle=-i*angle, pen_colour=curve_colour, pen_width=curve_width, arrow_head=arrow_head, rounded_corners=rounded_corners)

        # 7) Save SVG & close and supress warning
        save_canvas_svg(filename)
        clearscreen()

