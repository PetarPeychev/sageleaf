let list: [int] = [1, 2, 3]

let z: int or str = "error"

type RGB = {
    red: int,
    green: int,
    blue: int
}

type Result 'a =
    {ok: 'a} or
    {err: str}

fn read_file(path: str): Result str {
    match file.open(path) {
        none -> return {err: "file not found"},
        {file: f} -> {
            let content = read(f);
            close(f);
            return {ok: content}
        },
    }
}

type Role =
    {admin} or
    {user} or
    {guest};

type User = {
    name: str,
    age: int,
    role: Role,
}

fn is_admin(user: User): bool {
    return user.role is {admin};
}

let john: User = {
    name: "John",
    age: 20,
    role: {user}
}

let is_john_admin: bool =
    john
    |> is_admin

fn int_to_str(x: int): str {
    match x {
        0 -> return "zero",
        1 -> return "one",
        2 -> return "two",
        _ -> return "too much"
    }
}

fn fibonacci(x: int): int {
    if x is 0 or x is 1 {
        return x;
    }
    return fibonacci(x - 1) + fibonacci(x - 2);
}

type Option T = {some: T} or {none};

fn last_element(list: [T]): Option T {
    fn last_rec(list: [T], prev: Option T): Option T {
        match list {
            [] -> return prev,
            [x: xs] -> return last_rec(xs, x)
        }
    }

    return last_rec(list, {none})
}
