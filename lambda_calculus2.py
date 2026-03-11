#!/usr/bin/env python3
"""Lambda Calculus — full β-reduction with De Bruijn indices."""

class Term: pass
class Var(Term):
    def __init__(self, index): self.index = index
    def __repr__(self): return str(self.index)
class Abs(Term):
    def __init__(self, body): self.body = body
    def __repr__(self): return f"(λ.{self.body})"
class App(Term):
    def __init__(self, fn, arg): self.fn, self.arg = fn, arg
    def __repr__(self): return f"({self.fn} {self.arg})"

def shift(term, d, c=0):
    if isinstance(term, Var): return Var(term.index + d if term.index >= c else term.index)
    if isinstance(term, Abs): return Abs(shift(term.body, d, c + 1))
    return App(shift(term.fn, d, c), shift(term.arg, d, c))

def substitute(term, j, s):
    if isinstance(term, Var): return shift(s, j, 0) if term.index == j else term
    if isinstance(term, Abs): return Abs(substitute(term.body, j + 1, shift(s, 1, 0)))
    return App(substitute(term.fn, j, s), substitute(term.arg, j, s))

def beta_reduce(term):
    if isinstance(term, App) and isinstance(term.fn, Abs):
        return shift(substitute(term.fn.body, 0, shift(term.arg, 1, 0)), -1, 0)
    return None

def normalize(term, max_steps=100):
    for _ in range(max_steps):
        reduced = beta_reduce(term)
        if reduced is not None: term = reduced; continue
        if isinstance(term, App):
            fn = normalize(term.fn, max_steps // 2)
            if repr(fn) != repr(term.fn): term = App(fn, term.arg); continue
            arg = normalize(term.arg, max_steps // 2)
            if repr(arg) != repr(term.arg): term = App(term.fn, arg); continue
            reduced = beta_reduce(term)
            if reduced is not None: term = reduced; continue
        if isinstance(term, Abs):
            body = normalize(term.body, max_steps // 2)
            if repr(body) != repr(term.body): term = Abs(body); continue
        break
    return term

# Church encodings
ZERO = Abs(Abs(Var(0)))                          # λf.λx.x
ONE = Abs(Abs(App(Var(1), Var(0))))               # λf.λx.f x
TWO = Abs(Abs(App(Var(1), App(Var(1), Var(0)))))  # λf.λx.f(f x)
SUCC = Abs(Abs(Abs(App(Var(1), App(App(Var(2), Var(1)), Var(0))))))
TRUE = Abs(Abs(Var(1)))                           # λx.λy.x
FALSE = Abs(Abs(Var(0)))                          # λx.λy.y
I = Abs(Var(0))                                   # λx.x

if __name__ == "__main__":
    # I I = I
    result = normalize(App(I, I))
    print(f"I I = {result}")
    # SUCC ZERO
    one = normalize(App(SUCC, ZERO))
    print(f"SUCC 0 = {one}")
    # SUCC (SUCC ZERO)
    two = normalize(App(SUCC, App(SUCC, ZERO)))
    print(f"SUCC (SUCC 0) = {two}")
    # TRUE a b = a
    print(f"TRUE a b = {normalize(App(App(TRUE, Var(99)), Var(98)))}")
