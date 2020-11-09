# modified from fomu workshop blink example:
# https://github.com/im-tomu/fomu-workshop

PROJ = spi
PCF_FILE = ../pi_smi_up5k.pcf
YOSYSFLAGS?= 
PNRFLAGS  ?= --up5k --package sg48 --pcf $(PCF_FILE)

# Default target: build bitstream file
all: $(PROJ).bit
	@true

.DEFAULT: all

# Use *Yosys* to generate the synthesized netlist.
# This is called the **synthesis** and **tech mapping** step.
%.json: %.v
	yosys $(YOSYSFLAGS) -p 'synth_ice40 -top top -json $@' $^

# Use **nextpnr** to generate the FPGA configuration.
# This is called the **place** and **route** step.
%.asc: %.json $(PCF_FILE)
	nextpnr-ice40 $(PNRFLAGS) --json $< --asc $@

# Use icepack to convert the FPGA configuration into a "bitstream" loadable onto the FPGA.
# This is called the bitstream generation step.
%.bit: %.asc
	icepack $< $@

# use progam.py to load bitstream onto up5k using SPI
load: $(PROJ).bit
	python3 ../program.py $<

# Cleanup the generated files.
clean:
	-rm -f $(PROJ).json 	# Generate netlist
	-rm -f $(PROJ).asc 	# FPGA configuration
	-rm -f $(PROJ).bit 	# FPGA bitstream


.SECONDARY:
.PHONY: load clean
