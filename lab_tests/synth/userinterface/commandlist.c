#include "commands.h"

const CommandInfo commandTable[] = {
    {"?", "Report Status - Bits. D0 = 100MHz Lock, D1 = YIG PLL, D6 = Self Test, D7 = NOVO Lock", NULL},
    {"fxxxx", "Set frequency (e.g. F12345.678900)", "xxxxx"}, // Indicate placeholder for value
    {"L", "Set Level of RF Power Option (Only Option G)", "xx.xx"},
    {"MR", "Recall a user saved frequency setting from memory location (e.g. MR25)", "xx"},
    {"MS", "Save current frequency settinf of unit to memory location (e.g. MS75)", "xx"},
    {"POWERON", "Turns ON internal supplies related to +15V input (default = on power up", NULL},
    {"POWEROFF", "Turns OFF internal supplies related to +15V input (Low power state)", NULL},
    {"R", "Read a NOVO location (e.g. R0)", "xx"},
    {"SP", "Synthesizer preset to factory settings", NULL},
    {"SR", "Soft PIC reset", NULL},
    {"ST", "Self test (1 = Pass, 0 = Fail)", NULL},
    {"T", "Read internal temperature (0-60°C)", NULL},
    {"V1", "Read YIG PLL V (1-12V, 6.75V = normal)", NULL},
    {"V2", "Read 100MHz PLL V (1-12V, 5.00V = normal)", NULL},
    {"V3", "Read internal +2.5V (2.50V = normal)", NULL},
    {"V4", "Read internal +3.3V (3.30V = normal)", NULL},
    {"V5", "Read internal +5.0V (5.00V = normal)", NULL},
    {"V6", "Read internal +6.75V (6.75V = normal)", NULL},
    {"V7", "Read internal +12.0V (12.00V = normal)", NULL},
    {"V8", "Read internal +13.5V (13.50V = normal)", NULL},
    {"V9", "Read internal -5.0V (-5.00V = normal)", NULL},
    {"R0000", "Model Number", NULL},
    {"R0001", "Serial Number", NULL},
    {"R0002", "Internal Xtal Serial Number (Optional)", NULL},
    {"R0003", "Fmin, in MHz", NULL},
    {"R0004", "Fmax, in MHz", NULL},
    {"R0005", "Current Internal Reference Frequency Setting - MHz", NULL},
    {"R0006", "RFmin, in dBm", NULL},
    {"R0007", "RFmax, in dBm", NULL},
    {"R0008", "Temp min, in °C", NULL},
    {"R0009", "Temp max, in °C", NULL},
    {"R0010", "highest Temp reached, in °C", NULL},
    {"R0011", "NOVO State - Locked/Unlocked", NULL},
    {"R0012", "Firmware Version & date ", NULL},
    {"R0013", "Unit Health Status - Good or Self test failure information", NULL},
    {"R0014", "Unit Calibration Status - Yes/No", NULL},
    {"R0015", "Self Test Results - Pass/Fail", NULL},
    {"R0016", "Current Output Frequency Setting - MHz", NULL},
    {"R0017", "Internal Xtal Setting - Int or Ext or ExtXtal", NULL},
    {"R0018", "Xtal DAC # (Hex)", NULL},
    {"R0019", "Coarse DAC Fmin cal # (Hex)", NULL},
    {"R0020", "Coarse DAC Fmax cal # (Hex)", NULL},
    {"R0021", "Current Coarse DAC setting (Hex)", NULL},
    {"R0022", "Current Fine DAC interpolated setting (Hex)", NULL},
    {"R0023", "Current Loop Gain (CP) setting, 0-31 (Dec)", NULL},
    {"R0024", "Current Microwave Divider (DV) setting, 1, 2, 4, 8 (Dec)", NULL},
    {"R0025", "Current Reference divider setting", NULL},
    {"R0026", "Coarse Cal status - Yes/No", NULL},
    {"R0027", "Fine Cal status - Yes/No", NULL},
    {"R0028", "Xtal Cal status - Yes / No / N/A", NULL},
    {"R0029", "External reference freq. in MHz for 100 MHz PLL (ExtXtal mode)", NULL},
    {"R0030", "Curren loop gain (LG) setting - 0-127 (DEC), U29 gain setting", NULL},
    {"R0031", "Customer part number, if shown on P.O.", NULL},
    {"R0032", "Frequency resolution in MHz (or Step Size)", NULL},
    {"R0033", "Spurious Spec., in dBc", NULL},
    {"R0034", "Harmonics Spec., in dBc", NULL},
    {"R0035", "Phase Noise Spec @ 100 Hz Offset, in dBc/Hz", NULL},
    {"R0036", "Phase Noise Spec @ 1 kHz Offset, in dBc/Hz", NULL},
    {"R0037", "Phase Noise Spec @ 10 kHz Offset, in dBc/Hz", NULL},
    {"R0038", "Phase Noise Spec @ 100 kHz Offset, in dBc/Hz", NULL},
    {"R0039", "Phase Noise Spec @ 1 MHz Offset, in dBc/Hz", NULL},
    {"R0040", "Switching Speed, any step, in mS", NULL},
    {"R0041", "+15V Supply current Max, in mA", NULL},
    {"R0042", "+5V Supply current Max, in mA", NULL},
    {"R0043", "Level Control Option installed?", NULL},
    {"R0044", "Level Control Maximum Power Limit, in dB", NULL},
    {"R0045", "Level Control Minimum Power Limit, in dB", NULL},
    {"R0046", "Level Control Cal Point Frequency Setp (Cal data taken every - ___ MHz", NULL},
    {"R0047", "Level Control Cal Point Level Step (Cal data taken every - ___ dB", NULL},
    {"R0048", "Current RF Level Setting, in dBm", NULL},
    {"R0049", "Current Level DAC setting (Hex, ASCII)", NULL},
    {"R0050", "Level Control CAL Status (Is Level Option calibrated", NULL},
    {"R0051", "Level flatness Spec. in +/- dB", NULL},
    {"R0058", "MLWI Sales (Job) number", NULL},
    {"R0059", "MLWI Product Outline Drawing and # Revision", NULL},
    {"R0060", "Power State (Power supplies on or off) On power-up will default to ON", NULL},
    {"Ry", "User Saved / Recalled frequency setting locations (e.g. R200-R299)", "y"},
    {"Rw", "Config data backup safe area, SF - save factory stores data here (e.g. R900-R960)", "w"},
    {"Rz", "DAC cal data, stored in 25 MHz increments, Fmin-100 to Fmax+100 MHz, 8000 Nom. (e.g. R1000-R2047", "z"},
    // Add more commands here
};

int getCommandCount() {
    return sizeof(commandTable) / sizeof(commandTable[0]);
}
