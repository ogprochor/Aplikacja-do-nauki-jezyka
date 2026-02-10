import random
import json



class Slowo:
    def __init__(self, tekst: str, tlumaczenia: list, poziom_trudnosci):
        self.tekst = tekst
        self.tlumaczenia = tlumaczenia
        self.kategorie = []
        self.poziom_trudnosci = poziom_trudnosci

    def dodaj_kategorie(self, kategoria):
        self.kategorie.append(kategoria)

    def usun_kategorie(self, kategoria):
        self.kategorie.remove(kategoria)

    def get_tekst(self):
        return self.tekst

    def get_kategorie(self):
        return self.kategorie

    def notify_observer(self, poprawna_odpowiedz: bool):
        self.poziom_trudnosci.update(self, poprawna_odpowiedz)

    def get_trudnosc(self):
        return self.poziom_trudnosci

    def __str__(self):
        kategorie_str = ', '.join([i.nazwa for i in self.get_kategorie()])
        return f"Słowo: {self.tekst}, Tłumaczenia: {self.tlumaczenia}, Kategoria: {kategorie_str}, Poziom trudności: {self.poziom_trudnosci.get_trudnosc()}"


class DifficultyState:
    def __init__(self):
        self.poziom = "trudny"

    def update(self, slowo, poprawna_odpowiedz: bool):
        if poprawna_odpowiedz:
            print(f"Poprawna odpowiedź dla słowa: {slowo.tekst}")
            self.zmniejsz_trudnosc()

        else:
            print(f"Błędna odpowiedź dla słowa: {slowo.tekst}")
            self.zwieksz_trudnosc()

    def zwieksz_trudnosc(self):
        if self.poziom == "łatwy":
            self.poziom = "średni"

        elif self.poziom == "średni":
            self.poziom = "trudny"

    def zmniejsz_trudnosc(self):
        if self.poziom == "trudny":
            self.poziom = "średni"

        elif self.poziom == "średni":
            self.poziom = "łatwy"

    def get_trudnosc(self):
        return self.poziom


class DifficultyObserver:
    def __init__(self):
        self.obserwowane_slowa = []

    def dolacz(self, slowo: Slowo):
        if slowo not in self.obserwowane_slowa:
            self.obserwowane_slowa.append(slowo)

    def odlacz(self, slowo: Slowo):

        if slowo in self.obserwowane_slowa:
            self.obserwowane_slowa.remove(slowo)

    def powiadom(self, slowo: Slowo, poprawna_odpowiedz: bool):

        if slowo in self.obserwowane_slowa:
            slowo.notify_observer(poprawna_odpowiedz)


class Kategoria:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.slowa = []
        self.podkategorie = []

    def dodajSlowo(self, slowo):
        self.slowa.append(slowo)
        slowo.dodaj_kategorie(self)

    def usunKategorie(self, slowo):
        if slowo in self.slowa:
            self.slowa.remove(slowo)

    def dodajKategorie(self, kategoria):
        self.podkategorie.append(kategoria)

    def zwrocIlosc(self):
        return len(self.slowa)

    def __str__(self):
        return f"Kategoria: {self.nazwa}, Liczba słów: {len(self.slowa)}, Podkategorie: {self.podkategorie}"


class SlowoBuilder:
    def __init__(self):
        self.tekst = None
        self.tlumaczenia = []
        self.kategorie = []
        self.poziom_trudnosci = None

    def ustawTekst(self, tekst):
        self.tekst = tekst

        return self

    def dodajTlumaczenie(self, tlumaczenie):
        self.tlumaczenia.append(tlumaczenie)

        return self

    def dodajKategorie(self, kategoria):
        self.kategorie.append(kategoria)

        return self

    def ustawTrudnosc(self, poziom_trudnosci):
        self.poziom_trudnosci = poziom_trudnosci

        return self

    def build(self):
        if self.poziom_trudnosci is None:
            self.poziom_trudnosci = DifficultyState()

        return Slowo(self.tekst, self.tlumaczenia, self.poziom_trudnosci)

    def __str__(self):
        return f"Słowo: {self.tekst}"


class Backup:
    @staticmethod
    def zapisz_do_json(path, dane):
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(dane, json_file, ensure_ascii=False, indent=4)
        print(f"Dane zostały zapisane do pliku {path}.")

    @staticmethod
    def wczytaj_z_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as json_file:
                dane = json.load(json_file)
                print(f"Dane zostały wczytane z pliku {path}.")
                return dane
        except FileNotFoundError:
            print(f"Plik {path} nie został znaleziony.")
            return None

    @staticmethod
    def zapisz_uzytkownika(path, uzytkownik):
        dane = {
            "nazwa": uzytkownik.nazwa,
            "punkty_globalne": uzytkownik.punkty_globalne
        }
        Backup.zapisz_do_json(path, dane)

    @staticmethod
    def wczytaj_uzytkownika(path):
        dane = Backup.wczytaj_z_json(path)
        if dane:
            return dane
        else:
            print("Nie udało się wczytać danych użytkownika.")
            return None


class Uzytkownik:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.punkty_globalne = 0
        self.streak = 0
        self.max_streak = 0
        self.sciezka_pliku = f"{nazwa}_dane.json"
        self.slowa = []
        self.katalogi = {}

    def stworz_katalog(self, nazwa_katalogu: str):
        if nazwa_katalogu in self.katalogi:
            print(f"Katalog o nazwie '{nazwa_katalogu}' już istnieje.")
        else:
            self.katalogi[nazwa_katalogu] = []
            print(f"Katalog '{nazwa_katalogu}' został utworzony.")

    def dodaj_do_katalogu(self, nazwa_katalogu: str, slowa):
        if nazwa_katalogu not in self.katalogi:
            print(f"Katalog '{nazwa_katalogu}' nie istnieje.")
        else:
            if isinstance(slowa, list):
                self.katalogi[nazwa_katalogu].extend(slowa)
            elif isinstance(slowa, Slowo):
                self.katalogi[nazwa_katalogu].append(slowa)
            else:
                print(f"Nieobsługiwany typ danych: {type(slowa)}")
                return
            print(f"Słowa zostały dodane do katalogu '{nazwa_katalogu}'.")

    def pokaz_katalogi(self):

        if not self.katalogi:
            print("Brak katalogów.")
        else:
            for nazwa, slowa in self.katalogi.items():
                print(f"\nKatalog: {nazwa}")
                for slowo in slowa:
                    print(f" - {slowo.tekst}")

    def zarzadzaj_katalogami(self, slowa):
        print("\nCzy chcesz dodać słowa do katalogu?")
        print("1. Tak")
        print("2. Nie")
        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            print("\n1. Dodaj do istniejącego katalogu")
            print("2. Utwórz nowy katalog")
            pod_wybor = input("Wybierz opcję: ").strip()

            if pod_wybor == "1":
                self.pokaz_katalogi()
                nazwa_katalogu = input("\nPodaj nazwę katalogu: ").strip()
                self.dodaj_do_katalogu(nazwa_katalogu, slowa)

            elif pod_wybor == "2":
                nazwa_katalogu = input("\nPodaj nazwę nowego katalogu: ").strip()
                self.stworz_katalog(nazwa_katalogu)
                self.dodaj_do_katalogu(nazwa_katalogu, slowa)

            else:
                print("Nieprawidłowy wybór.")
        else:
            print("Słowa nie zostaną dodane do żadnego katalogu.")

    def stworz_nowego_uzytkownika(self, slowa):
        self.slowa = slowa
        self.zapisz_stan()
        print(f"Użytkownik '{self.nazwa}' został stworzony i zapisany do {self.sciezka_pliku}.")

    def wczytaj_uzytkownika(self):
        dane = Backup.wczytaj_uzytkownika(self.sciezka_pliku)
        if dane:
            try:
                self.nazwa = dane["nazwa"]
                self.punkty_globalne = dane["punkty_globalne"]
                self.streak = dane.get("streak", 0)
                self.max_streak = dane.get("max_streak", 0)
                self.slowa = [
                    SlowoBuilder()
                    .ustawTekst(wejscie["tekst"])
                    .dodajTlumaczenie(wejscie["tlumaczenia"][0])
                    .ustawTrudnosc(DifficultyState())
                    .build()
                    for wejscie in dane["slowa"]
                ]
                print(
                    f"Użytkownik '{self.nazwa}' wczytany. Punkty: {self.punkty_globalne}, Seria: {self.streak}, Najlepsza seria: {self.max_streak}")

            except KeyError as e:
                print(f"Brakuje klucza w danych użytkownika: {e}")
        else:
            print("Nie udało się wczytać danych użytkownika.")

    def zapisz_stan(self):
        dane = {
            "nazwa": self.nazwa,
            "punkty_globalne": self.punkty_globalne,
            "streak": self.streak,
            "max_streak": self.max_streak,
            "slowa": [
                {
                    "tekst": slowo.tekst,
                    "tlumaczenia": slowo.tlumaczenia,
                    "kategorie": [k.nazwa for k in slowo.kategorie],
                    "trudnosc": slowo.poziom_trudnosci.get_trudnosc()
                }
                for slowo in self.slowa
            ]
        }
        Backup.zapisz_do_json(self.sciezka_pliku, dane)

    def dodaj_punkty(self, punkty: int):
        self.punkty_globalne += punkty
        print(f"Użytkownik '{self.nazwa}' zdobył {punkty} punktów! Łącznie: {self.punkty_globalne}")

    def aktualizuj_streak(self, wygrana: bool):
        if wygrana:
            self.streak += 1
            if self.streak > self.max_streak:
                self.max_streak = self.streak

            print(f"Aktualna seria zwycięstw: {self.streak}. Najlepsza seria: {self.max_streak}")
        else:
            print(f"Seria zwycięstw przerwana. Twoja najlepsza seria to {self.max_streak}.")
            self.streak = 0

    def __str__(self):

        return f"Użytkownik: {self.nazwa}, Punkty globalne: {self.punkty_globalne}"


class Plik:
    def __init__(self, sciezka_slow: str, sciezka_tlumaczen: str):
        self.sciezka_slow = sciezka_slow
        self.sciezka_tlumaczen = sciezka_tlumaczen
        self.slowa = []
        self.kategoria = None
        self.kategoria_wszystkie = Kategoria("Wszystkie Słowa")
        self.kategoria_latwe = Kategoria("Łatwe")
        self.kategoria_srednie = Kategoria("Średnie")
        self.kategoria_trudne = Kategoria("Trudne")

    def wczytaj_z_pliku(self):

        nazwa_kategorii = self.sciezka_slow.split('.')[0]
        self.kategoria = Kategoria(nazwa_kategorii)

        with open(self.sciezka_slow, 'r') as plik_slow, open(self.sciezka_tlumaczen, 'r') as plik_tlumaczen:
            slowa = [linia.strip() for linia in plik_slow]
            tlumaczenia = [linia.strip() for linia in plik_tlumaczen]

            for tekst, tlumaczenie in zip(slowa, tlumaczenia):
                builder = SlowoBuilder()
                slowo = builder.ustawTekst(tekst).dodajTlumaczenie(tlumaczenie).build()

                self.slowa.append(slowo)
                self.kategoria.dodajSlowo(slowo)
                self.kategoria_wszystkie.dodajSlowo(slowo)
                self.przypisz_do_trudnosci(slowo)

    def przypisz_do_trudnosci(self, slowo: Slowo):
        trudnosc = slowo.poziom_trudnosci.get_trudnosc()
        if trudnosc == "łatwy":
            self.kategoria_latwe.dodajSlowo(slowo)
        elif trudnosc == "średni":
            self.kategoria_srednie.dodajSlowo(slowo)
        elif trudnosc == "trudny":
            self.kategoria_trudne.dodajSlowo(slowo)

    def zwroc_slowa(self):
        return self.slowa

    def zwroc_kategorie(self):
        return self.kategoria

    def zwroc_kategorie_wszystkie(self):
        return self.kategoria_wszystkie

    def zwroc_kategorie_latwe(self):
        return self.kategoria_latwe

    def zwroc_kategorie_srednie(self):
        return self.kategoria_srednie

    def zwroc_kategorie_trudne(self):
        return self.kategoria_trudne

    def losuj_slowo(self):
        if not self.slowa:
            raise ValueError("Lista słów jest pusta.")

        return random.choice(self.slowa)

    def zapisz_backup(self, path):
        Backup.zapisz_do_json(path, self.slowa)
        print(f"Backup został zapisany do {path}")

    def wczytaj_backup(self, path):
        self.slowa = Backup.wczytaj_z_json(path)
        print(f"Dane zostały przywrócone z pliku {path}.")


# =======================GRY==========================


class Gra:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.streak = 0
        self.max_streak = 0
        self.observers = []
        self.punkty = 0

    def dodaj_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def get_punkty(self):
        return self.punkty

    def dodaj_punkty(self, ilosc: int):
        self.punkty += ilosc
        print(f"Zyskałeś {ilosc} punktów! Aktualna liczba punktów: {self.punkty}")

    def zwieksz_streak(self):
        self.streak += 1
        if self.streak > self.max_streak:
            self.max_streak = self.streak
        print(f"Aktualna seria zwycięstw: {self.streak}. Najlepsza seria: {self.max_streak}")

    def reset_streak(self):
        print(f"Seria zwycięstw przerwana. Twoja najlepsza seria to {self.max_streak}.")
        self.streak = 0


class Wybory(Gra):
    def __init__(self, slowa, liczba):
        super().__init__("Wybory")
        self.slowa = slowa
        self.poprawne_odpowiedzi = 0
        self.bledne_odpowiedzi = 0
        self.rundy = 5
        self.wybrana_zmienna = liczba

        self.observer = DifficultyObserver()

        for slowo in self.slowa:
            self.observer.dolacz(slowo)

    def rozpocznij(self):
        instrukcja = "Gra Wybory polega na wyborze poprawnego tłumaczenia słowa z kilku opcji.\n(Wybierz numer odpowiadający poprawnemu tłumaczeniu)"

        print("\n\n\n---Instrukcje---")
        print("1. Wyświetl instrukcje")
        print("2. Pomin")

        wybor = input("Wybierz opcję: ")
        if wybor == "1":
            print(instrukcja)

        else:
            pass
        print("Rozpoczynamy grę w Wybory!")

        for i in range(self.rundy):
            self._runda(i, self.wybrana_zmienna)

        self.zakoncz_gre()

    def _runda(self, numer, liczba):
        slowo = self.slowa[numer]
        print(f"\nRunda {numer + 1}")
        print(f"Słowo: {slowo.tekst}")

        wszystkie_tlumaczenia = []
        if liczba == "1":
            for s in slowa_dom.zwroc_slowa():
                wszystkie_tlumaczenia.extend(s.tlumaczenia)

        if liczba == "2":
            for s in slowa_szkola.zwroc_slowa():
                wszystkie_tlumaczenia.extend(s.tlumaczenia)

        if liczba == "3":
            for s in slowa_czaswolny.zwroc_slowa():
                wszystkie_tlumaczenia.extend(s.tlumaczenia)

        wszystkie_tlumaczenia = [tlumaczenie for tlumaczenie in wszystkie_tlumaczenia if
                                 tlumaczenie != slowo.tlumaczenia[0]]

        if len(wszystkie_tlumaczenia) >= 2:
            bledne_opcje = random.sample(wszystkie_tlumaczenia, 2)
        else:
            bledne_opcje = wszystkie_tlumaczenia

        poprawna_opcja = slowo.tlumaczenia[0]

        opcje = bledne_opcje + [poprawna_opcja]
        random.shuffle(opcje)

        print("\nDostępne tłumaczenia:")
        for index, opcja in enumerate(opcje, 1):
            print(f'{index}. {opcja}')

        wybor = input("\nWybierz numer poprawnego tłumaczenia: ").strip()

        if opcje[int(wybor) - 1] == poprawna_opcja:
            print("Poprawna odpowiedź!")
            self.poprawne_odpowiedzi += 1
            self.dodaj_punkty(10)
            self.observer.powiadom(slowo, True)

        else:
            print(f"Błędna odpowiedź! Poprawne tłumaczenie to: {poprawna_opcja}")
            self.bledne_odpowiedzi += 1
            self.dodaj_punkty(-5)
            self.observer.powiadom(slowo, False)

    def zakoncz_gre(self):
        print("\nGra zakończona!")
        print(f"Poprawne odpowiedzi: {self.poprawne_odpowiedzi}")
        print(f"Błędne odpowiedzi: {self.bledne_odpowiedzi}")
        print(f"Finalna liczba punktów: {self.punkty}\n")
        print("Powrót do menu głównego...")
        print('\n')


class Fiszki(Gra):
    def __init__(self, slowa):
        super().__init__("Fiszki")
        self.slowa = slowa
        self.poprawne_odpowiedzi = 0
        self.bledne_odpowiedzi = 0

        # obserwator
        self.observer = DifficultyObserver()

        for slowo in self.slowa:
            self.observer.dolacz(slowo)

    def rozpocznij(self):
        instrukcja = "Gra w Fiszki polega na wpisaniu polskiego tlumaczenia wyświetlonego słowa.\n(Pamietaj o nie pisaniu polskich znakow w odpowiedzi)"
        print("\n\n\n---Instrukcje---")
        print("1. Wyświetl instrukcje")
        print("2. Pomin")
        opcja_uzytkownika = input("Wybierz opcję: ")
        if opcja_uzytkownika == "1":
            print(instrukcja)
        else:
            pass
        print("Rozpoczynamy grę w Fiszki!")

        for slowo in self.slowa:
            self._pokaz_slowo(slowo)

        self.zakoncz_gre()

    def _pokaz_slowo(self, slowo):

        print(f"\nSłowo po angielsku: {slowo.tekst}")
        odpowiedz = input("Podaj tłumaczenie: ").strip()

        if odpowiedz in slowo.tlumaczenia:
            print("Poprawna odpowiedź!")
            self.poprawne_odpowiedzi += 1
            self.dodaj_punkty(15)

            self.observer.powiadom(slowo, True)

        else:
            print(f"Błędna odpowiedź! Poprawne tłumaczenia to: {', '.join(slowo.tlumaczenia)}")
            self.bledne_odpowiedzi += 1
            self.dodaj_punkty(-5)

            self.observer.powiadom(slowo, False)

    def zakoncz_gre(self):

        print("\nGra zakończona!")
        print(f"Poprawne odpowiedzi: {self.poprawne_odpowiedzi}")
        print(f"Błędne odpowiedzi: {self.bledne_odpowiedzi}")
        print(f"Finalna liczba punktów: {self.punkty}\n")
        print('\n')


class Wisielec(Gra):
    def __init__(self, slowo: Slowo):
        super().__init__("Wisielec")

        self.slowo = slowo
        self.odgadniete = [" " if znak == " " else "_" for znak in self.slowo.tekst]
        self.bledy = 0
        self.max_bledow = 8
        self.uzyte_litery = []

        # obserwator
        self.observer = DifficultyObserver()
        self.observer.dolacz(slowo)

    def rozpocznij(self):
        instrukcja = "Gra wisielec polega na odgadnięciu losowego słowa po angielsku wpisuając pojedyńcze litery. \nDodatkowo masz opcje wpisania calego wyrazu a następnie odganięcie jego tłumaczenia za duzy bonus!"
        print("\n\n\n---Instrukcje---")
        print("1. Wyświetl instrukcje")
        print("2. Pomin")
        opcja_uzytkownika = input("Wybierz opcję: ")
        if opcja_uzytkownika == "1":
            print(instrukcja)
        else:
            pass
        print("Rozpoczynamy grę Wisielec!")

        while self.bledy < self.max_bledow and "_" in self.odgadniete:
            print(f"\nSłowo: {' '.join(self.odgadniete)}")
            print(f"Błędy: {self.bledy}/{self.max_bledow}")
            print(f"Użyte litery: {', '.join(self.uzyte_litery)}")

            litera = input("\nPodaj literę: ").lower()

            if litera in self.uzyte_litery:
                print("Ta litera była już użyta. Spróbuj ponownie.")
                continue

            self.uzyte_litery.append(litera)

            if litera == self.slowo.tekst:
                self.odgadniete = list(self.slowo.tekst)
                self.zakoncz_gre()
                return

            elif litera in self.slowo.tekst:
                print("Dobra odpowiedź!")

                for i, znak in enumerate(self.slowo.tekst):
                    if znak == litera:
                        self.odgadniete[i] = litera
                self.dodaj_punkty(5)


            else:
                print("Błędna odpowiedź!")
                self.bledy += 1
                self.dodaj_punkty(-5)

        self.zakoncz_gre()

    def zakoncz_gre(self):
        if "_" not in self.odgadniete:
            print(f"Brawo! Odgadłeś słowo: {self.slowo.tekst}, ale to jeszcze nie wszystko")
            print("Odgadnij tłumaczenie, a zostaniesz obdarowany bonusem punktowym!")

            wejscie = input("Podaj tłumaczenie: ")

            if wejscie in self.slowo.tlumaczenia:
                print("\n        *MEGA BIG WIN*\n")
                print("Brawo! Otrzymujesz bonus punktowy")
                self.dodaj_punkty(50)

                self.observer.powiadom(self.slowo, True)

            else:
                print("Błędne tłumaczenie, nici z bonusu")
                print(f"Tłumaczenie to: {', '.join(self.slowo.tlumaczenia)}")
                print("Za chciwość zostałeś ukarany, zabrano ci 30 punktów.")
                self.dodaj_punkty(-30)

                self.observer.powiadom(self.slowo, True)

        else:
            print(f"Przegrałeś! Słowo to: {self.slowo.tekst}")
            self.dodaj_punkty(-10)
            print(f"Tłumaczenie to: {', '.join(self.slowo.tlumaczenia)}")

            self.observer.powiadom(self.slowo, False)

        print(f"Liczba błędów: {self.bledy}/{self.max_bledow}")
        print(f"Finalna liczba punktów: {self.punkty}\n")


class Rozsypanka(Gra):
    def __init__(self, slowa: list):
        super().__init__("Rozsypanka")
        self.slowa = slowa
        self.poprawne = 0
        self.bledne = 0

        # obserwator
        self.observer = DifficultyObserver()

        for slowo in self.slowa:
            self.observer.dolacz(slowo)

    def rozpocznij(self):
        instrukcja = "Gra rozyspanka polega na ułożeniu z rozsypanych liter wyrazu po angielsku."
        print("\n\n\n---Instrukcje---")
        print("1. Wyświetl instrukcje")
        print("2. Pomin")
        opcja_uzytkownika = input("Wybierz opcję: ")
        if opcja_uzytkownika == "1":
            print(instrukcja)
        else:
            pass

        print("Rozpoczynamy grę w Rozsypankę!")

        for slowo in self.slowa:
            self._graj(slowo)

        self.zakoncz_gre()

    def _graj(self, slowo):
        wyraz = slowo.get_tekst()

        litery = list(wyraz)
        random.shuffle(litery)

        while ''.join(litery) == wyraz:
            random.shuffle(litery)

        print("Rozsypane litery:  ", ' '.join(litery))
        odpowiedz = input("Ułóż poprawne słowo:  ")

        if odpowiedz == wyraz:
            print("Poprawna odpowiedź!")
            self.poprawne += 1
            self.dodaj_punkty(18)
            self.observer.powiadom(slowo, True)
        else:
            print("Bledna odpowiedź.")
            self.bledne += 1
            self.dodaj_punkty(-5)
            self.observer.powiadom(slowo, False)

    def zakoncz_gre(self):
        print("\n\nGra zakończona!")
        print(f"Udało ci się poprawnie odpowiedzieć na {self.poprawne} pytań.")
        print(f"Niepoprawnie odpowiedziałeś na {self.bledne} pytań\n")
        print(f"Finalna liczba punktów: {self.punkty}\n")


# =======================MAIN==========================

def main():
    global slowa_szkola
    global slowa_czaswolny
    global slowa_dom
    uzytkownik = None  # wstepna inicjacja uzytkownika

    while True:
        print("--- Witaj w aplikacji do nauki słówek ---")
        print("1. Stwórz nowego użytkownika")
        print("2. Wczytaj istniejącego użytkownika")
        print("3. Zakończ program")
        print()
        opcja_uzytkownika = input("Wybierz opcję: ")

        if opcja_uzytkownika == "1":
            nazwa_uzytkownika = input("Podaj nazwę nowego użytkownika: ")
            uzytkownik = Uzytkownik(nazwa_uzytkownika)
            slowa_dom = Plik("dom.txt", "dom_tl.txt")
            slowa_dom.wczytaj_z_pliku()
            uzytkownik.stworz_nowego_uzytkownika(slowa_dom.zwroc_slowa())

        elif opcja_uzytkownika == "2":
            nazwa_uzytkownika = input("Podaj nazwę użytkownika do wczytania: ")
            uzytkownik = Uzytkownik(nazwa_uzytkownika)
            uzytkownik.wczytaj_uzytkownika()



        elif opcja_uzytkownika == "3":
            if uzytkownik is not None:
                print("\nDziękujemy za grę! Do zobaczenia!")
                print(f"Globalny wynik użytkownika '{uzytkownik.nazwa}': {uzytkownik.punkty_globalne}")

            else:
                print("\nZamykanie programu...")

            break

        else:
            print("Nieprawidłowy wybór. Kończymy program.")
            return

        slowa_dom = Plik("dom.txt", "dom_tl.txt")
        slowa_dom.wczytaj_z_pliku()

        slowa_szkola = Plik("szkola.txt", "szkola_tl.txt")
        slowa_szkola.wczytaj_z_pliku()

        slowa_czaswolny = Plik("czaswolny.txt", "czaswolny_tl.txt")
        slowa_czaswolny.wczytaj_z_pliku()

        wszystkie_slowa = []
        for i in slowa_dom.zwroc_slowa():
            wszystkie_slowa.append(i)
        for i in slowa_szkola.zwroc_slowa():
            wszystkie_slowa.append(i)
        for i in slowa_czaswolny.zwroc_slowa():
            wszystkie_slowa.append(i)




        # petla z grami i zapisem
        while True:
            print("\n--- Wybierz grę ---")
            print("1. Wybory")
            print("2. Fiszki")
            print("3. Rozsypanka")
            print("4. Wisielec")

            print("\n--- Pozostałe opcje ---")
            print("5. Zapis postępu")
            print("6. Wygeneruj raport")
            print("7. Wypisz katalogi użytkownika")
            print("8. Wyjście do wyboru użytkownika")
            wybor = input("\nWybierz opcję: ")
            slowa_z_gry = []

            if wybor == "1":
                print(f"Wybierz z jakiego katalogu chcesz brać słowa:")
                print("1. Dom i przedmioty domowe.")
                print("2. Szkola i przedmioty związane ze szkołą.")
                print("3. Czas wolny i zajęcia.")
                wybor_slow = input("\nWybierz opcję: ")

                if wybor_slow == "1":
                    słowa_wybrane_do_gry = slowa_dom

                elif wybor_slow == "3":
                    słowa_wybrane_do_gry = slowa_czaswolny

                elif wybor_slow == "2":
                    słowa_wybrane_do_gry = slowa_szkola

                else:
                    print(f"Wybor niepoprawny!")
                    continue

                slowa_z_gry = random.sample(słowa_wybrane_do_gry.zwroc_slowa(), 5)

                gra_wybory = Wybory(slowa_z_gry, wybor_slow)
                gra_wybory.rozpocznij()

                if gra_wybory.poprawne_odpowiedzi == len(slowa_z_gry):
                    uzytkownik.streak += 1

                    if uzytkownik.streak > uzytkownik.max_streak:
                        uzytkownik.max_streak = uzytkownik.streak
                    print(f"Aktualna seria zwycięstw: {uzytkownik.streak}")

                else:
                    uzytkownik.streak = 0
                    print("Seria przerwana!")

                uzytkownik.dodaj_punkty(gra_wybory.get_punkty())
                if slowa_z_gry:
                    uzytkownik.zarzadzaj_katalogami(slowa_z_gry)
                continue

            if wybor == "2":
                print(f"Wybierz z jakiego katalogu chcesz brać słowa:")
                print("1. Dom i przedmioty domowe.")
                print("2. Szkola i przedmioty związane ze szkołą.")
                print("3. Czas wolny i zajęcia.")
                wybor_slow = input("\nWybierz opcję: ")

                if wybor_slow == "1":
                    słowa_wybrane_do_gry = slowa_dom

                if wybor_slow == "3":
                    słowa_wybrane_do_gry = slowa_czaswolny

                if wybor_slow == "2":
                    słowa_wybrane_do_gry = slowa_szkola

                slowa_z_gry = random.sample(słowa_wybrane_do_gry.zwroc_slowa(), 5)
                gra_fiszki = Fiszki(slowa_z_gry)
                gra_fiszki.rozpocznij()

                if gra_fiszki.poprawne_odpowiedzi == len(slowa_z_gry):
                    uzytkownik.streak += 1

                    if uzytkownik.streak > uzytkownik.max_streak:
                        uzytkownik.max_streak = uzytkownik.streak
                    print(f"Aktualna seria zwycięstw: {uzytkownik.streak}")

                else:
                    uzytkownik.streak = 0
                    print("Seria przerwana!")

                uzytkownik.dodaj_punkty(gra_fiszki.get_punkty())
                if slowa_z_gry:
                    uzytkownik.zarzadzaj_katalogami(slowa_z_gry)

                continue

            elif wybor == "4":
                print(f"Wybierz z jakiego katalogu chcesz brać słowa:")
                print("1. Dom i przedmioty domowe.")
                print("2. Szkola i przedmioty związane ze szkołą.")
                print("3. Czas wolny i zajęcia.")
                wybor_slow = input("\nWybierz opcję: ")

                if wybor_slow == "1":
                    słowa_wybrane_do_gry = slowa_dom

                if wybor_slow == "3":
                    słowa_wybrane_do_gry = slowa_czaswolny

                if wybor_slow == "2":
                    słowa_wybrane_do_gry = slowa_szkola

                pierwsze_slowo = słowa_wybrane_do_gry.losuj_slowo()
                gra_wisielec = Wisielec(pierwsze_slowo)

                gra_wisielec.rozpocznij()

                if gra_wisielec.max_bledow > gra_wisielec.bledy:
                    uzytkownik.streak += 1

                    if uzytkownik.streak > uzytkownik.max_streak:
                        uzytkownik.max_streak = uzytkownik.streak
                    print(f"Aktualna seria zwycięstw: {uzytkownik.streak}")

                else:
                    uzytkownik.streak = 0
                    print("Seria przerwana!")

                uzytkownik.dodaj_punkty(gra_wisielec.get_punkty())
                if pierwsze_slowo:
                    uzytkownik.zarzadzaj_katalogami(pierwsze_slowo)
                continue

            elif wybor == "3":
                print(f"Wybierz z jakiego katalogu chcesz brać słowa:")
                print("1. Dom i przedmioty domowe.")
                print("2. Szkola i przedmioty związane ze szkołą.")
                print("3. Czas wolny i zajęcia.")
                wybor_slow = input("\nWybierz opcję: ")

                if wybor_slow == "1":
                    słowa_wybrane_do_gry = slowa_dom

                if wybor_slow == "3":
                    słowa_wybrane_do_gry = slowa_czaswolny

                if wybor_slow == "2":
                    słowa_wybrane_do_gry = slowa_szkola
                pierwsze_slowo = słowa_wybrane_do_gry.losuj_slowo()
                lista_slow = []
                lista_slow.append(pierwsze_slowo)

                while len(lista_slow) < 3:
                    wybrane_slowo = słowa_wybrane_do_gry.losuj_slowo()
                    if wybrane_slowo not in lista_slow:
                        lista_slow.append(wybrane_slowo)

                gra_rozsypanka = Rozsypanka(lista_slow)

                gra_rozsypanka.rozpocznij()

                if gra_rozsypanka.poprawne > gra_rozsypanka.bledne:
                    uzytkownik.streak += 1
                    if uzytkownik.streak > uzytkownik.max_streak:
                        uzytkownik.max_streak = uzytkownik.streak

                    print(f"Aktualna seria zwycięstw: {uzytkownik.streak}")

                else:
                    uzytkownik.streak = 0
                    print("Seria przerwana!")

                uzytkownik.dodaj_punkty(gra_rozsypanka.get_punkty())
                if lista_slow:
                    uzytkownik.zarzadzaj_katalogami(lista_slow)
                continue


            elif wybor == "5":
                uzytkownik.zapisz_stan()
                print("Postęp został zapisany.")

            elif wybor == "6":
                if uzytkownik is not None:
                    nazwa_pliku_raportu = f"{uzytkownik.nazwa}_raport.txt"
                    with open(nazwa_pliku_raportu, "w", encoding="utf-8") as raport:
                        raport.write(f"Raport użytkownika: {uzytkownik.nazwa}\n")
                        raport.write(f"Punkty globalne: {uzytkownik.punkty_globalne}\n")
                        raport.write(f"Najlepsza seria zwycięstw: {uzytkownik.max_streak}\n")
                        raport.write("\nSłowa w katalogach:\n")

                        for nazwa_katalogu, slowa in uzytkownik.katalogi.items():
                            raport.write(f"\nKatalog: {nazwa_katalogu}\n")
                            for slowo in slowa:
                                raport.write(f" - {slowo.tekst} (Trudność: {slowo.poziom_trudnosci.get_trudnosc()})\n")
                        trudne_slowa = []
                        for slowo in wszystkie_slowa:
                            if (slowo.poziom_trudnosci.get_trudnosc()) == "trudny":
                                trudne_slowa.append(slowo)
                        srednie_slowa = []
                        for slowo in wszystkie_slowa:
                            if (slowo.poziom_trudnosci.get_trudnosc()) == "średni":
                                srednie_slowa.append(slowo)
                        latwe_slowa = []
                        for slowo in wszystkie_slowa:
                            if (slowo.poziom_trudnosci.get_trudnosc()) == "łatwy":
                                latwe_slowa.append(slowo)
                        if trudne_slowa:
                            raport.write("\nTrudne słowa:\n")
                            for slowo in trudne_slowa:
                                raport.write(f" - {slowo.get_tekst()}\n")
                        else:
                            raport.write("\nBrak trudnych słów.\n")

                        if srednie_slowa:
                            raport.write("\nŚrednie słowa:\n")
                            for slowo in srednie_slowa:
                                raport.write(f" - {slowo.get_tekst()}\n")
                        else:
                            raport.write("\nBrak średnich słów.\n")

                        if latwe_slowa:
                            raport.write("\nŁatwe słowa:\n")
                            for slowo in latwe_slowa:
                                raport.write(f" - {slowo.get_tekst()}\n")
                        else:
                            raport.write("\nBrak łatwych słów.\n")

                    print(f"Raport został zapisany w pliku '{nazwa_pliku_raportu}'.")


            elif wybor == "7":
                print("Twoje katalogi:.")
                uzytkownik.pokaz_katalogi()

            elif wybor == "8":
                print("\nWracasz do wyboru użytkownika...")
                break

            else:
                print("Brak takiej opcji wyboru, spróbuj ponownie.")

            if slowa_z_gry:
                uzytkownik.zarzadzaj_katalogami(slowa_z_gry)


if __name__ == "__main__":
    main()
