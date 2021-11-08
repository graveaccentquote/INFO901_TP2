all: install run

install:
	pip install -r requirements.txt

run:
	python3 main.py ./resources/chablais-orig.png ./resources/test_out.png

clean:
	rm -rf __pycache__
	rm -rf ./src/__pycache__