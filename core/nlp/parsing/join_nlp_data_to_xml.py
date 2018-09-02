import xml.etree.ElementTree as ElementTree


def add_conllu_data_to_xml(xml_doc, nlp_file, output_file):
    with open(nlp_file, 'r', encoding='utf-8') as file:
        conllu_data = file.read().split('\n\n#')

    xml_root = xml_doc.getroot()

    for xml_child, conllu_data in zip(xml_root, conllu_data):
        xml_child.append(_add_element_with_text('CONLLU', conllu_data))

    xml_doc.write(output_file.name, encoding='utf-8')
    return output_file.name


def _add_conllu_data(main_element, conllu):
    """
    Reshapes a person data element structure so that the text is removed from the main
    element (<PERSON ...>) and put it under sub element <RAW> instead. CoNLLU-formatted
    NLP data is placed under the sub element <CONLLU>. Reshaping is performed in-place.
    :param main_element: The element to reshape
    :param conllu: Conllu data to add to element
    """
    main_element.append(_add_element_with_text('CONLLU', conllu))


def _add_element_with_text(element_name, element_text):
    new_element = ElementTree.Element(element_name)
    new_element.text = element_text
    return new_element
