from random import randint
import time


# vrati ake policko sa ma nachadzat na sachovnici na danej suradnici
def policko(x, y, n):
    if (((x==n//2+1 or x==n//2-1) and (y!=n//2)) or  # stlpce
        ((y==n//2+1 or y==n//2-1) and (x!=n//2)) or  # riadky
        ((y==n//2) and (x==0 or x==n-1)) or  # tam kde sa ide do domceku
        ((x==n//2) and (y==0 or y==n-1))):  # tam kde sa ide do domceku
        return '*'
    elif (((x<=4 and y==n//2) or (x>=n-5 and y==n//2)) or #ak su splnene podmienky
         ((y<=4 and x==n//2) or (y>=n-5 and x==n//2))): #ak su splnene podmienky
        return 'D'  #domceky
    elif (x==n//2 and y==x):  # stred
        return 'X'
    else:
        return ' '
      
# vrati sachovnicu o rozmere n
def gensachovnicu(n):
    return [[policko(x, y, n) for y in range(n)] for x in range(n)]

    
# funkcia ktora vypise sachovnicu
def printsachovnicu(sachovnica, hraci):
    # horny riadok so stlpcami
    print ('  ', end=' ')
    for x in range(0, len(sachovnica)):
        print ("%2d" % (x), end=' ')
    print()
    # sachovnica
    for y in range(0, len(sachovnica)):
        print ("%2d" % (y), end=' ')
        for x in range(0, len(sachovnica)):
            # je tu hrac?
            pp = False
            for p in range(0, len(hraci)):
                if (x,y) in hraci[p]:
                    # na tejto pozicii je hrac, vypiseme ho
                    print (chr(ord('A')+p)+' ', end=' ')
                    pp = True
                    break
            if not pp:  # ziadny hrac
                print (sachovnica[x][y]+' ', end=' ')
        print()
    print()

    
# vrati nasledujuce policko, ak stojime na x,y a sme 'hrac'
def krok(x, y, sachovnica, hrac):
    n = len(sachovnica)
    # sme kde su horne a dolne domceky
    if hrac==0 and x==n//2:
        if y>n//2+1:  # ideme do domceka dole
            return (x, y-1)
        elif y==0:  # toto je horny domcek, nas je dole
            return (x+1, y)
        else:
            return None  # sme v domceku a dalej sa ist neda
    # to iste ale pre horny domcek (hrac 2)
    if hrac==1 and x==n//2:
        if y<n//2-1:
            return (x, y+1)
        elif y==n-1:
            return (x-1, y)
        else:
            return None
    # da sa ist dolava? ak sme v dolnej polovici, ideme len do tej strany
    if x!=0 and y>n//2 and sachovnica[x-1][y]=='*':
        return (x-1, y)
    # sa sa ist doprava? v hornej polovici sa da ist len doprava (nie dolava)
    if x!=n-1 and y<n//2 and sachovnica[x+1][y]=='*':
        return (x+1, y)
    # da sa ist hore? v lavej polovici sa ide len hore
    if y!=0 and x<n//2 and sachovnica[x][y-1]=='*':
        return (x, y-1)
    # da sa ist dole? v pravej polovici sa ide len dole
    if y!=n-1 and x>n//2 and sachovnica[x][y+1]=='*':
        return (x, y+1)
    
    
# vrati poziciu panacika, ak je na 'pozicia' a chce ist o 'hod' tahov a patri hracovi 'hrac'
# ak sa tolko pohnut neda, vrati None
def dalsia_pozicia(pozicia, sachovnica, hrac, hod):
    # len dost krat zopakujeme krok
    for i in range(1, hod+1):
        pozicia=krok(pozicia[0], pozicia[1], sachovnica, hrac)
        if pozicia is None:
            return None
    return pozicia  

    
# overi, ci dany hrac vyhral
def vyhral(hrac, hraci, sachovnica):   
    n = len(sachovnica)
    # ma na sachovnici dost panakov?
    if len(hraci[hrac])<n//2-1:
        return False
    # su vsetci pekne zoradeni v domceku vedla seba?
    for panak in hraci[hrac]:
        if panak[0]!=n//2 and panak[1]!=n//2:
            return False
        if panak[0]==0 or panak[1]==0 or panak[0]==n-1 or panak[1]==n-1:
            return False
    return True
    
# kde ma byt nova figurka hraca?
def pozicia_domceku(hrac):
    return (n//2-1, n-1) if hrac==0 else (n//2+1,0)
   

while True: #Cyklus pre vstupy
    n = int(input("Zadaj velkost kriza(musi byt neparna a vacsia ako 11):")) #Vstup od uzivatela
    if n < 11:
        print("Zadal si malu hraciu plochu, zadaj vacsie cislo!")
    elif n%2==0:
        print("Zadal si parne cislo,zadaj neparne!")
    else:
        break  #Ak nie su podmienky splnene, cyklus sa breakne    

# 2ja hraci, kazdy ma po jednom panacikovi
hraci = [[pozicia_domceku(0)], [pozicia_domceku(1)]]
sachovnica = gensachovnicu(n)
printsachovnicu (sachovnica, hraci)
na_tahu=0

# chvilu sa chcem divat co sa deje
time.sleep(2)

# cyklus hry
while True:
    # kolko hodov mame?
    pocet_hodov = 1 if len(hraci[na_tahu])>=1 else 3
    # interne pocitadla
    cislo_hodu = 1
    # kolko realne hrac vo svojom hode hadzal kockou
    realne_cislo_hodu = 0
    while cislo_hodu<=pocet_hodov:
        hod = randint(1, 6)  # hod kockou
        nova_pozicia = None  # kam sa dostaneme
        if pocet_hodov==3:
            if hod==6:  # hodili sme 6, hura
                cislo_hodu=1
                pocet_hodov=1
                nova_pozicia = pozicia_domceku(na_tahu)
                print ("Vlozena figurka")
        # ak hodime 6, mozme ist znova
        if hod==6:
            cislo_hodu-=1
        # pre kazdeho panaka hraca skusime, ci sa moze pohnut
        # ak ano, pohneme s prvym najdenim
        for panak in hraci[na_tahu]:
            nova_pozicia = dalsia_pozicia(panak, sachovnica, na_tahu, hod)
            if (nova_pozicia is not None):  # mame sa kam pohnut
                if nova_pozicia in hraci[na_tahu]:  # no zial je tam nas panacik, mame smolu
                    nova_pozicia=None
                else:
                    # presunieme panacika
                    hraci[na_tahu].remove(panak)         
                    hraci[na_tahu].append(nova_pozicia)
                    break
        # ziadny panacik sa nemohol pohnut
        if nova_pozicia is None:
            if hod==6 and len(hraci[na_tahu])<n//2-1:  # ale mozno sme hodili 6? a este nemame vsetkych na sachovnici
                nova_pozicia=pozicia_domceku(na_tahu)
                hraci[na_tahu].append(nova_pozicia)
                print ("Vlozena figurka")
            else:
                print ("Zahodeny tah")
        # pristali sme na nepriatelovi?
        for i in range(0, len(hraci)):
            if i==na_tahu:
                continue
            if nova_pozicia in hraci[i]:
                print ("Vyhodeny hrac")
                hraci[i].remove(nova_pozicia)
        cislo_hodu+=1
        realne_cislo_hodu+=1
        printsachovnicu(sachovnica, hraci)
        print ("Hrac %s hodil %s (hod c.%s)" % ((chr(ord('A')+na_tahu)), hod, realne_cislo_hodu))
        
        time.sleep(2) # chvilu sa divame, co sa deje
       
    # ak sme spravili vitazny tah, skoncime
    if vyhral(na_tahu, hraci, sachovnica):
        break
    else:  # inak moze ist dalsi hrac
        na_tahu=(na_tahu+1)%len(hraci)
 
print ("Vyhral hrac %s." % (chr(ord('A')+na_tahu)))
input()

