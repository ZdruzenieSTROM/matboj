# Matbojový server

Malý server na vyhodnocovanie matbojov hlavne na minisústredkách. Určený je na lokálne spustenie.

## Ako rozbehať?

### Pred použítím

Naklonuj si tento projekt cez git:

```
git clone https://github.com/ZdruzenieSTROM/matboj.git
```

Spusti skript `build-dist.sh` v priečinku `matboj`. Tento skript vygeneruje zipko s nastaveným serverom.

### Na mieste

Rozbaľ si server, spusti skript `run.sh` a server by sa mal spustiť. Účet do administrácie sa volá `admin` a heslo je `gumibanan`. Keď sa na teba nevedia ľudia pripojiť, skús čarovný riadok:

```
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

### Požiadavky na spustenie

Na spustenie by mal stačiť hocijaký počítač s linuxom a trojkovým pythonom, na vygenerovanie zipka treba mať nainštalovaný `pip` a modul `virtualenv`. Dá sa rozbehať aj na windowsoch, len to je komplikovanejšie.
