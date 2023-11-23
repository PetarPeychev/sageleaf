let list: [int] = [1, 2, 3]

let z: int or str = "error"

type rgb = {
    red: int,
    green: int,
    blue: int
}

type result a =
    {ok: a} or {err: str}

let read_file: str -> {ok: str} or {err: str} =
    path ->
        if open path
        is none then {error: "file not found"}
        is {file: f} then
            let content = read f;
            close file;
            {ok: content}

type perms =
    {admin}
    or {user}
    or {guest}

type user = {
    name: str,
    age: int,
    perm: perms
}

# this is a comment explaining something
let is_admin: {perm: perms} -> bool =
    user ->
        if user.perm
        is {admin} then true # and another one
        else false

let john := {
    name: "John",
    age: 20,
    perm: {user}
}

let is_john_admin: bool =
    john
    |> is_admin

let int_to_str: int -> str:
    s ->
        if s
        is 1 then "one"
        is 2 then "two"
        is 3 then "three"
        else "i can't count that high"

let fibonacci: int -> int =
    num ->
        if num
        is 0 or num = 1 then num
        is n then fibonacci (n - 1) + fibonacci (n - 2)

let last_element: [a] -> a or none =
    list ->
        let last_rec =
            list -> prev ->
                if list
                is [] then prev
                is [x: xs] then last_rec xs prev;

        last_rec list none

let say_hello: str -> none =
    name ->
        print "Hello, ";
        print name;
        print "!\n"