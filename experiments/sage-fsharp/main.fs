open System.IO

[<EntryPoint>]
let main args =
    match args with
    // | [||] ->
    //     repl.run ()
    //     0
    | [| file |] ->
        file
        |> File.ReadAllText
        |> lexer.lex
        |> parser.parseFile (Path.GetFileNameWithoutExtension file)
        |> printfn "%A"
        // |> types.typeCheckStatements
        // |> interpreter.runStatements

        0
    | _ ->
        printfn "Usage: sage [file]"
        1
