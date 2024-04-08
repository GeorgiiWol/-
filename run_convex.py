#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import *

f = Void()
Figure().set_points()
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, {f.counter()}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
