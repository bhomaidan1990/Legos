(define (problem p02)
    (:domain Legos)

(:objects
        ; Two Grippers
        g_left - Gripper ; g_right
        ; Reference Points
        p_air_left - Point_Air; p_air_right
        ; Workspace Points, and Neighbouring fake points.
        ;  ===== g_right              Right
        ; ||
        ; YuMi  p_yy_xx        up    p_yy_xx     down
        ; ||
        ;  ===== g_left               Left
                        p_06_05 p_06_06 p_06_07
                p_07_04 p_07_05 p_07_06 p_07_07 p_07_08
                        p_08_05 p_08_06 p_08_07
                p_09_04 p_09_05 p_09_06 p_09_07 
        p_10_03 p_10_04 p_10_05 p_10_06 p_10_07 p_10_08 
        p_11_03 p_11_04 p_11_05 p_11_06 p_11_07 p_11_08 
        p_12_03 p_12_04 p_12_05 p_12_06 p_12_07 p_12_08 
        p_13_03 p_13_04 p_13_05 p_13_06 p_13_07 p_13_08 
                p_14_04 p_14_05 p_14_06 p_14_07         - Point_Workspace
        ; we have to increase the number of the blocks according to the needs
        ; b_2x2_id
        ; y_2x2_id
        ; b_2x4_id
        ; y_2x4_id
        ; b_2x6_id
        ; y_2x6_id
        ; -----
        ; | y |
        ; -----
        y_2x2_11
        y_2x2_12
        y_2x2_13
        y_2x2_14
        ; y_2x2_15
        ; y_2x2_16
        ; -----
        ; | B |
        ; -----
        b_2x2_41
        b_2x2_42
        b_2x2_43
        b_2x2_44 - Block_2x2
        ; b_2x2_45
        ; b_2x2_46
        ; b_2x2_61
        ; b_2x2_62
        ; b_2x2_63
        ; b_2x2_64
        ; b_2x2_65
        ; b_2x2_66 
        ; ---------
        ; | y | y |
        ; ---------
        y_2x4_21
        y_2x4_22
        y_2x4_31
        y_2x4_32
        ; ---------
        ; | B | B |
        ; ---------
        b_2x4_51
        b_2x4_52
        b_2x4_53 
        b_2x4_41 - Block_2x4
        ; -------------
        ; | y | y | y |
        ; -------------
        ; y_2x6_31
        ; y_2x6_32 - Block_2x6

        x_minus x_plus center y_minus y_plus no_dir - Direction
        ;-------------------------------------------------------------------------------------------------------
        ; 78/66 objects in Total: 2/1 grippers, 2/1 Point_Air, 42 Point_Workspace, 26/16 Blocks, 6 directions  |
        ;-------------------------------------------------------------------------------------------------------
    )

    (:htn
        :ordered-subtasks
        (and
            ;============
            ; ID_25 Y_5 |
            ;============
            (t1 (pick g_left y_2x2_11 no_dir))
            ; first option of place
            (t2 (place g_left y_2x2_11 p_13_04))
            ; second option of place
            ; (t2 (Rotate_2x2_loaded_gripper_V2H g_left y_2x2_11))
            ; (t3 (place g_left y_2x2_11 p_13_04))           
            ;============
            ; ID_25 B_5 |
            ;============
            ; first option
            (t4 (pick g_left b_2x4_51 y_minus))
            (t5 (place g_left b_2x4_51 p_12_05))
            ; second option
            ; (t4 (pick g_left b_2x4_51 y_plus))
            ; (t5 (place g_left b_2x4_51 p_13_05))
            ;============
            ; ID_25 B_4 |
            ;============
            ; first option
            (t6 (pick g_left b_2x4_52 y_minus))
            (t7 (place g_left b_2x4_52 p_11_04))
            ; second option
            ; (t6 (pick g_left b_2x4_52 y_plus))
            ; (t7 (place g_left b_2x4_52 p_12_04))
            ;============
            ; ID_25 Y_2 |
            ;============
            (t8 (pick g_left y_2x4_21 y_minus))
            ; first option
            (t9 (Rotate_2x4_right_loaded_gripper_V2H_Anticlk g_left y_2x4_21))
            (t10 (place g_left y_2x4_21 p_11_06))
            ; second option
            ; (t9 (Rotate_2x4_right_loaded_gripper_V2H_clk g_left y_2x4_21))
            ; (t10 (place g_left y_2x4_21 p_11_05))
            ;============
            ; ID_25 B_3 |
            ;============
            ; first option
            (t11 (pick g_left b_2x4_53 y_plus))
            (t12 (place g_left b_2x4_53 p_12_07))
            ; second option
            ; (t11 (pick g_left b_2x4_53 y_minus))
            ; (t12 (place g_left b_2x4_53 p_11_07))
            ;============
            ; ID_25 B_2 |
            ;============
            ; first option
            (t13 (pick g_left b_2x2_41 no_dir))
            (t14 (place g_left b_2x2_41 p_10_07))
            ; second option
            ; (t14 (Rotate_2x2_loaded_gripper_V2H g_left b_2x2_41))
            ; (t15 (place g_left b_2x2_41 p_10_07))
            ;============
            ; ID_25 Y_4 |
            ;============
            (t16 (pick g_left y_2x4_22 y_minus))
            ; first option of place
            (t17 (Rotate_2x4_right_loaded_gripper_V2H_clk g_left y_2x4_22))
            (t18 (place g_left y_2x4_22 p_13_06))
            ; second option of place
            ; (t17 (Rotate_2x4_right_loaded_gripper_V2H_Anticlk g_left y_2x4_22))
            ; (t18 (place g_left y_2x4_22 p_13_07))
            ;============
            ; ID_25 Y_1 |
            ;============
            ; first option
            (t19 (pick g_left y_2x2_12 no_dir))
            (t20 (place g_left y_2x2_12 p_10_04))
            ; second option
            ; (t20 (Rotate_2x2_loaded_gripper_V2H g_left y_2x2_12))
            ; (t21 (place g_left y_2x2_12 p_10_04))
            
            ;xxxxxxxxxxxxxxxxxxxxxxxxx
            ; Here we can't do more! x
            ;xxxxxxxxxxxxxxxxxxxxxxxxx

            ;============
            ; ID_25 B_1 |
            ;============
            ; (t22 (pick g_left b_2x4_54 y_minus))
            ; ; first option
            ; (t23 (Rotate_2x4_right_loaded_gripper_V2H_clk g_left b_2x4_54))
            ; (t24 (place g_left b_2x4_54 p_10_05))
            ; ; second option
            ; ; (t23 (Rotate_2x4_right_loaded_gripper_V2H_Anticlk g_left b_2x4_54))
            ; ; (t24 (place g_left b_2x4_54 p_10_06))
            ;============
            ; ID_25 Y_3 |
            ;============
            ; (t25 (pick g_left b_2x2_42 no_dir))
            ; first option of place
            ; (t26 (Rotate_2x2_loaded_gripper_V2H g_left b_2x2_42))
            ; (t27 (place g_left b_2x2_42 p_12_06))
            ; second option of place
            ; (t26 (place g_left b_2x2_42 p_12_06))

        )
    )

    (:init
        ;--------------------
        ; Gripper Relations |
        ;--------------------
        ; gripper at initial position.
        ( at g_left p_air_left )

        ; unloaded gripper
        ( unloaded g_left )
        
        ;-------------
        ; Directions |
        ;-------------
        (left_direction y_plus)
        (right_direction y_minus)
        (middle_direction center)
        (top_direction x_minus)
        (bottom_direction x_plus)

        ;------------------
        ; Empty Locations |
        ;------------------
        ; swap
        ( empty_location p_06_05)
        ( empty_location p_06_06)
        ( empty_location p_06_07)
        ( empty_location p_07_04)
        ( empty_location p_07_05)
        ( empty_location p_07_06)
        ( empty_location p_07_07)
        ( empty_location p_07_08)
        ( empty_location p_08_05)
        ( empty_location p_08_06)
        ( empty_location p_08_07)
        ; Workspace
        ( empty_location p_09_04)
        ( empty_location p_09_05)
        ( empty_location p_09_06)
        ( empty_location p_09_07)
        ( empty_location p_10_03)
        ( empty_location p_10_04)
        ( empty_location p_10_05)
        ( empty_location p_10_06)
        ( empty_location p_10_07)
        ( empty_location p_10_08)
        ( empty_location p_11_03)
        ( empty_location p_11_04)
        ( empty_location p_11_05)
        ( empty_location p_11_06)
        ( empty_location p_11_07)
        ( empty_location p_11_08)
        ( empty_location p_12_03)
        ( empty_location p_12_04)
        ( empty_location p_12_05)
        ( empty_location p_12_06)
        ( empty_location p_12_07)
        ( empty_location p_12_08)
        ( empty_location p_13_03)
        ( empty_location p_13_04)
        ( empty_location p_13_05)
        ( empty_location p_13_06)
        ( empty_location p_13_07)
        ( empty_location p_13_08)
        ( empty_location p_14_04)
        ( empty_location p_14_05)
        ( empty_location p_14_06)
        ( empty_location p_14_07)

        ;-------------
        ; Directions |
        ;-------------
        ; up
        ( up p_06_05 p_06_06)
        ( up p_06_06 p_06_07)
        ( up p_07_04 p_07_05)
        ( up p_07_05 p_07_06)
        ( up p_07_06 p_07_07)
        ( up p_07_07 p_07_08)
        ( up p_08_05 p_08_06)
        ( up p_08_06 p_08_07)
        ( up p_09_04 p_09_05)
        ( up p_09_05 p_09_06)
        ( up p_09_06 p_09_07)
        ( up p_10_03 p_10_04)
        ( up p_10_04 p_10_05)
        ( up p_10_05 p_10_06)
        ( up p_10_06 p_10_07)
        ( up p_10_07 p_10_08)
        ( up p_11_03 p_11_04)
        ( up p_11_04 p_11_05)
        ( up p_11_05 p_11_06)
        ( up p_11_06 p_11_07)
        ( up p_11_07 p_11_08)
        ( up p_12_03 p_12_04)
        ( up p_12_04 p_12_05)
        ( up p_12_05 p_12_06)
        ( up p_12_06 p_12_07)
        ( up p_12_07 p_12_08)
        ( up p_13_03 p_13_04)
        ( up p_13_04 p_13_05)
        ( up p_13_05 p_13_06)
        ( up p_13_06 p_13_07)
        ( up p_13_07 p_13_08)
        ( up p_14_04 p_14_05)
        ( up p_14_05 p_14_06)
        ( up p_14_06 p_14_07)
        ( up p_14_05 p_14_06)
        ( up p_14_06 p_14_07)
        
        ; down
        ( down p_06_06 p_06_05 )
        ( down p_06_07 p_06_06 )
        ( down p_07_05 p_07_04 )
        ( down p_07_06 p_07_05 )
        ( down p_07_07 p_07_06 )
        ( down p_07_08 p_07_07 )
        ( down p_08_06 p_08_05 )
        ( down p_08_07 p_08_06 )
        ( down p_09_05 p_09_04 )
        ( down p_09_06 p_09_05 )
        ( down p_09_07 p_09_06 )
        ( down p_10_04 p_10_03 )
        ( down p_10_05 p_10_04 )
        ( down p_10_06 p_10_05 )
        ( down p_10_07 p_10_06 )
        ( down p_10_08 p_10_07 )
        ( down p_11_04 p_11_03 )
        ( down p_11_05 p_11_04 )
        ( down p_11_06 p_11_05 )
        ( down p_11_07 p_11_06 )
        ( down p_11_08 p_11_07 )
        ( down p_12_04 p_12_03 )
        ( down p_12_05 p_12_04 )
        ( down p_12_06 p_12_05 )
        ( down p_12_07 p_12_06 )
        ( down p_12_08 p_12_07 )
        ( down p_13_04 p_13_03 )
        ( down p_13_05 p_13_04 )
        ( down p_13_06 p_13_05 )
        ( down p_13_07 p_13_06 )
        ( down p_13_08 p_13_07 )
        ( down p_14_05 p_14_04 )
        ( down p_14_06 p_14_05 )
        ( down p_14_07 p_14_06 )
        ( down p_14_06 p_14_05 )
        ( down p_14_07 p_14_06 )
        ; left
        ( left p_11_03 p_10_03 )
        ( left p_12_03 p_11_03 )
        ( left p_13_03 p_12_03 )
        ( left p_10_04 p_09_04 )
        ( left p_11_04 p_10_04 )
        ( left p_12_04 p_11_04 )
        ( left p_13_04 p_12_04 )
        ( left p_14_04 p_13_04 )
        ( left p_07_05 p_06_05 )
        ( left p_08_05 p_07_05 )
        ( left p_09_05 p_08_05 )
        ( left p_10_05 p_09_05 )
        ( left p_11_05 p_10_05 )
        ( left p_12_05 p_11_05 )
        ( left p_13_05 p_12_05 )
        ( left p_14_05 p_13_05 )
        ( left p_07_06 p_06_06 )
        ( left p_08_06 p_07_06 )
        ( left p_09_06 p_08_06 )
        ( left p_10_06 p_09_06 )
        ( left p_11_06 p_10_06 )
        ( left p_12_06 p_11_06 )
        ( left p_13_06 p_12_06 )
        ( left p_14_06 p_13_06 )
        ( left p_07_07 p_06_07 )
        ( left p_08_07 p_07_07 )
        ( left p_09_07 p_08_07 )
        ( left p_10_07 p_09_07 )
        ( left p_11_07 p_10_07 )
        ( left p_12_07 p_11_07 )
        ( left p_13_07 p_12_07 )
        ( left p_14_07 p_13_07 )
        ( left p_11_08 p_10_08 )
        ( left p_12_08 p_11_08 )
        ( left p_13_08 p_12_08 )
        ; right
        ( right p_10_03 p_11_03 )
        ( right p_11_03 p_12_03 )
        ( right p_12_03 p_13_03 )
        ( right p_09_04 p_10_04 )
        ( right p_10_04 p_11_04 )
        ( right p_11_04 p_12_04 )
        ( right p_12_04 p_13_04 )
        ( right p_13_04 p_14_04 )
        ( right p_06_05 p_07_05 )
        ( right p_07_05 p_08_05 )
        ( right p_08_05 p_09_05 )
        ( right p_09_05 p_10_05 )
        ( right p_10_05 p_11_05 )
        ( right p_11_05 p_12_05 )
        ( right p_12_05 p_13_05 )
        ( right p_13_05 p_14_05 )
        ( right p_06_06 p_07_06 )
        ( right p_07_06 p_08_06 )
        ( right p_08_06 p_09_06 )
        ( right p_09_06 p_10_06 )
        ( right p_10_06 p_11_06 )
        ( right p_11_06 p_12_06 )
        ( right p_12_06 p_13_06 )
        ( right p_13_06 p_14_06 )
        ( right p_06_07 p_07_07 )
        ( right p_07_07 p_08_07 )
        ( right p_08_07 p_09_07 )
        ( right p_09_07 p_10_07 )
        ( right p_10_07 p_11_07 )
        ( right p_11_07 p_12_07 )
        ( right p_12_07 p_13_07 )
        ( right p_13_07 p_14_07 )
        ( right p_10_08 p_11_08 )
        ( right p_11_08 p_12_08 )
        ( right p_12_08 p_13_08 )

    )

)