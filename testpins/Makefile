# modified from fomu workshop blink example:
# https://github.com/im-tomu/fomu-workshop

YOSYSFLAGS?= 
PNRFLAGS  ?= --up5k --package sg48 --pcf testpins.pcf

# Default target: build bitstream file
all: testpins.bit
	@true

.DEFAULT: all

# Use *Yosys* to generate the synthesized netlist.
# This is called the **synthesis** and **tech mapping** step.
testpins.json: testpins.v
	yosys \
		$(YOSYSFLAGS) \
		-p 'synth_ice40 -top top -json testpins.json' testpins.v

# Use **nextpnr** to generate the FPGA configuration.
# This is called the **place** and **route** step.
testpins.asc: testpins.json testpins.pcf
	nextpnr-ice40 \
		$(PNRFLAGS) \
		--json testpins.json \
		--asc testpins.asc

# Use icepack to convert the FPGA configuration into a "bitstream" loadable onto the FPGA.
# This is called the bitstream generation step.
testpins.bit: testpins.asc
	icepack testpins.asc testpins.bit

# use progam.py to load bitstream onto up5k using SPI
load: testpins.bit
	python3 program.py testpins.bit

.PHONY: load

# Cleanup the generated files.
clean:
	-rm -f testpins.json 	# Generate netlist
	-rm -f testpins.asc 	# FPGA configuration
	-rm -f testpins.bit 	# FPGA bitstream

.PHONY: clean
