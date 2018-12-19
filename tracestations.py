# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import sqlite3 as sq
import numpy as np
import matplotlib.pyplot as plt

base = sq.connect('acoucite-mesures.db')
b = base.cursor()

    
b.execute("SELECT 'time_iso' AND 'lday' FROM 'acoucite-mesures' WHERE 'procedure' = 'AF01' ")

r = b.fetchall()

debut=50
fin=150
t=np.linspace(debut,fin,fin-debut+1)

vecteur=[]

for i in range(len(t)):
    vecteur+=[r[i][2]]
    
plt.plot(t,vecteur)
plt.show()







