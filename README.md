# Sageleaf

Sageleaf is a static structurally-typed functional programming language with a "batteries-included" tooling approach. It's currently in the design phase, so this repository is mostly a collection of ideas and notes.

---

## Contents
- [Sageleaf](#sageleaf)
  - [Contents](#contents)
  - [To Do](#to-do)
    - [Language](#language)
    - [Tooling](#tooling)
  - [Program Structure](#program-structure)
  - [Bindings](#bindings)
  - [Type Aliases](#type-aliases)
  - [Imports](#imports)
  - [Primitive Types](#primitive-types)
  - [Composite Types](#composite-types)
    - [Lists](#lists)
    - [Records](#records)
    - [Unions](#unions)
  - [Expressions](#expressions)

---

## To Do
Current status of the project:

### Language
- [ ] Core Language Design          █████░░░░░
- [ ] Lexer & Parser                ░░░░░░░░░░
- [ ] Type checker                  ░░░░░░░░░░
- [ ] AST Interpreter               ██░░░░░░░░
- [ ] Standard Library              ░░░░░░░░░░

### Tooling
- [ ] VSCode Extension (TextMate)   ░░░░░░░░░░
- [ ] VSCode Extension (LSP)        ░░░░░░░░░░

---

## Program Structure
...

---

## Bindings
...

---

## Type Aliases
...

---

## Imports
...

---

## Primitive Types
The primitive types built into the language are:
- `int` - 64-bit signed integer (e.g. `42`)
- `float` - 64-bit signed floating point (e.g. `3.14`)
- `bool` - logical boolean (e.g. `true` or `false`)
- `str` - UTF-8 encoded string (e.g. `"sageleaf"`)
- `none` - [unit type](https://en.wikipedia.org/wiki/Unit_type) (e.g. `none`, equivalent to `None`, `void`, `()` or `unit` in other languages)

***Note:*** The type `none` has only one possible value, which is also written as `none`. This usually represents the input or return type of functions which are primarily used for their side effects, such as `print: str -> none` or `read_line: none -> str`. Additionally, it can be used to to represent the return type of partial functions, such as `divide: float -> float -> float | none`.

---

## Composite Types
In order to express more complex data structures, [primitive types](./primitive-types.md) can be combined into a variety of composite types i.e. collections.

### Lists
Lists are ordered homogenous sequences, denoted by `[a]` where `a` can be any other type:
- `[int]`
- `[[str]]`

List values can be constructed through list literals:
- `[1, 2, 3]`
- `[["a", "b"], ["c", "d"]]`

### Records
Records are unordered sets of elements, where each element has an associated name. They are denoted by `{x: a, y: b}` where `x` and `y` are names while `a` and `b` can be any other type:
- `{red: int, green: int, blue: int}`
- `{name: str, age: int, hobbies: [str]}`

Record values can be constructed through record literals:
- `{red: 128, green: 0, blue: 50}`
- `{name: "Robyn", age: 21, hobbies: ["programming", "pretending to be a cat"]}`

### Unions
Unions are [sum types](https://en.wikipedia.org/wiki/Tagged_union) which represent two or more alternative cases for the values they can hold. They are denoted by `a or b` where `a` and `b` can be any other type:
- `int or str`
- `int or {name: str} or none`

There is no special syntax for constructing values of untagged unions, as all types which compose the union are subtypes of it:
- `"hello"`
- `{name: "Robyn"}`

---

## Expressions
...
