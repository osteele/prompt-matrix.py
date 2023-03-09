import random
import re
from dataclasses import dataclass, field
from typing import Generator, List, Sequence, Union

DEFAULT_KEYWORDS = dict(ALT_LBRA="<", ALT_RBRA=">", ALT="|", OPT_LBRA="[", OPT_RBRA="]")


@dataclass
class Expr:
    children: List["Expr"] = field(default_factory=list)


class ConcatExpr(Expr):
    def __repr__(self):
        return "{" + " ".join(map(repr, self.children)) + "}"


class AltExpr(Expr):
    def __repr__(self):
        return "{" + " | ".join(map(repr, self.children)) + "}"


# handcrafted recursive descent parser
def parse_tokens(token_iter, keywords, close_bracket=None):
    res = head = ConcatExpr()
    # res = AltExpr([head])
    for t in token_iter:
        if t == keywords["ALT_LBRA"]:
            head.children.append(
                parse_tokens(token_iter, keywords, close_bracket=keywords["ALT_RBRA"])
            )
        elif t == keywords["OPT_LBRA"]:
            group = parse_tokens(
                token_iter, keywords, close_bracket=keywords["OPT_RBRA"]
            )
            if not isinstance(group, AltExpr):
                group = AltExpr([group])
            group.children.append(ConcatExpr())
            head.children.append(group)
            new_head = ConcatExpr()
            head.children.append(new_head)
            head = new_head
        elif t == close_bracket:
            return res
        elif t in (keywords["ALT_RBRA"], keywords["OPT_RBRA"]):
            if close_bracket != keywords["OPT_RBRA"]:
                raise ValueError("Unmatched closing bracket")
            return res
        elif t == keywords["ALT"]:
            if not isinstance(res, AltExpr):
                res = AltExpr([res])
            head = ConcatExpr()
            res.children.append(head)
        else:
            head.children.append(t)
    if close_bracket:
        raise ValueError("Unmatched opening bracket")
    return res


def parse(string: str, keywords: dict = DEFAULT_KEYWORDS) -> Expr:
    pattern = "(" + "|".join(re.escape(s) for s in keywords.values() if s) + ")"
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


def iterexpand(
    string: str, brackets=("<", ">"), alt="|", optional_brackets=("[", "]")
) -> Generator[str, None, None]:
    """Expand a string that specifies a prompt matrix into a list of
    strings.

    Args:
        string: The string to expand.
        brackets: A pair of strings that delimit the start and end of
            an alternation group.
        alt: The string that separates alternatives in a prompt
        optional_brackets: A pair of strings that delimit the start and end of
            an optional group.

    Returns:
        An iterator of strings.
    """
    brackets = brackets or (None, None)
    if len(brackets) != 2:
        raise ValueError("brackets must be a pair of strings")
    if not brackets[0] or not brackets[1]:
        brackets, alt = (None, None), None
    optional_brackets = optional_brackets or (None, None)
    if len(brackets) != 2:
        raise ValueError("optional_brackets must be a pair of strings")
    if not optional_brackets[0] or not optional_brackets[1]:
        brackets = (None, None)
    keywords = dict(
        ALT_LBRA=brackets[0],
        ALT_RBRA=brackets[1],
        OPT_LBRA=optional_brackets[0],
        OPT_RBRA=optional_brackets[1],
        ALT=alt,
    )
    expr = parse(string, keywords)
    yield from ("".join(words) for words in iter_expr(expr))


def expand(
    string: str, brackets=("<", ">"), alt="|", optional_brackets=("[", "]")
) -> List[str]:
    """Expand a string that specifies a prompt matrix into a list of
    strings.

    Args:
        string: The string to expand.
        brackets: A pair of strings that delimit the start and end of
            an alternation group.
        alt: The string that separates alternatives in a prompt
        optional_brackets: A pair of strings that delimit the start and end of
            an optional group.

    Returns:
        A list of strings.
    """
    return list(iterexpand(string, brackets, alt, optional_brackets))


def choice(
    string: str, brackets=("<", ">"), alt="|", optional_brackets=("[", "]")
) -> str:
    """Return a random expansion of a string that specifies a prompt matrix into
    a list of strings.

    Args:
        string: The string to expand. brackets: A pair of strings that delimit
        the start and end of
            an alternation group.
        alt: The string that separates alternatives in a prompt
        optional_brackets: A pair of strings that delimit the start and end of
            an optional group.

    Returns:
        A string.
    """
    return random.choice(expand(string, brackets, alt, optional_brackets))
