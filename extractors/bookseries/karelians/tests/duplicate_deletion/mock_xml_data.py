XML_CONTAINER = """<DATA bookseries="siirtokarjalaiset" book_number="1">
{}</DATA>
"""

DUPLICATED_PERSON = XML_CONTAINER.format(
    """
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 30. 12. -97 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 30. 12. -97 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
"""
)

DUPLICATED_PERSON_BAD_DOB = XML_CONTAINER.format(
    """
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 15. 3. -22 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 9. 8. -57 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
"""
)

DUPLICATED_PERSON_BAD_DOB_AND_NAME = XML_CONTAINER.format(
    """
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 15. 3. -22 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjagealassa Tokajätkä 39, 42-44. Mfauut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies  on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="SALAINEN, VIETTELIJÄ" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 9. 8. -57 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44.  asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvidsasodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
"""
)

DUPLICATED_PERSON_ONE_ENTRY_LONGER = XML_CONTAINER.format(
    """
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 30. 12. -97 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 30. 12. -97 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarina. Kuusisto 47-. Anonyymin perhe on itse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut talvisodassa työvelvollisena.</RAW><CONLLU></CONLLU></PERSON>
"""
)

DUPLICATED_PERSON_NO_DOB_SIMILAR_NAME = XML_CONTAINER.format(
    """
<PERSON name="ANANYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 10. 12. -27 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan. Jokutyttö -40 Kisko. Asuinfp Karjalassa Tokajätkä 39, 42-44. Muut asuinp.: Kisko 39—42. Kiikka, Pori. Reposaari. Kaarfina. Kuusisto 47-. Anonyymin perhe on itfse rakentanut omakotitalonsa. Puolisomies Anonyymi on palvellut tfalvisodassa työvelvollisena. On monesti harrastanut purjehtimista ja suunnistusta. Postitse saat kaikki viestit parhaiten perille.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="ANONYYMI, NAINEN" approximated_page="233-235"><RAW>o.s. Kissanainen, synt. 30. 11. -97 Johannekscs sa. Puol. Puolisomies, kirvesmies, synt. 8. 6. 96 Maaningalla. Lapset: Jokujätkä -34 Tokajätkä, k. -53 suorittaessaan asevelvollisuuttaan.  -40 Kisko. Asuinp Karjfaeageaglassa Tokajätgeageagkä 39, 42-44. Mduut asuinp.: Kisko 39—42. , Pori.. Kaarina. Kufusisto 47-. Anoeafnyyfmin perhe on itse rakentanut . Puolisonainen Anonyymi on palvellut talvisodegagassa työvelvoaefgeaghllisena. Mutta hän ei ole koskaan käynyt avaruudessa. AGeagaeg egeag eag eag aegea ghjarhaekj iph aek.</RAW><CONLLU></CONLLU></PERSON>
"""
)

NO_DUPLICATES = XML_CONTAINER.format(
    """
<PERSON name="JOKUMIES, HERRA" approximated_page="234-236" img_path="images/JokumiesHerra.jpg"><RAW>autonasentaja, synt. 25. 10. -25 Impilahdella. Puol. Naispuoliso Jokula o.s. Jokunen, rouva, synt. 26.7. -25 Perttelissä. Avioit. -62. Lapset: Lapsi Yksi -64 Turku, Lapsi Kaksi -67 Kaarina. Asuinp. Karjalassa: Impilahti, Huunukka -39, 41—44. Muut asuinp.: Liperi 39—41, Lapua. Koskikylä44-46, Vehmersalmi 46—52, Pertteli, Inkere52—55, Muurla, Ranta 55—62, Turku 62—64, Kaarina, Poikluoma 64—, Jokumiehet asuvat omakotitalossaan. He ovat itse rakentaneet saunan ja verstastilaa sekä autotallin. Heillä on autokorjaamo. Herra Jokumies on sotamies ja palvellut jatkosodassa JvKoulK 2:ssa. Hän on aikaisemmin ollut innokas metsästäjä, nykyään hän viihtyy puu-tarhatöiden parissa. Rouva Jokumies on käynyt Vehmaan Kotitalouskoulun v. -46. Hän on aikaisemmin harrastanut musiikkia. Nykyään hän on kiinnostunut puutarhanhoidosta ja käsitöistä.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="SUVENEERI, ROUVA" approximated_page="234-236"><RAW>o.s. Kollektivisti, synt. 24. 12. -21 Johannekses sa. Puol. Toimi, kirvesmies, synt. 25. 1. -20 Hii-tolassa. Avioil 43. Lapset: Keisaritar -44 Hiitola. Kuningas -50 Kaarina. Asuinp. Karjalassa: Johannes -39. 42-43. Hiitola 43-44. Muut asuinp.: Kisko. Hamina 42. Paimio -44. Kaarina. Isokyrö. Nakkila. Kaarina. Kuusisto 49—. Suveneerit muut tivat v. 60 Joensuun kylään. Sinne he rakensivat omakotitalon. Herra Suveneeri on ollut talvisodassa vapaaehtoisesti työvelvollisena ja välirauhan aikana asevelvollisuuttaan suorittamassa. Jatkosodan aikana hän palveli korpraalina KTR 11:ssä rintamalla, jossa haavoittui. Hänen harrastuksenaan on kalastus. Rouva on kiinnostunut käsitöiden teosta.</RAW><CONLLU></CONLLU></PERSON>
"""
)

NO_DUPLICATES_TWO = XML_CONTAINER.format(
    """
<PERSON name="SHAMAANI, REILU HYVÄ" approximated_page="236-238"><RAW>synt. -04 Johanneksessa. Puol. Pappi, synt. -02 Johanneksessa. Kuollut Kaarinassa. Lapset: Nuorempishamaani -37 Johannes,, Nuorempipappi 38 Johannes, Vapaamuurari -40 Muurla, Lapsi -45 Paimio, Asuinp. Karjalassa: Johannes -39, 42—44. Muut asuinp.. Paimio 39—42, —44 Kaarina, Kuusisto, Kaarina, Voivala 60—. Rouva Reilu hoitaa poikiensa taloutta,</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="VELHO, NOITA" approximated_page="1-3"><RAW>o.s. Taistelija, parsija, synt. 10 7 -30 Rus- 48—, Sotalukko Velho on tullut Suomeen Saksan kautta v. -43. Sen jälkeen Paimio, Masku, Kaarina Sotalukko Velhon harrastuksena on kalastus. Noita Velhon äiti, Vanhempinoita o.s. Velhoisempi kuoli Heinolassa -41 ja isä, Velhoinen Velhola kuoli Kaarinassa v. -61</RAW><CONLLU></CONLLU></PERSON>
"""
)

SHARES_ONE_ENTRY_WITH_EACH_NO_DUPLICATES = XML_CONTAINER.format(
    """
<PERSON name="SUVENEERI, ROUVA" approximated_page="234-236"><RAW>o.s. Kollektivisti, synt. 24. 12. -21 Johannekses sa. Puol. Toimi, kirvesmies, synt. 25. 1. -20 Hii-tolassa. Avioil 43. Lapset: Keisaritar -44 Hiitola. Kuningas -50 Kaarina. Asuinp. Karjalassa: Johannes -39. 42-43. Hiitola 43-44. Muut asuinp.: Kisko. Hamina 42. Paimio -44. Kaarina. Isokyrö. Nakkila. Kaarina. Kuusisto 49—. Suveneerit muut tivat v. 60 Joensuun kylään. Sinne he rakensivat omakotitalon. Herra Suveneeri on ollut talvisodassa vapaaehtoisesti työvelvollisena ja välirauhan aikana asevelvollisuuttaan suorittamassa. Jatkosodan aikana hän palveli korpraalina KTR 11:ssä rintamalla, jossa haavoittui. Hänen harrastuksenaan on kalastus. Rouva on kiinnostunut käsitöiden teosta.</RAW><CONLLU></CONLLU></PERSON>
<PERSON name="SHAMAANI, REILU HYVÄ" approximated_page="236-238"><RAW>synt. -04 Johanneksessa. Puol. Pappi, synt. -02 Johanneksessa. Kuollut Kaarinassa. Lapset: Nuorempishamaani -37 Johannes,, Nuorempipappi 38 Johannes, Vapaamuurari -40 Muurla, Lapsi -45 Paimio, Asuinp. Karjalassa: Johannes -39, 42—44. Muut asuinp.. Paimio 39—42, —44 Kaarina, Kuusisto, Kaarina, Voivala 60—. Rouva Reilu hoitaa poikiensa taloutta,</RAW><CONLLU></CONLLU></PERSON>
"""
)
