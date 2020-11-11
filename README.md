After reading a post on [iosoft.blog](https://iosoft.blog/) about the
[Raspberry Pi SMI interface](https://iosoft.blog/2020/07/16/raspberry-pi-smi/)
I wanted to test out using the interface for exchanging data with a FPGA.

This project involves some hardware and software (in verilog and python)
designed to test out the interface. There is no specific application for the
project (although I'm open to suggestions).


# Hardware

As described on the [iosoft blog post](https://iosoft.blog/2020/07/16/raspberry-pi-smi/)
SMI can use almost all the Pi GPIO pins. The only non-SMI pins are BCM pins 26 and 27.
A [FPGA hat](lattice_fpga_dev_board) was designed that connects to:

- all SMI pins
- BCM pin 27 as CRESET: to reset the FPGA
- BCM pin 26 as CDONE: to signify the FPGA programming is done
- 5V and GND for power

See [pinouts.csv](docs/pinouts.csv) for a full pinout table. Depending on what
Pi gpio pins your FPGA design uses you may have to disable several Pi interfaces
by modifying /boot/config.txt, removing kernel modules, and/or directly changing
gpio modes.

:exclamation: WARNING :exclamation: It is possible to have the Pi and FPGA fight
to drive pins which can cause regulators to get hot and magic blue smoke to escape.

The hat uses a lattice ice40-up5k in a 48-pin QFN package. The remaining FPGA pins
connect to:

- RGB led (using up5k led drivers)
- a 2x6 PMOD connector (:exclamation: WARNING :exclamation: the power and ground are swapped on the current design)

The hat does not include an oscillator and instead the up5k internal oscillator should be used.


## FPGA bitstream

For generating bitstreams the open source [icestorm](http://www.clifford.at/icestorm/) and [nextpnr](https://github.com/YosysHQ/nextpnr) tools were used.
The hat also does not include spi flash to hold the FPGA bitstream and the SPI_SS
pin of the FPGA is pulled low with a 10K resistor. To load a bitstream onto the
FPGA the Pi pins must be setup for SPI and the bistream sent to the FPGA using
a [custom python script](program.py) (similar to iceprog).

```bash
# enable SPI
sudo dtparam spi=on
# run in the same directory as program.py and provide a path to your bitstream file
python3 program.py bitstream.bit
```


# Software

The software for the project includes verilog and python code. The python
[program.py](program.py) script is used to reset and program the FPGA over
SPI. Other python scripts are included in some example project directories:

- [blink](blink): blink FPGA RGB leds
- [testpins](testpins): test (almost) all FPGA/Pi connections
- [spi](spi): FPGA as spi peripheral
- [spram](spram): read FPGA SPRAM over spi
- [smi](smi): read incrementing counter on FPGA over smi

Each example project includes verilog code, a Makefile for building the bitstream and
some contain python scripts for testing/interacting with the programmed FPGA.


# SMI Notes

## Using the SMI character device linux kernel modules

All of the testing used the [bcm2835_smi](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/include/linux/broadcom/bcm2835_smi.h) and smi-dev kernel modules.
To load the modules several Pi peripherals must be disabled (i2c, spi, uart, etc).
When correctly loaded a character device should appear at /dev/smi
This character device can be read from to initiate reads on the SMI bus and
written to to initiate writes on the SMI bus. Settings can be changed by
issuing ioctl system calls.
Setting descriptions can be found in [bcm2835_smi.h](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/include/linux/broadcom/bcm2835_smi.h#L68).
Defaults for these settings can be found in [bcm2835_smi.c](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/drivers/misc/bcm2835_smi.c#L128).
The ioctl magic number is [0x1](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/include/linux/broadcom/bcm2835_smi.h#L48)
and 3 types of requests are accepted:

- 0x0100: get settings
- 0x0101: set settings
- 0x0102: address

Get/set settings expect a Settings struct/Structure (as described in [bcm2835_smi.h](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/include/linux/broadcom/bcm2835_smi.h#L68))
Address accepts an (up to 6 bit) address that will be asserted on the SMI bus
during read/write cycles.


## Pin electrical specs

### Address pins

SA5:SA0 are normally high (3.3 volts) and are asserted just prior to and
slightly after a read/write cycle (see the smi settings setup, hole, pace,
and strobe settings). SA5 is the most significant bit and a 0 address bit
results in a low (0 volt) signal. With the default settings the address
bus asserts ~8 ns prior to the read/write signal (see below) and deasserts
~8 ns after the read/write signal inactivates.

It seems like the smi driver is OK with not commanding all address pins
which could open up a few signals on the Pi.


### Control pins [SOE/SE, SWE/SRW]

SOE/SE is normally high and goes low during a read cycle

SWE/SRW is normally high and goes low during a write cycle

For both signals and default settings the low period is ~24 ns.


### Data pins

:exclamation: So far only pins SD0 to SD15 have been tested

These pins appear to be driven low when not in a read/write cycle which
means the FPGA must release (put into high-z) these pins when not
in a read cycle.

I'm not sure at what edge of SOE/SE the Pi reads the data pins but based
off NAND datasheets and iosoft notes I think it's the rising edge of SOE/SE.
This gives the FPGA ~24 ns from falling edge and ~32 ns from address
assertion to assert the data lines.
