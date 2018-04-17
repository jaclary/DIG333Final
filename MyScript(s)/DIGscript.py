import time, math, random
import matplotlib.pyplot as plt
import spidev


#####Function that Adjusts the X-axis values to relfect time objects#####

def xCreation(xList =[], *args):
    for i in range(100):
        xList.append(1)
    return xList


#####Function that Adjusts the Y-axis values to reflect correct Gaseous Values#####

def yCreation(yList=[], *args):
    for i in range(100):
        yList.append(3)
    return yList


def main():
    #spidev
    spi = spidev.SpiDev()
    #list declaration
    xList =[]
    yList =[]
    #list manipulation
    try:
        finalXList = xCreation(xList)
        finalYList = yCreation(yList)
    except:
        print("x or y creation not operational")
    try:
        plt.plot(finalXList, finalYList)
        plt.ylabel("Gas-axis")
        plt.xlabel("Time-axis")
        plt.show(block=True)
    except:
        print("matplotlib not operating correctly")

main()
