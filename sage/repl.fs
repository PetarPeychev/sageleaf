module repl

open System

let rec run () =
    printf "> "
    let input = Console.ReadLine()

    if input = "exit" then
        ()
    else
        printfn "%A" (input |> lexer.lex |> parser.parseStatement)
        run ()
