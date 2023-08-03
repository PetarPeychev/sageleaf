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

### Records
Records are unordered sets of elements, where each element has an associated name. They are denoted by `{x: a, y: b}` where `x` and `y` are names while `a` and `b` can be any other type:
- `{red: int, green: int, blue: int}`
- `{name: str, age: int, hobbies: [str]}`

Record values can be constructed through record literals:
- `{red: 128, green: 0, blue: 50}`
- `{name: "Robyn", age: 21, hobbies: ["programming", "pretending to be a cat"]}`

---

### Unions
Unions are [sum types](https://en.wikipedia.org/wiki/Tagged_union) which represent two or more alternative cases for the values they can hold. They are denoted by `a or b` where `a` and `b` can be any other type:
- `int or str`
- `int or {name: str} or none`

There is no special syntax for constructing values of untagged unions, as all types which compose the union are subtypes of it:
- `"hello"`
- `{name: "Robyn"}`

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

```
type employee = {
    name: str,
    role: str,
    salary: int,
    permanent: bool
}
```

And then we can create values of this type:

```
let john: employee = {
    name: "John Doe",
    role: "Java Developer",
    salary: 40000,
    permanent: false
}

let mary: employee = (
    name: "Mary Sue",
    role: "Sageleaf Developer",
    salary: 450000,
    permanent: true
)
```

And we would probably also implement a parsing function to parse a json string into a list of employees:

```
let parse_employees: str -> [employee] =
    ...
```

Then we can write a function which matches on a subset of this data:

```
let say_hello: {name: str} -> none =
    named ->
        print ("Hello, " + named.name + "!")

say_hello mary # Hello, Mary Sue!
```

And since this function is in essence polymorphic over the rest of the record structure, we can pass other types into it which also have a name:

```
let obie: {name: str, age: int, color: str} = {
    name: "Obie", age: 7, color: "orange"
}

say_hello obie # Hello, Obie!
```
