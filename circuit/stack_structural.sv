module and3(output d, input a, input b, input c);
    wire s1;
    
    and(s1, a, b);
    and(d, s1, c);

endmodule

module nand3(output d, input a, input b, input c);
    wire s1;
    
    and3 w1(s1, a, b, c);
    not(d, s1);

endmodule

module d_trig(
    output y, input d,
    input clk);
    wire s1, s2, s4, notd,w,z,y1;
    
    assign w = y === 1'b1;
    assign z = y1 === 1'b1;

    not(notd, d);
    nand(s1, d, clk);
    nand(s2, notd, clk);
    nand(y, s1, z);
    nand(s4, w, s2);
    or(y1, 1'b0, s4);

endmodule

module add1mod5(output y1, output y2, input a0, input a1, input b);
    wire s1, s2, s3;
    
    xor(s1, a0, a1);
    and(s2, s1, b);
    and(s3, a0, a1);
    xor(y1, s1, b);
    or(y2, s2, s3);
    
endmodule

module mx2_1(output y, input x0, input x1, input a);
    wire s1, s2;
    
    not(b, a);
    and(s1, x0, b);
    and(s2, x1, a);
    or(y, s1, s2);
    
endmodule

module mx2_2(output y1, output y2, input x11, input x21, input x12, input x22, input a);
    
    mx2_1 w1(y1, x11, x12, a);
    mx2_1 w2(y2, x21, x22, a);
    
endmodule

module mx3_1(output y1, output y2, output y3, input x11, input x21, input x31, input x12, input x22, input x32, input a);
    
    mx2_1 w1(y1, x11, x12, a);
    mx2_1 w2(y2, x21, x22, a);
    mx2_1 w3(y3, x31, x32, a);
    
endmodule

module mx4_1(output y1, output y2, output y3, output y4, input x11, input x21, input x31, input x41, input x12, input x22, input x32, input x42, input a);
    
    mx2_1 w1(y1, x11, x12, a);
    mx2_1 w2(y2, x21, x22, a);
    mx2_1 w3(y3, x31, x32, a);
    mx2_1 w4(y4, x41, x42, a);
    
endmodule

module mx5_1(output y1, output y2, output y3, output y4, output y5, input x11, input x21, input x31, input x41, input x51, input x12, input x22, input x32, input x42, input x52, input a);
    
    mx2_1 w1(y1, x11, x12, a);
    mx2_1 w2(y2, x21, x22, a);
    mx2_1 w3(y3, x31, x32, a);
    mx2_1 w4(y4, x41, x42, a);
    mx2_1 w5(y5, x51, x52, a);
    
endmodule

module mx20_4(output y1, output y2, output y3, output y4, input x11, input x21, input x31, input x41, input x12, input x22, input x32, input x42, input x13, input x23, input x33, input x43, input x14, input x24, input x34, input x44, input x15, input x25, input x35, input x45, input a1, input a2, input a3, input a4, input a5);
    wire s11, s21, s31, s41, s12, s22, s32, s42, s13, s23, s33, s43, s14, s24, s34, s44;
    
    mx4_1 w1(s11, s21, s31, s41, 1'b0, 1'b0, 1'b0, 1'b0, x11, x21, x31, x41, a1);
    mx4_1 w2(s12, s22, s32, s42, s11, s21, s31, s41, x12, x22, x32, x42, a2);
    mx4_1 w3(s13, s23, s33, s43, s12, s22, s32, s42, x13, x23, x33, x43, a3);
    mx4_1 w4(s14, s24, s34, s44, s13, s23, s33, s43, x14, x24, x34, x44, a4);
    mx4_1 w5(y1, y2, y3, y4, s14, s24, s34, s44, x15, x25, x35, x45, a5);

endmodule

module mem1(output y, input x, input clk, input rst);
    wire s1, s2;
    
    mx2_1 w1(s2, x, 1'b0, rst);
    or(s1, clk, rst);
    d_trig w2(y, s2, s1);
    
endmodule

module mem3(output y1, output y2, output y3, input x1, input x2, input x3, input clk, input rst);
    
    mem1 w1(y1, x1, clk, rst);
    mem1 w2(y2, x2, clk, rst);
    mem1 w3(y3, x3, clk, rst);
    
endmodule

module mem4(output y1, output y2, output y3, output y4, input x1, input x2, input x3, input x4, input wr, input clk, input rst);
    wire c;
    
    and(c, wr, clk);
    mem1 w1(y1, x1, c, rst);
    mem1 w2(y2, x2, c, rst);
    mem1 w3(y3, x3, c, rst);
    mem1 w4(y4, x4, c, rst);

endmodule

module dec3_5(output y1, output y2, output y3, output y4, output y5,
    input x1, input x2, input x3);
    wire x11, x21, x31;
    
    not(x11, x1);
    not(x21, x2);
    not(x31, x3);
    and3 w1(y5, x31, x21, x11);
    and3 w2(y4, x31, x21, x1);
    and3 w3(y3, x31, x2, x11);
    and3 w4(y2, x31, x2, x1);
    and3 w5(y1, x3, x21, x11);
    
endmodule

module dec2_4(output y1, output y2, output y3, output y4, input x1, input x2);
    wire x11, x21;
    
    not(x11, x1);
    not(x21, x2);
    and(y1, x21, x11);
    and(y2, x21, x1);
    and(y3, x2, x11);
    and(y4, x2, x1);

endmodule

module c5_3(output y1, output y2, output y3, input x1, input x2, input x3, input x4, input x5);

    or(y1, x2, x4);
    or(y2, x3, x4);
    or(y3, x5, x5);

endmodule

module mod5min3(output y1, output y2, output y3, input x1, input x2, input x3);
    wire s1, s2, s3, s4, s5;
    
    dec3_5 w1(s1, s2, s3, s4, s5, x1, x2, x3);
    c5_3 w2(y1, y2, y3, s5, s1, s2, s3, s4);

endmodule

module mod5_4bit(output y1, output y2, output y3, input q0, input q1, input q2, input q3);
    wire x1, x2, x11, x21, s11, s21, s12, s22, s31, s32, s41, s42, s1, s2, s3, s;
    
    xor(x1, q0, q2);
    xor(x2, q1, q3);
    mx2_1 w1(x11, 1'b0, 1'b1, x1);
    mx2_1 w2(x21, 1'b0, 1'b1, x2);
    mx2_2 w3(s11, s21, 1'b0, 1'b0, q0, q2, x11);
    mx2_2 w4(s12, s22, 1'b0, 1'b0, q1, q3, x21);
    add1mod5 w5(s31, s32, s11, 1'b1, 1'b0);
    add1mod5 w6(s41, s42, s12, 1'b1, s32);
    mx3_1 w7(s1, s2, s3, s11, s12, s21, s31, s41, s42, s22);
    and(s, s2, s3);
    mx3_1 w8(y1, y2, y3, s1, s2, s3, 1'b1, 1'b0, 1'b0, s);
    
endmodule

module add3mod5(output y1, output y2, output y3, input a0, input a1, input a2, input b0, input b1, input b2);
    wire y10, y20, y11, y21, y12, y22;
    
    add1mod5 w1(y10, y20, a0, b0, 1'b0);
    add1mod5 w2(y11, y21, a1, b1, y20);
    add1mod5 w3(y12, y22, a2, b2, y21);
    mod5_4bit w4(y1, y2, y3, y10, y11, y12, y22);
endmodule

module gate(output y, input c, input a);
    wire cb;
    assign cb = ~c; 
    nmos n1(y,a,c);
    pmos p1(y,a,cb);
endmodule  

module stack(output y1, output y2, output y3, output y4, input ind0, input ind1, input ind2, input in0, input in1, input in2, input in3, input f0, input f1, input clk, input rst);
    wire ind0a, ind1a, ind2a, ind0b, ind1b, ind2b, ind0c, ind1c, ind2c, clk02, clk12, clk22, clk32, clk42, clk01, clk11, clk21, clk31, clk41, index00, index01, index02, clk0, clk1, clk2, clk3, clk4, f00, f01, f10, f11, el01, el11, el21, el31, el02, el12, el22, el32, el03, el13, el23, el33, el04, el14, el24, el34, el05, el15, el25, el35, z0, z1, z2, z3, z4, p0, p1, p2, r0, r1, r2, q00, q10, q20, q01, q11, q21, q02, q12, q22, index10, index11, index12, index20, index21, index22, notclk, con, y111, y211, y311, y411, y, ind0aa, ind1aa, ind2aa;

    // get
    add3mod5 w0(ind0aa, ind1aa, ind2aa, ind0, ind1, ind2, 1'b0, 1'b0, 1'b0);
    mod5min3 w1(ind0a, ind1a, ind2a, ind0aa, ind1aa, ind2aa);
    add3mod5 w2(ind0b, ind1b, ind2b, ind0a, ind1a, ind2a, index00, index01, index02);
    add3mod5 w3(ind0c, ind1c, ind2c, ind0b, ind1b, ind2b, 1'b0, 1'b0, 1'b1);
    dec3_5 w4(clk02, clk12, clk22, clk32, clk42, ind0c, ind1c, ind2c);
    dec3_5 w5(clk01, clk11, clk21, clk31, clk41, index00, index01, index02);
    mx5_1 w6(clk0, clk1, clk2, clk3, clk4, clk01, clk11, clk21, clk31, clk41, clk02, clk12, clk22, clk32, clk42, clk_f11);
    // input
    dec2_4 w7(f00, f01, f10, f11, f0, f1);
    and(clk_f10, clk, f10);
    and(clk_f11, clk, f11);
    and(clk_f01, clk, f01);
    // main_mem
    mem4 w8(el01, el11, el21, el31, in0, in1, in2, in3, clk_f01, clk0, rst);
    mem4 w9(el02, el12, el22, el32, in0, in1, in2, in3, clk_f01, clk1, rst);
    mem4 w10(el03, el13, el23, el33, in0, in1, in2, in3, clk_f01, clk2, rst);
    mem4 w11(el04, el14, el24, el34, in0, in1, in2, in3, clk_f01, clk3, rst);
    mem4 w12(el05, el15, el25, el35, in0, in1, in2, in3, clk_f01, clk4, rst);
    // output
    mx5_1 w13(z0, z1, z2, z3, z4, clk0, clk1, clk2, clk3, clk4, clk4, clk0, clk1, clk2, clk3, clk_f10);
    // let the stack always output something and not only when the commands are 10 or 11
    mx20_4 w14(y111, y211, y311, y411, el01, el11, el21, el31, el02, el12, el22, el32, el03, el13, el23, el33, el04, el14, el24, el34, el05, el15, el25, el35, z0, z1, z2, z3, z4);
    // indexes
    add3mod5 w15(p0, p1, p2, 1'b1, 1'b0, 1'b0, index00, index01, index02);
    add3mod5 w16(r0, r1, r2, 1'b0, 1'b0, 1'b1, index00, index01, index02);
    mx3_1 w17(q00, q10, q20, index00, index01, index02, r0, r1, r2, clk_f10);
    mx3_1 w18(q01, q11, q21, q00, q10, q20, 1'b0, 1'b0, 1'b0, rst);
    mx3_1 w19(q02, q12, q22, q01, q11, q21, p0, p1, p2, clk_f01);
    mem3 w20(index10, index11, index12, q02, q12, q22, clk, rst);
    mem3 w21(index20, index21, index22, index10, index11, index12, clk, rst);
    not(notclk, clk);
    mem3 w22(index00, index01, index02, index20, index21, index22, notclk, rst);
    or(con, clk_f10, clk_f11);
    gate w23(y, con, 1'b1);
    mx4_1 w24(y1, y2, y3, y4, 1'b0, 1'b0, 1'b0, 1'b0, y111, y211, y311, y411, y);

endmodule    

module stack_structural_easy(
    output wire[3:0] O_DATA, 
    input wire RESET, 
    input wire CLK, 
    input wire[1:0] COMMAND, 
    input wire[2:0] INDEX,
    input wire[3:0] I_DATA
    ); 
    
    stack w1(O_DATA[0], O_DATA[1], O_DATA[2], O_DATA[3], INDEX[0], INDEX[1], INDEX[2], I_DATA[0], I_DATA[1], I_DATA[2], I_DATA[3], COMMAND[0], COMMAND[1], CLK, RESET);

endmodule
