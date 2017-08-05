extract-all:
	python main.py -i material/siirtokarjalaiset_I.xml -o material/siirtokarjalaiset_I.json
	python main.py -i material/siirtokarjalaiset_II.xml -o material/siirtokarjalaiset_II.json
	python main.py -i material/siirtokarjalaiset_III.xml -o material/siirtokarjalaiset_III.json
	python main.py -i material/siirtokarjalaiset_IV.xml -o material/siirtokarjalaiset_IV.json

test-set:
	python main.py -i material/testset_I.xml -o material/testset_I.json

