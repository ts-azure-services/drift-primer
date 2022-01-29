install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

setup_run:
	./scripts/setup/create-aml-resources.sh
	python ./scripts/setup/clusters.py
	python ./scripts/setup/upload_baseline_data.py

lint:
	pylint --disable=R,C,W1203,W0702,E0110,W0703 ./modeling/retrain/create_retrain_dataset.py
	pylint --disable=R,C,W1203,W0702,E0110,W0703 ./modeling/conceptdrift/create_concept_dataset.py
	pylint --disable=R,C,W1203,W0702,E0110,W0703 ./modeling/datadrift/create_datadrift_dataset.py

create_datasets:
	python ./modeling/retrain/create_retrain_dataset.py
	python ./modeling/conceptdrift/create_concept_dataset.py
	python ./modeling/datadrift/create_datadrift_dataset.py

batch_score:
	./scripts/setup/batch-score.sh

all: install lint
