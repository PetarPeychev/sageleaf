module interpreter

let runFile path =
    path
    |> System.IO.File.ReadAllText
    |> lexer.lex
    |> parser.parseModule
    |> types.typeCheckModule
    |> fun res ->
        match res with
        | Ok(m) -> m
        | Error(e) -> failwith $"Type errors: %A{e}"
    |> printfn "%A"
