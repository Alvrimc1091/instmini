#ifndef COMMANDS_H
#define COMMANDS_H

// Structure to hold command details
typedef struct {
    const char *command;
    const char *description;
} CommandInfo;

// Define command lookup table
extern const CommandInfo commandTable[];

// Function to get the command count
extern int getCommandCount();

#endif
