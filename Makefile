install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,W1203,W0702 ./modeling/retrain/create_retrain_dataset.py
	pylint --disable=R,C,W1203,W0702 ./modeling/conceptdrift/create_concept_dataset.py
	pylint --disable=R,C,W1203,W0702 ./modeling/datadrift/create_datadrift_dataset.py
	#pylint --disable=R,C,W1203,W0702 ./scripts/authentication.py &&\
	pylint --disable=R,C,W1203,W0702 ./scripts/datasets.py &&\
	pylint --disable=R,C,W1203,W0702 ./scripts/clusters.py

create_datasets:
	python ./modeling/retrain/create_retrain_dataset.py
	python ./modeling/conceptdrift/create_concept_dataset.py
	python ./modeling/datadrift/create_datadrift_dataset.py

all: install lint
