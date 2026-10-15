// Bloom Lab — Level 2 (tested implementation)
// Spec: SEED --grow--> SPROUT --grow--> BLOOM (hold). Reset -> SEED.

module flower_level2 (
    input  logic       clk,
    input  logic       reset,
    input  logic       grow,
    output logic [1:0] state_code,
    output logic       led_seed,
    output logic       led_sprout,
    output logic       led_bloom
);

    typedef enum logic [1:0] {
        SEED,
        SPROUT,
        BLOOM
    } state_t;

    state_t state, next_state;

    always_ff @(posedge clk or posedge reset) begin
        if (reset)
            state <= SEED;
        else
            state <= next_state;
    end

    always_comb begin
        next_state = state;
        case (state)
            SEED:    if (grow) next_state = SPROUT;
            SPROUT:  if (grow) next_state = BLOOM;
            BLOOM:   next_state = BLOOM;
            default: next_state = SEED;
        endcase
    end

    always_comb begin
        led_seed   = 1'b0;
        led_sprout = 1'b0;
        led_bloom  = 1'b0;
        state_code = 2'd0;
        unique case (state)
            SEED: begin
                led_seed   = 1'b1;
                state_code = 2'd0;
            end
            SPROUT: begin
                led_sprout = 1'b1;
                state_code = 2'd1;
            end
            BLOOM: begin
                led_bloom  = 1'b1;
                state_code = 2'd2;
            end
            default: begin
                led_seed   = 1'b1;
                state_code = 2'd0;
            end
        endcase
    end

endmodule
