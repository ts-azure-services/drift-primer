install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,W1203,W0702 ./modeling/create_data.py &&\
	pylint --disable=R,C,W1203,W0702 ./modeling/data_analysis.py &&\
	pylint --disable=R,C,W1203,W0702 ./scripts/authentication.py &&\
	pylint --disable=R,C,W1203,W0702 ./scripts/datasets.py &&\
	pylint --disable=R,C,W1203,W0702 ./scripts/clusters.py

retrain:
	python ./modeling/retrain/create_retrain_dataset.py
	
concept_dataset:
	python ./modeling/conceptdrift/create_concept_dataset.py

datadrift_dataset:
	python ./modeling/datadrift/create_datadrift_dataset.py

all: install lint
