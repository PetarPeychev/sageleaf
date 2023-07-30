## Primitive Types

The primitive types built into the language are:
- `int` - 64-bit signed integer (e.g. `42`)
- `float` - 64-bit signed floating point (e.g. `3.14`)
- `bool` - logical boolean (e.g. `true` or `false`)
- `str` - UTF-8 encoded string (e.g. `"sageleaf"`)
- `none` - [unit type](https://en.wikipedia.org/wiki/Unit_type) (e.g. `none`, equivalent to `None`, `void`, `()` or `unit` in other languages)

***Note:*** The type `none` has only one possible value, which is also written as `none`. This usually represents the input or return type of functions which are primarily used for their side effects, such as `print: str -> none` or `read_line: none -> str`. Additionally, it can be used to to represent the return type of partial functions, such as `divide: float -> float -> float | none`.