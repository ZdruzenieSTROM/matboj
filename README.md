# Matbojový server

Malý server na vyhodnocovanie matbojov hlavne na minisústredkách. Určený je na lokálne spustenie.

## Ako rozbehať?

Naklonuj si tento projekt cez git:

```
git clone https://github.com/ZdruzenieSTROM/matboj.git --depth=1
```

Spusti skript `setup.sh` v priečinku `matboj`, ktorý spraví potrebné nastavenia. Server sa potom zapína vygenerovaným skriptom `run.sh`. Účet do administrácie sa volá `admin` a heslo je `gumibanan`. Keď sa na teba nevedia ľudia pripojiť, skús čarovný riadok:

```
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

### Požiadavky na spustenie

Na nastavenie a spustenie treba mať linuxový počítač s trojkovým pythonom, modul `virtualenv` a `pip`. Dá sa to rozbehať aj na windowsoch, len to je komplikovanejšie.
