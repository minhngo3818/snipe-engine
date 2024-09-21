# Notes: Install gcc in order to use makefile
.PHONY: run test custom-hash avro-dict

UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
    PYTHON := python3
else ifeq ($(UNAME), Windows)
    PYTHON := python
endif


install:
	chmod +x install.sh && ./install.sh

requirements:
	pip freeze > requirements.txt

format:
	black .

searcher-server:
	uvicorn api.run:app --reload

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

run:
	${PYTHON} -m snipe


# Test commands
test:
	@$(MAKE) $(filter-out $@,$(MAKECMDGOALS))

custom-hash:
	${PYTHON} ./tests/test_custom_hash.py

avro-dict:
	${PYTHON} ./tests/test_avro_dict.py
