// Rising-edge pulse, one clock wide.
module rise_pulse (
    input  logic clk,
    input  logic reset,
    input  logic d,
    output logic pulse
);

    logic d_d;

    always_ff @(posedge clk or posedge reset) begin
        if (reset)
            d_d <= 1'b0;
        else
            d_d <= d;
    end

    assign pulse = d & ~d_d;

endmodule
