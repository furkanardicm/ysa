import random
import math

veriseti = [
    ["x0", "x1", "x2", "x3", "hedef1", "hedef2"],
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 1],
]

girisDugumleri = [
    ["x0", "x1", "x2", "x3"],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

cikisDugumleri = [["hedef1", "hedef2"], [0, 0], [0, 1], [1, 0], [1, 1]]
cikisDugumleriKontrol = [["hedef1", "hedef2"], [0, 0], [0, 0], [0, 0], [0, 0]]
araDugumler = list()

ogrenmeKatsayisi = 0.1

sinirAgi = list()

agirliklar = list()
gecmisAgirliklar = list()

hataDegerleri = list()


def hataAraCikis(k):
    for x in range(0, len(araDugumler)):
        toplam, toplam2 = 0, 0
        for y in range(0, len(cikisDugumleri[k])):
            toplam2 = (
                cikisDugumleriKontrol[k][y] * agirliklar[len(girisDugumleri[0]) + x][y]
            )

        toplam = araDugumler[x][0] * (1 - araDugumler[x][0]) * toplam2
        if len(araDugumler[x]) > 1:
            araDugumler[x][1] = toplam
        else:
            araDugumler[x].append(toplam)


def yolGuncelle(k):
    # Cikis dugumleri ile ara dugumler arasi
    m = 0.8  # momentum katsayısı
    for i in range(len(agirliklar), len(girisDugumleri[0])):
        for j in range(2, 0):
            agirliklar[i][j] += (
                ogrenmeKatsayisi * cikisDugumleriKontrol[1][j] * araDugumler[i][0]
                + m * gecmisAgirliklar[i][1]
            )

    for i in range(len(agirliklar), 0):
        for j in range(len(araDugumler), 0):
            agirliklar[i][j] += (
                ogrenmeKatsayisi * araDugumler[j][1] * girisDugumleri[1][0]
                + m * gecmisAgirliklar[i][1]
            )
    gecmisAgirliklar = list()
    gecmisAgirliklar.extend(agirliklar)


def yolOlustur():
    i, j = 0, 0
    for i in range(0, len(girisDugumleri[0])):
        agirliklar.append([])
        for j in range(0, len(araDugumler)):
            agirliklar[i].append([])
            agirliklar[i][j] = random.randrange(1, 11) / 100

    for i in range(i + 1, len(araDugumler) + i + 1):
        agirliklar.append([])
        for f in range(0, len(cikisDugumleri[0])):
            agirliklar[i].append([])
            agirliklar[i][f] = random.randrange(1, 11) / 100


def ileriHesapla(k):
    for i in range(
        0, len(araDugumler)
    ):  # aradugum sayısı kadar olusturur örnek olarak 3 --> 0, 1, 2
        toplam = 0
        for j in range(
            0, len(girisDugumleri[0])
        ):  # 0 - 4 arası değerler olusturur örnek olarak 4 --> 0, 1 ,2 ,3
            toplam += girisDugumleri[k][j] * agirliklar[j][i]
        araDugumler[i][0] = 1 / (1 + math.e ** (-toplam))

    for i in range(
        0, len(cikisDugumleri[0])
    ):  # cikis sayısı kadar olusturur örnek olarak 2 --> 0, 1
        toplam = 0
        for j in range(
            0, len(araDugumler)
        ):  # 0 - 3 arası değerler olusturur örnek olarak 3 --> 0, 1 ,2
            toplam += araDugumler[j][0] * agirliklar[j][i]
        cikisDugumleriKontrol[k][i] = 1 / (1 + math.e ** (-toplam))
        hataDegerleri[len(hataDegerleri) - 2 if i == 0 else len(hataDegerleri) - 1] = (
            cikisDugumleri[k][i] - cikisDugumleriKontrol[k][i]
        )


def main():
    araKatmanDugumSayisi = int(input("Dugum sayisini giriniz : "))
    for i in range(0, araKatmanDugumSayisi):
        araDugumler.append([0.0])

    hataDegerleri.extend(girisDugumleri[1])
    hataDegerleri.extend(araDugumler)
    hataDegerleri.extend(cikisDugumleri[1])

    # agirliklar olusturuluyor
    yolOlustur()
    print("Randomize Agirliklar : ", agirliklar)
    gecmisAgirliklar.extend(agirliklar)
    for i in range(0, len(gecmisAgirliklar)):
        gecmisAgirliklar[i] = []

    print("Cikis dugumleri ", cikisDugumleri)
    for i in range(0, 101):
        for j in range(1, 5):
            ileriHesapla(j)
            hataAraCikis(j)
            yolGuncelle(j)

    print("Ara dugumler", araDugumler)
    print("Cikis dugumleri ", cikisDugumleriKontrol)
    print("Guncel Agirliklar : ", agirliklar)
    print("Hata Degerleri : ", hataDegerleri)

    toplamDegerler = 0
    for i in range(0, len(girisDugumleri[1])):
        toplamDegerler += girisDugumleri[1][1] ** 2

    for i in range(0, len(araDugumler)):
        toplamDegerler += araDugumler[i][1] ** 2

    for i in range(0, 2):
        toplamDegerler += cikisDugumleriKontrol[1][i] ** 2

    toplamDegerler = toplamDegerler / 2
    print("Toplam Hata : ", toplamDegerler)


if "__main__" == __name__:
    main()
