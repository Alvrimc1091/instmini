#ifndef COMMANDS_H
#define COMMANDS_H

typedef struct {
    const char *command;
    const char *description;
    int requiresValue; // Indicates if the command requires a value
} CommandInfo;

extern const CommandInfo commandTable[];

extern int getCommandCount();

#endif
