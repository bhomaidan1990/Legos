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
  :strips ; add delete effects.
  :typing ; add types.
  :hierarchy ; add tasks - subtasks ... etc.
  :method-preconditions ; add preconditions to the methods.
  :negative-preconditions ; add negative preconditions.
)
;----------------
;   Types
;----------------
(:types
  Point_Air - Location ; Point at Air
  Point_Workspace - Location ; Workspace Point
  Location - object 
  Block_2x2 - Block ; Block 2x2
  Block_2x4 - Block ; Block 2x4
  Block_2x6 - Block ; Block 2x6
  Block - object
  Gripper - object ; holds at most 1 Lego, only 1 Gripper per Location
  Direction - object ; direction of the lego placement  H: ====  V: ||
)
;-------------------------------------------------------------------------
;                          Predicates                                    |
;-------------------------------------------------------------------------
(:predicates
  ;; directions
  (left ?l1 - Point_Workspace ?l2 - Point_Workspace); Location l1 is to the left of l2.
  (right ?l1 - Point_Workspace ?l2 - Point_Workspace); Location l1 is to the right of l2.
  (up ?l1 - Point_Workspace ?l2 - Point_Workspace); Location l1 is to the upper side of l2.
  (down ?l1 - Point_Workspace ?l2 - Point_Workspace); Location l1 is to the lower side of l2.
  ; place of Lego
  (empty_location ?pos - Point_Workspace)
  ; holding point
  (held_from_left ?x - Block) ; if the block is held from left side.
  (held_from_right ?x - Block); if the block is held from right side.
  (held_from_middle ?x - Block); if the block is held from the middle.
  (held_from_top ?x - Block) ; if the block is held from top side.
  (held_from_bottom ?x - Block); if the block is held from bottom side.
  ;; define the orientation of the Gripper
  (gripper_vertical ?g - Gripper); Gripper g mode is vertical(movement is in x direction).
  ;; define the state of the Grippers
  (is_open ?g - Gripper); Gripper g is open.
  (unloaded ?g - Gripper); Gripper g is uloaded.
  (loaded ?g - Gripper ?x - Block); Gripper g is loaded with Lego block.
  (at ?g - Gripper ?l - Location); Gripper g is in Location l.
  ; (reachable ?g - Gripper ?l - Location); to define whether if this location is reachable by this gripper.
  ; holding direction
  (left_direction ?d - Direction)
  (right_direction ?d - Direction)
  (middle_direction ?d - Direction)
  (top_direction ?d - Direction)
  (bottom_direction ?d - Direction)
  ; attached to prevent picking blocks from Workspace
  (attached ?x - Block)
)

;-------------------------------------------------------------------------
;                               Tasks                                    |
;-------------------------------------------------------------------------
; 1. The task of picking a Lego.
(:task pick
  :parameters (?g - Gripper ?x - Block ?d - Direction)
)
; 2. The task of placing a Lego.
(:task place
  :parameters (?g - Gripper ?x - Block ?pos - Point_Workspace)
)
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
; 1.2 action of holding 2x2 block with the Gripper
;                ||
;   -----      -----
; =>| x |<= ,  | x |
;   -----      -----
;                ||
(:action Hold_gripper
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and
    (loaded ?g ?x)
    (not (is_open ?g))
    (not(unloaded ?g))
  )
)
; 1.3 action of holding block with the Gripper from left
;  ||              ||
; -------------   ---------
; | x | y | z | , | x | y |
; -------------   ---------
;  ||              ||
(:action Hold_gripper_left
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and
    (loaded ?g ?x)
    (not (is_open ?g))
    (not(unloaded ?g))
    (held_from_left ?x)
  )
)
; 1.4 action of holding block with the Gripper from right
;           ||          ||
; -------------   ---------
; | x | y | z | , | x | y |
; -------------   ---------
;           ||          ||
(:action Hold_gripper_right
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and
    (loaded ?g ?x)
    (not (is_open ?g))
    (not(unloaded ?g))
    (held_from_right ?x)
  )
)
; 1.5 action of holding block with the Gripper from top
;   -----
; =>| x |<=      -----
;   -----      =>| x |<=
;   | y |   ,    -----
;   -----        | y |
;   | z |        -----
;   -----
(:action Hold_gripper_top
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and 
    (not (is_open ?g))
    (loaded ?g ?x)
    (not(unloaded ?g))
    (held_from_top ?x)
  )
)
; 1.6 action of holding block with the Gripper from bottom
;   -----
;   | z |        -----
;   -----        | y |
;   | y |   ,    -----
;   -----      =>| x |<=
; =>| x |<=      -----
;   -----
(:action Hold_gripper_bottom
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and 
    (not (is_open ?g))
    (loaded ?g ?x)
    (not(unloaded ?g))
    (held_from_bottom ?x)
  )
)
; 1.7 action of holding block with the Gripper from middle
;   -----
;   | y |           ||
;   -----     -------------
; =>| x |<= , | y | x | z |
;   -----     -------------
;   | z |           ||
;   -----
(:action Hold_gripper_middle
  :parameters (?x - Block_2x6 ?g - Gripper)
  :precondition 
  (and 
    (is_open ?g)
    (unloaded ?g)
  )
  :effect
  (and 
    (not (is_open ?g))
    (loaded ?g ?x)
    (not(unloaded ?g))
    (held_from_middle ?x)
  )
)
; 1.8 action of releasing the loaded Gripper
(:action Release_gripper
  :parameters (?x - Block ?g - Gripper)
  :precondition 
  (and 
    (not (is_open ?g))
    (loaded ?g ?x)
  )
  :effect
  (and
    (is_open ?g)
    (unloaded ?g)
    (not (loaded ?g ?x))
    (not (held_from_left ?x))
    (not (held_from_right ?x))
    (not (held_from_middle ?x))
    (not (held_from_top ?x))
    (not (held_from_bottom ?x))
  )
)
;=========================================
; 2. Empty Gripper Move Group of Actions |
;=========================================
; 2.0 action of moving empty open Vertical Gripper to stock.
(:action Move_open_gripper_V_To_Stock
  :parameters (?g - Gripper ?current_point - Point_Air)
  :precondition 
  (and
      (is_open ?g)
      (unloaded ?g)
      (gripper_vertical ?g)
      (at ?g ?current_point)
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
  )
)
; 2.1 action of moving empty open Vertical Gripper to workspace.
(:action Move_open_gripper_V_To_Workspace
  :parameters (?g - Gripper ?current_point - Point_Air ?destination_point ?dest_upper ?dest_lower - Point_Workspace)
  :precondition 
  (and
      (is_open ?g)
      (unloaded ?g)
      (gripper_vertical ?g)
      (at ?g ?current_point)
      ; (reachable ?g ?destination_point)
      (up ?destination_point ?dest_upper)
      (down ?destination_point ?dest_lower)
      (empty_location ?dest_upper)
      (empty_location ?dest_lower)
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
; 2.2 action of moving empty open Horizontal Gripper to workspace.
(:action Move_open_gripper_H_To_Workspace
  :parameters (?g - Gripper ?current_point - Point_Air  ?destination_point ?dest_left ?dest_right - Point_Workspace)
  :precondition 
  (and
    (is_open ?g)
    (unloaded ?g)
    (not (gripper_vertical ?g))
    (at ?g ?current_point)
    ; (reachable ?g ?destination_point)
    (left ?destination_point ?dest_left)
    (right ?destination_point ?dest_right)
    (empty_location ?dest_left)
    (empty_location ?dest_right)
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
; 2.3 action of moving empty open Gripper from workspace
(:action Move_open_gripper_From_Workspace
  :parameters (?g - Gripper ?current_point - Point_Workspace ?destination_point - Point_Air)
  :precondition 
  (and
      (is_open ?g)
      (unloaded ?g)
      (at ?g ?current_point)
      ; (reachable ?g ?destination_point)
  )
  :effect 
  (and 
    (not(at ?g ?current_point))
    (at ?g ?destination_point)
  )
)
; ======================================
; 3. Gripper Rotation Group of Actions |
; ======================================
; -------------------------------------------------
; Note: All the Rotations are meant to be on Air, |
;    No collosion detection or neighboring        |
;        position assertion is done here!         |
; -------------------------------------------------
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
    (not (gripper_vertical ?g))
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
    (gripper_vertical ?g)
  )
)
; 3.3 action of rotating the 2x2_loaded Gripper V2H
;  ||
; -----          -----
; | x |  --->  =>| x |<=
; -----          -----
;  ||
(:action Rotate_2x2_loaded_gripper_V2H
  :parameters (?g - Gripper ?x - Block_2x2)
  :precondition 
  (and
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
  )
  :effect
  (and 
    (not (gripper_vertical ?g))
  )
)
; 3.4 action of rotating the 2x2_loaded Gripper H2V
;                  ||
;   -----         -----
; =>| x |<=  ---> | x |
;   -----         -----
;                  ||
(:action Rotate_2x2_loaded_gripper_H2V
  :parameters (?g - Gripper ?x - Block_2x2)
  :precondition 
  (and
    (loaded ?g ?x)
    (not (is_open ?g))
    (not(gripper_vertical ?g))
  )
  :effect
  (and 
    (gripper_vertical ?g)
  )
)
; 3.5 action of rotating the left holded 2x4_loaded Gripper V2H clockwise
;  ||               -----
; ---------       =>| x |<=
; | x | y |  --->   -----
; ---------         | y |
;  ||               -----
(:action Rotate_2x4_left_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_left ?x)
      
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_left ?x))
      (held_from_top ?x)
    )
)
; 3.6 action of rotating the left holded 2x4_loaded Gripper V2H Anti-clockwise
;  ||               -----
; ---------         | y |
; | x | y |  --->   -----
; ---------       =>| x |<=
;  ||               -----
(:action Rotate_2x4_left_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_left ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_left ?x))
      (held_from_bottom ?x)
    )
)
; 3.7 action of rotating the right holded 2x4_loaded Gripper V2H clockwise
;       ||          -----
; ---------         | y |
; | y | x |  --->   -----
; ---------       =>| x |<=
;       ||          -----
(:action Rotate_2x4_right_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_right ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_right ?x))
      (held_from_bottom ?x)
    )
)
; 3.8 action of rotating the right holded 2x4_loaded Gripper V2H Anti-clockwise
;       ||          -----
; ---------       =>| x |<=
; | y | x |  --->   -----
; ---------         | y |
;       ||          -----
(:action Rotate_2x4_right_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_right ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_right ?x))
      (held_from_top ?x)
    )
)
; 3.9 action of rotating the upper holded 4x2_loaded Gripper H2V clockwise
;   -----              ||
; =>| x |<=      ---------
;   -----   ---> | y | x | 
;   | y |        ---------
;   -----              ||
(:action Rotate_4x2_upper_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not(gripper_vertical ?g))
      (held_from_top ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_top ?x))
      (held_from_right ?x)
    )
)
; 3.10 action of rotating the upper holded 4x2_loaded Gripper H2V Anti-clockwise
;   -----         ||
; =>| x |<=      ---------
;   -----   ---> | x | y | 
;   | y |        ---------
;   -----         ||
(:action Rotate_4x2_upper_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not(gripper_vertical ?g))
      (held_from_top ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_top ?x))
      (held_from_left ?x)
    )
)
; 3.11 action of rotating the lower holded 4x2_loaded Gripper H2V clockwise
;   -----         ||
;   | y |        ---------
;   -----   ---> | x | y | 
; =>| x |<=      ---------
;   -----         ||
(:action Rotate_4x2_lower_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not(gripper_vertical ?g))
      (held_from_bottom ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_bottom ?x))
      (held_from_left ?x)
    )
)
; 3.12 action of rotating the lower holded 4x2_loaded Gripper H2V Anti-clockwise
;   -----              ||
;   | y |        ---------
;   -----   ---> | y | x | 
; =>| x |<=      ---------
;   -----              ||
(:action Rotate_4x2_lower_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x - Block_2x4)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not(gripper_vertical ?g))
      (held_from_bottom ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_bottom ?x))
      (held_from_right ?x)
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
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_left ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_left ?x))
      (held_from_top ?x)
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
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_left ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_left ?x))
      (held_from_bottom ?x)
    )
)
; 3.15 action of rotating the middle holded 2x6_loaded Gripper V2H
;                       -----
;      ||               | z |
; -------------         -----
; | y | x | z | --->  =>| x |<=
; -------------         -----
;      ||               | y |
;                       -----
(:action Rotate_2x6_middle_loaded_gripper_V2H
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_middle ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
    )
)
; 3.16 action of rotating the right holded 2x6_loaded Gripper V2H clockwise
;                       -----
;           ||          | z |
; -------------         -----
; | z | y | x | --->    | y |
; -------------         -----
;           ||        =>| x |<=
;                       -----
(:action Rotate_2x6_right_loaded_gripper_V2H_clk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_right ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_right ?x))
      (held_from_bottom ?x)
    )
)
; 3.17 action of rotating the right holded 2x6_loaded Gripper V2H Anticlockwise
;                       -----
;           ||        =>| x |<=
; -------------         -----
; | z | y | x | --->    | y |
; -------------         -----
;           ||          | z |
;                       -----
(:action Rotate_2x6_right_loaded_gripper_V2H_Anticlk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (gripper_vertical ?g)
      (held_from_right ?x)
    )
    :effect 
    (and
      (not (gripper_vertical ?g))
      (not (held_from_right ?x))
      (held_from_top ?x)
    )
)
; 3.18 action of rotating the upper holded 6x2_loaded Gripper H2V clockwise
;   -----
; =>| x |<=               ||
;   -----       -------------
;   | y |  ---> | z | y | x |
;   -----       -------------
;   | z |                 ||
;   -----
(:action Rotate_6x2_upper_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not (gripper_vertical ?g))
      (held_from_top ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_top ?x))
      (held_from_right ?x)
    )
)
; 3.19 action of rotating the upper holded 6x2_loaded Gripper H2V Anticlockwise
;   -----
; =>| x |<=      ||
;   -----       -------------
;   | y |  ---> | x | y | z |
;   -----       -------------
;   | z |        ||
;   -----
(:action Rotate_6x2_upper_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not (gripper_vertical ?g))
      (held_from_top ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_top ?x))
      (held_from_left ?x)
    )
)
; 3.20 action of rotating the middle holded 6x2_loaded Gripper H2V clockwise
;   -----
;   | y |               ||
;   -----         -------------
; =>| x |<=  ---> | z | x | y |
;   -----         -------------
;   | z |               ||
;   -----
(:action Rotate_6x2_middle_loaded_gripper_H2V
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not (gripper_vertical ?g))
      (held_from_middle ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
    )
)
; 3.21 action of rotating the lower holded 6x2_loaded Gripper H2V clockwise
;   -----
;   | z |        ||
;   -----       -------------
;   | y |  ---> | x | y | z |
;   -----       -------------
; =>| x |<=      ||
;   -----
(:action Rotate_6x2_lower_loaded_gripper_H2V_clk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not (gripper_vertical ?g))
      (held_from_bottom ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_bottom ?x))
      (held_from_left ?x)
    )
)
; 3.22 action of rotating the lower holded 6x2_loaded Gripper H2V Anticlockwise
;   -----
;   | z |                 ||
;   -----       -------------
;   | y |  ---> | z | y | x |
;   -----       -------------
; =>| x |<=               ||
;   -----
(:action Rotate_6x2_lower_loaded_gripper_H2V_Anticlk
    :parameters (?g - Gripper ?x - Block_2x6)
    :precondition 
    (and 
      (loaded ?g ?x)
      (not (is_open ?g))
      (not (gripper_vertical ?g))
      (held_from_bottom ?x)
    )
    :effect 
    (and
      (gripper_vertical ?g)
      (not (held_from_bottom ?x))
      (held_from_right ?x)
    )
)
;==============================================
; 4. Loaded Gripper Movement Group of Actions |
;==============================================
;------------------------------------------------------------
; Note: All the Take Actions are meant to be to Air,  and   |
;    Vise-versa Put Actions are done from point on Air.     |
;    No on-Air collosion detection assertion is done here!  |
;------------------------------------------------------------
;-------------------------
; take subset of actions |
;-------------------------
; 4.1 action of taking the vertical_loaded Gripper
;  ||  ||  ||
; -------------
; | x | x | x | ;
; -------------
;  ||  ||   ||
(:action take_V
  :parameters (?x - Block ?g - Gripper ?pa - Point_Air)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (not (attached ?x))
    ; (reachable ?g ?pa)
  )
  :effect 
  (and
    (at ?g ?pa)
  )
)
;------------------------
; Put subset of actions |
;------------------------
; 4.2 action of putting the 2x2_loaded Gripper
;  ||
; -----
; | x |
; -----
;  ||
(:action put_2x2_V
  :parameters (?x - Block_2x2 ?g - Gripper ?pa - Point_Air ?pos ?pos_upper ?pos_lower - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos ?pos_upper)
    (down ?pos_lower ?pos)
    (empty_location ?pos); x
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
  )
  :effect 
  (and 
    (at ?g ?pos)
    (not (at ?g ?pa))
    (attached ?x)
    (not (empty_location ?pos))
  )
)
; 4.13 action of putting the 2x2_loaded Gripper
;   -----
; =>| x |<=
;   -----
(:action put_2x2_H
  :parameters (?x - Block_2x2 ?g - Gripper ?pa - Point_Air ?pos ?pos_right ?pos_left - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
    (right ?pos_right ?pos)
    (right ?pos ?pos_left)
    (left ?pos_left ?pos)
    (left ?pos ?pos_right)
    (empty_location ?pos); x
    (empty_location ?pos_right)
    (empty_location ?pos_left)
  )
  :effect 
  (and 
    (at ?g ?pos)
    (not (at ?g ?pa))
    (attached ?x)
    (not (empty_location ?pos))
  )
)
; 4.14 action of putting the left holded 2x4_loaded Gripper
;  ||
; ---------
; | x | y |
; ---------
;  ||
(:action put_left_2x4
  :parameters (?x - Block_2x4 ?g - Gripper ?pa - Point_Air ?pos ?pos_upper ?pos_lower ?pos_right - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_right_2x4
  :parameters (?x - Block_2x4 ?g - Gripper ?pa - Point_Air ?pos ?pos_upper ?pos_lower ?pos_left - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_upper_4x2
  :parameters (?x - Block_2x4 ?g - Gripper ?pa - Point_Air ?pos ?pos_lower ?pos_left ?pos_right - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_lower_4x2
  :parameters (?x - Block_2x4 ?g - Gripper ?pa - Point_Air ?pos ?pos_upper ?pos_left ?pos_right - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_left_2x6
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right ?pos_right_right - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_middle_2x6
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right ?pos_left - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_right_2x6
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_left ?pos_left_left - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (gripper_vertical ?g)
    (at ?g ?pa); x
    (not (at ?g ?pos)); x
    (not (attached ?x))
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_upper_6x2
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_left ?pos_right ?pos_lower ?pos_lower_lower - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (not (at ?g ?pos)); x
    (not (attached ?x))
    (at ?g ?pa); x
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_middle_6x2
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_left ?pos_right ?pos_lower ?pos_upper - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (not (at ?g ?pos)); x
    (not (attached ?x))
    (at ?g ?pa); x
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
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
(:action put_lower_6x2
  :parameters (?x - Block_2x6 ?g - Gripper ?pa - Point_Air
   ?pos ?pos_left ?pos_right ?pos_upper ?pos_upper_upper - Point_Workspace)
  :precondition 
  (and 
    (loaded ?g ?x)
    (not (is_open ?g))
    (not (gripper_vertical ?g))
    (not (at ?g ?pos)); x
    (not (attached ?x))
    (at ?g ?pa); x
    ; (reachable ?g ?pos)
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
    (not (at ?g ?pa))
    (attached ?x)
    (not (empty_location ?pos))
    (not (empty_location ?pos_upper))
    (not (empty_location ?pos_upper_upper))
  )
)
; -------------------------------------------------------------------------
;                                Methods                                  |
; -------------------------------------------------------------------------
;=======================
; 1. Task Pick Methods |
;=======================
;------------------------------------------------------------
; Note: All pick-up methods assumes vertical gripper, and   |
;       horizontal placed Legos, since we have full control |
;       on the stock direction.                             |
;       Also Rotations if needed are done before placement  |
;       Separately                                          |
;------------------------------------------------------------
; 1.1 Method to pick-up 2x2 block
;  ||
; -----
; | x |
; -----
;  ||
(:method pick_2x2
  :parameters (?g - Gripper ?x - Block_2x2 ?d - Direction ?pa - Point_Air)
  :task (pick ?g ?x ?d)
  :precondition 
  (and
    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g)
    (Rotate_empty_gripper_V ?g)
    (Move_open_gripper_V_To_Stock ?g ?pa)
    (Hold_gripper ?x ?g)
    (take_V ?x ?g ?pa)
  )
)
; 1.2 Method to pick-up a block from left
;  ||              ||
; -------------   ---------
; | x | y | z | , | x | y |
; -------------   ---------
;  ||              ||
(:method pick_left
  :parameters (?g - Gripper ?x - Block ?d - Direction ?pa - Point_Air)
  :task (pick ?g ?x ?d)
  :precondition 
  (and
    (left_direction ?d)
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d ))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g)
    (Rotate_empty_gripper_V ?g)
    (Move_open_gripper_V_To_Stock ?g ?pa)
    (Hold_gripper_left ?x ?g)
    (take_V ?x ?g ?pa)
  )
)
; 1.3 Method to pick-up a block from right
;           ||          ||
; -------------   ---------
; | x | y | z | , | x | y |
; -------------   ---------
;           ||          ||
(:method pick_right
  :parameters (?g - Gripper ?x - Block ?d - Direction ?pa - Point_Air)
  :task (pick ?g ?x ?d)
  :precondition 
  (and
    (not (left_direction ?d))
    (right_direction ?d)
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g)
    (Rotate_empty_gripper_V ?g)
    (Move_open_gripper_V_To_Stock ?g ?pa)
    (Hold_gripper_right ?x ?g)
    (take_V ?x ?g ?pa)
  )
)
; 1.3 Method to pick-up a block from middle
;      ||
; -------------
; | y | x | z |
; -------------
;      ||
(:method pick_middle
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?pa - Point_Air)
  :task (pick ?g ?x ?d)
  :precondition 
  (and
    (not (left_direction ?d))
    (not (right_direction ?d))
    (middle_direction ?d)
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (Open_gripper ?g)
    (Rotate_empty_gripper_V ?g)
    (Move_open_gripper_V_To_Stock ?g ?pa)
    (Hold_gripper_middle ?x ?g)
    (take_V ?x ?g ?pa)
  )
)
;========================
; 2. Task Place Methods |
;========================
;------------------------------------------------------------
; Note: All place  methods assumes vertical gripper, and    |
;       horizontal placed Legos, hence one rotation only is |
;       considered if necessary.                            |
;------------------------------------------------------------
; 4.1 Method to place_down 2x2 block held with vertical gripper
;   ||
;  -----
;  | x |
;  -----
;   ||
(:method place_2x2_V
  :parameters (?g - Gripper ?x - Block_2x2 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (gripper_vertical ?g)
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (down ?pos ?pos_upper)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_2x2_V ?x ?g ?point_top ?pos ?pos_upper ?pos_lower)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.2 Method to place_down 2x2 block held with horizontal gripper
;    -----
;  =>| x |<= 
;    -----
(:method place_2x2_H
  :parameters (?g - Gripper ?x - Block_2x2 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_left ?pos_right - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (not (gripper_vertical ?g))
    (empty_location ?pos_right)
    (empty_location ?pos_left)
    (right ?pos_right ?pos)
    (right ?pos ?pos_left)
    (left ?pos_left ?pos)
    (left ?pos ?pos_right)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_2x2_H ?x ?g ?point_top ?pos ?pos_right ?pos_left)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.3 Method to place_down 2x4 block held from left with vertical gripper
;   ||
;  ---------
;  | x | y |
;  ---------
;   ||
(:method place_left_2x4
  :parameters (?g - Gripper ?x - Block_2x4 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (gripper_vertical ?g)
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (down ?pos ?pos_upper)
    (right ?pos_right ?pos)
    (left ?pos ?pos_right)

    (left_direction ?d)
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_left_2x4 ?x ?g ?point_top ?pos ?pos_upper ?pos_lower ?pos_right)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.4 Method to place_down 2x4 block held from right with vertical gripper
;        ||
;  ---------
;  | y | x |
;  ---------
;        ||
(:method place_right_2x4
  :parameters (?g - Gripper ?x - Block_2x4 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (gripper_vertical ?g)
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (down ?pos ?pos_upper)
    (left ?pos_left ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (right_direction ?d)
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_right_2x4 ?x ?g ?point_top ?pos ?pos_upper ?pos_lower ?pos_left)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)

; 4.5 Method to place_down 4x2 block held from top with horizontal gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
(:method place_upper_4x2
  :parameters (?g - Gripper ?x - Block_2x4 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_lower ?pos_left ?pos_right - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_left)
    (empty_location ?pos_right)
    (up ?pos ?pos_lower)
    (down ?pos_lower ?pos)
    (left ?pos_left ?pos)
    (left ?pos ?pos_right)
    (right ?pos_right ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (top_direction ?d)
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_upper_4x2 ?x ?g ?point_top ?pos ?pos_lower ?pos_left ?pos_right)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.6 Method to place_down 4x2 block held from top with horizontal gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:method place_lower_4x2
  :parameters (?g - Gripper ?x - Block_2x4 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_left ?pos_right - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_left)
    (empty_location ?pos_right)
    (up ?pos_upper ?pos)
    (down ?pos ?pos_upper)
    (left ?pos_left ?pos)
    (left ?pos ?pos_right)
    (right ?pos_right ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (bottom_direction ?d)
  )
  :ordered-subtasks 
  (and
    (put_lower_4x2 ?x ?g ?point_top ?pos ?pos_upper ?pos_left ?pos_right)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.7 Method to place_down 2x6 block held from left with vertical gripper
;  ||
; -------------
; | x | y | z |
; -------------
;  ||
(:method place_left_2x6
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right ?pos_right_right - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos ?pos_upper)
    (down ?pos_lower ?pos)
    (left ?pos ?pos_right)
    (left ?pos_right ?pos_right_right)
    (right ?pos_right_right ?pos_right)
    (right ?pos_right ?pos)
    
    (left_direction ?d)
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_left_2x6 ?x ?g ?point_top ?pos ?pos_upper ?pos_lower ?pos_right ?pos_right_right)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.8 Method to place_down 2x6 block held from middle with vertical gripper
;      ||
; -------------
; | y | x | z |
; -------------
;      ||
(:method place_middle_2x6
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos ?pos_upper)
    (down ?pos_lower ?pos)
    (left ?pos_left ?pos)
    (left ?pos ?pos_right)
    (right ?pos_right ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (middle_direction ?d)
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_middle_2x6 ?x ?g ?point_top ?pos ?pos_upper ?pos_lower ?pos_right ?pos_left)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.9 Method to place_down 2x6 block held from right with vertical gripper
;           ||
; -------------
; | z | y | x |
; -------------
;           ||
(:method place_right_2x6
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_left_left ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_upper)
    (empty_location ?pos_lower)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos ?pos_upper)
    (down ?pos_lower ?pos)
    (left ?pos_left ?pos)
    (left ?pos_left_left ?pos_left)
    (right ?pos_left ?pos_left_left)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (right_direction ?d)
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_right_2x6 ?x ?g ?point_top ?pos ?pos_upper ?pos_lower ?pos_left ?pos_left_left)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.10 Method to place_down 6x2 block held from top with horizontal gripper
;   -----
; =>| x |<=
;   -----
;   | y |
;   -----
;   | z |
;   -----
(:method place_top_6x2
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_lower ?pos_lower_lower ?pos_right ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_left)
    (empty_location ?pos_right)
    (up ?pos_lower ?pos_lower_lower)
    (up ?pos ?pos_lower)
    (down ?pos_lower_lower ?pos_lower)
    (down ?pos_lower ?pos)
    (left ?pos_left ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (top_direction ?d)
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_upper_6x2 ?x ?g ?point_top ?pos ?pos_left ?pos_right ?pos_lower ?pos_lower_lower)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.11 Method to place_down 6x2 block held from middle with horizontal gripper
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
;   | z |
;   -----
(:method place_middle_6x2
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_lower ?pos_right ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_left)
    (empty_location ?pos_right)
    (up ?pos_upper ?pos)
    (up ?pos ?pos_lower)
    (down ?pos ?pos_upper)
    (down ?pos_lower ?pos)
    (left ?pos_left ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (middle_direction ?d)
    (not (top_direction ?d))
    (not (bottom_direction ?d))
  )
  :ordered-subtasks 
  (and
    (put_middle_6x2 ?x ?g ?point_top ?pos ?pos_left ?pos_right ?pos_lower ?pos_upper)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
; 4.12 Method to place_down 6x2 block held from bottom with horizontal gripper
;   -----
;   | z |
;   -----
;   | y |
;   -----
; =>| x |<=
;   -----
(:method place_bottom_6x2
  :parameters (?g - Gripper ?x - Block_2x6 ?d - Direction ?point_top - Point_Air
   ?pos ?pos_upper ?pos_upper_upper ?pos_right ?pos_left - Point_Workspace)
  :task (place ?g ?x ?pos)
  :precondition 
  (and
    (empty_location ?pos_left)
    (empty_location ?pos_right)
    (up ?pos_upper ?pos)
    (up ?pos_upper_upper ?pos_upper)
    (down ?pos ?pos_upper)
    (down ?pos_upper ?pos_upper_upper)
    (left ?pos_left ?pos)
    (right ?pos ?pos_left)

    (not (left_direction ?d))
    (not (right_direction ?d))
    (not (middle_direction ?d))
    (not (top_direction ?d))
    (bottom_direction ?d)
  )
  :ordered-subtasks 
  (and
    (put_lower_6x2 ?x ?g ?point_top ?pos ?pos_left ?pos_right ?pos_upper ?pos_upper_upper)
    (Release_gripper ?x ?g)
    (Move_open_gripper_From_Workspace ?g ?pos ?point_top)
  )
)
)