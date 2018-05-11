def run_xml_data_transformation(bookseries, xml_doc, file_path):
    """
    Transforms data entries from a book and saves them to disk.
    :param bookseries: Instance of Bookseries class
    :param xml_doc: Parsed XML file with data entries to transform
    :param file_path: Directory path and file name stem that determines where
    to output new file
    :return: Path of new file
    """
    transformed_data = bookseries.transform_xml_data_for_fdp(xml_doc)
    return save_transformed_data_as_text(transformed_data, file_path)


def save_transformed_data_as_text(data, path):
    """
    Saves the transformed data in text format, with comments, in a way that the NLP parser
    can understand while retaining clear separation of where data entries begin and where
    they end.
    :param data: List of transformed data entries to write to disk
    :param path: Where to save the file, including original filename without extension
    :return: Path where file was saved
    """
    output_path = '{}_preprocessed.txt'.format(path)
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        output_file.write('\n\n'.join(data))
        output_file.write('\n')
    return output_path
