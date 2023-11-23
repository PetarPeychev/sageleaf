use std::env;

mod codegen;
mod lexer;
mod parser;

fn main() {
    let args: Vec<String> = env::args().collect();
    let args_str: Vec<&str> = args.iter().map(|s| s.as_str()).collect();

    match args_str[..] {
        [_, arg] if arg == "-h" || arg == "--help" => {
            print_usage(args_str[0]);
        }
        [_, arg] if arg == "-v" || arg == "--version" => {
            println!("sagec {}", env!("CARGO_PKG_VERSION"));
        }
        [_, file_path] => {
            compile(file_path);
        }
        _ => {
            print_usage(args_str[0]);
        }
    }
}

fn print_usage(program: &str) {
    println!("Usage: {} [OPTION] FILE", program);
    println!();
    println!("  -h, --help     Display this message and exit.");
    println!("  -v, --version  Output version information and exit.");
}

fn compile(file_path: &str) {
    let source = std::fs::read_to_string(file_path).expect("Failed to read file.");
    let tokens = lexer::lex(&source); // TODO: implement
    let ast = parser::parse(&tokens); // TODO: implement
    let code = codegen::generate(&ast); // TODO: implement
    println!("{}", code); // TODO: write to a file
}
