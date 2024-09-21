# Determine the operating system
UNAME := $(shell uname)

# Conditionally set the Python interpreter based on the operating system
ifeq ($(UNAME), Linux)
    PYTHON := python3
else
    PYTHON := python
endif

# Use python3 for linux system
install:
	@$(PYTHON) -m pip install packages/spacetime-2.1.1-py3-none-any.whl
	@$(PYTHON) -m pip install -r packages/requirements.txt

launch:
	@$(PYTHON) launch.py

# Restart the crawling operation, refresh all stored data
relaunch:
	@$(PYTHON) launch.py --restart


