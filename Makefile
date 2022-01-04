install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,W1203,W0702 ./modeling/create_data.py &&\
	pylint --disable=R,C,W1203,W0702 ./modeling/data_analysis.py


all: install lint
