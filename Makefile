ZIP_FILE = lambda.zip
PY_FILES = lambda_function.py github.py jira.py event.py column.py
TMP_DIR = ./tmp

$(ZIP_FILE): $(PY_FILES) setup.cfg
	mkdir $(TMP_DIR)
	pip install requests -t $(TMP_DIR)
	cd $(TMP_DIR) && zip -r $@ *
	mv $(TMP_DIR)/$@ ./$@
	rm -rf $(TMP_DIR)
	zip -u $@ $^

.PHONY: clean
clean:
	rm $(ZIP_FILE)
