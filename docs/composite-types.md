## Composite Types

In order to express more complex data structures, [primitive types](./primitive-types.md) can be combined into a variety of composite types i.e. collections.

### Lists
Lists are ordered homogenous sequences, denoted by `[a]` where `a` can be any other type:
- `[int]`
- `[[str]]`

List values can be constructed through list literals:
- `[1, 2, 3]`
- `[["a", "b"], ["c", "d"]]`

---

### Tuples
Tuples are ordered heterogenous sequences, denoted by `(a, b, c, ...)`, where `a`, `b` and `c` can be any other type:
- `(int, int)`
- `(str, str, [int])`

Tuple values can be constructed through tuple literals:
- `(12, 34)`
- `("cat", "meow", [1, 2, 3])`

---

### Records
Records are unordered sets of elements, where each element has an associated name. They are denoted by `(x: a, y: b)` where `x` and `y` are names while `a` and `b` can be any other type:
- `(red: int, green: int, blue: int)`
- `(name: str, age: int, hobbies: [str])`

Record values can be constructed through record literals:
- `(red: 128, green: 0, blue: 50)`
- `(name: "Robyn", age: 21, hobbies: ["programming", "pretending to be a cat"])`

---

### Unions
Unions are [sum types](https://en.wikipedia.org/wiki/Tagged_union) which represent two or more alternative cases for the values they can hold. They can either be tagged or untagged.

**Tagged unions** have an explicit name for each possible case and are denoted by `x: a | y: b` where `x` and `y` are names while `a` and `b` can be any other type:
- `result: float | error: str`
- `node: (int, int) | leaf: none`

Tagged union values can be constructed by using the associated name:
- `error: "division by zero"`
- `node: (3, 4)`

**Untagged unions** can be thought of as a special case of tagged unions, where each case is implicitly tagged by the type of its value. They are denoted by `a | b` where `a` and `b` can be any other type:
- `int | str`
- `int | float | none`

There is no special syntax for constructing values of untagged unions, as all types which compose the union can be though of as subtypes of it:
- `"hello"`
- `none`

