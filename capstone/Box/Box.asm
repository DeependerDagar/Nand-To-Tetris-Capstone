// K = 92
// Box starts at row 92
// Width = 16 pixels (1 word), because 92 mod 4 = 0
// Height = 20 rows
// Start address = 16384 + 32*92 = 19328
// Deepender

(LOOP)
    // Check keyboard
    @KBD
    D=M
    @BLACK
    D;JNE

    // No key pressed: white
    @R15
    M=0
    @DRAW
    0;JMP

(BLACK)
    // Key pressed: black (all 16 bits = 1)
    @R15
    M=-1

(DRAW)
    // R13 = current screen address
    @19328
    D=A
    @R13
    M=D

    // R14 = rows left
    @20
    D=A
    @R14
    M=D

(ROW)
    // Draw the one word of this row
    @R15
    D=M
    @R13
    A=M
    M=D

    // Move to the next screen row (32 words down)
    @32
    D=A
    @R13
    M=D+M

    // Decrease row counter
    @R14
    MD=M-1
    @ROW
    D;JGT

    // Repeat continuously
    @LOOP
    0;JMP