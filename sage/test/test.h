 #define test_assert(message, test) do { if (!(test)) return message; } while (true)
 #define test_run(test) do { char *message = test(); tests_run++; \
                                if (message) return message; } while (true)
 extern int tests_run;