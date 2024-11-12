module stack_behaviour_easy(
    output wire [3:0] O_DATA,
    input wire RESET,
    input wire CLK,
    input wire[1:0] COMMAND,
    input wire[2:0] INDEX,
    input wire[3:0] I_DATA
);

    reg [3:0] stack [0:4];
    reg [2:0] index;
    reg [3:0] data = 4'b0000;

    assign O_DATA = data;

    always @(posedge CLK or posedge RESET) begin
        if (RESET) begin
            index = 3'b000;
            for (integer i = 0; i < 5; i = i + 1)
                stack[i] = 4'b0000;
            data = 4'b0000;
        end else begin 
            case (COMMAND)
                2'b01: begin // push
                    stack[index] = I_DATA;
                    index = (index == 4) ? 0 : (index + 1) % 5;
                    data = 4'b0000;
                end
                2'b10: begin // pop
                    index = (index == 0) ? 4 : (index - 1) % 5;
                    data = stack[index];
                end
                2'b11: begin // get
                    index = index;
                    if (index == 0)
                        data = stack[4 - INDEX % 5];
                    else 
                        data = stack[(index - 1 < INDEX % 5) ? (index - 1 + 5 - INDEX % 5) : (index - 1 - INDEX % 5)];
                end
            endcase
        end
    end
endmodule
