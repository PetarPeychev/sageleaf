# using statements should indicate external module being used but
# wont necessarily correspond to an actual file so the module dependencies can
# be switched configurably by the compiler and allow for example to write dummy
# implementations of certain modules for testing/development
using str, list, console

let fizzbuzz: int -> str =
n ->
    match n
    | n if n % 15 is 0  => "FizzBuzz"
    | n if n % 3 is 0   => "Fizz"
    | n if n % 5 is 0   => "Buzz"
    | n                 => n |> str.from_int


let println: str -> () &io =
s ->
    s
    |> str.concat _ "\n"
    |> console.print


let main: [str] -> int =
_ ->
    do
        list.range 100
        |> list.map fizzbuzz
        |> println
    then 0
