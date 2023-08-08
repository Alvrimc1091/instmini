#include "commands.h"

const CommandInfo commandTable[] = {
    {"T", "Get temperature", 0},
    {"?", "Get status", 0},
    {"fxxxxx.xxxxx", "Set frequency", 1}, // Indicate that the command requires a value
    // Add more commands here
};

int getCommandCount() {
    return sizeof(commandTable) / sizeof(commandTable[0]);
}
