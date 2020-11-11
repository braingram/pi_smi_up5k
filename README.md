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
