// --- Sageleaf Runtime ---
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>

void sl_main(void);

int main(void) {
    sl_main();
    return 0;
}

// --- Sageleaf Library ---
int32_t sl_add(int32_t sl_a, int32_t sl_b);

int32_t sl_add(int32_t sl_a, int32_t sl_b) {
    return sl_a + sl_b;
}

// --- Sageleaf User Program ---
void sl_main() {
    printf("Hello, world!\n");
    
    for(int i = 0; i < 10; i++) {
        printf("i = %d\n", i);
    }
}

