# Prompt Matrix

A Python package to expand prompt matrix strings, e.g. the string `"The
<dog|cat> in the hat"` expands to the list `["The dog in the hat", "The cat in
the hat"]`.

```python
import prompt_matrix

prompt_matrix.expand("The <dog|cat> in the <cardigan|hat>")
["The dog in the cardigan",
 "The dog in the hat",
 "The cat in the cardigan",
 "The cat in the hat"]

prompt_matrix.expand("The <<small|large> <brown|black> dog|<red|blue> fish>")
["The small brown dog",
 "The small black dog",
 "The large brown dog",
 "The large black dog",
 "The red fish",
 "The blue fish"]

prompt_matrix.expand("The {dog,cat} in the {cardigan,hat}", brackets=['{', '}'], alt=',')
["The dog in the cardigan",
 "The dog in the hat",
 "The cat in the cardigan",
 "The cat in the hat"]
```

## License

MIT
