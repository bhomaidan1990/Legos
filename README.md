# Legos
> Author: Belal HMEDAN
> LIG labs, Marvin Team
> France, 2021

---

**PreRequests:**

---

The prerequests for this module are:
1. [PDD44J](https://github.com/pellierd/pddl4j/tree/devel) devel branch that contains the [TFD](https://github.com/pellierd/pddl4j/blob/devel/src/main/java/fr/uga/pddl4j/planners/htn/stn/tfd/TFDPlanner.java "TFD Planner") planner.
2. [RWS4Yumi](https://gricad-gitlab.univ-grenoble-alpes.fr/cantalut/rwsclient4yu) API to send the RAPID code to the robot.
3. The following `Python` Libraries:
  3.1 [OpenCV](https://github.com/opencv/opencv-python)
  3.2 [NumPy](https://numpy.org)
  3.3 [Paramiko](http://www.paramiko.org)
  3.4 [PyQt5](https://www.riverbankcomputing.com/software/pyqt)
  3.5 [RWS4YuMi](RWS4YuMi.py)

---

## 1. Perception Module

> This Module handles the vision part mainly.

---

<details>

<summary> See more ... </summary>

### 1.1 imageProcess script

[imageProcessor](imageProcessor.py) script has main class called `imageProcessor`, this class is responsible for:
1. Fisheye rectification.
2. Masking the colors in the HSV space.
3. Morphological closing.
4. Detecting and cropping the ROI (green platform, the workspace, swap zone, and the human stock).
5. Analysing the data in the image.
6. Hand detection$^1$ using YCrCb, and HSV colorspaces.

```
1:
S. Kolkur, D. Kalbande, P. Shimpi, C. Bapat, and J. Jatakia. 
Human skin detection using rgb, hsv and ycbcr color models.  
InProceedings of the International Conference on Communication and Signal Processing 2016 (ICCASP 2016), pages324–332. 
Atlantis Press, 2016/12.
```

### 1.2 yuVision script

[yuVision](yuVision.py) script has two classes:
1. `communicator` class to communicate with the RaspberryPi Module using SSH protocol to read the image.
> Note that the ip address, and host name has to be adjusted according to the used Module.
2. `visionHandler` class to call the image processor script to analyze the world, and detect whether if there is a hand or not, also this class does the comparision between the groundtruth, and the world state to detect any wrong placement.

</details>

---

## 2. Planning Module

> This Module handles the planning part mainly.
> Note that this module calls the [TFD](https://github.com/pellierd/pddl4j/blob/devel/src/main/java/fr/uga/pddl4j/planners/htn/stn/tfd/TFDPlanner.java "TFD Planner") Algorithm from the [PDDL4J](https://github.com/pellierd/pddl4j/tree/devel) library.

---

<details>

<summary> See more ... </summary>



### 2.1 problemHandler script

[problemHandler](problemHandler.py) script has the class `problemHandler` to read the world state, write the state to the problem, and excute the plan task by task, and run the planner to get the plan as a list of actions, this class does the dynamic manipulation of the problem, and the interfacing with the execution module

### 2.2 Domain-Problem model

The [domain](domain.hddl) is static, while the [Problem](problem.hddl) is dynamic, note that the tasks, the actions, and some literals are commented, the `problemHandler` script manages commenting/uncommening some lines to change the problem dynamically according to the world state. This dual is the input of the planner to generate the plan.

</details>

---

## 3. Execution Module

> This Module handles [RAPID](https://library.e.abb.com/public/b227fcd260204c4dbeb8a58f8002fe64/Rapid_instructions.pdf?x-sign=f79v/883X1nHGc8fqH+WAJ2F30y/M6TZfYUuPuQpP+jeMBygouyGg+WSj8A9Otry), and [RWS](https://developercenter.robotstudio.com/api/RWS).
> This Module uses **RWS4Yumi** API to write the RAPID code to YuMi robot.

---

<details>

<summary> See more ... </summary>

### 3.1 yuAction script

[yuAction](yuAction.py) script has the class `actionHandler` which communicates with the ABB IRB 14000 YuMi to get the accurate position, and the status of the cobot, also it does part of the interfacing with the planning module by interpreting the points locations, and the rotation of the gripper, also it does part of interfacing with the HRI controller by extracting the neighbouring positions from the plan.

### 3.2 RAPID code

[RAPID code](currLeft.mod) is used to move the left arm of the cobot, note than the pick/place positions are handeled dynamically.

</details>

---

## 4. GUI Module

> This Module handles the GUI part mainly.

---

<details>

<summary> See more ... </summary>

### 4.1 arucoGUI script

[arucoGUI](arucoGUI.py) script has two classes:
1. `AnimatedLabel` class to provide a blinking labels.
2. `Ui_MainWindow` class, which is the core of this module, this class is the **Graphical User Interface**, and the **HRI-Controller** which is done by mean of [Qt signals](https://wiki.qt.io/Qt_for_Python_Signals_and_Slots).


</details>