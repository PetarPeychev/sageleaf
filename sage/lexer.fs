module lexer

open System
open System.Text.RegularExpressions

type Token =
    // Keywords
    | Let
    | In
    | Type
    | If
    | Then
    | Else
    | Do
    | When
    | Is
    | And
    | Or
    | Not

    // Symbols
    | Lparen
    | Rparen
    | Colon
    | Equals
    | Comma
    | Arrow
    | DoubleArrow
    | Pipe

    // Types
    | IntType
    | BoolType
    | StrType

    // Literals
    | Int of int
    | Bool of bool
    | Str of string
    | Id of string

    // Special
    | Eof
    | Error of string

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
        | Prefix "(" rest -> Lparen :: lex' rest (pos + 1)
        | Prefix ")" rest -> Rparen :: lex' rest (pos + 1)
        | Prefix ":" rest -> Colon :: lex' rest (pos + 1)
        | Prefix "=" rest -> Equals :: lex' rest (pos + 1)
        | Prefix "," rest -> Comma :: lex' rest (pos + 1)
        | Prefix "->" rest -> Arrow :: lex' rest (pos + 2)
        | Prefix "=>" rest -> DoubleArrow :: lex' rest (pos + 2)
        | Prefix ">>" rest -> Pipe :: lex' rest (pos + 2)

        // Types
        | Prefix "int" rest -> IntType :: lex' rest (pos + 3)
        | Prefix "bool" rest -> BoolType :: lex' rest (pos + 4)
        | Prefix "str" rest -> StrType :: lex' rest (pos + 3)

        // Keywords
        | Prefix "let" rest -> Let :: lex' rest (pos + 3)
        | Prefix "in" rest -> In :: lex' rest (pos + 2)
        | Prefix "type" rest -> Type :: lex' rest (pos + 4)
        | Prefix "if" rest -> If :: lex' rest (pos + 2)
        | Prefix "then" rest -> Then :: lex' rest (pos + 4)
        | Prefix "else" rest -> Else :: lex' rest (pos + 4)
        | Prefix "do" rest -> Do :: lex' rest (pos + 2)
        | Prefix "when" rest -> When :: lex' rest (pos + 4)
        | Prefix "is" rest -> Is :: lex' rest (pos + 2)
        | Prefix "and" rest -> And :: lex' rest (pos + 3)
        | Prefix "or" rest -> Or :: lex' rest (pos + 2)
        | Prefix "not" rest -> Not :: lex' rest (pos + 3)

        // Literals
        | Regex "^([0]|[1-9][0-9]*)" (n, rest) ->
            try
                Int(Int32.Parse(n))
            with ex ->
                Error(n)
            :: lex' rest (pos + n.Length)
        | Prefix "true" rest -> Bool(true) :: lex' rest (pos + 4)
        | Prefix "false" rest -> Bool(false) :: lex' rest (pos + 5)
        | Regex "^\"[^\"]*\"" (s, rest) -> Str(s.Replace("\"", "")) :: lex' rest (pos + s.Length)
        | Regex "^[a-zA-Z_][a-zA-Z0-9_]*" (id, rest) -> Id(id) :: lex' rest (pos + id.Length)

        // Special
        | Regex "^[^\s]+" (v, rest) -> Error(v) :: lex' rest (pos + v.Length)
        | "" -> [ Eof ]
        | _ -> [ Error(input) ]

    lex' input 0
