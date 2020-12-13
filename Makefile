.PHONY: help pi_install preproces run cleanup

help :
	@echo "Requirements to run: python3.6 and above"
	@echo "Python libraries: ezdxf, tqdm"
	@echo "Step 1: Preprocessing of dxf into pickle: make preprocess file=<filepath> output=<output path>"
	@echo "Step 2: Run program: make run input=<pickle path>"

pi_install: 
	./scripts/setup_pi.sh

preprocess:
	@echo "Preprocessing of dxf into pickle"
	@echo "USAGE: make preprocess file=<filepath> output=<output path>"
	@echo "Output defaults to ./resources/pickle/`file`_pickle"
	mkdir -p ./resources/pickle
	python3 preprocess.py $(file) $(output)

run:
	@echo "Running of dxf from pickle in preprocess"
	@echo "USAGE: make run input=<input path>"
	@echo "Input defaults to ./resources/pickle/`file`_pickle"
	python3 main.py $(input)

cleanup:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +