# Sageleaf
Sageleaf is a statically-typed garbage-collected programming language which compiles to readable C99 code. It makes C interop easy by allowing escape hatches to drop down to native C code, similarly to how inline assembly works in other languages.

The language makes pragmatic performance-usability trade-offs by codifying common C patterns such as dynamic arrays, hashmaps, hash sets, tagged unions, length-based strings, non-nullable pointers, bounds checking, runtime type information, etc.

- [Sageleaf](#sageleaf)
  - [Program Structure](#program-structure)
  - [Literals](#literals)
    - [Comments](#comments)
    - [String Literals](#string-literals)
    - [Integer Literals](#integer-literals)
    - [Floating Point Literals](#floating-point-literals)
    - [Native Blocks (C Literals)](#native-blocks-c-literals)
  - [Imports](#imports)
  - [Primitive Types](#primitive-types)
  - [Pointers](#pointers)
  - [Composite Types](#composite-types)
    - [Lists](#lists)
    - [Structs](#structs)
    - [Unions](#unions)
    - [Maps](#maps)
    - [Sets](#sets)
  - [Functions](#functions)
    - [Function Overloading](#function-overloading)
    - [Method Syntax](#method-syntax)
  - [Variables](#variables)
    - [Assignment](#assignment)
  - [Constants](#constants)
  - [Operators](#operators)
    - [Arithmetic Operators](#arithmetic-operators)
    - [Comparison Operators](#comparison-operators)
    - [Logical Operators](#logical-operators)
    - [Pointer Operators](#pointer-operators)
  - [Control Flow](#control-flow)
    - [While Loop](#while-loop)
    - [For Loop](#for-loop)
    - [Break](#break)
    - [Continue](#continue)
    - [If Statement](#if-statement)
    - [Pattern Matching](#pattern-matching)
  - [Error Handling](#error-handling)
  - [Generics](#generics)
  - [Internals](#internals)
    - [Garbage Collection](#garbage-collection)
    - [Name Mangling](#name-mangling)
    - [Signed Integer Overflow](#signed-integer-overflow)
    - [Implicit Type Conversion](#implicit-type-conversion)
    - [Escape Analysis](#escape-analysis)

## Program Structure
Sageleaf programs are composed of imports, types, functions and native blocks, organized into packages.

Packages are directories of Sageleaf files. 

Package names are the same as the directory names. Package directory names must be all lowercase Latin alphanumeric characters or underscores, beginning with a letter (`[a-z][a-z0-9_]*`) e.g. `math`, `http_requests`, `sqlite3`. Code files are the same with the addition of the `.sl` extension.

If a package contains a `main` function, it can be compiled to an executable. Otherwise, it can either be imported by an executable package or compiled independently as a shared library. (`.so`, `.dll`, `.dylib`, etc.)

## Literals

### Comments
Sageleaf only supports single-line comments.
```
// a comment
```

### String Literals
String literals are wrapped in double quotes and may contain escape sequences starting with `\`.
```
"hello, world!\n"
```

Escape sequences:
- `\a` - Alert
- `\b` - Backspace
- `\e` - Escape
- `\f` - Formfeed Page Break
- `\n` - Newline
- `\r` - Carriage Return
- `\t` - Horizontal Tab
- `\v` - Vertical Tab
- `\\` - Backslash
- `\"` - Double Quote
- `\NNN` - Octal 6 bit character (3 digits)
- `\xNN` - Hexadecimal 8 bit character (2 digits)
- `\uNNNN` - Hexadecimal 16 bit Unicode character UTF-8 encoded (4 digits)
- `\UNNNNNNNN` - Hexadecimal 32 bit Unicode character UTF-8 encoded (8 digits)

### Integer Literals
Integer literals can be either `0`, any string of digits not starting with `0` or a hexadecimal number starting with `0x`.
```
0
10978
0x1F
```

### Floating Point Literals
Floating point literals cam be written either normally with a `.` or in scientific notation.
```
123.45
1.2345e2
```

### Native Blocks (C Literals)
Since Sageleaf compiles to C99 code, it's possible to directly insert C code into the compiled program via a native block. Sageleaf treats the content of the native blocks as a literal value and doesn't check it for errors.
```
native {
    #include <stdio.h>
}

fn println(s: str) {
    native {
        printf("%s\n", s.data);
    }
}
```

It's recommended to limit usage of native blocks to wrapping C libraries as they can be a source of subtle bugs and very difficult to debug.

Local variables and function arguments will be available in the native C code as-is, however top-level definitions will have their names mangled by the compiler so they must be referenced by their mangled names.

## Imports
Import statements bring in definitions from another package into the current namespace.
```
import os
```
By default, names from the imported package are prefixed with the package name e.g. `os.read_file()`.

To directly import names without the package prefix, import them by name.
```
import read_file, write_file from os
```

Or to shorten an import package prefix, add an alias.
```
import raylib as rl
```

## Primitive Types
- `i8` - 8 bit signed integer.
- `i16` - 16 bit signed integer.
- `i32` - 32 bit signed integer.
- `i64` - 64 bit signed integer.
- `u8` - 8 bit unsigned integer.
- `u16` - 16 bit unsigned integer.
- `u32` - 32 bit unsigned integer.
- `u64` - 64 bit unsigned integer.
- `usize` - Pointer-sized unsigned integer.
- `f32` - 32 bit floating point number.
- `f64` - 64 bit floating point number.
- `bool` - `true` or `false`, 1 byte representation
- `str` - UTF-8 string of u8 characters with a `usize` length.

## Pointers
Pointers can be stored to any primitive or composite type, however pointer arithmetic is disallowed. Pure sageleaf will never allow null or invalid pointers unless raw C is used in native blocks to create them.
```
age: u8 = 35;
age_ptr: *u8 = &age;
*age_ptr = 24;

// age = 24;
```

## Composite Types
### Lists
Heap-allocated homogenous dynamic array with a length (`usize`) and bounds checking.

```
list: List i32 = [1, 2, 3];
```

### Structs
Stack-allocated group of variables in contiguous memory. Maps 1-to-1 to C structs.

```
struct Point {
    x: i32,
    y: i32
}
```

### Unions
Stack-allocated tagged union with optional payloads. Internal representation is a 32-bit int tag and C union of payloads.

```
union HTTPResponse {
    Forbidden,
    NotFound,
    Ok: str
}
```

### Maps
Heap-allocated hashmap.

```
capitals: Map str str = {
    "Norway": "Oslo",
    "Bulgaria": "Sofia",
    "Italy": "Rome"
};
```

### Sets
Heap-allocated hashset.

```
countries: Set str = {
    "Norway",
    "Bulgaria",
    "Italy"
}
```

## Functions
Sageleaf functions map directly to C functions.
```
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}
```

Executable packages must define a main function which takes no arguments and doesn't return a value.
```
fn main() {
    print("Hello, world!");
}
```

### Function Overloading
Multiple functions with the same name but different argument lists can be defined. They are disambiguated at the call site based on the types being passed to them.
```
fn add(a: i32, b: i32) -> i32 {return a + b;}
fn add(a: u64, b: u64) -> u64 {return a + b;}
```

### Method Syntax
Method syntax is available as syntactic sugar for any function taking more than one argument. Automatic pointer dereferencing is done on method calls.
```
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}

x: i32 = 42;
y: i32 = 12;
x_ptr: *i32 = &x;

x.add(y); // 54
x_ptr.add(y); // 54
```

## Variables
Variables are always given an initial value when declared and are visible in the current scope.
```
answer: i32 = 42;
```

**Note:** Re-declaring variables with the same name in the same scope is not allowed.

### Assignment
Variables can be assigned different values of the same type.
```
answer = 12;
```

## Constants
Constants are similar to variables, but their values are immutable and can't be reassigned. Any reference types however may have their data modified. (e.g. lists, maps, sets, pointers)
```
const pi: f32 = 3.14;
```

## Operators

### Arithmetic Operators
- `+` - Addition of numbers, concatenation of strings and lists, union of sets and maps.
- `-` - Subtraction of numbers or sets.
- `*` - Multiplication of numbers.
- `/` - Division of numbers.
- `%` - Modulo (integer division remainder).

### Comparison Operators
- `==` - Value equality for any type.
- `!=` - Inverse of `==`.
- `>` - Greater than for numbers, lexicographical comparison for strings and lists, strict superset for sets.
- `<` - Less than for numbers, lexicographical comparison for strings and lists, strict subset for sets.
- `>=` - Greater than or equal for numbers, lexicographical comparison for strings and lists, superset for sets.
- `<=` - Less than or equal for numbers, lexicographical comparison for strings and lists, subset for sets.

### Logical Operators
- `not` - Logical negation for bools. 
- `and` - Logical `and` for bools.
- `or` - Logical `or` for bools.

### Pointer Operators
- `&` - Create a pointer by getting the address of a variable.
- `*` - Follow a pointer to the value it points to.

**Note:** Pointers in pure Sageleaf can never be null due to lack of pointer arithmetic, however it's possible to create null pointers via raw C in native blocks.

## Control Flow

### While Loop
While loops repeat a block of code while the condition after the while evaluates to `true`.
```
while x > 5 {
    x = x - 1;
}
```

### For Loop
For loops can be used to iterate over ranges of numbers. The range operators `..=` and `..<` stand for inclusive or exclusive range.
```
for i: i32 in 0..=5 {
    // 0, 1, 2, 3, 4, 5
}

for i: i32 in 0..<6 {
    // 0, 1, 2, 3, 4, 5
}

for i: i32 in 5..=0 {
    // 5, 4, 3, 2, 1, 0
}
```

For loops can also be used to iterate over lists, strings, maps and sets.
```
list: List i32 = [1, 2, 3, 4, 5];

for element in list {
    // 1, 2, 3, 4, 5
}

for element, index in list {
    // 1 0, 2 1, 3 2, 4 3, 5 4
}

for i: usize in len(list)-1 ..= 0 {
    // 4, 3, 2, 1, 0
}

for c in "hello" {
    // "h", "e", "l", "l", "o"
}

capitals: Map str str = {
    "Norway": "Oslo",
    "Bulgaria": "Sofia",
    "Italy": "Rome"
};

for key, value in capitals {
    // "Norway" "Oslo", "Bulgaria" "Sofia", "Italy" "Rome"
}

colors: Set str = {"red", "green", "blue"};

for element in colors {
    // "red", "green", "blue"
}
```

### Break
The `break;` statement can be used to end a loop early.
```
while true {
    break;
}
```

### Continue
The `continue;` statement ends the current loop iteration and continues to the next one.
```
for i: i32 in 0..=4 {
    if i == 3 {
        continue;
    }
    // 0, 1, 2, 4
}
```

### If Statement
The `if-elif-else` statement is is used to branch based on conditions. It always requires `{}`.
```
if x > 5 {
    ...
}

if x > 0 {
    ...
}
elif x == 0 {
    ...
}
else {
    // x < 0
}
```

### Pattern Matching
Pattern matching is used mainly with unions and lists, however it can also be used like a switch statement to match primitive types by value.
```
status_code: u8 = ...

match status_code {
    case 200: print("OK");
    case 404: print("Not Found");
    case 500..=599: print("Server Error");
    case _: print("Other");
}

union Color {
    rgb: struct{red: u8, green: u8, blue: u8},
    hsv: struct{hue: u16, saturation: u8, value: u8}
}

color: Color = ...

// If you use guards (case ... if ...) you need a catch-all case (case _) since 
// guards can't be checked for exhaustiveness at compile time.
match color {
    case .rgb{r, g, b} if r==g and g==b: 
        print("grayscale");
    case .rgb{255, 0, 0}:
        print("red");
    case .rgb{red: 0, green: 255, blue: 0}:
        print("green");
    case .rgb{0, 0, 255}:
        print("blue");
    case .hsv{_, _, _}:
        print("hsv");
    case _:
        print("other");
}

radii: List i32 = ...

match radii {
    case []:
        print("no radii");
    case [first, ..rest] if first==0:
        print("12 o'clock");
    case [rest.., last] if last==270:
        print("9 o'clock");
    case [first, ..middle.., last] if first==last:
        print("same start and end");
    case [0, 90, 180, 270]:
        print("straight angles");
    case _:
        print("something else");
}
```

## Error Handling
Error states in Sageleaf are considered normal states, part of the logic of the program, and are therefore treated as any other state. Functions which may fail should return a union of possible states.
```
fn find(list: List i32, element: i32) -> union {index: usize, not_found} {
    for e, i in list {
        if e == element {
            return .index{i};
        }
    }
    return .not_found;
}

list: List i32 = [1, 2, 3, 4, 5];

match find(list, 3) {
    case .index{i}: print(i);
    case .not_found: print("Not found");
}
```

## Generics
Generics are ways to parameterize composite types or functions based on types. Single quote `'` is used to declare a type parameter which is then used throughout the definition. Type parameters only need to be declared once in a generic definition.
```
union Either 'L 'R {
    left: L,
    right: R
}

struct Vec3 'T {
    x: T,
    y: T,
    z: T
}

fn add(v1: Vec3 'T, v2: Vec3 T) -> Vec3 T {
    res: Vec3 T = {
        v1.x + v2.x,
        v1.y + v2.y,
        v1.z + v2.z
    };
    return res;
}

fn main() {
    ok: Either i32 str = 42;
    err: Either i32 str = "Something went wrong";
}
```

Under the hood, Sageleaf will generate a copy of the generic type/function, specialised for each usage with different types. Type checking is performed after monomorphization so type errors can be caught based on the concrete types used in the generated code.

## Internals

### Garbage Collection
Sageleaf uses a mark-and-sweep garbage collector. The garbage collector only works with variables defined outside of native blocks and trusts the user not to shoot themselves in the foot by, for example, manually freeing an allocation inside a native block and causing a double-free. 

### Name Mangling
Since C doesn't have namespaces or packages, Sageleaf has to mangle names to prevent conflicts. The standard naming scheme is `sl_<package_prefix>_<name>`. Package prefix is optional and follows the same scheme as package prefixes in the language.

Monomorphized generic types and functions are also affixed with their type parameters e.g. `sl_Vec3_i32`, `sl_Either_Vec3_i32_str`.

### Signed Integer Overflow
To ensure wrapping for signed integer math, signed integers are always cast to their unsigned variants and back on every math operation. Division and modulo need special handling for the INT_MIN / -1 case to ensure wrapping, so they incur an extra cost.

### Implicit Type Conversion
C will liberally convert types which can hide bugs. To prevent this, explicit casts are required to ensure well-defined behaviour.

### Escape Analysis
Since Sageleaf allows getting the address of a stack-allocated variable like an `i32`, it performs escape analysis to ensure references don't live past the stack frame. If there is a possibility they could be referenced after the scope in which they were allocated, they are converted to a heap allocation and tracked by the GC.
