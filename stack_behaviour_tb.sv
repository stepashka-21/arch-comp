`include "stack_behaviour.sv"

module stack_behaviour_easy_tb;
    output wire[3:0] O_DATA;
    reg RESET;
    reg CLK;
    reg[1:0] COMMAND;
    reg[2:0] INDEX;
    reg[3:0] I_DATA;
    event print;
    stack_behaviour_easy stack(O_DATA, RESET, CLK, COMMAND, INDEX, I_DATA);
    initial begin
        // firstly, reset
        #2 CLK = 0; RESET = 0; COMMAND[0] = 0; COMMAND[1] = 0; INDEX[0] = 0; INDEX[1] = 0; INDEX[2] = 0; I_DATA[0] = 0; I_DATA[1] = 0; I_DATA[2] = 0; I_DATA[3] = 0;
        #2 CLK = 0;  RESET = 1;
        // push 
        #2 CLK = 0;  RESET = 0; COMMAND[0] = 1; COMMAND[1] = 0; INDEX[0] = 0; INDEX[1] = 0; INDEX[2] = 0; I_DATA[0] = 1; I_DATA[1] = 0; I_DATA[2] = 0; I_DATA[3] = 0;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[1] = 1;
        #2 CLK = 1;
        // check using get
        #2 CLK = 0; COMMAND[1] = 1; INDEX[0] = 0; INDEX[1] = 0; INDEX[2] = 0;
        #2 CLK = 1;
        for (integer i = 1; i < 7; i = i + 1) begin
            #2 CLK = 0;  INDEX = i;
            #2 CLK = 1;
        end
        // continue push
        #2 CLK = 0; COMMAND[1] = 0; I_DATA[2] = 1;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[3] = 1;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[0] = 0;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[1] = 0;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[2] = 0;
        #2 CLK = 1; 
        // pop 
        #2 CLK = 0; COMMAND[0] = 0; COMMAND[1] = 1;
        for (integer i = 0; i < 9; i = i + 1) begin
            #2 CLK = 1;
            #2 CLK = 0;
        end
        #2 CLK = 1;
        // again push
        #2 CLK = 0; COMMAND[0] = 1; COMMAND[1] = 0; I_DATA[0] = 1; I_DATA[1] = 0; I_DATA[2] = 0; I_DATA[3] = 1;
        #2 CLK = 1;
        #2 CLK = 0; I_DATA[1] = 1;
        #2 CLK = 1;
        // run pop to be sure that all's correct
        #2 CLK = 0; COMMAND[0] = 0; COMMAND[1] = 1;
        for (integer i = 0; i < 4; i = i + 1) begin
            #2 CLK = 1;
            #2 CLK = 0;
        end
        #2 CLK = 1;
        // get
        #2 CLK = 0; COMMAND[0] = 1; INDEX[0] = 0; INDEX[1] = 0; INDEX[2] = 0;
        #2 CLK = 1;
        for (integer i = 1; i < 7; i = i + 1) begin
            #2 CLK=0;  INDEX = i;
            #2 CLK=1;
        end
        // finally, reset
        #2 CLK = 0; 
        #2 CLK = 0; RESET = 1;
        #2 RESET = 0;
        #2 CLK = 1; COMMAND[0] = 0;
        // and pop for checking
        #2 CLK = 0;
        for (integer i = 0; i < 3; i = i + 1) begin
            #2 CLK = 1;
            #2 CLK = 0;
        end
        #2 CLK = 1;
        // push one element
        #2 CLK = 0; COMMAND[0] = 1; COMMAND[1] = 0; I_DATA[0] = 0; I_DATA[1] = 1; I_DATA[2] = 1; I_DATA[3] = 0;
        #2 CLK = 1;
        // get
        #2 CLK = 0; COMMAND[1] = 1; INDEX[0] = 0; INDEX[1] = 0; INDEX[2] = 0;
        #2 CLK = 1;
        for (integer i = 1; i < 7; i = i + 1) begin
            #2 CLK=0;  INDEX = i;
            #2 CLK=1;
        end
    end

    initial begin
        #1 $display("Из-за того, что вывод не успевает перезаписываться с каждым тактом, пришлось делать все операции на два такта (с одним тоже работает, но тогда вывод отстает..)");
        #0 $display("Если рор, то выводит 0000, иначе значение из ячейки; print каждые 4 такта, чтобы было clk = 1 или reset = 1");
        #0 $display("Вывод в формате");
        #0 $display("CLK, RESET, COMMAND, INDEX, I_DATA, O_DATA");
        #0 $display("Сначала reset");
        #4->print;
        #0 $display("push: 0001 и 0011");
        for (integer i = 0; i < 2; i = i + 1) begin
            #4->print;
        end
        #0 $display("get по индексам от 0 до 7");
        for (integer i = 0; i < 7; i = i + 1) begin
            #4->print;
        end
        #0 $display("push: 0111, 1111, 1110, 1100, 1000 (первые две ячейки перезапишутся)");
        for (integer i = 0; i < 5; i = i + 1) begin
            #4->print;
        end
        #0 $display("pop по индексам от 0 до 10 (это два цикла, вернемся в исходную)");
        for (integer i = 0; i < 10; i = i + 1) begin
            #4->print;
        end
        #0 $display("push: 1001 и 1011");
        for (integer i = 0; i < 2; i = i + 1) begin
            #4->print;
        end
        #0 $display("pop по индексам от 0 до 5");
        for (integer i = 0; i < 5; i = i + 1) begin
            #4->print;
        end
        #0 $display("get по индексам от 0 до 7");
        for (integer i = 0; i < 7; i = i + 1) begin
            #4->print;
        end
        #0 $display("reset");
        #4->print;
        #0 $display("pop по индексам от 0 до 5");
        for (integer i = 0; i < 5; i = i + 1) begin
            #4->print;
        end
        #0 $display("push: 0110");
        #4->print;
        #0 $display("get по индексам от 0 до 7");
        for (integer i = 0; i < 7; i = i + 1) begin
            #4->print;
        end

    end

    always @(print) $display("%d \t %d \t   %b \t %b \t %b \t %b", CLK, RESET, COMMAND, INDEX, I_DATA, O_DATA);
endmodule



