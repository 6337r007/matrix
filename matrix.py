'''
Animacja "digital rain" do kursu:
Wstęp do programowania i języka Python by sekurak
prowadzący Gynvael Coldwind

Autor: Krystian Kaczmarek
Data: 30.03.2025
'''

import random
import time

W, H = 40, 40 # szerokość, wysokość
droplet_odds_draws = 3 # ilość losowań
droplet_odds = 0.2 # prawdopodobieństwo powstania nowej kropli
speed_odds_from = 1 # prędkość spadania w ramkach na znak (najszybciej)
speed_odds_to = 3 # prędkość spadania w ramkach na znak (najwolniej)
bold_char_odds = 0.05 # szansa na pogróbienie znaku
fade_from = 4 # prędkość zanikania kropli w znakach na odświeżenie ekranu (najwolniej)
fade_to = 30 # prędkość zanikania kropli w znakach na odświeżenie ekranu (najszybciej)
frames =  70 # ilość ramek na sekundę
yellow = True # ogon kropli w kolorze żółtym


CHARSET = [chr(x) for x in range(0x30A1, 0x30FB)] # katakana
CHARSET += [chr(x) for x in range(0xFF10, 0xFF1A)] # szerokie cyfry
CHARSET += [chr(x) for x in range(0xFF21, 0xFF3B)] # szerokie wielkie litery
CHARSET += [chr(x) for x in range(0xFF41, 0xFF5B)] # szerokie małe litery
CHARSET += [chr(x) for x in range(0xFF01, 0xFF0F)] # kilka innych szerokich znaków
WIDE_SPACE = '\u3000' # szeroka spacja

def color(volume):
    '''
    Generuje kod ANSI dla koloru znaku, w zależności od wartości volume
    '''
    if volume >= 128:
        r = (volume - 128) * 2
        g = 255
        b = (volume - 128) * 2
    else:
        if yellow:
            r = volume * 2
        else:
            r = 0
        g = volume * 2
        b = 0
    # nie zerowa szansa na pogróbienie
    bold = ''
    if random.random() < bold_char_odds:
        bold = '1;'
    return f"\033[{bold}38;2;{r};{g};{b}m"

class Droplet:
    '''
    Klasa reprezentująca pojedynczą kroplę w "deszczu znaków".
    Kropla klonuje się w dół do nowej kropli i stopniowo zanika.
    '''
    def __init__(self, col, speed, fade, row, volume, ch):
        '''
        Inicjalizacja nowej kropli.
        '''
        self.col = col
        self.speed = speed
        self.speed_countdown = speed
        self.fade = fade
        self.row = row
        self.volume = volume
        self.ch = ch
        self.head = True # tworzenie nowej kropli

    def clone(self):
        '''
        Klonowanie aktualnej kropli do nowej w wierszu niżej.
        '''
        new_row = self.row + 1
        new_volume = 255
        new_ch =  CHARSET[random.randint(0, len(CHARSET) - 1)]
        return Droplet(self.col, self.speed, self.fade, new_row , new_volume, new_ch)

    def update(self):
        '''
        Zmiana intensywności koloru kropli (zanikanie).
        '''
        self.volume -= self.fade
        if self.volume <= 0:
            self.ch = WIDE_SPACE

    def countdown(self):
        '''
        Odliczanie ramek do kolejnego ruchu kropli (klonowania).
        '''
        self.speed_countdown -= 1

    def restart_count(self):
        '''
        Reset licznika do odliczania ramek do kolejnego ruchu kropli (klonowania).
        '''
        self.speed_countdown = self.speed

    def colored_char(self):
        '''
        Zwraca znak kropli z odpowiednim kodem ANSI dla koloru.
        '''
        if self.ch == WIDE_SPACE:
            return WIDE_SPACE
        return f"{color(self.volume)}{self.ch}\033[0m"

    def is_dead(self):
        '''
        Sprawdza czy kropla opuści ekran, lub całkowicie zanikła.
        '''
        return self.row > H or self.volume <= 0

def update_matrix(droplet):
    '''
    Zapisuje konkretną krople w odpowiednie miejsce macierzy (ekranu).
    '''
    matrix[droplet.row][droplet.col] = droplet.colored_char()

# Macierz ekranu
matrix = [[WIDE_SPACE for _ in range(W)] for _ in range(H)]
droplets = []

try:
    while True:
        # Aktualizacja istniejących kropli.
        '''
        TODO:   Dodać sprawdzanie jakiej szerokości i wysokości mamy okno terminala żeby
                dobrać szerokość, wysokość i inne parametry efektu.
        '''
        if droplets:
            cloned_droplets = []
            for droplet in droplets:
                # Kropla jest modyfikowana co zdefiniowaną ilość ramek (odświerzeń ekranu).
                if droplet.speed_countdown != 0:
                    droplet.countdown()
                else:
                    droplet.restart_count()

                    # Jeśli kropla jest najniżej w kolumnie to klonujemy ją do nowej poniżej.
                    if droplet.head and droplet.row < H:
                        droplet.head = False
                        cloned_droplets.append(droplet.clone())

                    droplet.update()

            # Dodawanie sklonowanych kropli do listy.
            droplets.extend(cloned_droplets)

        # Losowe tworzenie nowych kropli.
        for _ in range(int(droplet_odds_draws)):
            if random.random() < droplet_odds:
                col = random.randint(0, W - 1)
                speed = random.randint(speed_odds_from, speed_odds_to)
                fade = random.randint(fade_from, fade_to)
                row = 0
                volume = 255
                ch = CHARSET[random.randint(0, len(CHARSET) - 1)]

                droplets.append(Droplet(col, speed, fade, row, volume, ch))

        # Aktualizacja macierzy i usówanie "martwych" kropli.
        for droplet in droplets:
            if not droplet.row >= H:
                update_matrix(droplet)
            if droplet.is_dead():
                droplets.remove(droplet)

        # Czyszczenie ekranu i wyświetlanie macierzy ekranu (nowej ramki).
        print("\033[H\033[J", end="")  # Kod ANSI - czyść ekran
        for element in matrix:
            print(''.join(element))

        time.sleep(1/frames)

except (KeyboardInterrupt, SystemExit):
    print()
