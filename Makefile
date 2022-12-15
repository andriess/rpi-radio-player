ifeq ($(OS),Windows_NT)
    TOUCH = type nul >>.pip_install_timestamp & copy .pip_install_timestamp +,,
	PYTHON = py
else
    TOUCH = touch .pip_install_timestamp
	PYTHON = python
endif


.PHONY: all
all: test

.PHONY: init
init: .pip_install_timestamp
.pip_install_timestamp: requirements.txt
	$(PYTHON) -m pip install -r requirements.txt
	$(TOUCH)

.PHONY: test
test: .pip_install_timestamp
	nosetests tests