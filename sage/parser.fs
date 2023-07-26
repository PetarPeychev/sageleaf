module parser

type Module = Statement list

and Statement = Binding of name: string * typ: Type * value: Expression
// | TypeDef of name: string * body: unit

and Type =
    | IntType
    | BoolType
    | StrType
    | UnitType

and Expression =
    | Int of int
    | Bool of bool
    | Str of string
    | Unit

let parseExpression tokens =
    match tokens with
    | lexer.Int n :: rest -> (Int n, rest)
    | lexer.Bool b :: rest -> (Bool b, rest)
    | lexer.Str s :: rest -> (Str s, rest)
    | _ -> failwith "Expected an expression."

let parseType tokens =
    match tokens with
    | lexer.IntType :: rest -> (IntType, rest)
    | lexer.BoolType :: rest -> (BoolType, rest)
    | lexer.StrType :: rest -> (StrType, rest)
    | lexer.UnitType :: rest -> (UnitType, rest)
    | _ -> failwith "Expected a type."

let parseStatement tokens =
    match tokens with
    | lexer.Let :: rest ->
        let name, rest =
            match rest with
            | lexer.Id name :: rest -> (name, rest)
            | _ -> failwith "Expected a name for the let binding."

        let _, rest =
            match rest with
            | lexer.Colon :: rest -> ((), rest)
            | _ -> failwith "Expected a colon after the let binding name."

        let typ, rest = parseType rest

        let _, rest =
            match rest with
            | lexer.Equals :: rest -> ((), rest)
            | _ -> failwith "Expected an equals sign after the let binding type."

        let value, rest = parseExpression rest

        (Binding(name, typ, value), rest)
    // | lexer.Type :: rest ->
    //     let name, rest =
    //         match rest with
    //         | lexer.Id name :: rest -> (name, rest)
    //         | _ -> failwith "Expected a name for the type definition."

    //     let _, rest =
    //         match rest with
    //         | lexer.Equals :: rest -> ((), rest)
    //         | _ -> failwith "Expected an equals sign after the type definition type."

    //     let body, rest = parseTypeDef rest

    //     (TypeDef(name, body), rest)
    | _ -> failwith "Expected a top-level statement, either a let binding or a type definition."

let rec parseModule tokens =
    match tokens with
    | [ lexer.Eof ] -> []
    | _ ->
        let statement, rest = parseStatement tokens
        statement :: parseModule rest
