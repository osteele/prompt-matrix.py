from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class Expr:
    children: List['Expr'] = field(default_factory=list)


class ConcatExpr(Expr):
    def __repr__(self):
        return '{' + ' '.join(map(repr, self.children)) + '}'


class AltExpr(Expr):
    def __repr__(self):
        return '{' + ' | '.join(map(repr, self.children)) + '}'


def parse_tokens(token_iter, keywords):
    head = ConcatExpr()
    res = AltExpr([head])
    for t in token_iter:
        if t == keywords['LBRA']:
            head.children.append(parse_tokens(token_iter, keywords))
        elif t == keywords['RBRA']:
            break
        elif t == keywords['ALT']:
            head = ConcatExpr()
            res.children.append(head)
        else:
            head.children.append(t)
    return res


def parse(string, keywords):
    pattern = '(' + '|'.join(re.escape(s) for s in keywords.values()) + ')'
    tokens_iter = (s for s in re.split(pattern, string) if s)
    return parse_tokens(tokens_iter, keywords)


def seq_alts_i(exprs):
    if exprs:
        x, *xs = exprs
        yield from ([*y, *ys] for ys in seq_alts_i(xs) for y in expand_expr_i(x))
    else:
        yield []


def expand_expr_i(expr):
    if isinstance(expr, ConcatExpr):
        yield from seq_alts_i(expr.children)
    elif isinstance(expr, AltExpr):
        yield from (x for e in expr.children for x in expand_expr_i(e))
    else:
        yield [expr]


def expandi(string, brackets=('<', '>'), alt='|'):
    keywords = dict(LBRA=brackets[0], RBRA=brackets[1], ALT=alt)
    expr = parse(string, keywords)
    return (''.join(ar) for ar in expand_expr_i(expr))


def expand(string, brackets=('<', '>'), alt='|'):
    return list(expandi(string, brackets, alt))
