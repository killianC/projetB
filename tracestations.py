
import sqlite3 as sq
import matplotlib.pyplot as plt

import datetime as dt
import matplotlib.dates as pltd


def affcourbe(donneesc):
    """
    donneesc : [nomstat, y deb , m deb , d deb , y fin , m fin , d fin , courbe]
    """
    datedeb="'"+str(donneesc[1])+'-'+str(donneesc[2])+'-'+str(donneesc[3])+"'"
    datefin="'"+str(donneesc[4])+'-'+str(donneesc[5])+'-'+str(donneesc[6])+'Z'+"'"
    print(datedeb,datefin)
    nomstat="'"+donneesc[0]+"'"
    courbechoix=donneesc[7]
    conn = sq.connect('acoucite-mesures.db')
    c = conn.cursor()
    
    c.execute("SELECT time_iso FROM 'acoucite-mesures' WHERE procedure = "+nomstat+" AND time_iso > "+datedeb+" AND time_iso < "+datefin)
    vtime = c.fetchall()
    t = [pltd.date2num(dt.date(int(a[0][:4]),int(a[0][5:7]),int(a[0][8:10]))) for a in vtime]  

    
    c.execute("SELECT "+courbechoix+" FROM 'acoucite-mesures' WHERE procedure = "+nomstat+" AND time_iso > "+datedeb+" AND time_iso < "+datefin)
    val = c.fetchall()
    vall=[]
    n=len(val)
    for k in range (n):
        if val[n-k-1][0]=='None':
            val.pop(n-k-1)
            t.pop(n-k-1)
        else:
            vall.append(float(val[n-k-1][0]))
    vall.reverse()
    plt.plot_date(t,vall,linewidth=1, linestyle='-', marker='o')
    plt.show()    
    
affcourbe(['AF01',2008,1,2,2018,11,2,'levening'])
