# Prompt Matrix

[![Python](https://img.shields.io/pypi/pyversions/prompt-matrix.svg?style=plastic)](https://badge.fury.io/py/prompt-matrix)
[![PyPI](https://badge.fury.io/py/prompt-matrix.svg)](https://badge.fury.io/py/prompt-matrix)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package to expand prompt matrix strings. For example, the string `"The
<dog|cat> in the hat"` expands to the list `["The dog in the hat", "The cat in
the hat"]`.

The motivating case for this package is to compare the effects of different
prompts in text and image generation systems such as Stable Diffusion and GPT-3.

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

The special characters `<>{}|` can be replaced by different strings, or disabled
by specifying
`None` or the empty string.

> **Note**: The disjunction is bounded by the enclosing brackets, if any. `"The
dog|cat in the cardigan|hat"` generates the three strings `"The dog"`, `"cat in
the gardigan"`, and `"hat"`. This is in contrast to some other systems, that
scope a disjunction to the text delimited by surrounding whitespace.

## Install

```shell
$ pip install prompt-matrix
```

## Usage

Prompt Matrix provides two functions for expanding a prompt matrix:
`expand` and `iterexpand`. Both take a string that specifies
a prompt matrix.

**`expand`** returns an array of strings with all possible combinations of the
prompt matrix elements.

```python
import prompt_matrix

prompt = "<hi|hello> <there|you>"
expansion = prompt_matrix.expand(prompt)
print(expansion) # ["hi there", "hi you", "hello there", "hello you"]
```

**`iterexpand`** returns a generator that yields the expansions one by
one.

```python
import prompt_matrix

prompt = "<hi|hello> <there|you>"
for expansion in prompt_matrix.iterexpand(prompt):
  print(expansion) # "hi there", "hi you", "hello there", "hello you"
```

### Examples

Example 1: Basic usage

```python
import prompt_matrix

prompt_matrix.expand("The <dog|cat> in the hat")
# ->
# ["The dog in the hat",
#  "The cat in the hat"]
```

Example 2: Using multiple alternations

```python
prompt_matrix.expand("The <dog|cat> in the <cardigan|hat>")
# ->
# ["The dog in the cardigan",
#  "The dog in the hat",
#  "The cat in the cardigan",
#  "The cat in the hat"]
```

Example 3: Using nested brackets

```python
prompt_matrix.expand("The <<small|large> <brown|black> dog|<red|blue> fish>")
# ->
# ["The small brown dog",
#  "The small black dog",
#  "The large brown dog",
#  "The large black dog",
#  "The red fish",
#  "The blue fish"]
```

Example 4: Using custom brackets and separator

```python
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
