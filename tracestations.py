
import sqlite3 as sq
import numpy as np
import matplotlib.pyplot as plt


def affcourbe(donneesc):
    """
    donneesc : [nomstat, y deb , m deb , d deb , y fin , m fin , d fin , courbe]
    """
    nomstat="'"+donneesc[0]+"'"
    conn = sq.connect('acoucite-mesures.db')
    c = conn.cursor()
    c.execute("SELECT lday FROM 'acoucite-mesures' WHERE procedure = "+nomstat)
    vlday = c.fetchall()
    print(vlday)
    lday=[]
    for i in range(len(vlday)):
        lday+=[float(vlday[i][0])]
    
    
    c.execute("SELECT time_iso FROM 'acoucite-mesures' WHERE procedure = "+nomstat)
    vtime = c.fetchall()
    
    
    
    
    t=np.linspace(0,len(vtime),len(vtime))
    print(t)
    
    
    plt.plot(t,lday)
    plt.show()
    
affcourbe(['AF01'])