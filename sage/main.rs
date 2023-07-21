mod lexer;

use std::env;

use lexer::{Span, Token, TokenKind};

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() == 1 {
        println!("Sageleaf:\n");
        loop {
            print!("> ");
            let mut input = String::new();
            std::io::stdin().read_line(&mut input).unwrap();
            println!("{input}");
        }
    } else if args.len() == 2 {
        let file_path = &args[1];
        let content = std::fs::read_to_string(file_path).unwrap();
        println!("{content}")
    } else {
        println!("Usage: sageleaf [path]");
    }
}
