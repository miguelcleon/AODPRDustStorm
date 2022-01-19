import csv

import h5py
import numpy as np
import os
import string
import re
from datetime import datetime
# qslat = [18.32129, 18.32131]
# qslon = [-65.81711, -65.81709]
# sabanalat = [18.3249139, 18.3249141]
# sabanalon = [-65.7297631, -65.7297629]
# icacoslat = [18.2754479, 18.27544781]
# icacoslon = [-65.7854971, -65.7854969]
qsandicacoslat = -18.375
qsandicacoslon = -65.875
sabanalat = -18.375
sabanalon = -65.625
# C:/Users/12672/OneDrive - University of New Hampshire/AOD

def extractdatesfromfilename(file):
    #print(file)
    firstyeardate = file.split('-')[2]
    yeardatetime = file.split('-')[3]
    # print(yeardatetime[:4])
    year = yeardatetime[:4]
    date = yeardatetime.split('m')[1][:4]
    # print(date)
    time = yeardatetime.split('t')[1][:6]
    # print(time)
    #print(data)
    dt = datetime(int(year), int(date[:2]), int(date[2:4]), int(time[:2]), int(time[2:4]))
    # print(dt)
    #print(firstyeardate)
    year = firstyeardate[8:12]
    # print(year)
    month = firstyeardate[13:15]
    day = firstyeardate[15:17]
    # print(month)
    # print(day)
    firstdt = datetime(int(year), int(month), int(day))
    # print(firstdt)
    return firstdt, dt

def writedata(csvout, datasite,file,i, lat, lon,site):
    i+=1
    # print(i)
    firstdt, dt = extractdatesfromfilename(file)
    # print(firstdt)
    # print(dt)
    nanvals = {}
    nanvals['UVAerosolIndex'] = [-1.2676506e+30,-1.2676507e+30]
    nanvals['VISAerosolIndex'] = [-1.2676506e+30,-1.2676507e+30]
    nanvals['AerosolModelMW'] = [65535,65536]
    nanvals['AerosolOpticalThicknessPassedThresholdMean'] = [-32767, -32768]
    nanvals['AerosolOpticalThicknessMW'] = [-32767, -32768]
    nanvals['AerosolOpticalThicknessPassedThresholdStd'] = [-32767, -32768]
    nanvals['SingleScatteringAlbedoMW'] = [-32767, -32768]
    nanvals['SingleScatteringAlbedoPassedThresholdMean'] = [-32767, -32768]
    nanvals['SingleScatteringAlbedoPassedThresholdStd'] = [-32767, -32768]
    nanvals['SolarZenithAngle'] = [-1.2676506e+30,-1.2676507e+30]
    nanvals['TerrainReflectivity'] = [-32767, -32768]
    nanvals['ViewingZenithAngle'] = [-1.2676506e+30,-1.2676507e+30]
    nanvals['AerosolOpticalThicknessMW'] = [-32767,-32768]
    nanvals['SingleScatteringAlbedoMW'] = [-32767,-32768]
    #handle missing values change them to nan
    for key, val in datasite.items():
        for nankey, nanval in nanvals.items():

            if nankey in key and (val[0] == -1.2676506e+30 or (str(val[0]) == str(nanval[0]) or str(val[0]) == str(nanval[1]))):
                #print(key)
                #print(val[0])
                datasite[key] = [np.NAN]
    if i==1:
        row = ['site name','AOD Latitude', 'AOD Longitude', 'firstdate', 'datetime']
        # csvout.writerow(row)
        #  outfile.write('\r\n')
    else:
        row = [datasite['site'], str(lat), str(lon), str(firstdt), str(dt)]
    for key, val in datasite.items():
        if i==1 and not key == 'site':
            row.append(key)
        elif not key =='site':
            row.append(val[0])

    # print(row)
    csvout.writerow(row)
    # outfile.write('\r\n')
    return i
dirs = ['./2017', './2018','./2019','./2020']
i=0
with open('AODout.csv', 'w', newline='') as outfile:
    csvout = csv.writer(outfile)
    for dir in dirs:
        for file in os.listdir(dir):
            hdffile = file
            if file.endswith('.he5'):
                #print(file)
                # hdffile = './2017/OMI-Aura_L3-OMAEROe_2017m0101_v003-2017m0106t110227.he5'
                aodfile = h5py.File(dir + '/' + hdffile, mode='r')
                # print(list(aodfile['/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/'].keys()))

                hdf5lat = aodfile['/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/Latitude'][:] #
                hdf5lon = aodfile['/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/Longitude'][:] #
                # lat_index = np.logical_and(hdf5lat > qslat[0], hdf5lat < qslat[1])
                # lon_index = np.logical_and(hdf5lon > qslon[0], hdf5lon < qslon[1])
                qsbox_index = np.logical_and(qsandicacoslat == hdf5lat, qsandicacoslon == hdf5lon)
                sbbox_index = np.logical_and(sabanalat == hdf5lat, sabanalon == hdf5lon)
                # lon_index = np.logical_and(qslon[0] < hdf5lon, qslon[1] >  hdf5lon)
                # box_index = np.logical_and(lat_index, lon_index)
                hdf5fields = ['AerosolOpticalThicknessPassedThresholdMean','AerosolModelMW',
                              'UVAerosolIndex','VISAerosolIndex', 'AerosolOpticalThicknessPassedThresholdStd',
                              'SolarZenithAngle', 'TerrainReflectivity', 'ViewingZenithAngle',
                              'SingleScatteringAlbedoPassedThresholdMean', 'SingleScatteringAlbedoPassedThresholdStd']
                hdf5multifields = ['AerosolOpticalThicknessMW', 'SingleScatteringAlbedoMW' ]
                hdf5path = '/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/'
                site= 'QS  and Icacos'
                datasite = {} # [site, data, mwdata]
                datasite['site'] = site
                site= 'Sabana'
                sabdata = {}
                sabdata['site'] = site
                for field in hdf5fields:
                    curfield = hdf5path + field
                    data = aodfile[curfield][qsbox_index]
                    sbdata = aodfile[curfield][sbbox_index]
                    datasite[field] = data
                    sabdata[field] = sbdata
                for field in hdf5multifields:
                    for j in range(0,5):
                        curfield = hdf5path + field
                        data = aodfile[curfield][j][qsbox_index]
                        sbdata = aodfile[curfield][j][sbbox_index]
                        datasite[field + str(j)] = data
                        sabdata[field + str(j)] = sbdata
                #print(len(aodfile[hdf5path][:]))

                #print(i)
                i = writedata(csvout, datasite,file,i, qsandicacoslat, qsandicacoslon,site)

                i = writedata(csvout, sabdata,file,i, sabanalat, sabanalon,site)