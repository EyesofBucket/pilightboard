#include <unistd.h>
#include <cerrno>
#undef errno
extern int errno;
// ^^^^ Add these 4 lines to your includes

// Set this to something of your choosing.
Print *volatile stdPrint = &Serial;

extern "C" {
    int _write(int file, const void *buf, size_t len) {
        if (len == 0) {
            return 0;
        }

        Print *out;

        // Send both stdout and stderr to stdPrint
        if (file == STDOUT_FILENO || file == STDERR_FILENO) {
            out = stdPrint;
        } else if (file == STDIN_FILENO) {
            errno = EBADF;
            return -1;
        } else {
            out = (Print *)file;
        }

        if (out == nullptr) {
            return len;
        }
        return out->write((const uint8_t *)buf, len);
    }
}  // extern "C"
