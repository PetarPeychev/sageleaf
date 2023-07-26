module types

let typeCheckStatement s =
    match s with
    | parser.Binding(n, t, v) -> if typeCheckExpression

let typeCheckModule m =
    match
        (m
         |> List.map (fun s -> typeCheckStatement s)
         |> List.filter (fun r -> Result.isError r))
    with
    | [] -> Ok(m)
    | errors -> Error(errors)
