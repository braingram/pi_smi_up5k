// Simple tri-colour LED blink example.
// Modified from fomu workshop blink example
// https://github.com/im-tomu/fomu-workshop

// TODO the color-to-led mapping has NOT been verified
`define BLUEPWM  RGB0PWM
`define REDPWM   RGB1PWM
`define GREENPWM RGB2PWM

module top (
    // LED outputs
    // --------
    output RGB0,
    output RGB1,
    output RGB2,
    // GPIO
    output GPIO0,
    output GPIO1,
    output GPIO2,
    output GPIO3,
    output GPIO4,
    output GPIO5,
    output GPIO6,
    output GPIO7,
    output GPIO8,
	// skip spi pins as those must work to program
	// TODO check for shorts on spi pins
    //output GPIO9,
    //output GPIO10,
    //output GPIO11,
    output GPIO12,
    output GPIO13,
    output GPIO14,
    output GPIO15,
    output GPIO16,
    output GPIO17,
    output GPIO18,
    output GPIO19,
    output GPIO20,
    output GPIO21,
    output GPIO22,
    output GPIO23,
    output GPIO24,
    input GPIO25,
);


    wire clk;
    assign clk = GPIO25;
    /*
    SB_HFOSC inthosc (
        .CLKHFPU(1'b1),
        .CLKHFEN(1'b1),
        .CLKHF(clk)
    );
    */

	localparam NBITS = 22;
    reg [NBITS-1:0] cycler = 0;
	assign {
		GPIO24, GPIO23, GPIO22, GPIO21, GPIO20,
		GPIO19, GPIO18, GPIO17, GPIO16, GPIO15,
		GPIO14, GPIO13, GPIO12,
		GPIO8, GPIO7, GPIO6, GPIO5, GPIO4,
		GPIO3, GPIO2, GPIO1, GPIO0} = cycler;

    reg [2:0] counter = 0;
    always @(posedge clk) begin
        counter <= {counter[1:0], ~|counter};
		cycler <= {cycler[NBITS-1:0], ~|cycler};
    end

    SB_RGBA_DRV #(
        .CURRENT_MODE("0b1"),       // half current
        .RGB0_CURRENT("0b000001"),  // 2 mA
        .RGB1_CURRENT("0b000001"),  // 2 mA
        .RGB2_CURRENT("0b000001")   // 2 mA
    ) RGBA_DRIVER (
        .CURREN(1'b1),
        .RGBLEDEN(1'b1),
        .`BLUEPWM(counter[2]),     // Blue
        .`REDPWM(counter[1]),      // Red
        .`GREENPWM(counter[0]),    // Green
        .RGB0(RGB0),
        .RGB1(RGB1),
        .RGB2(RGB2)
    );

endmodule
