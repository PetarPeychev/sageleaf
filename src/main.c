#include <stdio.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <stdint.h>

void print_usage(char *program_name) {
    fprintf(stderr, "Usage: %s <command> [ARGUMENTS]\n", program_name);
    fprintf(stderr, "\n");
    fprintf(stderr, "Commands:\n");
    fprintf(stderr, "    build [FILE] - Build a sageleaf program.\n");
}

char *format(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    int required_length = vsnprintf(NULL, 0, fmt, ap);
    va_end(ap);

    if (required_length < 0)
        return NULL;

    size_t size = (size_t) required_length + 1; // +1 for '\0'
    char *string = malloc(size);
    if (string == NULL)
        return NULL;

    va_start(ap, fmt);
    required_length = vsnprintf(string, size, fmt, ap);
    va_end(ap);

    if (required_length < 0) {
        free(string);
        return NULL;
    }

    return string;
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

enum TokenKind {
    // Symbols
    TK_LPAREN,
    TK_RPAREN,
    TK_ARROW,
    TK_LCURLY,
    TK_RCURLY,
    TK_SEMICOLON,

    // Keywords
    TK_FN,
    TK_RETURN,
    TK_I32,
    
    TK_IDENTIFIER,
    TK_INTEGER,

    TK_EOF,
};

struct Slice {
    const char *data;
    size_t length;
};

struct Slice slice(const char *str) {
    struct Slice slice = {.data = str, .length = strlen(str)};
    return slice;
}

struct Token {
    enum TokenKind kind;
    struct Slice span;
    int32_t value;
};

struct Token *lex(char *source) {
    struct Token *tokens = malloc(sizeof(struct Token) * 1000); // TODO: dynamic array
    size_t t = 0;

    for (char c = *source; c != '\0'; c = *++source) {
        // Skip whitespace
        if (isspace(c)) {
            continue;
        }

        // Single-character symbols
        else if (c == '(') {
            struct Token token = {
                .kind = TK_LPAREN,
                .span = {
                    .data = source,
                    .length = 1
                }
            };
            tokens[t++] = token;
        }

        else if (c == ')') {
            struct Token token = {
                .kind = TK_RPAREN,
                .span = {
                    .data = source,
                    .length = 1
                }
            };
            tokens[t++] = token;
        }

        else if (c == '{') {
            struct Token token = {
                .kind = TK_LCURLY,
                .span = {
                    .data = source,
                    .length = 1
                }
            };
            tokens[t++] = token;
        }

        else if (c == '}') {
            struct Token token = {
                .kind = TK_RCURLY,
                .span = {
                    .data = source,
                    .length = 1
                }
            };
            tokens[t++] = token;
        }

        else if (c == ';') {
            struct Token token = {
                .kind = TK_SEMICOLON,
                .span = {
                    .data = source,
                    .length = 1
                }
            };
            tokens[t++] = token;
        }

        // Multi-character symbols
        else if (c == '-') {
            if (*++source != '>') {
                fprintf(stderr, "ERROR: Expected '>' in arrow token, got '%c'.\n", *source);
                exit(EXIT_FAILURE);
            }
            c = *source;
            struct Token token = {
                .kind = TK_ARROW,
                .span = {
                    .data = source - 1,
                    .length = 2
                }
            };
            tokens[t++] = token;
        }

        // Variable-length tokens
        else if (isalpha(c) || c == '_') {
            size_t length = 1;
            for (c = *++source; isalnum(c) || c == '_'; c = *++source) {
                length++;
            }
            struct Token token = {
                .kind = TK_IDENTIFIER,
                .span = {
                    .data = source - length,
                    .length = length
                }
            };
            tokens[t++] = token;
            source--;
        }

        else if(isdigit(c)) {
            char *end = source;   
            errno = 0; // To distinguish success/failure after call
            long int value = strtol(source, &end, 10);
            if (errno == ERANGE) {
                perror("strtol");
                exit(EXIT_FAILURE);
            }

            // Clamp to 32-bit int for now
            int32_t truncated = 0;
            if (value > INT32_MAX) truncated = INT32_MAX;
            else if (value < INT32_MIN) truncated = INT32_MIN;
            else truncated = (int32_t)value;
            
            struct Token token = {
                .kind = TK_INTEGER,
                .value = truncated,
                .span = {
                    .data = source,
                    .length = end - source   
                }
            };
            tokens[t++] = token;
            source = --end;
        }

        else {
            fprintf(stderr, "ERROR: Unrecognized token '%c'.\n", c);
            exit(EXIT_FAILURE);
        }
    }

    struct Token eof = {.kind = TK_EOF};
    tokens[t] = eof;

    return tokens;
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

        // Strip file extension
        size_t len = strlen(argv[2]);
        size_t len_stripped = len - 3;

        if (strcmp(argv[2] + len_stripped, ".sl") != 0) {
            fprintf(stderr, "ERROR: Expected a .sl file, got '%s'.\n", argv[2]);
            return EXIT_FAILURE;
        }

        char *path = malloc(len_stripped + 1);
        strncpy(path, argv[2], len_stripped);
        path[len_stripped] = '\0';

        // 1. Read source file.
        char *source = read_file(argv[2]);
        if (source == NULL) {
            fprintf(stderr, "ERROR: Failed to read file '%s'.\n", argv[2]);
            return EXIT_FAILURE;
        }

        // 2. Lex into tokens.
        struct Token *tokens = lex(source);
        for (struct Token t = *tokens; t.kind != TK_EOF; t = *++tokens) {
            if (t.kind == TK_INTEGER) {
                printf("%d ", t.value);
            }
            else {
                printf("%.*s ", (int)t.span.length, t.span.data);
            }
        }
        putchar('\n');
        
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
