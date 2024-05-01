use crate::parser::AST;

const HEADER: &str = r#"section .text
    global MAIN

MAIN:
    write STDOUT, msg, msg.len
    exit 0

; -------------------- Data --------------------
section .data
    msg: db "Hello, World!", NEWLINE
    .len equ $ - msg
"#;

fn generate(ast: &AST) -> String {
    let mut code = String::new();
    code.push_str("use std::io::{self, Write};\n");

    for statement in &ast.statements {
        match statement {
            _ => code.push_str("fn main() {\n"),
        }
    }

    code
}
