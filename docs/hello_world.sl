let println: string -> none =
    s -> (
        print s;
        print "\n"
    )


let main: none -> none =
    _ -> (println "Hello, World!\n")


let add: num -> num -> num =
    a -> b -> a + b


let increment: num -> num =
    a -> a + 1


fn add(a: int, b: int): int {
    return a + b
}

fn main() {

}

fn increment(a: int): int {
    return a + 1;
}
