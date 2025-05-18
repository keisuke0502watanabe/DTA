import Keigetpv
import Chino
import time
import setScanrate
import threading
import csv
import os
import vttotemp




print("You will start to setup DTA. If you have CSV file of experiment condition,you can start the experiment by loading the file.if not,you can start by anwsering the following questions")
Q1 = input("Do you have the CSV file? y/n:")
if Q1 == 'y':
    import Q1Yes
elif Q1 == 'n':
    import Q1No