from io import BytesIO


_XML_FRAME = '<DATA>\n{}\n</DATA>'


def mock_file(data):
    return BytesIO(data.encode('utf-8'))


XML_WITH_SIMPLE_PERSON_ENTRIES = _XML_FRAME.format(
    """
        <PERSON name="TESTIKÄS, TESTAAJA" approximated_page="450-452"><RAW>foo</RAW></PERSON>
        <PERSON name="TOINEN, TESTERI" approximated_page="660-662"><RAW>bar</RAW></PERSON>
        """
)

XML_WITH_COMPLEX_PERSON_ENTRIES = _XML_FRAME.format(
    """
        <PERSON name="TESTIKÄS, TESTAAJA" approximated_page="450-452">
            <RAW>foo</RAW>
            <CONLLU>fooconllu</CONLLU>
        </PERSON>
        <PERSON name="TOINEN, TESTERI" approximated_page="660-662">
            <RAW>bar</RAW>
            <CONLLU>barconllu</CONLLU>
        </PERSON>
        """
)

XML_WITH_MANY_SIMPLE_PERSON_ENTRIES = _XML_FRAME.format(
    """
        <PERSON name="TESTIKÄS, TESTAAJA" approximated_page="450-452"><RAW>foo</RAW></PERSON>
        <PERSON name="TOINEN, TESTERI" approximated_page="660-662"><RAW>bar</RAW></PERSON>
        <PERSON name="KOLMAS, TESTINEN" approximated_page="670-672"><RAW>asd</RAW></PERSON>
        <PERSON name="NELJÄS, TESTIHLÖ" approximated_page="680-682"><RAW>fgh</RAW></PERSON>
        <PERSON name="VIIDES, TESTIKAVERI" approximated_page="690-692"><RAW>qwe</RAW></PERSON>
        """
)
