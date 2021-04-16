# Legos
> author: Belal HMEDAN

---

## 1. Perception Module

> This Module handles the vision part mainly.

---

### imageProcess script

[This](imageProcessor.py) script has main class called `imageProcessor`.
This class is responsible for:
1. fisheye undistortion.
2. masking the colors in the HSV space.
3. Morphological closing.
4. detecting and cropping the green platform, the workspace, swap zone, and the human stock.
5. analysing the data in the image.
6. hand detection using YCrCb, and HSV colorspace

```
@inproceedings{Kolkur2016/12,
  title={Human Skin Detection Using RGB, HSV and YCbCr Color Models},
  author={S. Kolkur and D. Kalbande and P. Shimpi and C. Bapat and J. Jatakia},
  year={2016/12},
  booktitle={Proceedings of the International Conference on Communication and Signal Processing 2016 (ICCASP 2016)},
  pages={324-332},
  issn={1951-6851},
  isbn={978-94-6252-305-0},
  url={https://doi.org/10.2991/iccasp-16.2017.51},
  doi={https://doi.org/10.2991/iccasp-16.2017.51},
  publisher={Atlantis Press}
}
```

### yuVision script

[This](yuVision.py) script has two classes:
1. `communicator` class to communicate with the RaspberryPi Module, read image, writes control data, and runs scripts on the module.
> Note that the ip address, and host name has to be adjusted according to the used Module.
2. `visionHandler` class to call the image processor script to analyse the world, and detect whether if there is a hand or not!

### problemHandler script

[This](problemHandler.py) script has the class `problemHandler` to read the world state, write the state to the problem, and excute the plan task by task, and run the planner to get the plan as a list of actions.

---

## 2. Planning Module

> This Module handles the planning part mainly.

---

in this context we have the [domain](domain.hddl), and the [problem](problem.hddl), note that the tasks, the actions, and some literals are commented, the `problemHandler` script manages commenting/uncommening some lines to change the problem dynamically according to the world state.

---

## 3. GUI Module

> This Module handles the GUI part mainly.

---

---

## 4. Action Module

> This Module handles the RAPID part mainly.

---
