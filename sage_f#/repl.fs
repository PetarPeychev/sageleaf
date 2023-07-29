module repl

// open System

// let rec run () =
//     printf "> "
//     let input = Console.ReadLine()

//     if input = "exit" then
//         ()
//     else
//         input
//         |> lexer.lex
//         |> parser.parseModule
//         |> types.typeCheckModule
//         |> fun res ->
//             match res with
//             | Ok(m) -> printfn $"%A{m}"
//             | Error(e) -> printfn $"Type errors: %A{e}"

//         run ()
