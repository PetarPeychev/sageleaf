fn do_stuff() -> i8 {
    return 128;
}

fn main() {
    native {
        printf("%d\n", sl_do_stuff());
    }
}
