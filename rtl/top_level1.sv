// FPGA wrapper for Level 1. Students should not need to edit this file.
module top_level1 (
    input  logic       clk,
    input  logic [1:0] sw,
    input  logic       btnc,
    input  logic       btnu,
    output logic [2:0] led,
    output logic       uart_tx
);

    logic reset, water, sun, bloom;

    sync_debounce u_rst (
        .clk(clk), .reset(1'b0), .noisy(btnc), .clean(reset)
    );
    sync_debounce u_w (
        .clk(clk), .reset(reset), .noisy(sw[0]), .clean(water)
    );
    sync_debounce u_s (
        .clk(clk), .reset(reset), .noisy(sw[1]), .clean(sun)
    );

    flower_level1 u_flower (
        .water(water),
        .sun(sun),
        .bloom(bloom)
    );

    assign led[0]  = bloom;
    assign led[1]  = 1'b0;
    assign led[2]  = 1'b0;
    assign uart_tx = 1'b1;

    // btnu unused in Level 1; port exists so the same .xdc works for both tops.

endmodule
