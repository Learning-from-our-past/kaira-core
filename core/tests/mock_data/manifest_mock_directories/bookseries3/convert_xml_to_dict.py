def convert_xml_to_dict(person_element):
    _raw, _otherdata = person_element
    person_entry = {**person_element.attrib, 'text': _raw.text,
                    'other': _otherdata.text}
    person_entry['full_text'] = person_entry['text']
    return person_entry
