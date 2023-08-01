```json
{
    "x": 5,
    "y": "hello",
    "z": 3.14
}
```

```fsharp
type json = (
        str
        | int
        | float
        | bool
        | none
        | [json]
        | {str: json}
    )

let read: str -> json = 
    s -> ...

type my_type = (x: int, y: str, z: float)

let parse_my_json: json -> (parsed: my_type | error: str) =
    json ->
        match json with
        | {str: json} d ->
            let x = dict.at "x" d
            let y = dict.at "y" d
            let z = dict.at "z" d
            {x, y, z}
        | _ -> (error: "invalid json")
```
