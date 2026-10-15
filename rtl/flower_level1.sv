// Bloom Lab — Level 1 (tested implementation)
// Spec: bloom is 1 only when water AND sun are 1 (combinational).

module flower_level1 (
    input  logic water,
    input  logic sun,
    output logic bloom
);

    assign bloom = water & sun;

endmodule
