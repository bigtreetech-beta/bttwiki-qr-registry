# makefile config 
VENV := venv
PYTHON := $(VENV)/bin/python3
BUILD_DIR := .build
QRCODE_DIR := $(BUILD_DIR)/qrcode
QRCODE_ZIP := $(BUILD_DIR)/qrcode.7z

# default target
.PHONY: init product-list qrcode pack-build all clean

# init venv
init:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "python venv init in $(VENV)"

# build product list 
product-list: init
	$(PYTHON) product-list-gen.py
	@echo "finish build product list"

# build qrcode 
qrcode: product-list
	$(PYTHON) qrcode-gen.py
	@echo "finish build qrcode"

# package qrcode
pack-build: qrcode
	@echo "pack $(QRCODE_DIR) -> $(QRCODE_ZIP)..."
	7z a -t7z $(QRCODE_ZIP) $(QRCODE_DIR)
	@echo "finish pack $(QRCODE_ZIP)"

# build all
all: pack-build
	@echo "finish build"

# clean build file 
clean:
	rm -rf $(BUILD_DIR)
	@echo "clean build result"
