// spi spram reader


module top (
	output SPI_MISO,
	input SPI_MOSI,
	input SPI_SCLK,
	input SPI_CE0,
	input SPI_CE1
);
    // setup internal 48MHz oscillator
    wire clk;
    SB_HFOSC inthosc (
        .CLKHFPU(1'b1),  // power-up
        .CLKHFEN(1'b1),  // enable
        .CLKHF(clk)  // output
    );
	// inthosc.CLKHF_DIV = 2'b00;  divide by 1/2/4/8

	// register to store spi value
	reg [7:0] r0 = 0;
	reg [7:0] w0 = 0;

	reg [1:0] sclk_buf = 0;
	always @(posedge clk) begin
		// buffer SPI clock
		sclk_buf = {sclk_buf[0], SPI_SCLK};
	end

	reg [3:0] bit_count = 0;
	always @(posedge clk) begin
		// if buffered SPI clock has rising edge, clock in MOSI
		if (sclk_buf[1:0] == 2'b01) begin
			r0 = {r0[6:0], SPI_MOSI};
			bit_count <= bit_count + 1;
		end
		// if buffered SPI clock has falling edge
		if (sclk_buf[1:0] == 2'b10) begin
			if (bit_count[3]) begin
				bit_count <= 0;
				//w0 <= r0;
				w0 <= rdata[7:0];
			end else begin
				w0 <= {w0[6:0], 1'b0};
			end
		end
	end

	assign SPI_MISO = w0[7];

	wire [15:0] rdata;

	SB_SPRAM256KA mem (
		.DATAIN(16'b0),
		.ADDRESS({6'b0, r0}),
		.CHIPSELECT(bit_count[3]),
		.CLOCK(clk),
		.DATAOUT(rdata),
		.MASKWREN(4'b0),
		.WREN(1'b0),
		.STANDBY(1'b0),
		.SLEEP(1'b0),
		.POWEROFF(1'b1)
	);
endmodule
