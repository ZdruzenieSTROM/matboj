# Matbojový server

Malý server na vyhodnocovanie matbojov hlavne na minisústredkách. Určený je na lokálne spustenie.

## Ako rozbehať?

### Windows

Ak máš nainštalovaný Git naklonuj si tento projekt cez git v príkazovom riadku:

```
git clone https://github.com/ZdruzenieSTROM/matboj
```

Ak Git nainštalovaný nemáš, klikni na zelené tlačidlo vpravo hore `Clone or download --> Download ZIP` a súbor ulož na disk C. Rozzipuj, choď do priečinka (mal by sa volať `matboj-master`) až kým neuvidíš súbory ako napríklad `manage.py`, skopíruj riadok ukazujúci cestu do priečinka (`C:\...`). Otvor príkazový riadok, napíš `cd `, nakopíruj cestu a spusti príkaz. 

Spusti skript `setup.bat`, ktorý spraví potrebné nastavenia. Server sa potom zapína skriptom `run.bat`. Účet do administrácie sa volá `admin` a heslo je `gumibanan`. Keď sa na teba nevedia ľudia pripojiť a máš Eset, [pridaj do Esetu pravidlo](https://support.eset.com/kb2843/?locale=en_US&viewlocale=sk_SK), kde povolíš všetky requesty (dnu aj von) pre port `80`. 

### Linux

Naklonuj si tento projekt cez git:

```
git clone https://github.com/ZdruzenieSTROM/matboj.git --depth=1
```

Spusti skript `setup.sh` v priečinku `matboj`, ktorý spraví potrebné nastavenia. Server sa potom zapína vygenerovaným skriptom `run.sh`. Účet do administrácie sa volá `admin` a heslo je `gumibanan`. Keď sa na teba nevedia ľudia pripojiť, skús čarovný riadok:

```
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

### Požiadavky na spustenie

Na nastavenie a spustenie treba mať linuxový počítač s trojkovým pythonom, modul `virtualenv` a `pip`, alebo windowsový počítač s trojkovým pythonom.

## Ako sa pripojiť?

V počítači, na ktorom je spustený server zistite IP adresu (naprílad príkazom `ipconfig -all`). Pripojte tento počítač na sieť WiFi. Potom každý počítač prihlásený do tejto siete WiFi môže vo webovom prehliadači namiesto URL adresy napísať zistenú IP adresu a bude na server pripojený. 
