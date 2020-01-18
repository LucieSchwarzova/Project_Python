# sCRAP 
Project for Data Python IES
 

The aim of this project was to collect data on consumer goods prices at various online retailers to prepare a dataset for further analysis of their pricing habits and mainly for a possible detection of some coordination among the retailers.

The project as you can see it today does not yet contain a ready-to-use panel dataset for the analysis, but only because I did not manage to get in touch with you timely to discuss how to run in outside of my computer.
Moreover, the number of covered retailers is not overhalming. Currently, nomen omen sCRAP supports exclusively CZC.CZ and DATART.CZ (datart is more over not 100% debuged - the perfomance could be better) ...

Despite the mentioned space for improvement, I believe that the project still meets your requirements. 


1. Open the "Meet the robot" pdf file and see what is the idea behind our project
https://github.com/LucieSchwarzova/Project_Python/blob/master/Meet%20he%20robot!.pdf


2. Try it yourself in the user's notebook
https://github.com/LucieSchwarzova/Project_Python/blob/master/sCRAPs%20user%20interface.ipynb

3. Have a closer look on how it works (or doesn't work) in the actual code 
https://github.com/LucieSchwarzova/Project_Python/blob/master/sCRAP_the_robot.py





##### Out proposal:

The aim of out project is to build a program that scrapes data on retail prices from selected sources (czc.cz is confirmed to be feasible, other sources are being discussed) and saves it in pre-selected time intervals as a .csv file. Further, we will process the the collected data to transform it from a series of cross-sections into a panel / time series and prepare it for further analysis. 
We already have a robot to scrape all goods and prices from a given category in CZC CZ (see attached notebook) The task now is to teach it to scan across categories, save the data in files with systematic names and maily, to ge time-triggered. 
The output of this project should be, next to the precious code, also a unique dataset that can serve us (or someone else) to study the pricing strategies used by retailers in the peak season of their business.



