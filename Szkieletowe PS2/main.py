import math

#ZADANIE 1
imie = str(input("Podaj imie: "))
nazwisko = str(input("Podaj nazwisko: "))

print(f'{nazwisko}, {imie}')


#ZADANIE 2
l = []
dane = str(input('Podaj imie i nazwisko: '))
imie, nazwisko = dane.split(" ", 1)
print(f'{nazwisko}, {imie}')



#ZADANIE3
dane1 = str(input('Podaj wspolrzedne a i b punktu 1: '))
dane2 = str(input('Podaj wspolrzedne a i b punktu 2: '))

aa, ab = dane1.split(" ", 1)
ba, bb = dane2.split(" ", 1)

odl = math.sqrt((int(ba) - int(aa)) ** 2 + (int(bb) - int(ab)) ** 2)
odl = odl.__round__(2)
print("Odległość pomiedzy punktami to:", odl)



#ZADANIE 4
liczba = int(input("Podaj liczbe gosci: "))

z_dzieleniem = 32 / liczba

bez_dzielenia = 32 // liczba
pozostale = 32%liczba

print("Liczba gości: ", liczba)
print("Opcja 1:", f"{bez_dzielenia} kawałki dla każdego, {pozostale} pozostałe")
print("Opcja 2:", f"{z_dzieleniem} kawałka dla każdego." )




#ZADANIE 5
zdanie = str(input("Podaj zdanie: "))
l = []
l = zdanie.split(" " or ",")

k = -1
for i in range(len(l)):
    print(l[k])
    k-=1


#ZADANIE 6
dlugosc = int(input("Podaj dlugosc pytona: "))
if dlugosc <=6:
    powierzchnia = 6*0.5
else:
    powierzchnia = 6 * 0.5 + (dlugosc-6) * 0.75

print(f"Zalecana powierznia klatki to: {powierzchnia}m2")


#ZADANIE7
#a
kwadraty = [x**2 for x in range(1, 11)]
print(kwadraty)

#b
zdanie = str(input("Podaj zdanie: "))
litery = [slowo[0] for slowo in zdanie.split()]
print(litery)

#c
krotki = [(i, j) for i in range(2, 50) for j in range(2, 50) if i * j < 50]
print(krotki)



#ZADANIE 8
slowo = str(input("Podaj slowo: "))
l = [i for i in slowo]
if l == l[::-1]:
    print("Słowo jest palindromem")
else:
    print("Słowo nie jest palindromem")


#ZADANIE 9
def funkcja(n):
    if n < 10:
        return 0
    x = 1
    for cyfra in str(n):
        x *= int(cyfra)
    return 1 + funkcja(x)

liczba = int(input("Podaj liczbe: "))
print(f"Persistence of a number liczby {liczba} to {funkcja(liczba)}")