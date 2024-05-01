# Structs

```fsharp
struct Person {
    name: str*
    age: u32
}
```

```c
typedef struct {
    char *name;
    uint32_t age;
} Person;
```

-------------------------------------------------------
# Enums

```fsharp
enum Color {
    RED
    GREEN
    BLUE
}

Color.RED
```

```c
typedef enum {
    Color_RED,
    Color_GREEN,
    Color_BLUE
} Color;

Color_RED
```

-------------------------------------------------------
# Tagged Unions

union

