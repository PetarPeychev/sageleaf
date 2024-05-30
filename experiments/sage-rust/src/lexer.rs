use logos::Logos;

mod tok;

pub fn tokenize(input: &str) -> Option<Vec<tok.Token>> {
    let lexer = tok.Token::lexer(input);
    let mut tokens = Vec::new();
    for token in lexer {
        match token {
            Ok(token) => tokens.push(token),
            Err(_) => return None,
        }
    }
    Some(tokens)
}
