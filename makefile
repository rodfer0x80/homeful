.PHONY: build
build: # Build python venv with deps
	scripts/build.sh

.PHONY: clean
clean: # Cleanup venv build
	scripts/cleanup.sh

.PHONY: search
search: # Run main script
	echo "search" | scripts/run.py

.PHONY: spam
spam: # Run main script
	echo "spam" | scripts/run.py

.PHONY: test
test: # Run main script
	scripts/test.sh

