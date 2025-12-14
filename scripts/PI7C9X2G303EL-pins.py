pins = """
A2 NC C35 NC AA35 CGND AR21 TEST6
A4 NC D1 NC AB1 NC AR23 PL_512B
A6 NC D37 NC AB37 REFCLKO_P[2] AR25 NC
A8 NC E3 VDDR AC3 NC AR27 NC
A10 PETP[0] E35 VDDR AC35 NC AR29 CLKBUF_PD
A12 PETN[0] F1 DWNRST_L[1] AD1 TEST4 AR31 VDDR
A14 NC F37 NC AD37 REFCLKO_N[2] AR33 NC
A16 NC G3 NC AE3 RXPOLINV_DIS AR35 NC
A18 REXT G35 TRST_L AE35 REFCLKI_P AT1 NC
A20 NC H1 NC AF1 TEST5 AT37 NC
A22 REFCLKN H37 TMS AF37 NC AU2 NC
A24 REFCLKP J3 DWNRST_L[2] AG3 NC AU4 NC
A26 PERN[2] J35 TDI AG35 SCAN_EN AU6 GPIO[1]
A28 PERP[2] K1 NC AH1 SMBCLK AU8 GPIO[2]
A30 NC K37 TCK AH37 REFCLKI_N AU10 GPIO[4]
A32 NC L3 VDDR AJ3 PWR_SAV AU12 GPIO[5]
A34 NC L35 VDDC AJ35 EECLK AU14 GPIO[7]
A36 NC M1 PERST_L AK1 SMBDATA AU16 SLOT_IMP[2]
B1 NC M37 DGND AK37 EEPD AU18 NC
B37 NC N3 TEST1 AL3 NC AU20 NC
C3 NC N35 TDO AL35 PORTSTATUS[1] AU22 NC
C5 NC P1 VDDCAUX AM1 NC AU24 NC
C7 NC P37 REFCLKO_P[0] AM37 PORTSTATUS[2] AU26 NC
C9 PERP[0] R3 VDDCAUX AN3 NC AU28 NC
C11 PERN[0] R35 IREF AN35 VDDC AU30 DGND
C13 NC T1 TEST2 AP1 NC AU32 VDDR
C15 REXT_GND T37 REFCLKO_N[0] AP37 PORTSTATUS[0] AU34 NC
C17 AVDDH U3 VAUX AR3 NC AU36 NC
C19 AGND U35 NC AR5 NC T AVDD
C21 AGND V1 TEST3 AR7 SLOTCLK B VDDC
C23 PETN[2] V37 REFCLKO_P[1] AR9 GPIO[0] R CVDDR
C25 PETP[2] W3 VC1_EN AR11 GPIO[3] L VDDC
C27 PETN[1] W35 CGND AR13 GPIO[6] GND VSS
C29 PETP[1] Y1 PRSNT[1] AR15 SLOT_IMP[1]
C31 PERN[1] Y37 REFCLKO_N[1] AR17 NC
C33 PERP[1] AA3 PRSNT[2] AR19 VDDR
"""

header = """(symbol "PI7C9X2G303EL"
	(exclude_from_sim no)
	(in_bom yes)
	(on_board yes)
	(property "Reference" "U"
		(at 0 2.54 0)
		(effects
			(font (size 1.27 1.27))
		)
	)
	(property "Value" ""
		(at 0 0 0)
		(effects
			(font (size 1.27 1.27))
		)
	)
	(property "Footprint" ""
		(at 0 0 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Datasheet" ""
		(at 0 0 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Description" ""
		(at 0 0 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "ki_locked" ""
		(at 0 0 0)
		(effects
			(font (size 1.27 1.27))
		)
	)
	(symbol "PI7C9X2G303EL_1_1\""""

pin_template = """
		(pin PIN_TYPE line
			(at 0 -PIN_Y 0)
			(length 5.08)
			(name "PIN_NAME"
				(effects
					(font (size 1.27 1.27))
				)
			)
			(number "PIN_NUM"
				(effects
					(font (size 1.27 1.27))
				)
			)
		)"""

footer = """
	)
	(embedded_fonts no)
)"""


pin_mixed_list = pins.replace("\n", " ").split(" ")
key = ""
val = False
pin_table = {}
for pin in pin_mixed_list:
    if pin:
        if not val:
            key = pin
            val = True
        else:
            pin_table[key] = pin
            val = False


output = header

pin_y = 0
seen_nums = []
for num, name in pin_table.items():

    rendered_template = pin_template

    if name.count("["):
        
        name, index = name.split("[")
        index = int(index[:-1])

        if name[-2:] == "_N":
            name = f"{name[:-2]}_{index}_N"
        elif name[-2:] == "_P":
            name = f"{name[:-2]}_{index}_P"
        else:
            name = f"{name}{index}"
    
    print(str(num).ljust(10), name)

    if name == "NC":
        rendered_template = rendered_template.replace("PIN_TYPE", "no_connect")
    elif name in ("VDDC", "VDDR", "VDDCAUX", "VAUX", "AVDDH", "AVDD"):
        rendered_template = rendered_template.replace("PIN_TYPE", "power_in")
    else:
        rendered_template = rendered_template.replace("PIN_TYPE", "passive")

    rendered_template = rendered_template.replace("PIN_NAME", name)
    rendered_template = rendered_template.replace("PIN_NUM", num)
    rendered_template = rendered_template.replace("PIN_Y", str(pin_y))

    output += rendered_template

    pin_y = round(pin_y + 2.54, 2)
    assert num not in seen_nums
    seen_nums.append(num)
    

output += footer

with open("pins.txt", "w") as file:
    file.write(output)
