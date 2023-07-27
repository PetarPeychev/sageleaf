module lexer

open System
open System.Text.RegularExpressions

type Span = { start: int; length: int }

type Token =
    // Keywords
    | Let of span: Span
    | Do of span: Span
    | Then of span: Span

    // Symbols
    | Lbracket of span: Span
    | Rbracket of span: Span
    | Colon of span: Span
    | Equals of span: Span
    | Arrow of span: Span

    // Types
    | IntType of span: Span
    | BoolType of span: Span
    | StrType of span: Span

    // Literals
    | Int of span: Span * value: int
    | Bool of span: Span * value: bool
    | Str of span: Span * value: string
    | Id of span: Span * value: string

    // Special
    | Eof
    | Error of span: Span * msg: string

let lex input =
    let (|Prefix|_|) (p: string) (s: string) =
        if s.StartsWith(p) then
            Some(s.Substring(p.Length))
        else
            None

    let (|Regex|_|) p s =
        let m = Regex.Match(s, p)

        if m.Success then
            Some((m.Value, s.Substring(m.Length)))
        else
            None

    let rec lex' (input: string) pos =
        match input with
        // Whitespace
        | Prefix " " rest -> lex' rest (pos + 1)
        | Prefix "\n" rest -> lex' rest (pos + 1)
        | Prefix "\t" rest -> lex' rest (pos + 1)
        | Prefix "\r" rest -> lex' rest (pos + 1)

        // Symbols
        | Prefix "[" rest -> Lbracket { start = pos; length = 1 } :: lex' rest (pos + 1)
        | Prefix "]" rest -> Rbracket { start = pos; length = 1 } :: lex' rest (pos + 1)
        | Prefix ":" rest -> Colon { start = pos; length = 1 } :: lex' rest (pos + 1)
        | Prefix "=" rest -> Equals { start = pos; length = 1 } :: lex' rest (pos + 1)
        | Prefix "->" rest -> Arrow { start = pos; length = 2 } :: lex' rest (pos + 2)

        // Types
        | Prefix "int" rest -> IntType { start = pos; length = 3 } :: lex' rest (pos + 3)
        | Prefix "bool" rest -> BoolType { start = pos; length = 4 } :: lex' rest (pos + 4)
        | Prefix "str" rest -> StrType { start = pos; length = 3 } :: lex' rest (pos + 3)

        // Keywords
        | Prefix "let" rest -> Let { start = pos; length = 3 } :: lex' rest (pos + 3)
        | Prefix "do" rest -> Do { start = pos; length = 2 } :: lex' rest (pos + 2)
        | Prefix "then" rest -> Then { start = pos; length = 4 } :: lex' rest (pos + 4)

        // Literals
        | Regex "^([0]|[1-9][0-9]*)" (n, rest) ->
            try
                Int({ start = pos; length = n.Length }, Int32.Parse(n))
            with ex ->
                Error({ start = pos; length = n.Length }, "Lexer Error: Invalid integer literal %s{n}")
            :: lex' rest (pos + n.Length)
        | Prefix "true" rest -> Bool({ start = pos; length = 4 }, true) :: lex' rest (pos + 4)
        | Prefix "false" rest -> Bool({ start = pos; length = 5 }, false) :: lex' rest (pos + 5)
        | Regex "^\"[^\"]*\"" (s, rest) ->
            Str({ start = pos; length = s.Length }, s.Replace("\"", ""))
            :: lex' rest (pos + s.Length)
        | Regex "^[a-zA-Z_][a-zA-Z0-9_]*" (id, rest) ->
            Id({ start = pos; length = id.Length }, id) :: lex' rest (pos + id.Length)

        // Special
        | Regex "^[^\s]+" (v, rest) -> Error({ start = pos; length = v.Length }, v) :: lex' rest (pos + v.Length)
        | "" -> [ Eof ]
        | _ -> [ Error({ start = pos; length = 0 }, "Lexer Error: Unknown error.") ]

    lex' input 0
