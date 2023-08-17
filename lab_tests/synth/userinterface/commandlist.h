#ifndef COMMANDS_H
#define COMMANDS_H

typedef struct {
    const char *command;
    const char *description;
    const char *valuePlaceholder; // Placeholder for value in command (if any)
} CommandInfo;

extern const CommandInfo commandTable[];

extern int getCommandCount();

#endif
