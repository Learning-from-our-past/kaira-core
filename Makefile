create-venv:
	virtualenv -p python3 kaira-venv

setup:
	pip install -r requirements.txt;
	wget https://github.com/Learning-from-our-past/kaira-core/releases/download/mongodump2/geonames_dump.zip
	unzip geonames_dump.zip
	mongorestore dump
	rm -rf dump/
	rm -rf geonames_dump.zip

extract-all:
	python main.py -i material/siirtokarjalaiset_I.xml -o material/siirtokarjalaiset_I.json
	python main.py -i material/siirtokarjalaiset_II.xml -o material/siirtokarjalaiset_II.json
	python main.py -i material/siirtokarjalaiset_III.xml -o material/siirtokarjalaiset_III.json
	python main.py -i material/siirtokarjalaiset_IV.xml -o material/siirtokarjalaiset_IV.json

extract-all-four-processes:
	tasks/multi_process_extractor.sh -p 4

extract-all-two-processes:
	tasks/multi_process_extractor.sh -p 2

extract-test-set:
	python main.py -i material/testset_I.xml -o material/testset_I.json

test:
	python -m pytest
