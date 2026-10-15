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

    // btnu unused in Level 1; port exists so the same .xdc works for both tops.

    // Same byte format as top_level2: 8'h30 + {sun, water, state_code},
    // with state_code 0 (SEED) or 2 (BLOOM).
    logic        uart_busy, uart_send;
    logic [23:0] div;
    logic [7:0]  uart_data;

    assign uart_data = 8'h30 + {4'd0, sun, water, bloom, 1'b0};

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
