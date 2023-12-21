# Ohjelma luo pygame pelin, jossa pyritään keräämään kolikoita voittorajan saavuttamiseksi
# Vastustajana tässä pelissä toimii verottaja, jonka hirviöt yrittävät napata keräämäsi rahat
# Pelin sankarina toimii Robo, joka voi liikkua näytön alareunassa vasemmalle tai oikealle sekä hypätä

# Peli on luotu Mahtijahti luokkaan ja sen sisäisiin metodeihin
# Alussa tulostuu aloitusnäyttö, jossa voi muokata pelin asetuksia ja taustan väriä
# Aloitusnäytöstä voi valita ohjenäytön, jossa kerrotaan pelin tavoite ja käytettävissä olevat näppäimet

# V1.2 on lisätty alkuperäiseen taustamusiikki ja äänet napatessa kolikko ja osuessa verottajaan
import pygame
from random import randint
from pygame import mixer


# Luodaan luokka Mahtijahti
class Mahtijahti:
    # Luodaan konstuktori
    def __init__(self):
        # Käynnistetään pygame
        pygame.init()
        
        pygame.display.set_caption("Mahtijahti") # Annetaan pelille nimi pygame ikkunassa
        self.naytto = pygame.display.set_mode((640, 480)) # Määritetään näytön koko
        self.vari = (0, 150, 0) # Asetetaan aloitusväriksi vihertävä väri

        # Määritetään kuvat ja niiden mitat
        self.kolikko = pygame.image.load("kolikko.png")
        self.kolikko_korkeus = self.kolikko.get_height()
        self.kolikko_leveys = self.kolikko.get_width()

        self.hirvio = pygame.image.load("hirvio.png")
        self.hirvio_korkeus = self.hirvio.get_height()
        self.hirvio_leveys = self.hirvio.get_width()

        self.robo = pygame.image.load("robo.png")
        self.robo_korkeus = self.robo.get_height()
        self.robo_leveys = self.robo.get_width()

        # Luodaan tyhjät listat kolikoille ja hirviöille
        self.rahat = []
        self.hirviot = []

        # Kolme eri kokoista fontti, joita käytetään teksteissä
        # Fontiksi on valittu comic sans ms
        self.fontti = pygame.font.SysFont("comicsansms", 24)
        self.fontti_iso = pygame.font.SysFont("comicsansms", 70)
        self.fontti_pieni = pygame.font.SysFont("comicsansms", 14)

        # Alustetaan taustamusiikki pelkästään tekstiksi
        self.tausta_musiikki = "ei musiikkia"

        # Alusteaan arvo
        self.kolikot = 0
        self.hirvio_kolikot = 0
        self.xr = 320 - self.robo_leveys // 2
        self.yr = 478 - self.robo_korkeus

        # Määritetään kello, jota käytetään luodessa uusia kolikoita
        self.kello = pygame.time.Clock()
        self.edellinen = pygame.time.get_ticks()

        # Alustetaan arvoja
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.ilmassa = False
        self.peli = True
        self.alku = True
        self.voitto_aani = False
        self.voitto = False
        self.havio = False
        self.musiikki = False
        #self.musa_paalla = False

        self.vaikeustaso = 1
        self.nopeus = 1
        self.aika_alku = 1500
        self.aika_loppu = 3500
        self.hirviot_enintaan = 2
        self.voittoraja = 20
        
        self.teksti = ""

    # Tämä metodi päivittää arvoja vastaamaan haluttua vaikeustasoa
    def paivita_vaikeustaso(self, vaikeustaso):
        self.vaikeustaso = vaikeustaso

        if self.vaikeustaso == 1:
            self.aika_alku = 1500
            self.aika_loppu = 3500
            self.hirviot_enintaan = 2
            self.voittoraja = 20
        elif self.vaikeustaso == 2:
            self.aika_alku = 1000
            self.aika_loppu = 3000
            self.hirviot_enintaan = 3
            self.voittoraja = 40
        elif self.vaikeustaso == 3:
            self.aika_alku = 800
            self.aika_loppu = 2000
            self.hirviot_enintaan = 5
            self.voittoraja = 60

    # Metodi päivittää taustan värin
    def paivita_vari(self, sininen, vihrea, punainen):
        self.vari = (sininen, vihrea, punainen)

    # Aloitusnäyttö ja siinä olevat toiminnot
    def aloitus(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT: # Sulkee ohjelman jos klikataan hiirellä ruksia
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE: # Sulkee ohjelman jos painetaan ESC (tästä on myös infoteksti tulostettuna)
                        exit()
                    if tapahtuma.key == pygame.K_RETURN: # ENTER / RETURN painettaessa peli, eli pelisilmukka() käynnistyy
                        self.pelisilmukka()
                        mixer.music.stop()
                    if tapahtuma.key == pygame.K_1: # Määritetään vaikeustaso painamalla numeronäppäimiä 1, 2 tai 3
                        self.paivita_vaikeustaso(1)
                    if tapahtuma.key == pygame.K_2:
                        self.paivita_vaikeustaso(2)
                    if tapahtuma.key == pygame.K_3:
                        self.paivita_vaikeustaso(3)
                    if tapahtuma.key == pygame.K_7: # Määritetään haltessa taustan väri painamalla 7, 8 tai 9
                        self.paivita_vari(255, 0, 0) # Punainen
                    if tapahtuma.key == pygame.K_8:
                        self.paivita_vari(0, 150, 0) # Peliin sopiva vihreän sävy
                    if tapahtuma.key == pygame.K_9:
                        self.paivita_vari(0, 0, 255) # Sininen
                    if tapahtuma.key == pygame.K_o: # Painettaessa o, kutsutaan metodia tulosta_ohjeet()
                        self.tulosta_ohjeet()
                    if tapahtuma.key == pygame.K_4:
                        self.musiikki = False
                        self.tausta_musiikki = "ei musiikkia"
                        mixer.music.stop()
                    if tapahtuma.key == pygame.K_5:
                        self.tausta_musiikki = 'money_rain.mp3'
                        mixer.music.load(self.tausta_musiikki)
                        mixer.music.play(-1)
                        self.musiikki = True
                    if tapahtuma.key == pygame.K_6:
                        self.tausta_musiikki = 'robot_music.mp3'
                        mixer.music.load(self.tausta_musiikki)
                        mixer.music.play(-1)
                        self.musiikki = True

                self.naytto.fill(self.vari) # Täytetään tausta luokan self.vari mukaisesti

                # Tulostetaan näytölle tekstit
                teksti = self.fontti.render("ESC", True, (0, 0, 0))
                self.naytto.blit(teksti, (10 , 5))
                teksti = self.fontti.render(f"Musiikki: {self.tausta_musiikki}", True, (0, 0, 0))
                self.naytto.blit(teksti, (300 , 5))
                teksti = self.fontti_pieni.render("4 = ei musiikki, 5 = money rain 6 = robot music", True, (0, 0, 0))
                self.naytto.blit(teksti, (300 , 35))
                teksti = self.fontti_pieni.render("Poistu pelistä", True, (0, 0, 0))
                self.naytto.blit(teksti, (10 , 35))

                teksti = self.fontti_iso.render("Mahtijahti", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 110 - teksti.get_height() / 2))

                teksti = self.fontti.render("Haluatko pelata?", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 180 - teksti.get_height() / 2))
                teksti = self.fontti.render("ENTER = kyllä", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 230 - teksti.get_height() / 2))
                teksti = self.fontti.render("O = ohjeet", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 270 - teksti.get_height() / 2))
                teksti = self.fontti.render("ESC = poistu", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 310 - teksti.get_height() / 2))

                teksti = self.fontti_pieni.render("Valitse ensin vaikeustaso 1, 2 tai 3", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 355 - teksti.get_height() / 2))
                teksti = self.fontti_pieni.render("Valitse taustan väri 7 = punainen, 8 = vihreä. 9 = sininen", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 375 - teksti.get_height() / 2))

                teksti = self.fontti.render("Vaikeustaso: " + str(self.vaikeustaso), True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 415 - teksti.get_height() / 2))
                teksti = self.fontti_pieni.render("Valitse painamalla 1, 2 tai 3 ", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 440 - teksti.get_height() / 2))
            
            pygame.display.flip() # Päivittää näytön
    
    # Aloitusnäyttöä vastaava näyttö ohjeille ja pelissä käytettäville näppäimille
    def tulosta_ohjeet(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE: # Jos painetaan ESC ohjelma palaa aloitusnäyttöön
                        self.aloitus()

                # Tulostetaan näytölle tekstit
                self.naytto.fill(self.vari)
                teksti = self.fontti.render("ESC", True, (0, 0, 0))
                self.naytto.blit(teksti, (10 , 5))
                teksti = self.fontti_pieni.render("Palaa aloitusnäyttöön", True, (0, 0, 0))
                self.naytto.blit(teksti, (10 , 35))
                teksti = self.fontti_iso.render("Ohjeet", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 70 - teksti.get_height() / 2))
                teksti = self.fontti.render("Kerää kolikoita ja varo verottajia", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 150 - teksti.get_height() / 2))
                teksti = self.fontti.render("Verottaja kerää kolikoita osumalla sinuun", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 180 - teksti.get_height() / 2))
                teksti = self.fontti.render("Jos osut verottajaan, vie se sinulta", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 210 - teksti.get_height() / 2))
                teksti = self.fontti.render("enintään 10 kolikkoa", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 240 - teksti.get_height() / 2))
                teksti = self.fontti.render("Näppäimet", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 290 - teksti.get_height() / 2))
                teksti = self.fontti.render("T = tauko", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 320 - teksti.get_height() / 2))
                teksti = self.fontti.render("U = uusi peli", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 350 - teksti.get_height() / 2))
                teksti = self.fontti.render("ESC = palaa alkuun ", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 380 - teksti.get_height() / 2))
                teksti = self.fontti.render("vasen / oikea = liiku ", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 410 - teksti.get_height() / 2))
                teksti = self.fontti.render("ylös = hyppää ", True, (0, 0, 0))
                self.naytto.blit(teksti, (320 -teksti.get_width() / 2, 440 - teksti.get_height() / 2))
            
            pygame.display.flip() # Päivittää näytön

    # Jos pelisilmukassa kutsutaan metodia uusi_peli() -> palautetaan arvot
    def uusi_peli(self):
        self.kolikot = 0
        self.hirvio_kolikot = 0
        self.xr = 320 - self.robo_leveys // 2
        self.yr = 478 - self.robo_korkeus
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.ilmassa = False
        self.peli = True
        self.alku = True
        self.voitto_aani = False
        self.voitto = False
        self.havio = False
        self.rahat.clear()
        self.hirviot.clear()
        if self.musiikki == True:
            mixer.music.play(-1)
    
    # Kun peli ratkeaa tulostetaan keskelle näyttöä teksi ja sen alle suorakulmio
    def tulosta_lopputilanne(self):
        mixer.music.stop()
        #teksti = self.fontti_iso.render(self.teksti, True, (0, 0, 0))
        #pygame.draw.rect(self.naytto,(0, 255, 0),(320 - teksti.get_width() / 2 - 20, 240 - teksti.get_height() / 2 - 20, teksti.get_width() + 40, teksti.get_height() + 40,))
        #self.naytto.blit(teksti, (320 - teksti.get_width() / 2, 240 - teksti.get_height() / 2))
        self.voitto_aani = True
        if self.voitto == True:
            voitto_aani = mixer.Sound('coins_pouring.mp3')
            voitto_aani.play()
            jihuu = mixer.Sound('jihuu.mp3')
            jihuu.play()
            you_win = mixer.Sound('you_win.mp3')
            you_win.play()
            self.voitto = False
        if self.havio == True:
            #havio_aani = mixer.Sound('laugh_evil_end.mp3')
            havio_aani = mixer.Sound('verottaja_voitto.mp3')
            havio_aani.play()
            self.havio = False

    # Metodi tulostaa näytölle tekstit jotka kertovat pelin tilanteen ja lisäksi pienellä tekstillä käytettävissä olevat näppäimet
    def tulosta_tiedot(self):
        if self.kolikot < 10:
            piste_teksti = self.fontti.render(f"Kolikot: 0{self.kolikot}/{self.voittoraja}", True, (0, 0, 0))
        else:
            piste_teksti = self.fontti.render(f"Kolikot: {self.kolikot}/{self.voittoraja}", True, (0, 0, 0))
        self.naytto.blit(piste_teksti, (465, 5))
        if self.hirvio_kolikot < 10:
            piste_teksti = self.fontti.render(f"Verottaja: 0{self.hirvio_kolikot}/{self.voittoraja}", True, (0, 0, 0))
        else:
            piste_teksti = self.fontti.render(f"Verottaja: {self.hirvio_kolikot}/{self.voittoraja}", True, (0, 0, 0))
        self.naytto.blit(piste_teksti, (435, 30))
        if self.alku:
            piste_teksti = self.fontti_pieni.render("T = tauko", True, (0, 0, 0))
            self.naytto.blit(piste_teksti, (10, 15 - piste_teksti.get_height() / 2))
            teksti = self.fontti_pieni.render("U = uusi peli", True, (0, 0, 0))
            self.naytto.blit(teksti, (10, 30 - teksti.get_height() / 2))
            teksti = self.fontti_pieni.render("ESC = palaa alkuun", True, (0, 0, 0))
            self.naytto.blit(teksti, (10, 45 - teksti.get_height() / 2))
            teksti = self.fontti_pieni.render("vasen / oikea = liiku", True, (0, 0, 0))
            self.naytto.blit(teksti, (10, 60 - teksti.get_height() / 2))
            teksti = self.fontti_pieni.render("ylös = hyppää", True, (0, 0, 0))
            self.naytto.blit(teksti, (10, 75 - teksti.get_height() / 2))
    
    # Metodi jossa sattuman varaisesti kutsutaan metodia luo_uusi_kolikko()
    # Vaikeustason mukaan vaikutetaan miltä väliltä ilmestyminen arvotaan
    def generoi_uusi_kolikko(self):
        aika_nyt = pygame.time.get_ticks()
        if aika_nyt - self.edellinen > randint(self.aika_alku, self.aika_loppu):
            self.rahat.append(self.luo_uusi_kolikko())
            self.edellinen = aika_nyt

    # Metodi jossä määritetään kutustaanko metodia luo_uusi_hirvio() tai vaikeustason ollessa 3 luo_uusi_nopea_hirvio())
    def generoi_uusi_hirvio(self):
        sattuma = randint(0,3)
        if len(self.hirviot) < self.hirviot_enintaan and sattuma == 1:
            self.hirviot.append(self.luo_uusi_hirvio() if self.vaikeustaso in [1,2] else self.luo_uusi_nopea_hirvio())

    # Luo uuden kolikon
    def luo_uusi_kolikko(self):
        x = randint(0, 640 - self.kolikko_leveys)
        y = 0 - self.kolikko.get_height()
        return {'x': x, 'y': y, 'nopeus': self.nopeus}

    # Luo uuden hirviön
    def luo_uusi_hirvio(self):
        x = randint(0, 640 - self.hirvio_leveys)
        y = 0 - self.hirvio_korkeus
        return {'x': x, 'y': y, 'nopeus': self.nopeus + randint(1,2)}
    
    # Vaikeustason ollessa 3 kutsutaan tätä metodia, jolloin luodaan nopeampia hirviöitä
    def luo_uusi_nopea_hirvio(self):
        x = randint(0, 640 - self.hirvio_leveys)
        y = 0 - self.hirvio_korkeus
        return {'x': x, 'y': y, 'nopeus': self.nopeus + randint(2,3)}           

    # Varsinainen pelisilmukka
    def pelisilmukka(self):
        lets_go_ok = mixer.Sound('lets_go_ok.mp3')
        lets_go_ok.play()
        if self.musiikki == True:
                    mixer.music.load(self.tausta_musiikki)
                    mixer.music.play(-1)
        while True:
            for tapahtuma in pygame.event.get(): # Sama kuin aiemmin
                if tapahtuma.type == pygame.QUIT:
                    exit()

                if tapahtuma.type == pygame.KEYDOWN: # Jos painetaan jotain näppäintä
                    if tapahtuma.key == pygame.K_ESCAPE: # Palauttaa pelin aloitusnäyttöön ja palauttaa arvot
                        self.uusi_peli()
                        self.aloitus()
                        mixer.music.stop()
                    if tapahtuma.key == pygame.K_LEFT: # Robon liikkuminen
                        self.vasemmalle = True
                        liike_aani = mixer.Sound('robo_liikkuu1.mp3')
                        liike_aani.play()
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = True
                        liike_aani = mixer.Sound('robo_liikkuu1.mp3')
                        liike_aani.play()
                    if tapahtuma.key == pygame.K_t: # Painettaessa t self.alku totuusehto muuttuu ja peli tauottuu ja jatkuu painettaessa t uudelleen
                        self.alku = not self.alku
                    if tapahtuma.key == pygame.K_u: # Aloittaa uuden pelin
                        self.uusi_peli()
                    if tapahtuma.key == pygame.K_UP: # Painettaessa ylös Robo "hyppää"
                        if self.ilmassa == True: # self.ilmassa on määritetty sen vuoksi, ettei robo voi hypätä uudelleen ollessaan ilmassa
                            hyppy_aani = mixer.Sound('jump2.mp3')
                            hyppy_aani.play()
                            self.ylos = True
                        
                if tapahtuma.type == pygame.KEYUP: # Liike sivuille lakkaa jos näppäin nostetaan ylös
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = False

            if self.alku and self.oikealle and self.xr < 640 - self.robo_leveys: # Antaa Robon x kohdalle uuden arvon
                self.xr += 5
            if self.alku and self.vasemmalle and self.xr > 0:
                self.xr -= 5
    
            self.naytto.fill(self.vari) # Täytetään tausta valitulla värillä
            #pygame.draw.rect(self.naytto,(0, 255, 0),(320 - teksti.get_width() / 2 - 20, 240 - teksti.get_height() / 2 - 20, teksti.get_width() + 40, teksti.get_height() + 40,))
            if self.alku: # Jos ehto on tosi, peli etenee ja tulostetaan kolikot ja hirviöt näytölle
                for kohta in self.rahat:
                    self.naytto.blit(self.kolikko, (kohta['x'], kohta['y']))
                for kohta in self.hirviot:
                    self.naytto.blit(self.hirvio, (kohta['x'] + randint(-2,2), kohta['y'] + randint(-2,2)))
                
                self.naytto.blit(self.robo, (self.xr, self.yr)) # Tulostetaan Robo näytölle

                if self.peli: # Jos self.peli arvo on tosi, eli peli ei ole ratkennut ---> Ohjelma etenee

                    if self.yr < 280: # Määritetään raja kuinka korkealle robo voi hypätä
                        self.ilmassa = False # Tällä varmistetaan, ettei hyppääminen ilmassa onnistu ennen, kuin on laskeuduttu alas
                        self.ylos = False # "hyppäämisen" ehto muuttuu epötodeksi
                    if self.yr + self.robo_korkeus >= 480: # Kun Robo palaa takaisin alas...
                        self.ilmassa = True # self.ilmassa ehto palaa todeksi ja hyppääminen onnistuu
                    if self.ylos: # Tässä robo "hyppää"
                        for kohta in range(0,5):
                            self.yr -= 1
                            self.ilmassa = True
                    if not self.ylos and self.yr < 480 - self.robo_korkeus: # Robo palaa alas hypyn jälkeen
                        for kohta in range(0,5):
                            self.yr += 1
                            self.ilmassa = False

                    for kohta in self.hirviot: # Käsitellään hirviöiden liikettä näytöllä
                        kohta['y'] += kohta['nopeus']
                        if kohta ['y'] > 480:
                            if kohta in self.hirviot: # Ehto on lisätty mahdollisten Value Erroreiden vuoksi
                                self.hirviot.remove(kohta) # Jos hirviö poistuu näytöltä, poistetaan se myös listasta
                        if kohta ['y'] < 440: # Pelattavuuden vuoksi verottaja voi napata robon jos se on näytöllä kohdassa 440 tai sitä ylempänä
                            # Alla oleva ehto on rajattu niin, kosketus verottajaan vaikuttaa luontevalta, eikä ole siis liian "herkkä"
                            if kohta['y'] + self.hirvio_korkeus - 15 in range(int(self.yr), int(self.yr) + self.robo_korkeus + self.hirvio_korkeus) and int(self.xr) in range(int(kohta['x'] - self.hirvio_leveys / 2 - 10), int(kohta['x'] + self.hirvio_leveys - 10)):
                                hirvio_aani = mixer.Sound('laugh_evil.mp3')
                                hirvio_aani.play()
                                ou_nou_aani = mixer.Sound('aana_ou_nou.mp3')
                                ou_nou_aani.play()
                                if self.kolikot in range(1,9): # Jos pelaajalla on alle kymmenen kolikkoa verottaja vie kaikki, mutta kolikot eivät mene miinukselle
                                    self.hirvio_kolikot += self.kolikot
                                    self.kolikot -= self.kolikot
                                if self.kolikot > 9: #Jos kolikkoja on vähintään kymmenen, vie verottaja 10"
                                    self.hirvio_kolikot += 10 # Verottajan kolikkomäärä kasvaa
                                    self.kolikot -= 10
                                if kohta in self.hirviot: # Ehto on lisätty mahdollisten Value Erroreiden vuoksi
                                    self.hirviot.remove(kohta) # Hirviö poistetaan listalta jos se osuu roboon
            
                    # Vastaava silmukka kolikoiden käsittelyyn
                    for kohta in self.rahat:
                        kohta['y'] += kohta['nopeus']

                        if kohta['y'] + self.kolikko.get_height() in range(self.yr, self.yr + self.robo_korkeus + self.kolikko.get_height()) and int(self.xr) in range(int(kohta['x'] - self.kolikko_leveys / 2 - 20), int(kohta['x'] + self.kolikko_leveys + 10),):
                            if kohta in self.rahat:
                                self.rahat.remove(kohta)
                                self.kolikot += 1
                                kolikko_aani = mixer.Sound('coin_drop.mp3')
                                kolikko_aani.play()
                        if self.kolikot >= self.voittoraja: # Ehto jolla pelaaja voittaa
                            self.teksti = "Sinä voitit :)"
                            self.peli = False # Peli päättyy
                            self.voitto = True
                        if self.hirvio_kolikot >= self.voittoraja: # Ehto jolla verottaja voittaa
                            self.peli = False
                            self.havio = True
                            self.teksti = "Verottaja voitti :("
                        if kohta['y'] > 480:
                            if kohta in self.rahat:
                                self.rahat.remove(kohta) # Näytöltä poistunut kolikko poistetaan listalta

                if not self.peli: # Jos peli päättyy näytölle jää kolikot, hirviöt ja tekstit
                    self.tulosta_lopputilanne() # Tulostaan näytön keskelle kumpi voitti
                    

                self.tulosta_tiedot() # Kutsuu metodia, joka tulsotaan tiedot näytölle

                self.generoi_uusi_kolikko() # Mutsutaan metodia joka, luo uuden kolikon listaan
                if len(self.rahat) >= 3: # Hirviöitä luovaa metodia aletaan kutsua kun näytöllä on vähintään kolme kolikkoa
                    self.generoi_uusi_hirvio() # Kutsuu metodia
                

                pygame.display.flip() # Päivittää näytön
                self.kello.tick(60) # Luonnollinen nopeus peliin

    

# Kutsutaan peli käyntiin
if __name__ == "__main__":
    
    peli = Mahtijahti()
    peli.aloitus()
    