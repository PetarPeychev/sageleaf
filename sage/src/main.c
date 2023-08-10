#include <stdio.h>
#include <stdlib.h>

#include "utils.h"
#include "lexer.h"

#define _POSIX_C_SOURCE 200809L

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    char *buffer = read_file(argv[1]);
    printf("%s\n", buffer);

    free(buffer);

    return 0;
}
