fn do_stuff() -> u8 {
    return 256;
}

fn main() {
    native {
        printf("Hello, world!\n");

        for(int i = 0; i < 10; i++) {
            printf("i = %d\n", i);
        }

        printf("stuff: %d\n", sl_do_stuff());
    }
}
