MODULE MainModule

  !------------------
  ! Left Arm Points
  !------------------
  CONST robtarget LRef := [[-12.48262, 188.8462, 195.1932], [0.06165144, 0.8419135, -0.1228757, 0.5218068], [0.0, 0.0, 0.0, 4.0], [101.7427,9E+09,9E+09,9E+09,9E+09,9E+09]];
  CONST robtarget placeap := [[429.4088, 43.17268, 392.192], [0.001483749, -0.6896544, 0.7241371, 0.0002948535],[0.0, 1.0, 2.0, 4.0], [-148.5723, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  CONST robtarget pickap := [[375.9644, 270.074, 371.3876], [0.02350171, -0.9992896, 0.02860069, -0.007074669], [0.0, 1.0, 2.0, 4.0], [-141.3491, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];

  CONST robtarget pickpoint := [[235.858, 319.6979, 158.0], [0.006762601, -0.9999652, 0.003439943, -0.003464191], [-1.0, 0.0, 0.0, 5.0], [152.1098, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  CONST robtarget placepoint := [[447.4478, 5.313061, 158.0], [0.01330368, 0.9998788, 0.002927237, -0.007532438], [-1.0, 1.0, 1.0, 4.0], [166.0087, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  
  !===============
  ! Procedure main
  !===============
  PROC main()

  ! calibrateGripper;
  ! g_GripOut;
  ! MoveJ pickap, v100, z10, tool0;

  ! MoveJ pickpoint, v100, z10, tool0;
  
  pick pickpoint;
  place placepoint;

  ENDPROC

  PROC unlock(robtarget lastpoint)
    g_GripOut;
    MoveJ lastpoint, v100, fine, tool0;
    WaitRob \ZeroSpeed;
  ENDPROC

  PROC calibrateGripper()
    g_Init \maxSpd := 25, \holdForce := 20;
    g_Calibrate \Grip;
    g_GripOut;
  ENDPROC

  PROC pick(robtarget actualpoint)
    MoveJ Offs(actualpoint, 0, 0, 40), v100, z10, tool0;
    MoveL actualpoint, v100, fine, tool0;
    WaitRob \ZeroSpeed;
    g_GripIn;
    MoveL Offs(actualpoint, 0, 0, 40), v100, z10, tool0;
    MoveJ pickap, v100, z10, tool0;
  ENDPROC

  PROC place(robtarget targetpoint)
    MoveJ placeap, v100, z10, tool0;
    MoveJ Offs(targetpoint, 0, 0, 40), v100, z10, tool0;
    MoveL targetpoint, v100, fine,tool0;
    g_GripOut;
    MoveL Offs(targetpoint, 0, 0, 45), v100, z10,tool0;
    g_GripIn;
    MoveL Offs(targetpoint, 0, 0, 15.8), v100, fine,tool0;
    MoveL Offs(targetpoint, 0, 0, 40), v100, z10, tool0;
    MoveJ placeap, v100, z10, tool0;
    g_GripOut;
    MoveJ pickap, v100, z10, tool0;
  ENDPROC

ENDMODULE