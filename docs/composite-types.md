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
