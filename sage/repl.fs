module repl

open System

let rec run () =
    printf "> "
    let input = Console.ReadLine()

    if input = "exit" then
        ()
    else
        input
        |> lexer.lex
        |> parser.parseModule
        |> types.typeCheckModule
        |> printfn "%A"

        run ()
