module types

let typeCheckExpression t e =
    match t with
    | parser.IntType ->
        match e with
        | parser.Int(_) -> Ok(e)
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
        | t -> Error($"Expected a Unit, got a %A{t}")

let typeCheckStatement s =
    match s with
    | parser.Binding(n, t, v) ->
        match typeCheckExpression t v with
        | Ok(_) -> Ok(s)
        | Error(e) -> Error(e)

let typeCheckModule m =
    match
        (m
         |> List.map (fun s -> typeCheckStatement s)
         |> List.filter (fun r -> Result.isError r))
    with
    | [] -> Ok(m)
    | errors -> Error(errors)
