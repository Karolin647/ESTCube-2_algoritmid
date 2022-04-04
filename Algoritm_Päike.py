import ephem
import datetime
from ephem import *
from datetime import *
import math
import pymap3d as pm
import numpy as np

#https://stackoverflow.com/questions/56420909/calculating-the-radius-of-earth-by-latitude-in-python-replicating-a-formula
def raadius (B): #Maa raadiuse arvutused, B on päikese laiuskraad
    a = 6378.137  #Raadius ekvaatoril mere kõrgusel
    b = 6356.752  #Raadius poolustel
    c = (a**2*math.cos(B))**2
    d = (b**2*math.sin(B))**2
    e = (a*math.cos(B))**2
    f = (b*math.sin(B))**2
    R = math.sqrt((c+d)/(e+f))*1000 #Maa raadius antud asukohas
    return R

#Sisestatud TLE
#Hetkel on programmi sisestatud ISSi 2022 aasta 25. Märtsi TLE, et
#saaks programmi kasutada ja katsetada. Programmiga töötamiseks tuleb
#näide kustutada ja allolevate kommentaaride eest trellid eemaldada.

#nimi = input()
#line1 = input()
#line2 = input()


#ISS TLE
nimi = "ISS (ZAYA)"
line1 = "1 25544U 98067A   22085.54972260  .00007645  00000+0  14396-3 0  9999"
line2 = "2 25544  51.6449  25.8751 0003971 314.1827 209.7972 15.49562496332369"



#Satelliidid pikkus- ja laiuskraadi leidmine
#https://space.stackexchange.com/questions/4211/calculate-satellite-coordinates-from-tle-data
sat = ephem.readtle(nimi, line1, line2);
sat.compute();

longs = sat.sublong / degree #satelliidi pikkuskraad
lats = sat.sublat / degree #satelliidi laiuskraad



#Päikse pikkus- ja laiuskraadi leidmine
pai=ephem.Sun(ephem.Date(datetime.utcnow()))
pai.compute()

Long=pai.ra / degree

#Viin kraadid pikkuskraadi vormistusse
if Long > 180:
    longp =  Long-360 #Päikese pikkuskraad
else:
    longp = Long #Päikese pikkuskraad
latp=pai.dec / degree #Päikese laiuskraad



#ECEF süsteem
#https://pythonrepo.com/repo/geospace-code-pymap3d-python-geolocation
h = 408000 #satelliidi kõrgus maapinnast (vajadusel avaldada)

#Päikese keskme kõrgus maapinnast
AU = pai.earth_distance*ephem.meters_per_au - raadius(latp)

#Vektorite leidmine Maa keskpunktist Päikeseni ja satelliididni
xs,ys,zs = pm.geodetic2ecef(lats,longs,h) #Satelliidi vektor
xp, yp, zp = pm.geodetic2ecef(lats,longs,AU) #Päikese vektor

#Suunavektori leidmine
xx=xp-xs
yy=yp-ys
zz=zp-zs

SPs=np.array([xx,yy,zz])

#Suunavektori muutmine ühikvektoriks
SP = SPs / np.linalg.norm(SPs)

SP=SP.tolist()

#Suunavektor sateliidi ja Päikese vahel
print(SP)