import sys

comandos_disponibles = {
    "comando1": {
        "comando": "?",
        "funcion": "Report Status – Bits, D0 = 100 MHz lock, D1 = YIG PLL, D6 = self test,
                    D7 = NOVO lock",
        "comentario": "Typical return = 11000011",
    },
    "comando2": {
        "comando": "F",
        "funcion": "Frequency (ASCII) (Dec. #)",
        "comentario": "ASCII freq in MHz: xxxxx.xxxxxx; (example: F12345.678900)",
    },
    "comando3": {
        "comando": "L",
        "funcion": "Set Level of RF Power option (Option G)",
        "comentario": "Sets the Leveling DAC to a specific Level (L-0.5) (L9.5)",
    },
    "comando4": {
        "comando": "MR",
        "funcion": "Recall a user saved frequency setting from memory location (MR25)",
        "comentario": "0-99, stored @ NOVO location 200-299",
    },
    "comando5": {
        "comando": "MS",
        "funcion": "Save current frequency setting of unit to memory location (MS75)",
        "comentario": "0-99, stored @ NOVO location 200-299",
    },
    "comando6": {
        "comando": "POWERON",
        "funcion": "Turns ON internal supplies related to +15V input",
        "comentario": "Turns ON YIG / PLL / Analog supplies. (default = on power up)",
    },
    "comando7": {
        "comando": "POWEROFF",
        "funcion": "Turns OFF internal supplies related to +15V input (Low power state)",
        "comentario": "Digital logic and Xtal Osc. Supplies are always on",
    },
    "comando8": {
        "comando": "R",
        "funcion": "Read a NOVO location",
        "comentario": "R0 returns model number",
    },
    "comando9": {
        "comando": "SP",
        "funcion": "Synthesizer preset to factory settings.",
        "comentario": "Copy NOVO Loc. 900-960 to 0-60",
    },
    "comando10": {
        "comando": "SR",
        "funcion": "Soft PIC Reset",
        "comentario": "Reset PIC, clear var. run PIC code from start; (example: SR)",
    },
    "comando11": {
        "comando": "ST",
        "funcion": "Self Test",
        "comentario": "Execute internal test; 1 = Pass; (example: SR, then read data)",
    },
    "comando12": {
        "comando": "SR",
        "funcion": "Soft PIC Reset",
        "comentario": "Reset PIC, clear var. run PIC code from start; (example: SR)",
    },
    "comando13": {
        "comando": "T",
        "funcion": "Read internal temp.",
        "comentario": "Returns ASCII chars, reading in Deg. C; (example: T, then read
                        data)",
    },
    "comando14": {
        "comando": "V1",
        "funcion": "Read YIG PLLV (typical Range = 1V to 12V)",
        "comentario": "6.75V = normal; (example: V1, then read data)",
    },
    "comando15": {
        "comando": "V2",
        "funcion": "Read 100 MHz PLL V (typical Range = 1V to 12V)",
        "comentario": "5.00V = normal; (example: V2, then read data)",
    },
    "comando16": {
        "comando": "V3",
        "funcion": "Read internal +2.5V voltage",
        "comentario": "2.50V = normal; (example: V3, then read data)",
    },
    "comando17": {
        "comando": "V3",
        "funcion": "Read internal +2.5V voltage",
        "comentario": "2.50V = normal; (example: V3, then read data)",
    },
    "comando18": {
        "comando": "V4",
        "funcion": "Read internal +3.3V voltage",
        "comentario": "3.30V = normal; (example: V4, then read data)",
    },
    "comando19": {
        "comando": "V5",
        "funcion": "Read internal +5.0V voltage",
        "comentario": "5.00V = normal; (example: V5, then read data)",
    },
    "comando20": {
        "comando": "V6",
        "funcion": "Read internal +6.75V voltage",
        "comentario": "6.75V = normal; (example: V6, then read data)",
    },
    "comando21": {
        "comando": "V7",
        "funcion": "Read internal +12.0V voltage",
        "comentario": "12.00V = normal; (example: V7, then read data)",
    },
    "comando22": {
        "comando": "V8",
        "funcion": "Read internal +13.5V voltage",
        "comentario": "13.50V = normal; (example: V8, then read data)",
    },
    "comando23": {
        "comando": "V9",
        "funcion": "Read internal -5.0V voltage",
        "comentario": "-5.00V = normal; (example: V9, then read data)",
    },
    "comando24": {
        "comando": "R0000",
        "funcion": "Model Number (Example = R0) Read Location 0.",
        "comentario": "MLSP-0208CD ("W" blocked with NOVO locked.) (R/W =
                    16 Bytes)",
    },
    "comando25": {
        "comando": "R0001",
        "funcion": "Serial Number",
        "comentario": "0002",
    },
    "comando26": {
        "comando": "R0002",
        "funcion": "Internal Xtal Serial Numer (Optional)",
        "comentario": "0940-002",
    },
    "comando27": {
        "comando": "R0003",
        "funcion": "Fmin, in MHz",
        "comentario": "2000 (unit is tunable 100.0 MHz below Fmin.)",
    },
    "comando28": {
        "comando": "R0004",
        "funcion": "Fmax, in MHz",
        "comentario": "8000 (unit is tunable 100.0 MHz above Fmax.)",
    },
    "comando29": {
        "comando": "R0005",
        "funcion": "Current Internal Reference Frequency Setting - MHz",
        "comentario": "R# = 1 – 200 MHz, typ. = 100",
    },
    "comando30": {
        "comando": "R0006",
        "funcion": "RF min, in dBm",
        "comentario": "10.0",
    },
    "comando31": {
        "comando": "R0007",
        "funcion": "RF max, in dBm",
        "comentario": "15.0",
    },
    "comando32": {
        "comando": "R0008",
        "funcion": "Temp min, in Deg. C",
        "comentario": "0",
    },
    "comando33": {
        "comando": "R0009",
        "funcion": "Temp max, in Deg. C",
        "comentario": "60",
    },
    "comando34": {
        "comando": "R0010",
        "funcion": "Highest Temp reached, in Deg. C",
        "comentario": "59.8",
    },
    "comando35": {
        "comando": "R0011",
        "funcion": "NOVO State - Locked/Unlocked",
        "comentario": "Locked",
    },
    "comando36": {
        "comando": "R0012",
        "funcion": "Firmware Version & date",
        "comentario": "1.5 Nov 16 2011",
    },
    "comando37": {
        "comando": "R0013",
        "funcion": "Unit Health Status - "Good" or Self test failure information",
        "comentario": "Good or Fail V5 as example",
    },
    "comando38": {
        "comando": "R0014",
        "funcion": "Unit Calibration Status - Yes/No",
        "comentario": "Yes",
    },
    "comando39": {
        "comando": "R0015",
        "funcion": "Self Test Results - Pass/Fail",
        "comentario": "Pass",
    },
    "comando40": {
        "comando": "R0016",
        "funcion": "Current Output Frequency setting - MHz",
        "comentario": "2500",
    },
    "comando41": {
        "comando": "R0017",
        "funcion": "Internal Xtal Setting – Int or Ext or ExtXtal",
        "comentario": "ExtXtal (3 modes; Internal Xtal, External and External with Xtal.)",
    },
    "comando42": {
        "comando": "R0018",
        "funcion": "Xtal DAC cal # (Hex)",
        "comentario": "0000-FFFF",
    },
    "comando43": {
        "comando": "R0019",
        "funcion": "Coarse DAC Fmin cal # (Hex)",
        "comentario": "0000-FFFF",
    },
    "comando44": {
        "comando": "R0020",
        "funcion": "Coarse DAC Fmax cal # (Hex)",
        "comentario": "0000-FFFF",
    },
    "comando45": {
        "comando": "R0021",
        "funcion": "Current Coarse DAC setting (Hex)",
        "comentario": "0000-FFFF",
    },
    "comando46": {
        "comando": "R0022",
        "funcion": "0000-FFFF, 8000 nominal",
        "comentario": "0000-FFFF, 8000 nominal",
    },
    "comando47": {
        "comando": "R0023",
        "funcion": "Current Loop Gain (CP) setting, 0-31 (Dec)",
        "comentario": "31 charge pump current",
    },
    "comando48": {
        "comando": "R0024",
        "funcion": "Current Microwave Divider (DV) setting, 1, 2 ,4 ,8 (Dec)",
        "comentario": "2 (Sets external Prescaler to 1, 2, 4, or 8)",
    },
    "comando49": {
        "comando": "R0026",
        "funcion": "Coarse Cal status; Yes / No",
        "comentario": "Yes",
    },
    "comando50": {
        "comando": "R0027",
        "funcion": "Fine Cal status; Yes / No",
        "comentario": "Yes",
    },
    "comando51": {
        "comando": "R0028",
        "funcion": "Xtal Cal status; Yes / No N/A",
        "comentario": "Yes N/A if Internal Xtal setting = Ext or ExtXtal",
    },
    "comando52": {
        "comando": "R0029",
        "funcion": "External reference freq. In MHz for 100 MHz PLL (ExtXtal mode)",
        "comentario": "i.e.: 10 = 10 MHz external reference. 1.0 MHz increments only",
    },
    "comando53": {
        "comando": "R0030",
        "funcion": "Current loop gain (LG) setting; 0-127 (Dec), U29 gain setting.",
        "comentario": "Written by PIC after LG command, read at boot and sent to U29",
    },
    "comando54": {
        "comando": "R0031",
        "funcion": "Customer part number, if shown on P.O.",
        "comentario": "123-45-6789 (Shown on unit label as PN:)",
    },
    "comando55": {
        "comando": "R0032",
        "funcion": "Frequency resolution in MHz (or Step Size)",
        "comentario": "0.001 = 1.0 kHz",
    },
    "comando56": {
        "comando": "R0033",
        "funcion": "Spurious Spec., in dBc",
        "comentario": "-60",
    },
    "comando57": {
        "comando": "R0034",
        "funcion": "Harmonics Spec., in dBc",
        "comentario": "-12",
    },
    "comando58": {
        "comando": "R0035",
        "funcion": "Phase Noise Spec. @ 100 Hz Offset, in dBc/Hz",
        "comentario": "-85",
    },
    "comando59": {
        "comando": "R0036",
        "funcion": "Phase Noise Spec. @ 1 kHz Offset, in dBc/Hz",
        "comentario": "-90",
    },
    "comando60": {
        "comando": "R0037",
        "funcion": "Phase Noise Spec. @ 10 kHz Offset, in dBc/Hz",
        "comentario": "-100",
    },
    "comando61": {
        "comando": "R0038",
        "funcion": "Phase Noise Spec. @ 100 kHz Offset, in dBc/Hz",
        "comentario": "-120",
    },
    "comando62": {
        "comando": "R0039",
        "funcion": "Phase Noise Spec. @ 1 MHz Offset, in dBc/Hz",
        "comentario": "-140",
    },
    "comando63": {
        "comando": "R0040",
        "funcion": "Switching Speed, any step, in mS",
        "comentario": "5.0",
    },
    "comando64": {
        "comando": "R0041",
        "funcion": "+15V Supply current Max, in mA",
        "comentario": "750",
    },
    "comando65": {
        "comando": "R0042",
        "funcion": "+5V Supply current Max, in mA",
        "comentario": "300",
    },
    "comando66": {
        "comando": "R0043",
        "funcion": "Level Control Option installed?",
        "comentario": "Yes/No",
    },
    "comando67": {
        "comando": "R0044",
        "funcion": "Level Control Maximum Power Limit, in dB",
        "comentario": "10.0",
    },
    "comando68": {
        "comando": "R0045",
        "funcion": "Level Control Minimum Power Limit, in dB",
        "comentario": "-10.0",
    },
    "comando69": {
        "comando": "R0046",
        "funcion": "Level Control Cal Point Frequency Step (Cal data taken every - ___ MHz)",
        "comentario": "100.0 MHz",
    },
    "comando70": {
        "comando": "R0047",
        "funcion": "Level Control Cal Point Level step (Cal data taken every - ___ dB)",
        "comentario": "1.0",
    },
    "comando71": {
        "comando": "R0048",
        "funcion": "Current RF Level Setting, in dBm",
        "comentario": "9.5",
    },
    "comando72": {
        "comando": "R0049",
        "funcion": "Current Level DAC setting (Hex, ASCII)",
        "comentario": "AF61",
    },
    "comando73": {
        "comando": "R0050",
        "funcion": "Level Control CAL Status (Is Level option calibrated)",
        "comentario": "Yes / No",
    },
    "comando74": {
        "comando": "R0051",
        "funcion": "Level flatness Spec. in +/- dB (+/- 2.0 = 4.0 total)",
        "comentario": "2.0",
    },
    "comando75": {
        "comando": "R0058",
        "funcion": "MLWI Sales (Job) number",
        "comentario": "18-0024",
    },
    "comando76": {
        "comando": "R0059",
        "funcion": "MLWI Product Outline Drawing # and Revision",
        "comentario": "181-003 G",
    },
    "comando77": {
        "comando": "R0060",
        "funcion": "Power State (Power supplies on or off) On power-up will default to ON!",
        "comentario": ""ON" or "OFF"(Low power) - Show status of "poweron" and
                    "poweroff" commands.",
    },
    "comando78": {
        "comando": "200-299",
        "funcion": "User Saved / Recalled frequency setting locations, (0-99)",
        "comentario": "Frequency stored in MHz",
    },
    "comando79": {
        "comando": "R 900-960",
        "funcion": "Config data backup safe area, SF - save factory stores data here.",
        "comentario": "Backup copy of NOVO location 0000 to 0060 (Config Data)",
    },
    "comando80": {
        "comando": "R 1000-2047",
        "funcion": "DAC cal data, stored in 25 MHz increments, Fmin-100 to Fmax+100
                    MHz, 8000 Nom.",
        "comentario": "Stored in 16 bit HEX numbers (ASCII format)",
    },

    # Agrega más comandos aquí según sea necesario
}

def imprimir_lista_comandos():
    print("Lista de comandos disponibles:")
    for comando, detalles in comandos_disponibles.items():
        print(f"Comando: {comando} ({detalles['abreviatura']})")
        print(f"Función: {detalles['funcion']}")
        print(f"Comentario: {detalles['comentario']}")
        print()

def imprimir_info_comando(comando):
    if comando in comandos_disponibles:
        detalles = comandos_disponibles[comando]
        print(f"Información del comando {comando}:")
        print(f"Función: {detalles['funcion']}")
        print(f"Comentario: {detalles['comentario']}")
    else:
        print(f"El comando {comando} no existe.")

# Obtener los argumentos de línea de comandos
args = sys.argv[1:]

# Verificar los argumentos y ejecutar el comportamiento correspondiente
if len(args) == 0:
    imprimir_lista_comandos()
else:
    comando = args[0]
    imprimir_info_comando(comando)

