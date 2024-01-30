from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import scipy


# function to read from the sample.mat file
# input:the path of the file
# output return the array of all the sample x and the time array
# data = loadmat(r"C:\Users\I-SEVEN\PycharmProjects\pythonProject\Sample_Process_2022.mat")


def readFromTheMatFile():
    path = filenameE.get()
    data = loadmat(path)
    return data["X"], data["t"]


# function to plot the user entered numbered of samples with time


def plotSamples():
    numberRequired = int(samplesPlotingE.get())
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    x = np.random.randint(0, len(samples), size=(numberRequired))
    sample = []
    for i in x:
        sample.append(samples[i])
    plt.figure()
    fig, axs = plt.subplots(numberRequired)
    fig.suptitle('samples plots')
    for i in range(numberRequired):
        axs[i].plot(time[0], sample[i])
    plt.show()


def calcEnsampleMean():
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    ensampleMeanFinal = np.mean(samples, axis=0)
    plt.figure()
    plt.plot(time[0], ensampleMeanFinal)
    plt.title(" the ensample mean")
    plt.xlabel(" the time ")
    plt.ylabel(" the mean ")
    plt.show()


def calcAutoColeration(i, j):
    print(i,j)
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    temp = []
    autoColeration = 0
    if int(i) < len(samples[0]) and int(j) < len(samples[0]):
        print(i,j)
        row1, row2 = samples[int(i)], samples[int(j)]
        print(row1,row2)
        tuo = abs(row1 - row2)
        for it in range(len(row1)):
            temp.append(row1[it] * row2[it] * (1 / len(samples)))
        autoColeration = round(sum(temp), 4)
        print(autoColeration)
    return autoColeration


# to calculate the time mean for specific sample we sum the whole sample and divide by its length
# the user will be asked to enter the required sample number and the function will return its time mean

def timeMean(i):
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    sample = samples[int(i)]
    timemean = sum(sample) / len(sample)
    return timemean


# the user will be asked to enter two samples numbers i and j the function will multiple each corresponding columns
# and the probability of the row then will sum their values and return it and the tou for the future calculation


def threeD_ACF():
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    acf = []
    for i in range(len(samples)):
        temp = []
        for j in range(len(samples)):
            temp.append(calcAutoColeration(i, j))
        acf.append(temp)

    return acf


# function to calculate the time acf for the user chosed sample by evaluating each
def timeACF(n, tou):
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    sample = samples[n]
    dt = time[0][1] - time[0][0]
    temp = []
    for i in range(len(sample)):
        if i + tou < len(sample):
            temp.append(sample[i] * sample[i + tou] * dt)
    return round(sum(temp)/(time[0][-1]-time[0][0]), 3)


def timeACfforalltoues(n):
    time = readFromTheMatFile()[1]
    samples = readFromTheMatFile()[0]
    timp = []
    tou = []
    for i in range(len(time[0])):
        tou.append(i)
        timp.append(timeACF(n, i))
    plt.figure()
    plt.plot(tou, timp)
    plt.title("the ACF for sample "+str(n))
    plt.xlabel("the time difference  ")
    plt.ylabel("the ACF value   ")
    plt.show()
    return timp

def plot_timeacfforalltous():
    n=timemeanE.get()
    timeACfforalltoues(int(n))

def dsp():
    time = readFromTheMatFile()[1]
    timeini = time[0][0]
    timefin = time[0][-1]
    samples = readFromTheMatFile()[0]
    temp = []
    for i in samples:
        f = np.fft.fft(i)
        shift = np.fft.fftshift(f)
        abs = np.abs(shift)
        temp.append(abs)
    stemp = np.square(temp) * (1 / len(samples))
    average = np.mean(stemp, axis=0)
    dsp = average / (timefin - timeini)
    plt.figure()
    plt.plot(dsp)
    plt.title("the power spectrum density ")
    plt.show()


def total_average_power():
    samples = readFromTheMatFile()[0]
    temp = []
    for i in range(len(samples)):
        value = calcAutoColeration(i, i)
        temp.append(value)
    final = round(sum(temp), 3)
    return final


# #######################################################################################################################
def acfploting():
    i = acfplotingEi.get()
    j = acfplotingEj.get()
    value = calcAutoColeration(i, j)
    acflable = tk.Label(window, text="the acf = " + str(value))
    acflable.grid(column=2, row=4)


def printTimemenn():
    n = timemeanE.get()
    value = round(timeMean(n), 3)
    timemean = tk.Label(window, text="the time mean  = " + str(value))
    timemean.grid(column=2, row=10)


def timeacf():
    n = timemeanE.get()
    value = round(timeACF(int(n), 5), 3)
    timemean = tk.Label(window, text=" for tou = 5 is " + str(value))
    timemean.grid(column=2, row=11)


def threeDploting():
    samples = readFromTheMatFile()[0]
    x = np.arange(0, len(samples), 1)
    acf = threeD_ACF()
    array = np.array(acf)
    x2, y = np.meshgrid(x, x)
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x2, y, array)
    plt.show()


def printtotalaverage():
    value = total_average_power()
    timemean = tk.Label(window, text=" total average power = " + str(value))
    timemean.grid(column=1, row=15)


# ########################################################################################################################
window = tk.Tk()
window.geometry("600x600")
filenameL = tk.Label(window, text="enter the path of the file ")
filenameL.grid(column=0, row=0, pady=10)
filenameE = tk.Entry(window)
filenameE.grid(column=1, row=0, pady=10)
filenameB = tk.Button(window, text="Enter ", command=readFromTheMatFile, width=17)
filenameB.grid(column=2, row=0, pady=10, padx=10)
# for the samples ploting
samplesPlotingL = tk.Label(window, text="enter the number of sample")
samplesPlotingL.grid(column=0, row=1)
samplesPlotingE = tk.Entry(window)
samplesPlotingE.grid(column=1, row=1)
samplesPlotingB = tk.Button(window, text="Enter to show the plots ", command=plotSamples)
samplesPlotingB.grid(column=2, row=1, padx=10)
# mean ploting
meanplotingL = tk.Label(window, text="enter to plot the mean ")
meanplotingL.grid(column=0, row=2)
meanplotingB = tk.Button(window, text="Enter", command=calcEnsampleMean, width=17)
meanplotingB.grid(column=1, row=2, pady=10)
# separator

# auto coluration calculation
sign1 = tk.Label(window, text="    For The Auto Coluration Function    ", bg="black", width=30, fg="white")
sign1.grid(column=1, row=3, pady=10)
acfplotingLi = tk.Label(window, text=" enter the first colum ")
acfplotingLi.grid(column=0, row=4)
acfplotingEi = tk.Entry(window)
acfplotingEi.grid(column=1, row=4)
acfplotingLj = tk.Label(window, text="enter the second colum ")
acfplotingLj.grid(column=0, row=5)
acfplotingEj = tk.Entry(window)
acfplotingEj.grid(column=1, row=5)
acfplotingBj = tk.Button(window, text="Enter to show the value  ", command=acfploting, width=30)
acfplotingBj.grid(column=1, row=6, pady=10)
threed = tk.Button(window, text="Enter to plot the three D plotting  of ACF", command=threeDploting)
threed.grid(column=1, row=7, pady=2)
# separate
sign2 = tk.Label(window, text="    For The time           ", bg="black", width=35, fg="white")
sign2.grid(column=1, row=8, pady=15)
# print time mean
timemeanL = tk.Label(window, text=" enter the number of the sample  ")
timemeanL.grid(column=0, row=9)
timemeanE = tk.Entry(window)
timemeanE.grid(column=1, row=9)
timemeanB = tk.Button(window, text="Enter to print time mean ", command=printTimemenn)
timemeanB.grid(column=1, row=10, pady=10)
# print the acf mean
acfmeanB = tk.Button(window, text="Enter to ptint acf mean  ", command=timeacf, width=20)
acfmeanB.grid(column=1, row=11)
alltous = tk.Button(window, text="Enter to plot ACF  ", command=plot_timeacfforalltous, width=20)
alltous.grid(column=1, row=12)
# for the power spectrogram density
sign3 = tk.Label(window, text="    For The power        ", bg="black", width=35, fg="white")
sign3.grid(column=1, row=13, pady=10)
totalaverageB = tk.Button(window, text="Enter to rint the total average power", command=printtotalaverage)
totalaverageB.grid(column=1, row=14, pady=2)
powerplot = tk.Button(window, text="Enter to plot power spectral density ", command=dsp)
powerplot.grid(column=1, row=17, pady=2)
window.mainloop()

# data = loadmat(r"C:\Users\I-SEVEN\PycharmProjects\pythonProject\Sample_Process_2022.mat")
