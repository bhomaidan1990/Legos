;-------------------------------------------------
;; Specification in HDDL of the Legos domain
;-------------------------------------------------
(define (domain Legos)
;-------------------------------------------------------------------------
;                       Description                                      |
;------------------------------------------------------------------------|
; This File contains:                                                    |
; # 1. Predicates, that describes properties of the world.               |
; # 2. Operators(Actions), that describes the way in which the state     |
;      can change, These operators are limited to the agent capabilities.|
; # 3. Tasks(fully or partially ordered).                                |
; # 4. Methods to decompose the non-premitive tasks into subtasks        |
;-------------------------------------------------------------------------
;-------------------
;;   Requirements
;-------------------
(:requirements 
  :strips ; add delete effects
  :typing ; add types
  :hierarchy ; add tasks - subtasks ... etc.
  :method-preconditions ; add preconditions to the methods.
  :negative-preconditions ; add negative preconditions.
  :equality ; to use = symbol to compare objects (= ?s1 ?s2).
)
;----------------
;   Types
;----------------
(:types
  Location - object 
  Block - object ; Block 2x2.
  Gripper - agent ; holds at most 1 Lego, only 1 Gripper per Location.
)
;-------------------------------------------------------------------------
;                          Predicates                                    |
;-------------------------------------------------------------------------
(:predicates 
  ;; define block static characteristics.
  (color_blue ?x - Block); Lego x color is blue.
  (color_yellow ?x - Block); Lego x color is yellow. 
  ;; define the position of the Lego.
  (single ?x - Block) ; lego x is 2x2
  (connected ?x - Block ?y - Block); Lego x has Lego y connected to it 2x4.
  (double_connected ?x - Block ?y - Block ?z - Block) ; lego x has lego y, and lego z connected to it 2x6.
  ;; Directions
  (left ?l1 - Location ?l2 - Location); Location l1 is to the left of l2.
  (right ?l1 - Location ?l2 - Location); Location l1 is to the right of l2.
  (up ?l1 - Location ?l2 - Location); Location l1 is to the upper side of l2.
  (down ?l1 - Location ?l2 - Location); Location l1 is to the lower side of l2.
  ;; define the Location characteristics.
  (belong ?x - Block ?l - Location); Lego x is located on Location l.
  (has_left ?x - Block ?y - Block); Lego x is to the left side of Lego y (from robot point of view y++).
  (has_right ?x - Block ?y - Block); Lego x has Lego y on the right side(from robot point of view y--).
  (has_upper ?x - Block ?y - Block); Lego x has Lego y on the upper side(from robot point of view x++).
  (has_lower ?x - Block ?y - Block); Lego x has Lego y on the lower side(from robot point of view x--).
  (empty_location ?l - Location); Location l is empty no Lego block.
  ;; define the orientation of the Gripper
  (vertical ?g - Gripper)   ; Gripper g mode is vertical(movement is in x direction).
  ;; define the state of the Grippers
  (is_open ?g - Gripper); Gripper g is open.
  (unloaded ?g - Gripper); Gripper g is uloaded.
  (loaded ?x - Block ?g - Gripper); Gripper g is loaded with Lego block.
  (at ?g - Gripper ?l - Location); Gripper g is in Location l.
)
;-------------------------------------------------------------------------
;                               Tasks                                    |
;-------------------------------------------------------------------------
; The task of picking a Lego.
(:task pick
  :parameters (?g - Gripper ?x - Block ?pos - Location)
)
; ; The task of placing a Lego.
; (:task place
;   :parameters (?g - Gripper ?x - Block ?pos - Location)
; )
; ; The task of shifting stock from Robot stock to Operator stock.
; (:task shift
;   :parameters (?g_left - Gripper ?g_right - Gripper ?x - Block ?pos - Location)
; )
;-------------------------------------------------------------------------
;                               Methods                                  |
;-------------------------------------------------------------------------
;====================
; Task Pick Methods |
;====================
; Method to pick-up 2x2 blue block
(:method pick_2x2_Blue
  :parameters (?g - Gripper ?x ?y - Block ?point_air ?pos ?pos_upper ?pos_lower - Location)
  :task (pick ?g ?x ?pos)
  :precondition 
  (and
    (at ?g ?point_air)
    (not (at ?g ?pos))
    (unloaded ?g)
    (is_open ?g)
    (single ?x)
    (color_blue ?x)
    (belong ?x ?pos)
    (not (empty_location ?pos))
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (down ?pos ?pos_upper)
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g)
    (Rotate_empty_gripper_V ?g)
    (Move_open_gripper_V ?g ?point_air ?pos ?pos_upper ?pos_lower)
    (Hold_gripper ?x ?g ?pos)
    (take_2x2_gripper ?x ?g ?pos ?point_air)
    (fill_stock_2x2_blue ?y ?pos)
  )
)
; Method to pick-up 2x2 yellow block
(:method pick_2x2_Yellow
  :parameters (?g - Gripper ?x ?y - Block ?point_air ?pos ?pos_upper ?pos_lower - Location)
  :task (pick ?g ?x ?pos)
  :precondition 
  (and
    (at ?g ?point_air)
    (not (at ?g ?pos))
    (unloaded ?g)
    (is_open ?g)
    (single ?x)
    (color_yellow ?x)
    (belong ?x ?pos)
    (not (empty_location ?pos))
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (down ?pos ?pos_upper)
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g); gripper is open
    (Rotate_empty_gripper_V ?g); gripper is vertical
    (Move_open_gripper_V ?g ?point_air ?pos ?pos_upper ?pos_lower); gripper at pos / not point_air
    (Hold_gripper ?x ?g ?pos); not open gripper, loaded, not unloaded
    (take_2x2_gripper ?x ?g ?pos ?point_air); g at point_air, x not belong pos, empty pos
    (fill_stock_2x2_yellow ?x ?pos)
  )
)
;=====================
; Task Place Methods |
;=====================

;=====================
; Task Shift Methods |
;=====================

;-------------------------------------------------------------------------
;                        Operators(Actions)                              |
;-------------------------------------------------------------------------
;============================================
; 1. Empty Gripper Fingers Group of Actions |
;============================================
; 1.1 action of openning the empty Gripper
(:action Open_gripper
  :parameters (?g - Gripper)
  :precondition 
  (and 
    (unloaded ?g)
  )
  :effect
  (and 
    (is_open ?g)
  )
)
; 1.2 action of closing the empty Gripper
(:action Close_gripper
  :parameters (?g - Gripper)
  :precondition 
  (and 
    (unloaded ?g)
  )
  :effect
  (and 
    (not (is_open ?g))
  )
)
; 1.3 action of holding block with the Gripper
(:action Hold_gripper
  :parameters (?x - Block ?g - Gripper ?l - Location)
  :precondition 
  (and 
    (is_open ?g)
    (not (empty_location ?l))
    (unloaded ?g)
  )
  :effect
  (and 
    (not (is_open ?g))
    (loaded ?x ?g)
    (not(unloaded ?g))
  )
)
; 1.4 action of releasing the loaded Gripper
(:action Release_gripper
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (not (is_open ?g))
    (loaded ?x ?g)
  )
  :effect
  (and 
    (is_open ?g)
    (unloaded ?g)
    (not (loaded ?x ?g))
  )
)
;=========================================
; 2. Empty Gripper Move Group of Actions |
;=========================================

; 2.1 action of moving empty closed Gripper.
(:action Move_closed_gripper
  :parameters (?g - Gripper ?current_point ?destination_point - Location)
  :precondition 
  (and
    (not (is_open ?g))
    (unloaded ?g)
    (at ?g ?current_point)
    (empty_location ?destination_point)
    (not (= ?current_point ?destination_point))
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
; 2.2 action of moving empty open Vertical Gripper.
(:action Move_open_gripper_V
  :parameters (?g - Gripper ?current_point  ?destination_point ?dest_upper ?dest_lower - Location)
  :precondition 
  (and
    (is_open ?g)
    (unloaded ?g)
    (vertical ?g)
    (at ?g ?current_point)
    (up ?destination_point ?dest_upper)
    (down ?destination_point ?dest_lower)
    (empty_location ?dest_upper)
    (empty_location ?dest_lower)
    (not (= ?current_point ?destination_point))
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
; 2.3 action of moving empty open Horizontal Gripper.
(:action Move_open_gripper_H
  :parameters (?g - Gripper ?current_point  ?destination_point ?dest_left ?dest_right - Location)
  :precondition 
  (and
    (is_open ?g)
    (unloaded ?g)
    (not (vertical ?g))
    (at ?g ?current_point)
    (left ?destination_point ?dest_left)
    (right ?destination_point ?dest_right)
    (empty_location ?dest_left)
    (empty_location ?dest_right)
    (not (= ?current_point ?destination_point))
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
;=======================================
; 3. Gripper Rotation Group of Actions |
;=======================================
;--------------------------------------------------
; Note: All the Rotations are meant to be on Air, |
;    No colloision detection or neighbouring      |
;        position assertion is done here!         |
;--------------------------------------------------
; 3.1 action of rotating the empty Gripper H
; ( ? ) --> ( => <= )
(:action Rotate_empty_gripper_H
  :parameters (?g - Gripper)
  :precondition 
  (and 
    (unloaded ?g)
  )
  :effect
  (and 
    (not (vertical ?g))
  )
)
; 3.2 action of rotating the empty Gripper V
; ( ? ) --> ( || )
(:action Rotate_empty_gripper_V
  :parameters (?g - Gripper)
  :precondition 
  (and 
    (unloaded ?g)
  )
  :effect
  (and 
    (vertical ?g)
  )
)
; 3.3 action of rotating the 2x2_loaded Gripper V2H
;  ||
; -----          -----
; | x |  --->  =>| x |<=
; -----          -----
;  ||
(:action Rotate_2x2_loaded_gripper_V2H
  :parameters (?g - Gripper ?x - Block)
  :precondition 
  (and
    (loaded ?x ?g)
    (not (is_open ?g))
    (vertical ?g)
    (single ?x)
  )
  :effect
  (and 
    (not (vertical ?g))
  )
)
; 3.4 action of rotating the 2x2_loaded Gripper H2V
;                  ||
;   -----         -----
; =>| x |<=  ---> | x |
;   -----         -----
;                  ||
(:action Rotate_2x2_loaded_gripper_H2V
  :parameters (?g - Gripper ?x - Block)
  :precondition 
  (and
    (loaded ?x ?g)
    (not (is_open ?g))
    (not(vertical ?g))
    (single ?x)
  )
  :effect
  (and 
    (vertical ?g)
  )
)
; 3.5 action of rotating the left holded 2x4_loaded Gripper V2H clockwise
;  ||               -----
; ---------       =>| x |<=
; | x | y |  --->   -----
; ---------         | y |
;  ||               -----
(:action Rotate_2x4_left_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_right ?x ?y)
      (has_left ?y ?x)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?y))
      (not (has_left ?y ?x))
      (has_lower ?x ?y)
      (has_upper ?y ?x)
    )
)
; 3.6 action of rotating the left holded 2x4_loaded Gripper V2H Anti-clockwise
;  ||               -----
; ---------         | y |
; | x | y |  --->   -----
; ---------       =>| x |<=
;  ||               -----
(:action Rotate_2x4_left_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_right ?x ?y)
      (has_left ?y ?x)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?y))
      (not (has_left ?y ?x))
      (has_lower ?y ?x)
      (has_upper ?x ?y)
    )
)
; 3.7 action of rotating the right holded 2x4_loaded Gripper V2H clockwise
;       ||          -----
; ---------         | y |
; | y | x |  --->   -----
; ---------       =>| x |<=
;       ||          -----
(:action Rotate_2x4_right_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_left ?x ?y)
      (has_right ?y ?x)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_left ?x ?y))
      (not (has_right ?y ?x))
      (has_lower ?y ?x)
      (has_upper ?x ?y)
    )
)
; 3.8 action of rotating the right holded 2x4_loaded Gripper V2H Anti-clockwise
;       ||          -----
; ---------       =>| x |<=
; | y | x |  --->   -----
; ---------         | y |
;       ||          -----
(:action Rotate_2x4_right_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_left ?x ?y)
      (has_right ?y ?x)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?y))
      (not (has_left ?y ?x))
      (has_lower ?x ?y)
      (has_upper ?y ?x)
    )
)
; 3.9 action of rotating the upper holded 4x2_loaded Gripper H2V clockwise
;   -----              ||
; =>| x |<=      ---------
;   -----   ---> | y | x | 
;   | y |        ---------
;   -----              ||
(:action Rotate_4x2_upper_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not(vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_lower ?x ?y)
      (has_upper ?y ?x)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_lower ?x ?y))
      (not (has_upper ?y ?x))
      (has_left ?x ?y)
      (has_right ?y ?x)
    )
)
; 3.10 action of rotating the upper holded 4x2_loaded Gripper H2V Anti-clockwise
;   -----         ||
; =>| x |<=      ---------
;   -----   ---> | x | y | 
;   | y |        ---------
;   -----         ||
(:action Rotate_4x2_upper_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not(vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_lower ?x ?y)
      (has_upper ?y ?x)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_lower ?x ?y))
      (not (has_upper ?y ?x))
      (has_right ?x ?y)
      (has_left ?y ?x)
    )
)
; 3.11 action of rotating the lower holded 4x2_loaded Gripper H2V clockwise
;   -----         ||
;   | y |        ---------
;   -----   ---> | x | y | 
; =>| x |<=      ---------
;   -----         ||
(:action Rotate_4x2_lower_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not(vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_lower ?y ?x)
      (has_upper ?x ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_lower ?y ?x))
      (not (has_upper ?x ?y))
      (has_left ?y ?x)
      (has_right ?x ?y)
    )
)
; 3.12 action of rotating the lower holded 4x2_loaded Gripper H2V Anti-clockwise
;   -----              ||
;   | y |        ---------
;   -----   ---> | y | x | 
; =>| x |<=      ---------
;   -----              ||
(:action Rotate_4x2_lower_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x ?y - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not(vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (connected ?x ?y)
      (connected ?y ?x)
      (has_lower ?y ?x)
      (has_upper ?x ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_lower ?y ?x))
      (not (has_upper ?x ?y))
      (has_right ?y ?x)
      (has_left ?x ?y)
    )
)
; 3.13 action of rotating the left holded 2x6_loaded Gripper V2H clockwise
;                       -----
;  ||                 =>| x |<=
; -------------         -----
; | x | y | z | --->    | y |
; -------------         -----
;  ||                   | z |
;                       -----
(:action Rotate_2x6_left_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?x ?y)
      (has_right ?y ?z)
      (has_left ?y ?x)
      (has_left ?z ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?y))
      (not (has_right ?y ?z))
      (not (has_left ?y ?x))
      (not (has_left ?z ?y))
      (has_lower ?x ?y)
      (has_lower ?y ?z)
      (has_upper ?y ?x)
      (has_upper ?z ?y)
    )
)
; 3.14 action of rotating the left holded 2x6_loaded Gripper V2H Anticlockwise
;                       -----
;  ||                   | z |
; -------------         -----
; | x | y | z | --->    | y |
; -------------         -----
;  ||                 =>| x |<=
;                       -----
(:action Rotate_2x6_left_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?x ?y)
      (has_right ?y ?z)
      (has_left ?y ?x)
      (has_left ?z ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?y))
      (not (has_right ?y ?z))
      (not (has_left ?y ?x))
      (not (has_left ?z ?y))
      (has_lower ?z ?y)
      (has_lower ?y ?x)
      (has_upper ?y ?z)
      (has_upper ?x ?y)
    )
)
; 3.15 action of rotating the middle holded 2x6_loaded Gripper V2H clockwise
;                       -----
;      ||               | y |
; -------------         -----
; | y | x | z | --->  =>| x |<=
; -------------         -----
;      ||               | z |
;                       -----
(:action Rotate_2x6_middle_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?x ?z)
      (has_right ?y ?x)
      (has_left ?z ?x)
      (has_left ?x ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?z))
      (not (has_right ?y ?x))
      (not (has_left ?z ?x))
      (not (has_left ?x ?y))
      (has_lower ?y ?x)
      (has_lower ?x ?z)
      (has_upper ?z ?x)
      (has_upper ?x ?y)
    )
)
; 3.16 action of rotating the middle holded 2x6_loaded Gripper V2H Anticlockwise
;                       -----
;      ||               | z |
; -------------         -----
; | y | x | z | --->  =>| x |<=
; -------------         -----
;      ||               | y |
;                       -----
(:action Rotate_2x6_middle_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?x ?z)
      (has_right ?y ?x)
      (has_left ?z ?x)
      (has_left ?x ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?x ?z))
      (not (has_right ?y ?x))
      (not (has_left ?z ?x))
      (not (has_left ?x ?y))
      (has_lower ?z ?x)
      (has_lower ?x ?y)
      (has_upper ?y ?x)
      (has_upper ?x ?z)
    )
)
; 3.17 action of rotating the right holded 2x6_loaded Gripper V2H clockwise
;                       -----
;           ||          | z |
; -------------         -----
; | z | y | x | --->    | y |
; -------------         -----
;           ||        =>| x |<=
;                       -----
(:action Rotate_2x6_right_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?z ?y)
      (has_right ?y ?x)
      (has_left ?y ?z)
      (has_left ?x ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?z ?y))
      (not (has_right ?y ?x))
      (not (has_left ?y ?z))
      (not (has_left ?x ?y))
      (has_lower ?z ?y)
      (has_lower ?y ?x)
      (has_upper ?y ?z)
      (has_upper ?x ?y)
    )
)
; 3.18 action of rotating the right holded 2x6_loaded Gripper V2H Anticlockwise
;                       -----
;           ||        =>| x |<=
; -------------         -----
; | z | y | x | --->    | y |
; -------------         -----
;           ||          | z |
;                       -----
(:action Rotate_2x6_right_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (vertical ?g)
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_right ?z ?y)
      (has_right ?y ?x)
      (has_left ?y ?z)
      (has_left ?x ?y)
    )
    :effect 
    (and
      (not (vertical ?g))
      (not (has_right ?z ?y))
      (not (has_right ?y ?x))
      (not (has_left ?y ?z))
      (not (has_left ?x ?y))
      (has_lower ?x ?y)
      (has_lower ?y ?z)
      (has_upper ?y ?x)
      (has_upper ?z ?y)
    )
)
; 3.19 action of rotating the upper holded 6x2_loaded Gripper H2V clockwise
;   -----
; =>| x |<=               ||
;   -----       -------------
;   | y |  ---> | z | y | x |
;   -----       -------------
;   | z |                 ||
;   -----
(:action Rotate_6x2_upper_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?z ?y)
      (has_upper ?y ?x)
      (has_lower ?y ?z)
      (has_lower ?x ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?z ?y))
      (not (has_upper ?y ?x))
      (not (has_lower ?y ?z))
      (not (has_lower ?x ?y))
      (has_right ?z ?y)
      (has_right ?y ?x)
      (has_left ?y ?z)
      (has_left ?x ?y)
    )
)
; 3.20 action of rotating the upper holded 6x2_loaded Gripper H2V Anticlockwise
;   -----
; =>| x |<=      ||
;   -----       -------------
;   | y |  ---> | x | y | z |
;   -----       -------------
;   | z |        ||
;   -----
(:action Rotate_6x2_upper_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?z ?y)
      (has_upper ?y ?x)
      (has_lower ?y ?z)
      (has_lower ?x ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?z ?y))
      (not (has_upper ?y ?x))
      (not (has_lower ?y ?z))
      (not (has_lower ?x ?y))
      (has_right ?x ?y)
      (has_right ?y ?z)
      (has_left ?y ?x)
      (has_left ?z ?y)
    )
)
; 3.21 action of rotating the middle holded 6x2_loaded Gripper H2V clockwise
;   -----
;   | y |               ||
;   -----         -------------
; =>| x |<=  ---> | z | x | y |
;   -----         -------------
;   | z |               ||
;   -----
(:action Rotate_6x2_middle_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?z ?x)
      (has_upper ?x ?y)
      (has_lower ?y ?x)
      (has_lower ?x ?z)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?z ?x))
      (not (has_upper ?x ?y))
      (not (has_lower ?y ?x))
      (not (has_lower ?x ?z))
      (has_right ?z ?x)
      (has_right ?x ?y)
      (has_left ?y ?x)
      (has_left ?x ?z)
    )
)
; 3.22 action of rotating the middle holded 6x2_loaded Gripper H2V Anticlockwise
;   -----
;   | y |               ||
;   -----         -------------
; =>| x |<=  ---> | y | x | z |
;   -----         -------------
;   | z |               ||
;   -----
(:action Rotate_6x2_middle_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?z ?x)
      (has_upper ?x ?y)
      (has_lower ?y ?x)
      (has_lower ?x ?z)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?z ?x))
      (not (has_upper ?x ?y))
      (not (has_lower ?y ?x))
      (not (has_lower ?x ?z))
      (has_right ?y ?x)
      (has_right ?x ?z)
      (has_left ?z ?x)
      (has_left ?x ?y)
    )
)
; 3.23 action of rotating the lower holded 6x2_loaded Gripper H2V clockwise
;   -----
;   | z |        ||
;   -----       -------------
;   | y |  ---> | x | y | z |
;   -----       -------------
; =>| x |<=      ||
;   -----
(:action Rotate_6x2_lower_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?x ?y)
      (has_upper ?y ?z)
      (has_lower ?y ?x)
      (has_lower ?z ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?x ?y))
      (not (has_upper ?y ?z))
      (not (has_lower ?y ?x))
      (not (has_lower ?z ?y))
      (has_right ?x ?y)
      (has_right ?y ?z)
      (has_left ?y ?x)
      (has_left ?z ?y)
    )
)
; 3.24 action of rotating the lower holded 6x2_loaded Gripper H2V Anticlockwise
;   -----
;   | z |                 ||
;   -----       -------------
;   | y |  ---> | z | y | x |
;   -----       -------------
; =>| x |<=               ||
;   -----
(:action Rotate_6x2_lower_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x ?y ?z - Block)
    :precondition 
    (and 
      (loaded ?x ?g)
      (not (is_open ?g))
      (not (vertical ?g))
      (not (single ?x))
      (not (single ?y))
      (not (single ?z))
      (not (connected ?x ?y))
      (not (connected ?x ?z))
      (not (connected ?y ?x))
      (not (connected ?y ?z))
      (not (connected ?z ?y))
      (not (connected ?z ?x))
      (double_connected ?x ?y ?z)
      (double_connected ?x ?z ?y)
      (double_connected ?y ?x ?z)
      (double_connected ?y ?z ?x)
      (double_connected ?z ?y ?x)
      (double_connected ?z ?x ?y)
      (has_upper ?x ?y)
      (has_upper ?y ?z)
      (has_lower ?y ?x)
      (has_lower ?z ?y)
    )
    :effect 
    (and
      (vertical ?g)
      (not (has_upper ?x ?y))
      (not (has_upper ?y ?z))
      (not (has_lower ?y ?x))
      (not (has_lower ?z ?y))
      (has_right ?z ?y)
      (has_right ?y ?x)
      (has_left ?y ?z)
      (has_left ?x ?y)
    )
)
;==============================================
; 4. Loaded Gripper Movement Group of Actions |
;==============================================
;------------------------------------------------------------
; Note: All the Take Actions are meant to be to Air,  and   |
;    Vise-versa Put Actions are done from point on Air.     |
;    No on-Air colloision detection assertion is done here! |
;------------------------------------------------------------
; 4.1 action of taking the 2x2_loaded Gripper
;  ||
; -----     -----
; | x | ; =>| x |<=
; -----     -----
;  ||
(:action take_2x2_gripper
  :parameters (?x - Block ?g - Gripper ?pos ?point_air - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (belong ?x ?pos); x
  (single ?x)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (not (belong ?x ?pos))
  (empty_location ?pos)
  )
)
; 4.2 action of taking the left holded 2x4_loaded Gripper
;  ||
; ---------
; | x | y |
; ---------
;  ||
(:action take_left_2x4_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_right)); x
  (not (= ?pos ?pos_right))
  (right ?pos_right ?pos)
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (belong ?x ?pos); x
  (belong ?y ?pos_right); x
  (has_left ?y ?x)
  (has_right ?x ?y)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_right)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_right))  
  )
)
; 4.3 action of taking the right holded 2x4_loaded Gripper
;       ||
; ---------
; | y | x |
; ---------
;       ||
(:action take_right_2x4_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_left)); x
  (not (= ?pos ?pos_left))
  (left ?pos_left ?pos)
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (belong ?x ?pos); x
  (belong ?y ?pos_left); x
  (has_left ?y ?x)
  (has_right ?x ?y)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_left)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_left))  
  )
)
; 4.4 action of taking the upper holded 4x2_loaded Gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
(:action take_upper_4x2_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_lower - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_lower)); x
  (not (= ?pos ?pos_lower))
  (down ?pos_lower ?pos)
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (belong ?x ?pos); x
  (belong ?y ?pos_lower); x
  (has_left ?y ?x)
  (has_right ?x ?y)
  )
  :effect 
  (and
  (at ?g ?point_air); x
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_lower)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_lower))  
  )
)
; 4.5 action of taking the upper holded 4x2_loaded Gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:action take_lower_4x2_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_upper - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_upper)); x
  (not (= ?pos ?pos_upper))
  (up ?pos_upper ?pos)
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (belong ?x ?pos); x
  (belong ?y ?pos_upper); x
  (has_left ?y ?x)
  (has_right ?x ?y)
  )
  :effect 
  (and 
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_upper)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_upper))  
  )
)
; 4.6 action of taking the left holded 2x6_loaded Gripper
;  ||
; -------------
; | x | y | z |
; -------------
;  ||
(:action take_left_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_right ?pos_right_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_right)); x
  (not (empty_location ?pos_right_right)); x
  (not (= ?pos ?pos_right))
  (not (= ?pos ?pos_right_right))
  (not (= ?pos_right ?pos_right_right))
  (right ?pos_right ?pos)
  (right ?pos_right ?pos_right_right)
  (left ?pos ?pos_right)
  (left ?pos_right_right ?pos_right)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_right); x
  (belong ?z ?pos_right_right); x
  (has_right ?y ?z)
  (has_right ?x ?y) 
  (has_left ?y ?x)
  (has_left ?z ?y)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_right)
  (empty_location ?pos_right_right)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_right))
  (not (belong ?z ?pos_right_right))
  )
)
; 4.7 action of taking the middle holded 2x6_loaded Gripper
;       ||
; -------------
; | y | x | z |
; -------------
;       ||
(:action take_middle_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_right ?pos_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_right)); x
  (not (empty_location ?pos_left)); x
  (not (= ?pos ?pos_right))
  (not (= ?pos ?pos_left))
  (not (= ?pos_right ?pos_left))
  (right ?pos_right ?pos)
  (left ?pos ?pos_right)
  (right ?pos ?pos_left)
  (left ?pos_left ?pos)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_left); x
  (belong ?z ?pos_right); x  
  (has_right ?x ?z)
  (has_right ?y ?x)
  (has_left ?x ?y)
  (has_left ?z ?x)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_right)
  (empty_location ?pos_left)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_left))
  (not (belong ?z ?pos_right))
  )
)
; 4.8 action of taking the right holded 2x6_loaded Gripper
;           ||
; -------------
; | z | y | x |
; -------------
;           ||
(:action take_right_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_left ?pos_left_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_left)); x
  (not (empty_location ?pos_left_left)); x
  (not (= ?pos ?pos_left))
  (not (= ?pos ?pos_left_left))
  (not (= ?pos_left ?pos_left_left))
  (left ?pos_left ?pos)
  (left ?pos_left_left ?pos_left)
  (right ?pos ?pos_left)
  (right ?pos_left ?pos_left_left)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_left); x
  (belong ?z ?pos_left_left); x  
  (has_right ?x ?z)
  (has_right ?y ?x)
  (has_left ?x ?y)
  (has_left ?z ?x)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_left)
  (empty_location ?pos_left_left)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_left))
  (not (belong ?z ?pos_left_left))
  )
)
; 4.9 action of taking the upper holded 6x2_loaded Gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
;   | z |
;   -----
(:action take_upper_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_lower ?pos_lower_lower - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_lower)); x
  (not (empty_location ?pos_lower_lower)); x
  (not (= ?pos ?pos_lower))
  (not (= ?pos ?pos_lower_lower))
  (not (= ?pos_lower ?pos_lower_lower))
  (up ?pos ?pos_lower)
  (up ?pos_lower ?pos_lower_lower)
  (down ?pos_lower ?pos)
  (down ?pos_lower_lower ?pos_lower)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_lower); x
  (belong ?z ?pos_lower_lower); x
  (has_upper ?y ?x)
  (has_upper ?z ?y)
  (has_lower ?x ?y)
  (has_lower ?y ?z)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_lower)
  (empty_location ?pos_lower_lower)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_lower))
  (not (belong ?z ?pos_lower_lower))
  )
)
; 4.10 action of taking the middle holded 6x2_loaded Gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
;   | z |
;   -----
(:action take_middle_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_upper)); x
  (not (empty_location ?pos_lower)); x
  (not (= ?pos ?pos_upper))
  (not (= ?pos ?pos_lower))
  (not (= ?pos_upper ?pos_lower))
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos_lower ?pos)
  (down ?pos ?pos_upper)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_upper); x
  (belong ?z ?pos_lower); x
  (has_upper ?x ?y)
  (has_upper ?z ?x)
  (has_lower ?y ?x)
  (has_lower ?x ?z)
  )
  :effect 
  (and
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_upper))
  (not (belong ?z ?pos_lower))
  )
)
; 4.11 action of taking the lower holded 6x2_loaded Gripper
;   -----
;   | z |
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:action take_lower_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_upper_upper - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?pos); x
  (not (at ?g ?point_air)); x
  (not (empty_location ?pos)); x
  (not (empty_location ?pos_upper)); x
  (not (empty_location ?pos_upper_upper)); x
  (not (= ?pos ?pos_upper))
  (not (= ?pos ?pos_upper_upper))
  (not (= ?pos_upper ?pos_upper_upper))
  (up ?pos_upper ?pos)
  (up ?pos_upper_upper ?pos_upper)
  (down ?pos ?pos_upper)
  (down ?pos_upper ?pos_upper_upper)
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (belong ?x ?pos); x
  (belong ?y ?pos_upper); x
  (belong ?z ?pos_upper_upper); x
  (has_upper ?x ?y)
  (has_upper ?y ?z)
  (has_lower ?y ?x)
  (has_lower ?z ?y)
  )
  :effect 
  (and 
  (at ?g ?point_air)
  (not (at ?g ?pos))
  (empty_location ?pos)
  (empty_location ?pos_upper)
  (empty_location ?pos_upper_upper)
  (not (belong ?x ?pos))
  (not (belong ?y ?pos_upper))
  (not (belong ?z ?pos_upper_upper))
  )
)
; 4.12 action of putting the 2x2_loaded Gripper
;  ||
; -----
; | x |
; -----
;  ||
(:action put_2x2_gripper_V
  :parameters (?x - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (empty_location ?pos); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  (single ?x)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (not (empty_location ?pos))
  )
)
; 4.13 action of putting the 2x2_loaded Gripper
;   -----
; =>| x |<=
;   -----
(:action put_2x2_gripper_H
  :parameters (?x - Block ?g - Gripper ?pos ?point_air ?pos_right ?pos_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (right ?pos_right ?pos)
  (right ?pos ?pos_left)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (empty_location ?pos); x
  (empty_location ?pos_right)
  (empty_location ?pos_left)
  (single ?x)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (not (empty_location ?pos))
  )
)
; 4.14 action of putting the left holded 2x4_loaded Gripper
;  ||
; ---------
; | x | y |
; ---------
;  ||
(:action put_left_2x4_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower ?pos_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (has_right ?x ?y)
  (has_left ?y ?x)
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (right ?pos_right ?pos)
  (left ?pos ?pos_right)
  (empty_location ?pos); x
  (empty_location ?pos_right); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_right)
  (not (empty_location ?pos))
  (not (empty_location ?pos_right))
  )
)
; 4.15 action of putting the right holded 2x4_loaded Gripper
;       ||
; ---------
; | y | x |
; ---------
;       ||
(:action put_right_2x4_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower ?pos_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (has_right ?y ?x)
  (has_left ?x ?y)
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (left ?pos_left ?pos)
  (right ?pos ?pos_left)
  (empty_location ?pos); x
  (empty_location ?pos_left); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_left)
  (not (empty_location ?pos))
  (not (empty_location ?pos_left))
  )
)
; 4.16 action of putting the upper holded 4x2_loaded Gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
(:action put_upper_4x2_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_lower ?pos_left ?pos_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (has_upper ?y ?x)
  (has_lower ?x ?y)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (right ?pos ?pos_left)
  (right ?pos_right ?pos)
  (up ?pos ?pos_lower)
  (down ?pos_lower ?pos)
  (empty_location ?pos); x
  (empty_location ?pos_lower); x
  (empty_location ?pos_left)
  (empty_location ?pos_right)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_lower)
  (not (empty_location ?pos))
  (not (empty_location ?pos_lower))
  )
)
; 4.17 action of putting the lower holded 4x2_loaded Gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:action put_lower_4x2_gripper
  :parameters (?x ?y - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_left ?pos_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (connected ?x ?y)
  (connected ?y ?x)
  (has_upper ?x ?y)
  (has_lower ?y ?x)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (right ?pos ?pos_left)
  (right ?pos_right ?pos)
  (up ?pos_upper ?pos)
  (down ?pos ?pos_upper)
  (empty_location ?pos); x
  (empty_location ?pos_upper); x
  (empty_location ?pos_left)
  (empty_location ?pos_right)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_upper)
  (not (empty_location ?pos))
  (not (empty_location ?pos_upper))
  )
)
; 4.18 action of putting the left holded 2x6_loaded Gripper
;  ||
; -------------
; | x | y | z |
; -------------
;  ||
(:action put_left_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower ?pos_right ?pos_right_right - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_right ?x ?y)
  (has_right ?y ?z)
  (has_left ?y ?x)
  (has_left ?z ?y)
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (right ?pos_right ?pos)
  (right ?pos_right_right ?pos_right)
  (left ?pos ?pos_right)
  (left ?pos_right ?pos_right_right)
  (empty_location ?pos); x
  (empty_location ?pos_right); x
  (empty_location ?pos_right_right); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_right)
  (belong ?z ?pos_right_right)
  (not (empty_location ?pos))
  (not (empty_location ?pos_right))
  (not (empty_location ?pos_right_right))
  )
)
; 4.19 action of putting the middle holded 2x6_loaded Gripper
;      ||
; -------------
; | y | x | z |
; -------------
;      ||
(:action put_middle_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower ?pos_right ?pos_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_right ?y ?x)
  (has_right ?x ?z)
  (has_left ?x ?y)
  (has_left ?z ?x)
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (right ?pos_right ?pos)
  (right ?pos ?pos_left)
  (left ?pos ?pos_right)
  (left ?pos_left ?pos)
  (empty_location ?pos); x
  (empty_location ?pos_right); x
  (empty_location ?pos_left); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_left)
  (belong ?z ?pos_right)
  (not (empty_location ?pos))
  (not (empty_location ?pos_right))
  (not (empty_location ?pos_left))
  )
)
; 4.20 action of putting the right holded 2x6_loaded Gripper
;           ||
; -------------
; | z | y | x |
; -------------
;           ||
(:action put_right_2x6_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_upper ?pos_lower ?pos_left ?pos_left_left - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (vertical ?g)
  (at ?g ?point_air); x
  (not (at ?g ?pos)); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_right ?y ?x)
  (has_right ?z ?y)
  (has_left ?x ?y)
  (has_left ?y ?z)
  (up ?pos_upper ?pos)
  (up ?pos ?pos_lower)
  (down ?pos ?pos_upper)
  (down ?pos_lower ?pos)
  (right ?pos ?pos_left)
  (right ?pos_left ?pos_left_left)
  (left ?pos_left ?pos)
  (left ?pos_left_left ?pos_left)
  (empty_location ?pos); x
  (empty_location ?pos_left); x
  (empty_location ?pos_left_left); x
  (empty_location ?pos_upper)
  (empty_location ?pos_lower)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_left)
  (belong ?z ?pos_left_left)
  (not (empty_location ?pos))
  (not (empty_location ?pos_left))
  (not (empty_location ?pos_left_left))
  )
)
; 4.21 action of putting the upper holded 2x6_loaded Gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
;   | z |
;   -----
(:action put_upper_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_left ?pos_right ?pos_lower ?pos_lower_lower - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (not (at ?g ?pos)); x
  (at ?g ?point_air); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_upper ?y ?x)
  (has_upper ?z ?y)
  (has_lower ?x ?y)
  (has_lower ?y ?z)
  (up ?pos ?pos_lower)
  (up ?pos_lower ?pos_lower_lower)
  (down ?pos_lower ?pos)
  (down ?pos_lower_lower ?pos_lower)
  (right ?pos_right ?pos)
  (right ?pos ?pos_left)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (empty_location ?pos); x
  (empty_location ?pos_lower); x
  (empty_location ?pos_lower_lower); x
  (empty_location ?pos_right)
  (empty_location ?pos_left)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_lower)
  (belong ?z ?pos_lower_lower)
  (not (empty_location ?pos))
  (not (empty_location ?pos_lower))
  (not (empty_location ?pos_lower_lower))
  )
)
; 4.22 action of putting the middle holded 2x6_loaded Gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
;   | z |
;   -----
(:action put_middle_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_left ?pos_right ?pos_lower ?pos_upper - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (not (at ?g ?pos)); x
  (at ?g ?point_air); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_upper ?x ?y)
  (has_upper ?z ?x)
  (has_lower ?y ?x)
  (has_lower ?x ?z)
  (up ?pos ?pos_lower)
  (up ?pos_upper ?pos)
  (down ?pos_lower ?pos)
  (down ?pos ?pos_upper)
  (right ?pos_right ?pos)
  (right ?pos ?pos_left)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (empty_location ?pos); x
  (empty_location ?pos_upper); x 
  (empty_location ?pos_lower); x
  (empty_location ?pos_right)
  (empty_location ?pos_left)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_upper)
  (belong ?z ?pos_lower)
  (not (empty_location ?pos))
  (not (empty_location ?pos_upper))
  (not (empty_location ?pos_lower))
  )
)
; 4.23 action of putting the lower holded 2x6_loaded Gripper
;   -----
;   | z |
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:action put_lower_6x2_gripper
  :parameters (?x ?y ?z - Block ?g - Gripper ?pos ?point_air ?pos_left ?pos_right ?pos_upper ?pos_upper_upper - Location)
  :precondition 
  (and 
  (loaded ?x ?g)
  (not (is_open ?g))
  (not (vertical ?g))
  (not (at ?g ?pos)); x
  (at ?g ?point_air); x
  (not (single ?x))
  (not (single ?y))
  (not (single ?z))
  (not (connected ?x ?y))
  (not (connected ?x ?z))
  (not (connected ?y ?x))
  (not (connected ?y ?z))
  (not (connected ?z ?y))
  (not (connected ?z ?x))
  (double_connected ?x ?y ?z)
  (double_connected ?x ?z ?y)
  (double_connected ?y ?x ?z)
  (double_connected ?y ?z ?x)
  (double_connected ?z ?y ?x)
  (double_connected ?z ?x ?y)
  (has_upper ?x ?y)
  (has_upper ?y ?z)
  (has_lower ?y ?x)
  (has_lower ?z ?y)
  (up ?pos_upper ?pos)
  (up ?pos_upper_upper ?pos_upper)
  (down ?pos ?pos_upper)
  (down ?pos_upper ?pos_upper_upper)
  (right ?pos_right ?pos)
  (right ?pos ?pos_left)
  (left ?pos_left ?pos)
  (left ?pos ?pos_right)
  (empty_location ?pos); x
  (empty_location ?pos_upper); x 
  (empty_location ?pos_upper_upper); x
  (empty_location ?pos_right)
  (empty_location ?pos_left)
  )
  :effect 
  (and 
  (at ?g ?pos)
  (not (at ?g ?point_air))
  (belong ?x ?pos)
  (belong ?y ?pos_upper)
  (belong ?z ?pos_upper_upper)
  (not (empty_location ?pos))
  (not (empty_location ?pos_upper))
  (not (empty_location ?pos_upper_upper))
  )
)
;==============================
; 5. Utility Group of Actions |
;==============================
; 5.1 action of filling empty robot stock 2x2_blue
;  ||
; -----     -----
; | B | ; =>| B |<=
; -----     -----
;  ||
(:action fill_stock_2x2_blue
    :parameters (?x - Block ?pos - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (belong ?x ?pos)
    (single ?x)
    (color_blue ?x)
    )
)
; 5.2 action of filling empty robot stock 2x2_yellow
;  ||
; -----     -----
; | y | ; =>| y |<=
; -----     -----
;  ||
(:action fill_stock_2x2_yellow
    :parameters (?x - Block ?pos - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (belong ?x ?pos)
    (single ?x)
    (color_yellow ?x)
    )
)
; 5.3 action of filling empty robot stock 2x4_blue
;       ||
; ---------
; | y | x | Blue
; ---------
;       ||
(:action fill_stock_2x4_blue
    :parameters (?x ?y - Block ?pos ?pos_left - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    (empty_location ?pos_left)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (not (empty_location ?pos_left))
    (belong ?x ?pos)
    (belong ?y ?pos_left)
    (has_left ?x ?y)
    (has_right ?y ?x)
    (connected ?x ?y)
    (connected ?y ?x)
    (color_blue ?x)
    (color_blue ?y)
    )
)
; 5.4 action of filling empty robot stock 2x4_yellow
;       ||
; ---------
; | y | x | Yellow
; ---------
;       ||
(:action fill_stock_2x4_yellow
    :parameters (?x ?y - Block ?pos ?pos_left - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    (empty_location ?pos_left)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (not (empty_location ?pos_left))
    (belong ?x ?pos)
    (belong ?y ?pos_left)
    (has_left ?x ?y)
    (has_right ?y ?x)
    (connected ?x ?y)
    (connected ?y ?x)
    (color_yellow ?x)
    (color_yellow ?y)
    )
)
; 5.5 action of filling empty robot stock 2x6_blue
;           ||
; -------------
; | z | y | x | Blue
; -------------
;           ||
(:action fill_stock_2x6_blue
    :parameters (?x ?y ?z - Block ?pos ?pos_left ?pos_left_left - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    (empty_location ?pos_left)
    (empty_location ?pos_left_left)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (not (empty_location ?pos_left))
    (not (empty_location ?pos_left_left))
    (belong ?x ?pos)
    (belong ?y ?pos_left)
    (belong ?z ?pos_left_left)
    (has_left ?x ?y)
    (has_left ?y ?z)
    (has_right ?y ?x)
    (has_right ?z ?y)
    (double_connected ?x ?y ?z)
    (double_connected ?x ?z ?y)
    (double_connected ?y ?x ?z)
    (double_connected ?y ?z ?x)
    (double_connected ?z ?y ?x)
    (double_connected ?z ?x ?y)
    (color_blue ?x)
    (color_blue ?y)
    (color_blue ?z)
    )
)
; 5.6 action of filling empty robot stock 2x6_blue
;           ||
; -------------
; | z | y | x | Yellow
; -------------
;           ||
(:action fill_stock_2x6_yellow
    :parameters (?x ?y ?z - Block ?pos ?pos_left ?pos_left_left - Location)
    :precondition 
    (and 
    (empty_location ?pos)
    (empty_location ?pos_left)
    (empty_location ?pos_left_left)
    )
    :effect 
    (and 
    (not (empty_location ?pos))
    (not (empty_location ?pos_left))
    (not (empty_location ?pos_left_left))
    (belong ?x ?pos)
    (belong ?y ?pos_left)
    (belong ?z ?pos_left_left)
    (has_left ?x ?y)
    (has_left ?y ?z)
    (has_right ?y ?x)
    (has_right ?z ?y)
    (double_connected ?x ?y ?z)
    (double_connected ?x ?z ?y)
    (double_connected ?y ?x ?z)
    (double_connected ?y ?z ?x)
    (double_connected ?z ?y ?x)
    (double_connected ?z ?x ?y)
    (color_yellow ?x)
    (color_yellow ?y)
    (color_yellow ?z)
    )
)

)