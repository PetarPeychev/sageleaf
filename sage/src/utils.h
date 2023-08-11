#ifndef SAGE_UTILS_H
#define SAGE_UTILS_H

#include "types.h"

char *read_file(const char *path);

int print_to_string(char **str, const char *fmt, ...);

#endif // SAGE_UTILS_H
