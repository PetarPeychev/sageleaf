#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

void print_usage(char *program_name) {
    fprintf(stderr, "Usage: %s <command> [ARGUMENTS]\n", program_name);
    fprintf(stderr, "\n");
    fprintf(stderr, "Commands:\n");
    fprintf(stderr, "    build [FILE] - Build a sageleaf program.\n");
}

char *format(const char *fmt, ...)
{
    int n = 0;
    size_t size = 0;
    char *p = NULL;
    va_list ap;

    va_start(ap, fmt);
    n = vsnprintf(p, size, fmt, ap);
    va_end(ap);

    if (n < 0)
        return NULL;

    size = (size_t) n + 1;
    p = malloc(size);
    if (p == NULL)
        return NULL;

    va_start(ap, fmt);
    n = vsnprintf(p, size, fmt, ap);
    va_end(ap);

    if (n < 0) {
        free(p);
        return NULL;
    }

    return p;
}

char *read_file(char *path) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return NULL;
    }
    fseek(file, 0, SEEK_END);
    long position = ftell(file);
    if (position < 0) {
        fprintf(stderr, "ERROR: Could not read file '%s'\n", path);
        fclose(file);
        return NULL;
    }
    size_t length = (size_t)position;
    rewind(file);

    char *buffer = malloc(length + 1);
    if (!buffer) {
        fprintf(stderr, "ERROR: Not enough memory to read '%s'\n", path);
        fclose(file);
        return NULL;
    }
    size_t read = fread(buffer, 1, length, file);
    if (read != length) {
        fprintf(stderr, "ERROR: Could not read file '%s'\n", path);
        fclose(file);
        return NULL;
    }
    buffer[length] = '\0';

    fclose(file);
    return buffer;
}

void write_file(char *path, char *content) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        fprintf(stderr, "ERROR: Failed to write to file '%s'.\n", path);
        exit(EXIT_FAILURE);
    }
    
    fputs(content, file);
    
    fclose(file);
}

int main(int argc, char *argv[]) {
    char *program_name = argv[0];
    
    if (argc < 2) {
        print_usage(program_name);
        return EXIT_FAILURE;
    }
    
    if (strcmp(argv[1], "build") == 0) {
        if (argc < 3) {
            fprintf(stderr, "ERROR: Filename not provided.\n\n");
            print_usage(program_name);
            return EXIT_FAILURE;
        } else if (argc > 3) {
            fprintf(stderr, "ERROR: Too many arguments.\n\n");
            print_usage(program_name);
            return EXIT_FAILURE;
        }

        // 1. Read source file.
        char *source = read_file(argv[2]);
        if (source == NULL) {
            fprintf(stderr, "ERROR: Failed to read file '%s'.\n", argv[2]);
            return EXIT_FAILURE;
        }

        size_t len = strlen(argv[2]);
        size_t len_stripped = len - 3;

        if (strcmp(argv[2] + len_stripped, ".sl") != 0) {
            fprintf(stderr, "ERROR: Expected .sl file, got '%s'.\n", argv[2]);
            return EXIT_FAILURE;
        }

        char *path = malloc(len_stripped + 1);
        strncpy(path, argv[2], len_stripped);
        path[len_stripped] = '\0';

        // 2. Lex into tokens.
        
        // 3. Parse into an AST.

        // 4. Generate assembly.
        write_file(format("%s.s", path),
            "\t.globl main\n"
            "main:\n"
            "\tmovl $2, %eax\n"
            "\tret\n"
            "\t.section .note.GNU-stack,\"\",@progbits\n"
        );

        // 5. Invoke linker to produce executable.
        system(format("gcc %s.s -o %s", path, path));
        system(format("rm %s.s", path));

        return EXIT_SUCCESS;
    } else {
        fprintf(stderr, "ERROR: Unrecognized command '%s'.\n\n", argv[1]);
        print_usage(program_name);
        return EXIT_FAILURE;
    }
}
