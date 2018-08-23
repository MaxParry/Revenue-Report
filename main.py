import os
import csv
import operator

print('Welcome to the Financial Record Analyzer')

filenum = int(input('How many files would you like to analyze? > '))

# Earliest year is 2009, latest is 2016
# Map two date formats, xx and xxxx to xxxx for compilation
datedict = {'09':'2009',
            '10':'2010',
            '11':'2011',
            '12':'2012',
            '13':'2013',
            '14':'2014',
            '15':'2015',
            '16':'2016',
            '17':'2017',
            '18':'2018',
            '19':'2019',
            '20':'2020',
            '2009':'2009',
            '2010':'2010',
            '2011':'2011',
            '2012':'2012',
            '2013':'2013',
            '2014':'2014',
            '2015':'2015',
            '2016':'2016',
            '2017':'2017',
            '2018':'2018',
            '2019':'2019',
            '2020':'2020'}

#input_data/budget_data_1.csv
#input_data/budget_data_2.csv

directories = []

for i in range(1, filenum + 1):
    dirpath = input('Please enter filepath of source: > ')
    directories.append(dirpath)

array = []

for i in range(0, filenum):
    pathlist = directories[i].split('/')
    path = os.path.join(*pathlist)
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rawdate = row[0]
            if rawdate == 'Date' or rawdate == 'date':
                pass
            else:
                parselist = rawdate.split('-')
                yearlookup = parselist[-1]
                year = datedict[yearlookup]
                month = parselist[0]
                revenue = row[1]
                prelist = [year, month, int(revenue)]
                array.append(prelist)

yeardict = {'2009':1,
            '2010':2,
            '2011':3,
            '2012':4,
            '2013':5,
            '2014':6,
            '2015':7,
            '2016':8,
            '2017':9,
            '2018':10,
            '2019':11,
            '2020':12}

monthdict = {'Jan':1,
             'Feb':2,
             'Mar':3,
             'Apr':4,
             'May':5,
             'Jun':6,
             'Jul':7,
             'Aug':8,
             'Sep':9,
             'Oct':10,
             'Nov':11,
             'Dec':12}

for i in array:
    i[0] = yeardict[i[0]]
    i[1] = monthdict[i[1]]

array = sorted(array, key=operator.itemgetter(0,1))

for i in array:
    for v, k in yeardict.items():
        if i[0] == k:
            i[0] = v
    for v, k in monthdict.items():
        if i[1] == k:
            i[1] = v

# array has been decoded to ordinal, sorted, and re-encoded
# now we can iterate over sorted array to summate doubles

finalarray = []
thatyear = ''
thatmonth = ''
thatrev = 0


for i in array:
    if i[0] != thatyear or i[1] != thatmonth:
        finalarray.append(i)
    elif i[0] == thatyear and i[1] == thatmonth:
        newrev = i[2] + thatrev
        i[2] = newrev
        finalarray[-1] = i
    else:
        print("Base case reached in summation step")
    thatyear = i[0]
    thatmonth = i[1]
    thatrev = i[2]

# calculating total months:

monthcount = 0
firsttime = 0
revenue = 0
topdog = 0
topmonth = ''
topyear = ''
underdog = 1000000000
undermonth = ''
underyear = ''
lastrev = 0
chgtot = 0

for i in finalarray:
    revenue = revenue + i[2]
    chgtot = chgtot + (i[2] - lastrev)
    if i[2] - lastrev > topdog:
        topdog = i[2] - lastrev
        topmonth = i[1]
        topyear = i[0]
    else:
        pass
    if i[2] - lastrev < underdog:
        underdog = i[2] - lastrev
        undermonth = i[1]
        underyear = i[0]
    else:
        pass
    if firsttime == 0:
        month = i[1]
        monthcount = 1
        firsttime = 1
    else:
        if i[1] == month:
            pass
        else:
            monthcount = monthcount + 1
            month = i[1]
    lastrev = i[2]

print('Financial Analysis')
print('-' * 30)
print('Total Months: ', monthcount)
print('Total Revenue: $', revenue)
print('Average Revenue Change: $', int((chgtot / (monthcount - 1))))
print('Greatest Increase in Revenue: ', topyear, topmonth, '($', topdog, ')')
print('Greatest Decrease in Revenue: ', underyear, undermonth, '($', underdog, ')')

outputpath = os.path.join('output_analysis', 'financial_report.txt')

with open(outputpath, 'w', newline='') as textfile:
    textfile.write('Financial Analysis')
    textfile.write('\n')    
    textfile.write('-' * 30)
    textfile.write('\n')
    textfile.write('Total Months: ' + str(monthcount))
    textfile.write('\n')
    textfile.write('Total Revenue: $' + str(revenue))
    textfile.write('\n')
    textfile.write('Average Revenue Change: $' + str(int((chgtot / (monthcount - 1)))))
    textfile.write('\n')
    textfile.write('Greatest Increase in Revenue: ' + str(topyear) + '-' + str(topmonth) + '($' + str(topdog) + ')')
    textfile.write('\n')
    textfile.write('Greatest Decrease in Revenue: ' + str(underyear) + '-' + str(undermonth) + '($' + str(underdog) + ')')