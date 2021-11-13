from itertools import combinations
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Sub-basin
#0- Dashte Abbas (DA) 19024  ha
#1- Dosalegh (DO) 17140
#2- Arayez (AR) 24000
#3- Hamidiyeh(HA) 18388
#4- Azadegan(AZ) 60000
#Total=138552 ha

#Mandatory
month_day=[31,28,31,30,31,30,31,31,30,31,30,31]

def agr(area,crop_type,di):

#Crops Index                   Month
# 0- Winter Wheat              Jan
# 1- Barley                    Feb
# 2- Maize                     Mar
# 3- Beans                     Apr
# 4- Cucumbers                 may
# 5- Tomatoes                  Jun
# 6- Watermelons               July
# 7- Alfalfa                   Agu
# 8- Sorghum                   Sep
# 9- Rapeseed                  Oct
# 10-                          Nov
# 11-                          Dec

    name=['Winter Wheat','Barley', 'Maize', 'Beans','Cucumbers','Tomatoes','Watermelons','Alfalfa','Sorghum','Rapeseed']
    month_day=[31,28,31,30,31,30,31,31,30,31,30,31]
    k_c_y=[[0.2,0.6,0.5,0.4],
           [0.2,0.6,0.5,0.4],
           [0.4,1.5,0.5,0.2],
           [0.2,1.1,0.75,0.2],
           [0.84,0.84,0.84], #
           [0.4,1.1,0.8,0.4],
           [0.45,0.7,0.8,0.8],#
           [1.1,1.1],
           [0.2,0.55,0.45,0.20],
           [0.87,0.87,0.87]]
    
    months=[0,0,0,0,0,0,0,0,0,0,0,0]
    month_day=[31,28,31,30,31,30,31,31,30,31,30,31]
    total_water_per_crop=[0]
    plott=[1,2,3,4,5,6,7,8,9,10,11,12]
    y_c_a=[0,0,0,0,0,0,0,0,0,0]
    price=[40000,23798,24650,68694.3,20692,16680.3,8859.9,25833,20011.5,28298.7] #Rial/kg
    income=[0,0,0,0,0,0,0,0,0,0]
    net_benefit=[0,0,0,0,0,0,0,0,0,0]
    #k_c_y=[1.05,1.1,1.25,1.15,0.84,1.05,1.1,0.9,0.9,0.87]
    y_c_max=[7,4.7,10,12,25,35,40,3.5,8,4] #ton/ha
    crop_factor=[[0.6,1.2,0.75,0.25], # Kc
    [0.8,1.0,1.05,0.4],
    [0.7,1.2,1.15,1.1],
    [0.6,1.2,0.75,0.3],
    [0.5,1.0,0.80], #
    [0.65,1.25,0.95,0.65],
    [0.65,1.05,0.9,0.75],#
    [0.4,1.2],
    [0.575,1.15,0.8 ,0.55], 
    [0.35,1.15,0.35]] 
    w_c_p=9 #mm/day 9
    
    w_c_a=[di*i*w_c_p for i in crop_factor[crop_type]]
    

    # Cost  Rial/ha 
    cost=[26891710,19710930,45460320,50058840,76835360,93581210,66868420,32469710,48214420,25928570]

    # w_c_a_l=list()
    # for i in range(len(k_c_y)):
    #     n=len(k_c_y[i])
    #     w_c_a_l.append(w_c_a[:n])
    #     w_c_a=w_c_a[n:]
    # w_c_a=w_c_a_l
    
    
    r=list()
    tmp=list()
    
    for j in range(len(k_c_y[crop_type])):
        tmp.append(k_c_y[crop_type][j]*(1-(w_c_a[j]/(crop_factor[crop_type][j]*w_c_p))))
    r.append(tmp)

    result=list(map(sum, r))
    
    
    y_c_a=y_c_max[crop_type]*(1-result[0])
    income=y_c_a*area*price[crop_type]*1000  #for each crop 1000 is to convert ton to kg
    net_benefit=income-cost[crop_type]*area
   

    eff=0.464 #irrigation efficiency for each subbasin
    
   
    #total_water_per_months = [element/eff for element in months] 
    total_water_per_crop=[element/eff for element in total_water_per_crop]


    return [y_c_a,income,net_benefit]
   
  
    

def gini(ratio):
    diff=0
    gini_coef=[]
    for k in range(10): #10 YEARS
        r=ratio[k]
        for i in r:
            for j in r:
                diff+=abs(i-j)
        gini_coef.append((1/(2*len(r)*sum(r)))*diff)
    return[gini_coef] # it returns 10 values which is the 10 Gini coeff. of 10 years 



def GWP(total_water_per_crop,area,sub):     #area (ha)  water(M^3)
    
    
    GWP_fertilizer=[0,0,0,0,0,0,0,0,0,0]
    GWP_biocide=[0,0,0,0,0,0,0,0,0,0]
    GWP_machinery=[0,0,0,0,0,0,0,0,0,0]
    GWP_fuel=[0,0,0,0,0,0,0,0,0,0]
    GWP_electricity=[0,0,0,0,0,0,0,0,0,0]
    GWP_total=[0,0,0,0,0,0,0,0,0,0]

    manure=[0,0,0,0,3500,3400,2800,2200,1000,0]                                       #kg/ha
    phosphorus=[89.96,18.72,136.66,93.33,125.54,86.45,109.77,198.57,91.14,73.65]      #P2O5 
    nitrogen =[200.06,102.87,246.85,186.66,210.06,177.23,201.76,13.56,393.59,232.62]
    potassium=[29.99,17.32,39,0,72.99,43.22,59.01,14.28,11.47,20.94]                  #K2O
    herbicide=[630,230,660,0,1200,1190,1280,160,2560,2570]
    insecticide=[100,10,0,0,880,1040,1020,120,480,630]
    fungicide=[10,0,30,0,1030,900,700,50,0,120]
    labor=[3.67,5.46,6.14,8.62,34.53,28.05,13.79,11.31,4.48,2.65]                     #person perday per hectare
    machinery_hour=[18.5,18.5,19,16,22.5,22.5,22.5,19,19,0,16]                        #h  17.81 lit/h fuel   93.38 hp  1 hp*h=2.6845 MJ  2.3477
                                                                                      # electricity 0.2323 Kwh/m^3   

    if sub==0:
        area = [element * 19024 for element in area]
    elif sub==1:
        area = [element * 17140 for element in area]
    elif sub==2:
        area = [element * 24000 for element in area]
    elif sub==3:
        area = [element * 18388 for element in area]
    elif sub==4:
        area = [element * 60000 for element in area]

    for i in range(10):
        GWP_fertilizer[i]=(manure[i]*8.96384+phosphorus[i]*1.5+potassium[i]*0.98+nitrogen[i]*8.3)*area[i]
        GWP_biocide[i]=(herbicide[i]*6.3+insecticide[i]*5.1+fungicide[i]*3.9)*area[i]
        GWP_machinery[i]=93.38*machinery_hour[i]*2.6845*0.071*area[i]
        GWP_fuel[i]=machinery_hour[i]*17.81*2.347*area[i]
        GWP_electricity[i]=total_water_per_crop[i]*10*0.2323*0.608
        GWP_total[i]=GWP_fertilizer[i]+ GWP_biocide[i]+GWP_machinery[i]+GWP_fuel[i]+GWP_electricity[i]
    return GWP_total

