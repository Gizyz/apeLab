import math
import random
# fikset denne takket vere chatGpt og https://medium.com/@mbayburt/walkthrough-of-the-gjk-collision-detection-algorithm-80823ef5c774
# ===== Vector utilities =====
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def neg(a):
    return (-a[0], -a[1])

def triple_cross(a, b, c):
    """2D equivalent of a × (b × c), gives a vector."""
    return (
        b[0]*dot(a, c) - c[0]*dot(a, b),
        b[1]*dot(a, c) - c[1]*dot(a, b)
    )

def normalize(v):
    l = math.hypot(v[0], v[1])
    return (v[0]/l, v[1]/l) if l != 0 else (0, 0)

# ===== Support functions =====
def farthest(shape, direction):
    """Find the vertex of 'shape' farthest along 'direction'."""
    best = shape[0]
    best_dot = dot(best, direction)
    for p in shape[1:]:
        d = dot(p, direction)
        if d > best_dot:
            best_dot = d
            best = p
    return best

def support(A, B, d):
    """Minkowski difference support point."""
    p1 = farthest(A, d)
    p2 = farthest(B, neg(d))
    return sub(p1, p2)

# ===== Simplex handling =====
def handle_simplex(simplex, direction):
    """Update simplex and direction. Return (collision, new_direction)."""
    A = simplex[-1]
    AO = neg(A)

    if len(simplex) == 2:
        B = simplex[0]
        AB = sub(B, A)

        if dot(AB, AO) > 0:
            # Direction perpendicular to AB toward origin
            direction = triple_cross(AB, AO, AB)
        else:
            simplex[:] = [A]
            direction = AO
        return False, direction

    elif len(simplex) == 3:
        B = simplex[1]
        C = simplex[0]

        AB = sub(B, A)
        AC = sub(C, A)

        AB_perp = triple_cross(AC, AB, AB)
        AC_perp = triple_cross(AB, AC, AC)

        if dot(AB_perp, AO) > 0:
            simplex[:] = [A, B]
            direction = AB_perp
            return False, direction
        elif dot(AC_perp, AO) > 0:
            simplex[:] = [A, C]
            direction = AC_perp
            return False, direction
        else:
            return True, direction

# ===== GJK main loop =====
def GJK(A, B, verbose=False):
    direction = (1, 0)
    simplex = [support(A, B, direction)]
    direction = neg(simplex[0])

    for iteration in range(50):  # limit to prevent infinite loops
        new_point = support(A, B, direction)
        if dot(new_point, direction) <= 0:
            if verbose:
                print(f"[{iteration}] No collision: dot={dot(new_point, direction):.3f}")
            return False

        simplex.append(new_point)
        collision, direction = handle_simplex(simplex, direction)

        if verbose:
            print(f"[{iteration}] simplex={simplex}, dir={direction}, collision={collision}")

        if collision:
            return True

    return False


# --- Example test shapes ---
shapeA = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
shapeB_far = [(3, -1), (3, 1), (5, 1), (5, -1)]
shapeB_overlap = [(0.5, -1), (0.5, 1), (2.5, 1), (2.5, -1)]

triangle_A = [(0, 0), (2, 0), (1, 2)]
triangle_B_far = [(5, 0), (7, 0), (6, 2)]
triangle_B_overlap = [(1, 1), (3, 1), (2, 3)]

# --- Run tests ---
tests = [
    ("Separate squares", shapeA, shapeB_far),
    ("Overlapping squares", shapeA, shapeB_overlap),
    ("Separated triangles", triangle_A, triangle_B_far),
    ("Overlapping triangles", triangle_A, triangle_B_overlap)
]

if __name__ == '__main__':
    for name, A, B in tests:
        print(f"\n{name}:")
        result = GJK(A, B, verbose=True)
        print(f"Result → {result}")
