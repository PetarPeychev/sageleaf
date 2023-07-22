[<EntryPoint>]
let main args =
    match args with
    | [||] ->
        repl.run ()
        0
    | [| file |] ->
        printfn "... %s" file
        0
    | _ ->
        printfn "Usage: sage <file>"
        1
