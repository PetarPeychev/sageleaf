module types

let typeCheckSymbol id typ symbols =
    match Map.tryFind id symbols with
    | Some(t) when t = typ -> Ok(id)
    | Some(t) -> Error($"Expected a %A{t}, got a %A{typ}")
    | None -> Error($"Unknown symbol %A{id}")

let rec typeCheckExpression t e symbols =
    match t with
    | parser.IntType ->
        match e with
        | parser.Int(_) -> Ok(e)
        | parser.Id(n) ->
            match typeCheckSymbol n t symbols with
            | Ok(_) -> Ok(e)
            | Error(e) -> Error(e)
        | t -> Error($"Expected an Int, got a %A{t}")
    | parser.BoolType ->
        match e with
        | parser.Bool(_) -> Ok(e)
        | t -> Error($"Expected a Bool, got a %A{t}")
    | parser.StrType ->
        match e with
        | parser.Str(_) -> Ok(e)
        | t -> Error($"Expected a Str, got a %A{t}")
    | parser.UnitType ->
        match e with
        | parser.Unit -> Ok(e)
        | t -> Error($"Expected a unit, got a %A{t}")
    | parser.FunctionType(in_type, out_type) ->
        match e with
        | parser.Function(arg, body) ->
            let symbols = Map.add arg in_type symbols

            match typeCheckExpression out_type body symbols with
            | Ok(_) -> Ok(e)
            | Error(e) -> Error(e)
        | t -> Error($"Expected a function, got a %A{t}")

let typeCheckStatement s symbols =
    match s with
    | parser.Binding(n, t, v) ->
        let symbols = Map.add n t symbols

        match typeCheckExpression t v symbols with
        | Ok(_) -> Ok(s)
        | Error(e) -> Error(e)

let typeCheckModule m =
    let symbols =
        m
        |> List.map (fun s ->
            match s with
            | parser.Binding(n, t, v) -> (n, t))
        |> Map.ofList

    match
        (m
         |> List.map (fun s -> typeCheckStatement s symbols)
         |> List.filter (fun r -> Result.isError r)
         |> List.map (fun r ->
             match r with
             | Error(e) -> e
             | _ -> failwith "This should never happen."))
    with
    | [] -> Ok(m, symbols)
    | errors -> Error(errors)
