import re
from dataclasses import dataclass, field
from typing import Generator, List, Sequence, Union

DEFAULT_KEYWORDS = dict(LBRA="<", RBRA=">", ALT="|")


@dataclass
class Expr:
    children: List["Expr"] = field(default_factory=list)


class ConcatExpr(Expr):
    def __repr__(self):
        return "{" + " ".join(map(repr, self.children)) + "}"


class AltExpr(Expr):
    def __repr__(self):
        return "{" + " | ".join(map(repr, self.children)) + "}"


def parse_tokens(token_iter, keywords, is_outer=True):
    head = ConcatExpr()
    res = AltExpr([head])
    for t in token_iter:
        if t == keywords["LBRA"]:
            head.children.append(parse_tokens(token_iter, keywords, is_outer=False))
        elif t == keywords["RBRA"]:
            if is_outer:
                raise ValueError("Unmatched closing bracket")
            return res
        elif t == keywords["ALT"]:
            head = ConcatExpr()
            res.children.append(head)
        else:
            head.children.append(t)
    if not is_outer:
        raise ValueError("Unmatched opening bracket")
    return res


def parse(string: str, keywords: dict = DEFAULT_KEYWORDS) -> Expr:
    pattern = "(" + "|".join(re.escape(s) for s in keywords.values()) + ")"
    tokens_iter = (s for s in re.split(pattern, string) if s)
    return parse_tokens(tokens_iter, keywords)


def iter_alts(exprs: Sequence[Union[Expr, str]]) -> Generator[List[str], None, None]:
    """Iterate over all possible combinations of expressions."""
    if exprs:
        x, *xs = exprs
        yield from ([*y, *ys] for ys in iter_alts(xs) for y in iter_expr(x))
    else:
        yield []


def iter_expr(expr: Union[Expr, str]) -> Generator[List[str], None, None]:
    if isinstance(expr, ConcatExpr):
        yield from iter_alts(expr.children)
    elif isinstance(expr, AltExpr):
        yield from (x for e in expr.children for x in iter_expr(e))
    elif isinstance(expr, str):
        yield [str(expr)]  # mypy needs the str() here


def iterexpand(string: str, brackets=("<", ">"), alt="|") -> Generator[str, None, None]:
    """Expand a string that specifies a prompt matrix into a list of
    strings.

    Args:
        string: The string to expand.
        brackets: A pair of characters that delimit the start and end of
            an alternation group.
        alt: The character that separates alternatives in a prompt

    Returns:
        An iterator of strings.
    """
    keywords = dict(LBRA=brackets[0], RBRA=brackets[1], ALT=alt)
    expr = parse(string, keywords)
    yield from ("".join(words) for words in iter_expr(expr))


def expand(string: str, brackets=("<", ">"), alt="|") -> List[str]:
    """Expand a string that specifies a prompt matrix into a list of
    strings.

    Args:
        string: The string to expand.
        brackets: A pair of characters that delimit the start and end of
            an alternation group.
        alt: The character that separates alternatives in a prompt

    Returns:
        A list of strings.
    """
    return list(iterexpand(string, brackets, alt))
