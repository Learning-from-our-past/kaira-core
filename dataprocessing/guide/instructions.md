## 1. Tekstin skannaus ja OCR
Tarvittava matrikkeliteos on ensiksi muutettava digitaaliseksi tekstiksi. Tämä edellyttää kirjan skannaamista ja sen tekstin ajamista OCR-ohjelmiston kuten ABBYY Finereaderin lävitse.  Tarvittava formaatti riippuu kirjasarjasta:

#### Suomen Rintamamiehet
Tallenna OCR-teksti txt-tiedostoon siten, että teksti sisältää ainoastaan sotilaiden tiedot. Poista siis kirjojen sisältämät johdannot, epilogit ja sisällysluettelot. 

#### Siirtokarjalaisten tie, Suuret maatilat, Suomen pienviljelijät
Näiden kirjasarjojen tapauksessa tee OCR ABBYY Finereaderillä ja tallenna tulos html-tiedostoksi ilman css-muotoiluja. 

## 2. Tekstin muuntaminen analysoitavaan muotoon
Ennenkuin materiaalia voidaan käsitellä ja analysoida, se täytyy muuntaa editoitavaan muotoon. Kaira muuntaa sille annetun OCR-tiedoston (txt, html jne) xml-tiedostoksi, jota käytetään analysointiin, editointiin yms.

1.  Kairassa avaa valikko **File -> Import -> From OCR**
2. Avautuvassa ikkunassa valitse ensin lähdetiedosto jossa OCR-tiedot ovat. Tämä on tiedosto, jonka loit luvussa 1. Valitse myös paikka johon syntynyt xml-tiedosto tallennetaan. 
3. Valitse ikkunassa kirjasarja, jonka materiaalia olet muuntamassa ja paina OK-nappia.
4. Odota kärsivällisesti kunnes saat ilmoituksen muunnoksen onnistumisesta. Prosessi voi viedä materiaalin koon ja mahdollisten kuvien vuoksi useita minuutteja (jopa 15min) ja tänä aikana ohjelma saattaa näyttää jumittuneelta. 

## 3. Materiaalin lukeminen Kairalla
Kun olet luonut aineistostasi xml-tiedoston luvun 2 ohjeiden mukaisesti, voit avata tiedoston Kairalla, jolloin sen sisältö analysoidaan ja Kaira yrittää poimia tekstiaineistosta dataa. 

1. Avaa valikko **File -> Open xml** ja valitse aiemmin luomasi xml-tiedosto. Odota kunnes analysointi on valmis. Tämä voi materiaalin koosta riippuen viedä runsaasti aikaa.
2. Analysoinnin päätyttyä tiedoston sisältö esitetään Kairan päänäkymässä seuraavasti:

### 3.1 Henkilölistaus
Päänäkymän vasemmassa reunassa on listaus kirjasta löytyneistä henkilöistä tai tiloista. Henkilöä voi tarkastella klikkaamalla nimeä. Nimeä voi muokata tuplaklikkaamalla nimeä listassa ja kirjoittamalla uuden nimen.

Henkilölistauksen yläpuolella on pudotusvalikko, jolla voi valita listassa näytettäviksi henkilöitä sen mukaan millaisia analysointivirheitä tai puuttuvia tietoja heillä on. Esimerkiksi valitsemalla "BIRTHDAY" pudotusvalikosta, näet henkilölistauksessa ihmiset, joiden syntymäpäivää ei jostain syystä kyetty löytämään.

### 3.2 Raakatekstinäkymä
Pääikkunan keskellä on kolme tekstikenttää, joissa on tarkasteltavan henkilön alkuperäisteksti, sekä henkilöä edeltävän ja seuraavan henkilön alkuperäistekstit. 

Alkuperäistekstejä voi muokata vapaasti ja tallentaa xml:ään, jolloin seuraavalla analysointikerralla ne otetaan huomioon. Voit esimerkiksi korjata kirjoitusvirheitä tai muita vastaavia ongelmia ja siten parantaa seuraavan kerran analysoinnin tarkkuutta. Tämä on erityisen tärkeää siksi, että Kaira tunnistaa halutut tiedot niiden tekstin muodon perusteella. Esimerkiksi sanaa "lypsylehmä" ei tunnisteta, jos sen kirjoitusasu on muotoa "ly psyl ehmä".

#### 3.2.1 Henkilöiden poistaminen
Voit poistaa henkilön lopullisesti analysoitavista yksinkertaisesti tyhjentämällä raakatekstikentän ja tallentamalla tiedoston (**File->Save**). Seuraavalla analysointikerralla kyseistä henkilöä ei enää ole.

#### 3.2.1 Henkilöiden yhdistäminen
Ajoittain etenkin Suomen Rintamamiehet kirjasarjassa yhden ihmisen tiedot ovat jakautuneet muunnosprosessissa useammaksi henkilöksi. Tällöin voit yksinkertaisesti yhdistää nämä tiedot kopioimalla tekstit oikean henkilön raakatekstikenttään. Jättämällä tyhjäksi virheelliset ylimääräiset raakatekstikentät ne poistetaan tallennuksen yhteydessä.

### 3.3 Henkilöstä irroitetut tiedot
Päänäkymän oikeassa reunassa on puurakenne, joka näyttää tarkasteltavasta henkilöstä löydetyt tiedot. Tietoja voi muokata tuplaklikkaamalla niitä ja kirjoittamalla uuden arvon.

#### 3.3.1 Värikoodit
Puunäkymässä on muutama erilainen värikoodi:

**Punainen**
Punainen kenttä on kenttä, josta puuttuu arvo. Lisäksi puuttuva arvo on siinä mielessä "kriittinen", että se on johtanut henkilön luokittelemiseen johonkin virheryhmään. Esimerkiksi jos "BirthDay" kenttä on punainen, löytyy kyseinen henkilö Henkilölistauksen pudotusvalikon "BIRTHDAY" listauksesta. 

**Keltainen**
Keltainen symboloi myös puuttuvaa dataa, mutta joka ei luokittele henkilöä mihinkään erityiseen virheryhmään. Yleensä nämä kentät ovat arvoja, jotka luonnollisista syistä puuttuvat suurelta osalta henkilöitä, esimerkiksi tyttönimeä kuvaava "OriginalFamily", jota harvemmin miehiltä löytyy.

**Vihreä**
Vihreä kenttä kuvaa arvoa, joka on asetettu käsin editorissa. Kyseistä arvoa ei muuteta automaattisen analysoinnin yhteydessä. Toisin sanoen kun seuraavan kerran avaat tiedoston muokattavaksi, vihreissä kentissä näkyvät asettamasi arvot Kairan löytämän alkuperäisen arvon sijaan.

#### 3.3.2 Puuttuvat paikat ja lapset
Ajan loppumisen vuoksi käyttöliittymä ei tällä hetkellä tue uusien lasten tai paikkojen lisäämistä tietoihin suoraan. Mikäli osa henkilön lapsista näyttäisi jäävän löytymättä, voit kokeilla muokata niiden tekstiä **raakatekstinäkymässä** muotoon, jossa niiden irroittaminen onnistuu. Tämä tarkoittaa yleensä kirjoitusvirheiden poistamista tai erityisilmausten kuten "sekä viimeinen poika Matias -53" muuttamista muotoon "Matias -53". Voit katsoa esimerkkiä niistä henkilöistä, joiden kohdalla irroitus on onnistunut.

### 4. Uusien ihmisten lisääminen
Voit luoda uusia ihmisiä tiedostoosi **Create new Person** painikkeella ohjelman yläreunassa. 

Avautuneessa ikkunassa anna ylempään kenttään henkilön nimi (joka mm. näkyy henkilölistauksessa) ja hänen raakatekstinsä ja paina OK. Uuden henkilön pitäisi ilmestyä henkilölistauksen loppuun. Tallentamalla tiedostosi lisätty henkilö lisätään pysyvästi xml-tiedostoon.

Tämä toiminto on kätevä tilanteissa joissa vahingossa useampi henkilö on tallennettu samaan raakatekstiosaan. Tämä on suhteellisen yleistä Suomen Rintamamiehet kirjasarjan tapauksessa.

### 5. Tulosten vieminen csv ja json-formaatteihin

#### 5.1 CSV
Kun data on sopivassa muodossa, se voidaan viedä csv-muotoon Excel analysointia varten. Mene **File -> Export -> CSV** ja valitse paikka johon CSV tallennetaan.

#### 5.2 JSON
JSON on tiedosto-formaatti, joka on kätevä datan lukemiseen ja käsittelyyn ohjelmallisesti useimmilla moderneilla ohjelmointikielillä. Mene **File -> Export -> JSON** ja valitse paikka johon JSON tallennetaan.

Jsonin käytöstä on huomatettava, että ennen lukemista kannattaa tutustua sen muotoon. Koska useat kentät voidaan jättää tyhjiksi, saattavat numeeriset kentät ajoittain sisältää tyhjän merkkijonon. Niinpä lukiessa dataa ohjelmaasi kannattaa kiinnittää huomioita tyyppimuunnoksiin.