module parser

type File =
    { name: string
      statements: Statement list }

and Statement = Binding of name: string * typ: Type * value: Expression

and Type =
    | IntType
    | BoolType
    | StrType
    | ListType of Type
    | FunctionType of input: Type * output: Type

and Expression =
    | Id of string
    | Int of int
    | Bool of bool
    | Str of string
    | Apply of func: Expression * arg: Expression
    | DoThen of d: Expression * t: Expression
    | Function of arg: string * body: Expression

let rec parseExpression tokens =
    match tokens with
    | lexer.Id(_, a) :: lexer.Arrow _ :: rest ->
        let b, rest = parseExpression rest
        (Function(a, b), rest)
    | lexer.Int(_, n) :: rest -> (Int n, rest)
    | lexer.Bool(_, b) :: rest -> (Bool b, rest)
    | lexer.Str(_, s) :: rest -> (Str s, rest)
    | lexer.Id(_, a) :: rest -> (Id a, rest)
    | _ -> failwith "Expected an expression."

let parseBasicType token =
    match token with
    | lexer.IntType _ -> IntType
    | lexer.BoolType _ -> BoolType
    | lexer.StrType _ -> StrType
    | _ -> failwith "Expected a basic type."

let rec parseType tokens =
    match tokens with
    | a :: lexer.Arrow _ :: rest ->
        let b, rest = parseType rest
        (FunctionType(parseBasicType a, b), rest)
    | lexer.IntType _ :: rest -> (IntType, rest)
    | lexer.BoolType _ :: rest -> (BoolType, rest)
    | lexer.StrType _ :: rest -> (StrType, rest)
    | _ -> failwith "Expected a type."

let parseStatement tokens =
    match tokens with
    | lexer.Let _ :: rest ->
        let name, rest =
            match rest with
            | lexer.Id(_, name) :: rest -> (name, rest)
            | _ -> failwith "Expected a name for the let binding."

        let _, rest =
            match rest with
            | lexer.Colon _ :: rest -> ((), rest)
            | _ -> failwith "Expected a colon after the let binding name."

        let typ, rest = parseType rest

        let _, rest =
            match rest with
            | lexer.Equals _ :: rest -> ((), rest)
            | _ -> failwith "Expected an equals sign after the let binding type."

        let value, rest = parseExpression rest

        (Binding(name, typ, value), rest)
    | _ -> failwith "Expected a top-level statement, either a let binding or a type definition."

let rec parseStatements tokens =
    match tokens with
    | [ lexer.Eof ] -> []
    | _ ->
        let statement, rest = parseStatement tokens
        statement :: parseStatements rest

let rec parseFile name tokens =
    { name = name
      statements = parseStatements tokens }
