## Simulation Of Container Bay Stacking Algorithms

Author: [Peiwen Lei](mailto:peiwen.lei@hotmail.com)

#### Introduction

This program is developed for the bachelor thesis `Überblick und Analyse quantitativer 
Yard-Strategie-Modelle von Container-Terminals` from `Peiwen Lei` under the supervise of `Prof. Dr. Leif Meier` from `Hochschule Bremerhaven`.

This program simulates the process of the loading of containers into a container bay and then retrieving them out of the bay. 
It calculates the KPI `Extra Movements` when putting containers into the bay, and the KPI `Rehandling` when retrieving containers from the bay.

Simulations of the following container stacking algorithms are included in the program:
- Hybrid Sequence Stacking Algorithm (`HSSA`)
- Vertical Stacking Algorithm (`VSA`)
- Random Stacking Algorithm (`RSA`)
- Hybrid Sequence Left Stacking  Algorithm  (`HSLSA`, one variation of `HSSA`)
- Hybrid Sequence Right Stacking Algorithm (`HSRSA`, one variation of `HSSA`)

#### Getting Started

This program requires `Python > 3.7.1` and `pip`. Please make sure you have both installed before starting the following steps.

1. Install dependencies. This program depends on the Python libraries `pandas` and `seaborn`:
    ```bash
    pip install pandas seaborn
    ```

2. Generate simulation data. In the beginning of the script `generate_data.py` you can specify
the width and height of the simulated bay, as well as the number of simulation iterations.
Once you have modified the number to your requirements, then yo can run the following to generate the simulated data:
    ```bash
    python generate_data.py
    ```
   After this, your data will be put into a sub-folder in the `data` directory. The name of the sub-folder is constructed as followed: `w{width}_h{height}_s{number of iteration}`.

3. Show results of `HSSA`, `VSA` and `RSA`. In the beginning of the sript `show_dist.py`, you can define from which sub-folder in `data` directory the data should be read. 
Once you have set this parameter, run the following command to show the data distribution among the algorithms:
    ```bash
    python show_dist.py
    ```
   
4. Show the change of distribution with different width and height of the simulated bay. In the beginning of the sript `show_trend.py`, you can define from which sub-folders in `data` directory the data should be read. 
Once you have set this parameter, run the following command to show the change with different bay dimensions:
    ```bash
    python show_trend.py
    ```