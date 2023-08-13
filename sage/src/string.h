#ifndef STRING_H
#define STRING_H

#include "types.h"

typedef struct
{
    u32 length;
    u32 size;
    u32 capacity;
    utf8 *data;
} String;

#define string_new(X)          \
    _Generic(                  \
        (X),                   \
        u32: str_new_from_str, \
        default: cbrt,         \
        char *: _str_new_from_cstr)(X)

String string_new_from_str(u32 capacity);
String string_new_from_cstr(char *cstr);

void string_free(String str);

#define string_equals(str, X)         \
    _Generic(                         \
        (X),                          \
        String: string_equals_string, \
        default: cbrt,                \
        char *: string_equals_cstring)(str, X)

bool string_equals_string(String str, String other);
bool string_equals_cstring(String str, char *cstr);

void string_append(String str, String other);
void string_append_cstring(String str, char *cstr);
void string_append_char(String str, char c);

#endif // STRING_H