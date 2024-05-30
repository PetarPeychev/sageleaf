use std::env;
use std::fs;

mod lexer;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!("Usage: sage [file]");
        return;
    }

    let file = &args[1];
    match fs::read_to_string(file) {
        Ok(content) => {
            let lex = lexer::tokenize(&content);
            match lex {
                Some(tokens) => println!("{:?}", tokens),
                None => println!("Error: Could not tokenize file"),
            }
        }
        Err(e) => println!("Error: {}", e),
    }
}
