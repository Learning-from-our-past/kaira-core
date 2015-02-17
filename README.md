# Matrikel book -> Excel extractor for Finnish soldiers
This is a Python software which lets user to convert "Suomen Rintamamiehet 1939-43" matrikel books to a csv-format. The book series was originally published in 1970s and they contain brief descriptions of the soldiers, their life, children, spouses etc. This data is scientifically interesting but difficult to analyze statistically in a written format. 

# What does this tool do?
At the moment it lets the user to extract most of the interesting information from a subset of soldier matrikels to a csv-format. 

#How does it work?
![Imgur](http://i.imgur.com/Obp8gM8.jpg)
1. First you need a digital scan of the book. Preferably as good quality as possible.
2. Run an OCR for the scanned documents to get the raw text in a simple .txt format. Picking up a good OCR-software and settings is a bit trial and error. We used Adobe's and will be using ABBYY Finereader because of the good support for Finnish language.
3. We run "chunker" for the raw text-file which tries to isolate every one person entry to a separate XML-tag for easy processing. This is done with a regex which looks for patterns common in beginning of the one soldier's entry. It works most of the time but might make mistakes which has to be fixed in the fixer-tool (more about that below).
4. We ran the actual extractor software which reads the XML-file and runs multiple tailored regexes and other domain-specific logic and generates a csv-file containing the data. At this point user can use fixing-tool to find missing information, edit the xml-file to fix the extraction errors and rerun the process.

#Fixing tool
At the moment the fixing-tool (can be found from GUI-tools) is **really** crude. Basically it is cobbled together from some Tkinter examples so that I could easily test and see the data and possible errors. There will be a much better fixing tool with actually working and usable GUI in future!

Instead of Tkinter future gui will most likely use PyQt5. 

#Usage
Since this software only works for the certain book-series you obviously need them for the source-data. There is short sample XML file provided with anonymized data to test the program. To run the project, I recommend opening it in the Pycharm and running **GUITool/processDialog.py** which first generates the csv and then opens fixing-tool to show data on the missing data (and simple tools to fix them).

You'll need the Python packages described in *requirements.txt* file as well as Python 3.4.

#Code
For those interested in checking the sourcecode, I suggest starting from either **processData.py** or **dataExtraction.py**. The software basically reads provided XML-file one node at a time and run multiple extractor-classes for each and saves the data to be saved in the csv.

#### Style and architecture
The software was initially supposed to extract only couple pieces of information. However, the requirements expanded over time resulting to an architecture which wasn't planned well ahead of time. This combined with high need to know the domain-specific information (getting familiar with the source text, patterns...) may make it difficult to understand certain design choices.

As for style, since I have been the only programmer in this project, the naming conventions remind more of Java (which I like) than PEP8-conventions. I might rename everything in a more Pythonic way in future.

#Future
The software is not yet ready. The fixing-tool will need to be rewritten and there are still stuff which needs to be refactored. Later there will also be extractors for other similar books but they'll likely be rewritten by using some of the components from this codebase. Ideally I'd like the fixing-tool to be compatible with different extractors.
