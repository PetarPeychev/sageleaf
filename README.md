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
    - [Type Aliases](#type-aliases)
    - [Functions](#functions)
    - [Modules and Imports](#modules-and-imports)

---

## To Do

Current status of the project:

### Language

- [ ] Core Language Design ████████░░
- [ ] Lexer & Parser ░░░░░░░░░░
- [ ] Type checker ░░░░░░░░░░
- [ ] AST Interpreter ██░░░░░░░░
- [ ] Standard Library ░░░░░░░░░░

### Tooling

- [ ] VSCode Extension (TextMate) ██████░░░░
- [ ] VSCode Extension (LSP) ░░░░░░░░░░

---

## Overview

Sageleaf programs are made up of modules. Modules are collections of types, functions and variables colocated in the same file.

Programs have a single entry point, a function `main()` which is called when the program is run.

### Bindings

Bindings are used to bind a value to a name in the current scope. They are denoted by the `let` keyword:

- `let x: i32 = 42;`
- `let y: str = "hello";`

**_Note:_** Bindings are immutable, so once a value is bound to a name, it cannot be changed.

### Variables

Mutable variables are similar to bindings, but their values can be changed. They are denoted by the `var` keyword:

```
var x: i32 = 42;
x = 43;
```

**_Note:_** Variables should be used sparingly and module-level variables should be avoided if possible, as mutable state can lead to bugs and make programs harder to reason about.

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

**_Note:_** The empty tuple `()` has only one possible value, which is also written as `()`. This is the [unit type](https://en.wikipedia.org/wiki/Unit_type) for the language. (equivalent to `None`, `void` or `unit` in other languages) It's used to represent the input or return type of functions which are primarily used for their side effects, such as `print(str): ()` or `read_line(): str`.

### Lists

Lists are ordered homogenous sequences, denoted by `['a]` where `'a` can be any other type:

- `[i32]`
- `[[str]]`

List values can be constructed through list literals:

- `let nums: [i32] = [1, 2, 3];`
- `let nested: [[str]] = [["a", "b"], ["c", "d"]];`

### Records

Records are structures made up of named fields. They are declared using the `type` keyword and aredenoted by `{x: 'a, y: 'b}` where `x` and `y` are field names while `'a` and `'b` can be any other type:

- `type color = {red: i8, green: i8, blue: i8};`
- `type person = {name: str, age: i32, hobbies: [str]};`

Record values can be constructed through record literals:

- `let purple: color = {red: 128, green: 0, blue: 128};`
- `let robyn: person = {name: "Robyn", age: 21, hobbies: ["programming", "drawing"]};`

**_Note:_** Records must be declared before they can be used. Anonymous records can't be used as types. (e.g. `let blue: {red: i8, green: i8, blue: i8} = {red: 0, green: 0, blue: 128};` is not valid syntax)

**_Note:_** Records are nominally typed which means that two records with the same field names but different types are not considered equal. To write functions which are polymorphic over different records with the same subset of fields, use an [interface](#interfaces).

### Variants

Variants are [sum types](https://en.wikipedia.org/wiki/Tagged_union) which represent two or more alternative named cases which can optionally contain extra data. They are declared using the `type` keyword and are denoted by `x or 'y(a')` where `a` can be any other type:

- `type PrimaryColor = Red or Blue or Green;`
- `type Result('a) = Ok('a) or Error(str);`
- `type LinkedList 'a = Empty or Node('a, LinkedList('a));`

Variant values can be constructed by using the name of the variant:

- `let red: PrimaryColor = Red;`
- `let output: Result(i32) = Error("not found");`
- `let list: LinkedList(i32) = Node(34, Node(35, Empty));`

### Interfaces

Interfaces are used to define a subset of a record type which can be used as
an input for a polymorphic function. They are declared using the `interface`
keyword and are denoted by `interface name = {field: 'a, field: 'b};` where
`'a` and `'b` are the names of the fields in the interface:

```
interface Person = {name: str, age: i32};

# Employee satisfies the Person interface
type Employee = {name: str, age: i32, salary: i32};

print_person(person: Person) {
    print("Name: " + person.name);
    print("Age: " + person.age);
}

main() {
    let employee: Employee = {name: "John Doe", age: 42, salary: 100000};

    # since Employee satisfies the Person interface, we can pass it to print_person
    print_person(employee);
}
```

### Type Aliases

Type aliases are used to create new names for existing types. They are declared using the `type` keyword and are denoted by `type name = 'a;` where `'a` is the name of the type to alias:

- `type Age = i32; let age: Age = 42;`
- `type Name = str; let name: Name = "John Doe";`

Type aliases can be used to specialize a generic type:

- `type IntList = [i32]; let list: IntList = [1, 2, 3];`
- `type StrResult = Result(str); let result: StrResult = Ok("hello");`

### Functions

Functions are declared using the `name(x: 'a, y: 'b): 'c` syntax where `'a` and
`'b` are the types of the function's arguments and `c` is the type of the
function's return value:

```
add(a: i32, b: i32): i32 {
    let sum: i32 = a + b;
    return sum;
}
```

The return type can optionally be omitted as syntactic sugar for returning the
unit type`: ()`:

```
say_hello(name: str) {
    print("Hello, " + name + "!");
}
```

Functions can be called by using the name of the function:

- `let result: i32 = add(1, 2);`
- `print("hello");`

Anonymous functions can be created using the `fn` keyword:

```
filter(list: ['a], predicate: ('a) -> bool) -> ['a] {
    var result: ['a] = [];
    for x in list {
        if predicate(x) {
            result.append(x);
        }
    }
    return result;
}

main() {
    let list: [i32] = [1, 2, 3, 4, 5];

    # filter out all even numbers
    let even: [i32] = filter(list, (x) { return x % 2 == 0; });
}
```

### Modules

Each sageleaf file is a module. Other modules or their members can be imported
into the current module using the `import` keyword:

```
import {
    math,
    pprint from string
}
```

When importing a module, the exported members of the module are made available
under a namespace of the same name:

```
let pi: f64 = math.pi;
```

When importing specific members of a module with the `from` keyword, the
imported members are added to the current module's namespace:

```
let john: Employee = {name: "John Doe", age: 42, salary: 100000};
pprint(john);
```

By default, modules don't export any members. To export a member, use the
`export` keyword:

```
export {
    Employee,
    print_person
}
```

**_Note:_** There can only be one `import` statement and one `export` statement
in a module. It's recommended to keep these statements at the top of the file
to have a clear definition of the module's interface.

Directories can be used to organize modules. Modules can be imported from
subdirectories using the `subdir.module` syntax:

```
import {
    ds.hashmap,
    filter from ds.list
}
```

To resolve name conflicts or shorten names, imports can be aliased using the
`as` keyword:

```
import {
    very.long.module_name as mod,
    very_long_function_name from module as func
}
```
