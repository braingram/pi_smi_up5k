// spi spram reader


module top (
    // address lines appear to be pulled up and are asserted just prior to
    // SOE/SWE
    input SMI_SA5,
    input SMI_SA4,
    input SMI_SA3,
    input SMI_SA2,
    input SMI_SA1,
    input SMI_SA0,
    // SOE: pi reading from SD lines
    input SMI_SOE,
    // SWE: pi writing outputing to SD lines
    input SMI_SWE,
    // SD lines appear to be driven after a pi write (maybe floating)
    // after a pi read they seem to stay low (maybe floating)
    output SMI_SD0,
    output SMI_SD1,
    output SMI_SD2,
    output SMI_SD3,
    output SMI_SD4,
    output SMI_SD5,
    output SMI_SD6,
    output SMI_SD7,
    output SMI_SD8,
    output SMI_SD9,
    output SMI_SD10,
    output SMI_SD11,
    output SMI_SD12,
    output SMI_SD13,
    output SMI_SD14,
    output SMI_SD15,
    output SMI_SD16,
    output SMI_SD17
);
    // setup internal 48MHz oscillator
    wire clk;
    SB_HFOSC inthosc (
        .CLKHFPU(1'b1),  // power-up
        .CLKHFEN(1'b1),  // enable
        .CLKHF(clk)  // output
    );

	// increment value at some rate (24 MHz)
    //assign inthosc.CLKHF_DIV = 2'b11; // divide by 1/2/4/8
    defparam inthosc.CLKHF_DIV = "0b01"; // divide by 1/2/4/8

	reg [15:0] counter = 0;

	always @(posedge clk) begin
		counter <= counter + 1;
	end

	wire ce;

	assign ce = {SMI_SA5, SMI_SA4, SMI_SA3, SMI_SA2, SMI_SA1, SMI_SA0} === 6'b101010;

	wire [15:0] o_data;

	assign {
		SMI_SD15, SMI_SD14, SMI_SD13, SMI_SD12,
		SMI_SD11, SMI_SD10, SMI_SD9, SMI_SD8,
		SMI_SD7, SMI_SD6, SMI_SD5, SMI_SD4,
		SMI_SD3, SMI_SD2, SMI_SD1, SMI_SD0
	} = o_data;

	always @(negedge SMI_SOE) begin
		if (ce) begin
			o_data <= counter;
		end else begin
			o_data <= 16'b0;
		end
	end
endmodule
