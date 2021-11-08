all: install run

install:
	pip install -r requirements.txt

run:
	python3 main "test.png" "test_out.png"
