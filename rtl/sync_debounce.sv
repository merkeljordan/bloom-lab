// Synchronize and debounce an asynchronous button/switch.
module sync_debounce #(
    parameter int STABLE_CYCLES = 200_000 // ~2 ms at 100 MHz
) (
    input  logic clk,
    input  logic reset,
    input  logic noisy,
    output logic clean
);

    logic sync_0, sync_1;
    logic [17:0] count;
    logic stable;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            sync_0 <= 1'b0;
            sync_1 <= 1'b0;
        end else begin
            sync_0 <= noisy;
            sync_1 <= sync_0;
        end
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            count  <= '0;
            stable <= 1'b0;
        end else if (sync_1 == stable) begin
            count <= '0;
        end else begin
            count <= count + 18'd1;
            if (count >= STABLE_CYCLES[17:0]) begin
                stable <= sync_1;
                count  <= '0;
            end
        end
    end

    assign clean = stable;

endmodule
