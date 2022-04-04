import pmagpy.ipmag as ipmag
import ephem
from ephem import *
import datetime
import math

#https://stackoverflow.com/questions/6451655/how-to-convert-python-datetime-dates-to-decimal-float-years
def year_fraction(date): #Vajalik on leida hetkaeg aasta kümnendmurruna.
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return date.year + float(date.toordinal() - start) / year_length

#Hetkaeg: hetkaega küsitakse nelja komakohaga
kuup = round(year_fraction(datetime.datetime.today()), 4)

#Sisestatud TLE
#Hetkel on programmi sisestatud ISSi 2022 aasta 25. Märtsi TLE, et
#saaks programmi kasutada ja katsetada. Programmiga töötamiseks tuleb
#näide kustutada ja allolevate kommentaaride eest trellid eemaldada.

#nimi = input()
#line1 = input()
#line2 = input()


#ISS TLE
nimi = "ISS (ZAYA)";
line1 = "1 25544U 98067A   22085.54972260  .00007645  00000+0  14396-3 0  9999"
line2 = "2 25544  51.6449  25.8751 0003971 314.1827 209.7972 15.49562496332369"

#Satelliidid pikkus- ja laiuskraadi leidmine
#https://space.stackexchange.com/questions/4211/calculate-satellite-coordinates-from-tle-data
sat = ephem.readtle(nimi, line1, line2);
sat.compute();

longs = sat.sublong / degree #satelliidi pikkuskraad
lats = sat.sublat / degree #satelliidi laiuskraad


#Suunavektori leidmine
h = 408000 #satelliidi kõrgus maapinnast (vajadusel avaldada)

#Deklinatsiooni, inklinatsiooni ja tugevuse leidmine
local_field = ipmag.igrf([kuup, h, lats, longs], mod="")
#mod="" tähendab tavalist IGRF mudelit, sellega saab algoritmi täpsust muuta

#Saadud tulemused
d=local_field[0] #Deklinatsioon
i=local_field[1]+90 #Inklinatsioon
f=local_field[2] #Tugevus

#Suunavektori leidmine vastavalt sfäärilisele koordinaatsüsteemile
x=math.cos(d)*math.sin(i)
y=math.sin(d)*math.sin(i)
z=math.cos(i)

#Otsitud suunavektor
MG=[x,y,z]

print(MG) #Suunavektor
print(f) #Tugevus