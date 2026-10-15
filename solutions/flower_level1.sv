// Instructor reference — Level 1
module flower_level1 (
    input  logic water,
    input  logic sun,
    output logic bloom
);

    assign bloom = water & sun;

endmodule
