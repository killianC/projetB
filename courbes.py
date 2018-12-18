import sqlite3
import matplotlib.pyplot as plt
courbes=['lday','lden','levening','lnight']


conn = sqlite3.connect('acoucite-mesures.db')
c = conn.cursor()
c.execute("SELECT * FROM 'acoucite-mesures'")
r = c.fetchall()


lday=[]
lden=[]
levening=[]
lnight=[]
abs=[]

for row in r:
    if row[2] != 'None' and row[4] !='None' and row[5] != 'None':
        lday.append(float(row[2]))
        lden.append(float(row[3]))
        levening.append(float(row[4]))
        lnight.append(float(row[5]))
        abs.append(len(abs))
    
plt.plot(abs,lday)
plt.plot(abs,lden)
plt.plot(abs,levening)
plt.plot(abs,lnight)
plt.show()
    