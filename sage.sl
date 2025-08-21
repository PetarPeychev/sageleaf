fn is_petar_cool() -> bool {
    return true;
}

fn main() {
    native {
        printf("Hello, world!\n");

        for(int i = 0; i < 10; i++) {
            printf("i = %d\n", i);
        }

        printf("is petar cool: %d\n", sl_is_petar_cool());
    }
}
