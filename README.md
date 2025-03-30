## Digital rain

Zadanie omawiane podczas pierwszej lekcji kursu:
Wstęp do programowania i języka Python - sekurak 21.03.2025
Prowadzący: Gynvael Coldwind

Zadanie polega na napisaniu programu który imituje efekt znany z filmu Matrix.
Jako inspiracja przykładowa animacja dostępna na Wikipedia.

[https://en.wikipedia.org/wiki/Digital_rain](https://en.wikipedia.org/wiki/Digital_rain)
![An interpretation of digital rain - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/c/cc/Digital_rain_animation_medium_letters_shine.gif)
[by:Jahobr (CC0)](https://commons.wikimedia.org/wiki/User:Jahobr)

Zadanie zostało napisane na podstawie lekcji z podstaw programowania w języku Python, jego celem było przećwiczenie umiejętności zdobytych podczas kursu.
Obiektowe podejście zastosowane podczas rozwiązywania zadania wykracza poza zakres szkolenia i było dodatkowym auto-wyzwaniem autora. Jest to pierwszy program zrealizowany za pomocą takiego podejścia przez autora.

Efekt osiągnięty za pomocą tego programu jest delikatnie zmodyfikowany pod preferencje autora (kolor, losowe pogróbianie liter).
Kod który przedstawia zadowalający efekt uwzględniający losowość co do prędkości spadania kropli, czasu ich zanikania, ich ilości i długości powstał w około ~8h.

Aby przetestować działanie programu, należy uruchomić terminal w miejscu z projektem, i użyć komendy:

```python
python3 matrix.py
```

Znane problemy wynikające z niekompatybilnego środowiska, to brak obsługi kodów ANSI i/lub brak kolorów i odpowiedniego kodowania/czcionki w terminalu.
