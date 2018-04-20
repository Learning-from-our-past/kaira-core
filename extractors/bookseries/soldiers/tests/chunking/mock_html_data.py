HTML_CONTAINER = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<meta name="generator" content="ABBYY FineReader 12"/>
</head>
<body>
{}
</body>
</html>
"""

PERSON1 = """<p>TESTI, Ahto Simakuutio, s 19.8.21 Tku, rakmest. Pso vsta 42 Nainen Naiskari Naiseva, s 27.1.21 Naantali, puhväl. Lapset&nbsp;Lapsi1 42, Lapsi2 48, Lapsi3- 50, Lapsi4 56. -Ts: Er P 33; Vironlahti. Js: JR 1, JR 49; Ojajärvi, Lempaalanjärvi, Vuosalmi, Kaukola.&nbsp;Haav 41 Reisjärvi, oik käsi. VR 3, VR 4 tl k.&nbsp;Kot 3.12.44 Tku. Sotarvo ylil. - Naantalin&nbsp;Löyly johtok j ja talhoit, Naantalin Seudun&nbsp;Veteraanit ja Resupskerho j. - SU hop amr.&nbsp;- Harr urheilu. - Os Mäntykaari 3, Lietsala.</p><img src="8. Suomen rintamamiehet, 10. divABBYY_OCR_files/8. Suomen rintamamiehet, 10. divABBYY_OCR-2.jpg" style="width:69pt;height:101pt;"/>"""
PERSON2 = """
<p>TESTINEN, Hessu, s 30.3.06 Luhanka, mv. Pso vsta 29 Vaimo Vaimokas, s 05 Sysmä,&nbsp;emäntä. Lapset Lapsi1 29, Lapsi2 33, Lapsi3 44.&nbsp;- Ts: 10 LK; Kannas; sairkant. Haav</p>
<p>27.12.39 Kannas, rinta ja käsivarsi; 35 %.&nbsp;Kot 15.5.40 Hki. Sotarvo stm. - Uskottu m,&nbsp;Sotavetliitto j. - Harr kalastus. - Os 19910&nbsp;Tammijärvi.</p><img src="8. Suomen rintamamiehet, 10. divABBYY_OCR_files/8. Suomen rintamamiehet, 10. divABBYY_OCR-3.jpg" style="width:71pt;height:94pt;"/>
"""

TWO_PEOPLE = HTML_CONTAINER.format("""
<img src="8. Suomen rintamamiehet, 10. divABBYY_OCR_files/8. Suomen rintamamiehet, 10. divABBYY_OCR-1.jpg" style="width:70pt;height:101pt;"/>
{}
{}
""".format(PERSON1, PERSON2))


ENTRIES_ACROSS_PAGES = HTML_CONTAINER.format("""
<p>141</p>
{}
<p>142</p>
{}
""".format(PERSON1, PERSON2))
