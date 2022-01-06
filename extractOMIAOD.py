import csv

import h5py
import numpy as np
import os
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
    print(file)
    firstyeardate = file.split('-')[2]
    yeardatetime = file.split('-')[3]
    # print(yeardatetime[:4])
    year = yeardatetime[:4]
    date = yeardatetime.split('m')[1][:4]
    # print(date)
    time = yeardatetime.split('t')[1][:6]
    # print(time)
    print(data)
    dt = datetime(int(year), int(date[:2]), int(date[2:4]), int(time[:2]), int(time[2:4]))
    # print(dt)
    print(firstyeardate)
    year = firstyeardate[8:12]
    print(year)
    month = firstyeardate[13:15]
    day = firstyeardate[15:17]
    print(month)
    print(day)
    firstdt = datetime(int(year), int(month), int(day))
    # print(firstdt)
    return firstdt, dt

def writedata(csvout, datasite,file,i, lat, lon,site):
    if (len(datasite['AerosolOpticalThicknessPassedThresholdMean'])> 0 \
            and not datasite['AerosolOpticalThicknessPassedThresholdMean'] ==-32767) or \
            (len(datasite['AerosolModelMW'])> 0 \
         and not datasite['AerosolModelMW'] ==65535) or \
            (len(datasite['UVAerosolIndex'])> 0 \
         and not datasite['UVAerosolIndex'] ==-1.2676506E+30):
        i+=1
        print(i)
        firstdt, dt = extractdatesfromfilename(file)
        print(firstdt)
        print(dt)
        #handle missing values change them to nan
        if datasite['UVAerosolIndex'][0]  == -1.2676506E+30:
            datasite['UVAerosolIndex'] = [np.NAN]
        if datasite['AerosolModelMW'] ==65535:
            datasite['AerosolModelMW'] = [np.NAN]
        if datasite['AerosolOpticalThicknessPassedThresholdMean'] ==-32767:
            datasite['AerosolOpticalThicknessPassedThresholdMean'] = [np.NAN]
        if i==1:
            row = ['site name','AOD Latitude', 'AOD Longitude', 'firstdate', 'datetime',
                   'AerosolOpticalThicknessPassedThresholdMean',  'AerosolModelMW' , 'UVAerosolIndex']
            csvout.writerow(row)
            #  outfile.write('\r\n')
        row = [datasite['site'],str(lat), str(lon),str(firstdt),
               str(dt), str(datasite['AerosolOpticalThicknessPassedThresholdMean'][0]),
               str(datasite['AerosolModelMW'][0]),
               str(datasite['UVAerosolIndex'][0])]
        print(row)
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
                hdf5path = '/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/AerosolOpticalThicknessPassedThresholdMean'
                #print(len(aodfile[hdf5path][:]))
                data = aodfile[hdf5path][qsbox_index]
                sbdata = aodfile[hdf5path][sbbox_index]
                hdf5pathMW = '/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/AerosolModelMW'
                # print(len(aodfile[hdf5pathMW][:]))
                mwdata = aodfile[hdf5pathMW][qsbox_index]
                mwsbdata = aodfile[hdf5pathMW][sbbox_index]
                hdf5pathUVAI= '/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/UVAerosolIndex'
                mwUVAIdata = aodfile[hdf5pathUVAI][qsbox_index]
                mwUVAIbdata = aodfile[hdf5pathUVAI][sbbox_index]
                site= 'QS  and Icacos'
                datasite = {} # [site, data, mwdata]
                datasite['site'] = site
                datasite['AerosolOpticalThicknessPassedThresholdMean'] = data
                datasite['AerosolModelMW'] = mwdata
                datasite['UVAerosolIndex'] = mwUVAIdata
                #print(i)
                i = writedata(csvout, datasite,file,i, qsandicacoslat, qsandicacoslon,site)
                site= 'Sabana'
                datasite['site'] = site
                datasite['AerosolOpticalThicknessPassedThresholdMean'] = sbdata
                datasite['AerosolModelMW'] = mwsbdata
                datasite['UVAerosolIndex'] = mwUVAIbdata
                i = writedata(csvout, datasite,file,i, sabanalat, sabanalon,site)
