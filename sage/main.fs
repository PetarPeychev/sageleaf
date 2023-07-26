open System.IO

[<EntryPoint>]
let main args =
    match args with
    | [||] ->
        repl.run ()
        0
    | [| file |] ->
        file
        |> File.ReadAllText
        |> lexer.lex
        |> parser.parseModule
        |> types.typeCheckModule
        |> printfn "%A"

        0
    | _ ->
        printfn "Usage: sage <file>"
        1
