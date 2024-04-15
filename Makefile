ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: jungmin

jungmin:
	PYTHONPATH=$(ROOT_DIR) streamlit run pages/3_jungmin.py
