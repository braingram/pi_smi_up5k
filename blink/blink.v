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
);

    wire clk;
    SB_HFOSC inthosc (
        .CLKHFPU(1'b1),
        .CLKHFEN(1'b1),
        .CLKHF(clk)
    );

    // divide down the clock
    reg [28:0] counter = 0;
    always @(posedge clk) begin
        counter <= counter + 1;
    end

    // Instantiate iCE40 LED driver hard logic, connecting up
    // counter state and LEDs.
    //
    // Note that it's possible to drive the LEDs directly,
    // however that is not current-limited and results in
    // overvolting the red LED.
    //
    // See also:
    // https://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/IK/ICE40LEDDriverUsageGuide.ashx?document_id=50668
    SB_RGBA_DRV #(
        .CURRENT_MODE("0b1"),       // half current
        .RGB0_CURRENT("0b000011"),  // 4 mA
        .RGB1_CURRENT("0b000011"),  // 4 mA
        .RGB2_CURRENT("0b000011")   // 4 mA
    ) RGBA_DRIVER (
        .CURREN(1'b1),
        .RGBLEDEN(1'b1),
        .`BLUEPWM(counter[25]),     // Blue
        .`REDPWM(counter[24]),      // Red
        .`GREENPWM(counter[23]),    // Green
        .RGB0(RGB0),
        .RGB1(RGB1),
        .RGB2(RGB2)
    );

endmodule
