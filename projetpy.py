# Lien du site :
# http://localhost:8080/htmlbruit_acoucite.html

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3
import datetime as dt
import matplotlib.dates as pltd
import matplotlib.pyplot as plt

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client'
  # version du serveur
  server_version = 'ProjetB/serveurpy.py/0.1'

  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self):
    self.init_params()

    # requete location - retourne la liste de lieux et leurs coordonnées géographiques
    if self.path_info[0] == "location":     
        self.send_json(self.data())

    elif self.path_info[0] == "courbe":
        donneesc = self.path_info[1]
        verifdate = donneesc.split("-")
        if verifdate[1]+verifdate[2]+verifdate[3] < verifdate[4]+verifdate[5]+verifdate[6] :
            conn = sqlite3.connect('client/courbesstockees.db')
            c = conn.cursor()
            c.execute("SELECT Nom FROM 'courbesstockees'")
            r = c.fetchall()
            noms=[]
            for nom in r:
                noms.append(nom[0])
            if len(noms)!=0 and donneesc in noms:
                self.send(self.path_info[1])
            else:
                donneesc = donneesc.split("-")
                for k in range (len(donneesc)):
                    if k!=len(donneesc)-1:
                        donneesc[k]=int(donneesc[k])
                data=self.data()
                if data[donneesc[0]-1]["name"][-6:-2]=="CF22":
                    nomstat=data[donneesc[0]-1]["name"][-6:]
                else:
                    nomstat=data[donneesc[0]-1]["name"][-4:]
                donneesc[0]=nomstat
                self.creecourbe(self.path_info[1],donneesc)
                c = conn.cursor()
                c.execute("INSERT INTO 'courbesstockees'('Nom') VALUES ('"+self.path_info[1]+"');")
                conn.commit()
                self.send(self.path_info[1])
        else :
            None
        
    else:
      self.send_static()

 
    
  #Methode annexe 
    
  def data(self):
      conn = sqlite3.connect('stations-acoucite-2018.db')
      c = conn.cursor()
      c.execute("SELECT * FROM 'stations-acoucite-2018'")
      r = c.fetchall()
      data=[]
      for k in range (len(r)):
          dicotempo={}
          dicotempo['id']=k+1
          dicotempo['lat']=float(r[k][1])
          dicotempo['lon']=float(r[k][0])
          dicotempo['name']=r[k][4]
          data.append(dicotempo)
      return(data)
      
      
  def creecourbe(self,url,donneesc):
    """
    donneesc : [nomstat, y deb , m deb , d deb , y fin , m fin , d fin , courbe]
    """
    datedeb="'"+str(donneesc[1])+'-'+'0'*(2-len(str(donneesc[2])))+str(donneesc[2])+'-'+'0'*(2-len(str(donneesc[3])))+str(donneesc[3])+"'"
    datefin="'"+str(donneesc[4])+'-'+'0'*(2-len(str(donneesc[5])))+str(donneesc[5])+'-'+'0'*(2-len(str(donneesc[6])))+str(donneesc[6])+'Z'+"'"
    nomstat="'"+donneesc[0]+"'"
    courbechoix=donneesc[7]
    conn = sqlite3.connect('acoucite-mesures.db')
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

    plt.clf()
    plt.plot_date(t,vall,linewidth=1, linestyle='-', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Niveau sonore en dB')
    plt.title('Niveau sonore de la station '+nomstat +' en fonction du temps')
    fichier = url+'.png'
    plt.savefig('client/bdd/{}'.format(fichier))
    
    
  # méthode pour traiter les requêtes HEAD
  def do_HEAD(self):
      self.send_static()


  # méthode pour traiter les requêtes POST - non utilisée dans l'exemple
  def do_POST(self):
    self.init_params()

    # requête générique
    if self.path_info[0] == "service":
      self.send_html(('<p>Path info : <code>{}</code></p><p>Chaîne de requête : <code>{}</code></p>' \
          + '<p>Corps :</p><pre>{}</pre>').format('/'.join(self.path_info),self.query_string,self.body));

    else:
      self.send_error(405)


  # on envoie le document statique demandé
  def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)


  # on envoie un document html dynamique
  def send_html(self,content):
     headers = [('Content-Type','text/html;charset=utf-8')]
     html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
         .format(self.path_info[0],content)
     self.send(html,headers)

  # on envoie un contenu encodé en json
  def send_json(self,data,headers=[]):
    body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
    self.send_response(200)
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length',int(len(body)))
    [self.send_header(*t) for t in headers]
    self.end_headers()
    self.wfile.write(body) 

  # on envoie la réponse
  def send(self,body,headers=[]):
     encoded = bytes(body, 'UTF-8')

     self.send_response(200)

     [self.send_header(*t) for t in headers]
     self.send_header('Content-Length',int(len(encoded)))
     self.end_headers()

     self.wfile.write(encoded)


  # on analyse la requête pour initialiser nos paramètres
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''
   
    # traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)


# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
