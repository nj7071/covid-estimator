import matplotlib.pyplot as plt
import math as mt
import random
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np

#verjetnosti = [0.0125, 0.025, 0.0375, 0.05, 0.0625, 0.075, 0.0625, 0.05, 0.0375, 0.025, 0.0125]
verjetnosti = [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025]
a1 = 0.001   #parameter s katerim okužuje kužni
a2 = 0.00025    #parameter s katerim okužuje bolni
N = 1000   #populacija
populacija = 1000

D = 999
K = 1
B = 0
O = 0

dnevi = []
Dovzetni= []
Kuzni = []
Bolni = []
Odporni = []
dovzetne_celice = []
bolne_celice = []
kuzne_celice = []
odporne_celice = []

cas = 100

def koliko_dovzetnih_moram_pristeti(seznam_indexov):
    counter = 0
    for index in seznam_indexov:
        if lista_oseb[index].stanje == "D":
            lista_oseb[index].stanje = "K"
            lista_oseb[index].sprememba = dan + 1
            counter += 1
    return counter

def koliko_kuznih_moram_pristeti(seznam_indexov):
    counter1 = 0
    for index in seznam_indexov:
        if lista_oseb[index].stanje == "K":
            lista_oseb[index].stanje = "B"
            lista_oseb[index].sprememba = dan + 1
            counter1 += 1
    return counter1

def verjetnost_zbolevanja(verjetnost):      #funkcija izracuna na podlagi verjetnosti iz seznama verjetnosti ali je oseba zbolela
  x = random.random()
  if x < verjetnost:
    return True
  else:
    return False

class Oseba():
    def __init__(self, stanje = "D", sprememba = 0):
        self.stanje = "D"
        self.sprememba = 0

class Celica():
    def __init__(self, stanje_c = "D", spremeba_c = 0, clanstvo = []):
        self.stanje_c = "D"
        self.sprememba_c = 0
        self.clanstvo = []

#inicijalizacija
#kreiraj listo 1000 oseb z deafult atributi
lista_oseb =  []
objs = [Oseba() for i in range(1, N + 1)]
for obj in objs:
    lista_oseb.append(obj)

#kreirali bomo listo katere elementi so liste
#v vsakem elementu (listi) bo 1-10 indeksov oseb
#z normalno distribucijo smo poskrbeli, da je vecina celic velikosti okoli 2
#clanstvo v celici vsebuje tocne indexe vsebovanih oseb
lista_celic = []
populacija = len(lista_oseb)
start = 0
indexi_oseb_v_celicah = []

while start < populacija:
  random_cifra = round(random.gauss(2, 3))
  if random_cifra >= 1:
    stop = start + random_cifra
    if stop <= populacija:
      for x in range(start, stop, 1):
        indexi_oseb_v_celicah.append(x)
#      print("Indexi oseb v celicah:", indexi_oseb_v_celicah)
      celica = Celica()
      celica.clanstvo = indexi_oseb_v_celicah
      lista_celic.append(celica)
      print(indexi_oseb_v_celicah)

      start = stop
      indexi_oseb_v_celicah = []
Imune_celice = len(lista_celic) // 10
print(Imune_celice)
for i in range(0, Imune_celice):
    random_index = random.randint(0, len(lista_celic) - 1)
    lista_celic[random_index].stanje = "O"
    for j in range(len(lista_celic[random_index].clanstvo)):
        O += 1
        D -= 1


D_c = len(lista_celic) - Imune_celice
B_c = 0
K_c = 0
O_c = Imune_celice

for dan in range(1, cas):
    #izracunamo nove parametre za specificni dan
    novo_okuzeni = round((a1 * K + a2 * B) * D)
    if K + novo_okuzeni <= populacija and D - novo_okuzeni >= round(0.1 * N) and (D + K + B + O) == N:
        K += novo_okuzeni
        D -= novo_okuzeni
    if K + novo_okuzeni > N and D - novo_okuzeni < 0:
        K = N
        D = 0
    if D - novo_okuzeni <= round(0.1 * N):
        novo_okuzeni = 0


    #spremenimo status novo okuzenih oseb (random) > iz D v K in spremeba je dan (i) samo za osebe, ki so Dovzetne
    for i in range(1, novo_okuzeni):
      indeks_osebe = random.randint(0, populacija - 1)
      if lista_oseb[indeks_osebe].stanje == "D":
        lista_oseb[indeks_osebe].stanje = "K"
        lista_oseb[indeks_osebe].sprememba = dan


    #ali je oseba na ta dan zbolela in spremenimo stanja, da ne gremo večkrat po vseh osebah in da ne traja preveč časa
    #Če oseba zboli ali ozdravi, se temu ustrezno spremenijo dnevne številke kužnih, Bolnih in Odpornih
    #povsod so failsafi, da nikoli okuženi ne padejo pod 0 in dovzetni ne padejo pod 0 in vsi ostali parametri ne presežejo populacije
    for oseba in lista_oseb:
        razlika_dni = dan - oseba.sprememba
        if oseba.stanje == "K":
            if razlika_dni < 11:
                if verjetnost_zbolevanja(verjetnosti[razlika_dni - 1]):
                    if K - 1 >= 0 and B + 1 <= N:
                        oseba.stanje = "B"
                        oseba.sprememba = dan
                        K -= 1
                        B += 1
            if razlika_dni >= 11:
                if K - 1 >= 0 and O + 1 <= N:
                    oseba.stanje = "O"
                    K -= 1
                    O += 1
        if oseba.stanje == "B":
            if razlika_dni >= 15:
                if B - 1 >= 0 and O + 1 <= N:
                    oseba.stanje = "O"
                    B -= 1
                    O += 1
#        print(oseba.stanje)

    for i in range(0, len(lista_celic)):
#      print("Velikost celice:", len(lista_celic[i].clanstvo))
                                                                                #gremo po vseh celicah      --------> TEZAVA No.2 (Stevilke D_c, K_c, B_c in O_c se ne spreminjajo)
      for j in range(0, len(lista_celic[i].clanstvo)):                          #gremo po vseh osebah v celicah
        if lista_oseb[lista_celic[i].clanstvo[j]].stanje == "K" and lista_celic[i].stanje_c == "D":      #izognemo se primeru, da bi se celica še enkrat okužila
          lista_celic[i].stanje_c = "K"
          lista_celic[i].sprememba_c = dan + 1                                  #naslednji dan se okuži cela celica
          if D_c - 1 >= 0 and K_c + 1 <= len(lista_celic):
              D_c -= 1
              K_c += 1

#      for y in range(0, len(lista_celic[i].clanstvo)):
#        print(lista_oseb[lista_celic[i].clanstvo[y]].stanje)
        if lista_oseb[lista_celic[i].clanstvo[j]].stanje == "B" and lista_celic[i].stanje_c == "K":
             #izognemo se primeru, da bi celica še enkrat zbolela
          lista_celic[i].stanje_c = "B"
          lista_celic[i].sprememba_c = dan + 1                                  #naslednji dan zboli cela celica
          if K_c - 1 >= 0 and B_c + 1 <= len(lista_celic):
              B_c += 1
              K_c -= 1



      if lista_celic[i].stanje_c == "K":                                      #Če je celica kužna ima 2 možnosti: da ozdravi in se njeni člani prištejejo odpornim ali pa da zboli in se njeni člani prištejejo bolnim
            if dan - lista_celic[i].sprememba_c == 12:
               if O_c + 1 <= len(lista_celic) and K_c - 1 >= 0:
                   lista_celic[i].stanje_c = "O"
                   O_c += 1
                   K_c -= 1
                   for clan in range(len(lista_celic[i].clanstvo)):
                       if O + 1 <= N and K - 1 >= 0:
                           O += 1
                           K -= 1
            if dan - lista_celic[i].sprememba_c == 2:
                if K + koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo) <= N and D - koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo) >= 0:
                    K += koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo)   #s funkcijo se izognemo primeru, ki bi nas sesul, če pade/jo v isto celico več kot 1 okuženi
                    D -= koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo)
                if K + koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo) > N and D - koliko_dovzetnih_moram_pristeti(lista_celic[i].clanstvo) < 0:
                    K = N
                    D = 0

                        #funkcija prišteje okuženim vse dovzetne, ki so se okuzili po pravilu okuzevanja v celicah
#                      oseba[dovzetni].stanje == "K"
#                      oseba[dovzetni].sprememba = dan + 1
      if lista_celic[i].stanje_c == "B":                                      #če je celica zboli, se novi bolni prištejejo bolnim in na 16.dan se prištejejo odpornim
            if dan - lista_celic[i].sprememba_c == 16:
                lista_celic[i].stanje_c = "O"
                if O_c + 1 <= len(lista_celic) and B_c - 1 >= 0:
                    O_c += 1
                    B_c -= 1
                for i in range(len(lista_celic[i].clanstvo)):
                    if O + 1 <= N and B - 1 >= 0:
                        O += 1
                        B -= 1
            if dan - lista_celic[i].sprememba_c == 2:
                for kuzni in lista_celic[i].clanstvo:
                    if B + koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo) <= N and K - koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo) >= 0:
                        B += koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo)  #Podobno kot prejsna funkcija za okuzene
                        K -= koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo)  #ko en zboli, zbolijo vsi okuzeni v celici in se pristejejo h bolnim
                    if B + koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo) > N and K - koliko_kuznih_moram_pristeti(lista_celic[i].clanstvo) < 0:
                        B = N - O - D
                        K = 0
    random_index2 = random.randint(1, 10)
    if K - random_index2 >= 0 and B + random_index2 <= N:
        K -= random_index2
        B += random_index2



    Dovzetni.append(D)
    Kuzni.append(K)
    Bolni.append(B)
    Odporni.append(O)
    dovzetne_celice.append(D_c)
    kuzne_celice.append(K_c)
    bolne_celice.append(B_c)
    odporne_celice.append(O_c)
    dnevi.append(dan)

print("Stevilo gospodinjstev:", len(lista_celic))
print("Populacija:", N)

cnt1 = 0
cnt2 = 0
cnt3 = 0
cnt4 = 0
cnt5 = 0
cnt6 = 0
cnt7 = 0
cnt8 = 0
cnt9 = 0
cnt10 = 0


for celica in lista_celic:
    if len(celica.clanstvo) == 1:
        cnt1 += 1
    if len(celica.clanstvo) == 2:
        cnt2 += 1
    if len(celica.clanstvo) == 3:
        cnt3 += 1
    if len(celica.clanstvo) == 4:
        cnt4 += 1
    if len(celica.clanstvo) == 5:
        cnt5 += 1
    if len(celica.clanstvo) == 6:
        cnt6 += 1
    if len(celica.clanstvo) == 7:
        cnt7 += 1
    if len(celica.clanstvo) == 8:
        cnt8 += 1
    if len(celica.clanstvo) == 9:
        cnt9 += 1
    if len(celica.clanstvo) == 10:
        cnt10 += 1

print(cnt1)
print(cnt2)
print(cnt3)
print(cnt4)
print(cnt5)
print(cnt6)
print(cnt7)
print(cnt8)
print(cnt9)
print(cnt10)

xnew = np.linspace(0, 50, 99)
spl1 = make_interp_spline(dnevi, Dovzetni, k=3)
Dovzetni_smooth = spl1(xnew)


plt.title('Spreminjanje števil D, K, B, O, v odvisnosti od dni')
plt.xlabel('Dan')
plt.ylabel('Število ljudi')
plt.plot(dnevi, Dovzetni_smooth, 'r-', color='g', label='Dovzetni')
plt.plot(dnevi, Kuzni, 'r-', color='b', label='Kuzni')
plt.plot(dnevi, Bolni, 'r-', color='r', label='Bolni')
plt.plot(dnevi, Odporni, 'r-', color='c', label='Odporni')
plt.legend()
plt.show()
plt.savefig('Spreminjanjestevil.pdf')

plt.clf()
plt.title('Spreminajanje števila dovzetnih, kuznih, bolnih in odpornih celic (gospodinjstev)')
plt.xlabel('Dan')
plt.ylabel('Število celic')
plt.plot(dnevi, dovzetne_celice, color='g', label='Dovzetne celice')
plt.plot(dnevi, kuzne_celice, color='b', label='Kuzne celice')
plt.plot(dnevi, bolne_celice, color='r', label='Bolne celice')
plt.plot(dnevi, odporne_celice, color='c', label='Odporne celice')
plt.legend()
plt.show()
plt.savefig('SpreminjanjestevilaCelice.pdf')
