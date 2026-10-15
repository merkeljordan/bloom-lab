// Bloom Lab — Level 2 student starter
// Spec: SEED --grow--> SPROUT --grow--> BLOOM (hold). Reset -> SEED.
// `grow` is a one-cycle pulse meaning "water AND sun event".

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
            SEED: begin
                // TODO: if grow, go to SPROUT
            end
            SPROUT: begin
                // TODO: if grow, go to BLOOM
            end
            BLOOM: begin
                // TODO: stay in BLOOM
            end
            default: begin
                next_state = SEED;
            end
        endcase
    end

    always_comb begin
        led_seed   = 1'b0;
        led_sprout = 1'b0;
        led_bloom  = 1'b0;
        state_code = 2'd0;

        case (state)
            SEED: begin
                // TODO
            end
            SPROUT: begin
                // TODO
            end
            BLOOM: begin
                // TODO
            end
            default: begin
                led_seed   = 1'b1;
                state_code = 2'd0;
            end
        endcase
    end

endmodule
