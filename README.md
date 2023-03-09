# Prompt Matrix

[![Python](https://img.shields.io/pypi/pyversions/prompt-matrix.svg?style=plastic)](https://badge.fury.io/py/prompt-matrix)
[![PyPI](https://badge.fury.io/py/prompt-matrix.svg)](https://badge.fury.io/py/prompt-matrix)

A Python package to expand prompt matrix strings, *e.g.* the string `"The
<dog|cat> in the hat"` expands to the list `["The dog in the hat", "The cat in
the hat"]`.

The motivating use case for this package is the comparison of different prompts
in text and image generation systems such as Stable Diffusion and GPT-3.

## Features

A prompt string may contain multiple alternations. For example, `"The <dog|cat>
in the <cardigan|hat>"` produces a list of the four strings `"The dog in the
cardigan"`, `"The dog in the hat"`, `"The cat in the cardigan"`, and `"The cat
in the hat"`.

A prompt string may contain nested alternations. For example, `"The
<<small|large> dog|cat>"` produces the strings `"The small dog"`, `"The large
do"`, and `"The cat"`.

Brackets `[]` enclose optional elements. For example, `"The [small] cat"` is
equivalent to `"The <small,> cat"`, and both produce the strings `"The small
cat"` and `"The  cat"`.

The special characters `<>{}|` can be replaced strings, or disabled by specifying
`None` or the empty string.

> **Note**: The disjunction is bounded by the enclosing brackets, if any. `"The
dog|cat in the cardigan|hat"` generates the three strings `"The dog"`, `"cat in
the gardigan"`, and `"hat"`. This is in constrat to some other systems, that
scope a disjunction to the text delimited by surrounding whitespace.

## Install

```shell
$ pip install prompt-matrix
```

## Usage

```python
import prompt_matrix

prompt_matrix.expand("The <dog|cat> in the hat")
# ->
# ["The dog in the hat",
#  "The cat in the hat"]

prompt_matrix.expand("The <dog|cat> in the <cardigan|hat>")
# ->
# ["The dog in the cardigan",
#  "The dog in the hat",
#  "The cat in the cardigan",
#  "The cat in the hat"]

prompt_matrix.expand("The <<small|large> <brown|black> dog|<red|blue> fish>")
# ->
# ["The small brown dog",
#  "The small black dog",
#  "The large brown dog",
#  "The large black dog",
#  "The red fish",
#  "The blue fish"]

prompt_matrix.expand("The {dog,cat} in the {cardigan,hat}",
                     brackets=['{', '}'], alt=',')
# ->
# ["The dog in the cardigan",
#  "The dog in the hat",
#  "The cat in the cardigan",
#  "The cat in the hat"]
```

## License

MIT
