// FPGA wrapper for Level 2. Students should not need to edit this file.
module top_level2 (
    input  logic       clk,
    input  logic [1:0] sw,
    input  logic       btnc,
    input  logic       btnu,
    output logic [2:0] led,
    output logic       uart_tx
);

    logic reset, water, sun, btn_grow, both, both_rise, btn_rise, grow;
    logic [1:0] state_code;
    logic led_seed, led_sprout, led_bloom;

    sync_debounce u_rst (
        .clk(clk), .reset(1'b0), .noisy(btnc), .clean(reset)
    );
    sync_debounce u_w (
        .clk(clk), .reset(reset), .noisy(sw[0]), .clean(water)
    );
    sync_debounce u_s (
        .clk(clk), .reset(reset), .noisy(sw[1]), .clean(sun)
    );
    sync_debounce u_gbtn (
        .clk(clk), .reset(reset), .noisy(btnu), .clean(btn_grow)
    );

    assign both = water & sun;

    rise_pulse u_both (
        .clk(clk), .reset(reset), .d(both), .pulse(both_rise)
    );
    rise_pulse u_btn (
        .clk(clk), .reset(reset), .d(btn_grow), .pulse(btn_rise)
    );

    assign grow = both_rise | (btn_rise & both);

    flower_level2 u_flower (
        .clk(clk),
        .reset(reset),
        .grow(grow),
        .state_code(state_code),
        .led_seed(led_seed),
        .led_sprout(led_sprout),
        .led_bloom(led_bloom)
    );

    assign led = {led_bloom, led_sprout, led_seed};

    // About 10 times per second send 8'h30 + {sun, water, state_code}:
    // ASCII '0'..'?', so '0'/'1'/'2' still mean SEED/SPROUT/BLOOM with both switches off.
    logic        uart_busy, uart_send;
    logic [23:0] div;
    logic [7:0]  uart_data;

    assign uart_data = 8'h30 + {4'd0, sun, water, state_code};

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            div       <= '0;
            uart_send <= 1'b0;
        end else begin
            uart_send <= 1'b0;
            if (div == 24'd10_000_000) begin
                div <= '0;
                if (!uart_busy)
                    uart_send <= 1'b1;
            end else
                div <= div + 24'd1;
        end
    end

    uart_tx u_uart (
        .clk(clk),
        .reset(reset),
        .send(uart_send),
        .data(uart_data),
        .tx(uart_tx),
        .busy(uart_busy)
    );

endmodule
