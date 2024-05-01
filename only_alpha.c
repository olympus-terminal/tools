#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        fprintf(stderr, "Error opening file: %s\n", argv[1]);
        return 1;
    }

    char output_filename[256];
    sprintf(output_filename, "%s.cleaned", argv[1]);

    FILE *output_file = fopen(output_filename, "w");
    if (!output_file) {
        fprintf(stderr, "Error creating output file: %s\n", output_filename);
        fclose(input_file);
        return 1;
    }

    int c;
    while ((c = fgetc(input_file)) != EOF) {
        if (isalpha(c) || c == ' ' || c == '\n') {
            fputc(c, output_file);
        }
    }

    fclose(input_file);
    fclose(output_file);

    return 0;
}
