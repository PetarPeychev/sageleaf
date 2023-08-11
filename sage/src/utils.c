#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include "utils.h"

char *read_file(const char *path)
{
    FILE *file = fopen(path, "rb");

    if (file == NULL)
    {
        fprintf(stderr, "Could not open file \"%s\".\n", path);
        exit(1);
    }

    fseek(file, 0L, SEEK_END);
    u32 file_size = ftell(file);
    rewind(file);

    char *buffer = (char *)malloc(file_size + 1);

    if (buffer == NULL)
    {
        fprintf(stderr, "Not enough memory to read \"%s\".\n", path);
        exit(1);
    }

    u32 bytes_read = fread(buffer, sizeof(char), file_size, file);

    if (bytes_read < file_size)
    {
        fprintf(stderr, "Could not read file \"%s\".\n", path);
        exit(1);
    }

    buffer[bytes_read] = '\0';

    fclose(file);
    return buffer;
}

i32 vasprintf(char **str, const char *fmt, va_list args)
{
    i32 size = 0;
    va_list tmpa;

    // copy
    va_copy(tmpa, args);

    // apply variadic arguments to
    // sprintf with format to get size
    size = vsnprintf(NULL, 0, fmt, tmpa);

    // toss args
    va_end(tmpa);

    // return -1 to be compliant if
    // size is less than 0
    if (size < 0)
    {
        return -1;
    }

    // alloc with size plus 1 for `\0'
    *str = (char *)malloc(size + 1);

    // return -1 to be compliant
    // if pointer is `NULL'
    if (NULL == *str)
    {
        return -1;
    }

    // format string with original
    // variadic arguments and set new size
    size = vsprintf(*str, fmt, args);
    return size;
}

i32 print_to_string(char **str, const char *fmt, ...)
{
    i32 size = 0;
    va_list args;

    // init variadic argumens
    va_start(args, fmt);

    // format and get size
    size = vasprintf(str, fmt, args);

    // toss args
    va_end(args);

    return size;
}