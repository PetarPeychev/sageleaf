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

---

## Code Examples

**Parsing JSON**

Imagine we want to parse and work with a json file, containing a list of employees:

```json
[
    {
        "name": "John Doe",
        "role": "Java Developer",
        "salary": 40000,
        "permanent": false
    },
    {
        "name": "Mary Sue",
        "role": "Sageleaf Developer",
        "salary": 450000,
        "permanent": true
    }
]
```

We can model the structure of an employee in our data using a record:

```fsharp
type employee = (
    name: str,
    role: str,
    salary: int,
    permanent: bool
)
```

And then we can create values of this type:

```fsharp
let john: employee = (
    name: "John Doe",
    role: "Java Developer",
    salary: 40000,
    permanent: false
)

let mary: employee = (
    name: "Mary Sue",
    role: "Sageleaf Developer",
    salary: 450000,
    permanent: true
)
```

And we would probably also implement a parsing function to parse a json string into a list of employees:

```fsharp
let parse_employees: str -> [employee] =
    ...
```

Then we can write a function which matches on a subset of this data:

```fsharp
let say_hello: (name: str) -> none =
    with_name ->
        print ("Hello, " + name + "!")

say_hello mary // Hello, Mary Sue!
```

And since this function is in essence polymorphic over the rest of the record structure, we can pass other types into it which also have a name:

```fsharp
let obie: (name: str, age: int, color: str) = (
    name: "Obie", age: 7, color: "orange"
)

say_hello obie // Hello, Obie!
```