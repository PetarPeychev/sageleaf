import system
import math
import Vector, Matrix from geometry
import collections as col

native {
    #include <math.h>
    #include <complex.h>
    
    typedef struct {
        double real;
        double imag;
    } complex_t;
}

struct ComplexNumber {
    real: f64,
    imag: f64
}

struct Matrix 'T {
    data: List (List T),
    rows: usize,
    cols: usize
}

union ParseResult 'T {
    success: struct { value: T, remaining: str },
    error: struct { message: str, position: usize }
}

union Either 'L 'R {
    left: L,
    right: R
}

const EPSILON: f64 = 1e-10;
const MAX_ITERATIONS: u32 = 1000;

fn test_complex_expressions() {
    a: i32 = 42;
    b: f64 = 3.14159;
    c: bool = true;
    
    result1: i32 = (a + 10) * (a - 5) / ((a % 3) + 1);
    result2: f64 = ((b * 2.0) + 1.0) / ((b - 1.0) * (b + 1.0));
    result3: bool = ((a > 10) and (b < 5.0)) or (not c and (a == 42));
    
    complex_expr: i32 = (((a + 5) * 3) - ((a * 2) + (5 / 2))) % 100;
    
    simple_conditional: i32 = a * 2;
    
    deeply_nested: i32 = ((((a + 1) * 2) - ((5 - 5) / 2)) + (((a % 3) * 4)));
}

fn test_edge_case_literals() {
    hex_nums: List u32 = [0x0, 0xFF, 0xDEADBEEF, 0xABC123];
    bin_nums: List u8 = [0b0, 0b1, 0b11111111, 0b10101010];
    oct_nums: List u16 = [0o0, 0o7, 0o777];
    
    floats: List f64 = [
        0.0, 1.0, -1.0,
        1.23e10, -4.56e-20,
        0.5, 1.0, 2.5
    ];
    
    strings: List str = [
        "",
        "simple",
        "with newlines and tabs",
        "concatenated " + "string " + "parts"
    ];
    
    chars: List char = ["a", "b", "c", "d", "e"];
}

fn test_complex_control_flow() {
    data: List i32 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    for value in data {
        if (value % 2 == 0) and (value > 4) {
            if value == 6 {
                continue;
            } elif value == 8 {
                break;
            } else {
                native {
                    printf("Even value > 4: %d\n", value);
                }
            }
        }
    }
    
    for i in 0..<10 {
        for j in 0..=i {
            for k in (j + 1)..<20 {
                if ((i * j + k) % 7 == 0) and (i + j + k > 15) {
                    break;
                }
            }
        }
    }
    
    x: i32 = 0;
    y: i32 = 100;
    
    while (x < 50) and (y > 25) and ((x + y) % 3 != 0) {
        if (x % 2 == 0) {
            x = x + 1;
            continue;
        }
        
        x = x + 2;
        y = y - 1;
        
        if (x > y) {
            break;
        }
    }
}

fn test_pattern_matching() {
    result: ParseResult i32 = .success{42, "remaining"};
    
    match result {
        case .success{value, remaining} if (value > 0) and (len(remaining) > 0):
            native { printf("Successful parse: %d\n", value); }
        
        case .success{value, remaining}:
            native { printf("Small value: %d\n", value); }
            
        case .success{value, remaining} if value < 0:
            native { printf("Negative value not allowed\n"); }
            
        case .error{message, position}:
            native { printf("Parse failed at %zu: %s\n", position, message.data); }
            
        case .error{message, position} if position > 100:
            native { printf("Error far in input\n"); }
            
        case _:
            native { printf("Other case\n"); }
    }
    
    matrix: List (List i32) = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    
    match matrix {
        case []:
            native { printf("Empty matrix\n"); }
            
        case [[single]]:
            native { printf("1x1 matrix: %d\n", single); }
            
        case [[a, b], [c, d]] if (a * d - b * c) != 0:
            native { printf("Invertible 2x2 matrix\n"); }
            
        case [first_row, ..other_rows]:
            native { printf("Matrix with multiple rows\n"); }
            
        case rows:
            native { printf("Other matrix pattern\n"); }
            
        case _:
            native { printf("Irregular matrix\n"); }
    }
}

fn test_parenthesized_expressions() {
    x: i32 = 10;
    y: i32 = 20;
    z: f64 = 3.14;
    
    complex1: i32 = ((x + y) * (x - y)) / ((x * 2) + (y / 3));
    complex2: f64 = ((z * z) + 10.0) - (20.0 / (z + 1.0));
    complex3: bool = ((x > 5) and (y < 30)) or ((z > 3.0) and not (x == y));
    
    deeply_nested: i32 = ((((x + 1) * 2) - ((y - 5) / 2)) + ((3 % 3) * 4));
    
    simple_expr: i32 = ((x + y) * 2);
}

global_var: List str = [];

fn test_global_variables() {
    global_var.append("\n\t stringz");

    PROGRAM_VERSION: str = "1.2.3";
    DEBUG_MODE: bool = false;
    MAX_BUFFER_SIZE: usize = 8192;
    DEFAULT_TIMEOUT: f64 = 30.0;
    GLOBAL_COUNTER: i32 = 0;
    SHARED_CONFIG: Map str str = {
        "host": "localhost",
        "port": "8080",
        "protocol": "https"
    };
    ERROR_CODES: List str = ["SUCCESS", "INVALID_INPUT", "NETWORK_ERROR", "TIMEOUT"];
    
    GLOBAL_COUNTER = GLOBAL_COUNTER + 1;
    
    version_parts: List str = PROGRAM_VERSION.split(".");
    
    if DEBUG_MODE {
        native {
            printf("Debug mode enabled, counter: %d\n", GLOBAL_COUNTER);
        }
    }
    
    host: str = SHARED_CONFIG["host"];
    timeout: f64 = DEFAULT_TIMEOUT * 2.0;
    
    error_msg: str = ERROR_CODES[1];
}

fn main() {
    native {
        printf("Testing edge cases and complex expressions...\n");
    }
    
    test_complex_expressions();
    test_edge_case_literals();
    test_complex_control_flow();
    test_global_variables();
    test_pattern_matching();
    test_parenthesized_expressions();
    
    native {
        printf("Edge case testing completed!\n");
    }
}