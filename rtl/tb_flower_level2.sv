`timescale 1ns/1ps

module tb_flower_level2;

    logic       clk;
    logic       reset;
    logic       grow;
    logic [1:0] state_code;
    logic       led_seed, led_sprout, led_bloom;

    flower_level2 dut (
        .clk(clk),
        .reset(reset),
        .grow(grow),
        .state_code(state_code),
        .led_seed(led_seed),
        .led_sprout(led_sprout),
        .led_bloom(led_bloom)
    );

    initial clk = 0;
    always #5 clk = ~clk; // 100 MHz-like (10 ns period)

    int errors;

    task automatic step(input logic g);
        grow = g;
        @(posedge clk);
        #1;
        grow = 1'b0;
    endtask

    task automatic expect_state(input logic [1:0] exp, input string name);
        if (state_code !== exp) begin
            $display("FAIL %s: state_code=%0d expected %0d", name, state_code, exp);
            errors++;
        end else begin
            $display("PASS %s: state_code=%0d", name, state_code);
        end
    endtask

    initial begin
        errors = 0;
        grow   = 0;
        reset  = 1;
        repeat (3) @(posedge clk);
        reset  = 0;
        @(posedge clk);
        #1;
        expect_state(2'd0, "after reset (SEED)");

        // Test 2: no grow stays SEED
        repeat (4) step(0);
        expect_state(2'd0, "no grow stays SEED");

        // Test 1 first pulse
        step(1);
        expect_state(2'd1, "SEED + grow -> SPROUT");

        // Test 3: hold sprout
        repeat (3) step(0);
        expect_state(2'd1, "hold SPROUT");

        // second pulse
        step(1);
        expect_state(2'd2, "SPROUT + grow -> BLOOM");

        // Test 4: extra grow stays BLOOM
        step(1);
        expect_state(2'd2, "BLOOM holds");

        // reset again
        reset = 1;
        @(posedge clk);
        #1;
        reset = 0;
        @(posedge clk);
        #1;
        expect_state(2'd0, "reset returns to SEED");

        if (led_seed && !led_sprout && !led_bloom)
            $display("PASS LED one-hot after reset");
        else begin
            $display("FAIL LEDs after reset seed=%0b sprout=%0b bloom=%0b",
                     led_seed, led_sprout, led_bloom);
            errors++;
        end

        if (errors == 0)
            $display("LEVEL2 TESTBENCH PASSED");
        else
            $display("LEVEL2 TESTBENCH FAILED (%0d errors)", errors);

        $finish;
    end

endmodule
