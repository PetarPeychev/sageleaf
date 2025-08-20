// Comprehensive test file covering all token types and edge cases

// Parentheses and braces - no whitespace, various whitespace
()(  )
{}{ }
[][ ]

// Punctuation - adjacent tokens
;,.:
;;;,,,:::...

// Operators - all combinations, no whitespace between
+-*/%
!=>=<=
=====!=!====>=<=<<>>=
->>>>
&&&

// Range operators
....=..<

// Keywords - all keywords separated by various whitespace
fn type return for while if elif else and or not in break continue match case const import from as struct union true false

// Type keywords
i8 i16 i32 i64 u8 u16 u32 u64 usize f32 f64 bool str

// Mixed keywords with no whitespace
fntype returnfor whileif elifelse andor notin breakcontinue

// Identifiers - various valid patterns
identifier _underscore _123 abc123 UPPER_CASE camelCase
_
__multiple__underscores__
identifier_with_unicode_αβγ
très_nice
café

// Numbers - integers and floats
0 1 42 123456789
0.0 1.5 3.14159 0.123 999.999
123.456.789

// Edge case: number followed by dot followed by identifier
123.toString
42.max_value

// String literals - various escape sequences and content
"simple string"
"string with spaces"
"string\nwith\tescapes\r\\"
"string with \"quotes\""
"string with \0 null terminator"
"string with unicode: café, αβγ, 你好"
""
"string with \\ backslash"

// Adjacent string literals
"first""second"
"a""b""c"

// Comments - single line
// This is a comment
//Another comment with no space
//   comment with leading spaces
fn test() {} // inline comment

// Native blocks
native {
    #include <stdio.h>
    printf("Hello from C!\n");
}

native{
    int x = 42;
    return x;
}

// Complex native block with nested braces
native {
    if (condition) {
        for (int i = 0; i < 10; i++) {
            printf("i = %d\n", i);
        }
    }
}

// Mixed content with minimal whitespace
fn(x:i32)->bool{return x>0;}
struct Point{x:f32,y:f32}
type Result=union{Ok:i32,Err:str}

// Mixed content with excessive whitespace
fn   add   (   a   :   i32   ,   b   :   i32   )   ->   i32   {
    return   a   +   b   ;
}

// Unicode identifiers and content
const π = 3.14159;
const café_price = 4.50;
fn naïve_approach() -> bool { return false; }

// Edge cases with underscores
_ = 42;
_var = "test";
var_ = true;
_123_ = 456;

// Complex expressions with no whitespace
result=(a+b)*(c-d)/e%f;
array[index]=value;
obj.field.method();

// Range expressions
0..10
0..<10
start..=end
begin..<finish

// Boolean literals in various contexts
if true and false or not true {}
match result {
    true -> "yes",
    false -> "no"
}

// All assignment and comparison operators
x=y;
a==b;
c!=d;
e>f;
g<h;
i>=j;
k<=l;

// Function calls and method chains
func(arg1,arg2,arg3);
object.method().chain().call();

// Array and struct access
arr[0][1][2];
point.x.abs().sqrt();

// Complex nested structures
fn complex_function(
    param1: struct { x: i32, y: f32 },
    param2: union { A: bool, B: str }
) -> Result<i32, str> {
    match param1 {
        { x: 0, y: _ } -> Result.Err("zero x"),
        { x, y } if x > 0 -> {
            for i in 0..x {
                if i % 2 == 0 {
                    continue;
                }
                return Result.Ok(i * y as i32);
            }
        },
        _ -> Result.Ok(42)
    }
}

// Import statements
import std.io;
from std.collections import Vector, HashMap;
import math as m;

// Constants with various types
const MAX_SIZE: usize = 1000;
const PI: f64 = 3.141592653589793;
const GREETING: str = "Hello, World!";
const ENABLED: bool = true;

// While and for loops
while condition {
    break;
}

for item in collection {
    continue;
}

// Edge case: operators at line boundaries
result = a +
    b *
    c /
    d;

// Minimal valid program
fn main() {}

// Random token dump - not valid program structure, just testing lexer
}}}]]]; native{printf("test");} 42.5.toString() "unclosed"
===!===<<>>>>=
_ _ _ identifier123 _var_ true false and or not
..=..<..=..<..=
(){},.,;:;:;:
+-*/%&>&<&<<=>=!=
/* this isn't a valid comment but should lex as individual tokens
*/
struct{union{match{case{if{while{for{
i8i16i32i64u8u16u32u64usizef32f64boolstr
"escaped\"quotes""adjacent""strings"
123.456.789.abc
fn(){}()[][]{}{}
import from as type const return break continue
nativenative{code}native{more code}
αβγδεζηθ café naïve résumé 你好世界
0x 0b 0o // invalid number prefixes but should lex as separate tokens
..........=====<<<>>>
"string with\nnewlines\tand\tescapes"
"string_with_underscores_and_123_numbers"
_trailing_underscores_
__double__underscores__throughout__
===