install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,W1203,W0702 analysis.py &&\
	pylint --disable=R,C,W1203,W0702 common_functions.py &&\
	pylint --disable=R,C,W1203,W0702 update_script.py &&\
	pylint --disable=R,C,W1203,W0702 one_time_historicals.py &&\
	pylint --disable=R,C,W1203,W0702 definitions.py

check_definitions:
	python definitions.py

update_records:
	python update_script.py

run_analysis:
	python analysis.py

all: install check_definitions update_records run_analysis lint
main_update: check_definitions update_records run_analysis
