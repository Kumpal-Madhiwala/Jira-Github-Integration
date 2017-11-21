ZIP_FILE = lambda.zip
PY_FILES = lambda_function.py github.py jira.py event.py

$(ZIP_FILE): $(PY_FILES) setup.cfg
	mkdir lib
	pip install requests -t lib
	zip -r $@ $^ lib/*
	rm -rf lib

.PHONY: clean
clean:
	rm $(ZIP_FILE)
