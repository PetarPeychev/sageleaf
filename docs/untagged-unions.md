## Untagged Unions

While it's possible to use an algebraic data type to express optional values

```
type Maybe a =
    | Just a
    | Nothing
```

or to explicitly define alternatives

```
type Either a b =
    | Left a
    | Right b
```

we believe they [aren't the best general solution](https://www.youtube.com/watch?v=YR5WdGrpoug).

Suppose we implement a simple print function, which outputs a string to the console

```
let print: str -> none =
    ...
```

and then we use it throughout our program like `print "Hello, World!"`. At some point down the line however, we decide to extend this function to also be able to print integers. If we use an Either type to achieve this like

```
let print: Either str int -> none =
    ...
```

then we have introduced a breaking change to every caller of `print`. No bueno! Instead, in sageleaf we can use an untagged union

```
let print: str | int -> none =
    input ->
        match input
        | str s => ...
        | int i => ...
```

and now all previous users of `print "Hello, World!"` are happy and we now also support `print 42`.

A common use case for untagged unions is to represent partial functions by returning the `none` type.

```
let divide: float -> float -> float | none =
    x -> y ->
        if y is 0
        then none
        else x / y
```

And to work with functions like these, we simply need to pattern match and handle both cases

```
    match divide x y
    | float f => ...
    | none n => ...
```