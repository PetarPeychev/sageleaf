#include "test.h"
#include "../src/lexer.h"



static char* all_tests() {
    test_run(test_lexer);
    return 0;
}

i32 main (i32 argc, char **argv)
{
    char *result = all_tests();
    if (result != 0) {
         printf("%s\n", result);
     }
     else {
         printf("All tests passed!\n");
     }
     printf("Tests run: %d.\n", tests_run);
 
     return result != 0;
}