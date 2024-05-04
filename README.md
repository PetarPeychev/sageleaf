# Sageleaf

Sageleaf is a procedural programming language with garbage collection, static
types, null-safety, errors as values, algebraic data types and pattern matching.

---

## Contents
- [Sageleaf](#sageleaf)
  - [Contents](#contents)
  - [To Do](#to-do)
    - [Language](#language)
    - [Tooling](#tooling)
  - [Overview](#overview)
    - [Bindings](#bindings)
    - [Variables](#variables)
    - [Primitive Types](#primitive-types)
    - [Lists](#lists)
    - [Records](#records)
    - [Variants](#variants)
    - [Interfaces](#interfaces)

---

## To Do
Current status of the project:

### Language
- [ ] Core Language Design          ████████░░
- [ ] Lexer & Parser                ░░░░░░░░░░
- [ ] Type checker                  ░░░░░░░░░░
- [ ] AST Interpreter               ██░░░░░░░░
- [ ] Standard Library              ░░░░░░░░░░

### Tooling
- [ ] VSCode Extension (TextMate)   ██████░░░░
- [ ] VSCode Extension (LSP)        ░░░░░░░░░░

---

## Overview
Sageleaf programs are made up of modules. Modules are collections of types, functions and variables colocated in the same file.

Programs have a single entry point, a function `fn main(): ()` which is called when the program is run.

### Bindings
Bindings are used to bind a value to a name in the current scope. They are denoted by the `let` keyword:
- `let x: int = 42;`
- `let y: str = "hello";`

***Note:*** Bindings are immutable, so once a value is bound to a name, it cannot be changed.

### Variables
Mutable variables are similar to bindings, but their values can be changed. They are denoted by the `var` keyword:
```
var x: int = 42;
x = 43;
```
***Note:*** Variables should be used sparingly and module-level variables should be avoided if possible, as mutable state can lead to bugs and make programs harder to reason about.

### Primitive Types
The primitive types built into the language are:
- `i8` - 8-bit signed integer
- `u8` - 8-bit unsigned integer
- `i16` - 16-bit signed integer
- `u16` - 16-bit unsigned integer
- `i32` - 32-bit signed integer
- `u32` - 32-bit unsigned integer
- `i64` - 64-bit signed integer
- `u64` - 64-bit unsigned integer
- `i128` - 128-bit signed integer
- `u128` - 128-bit unsigned integer
- `f32` - 32-bit signed floating point
- `f64` - 64-bit signed floating point
- `bool` - logical boolean (e.g. `true` or `false`)
- `str` - UTF-8 encoded string (e.g. `"sageleaf"`)

### Tuples
Tuples are ordered heterogenous sequences, denoted by `('a, 'b, 'c)` where `'a`, `'b` and `'c` can be any other type:
- `(i32, str, bool)`
- `(str, str)`
- `(str,)`

Tuple values can be constructed through tuple literals:
- `let three: (i32, str, bool) = (1, "hello", true);`
- `let two: (str, str) = ("a", "b");`
- `let one: (str,) = ("hello",);`

***Note:*** The empty tuple `()` has only one possible value, which is also written as `()`. This is the [unit type](https://en.wikipedia.org/wiki/Unit_type) for the language. (equivalent to `None`, `void` or `unit` in other languages) It's used to represent the input or return type of functions which are primarily used for their side effects, such as `fn print(str): ()` or `fn read_line(): str`.

### Lists
Lists are ordered homogenous sequences, denoted by `['a]` where `'a` can be any other type:
- `[int]`
- `[[str]]`

List values can be constructed through list literals:
- `let nums: [int] = [1, 2, 3];`
- `let nested: [[str]] = [["a", "b"], ["c", "d"]];`

### Records
Records are structures made up of named fields. They are declared using the `type` keyword and aredenoted by `{x: 'a, y: 'b}` where `x` and `y` are field names while `'a` and `'b` can be any other type:
- `type color = {red: int, green: int, blue: int};`
- `type person = {name: str, age: int, hobbies: [str]};`

Record values can be constructed through record literals:
- `let purple: color = {red: 128, green: 0, blue: 128};`
- `let robyn: person = {name: "Robyn", age: 21, hobbies: ["programming", "drawing"]};`

***Note:*** Records must be declared before they can be used. Anonymous records can't be used as types. (e.g. `let blue: {red: int, green: int, blue: int} = {red: 0, green: 0, blue: 128};` is not valid syntax)

***Note:*** Records are nominally typed which means that two records with the same field names but different types are not considered equal. To write functions which are polymorphic over different records with the same subset of fields, use an [interface](#interfaces).

### Variants
Variants are [sum types](https://en.wikipedia.org/wiki/Tagged_union) which represent two or more alternative named cases which can optionally contain extra data. They are declared using the `type` keyword and are denoted by `x or 'y(a')` where `a` can be any other type:
- `type PrimaryColor = Red or Blue or Green;`
- `type Result 'a = Ok(a') or Error(str);`
- `type LinkedList 'a = Empty or Node('a, LinkedList('a));`

Variant values can be constructed by using the name of the variant:
- `let red: PrimaryColor = Red;`
- `let output: Result(int) = Error("not found");`
- `let list: LinkedList(int) = Node(34, Node(35, Empty));`

### Interfaces
...
