`timescale 1ns/1ps

module tb_flower_level1;

    logic water, sun, bloom;

    flower_level1 dut (
        .water(water),
        .sun(sun),
        .bloom(bloom)
    );

    int errors;

    task automatic check(input logic w, input logic s, input logic exp, input string name);
        water = w;
        sun   = s;
        #1;
        if (bloom !== exp) begin
            $display("FAIL %s: water=%0b sun=%0b bloom=%0b expected %0b", name, w, s, bloom, exp);
            errors++;
        end else begin
            $display("PASS %s: water=%0b sun=%0b bloom=%0b", name, w, s, bloom);
        end
    endtask

    initial begin
        errors = 0;
        check(0, 0, 0, "00");
        check(0, 1, 0, "01");
        check(1, 0, 0, "10");
        check(1, 1, 1, "11");

        if (errors == 0)
            $display("LEVEL1 TESTBENCH PASSED");
        else
            $display("LEVEL1 TESTBENCH FAILED (%0d errors)", errors);

        $finish;
    end

endmodule
