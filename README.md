# Veðurstöð

## Innihaldslýsing
* Raspberry Pi (t.d. 3 eða 4)
* Arduino (t.d. CH340)
* MicroSD kort (t.d. 16GB)
* DHT11 skynjari
* SGP30 skynjari
* BMP280 skynjari
* Kaplar eftir þörfum
* (Raspberry Pi Camera V2)

Þessir hlutir eru að miklu leyti fáanlegir í Öreind, Computer.is, Elko og hjá [SparkFun](https://sparkfun.com).

## Kóði í Arduino
Fyrst þarf að setja upp [Arduino IDE](https://www.arduino.cc/en/software). Þar eru sóttir pakkar í Library Manager fyrir þá skynjara sem keyptir hafa verið. Svo er hægt að nota __hita-raka.ino__ skrána héðan til að hlaða á stýrispjaldið.

## Tenging skynjara við Arduino
Athugið að í Arduino Nano eru pinnarnir ekki númeraðir 1, 2, 3 o.s.frv., heldur A1, A2, A3 o.s.frv. Á Arduino Nano er SDL tengið (fyrir Qwiic tengingarnar) á A4 og SCL á A5.

## Aflestur skynjara í Raspberry Pi
Forritið __read.py__ er skrifað í Python 3.8 og þarfnast nokkurra pakka þegar það er keyrt. Leiðbeiningar um notkun _pip_ eru [fáanlegar hér](https://packaging.python.org/tutorials/installing-packages/).

Til þess að setja upp þau forritasöfn sem þarf til að keyra kóðann keyrið þá skipunina `pip3 install -r requirements.txt`

## Myndgreining í Raspberry Pi
Forritið __cam.py__ er skrifað í Python 3.8 og þarfnast meðal annars _Pillow_ pakkans. Leiðbeiningar um uppsetningu hans eru [fáanlegar hér](https://pillow.readthedocs.io/en/stable/installation.html). Til að leyfa notkun myndavélarinnar í Pi þarf að breyta grunnstillingum tölvunnar í skipanalínu gegnum _raspi-config_ skipunina.

## Hafa samband
Heyrið í mér á postur@benjaminjulian.com eða með því að senda mér skilaboð hér. Kóðinn er að miklu leyti byggður á annarra verkum og ég er fyllilega ómenntaður í tölvun eða rafeindatækni. Honum ber því ekki að taka sem fyrirmynd, heldur sem nothæfri reddingu.
