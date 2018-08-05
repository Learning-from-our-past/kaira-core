# ![alt text](http://i.imgur.com/vBIAv3m.png "Kaira logo") Kaira-core

Main module containing logic for data extraction and command line interface.

## Dependencies
* Python 3

## Setup
```
virtualenv -p python3 kaira-venv
source kaira-venv/bin/activate
pip install -r requirements.txt
```

If you wish to chunk the html files with duplicate filtering, you will also need ssdeep. Installation of ssdeep is 
done through pip, but you also need to install ssdeep on your system, which can be done with apt:
```
sudo apt-get install ssdeep libfuzzy-dev 
```
More on ssdeep installation can be found [here](http://python-ssdeep.readthedocs.io/en/latest/installation.html)

If you need to generate the XML files with the CoNLLU/NLP data, you will need to perform the nlp-setup step:
```
inv nlp-setup
```

Note that ssdeep pip-package seems to be difficult to install on MacOS since it was tested
only on Linux systems according to their documentation. Ignore the dependency on MacOS 
and install other packages from `requirements.txt`. Everything else than chunking and
duplicating code will work and affected tests are skipped when ssdeep is not available.

# Attribution
Please cite if you use this software or datasets generated by it in your research:
> T. Salmi, J. Kallioniemi, J. Loehr. Kaira-core [computer software]. Lammi Biological Station 2018
> Available at https://github.com/Tumetsu/Kaira
