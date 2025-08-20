import os
import read_file, write_file from io
import math as m

native {
    #include <stdio.h>
    #include <stdlib.h>
}

struct Point 'T {
    x: T,
    y: T
}

struct Vector3 {
    x: f32,
    y: f32,
    z: f32
}

union Result 'T 'E {
    ok: T,
    error: E
}

union Color {
    rgb: struct{red: u8, green: u8, blue: u8},
    hsv: struct{hue: u16, saturation: u8, value: u8},
    named: str
}

const PI: f32 = 3.14159;
const MAX_SIZE: usize = 1024;

fn add(a: i32, b: i32) -> i32 {
    return a + b;
}

fn add_vec3(v1: Vector3, v2: Vector3) -> Vector3 {
    result: Vector3 = {
        x: v1.x + v2.x,
        y: v1.y + v2.y,
        z: v1.z + v2.z
    };
    return result;
}

fn find_max 'T (list: List T) -> union {value: T, empty} {
    if len(list) == 0 {
        return .empty;
    }
    
    max_val: T = list[0];
    for element in list {
        if element > max_val {
            max_val = element;
        }
    }
    
    return .value{max_val};
}

fn process_numbers() {
    numbers: List i32 = [1, 2, 3, 4, 5];
    sum: i32 = 0;
    
    for num, idx in numbers {
        sum = sum + num;
        
        if num == 3 {
            continue;
        }
        
        if num > 4 {
            break;
        }
    }
    
    for i: i32 in 0..=10 {
        if i % 2 == 0 {
            sum = sum + i;
        }
    }
    
    while sum > 100 {
        sum = sum - 10;
    }
}

fn test_pattern_matching() {
    color: Color = .rgb{255, 128, 0};
    
    match color {
        case .rgb{r, g, b} if r > 200:
            native {
                printf("Bright color\n");
            }
        case .rgb{255, 0, 0}:
            native {
                printf("Pure red\n");
            }
        case .hsv{_, _, _}:
            native {
                printf("HSV color\n");
            }
        case .named{name}:
            native {
                printf("Named color: %s\n", name.data);
            }
        case _:
            native {
                printf("Unknown color\n");
            }
    }
    
    data: List i32 = [1, 2, 3, 4, 5];
    
    match data {
        case []:
            native {
                printf("Empty list\n");
            }
        case [first, ..rest]:
            native {
                printf("First: %d\n", first);
            }
        case [1, 2, 3, 4, 5]:
            native {
                printf("Exact match\n");
            }
        case _:
            native {
                printf("Other\n");
            }
    }
}

fn test_collections() {
    scores: Map str i32 = {
        "Alice": 95,
        "Bob": 87,
        "Charlie": 92
    };
    
    visited: Set str = {
        "Paris",
        "London", 
        "Tokyo"
    };
    
    for name, score in scores {
        if score > 90 {
            native {
                printf("%s scored well: %d\n", name.data, score);
            }
        }
    }
    
    for city in visited {
        native {
            printf("Visited: %s\n", city.data);
        }
    }
}

fn test_pointers_and_references() {
    age: u8 = 25;
    age_ptr: *u8 = &age;
    *age_ptr = 30;
    
    point: Point i32 = {x: 10, y: 20};
    point_ptr: *Point i32 = &point;
    
    x_val: i32 = point_ptr.x;
}

fn test_expressions() {
    a: i32 = 10;
    b: i32 = 20;
    c: f32 = 3.14;
    d: f64 = 2.718e10;
    
    result1: bool = a == b and c > 2.0;
    result2: bool = not (a != b or c <= 1.0);
    result3: i32 = a + b * 2 - a / 3;
    result4: i32 = a % 3;
    
    greeting: str = "Hello, " + "world!";
    numbers: List i32 = [1, 2] + [3, 4, 5];
}

fn fibonacci(n: i32) -> i32 {
    if n <= 1 {
        return n;
    } elif n == 2 {
        return 1;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

fn main() {
    native {
        printf("Starting Sageleaf test program\n");
    }
    
    process_numbers();
    test_pattern_matching();
    test_collections();
    test_pointers_and_references();
    test_expressions();
    
    fib_result: i32 = fibonacci(10);
    
    native {
        printf("Fibonacci(10) = %d\n", fib_result);
        printf("Program completed successfully\n");
    }
}