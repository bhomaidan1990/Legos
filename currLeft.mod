MODULE MainModule

  !------------------
  ! Left Arm Points
  !------------------
  CONST robtarget LRef := [[-12.48262, 188.8462, 195.1932], [0.06165144, 0.8419135, -0.1228757, 0.5218068], [0.0, 0.0, 0.0, 4.0], [101.7427,9E+09,9E+09,9E+09,9E+09,9E+09]];
  CONST robtarget placeap := [[429.4088, 43.17268, 392.192], [0.001483749, -0.6896544, 0.7241371, 0.0002948535],[0.0, 1.0, 2.0, 4.0], [-148.5723, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  CONST robtarget pickap := [[375.9644, 270.074, 371.3876], [0.02350171, -0.9992896, 0.02860069, -0.007074669], [0.0, 1.0, 2.0, 4.0], [-141.3491, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];

  CONST robtarget pickpoint := [[490.3113, 354.8676, 159.4501], [0.008441729, 0.9999098, -0.002559415, 0.0101336], [-1.0, -1.0, 0.0, 5.0], [-144.1124, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  CONST robtarget placepoint := [[412.0412, 33.07267, 158.0], [0.0001519844, -0.9999423, 0.009992004, -0.003945677], [-1.0, 2.0, 1.0, 4.0], [168.7616, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]];
  
  TASK PERS loaddata load1:=[0.4,[0,0,5],[1,0,0,0],0,0,0];
  !===============
  ! Procedure main
  !===============
  PROC main()

  ! calibrateGripper;
  g_GripOut;
  MoveJ pickap, v100, z10, tool0;

  ! MoveJ placepoint, v100, z10, tool0;
  
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
    GripLoad load1;
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
    MoveL Offs(targetpoint, 0, 0, 16), v100, fine,tool0;
    MoveL Offs(targetpoint, 0, 0, 40), v100, z10, tool0;
    MoveJ placeap, v100, z10, tool0;
    g_GripOut;
    MoveJ pickap, v100, z10, tool0;
  ENDPROC

ENDMODULE