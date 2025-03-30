import random
import time

W, H = 78, 38
droplet_odds_draws = 4
droplet_odds = 0.8
bold_char_odds = 0.1
fade_from = 2
fade_to = 40
frames =  30


# katakana
CHARSET = [chr(x) for x in range(0x30a1, 0x30fb)]
# szerokie cyfry
CHARSET += [chr(x) for x in range(0xFF10, 0xFF1A)]
# serokie wielkie litery
CHARSET += [chr(x) for x in range(0xFF21, 0xFF3B)]
# szerokie małe litery
CHARSET += [chr(x) for x in range(0xFF41, 0xFF5B)]
# kilka innych szerokich znaków
CHARSET += [chr(x) for x in range(0xFF01, 0xFF0F)]
# szeroka spacja
WIDE_SPACE = '\u3000'

# CHARSET += [chr(x) for x in range(0x41, 0x5B)]
# CHARSET += [chr(x) for x in range(0x61, 0x7B)]
# CHARSET += [
#     '!','@','#','$','%','^','&','*','(',')','_','-','=','+','[',']','{','}',';',
#     ':','"','\\','|',',','<','.','>','/','?',"\'",'`','~'
#     ]
# # CHARSET += [chr(x) for x in range(0x__, 0x__)]
# WIDE_SPACE = ' '


def color(volume):
    if volume >= 128:
        r = (volume - 128) * 2
        g = 255
        b = (volume - 128) * 2
    else:
        r = volume * 2
        g = volume * 2
        b = 0
    # nie zerowa szansa na pogróbienie
    bold = ''
    if random.random() < bold_char_odds:
        bold = '1;'
    return f"\033[{bold}38;2;{r};{g};{b}m"

class Droplet:
    def __init__(self, col, speed, fade, row, volume, ch):
        self.col = col
        self.speed = speed
        self.fade = fade
        self.row = row
        self.volume = volume
        self.ch = ch
        self.head = True # tworzenie nowej kropli

    def clone(self):
        new_row = self.row + 1
        new_volume = 255
        new_ch =  CHARSET[random.randint(0, len(CHARSET) - 1)]
        return Droplet(self.col, self.speed, self.fade, new_row , new_volume, new_ch)

    def update(self):
        self.volume -= self.fade
        if self.volume <= 0:
            self.ch = WIDE_SPACE

    def colored_char(self):
        if self.ch == WIDE_SPACE:
            return WIDE_SPACE
        return f"{color(self.volume)}{self.ch}\033[0m"

    def is_dead(self):
        return self.row > H or self.volume <= 0

def update_matrix(droplet):
    matrix[droplet.row][droplet.col] = droplet.colored_char()

matrix = [[WIDE_SPACE for _ in range(W)] for _ in range(H)]
droplets = []


try:
    while True:
        '''
        Tworzenie nowych kropli jest później, najpierw trzeba zarządzić tymi co już są
        (jak nie ma) to nic nie zrobi i przejdzie do losowania czy stworzyć nową krople
        a na samym końcu trzeba zaktualizować macierz i ją wyświetlić

        TODO:   Dodać sprawdzanie jakiej szerokości i wysokości mamy okno terminala żeby
                dobrać szerokość i wysokość efektu
        '''
        if droplets:
            '''
            Istnieje choć jedna kropla więc trzeba ją zaktualizować stworzyć na jej podstawie
            kolejne pod nią, lub jeśli wyparowała albo skapnęła z okna to ją usunąć z listy

            Jeśli jest to kropla nowa lub najniższy punkt całej strugi to trzeba ją skopiować
            i późńiej odświerzyć jej parametry, jeśli nie to można ją tylko
            odświerzać (metoda .update())
            '''
            cloned_droplets = []
            for droplet in droplets:
                if droplet.head and droplet.row < H:
                    droplet.head = False
                    cloned_droplets.append(droplet.clone())
                    '''
                    klonujemy ją - a ma to do siebie to że przejmujemy istotne parametry całej strugi
                    (kolumne, prędkość płynięcia i zanikanie) ale nowa kropla ma pełne nasycenie
                    koloru, jest o wiersz niżej i ma nowy wylosowany znak - metoda .clone
                    a stara kropla ta którą kopiowaliśmy przestaje być końcówką strugi (.head = False)
                    '''
                droplet.update()
            '''
            skoro mamy sprawdzone i zaktualizowane wszystkie krople i te które należało sklonować są na nowej liście to teraz tą liste trzeba dodać do listy wszystkich kropli
            '''
            droplets.extend(cloned_droplets)

        '''
        Dodatkowo jest nie zerowa szansa że powstanie nowa kropla
        '''
        for _ in range(int(droplet_odds_draws)):
            if random.random() < droplet_odds:
                col = random.randint(0, W - 1)
                speed = 1 + random.random() * 2
                fade = random.randint(fade_from, fade_to)
                row = 0
                volume = 255
                ch = CHARSET[random.randint(0, len(CHARSET) - 1)]

                droplets.append(Droplet(col, speed, fade, row, volume, ch))

        '''
        wszelkie krople które są jeszcze na oknie należy teraz wypisać do macierzy a po wypisaniu te,
        które już odparowały, skapnęły z okna to usunąć
        '''
        for droplet in droplets:
            if not droplet.row >= H:
                update_matrix(droplet)
            if droplet.is_dead():
                droplets.remove(droplet)

        # Wyświetlanie macierzy
        print("\033[H\033[J", end="")  # Czyść ekran w terminalu
        for row in matrix:
            print(''.join(row))

        time.sleep(1/frames)

except (KeyboardInterrupt, SystemExit):
    print()
