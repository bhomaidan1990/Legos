# Legos Domain and Problems

> HDDL Legos Planning Domain and Problems.
> 
> @author: Belal HMEDAN

---

## Domain

---

### Types

---

- Within this domain there are three **types**:
    - **1. Location**: which refers to points in the air, or within the workspace.
    - **2. Block**: refers to a 2x2 minimal Lego-duplo block.
    - **3. Gripper**: refers to the robot gripper.

---

### Tasks

---

- The main **tasks** to be achieved are:
    - 1. The task of **picking** a Lego:
    `(:task pick
  :parameters (?g - Gripper ?x - Block ?pos - Location))`
    - 2. The task of **placing** a Lego:
    `(:task place
  :parameters (?g - Gripper ?x - Block ?pos - Location))`
    - 3. The task of **shifting** stock from Robot stock to Operator stock:
    `(:task shift
  :parameters (?g_left - Gripper ?g_right - Gripper ?x - Block ?pos - Location))`

---

### Methods

---

- The **Methods** to decompose the tasks so far are:
    - 1. Method to pick-up 2x2 blue block:
        ```
        (:method pick_2x2_Blue
        :parameters (?g - Gripper ?x ?y - Block ?point_air ?pos ?pos_upper ?pos_lower - Location)
        ...
        )
        ```
    - 2. Method to pick-up 2x2 yellow block:
        ```
        (:method pick_2x2_Yellow
        :parameters (?g - Gripper ?x ?y - Block ?point_air ?pos ?pos_upper ?pos_lower - Location)
        ...
        )
        ```
---

### Actions

---

> 1. Empty Gripper Fingers Group of Actions
- 1.1 `Open_gripper ?g`
- 1.2 `Close_gripper ?g`
- 1.3 `Hold_gripper ?block1 ?g ?pos`
- 1.4 `Release_gripper ?block1 ?g`
> 2. Empty Gripper Move Group of Actions
- 2.1 `Move_closed_gripper ?g ?current_point ?destination_point`
- 2.2 `Move_open_gripper_V ?g ?current_point  ?destination_point ?dest_upper ?dest_lower`
- 2.3 `Move_open_gripper_H ?g ?current_point  ?destination_point ?dest_left ?dest_right`
> 3. Gripper Rotation Group of Actions
- 3.1 `Rotate_empty_gripper_H ?g`
- 3.2 `Rotate_empty_gripper_V ?g`
- TBC later ....

> 4. Loaded Gripper Movement Group of Actions
- 4.1 `take_2x2_gripper ?block1 ?g ?pos ?point_air`
- TBC later ...

> 5. Utility Group of Actions
- 5.1 `fill_stock_2x2_blue ?block1 ?pos`
- TBC later ...

---

## Problem 01

---
