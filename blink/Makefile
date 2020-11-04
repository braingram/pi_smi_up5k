# modified from fomu workshop blink example:
# https://github.com/im-tomu/fomu-workshop

YOSYSFLAGS?= 
PNRFLAGS  ?= --up5k --package sg48 --pcf blink.pcf

# Default target: build bitstream file
all: blink.bit
	@true

.DEFAULT: all

# Use *Yosys* to generate the synthesized netlist.
# This is called the **synthesis** and **tech mapping** step.
blink.json: blink.v
	yosys \
		$(YOSYSFLAGS) \
		-p 'synth_ice40 -top top -json blink.json' blink.v

# Use **nextpnr** to generate the FPGA configuration.
# This is called the **place** and **route** step.
blink.asc: blink.json blink.pcf
	nextpnr-ice40 \
		$(PNRFLAGS) \
		--json blink.json \
		--asc blink.asc

# Use icepack to convert the FPGA configuration into a "bitstream" loadable onto the FPGA.
# This is called the bitstream generation step.
blink.bit: blink.asc
	icepack blink.asc blink.bit

# use progam.py to load bitstream onto up5k using SPI
load: blink.bit
	python3 program.py blink.bit

.PHONY: load

# Cleanup the generated files.
clean:
	-rm -f blink.json 	# Generate netlist
	-rm -f blink.asc 	# FPGA configuration
	-rm -f blink.bit 	# FPGA bitstream

.PHONY: clean
