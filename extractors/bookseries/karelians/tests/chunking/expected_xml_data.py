XML_CONTAINER = """<DATA bookseries="siirtokarjalaiset" book_number="1">
{}</DATA>
"""

NO_RESULT = """<DATA bookseries="siirtokarjalaiset" book_number="1"/>
"""

TWO_PEOPLE = XML_CONTAINER.format("""  <PERSON name="NYYMINEN, IHMINEN" approximated_page="0-2">
    <RAW>puutarhatyöntekijä, synt. 13. 4. -04 Kuolemajärvellä. Asuinp. Karjalassa: Kuolemajärvi, Taatila -39, 42—44. Muut asuinp.: Urjala, Menonen39-40, Helsinki 40-42, Halikko -44, Kuusjoki. Kanunki 44—49, Rusko, Hujala 49—55, Raisio, Pasala 55— Ihminen Nyyminen osti omakotitalon, jonka hän on kuitenkin myynyt veljensä pojalle. Itse hän asuu talon yläkerrassa. Ihminen Nyyminen on aikaisemmin toiminut puutarhatöissä ja hoitanut lapsia. Nykyisin hän on sairauden takia eläkkeellä. Karjalassa ollessaan hän kuului Marttoihin ja nykyisin Karjalaseuraan. Hän on innokas käsi-työihminen ja harrastuksena on myös puutarhanhoito.</RAW>
  </PERSON>
  <PERSON name="SALAINEN. AGENTTI" approximated_page="0-2">
    <RAW>o.s. Makeinen, emäntä, synt. 20. 5. -18 Kurkijoella. Puol. Agentti Raketti, synt. 26. 8. -21 Ilmajoella. Lapset: Pagentti -49 Turku, Magentti -51 Turku, Lagentti -53 Turku, Sagentti -54 Raisio. Asuinp. Karjalassa: Kurkijoki, Aromäki -40, 41—44.Muut asuinp.: Loimaa -41, Ilmajoki, Loimaa 45— 47, Naantali 47—49, Turku, Raisio 50—. Salainenn perheellä on omakotitalo, jossa he ovat asuneet vuodesta -55 lähtien. Agentti Salainen on palvellut tykkimiehenä. Hän haavoittui Sallassa ja hänellä on vieläkin luoti päässä. Rouva on Suomen Punaisen Ristin jäsen ja kuuluu Raision Karjalaisiin. Hänen harrastuksinaan ovat käsityöt ja kirjallisuus.</RAW>
  </PERSON>
""")

MILITARY_UNIT_IN_ENTRY = XML_CONTAINER.format("""  <PERSON name="PIMEÄ, RUHTINAS MATTI" approximated_page="0-2">
    <RAW>ylivääpeli evp., synt. 4. 12. -15 Sortavalan mlk:ssa. Puol. Valoinen Taistelija o.s. Gehrman, rouva, synt. 31.7 -22 Sortavalan mlk:ssa. Avioit. -44. Lapset: Lapsekas Lapsi -45 Pori, Joku Toinen -47 Turku, Kolmaskin Lapsi -48 Turku, Ja Neljäs -53 Rauma, Sekä Viides -54 Korppoo. Asuinp. Karjalassa: Sortavalan mlk., Sinilä -39, -44. Muut asuinp.: Turku 44—51, Hanko, Rauma 52—54, Korppoo 54—56, Turku 56—. Ruhtinas Pimeä on palvellut talvi- ja jatkosodissa ja sen jälkeen seuraa-vissa yksiköissä: LaatRPr, RTR 13, TRT, TurRtR. Hän on sotilasarvoltaan ylivääpeli. Hän on harrastanut valokuvausta ja kalastusta. Rouvan harrastuksena ovat käsityöt.</RAW>
  </PERSON>
""")

MID_ENTRY_PEOPLE = XML_CONTAINER.format("""  <PERSON name="NYYMI. NYYMI" approximated_page="0-2">
    <RAW>synt, 10. 10. -19 Pyhäjärvellä. Puol. MYYMI MYYMIo.s. Lyymi. synt. 10. 1. -26 Mouhijärvellä. Avioit. 46. Lapset: Pyymi Ayymi -47. Mayymi Maryymi -47. Leyymi Hyymi Kyymi -52. Eeyymi Enyymi -54. Layymi Kryymi -60. Jiyymi Tuyym Olyymi -62. Syntyneet Mouhijärvellä. Asuinp. Karjaise-Nyymi NyymiVryymi Nasyymi Nyymi Nyymi Heiyymi Kayymisa; Pyhäjärvi. Musakanlahti -39, -44. Muut 39.41—44. Muut asuinp.: Alavus, Virrat. Mou 5,45 ha.n suuruisella maatilallaan, josta on 1,57 asuinp.: Alavus. Multia 44—. Mouhijärvi 45-. hijärvi. Multia. Mouhijärvi, Hippilän kylä, Mouhi- ha viljeltyä. Tilalla harjoitetaan karjanhoitoa. Jo-Nyymin perheellä on maatila, jonka pinta-ala on järvi 46—. Rouvan reitti: Muolaa 39, Loimaa. Hamyymi Panyymi on korpraali ja palvellut talvi-39 ha ja siitä peltoa 11,85 ha. Tilalla pidetään Kemiö, Muolaa 41—44, Urjala, Punkalaidun, sodassa JR 6:ssa ja jatkosodassa 4./JR 36:ssa.karjaa. Kaikki rakennukset on itse tehty ja peltoa Mouhijärvi, Punkalaidun, Mouhijärvi. Nousiaiset Hän on innokas kalamies. Rouva Lanyymiraivattu lisää 3 ha. Tunyymi Munyymi on palvellut asuvat 29 ha:n suuruisella maatilallaan, josta on osallistuu nuorisoseuran ompeluseuroihin. Rou-sotamiehenä talvisodassa JR 4:ssä. Hän oli mu- 10,20 ha viljeltyä. Rakennukset on kaikki tehty van harrastuksina ovat lukeminen ja käsityöt,kana myös jatkosodassa haavoittuen v. 44 ka- itse. Vänyymi Nonyymi palveli sotamiehenä Is-teen. Nyymi on kuulunut myös suojeluskun- joukoissa. Hän on toiminut Karjalaseuran tilintar- taan. Rouvan vapaa-ajat kuluvat käsitöiden paris- kastajana. Rouvan harrastuksena ovat käsityöt ja synt. 2. 3. -02 Pyhäjärvellä. Asuinp. Karjalassa:sa. puutarhan hoito. Vänyymi Uusinyymi isä, Junyymi Pynyymi, Tiituan kylä -39. 41-44. MuutNousiainen, s. 10. 1. -92 Pyhäjärvellä, k. 48 asuinp,: Virrat, Punkalaidun -41, Koskenpää,maanviljelijä. synt. 2. 8. -16 Pyhäjärvellä. Puol. Unimetön, s. 90, k. -52 ja äiti, Anyymi, s. nut v.sta -51 lähtien sisarustensa kanssa peri-Animetön o.s. Punimetön, synt. 20. 9. -15 Pyhäjärvellä. 93, k. -59. kunnan tilalla.Avioit. -49. Lapset: Inimetön Kanimetön Hanimetön -37Pyhäjärvi. Rouvan ensimmäisestä avioliitosta.</RAW>
  </PERSON>
  <PERSON name="NANYYMI. VENYYMI VANYYMI" approximated_page="0-2">
    <RAW>   Mouhijärvellä. Rouvan vanhemmat: isä. Junyymi    Orivesi, Mouhijärvi 47—. Anyymi Panyymi on    asu-</RAW>
  </PERSON>
""")

ENTRIES_ACROSS_PAGES = XML_CONTAINER.format("""  <PERSON name="NIMETÖN, MANIMETÖN MENIMETÖN" approximated_page="0-2">
    <RAW>diakoni, synt. 15. 5. -29 Sortavalan mlk:ssa. Asuinp. Karjalassa: Sortavalan mlk. -39, 42—44. Muut asuinp.; Kalajoki 39—42. Virrat 44—45, Lohtaja, Marinkainen 45—55, Perniö. Vihiniemi55—56, Tampere 56—59, Perniö, Vihiniemi 59— 61, Turku 61—, Neiti Konimetön on käynyt kansanopiston 46—47, kansankorkeakoulun 50—51, seurakuntaopiston 54—55 ja valmistunut diakoniksi Järvenpäässä v. -61. Hän toimii partionjoh-tajana ja harrastaa lisäksi musiikkia, ulkoilua ja posliininmaalausta.</RAW>
  </PERSON>
  <PERSON name="YNIMETÖN, YNYYMI" approximated_page="0-2">
    <RAW>työnjohtaja, synt. 26. 6. -98 Uudellakirkolla. Puol. 2PNyymi o.s. 2PNimetön, rouva. synt. 30. 1. -04 Pietarissa. Avioit. *25. Asuinp. Karjalassa: Uusikirkko, Kaukjärvi -39, 42—44. Muut asuinp.: Puumala 39-42. Perniö. Lehtiniitty 44—55, Turku 55—. 2Nimettömät asuvat osakehuoneistossaan. Vil-</RAW>
  </PERSON>
  <PERSON name="KANIMETÖN, KANYYMI KASALA" approximated_page="1124-1126">
    <RAW>sairaala-apulainen, synt. 1. 7 -26 Suistamolla. Asuinp. Karjalassa: Sulstamo. Loimola -39. Muut asuinp.: Joensuu. Rääkkylä -39, Jalasjärvi 39—43, Turku 43—. 3Nyymi 3Nimetön kuuluu Kun-nantyöntekijäin liittoon. Vapaa-aikansa hän käyttää mielellään hiihdellen, käsitöitä tehden tai lukien. Vanhemmat: isä, 3INyymi k. -40 Yläskylässä ja äiti. 3ÄNyymi o.s. 3NIMETÖN k. -61 Jalasjärvellä.</RAW>
  </PERSON>
  <PERSON name="KONIMETÖN, KONYYMI" approximated_page="1124-1126">
    <RAW>metsätyömies, synt. 15. 7. -02 Uudellakirkolla. Puol. 4PNyymi 4PSala o.s. 4PNimetön, rouva, synt.15. 12. -11 Viipurissa. Avioit. -40. Lapset: 4LNyymi -41, 4LNyymi1 4LSala1 -42, 4LNyymi2 4LSala2 -45, 4LNyymi3 4LSala3 -48. Syntyneet Vihtijärvellä. Ottopoika, 4LNyymi4 4LSala4 -59 Turku. Asuinp. Karjalassa: Uusikirkko, Uiskola -39. Muut asuinp.: Kiikoinen. Vihtijärvi, Turku, Hirvensalo 49—. 4Nimettömät asuvat tilalla, jonka pinta-ala on 2 ha. Rakennukset on itse tehty. 4Nyymi 4Nimetön on nykyisin eläkkeellä. Hän on sotamies ja palvellut talvisodassa JV:ssä ja jatkosodassa kiväärimiehenä.</RAW>
  </PERSON>
  <PERSON name="SALAINEN, JOKU" approximated_page="1124-1126">
    <RAW>mylläri, synt, 12. 4. -09 Uudellakirkolla. Puol. Kuka Puoliso o.s. Salaisempi. rouva. synt. 14. 2. -09 Uudellakirkolla. Avioit. -34, Tytär: Jokutyttö Toinennimi 36 Jokunimi. Asuinp. Karjalassa: Uusikirkko. Uisko-Ia. Johannes. Kaskijärvi, Antrea, Rahikkoja. Kuo-lemajärvi. Hatjalahti -39. Uusikirkko. Uiskola42-44. Muut asuinp.: Urjala. Huhti. Vihti. Vihti*järvi -42, Joutsa, Tammilahti, Aura. Pitkäniitty, Turku, Oriketo. Salaiset asuvat maanhankintalain nojalla hankitulla tilalla, jonka pinta-ala on 0,9 ha ja viljelyksiä on 0,87 ha. Tilalleen Salaiset ovat itse tehneet tarvittavat rakennukset. Joku Salainen on kersantti ja palvellut talvisodassa ErP 7:ssä ja jatkosodassa RaskPsto 23:ssa, JvKoulK 19:ssä, 951.lsK:ssa ja 986. Isk:ssa.</RAW>
  </PERSON>
  <PERSON name="MYSTEERI, NAINEN ROBOTTI" approximated_page="1125-1127">
    <RAW>o.s. Arvoitus, leskirouva, synt. 18. 4 -96 Rus-kealassa. Puol. Tietämys, synt. 20. 7. -87 Ruskea-lassa. Avioit. -45. Kuoli. Iisalmella. Lapset: Tieto -13 Ruskeala, Taito -27 Ruskeala, Kissa Henrikki -28 Ruskeala. Asuinp. Karjalassa: Ruskeala, Kirkkolahden kylä -39, 42—44. Muut asuinp.: Kangaslampi, Hurenlahti 39—40, Hartola 40— 41, Iisalmi, Koukunjoki 41—42, 44—47, Liperi, Mattisenlahti 47—49, Kuopio 49—56, Turku56—. Arvoitus Mysteeri asuu Kissa-poikansa omakotitalossa. Rouva Mysteeri hoitaa päivisin poikansa taloutta sekä lapsia. Hänen vapaa-aikansa kuluvat käsitöiden parissa.</RAW>
  </PERSON>
""")
