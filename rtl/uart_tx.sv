// Minimal 8N1 UART transmitter (100 MHz, 115200 baud).
module uart_tx #(
    parameter int CLKS_PER_BIT = 868
) (
    input  logic       clk,
    input  logic       reset,
    input  logic       send,
    input  logic [7:0] data,
    output logic       tx,
    output logic       busy
);

    typedef enum logic [1:0] {IDLE, START, DATA, STOP} state_t;
    state_t state;
    logic [15:0] clk_cnt;
    logic [2:0]  bit_idx;
    logic [7:0]  shift;

    assign busy = (state != IDLE);

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            state   <= IDLE;
            clk_cnt <= '0;
            bit_idx <= '0;
            shift   <= '0;
            tx      <= 1'b1;
        end else begin
            unique case (state)
                IDLE: begin
                    tx      <= 1'b1;
                    clk_cnt <= '0;
                    bit_idx <= '0;
                    if (send) begin
                        shift <= data;
                        state <= START;
                    end
                end
                START: begin
                    tx <= 1'b0;
                    if (clk_cnt == CLKS_PER_BIT-1) begin
                        clk_cnt <= '0;
                        state   <= DATA;
                    end else
                        clk_cnt <= clk_cnt + 16'd1;
                end
                DATA: begin
                    tx <= shift[bit_idx];
                    if (clk_cnt == CLKS_PER_BIT-1) begin
                        clk_cnt <= '0;
                        if (bit_idx == 3'd7)
                            state <= STOP;
                        else
                            bit_idx <= bit_idx + 3'd1;
                    end else
                        clk_cnt <= clk_cnt + 16'd1;
                end
                STOP: begin
                    tx <= 1'b1;
                    if (clk_cnt == CLKS_PER_BIT-1) begin
                        clk_cnt <= '0;
                        state   <= IDLE;
                    end else
                        clk_cnt <= clk_cnt + 16'd1;
                end
                default: state <= IDLE;
            endcase
        end
    end

endmodule
