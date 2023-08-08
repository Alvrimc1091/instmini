#include "commands.h"

const CommandInfo commandTable[] = {
    {"T", "Get temperature", NULL},
    {"?", "Get status", NULL},
    {"fxxxxx.xxxxx", "Set frequency", "xxxxx.xxxxx"}, // Indicate placeholder for value
    {"oxxx", "Other command with value", "xxx"},
    // Add more commands here
};

int getCommandCount() {
    return sizeof(commandTable) / sizeof(commandTable[0]);
}
