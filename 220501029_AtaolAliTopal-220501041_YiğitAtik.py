import pygame
import sys
import numpy as np
from queue import PriorityQueue, Queue


pygame.init()


HÜCRE_BOYUTU = 50
PENCERE_GENİŞLİĞİ = 700
PENCERE_YÜKSEKLİĞİ = 550
FPS = 30


BEYAZ = (255, 255, 255)
SİYAH = (0, 0, 0)
KIRMIZI = (255, 0, 0)
YEŞİL = (0, 255, 0)
MAVİ = (0, 0, 255)
SARI = (255, 255, 0)
GRİ = (128, 128, 128)


screen = pygame.display.set_mode((PENCERE_GENİŞLİĞİ, PENCERE_YÜKSEKLİĞİ))
pygame.display.set_caption("Star Wars Labirent Oyunu")
clock = pygame.time.Clock()


class Konum:
    def __init__(self, x, y):
        self.x = x  
        self.y = y  
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, new_x):
        self.x = new_x
    
    def setY(self, new_y):
        self.y = new_y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


class Karakter:
    def __init__(self, name, char_type, konum):
        self.name = name
        self.char_type = char_type
        self.konum = konum
        self.image = None  
    
    def getAd(self):
        return self.name
    
    def setAd(self, name):
        self.name = name
    
    def getTur(self):
        return self.char_type
    
    def setTur(self, char_type):
        self.char_type = char_type
    
    def getKonum(self):
        return self.konum
    
    def setKonum(self, konum):
        self.konum = konum
    
    def enKısaYol(self, labirent, hedefKonum):
        
        pass
    
    def draw(self, screen):
        
        x = self.konum.getY() * HÜCRE_BOYUTU
        y = self.konum.getX() * HÜCRE_BOYUTU
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, KIRMIZI, (x, y, HÜCRE_BOYUTU, HÜCRE_BOYUTU))


class LukeSkywalker(Karakter):
    def __init__(self, konum):
        super().__init__("Luke Skywalker", "İyi", konum)
        
        self.image = pygame.Surface((HÜCRE_BOYUTU, HÜCRE_BOYUTU))
        self.image.fill(YEŞİL)
        self.can = 3
    
    def getCan(self):
        return self.can
    
    def setCan(self, can):
        self.can = can
    
    def can_kaybet(self):
        self.can -= 1
        return self.can <= 0  

class MasterYoda(Karakter):
    def __init__(self, konum):
        super().__init__("Master Yoda", "İyi", konum)
        
        self.image = pygame.Surface((HÜCRE_BOYUTU, HÜCRE_BOYUTU))
        self.image.fill(MAVİ)
        self.can = 6  
    
    def getCan(self):
        return self.can
    
    def setCan(self, can):
        self.can = can
    
    def can_kaybet(self):
        self.can -= 0.5  
        return self.can <= 0  


class Stormtrooper(Karakter):
    def __init__(self, konum):
        super().__init__("Stormtrooper", "Kötü", konum)
        
        self.image = pygame.Surface((HÜCRE_BOYUTU, HÜCRE_BOYUTU))
        self.image.fill(KIRMIZI)
    
    def enKısaYol(self, labirent, hedefKonum):
        xs, ys = len(labirent), len(labirent[0])
        queue = Queue()
        queue.put((self.konum.getX(), self.konum.getY()))
        gidilmiş = set([(self.konum.getX(), self.konum.getY())])
        ana = {(self.konum.getX(), self.konum.getY()): None}
        
        yönler = [(1, 0), (0, 1), (-1, 0), (0, -1)]  
        
        while not queue.empty():
            anlıkX, anlıkY = queue.get()
            
            
            if anlıkX == hedefKonum.getX() and anlıkY == hedefKonum.getY():
                break
                
            for dr, dc in yönler:
                nr, nc = anlıkX + dr, anlıkY + dc
                
                
                if (0 <= nr < xs and 0 <= nc < ys and 
                    labirent[nr][nc] == 1 and (nr, nc) not in gidilmiş):
                    queue.put((nr, nc))
                    gidilmiş.add((nr, nc))
                    ana[(nr, nc)] = (anlıkX, anlıkY)
        
        
        yol = []
        anlıkKonum = (hedefKonum.getX(), hedefKonum.getY())
        
        if anlıkKonum not in ana:  
            return [], float('inf')
            
        while anlıkKonum:
            yol.append(anlıkKonum)
            anlıkKonum = ana[anlıkKonum]
            
        yol.reverse()
        
        
        if len(yol) > 1:
            sıradakiHamle = Konum(yol[1][0], yol[1][1])
            return yol, len(yol) - 1
        else:
            return yol, float('inf')

class DarthVader(Karakter):
    def __init__(self, konum):
        super().__init__("Darth Vader", "Kötü", konum)
        
        self.image = pygame.Surface((HÜCRE_BOYUTU, HÜCRE_BOYUTU))
        self.image.fill((0, 0, 0))  
    
    def enKısaYol(self, labirent, hedefKonum):
        xs, ys = len(labirent), len(labirent[0])
        
        
        modifiedLabirent = [[1 for _ in range(ys)] for _ in range(xs)]
        
        queue = PriorityQueue()
        queue.put((0, (self.konum.getX(), self.konum.getY())))
        gidilmiş = set()
        ana = {(self.konum.getX(), self.konum.getY()): None}
        mesafe = {(self.konum.getX(), self.konum.getY()): 0}
        
        yönler = [(1, 0), (0, 1), (-1, 0), (0, -1)]  
        
        while not queue.empty():
            dist, (anlıkX, anlıkY) = queue.get()
            
            if (anlıkX, anlıkY) in gidilmiş:
                continue
                
            gidilmiş.add((anlıkX, anlıkY))
            
            
            if anlıkX == hedefKonum.getX() and anlıkY == hedefKonum.getY():
                break
                
            for dr, dc in yönler:
                nr, nc = anlıkX + dr, anlıkY + dc
                
                
                if 0 <= nr < xs and 0 <= nc < ys and modifiedLabirent[nr][nc] == 1:
                    new_dist = dist + 1
                    
                    if (nr, nc) not in mesafe or new_dist < mesafe[(nr, nc)]:
                        mesafe[(nr, nc)] = new_dist
                        ana[(nr, nc)] = (anlıkX, anlıkY)
                        queue.put((new_dist, (nr, nc)))
        
        
        yol = []
        anlıkKonum = (hedefKonum.getX(), hedefKonum.getY())
        
        if anlıkKonum not in ana:  
            return [], float('inf')
            
        while anlıkKonum:
            yol.append(anlıkKonum)
            anlıkKonum = ana[anlıkKonum]
            
        yol.reverse()
        
        
        if len(yol) > 1:
            sıradakiHamle = Konum(yol[1][0], yol[1][1])
            return yol, len(yol) - 1
        else:
            return yol, float('inf')

class KyloRen(Karakter):
    def __init__(self, konum):
        super().__init__("Kylo Ren", "Kötü", konum)
        
        self.image = pygame.Surface((HÜCRE_BOYUTU, HÜCRE_BOYUTU))
        self.image.fill((128, 0, 0))  
    
    def enKısaYol(self, labirent, hedefKonum):
        xs, ys = len(labirent), len(labirent[0])
        queue = Queue()
        queue.put((self.konum.getX(), self.konum.getY()))
        gidilmiş = set([(self.konum.getX(), self.konum.getY())])
        ana = {(self.konum.getX(), self.konum.getY()): None}
        
        
        yönler = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  
            (2, 0), (0, 2), (-2, 0), (0, -2)   
        ]
        
        while not queue.empty():
            anlıkX, anlıkY = queue.get()
            
            
            if anlıkX == hedefKonum.getX() and anlıkY == hedefKonum.getY():
                break
                
            for dr, dc in yönler:
                nr, nc = anlıkX + dr, anlıkY + dc
                
                
                if abs(dr) == 2 or abs(dc) == 2:
                    
                    ir, ic = anlıkX + dr//2, anlıkY + dc//2
                    if not (0 <= ir < xs and 0 <= ic < ys and labirent[ir][ic] == 1):
                        continue
                
                
                if (0 <= nr < xs and 0 <= nc < ys and 
                    labirent[nr][nc] == 1 and (nr, nc) not in gidilmiş):
                    queue.put((nr, nc))
                    gidilmiş.add((nr, nc))
                    ana[(nr, nc)] = (anlıkX, anlıkY)
        
        
        yol = []
        anlıkKonum = (hedefKonum.getX(), hedefKonum.getY())
        
        if anlıkKonum not in ana:  
            return [], float('inf')
            
        while anlıkKonum:
            yol.append(anlıkKonum)
            anlıkKonum = ana[anlıkKonum]
            
        yol.reverse()
        
        
        if len(yol) > 1:
            sıradakiHamle = Konum(yol[1][0], yol[1][1])
            
            mesafe = (len(yol) - 1) // 2 + (len(yol) - 1) % 2
            return yol, mesafe
        else:
            return yol, float('inf')

class Oyun:
    def __init__(self):
        self.labirent = []
        self.oyuncu = None
        self.düşmanlar = []
        self.ödülKonumu = Konum(9, 13)  
        self.gameOver = False
        self.kazanıldı = False
        self.seçilmişKarakter = None
        
        
        self.haritayıYükle("Star wars harita.txt")
        
        
        self.oyuncuBaşlangıcı = Konum(5, 6)
        
        
        self.kapılar = {
            'A': Konum(5, 0),   
            'B': Konum(9, 13),  
            'C': Konum(10, 4)   
        }
        
    def haritayıYükle(self, filename):
        try:
            with open(filename, 'r') as file:
                
                self.düşmanlar = []
                line = file.readline().strip()
                while line.startswith('Karakter:'):
                    parçalar = line.split(',')
                    düşmanTürü = parçalar[0].split(':')[1]
                    kapı = parçalar[1].split(':')[1]
                    
                    
                    düşmanKonumu = None
                    if kapı == 'A':
                        düşmanKonumu = Konum(5, 0)  
                    elif kapı == 'B':
                        düşmanKonumu = Konum(9, 13)  
                    elif kapı == 'C':
                        düşmanKonumu = Konum(10, 4)  
                    
                    if düşmanKonumu:
                        if düşmanTürü == 'Stormtrooper':
                            self.düşmanlar.append(Stormtrooper(düşmanKonumu))
                        elif düşmanTürü == 'DarthVader':
                            self.düşmanlar.append(DarthVader(düşmanKonumu))
                        elif düşmanTürü == 'KyloRen':
                            self.düşmanlar.append(KyloRen(düşmanKonumu))
                    
                    line = file.readline().strip()
                
                
                self.labirent = []
                while line:
                    if not line.startswith('Karakter:'):
                        x = [int(cell) for cell in line.split('\t')]
                        self.labirent.append(x)
                    line = file.readline().strip()
                
        except Exception as e:
            print(f"Haritayı yüklerken hata: {e}")
            sys.exit(1)
    
    def karakterSeç(self, choice):
        if choice == 1:  
            self.oyuncu = LukeSkywalker(Konum(self.oyuncuBaşlangıcı.getX(), self.oyuncuBaşlangıcı.getY()))
        else:  
            self.oyuncu = MasterYoda(Konum(self.oyuncuBaşlangıcı.getX(), self.oyuncuBaşlangıcı.getY()))
        self.seçilmişKarakter = True
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if not self.seçilmişKarakter:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.karakterSeç(1)  
                    elif event.key == pygame.K_2:
                        self.karakterSeç(2)  
            elif not self.gameOver and not self.kazanıldı:
                if event.type == pygame.KEYDOWN:
                    self.oyuncuyuHareketEttir(event.key)
        
        return True
    
    def oyuncuyuHareketEttir(self, key):
        x, y = self.oyuncu.getKonum().getX(), self.oyuncu.getKonum().getY()
        new_x, new_y = x, y
        
        
        if key == pygame.K_UP:
            new_x = x - 1  
        elif key == pygame.K_DOWN:
            new_x = x + 1  
        elif key == pygame.K_LEFT:
            new_y = y - 1  
        elif key == pygame.K_RIGHT:
            new_y = y + 1  
            
        
        if (0 <= new_x < len(self.labirent) and 0 <= new_y < len(self.labirent[0]) and 
            self.labirent[new_x][new_y] == 1):
            self.oyuncu.setKonum(Konum(new_x, new_y))
            
            
            if new_x == self.ödülKonumu.getX() and new_y == self.ödülKonumu.getY():
                self.kazanıldı = True
                return
            
            
            self.düşmanlarıHareketEttir()
            
            
            self.çarpışmalarıKontrolEt()
    
    def düşmanlarıHareketEttir(self):
        for düşman in self.düşmanlar:
            yol, mesafe = düşman.enKısaYol(self.labirent, self.oyuncu.getKonum())
            if yol and len(yol) > 1:
                düşman.setKonum(Konum(yol[1][0], yol[1][1]))
    
    def çarpışmalarıKontrolEt(self):
        for düşman in self.düşmanlar:
            if (düşman.getKonum().getX() == self.oyuncu.getKonum().getX() and 
                düşman.getKonum().getY() == self.oyuncu.getKonum().getY()):
                gameOver = self.oyuncu.can_kaybet()
                if gameOver:
                    self.gameOver = True
                else:
                    
                    self.oyuncu.setKonum(Konum(self.oyuncuBaşlangıcı.getX(), self.oyuncuBaşlangıcı.getY()))
    
    def draw(self):
        screen.fill(BEYAZ)
        
        
        for i in range(len(self.labirent)):
            for j in range(len(self.labirent[0])):
                if self.labirent[i][j] == 0:
                    pygame.draw.rect(screen, SİYAH, (j * HÜCRE_BOYUTU, i * HÜCRE_BOYUTU, HÜCRE_BOYUTU, HÜCRE_BOYUTU))
                else:
                    pygame.draw.rect(screen, BEYAZ, (j * HÜCRE_BOYUTU, i * HÜCRE_BOYUTU, HÜCRE_BOYUTU, HÜCRE_BOYUTU), 1)
        
        
        pygame.draw.rect(screen, SARI, 
                        (self.oyuncuBaşlangıcı.getY() * HÜCRE_BOYUTU, 
                         self.oyuncuBaşlangıcı.getX() * HÜCRE_BOYUTU, 
                         HÜCRE_BOYUTU, HÜCRE_BOYUTU), 3)
        
        
        for kapıAdı, kapıKonumu in self.kapılar.items():
            pygame.draw.rect(screen, MAVİ, 
                           (kapıKonumu.getY() * HÜCRE_BOYUTU, 
                            kapıKonumu.getX() * HÜCRE_BOYUTU, 
                            HÜCRE_BOYUTU, HÜCRE_BOYUTU), 3)
        
        
        pygame.draw.rect(screen, YEŞİL, 
                        (self.ödülKonumu.getY() * HÜCRE_BOYUTU, 
                         self.ödülKonumu.getX() * HÜCRE_BOYUTU, 
                         HÜCRE_BOYUTU, HÜCRE_BOYUTU), 3)
        
        
        if self.oyuncu:
            self.oyuncu.draw(screen)
            
            
            font = pygame.font.SysFont(None, 36)
            canMetni = font.render(f"Can: {self.oyuncu.getCan()}", True, KIRMIZI)
            screen.blit(canMetni, (10, 10))
            
            
            adMetni = font.render(f"Karakter: {self.oyuncu.getAd()}", True, YEŞİL)
            screen.blit(adMetni, (200, 10))
        
        
        for düşman in self.düşmanlar:
            düşman.draw(screen)
            
            
            if self.oyuncu:
                yol, mesafe = düşman.enKısaYol(self.labirent, self.oyuncu.getKonum())
                
                
                for i in range(1, len(yol)-1):
                    x, y = yol[i]
                    pygame.draw.rect(screen, (255, 200, 200), 
                                    (y * HÜCRE_BOYUTU + 10, x * HÜCRE_BOYUTU + 10, 
                                     HÜCRE_BOYUTU - 20, HÜCRE_BOYUTU - 20))
                
                
                font = pygame.font.SysFont(None, 20)
                mesafeMetni = font.render(f"{düşman.getAd()}: {mesafe} adım", True, MAVİ)
                screen.blit(mesafeMetni, (550, 10 + self.düşmanlar.index(düşman) * 30))
        
        
        if self.gameOver:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, KIRMIZI)
            screen.blit(text, (PENCERE_GENİŞLİĞİ//2 - text.get_width()//2, PENCERE_YÜKSEKLİĞİ//2 - text.get_height()//2))
        elif self.kazanıldı:
            font = pygame.font.SysFont(None, 72)
            text = font.render("KAZANDIN!", True, YEŞİL)
            screen.blit(text, (PENCERE_GENİŞLİĞİ//2 - text.get_width()//2, PENCERE_YÜKSEKLİĞİ//2 - text.get_height()//2))
        elif not self.seçilmişKarakter:
            font = pygame.font.SysFont(None, 36)
            text1 = font.render("Karakterini seç:", True, MAVİ)
            text2 = font.render("1 - Luke Skywalker (3 can)", True, SARI)
            text3 = font.render("2 - Master Yoda (yakalanınca yarı can gider)", True, YEŞİL)
            screen.blit(text1, (PENCERE_GENİŞLİĞİ//2 - text1.get_width()//2, PENCERE_YÜKSEKLİĞİ//2 - 80))
            screen.blit(text2, (PENCERE_GENİŞLİĞİ//2 - text2.get_width()//2, PENCERE_YÜKSEKLİĞİ//2 - 30))
            screen.blit(text3, (PENCERE_GENİŞLİĞİ//2 - text3.get_width()//2, PENCERE_YÜKSEKLİĞİ//2 + 20))
    
    def run(self):
        running = True
        
        while running:
            running = self.handleEvents()
            self.draw()
            
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Oyun()
    game.run()