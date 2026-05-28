PYTHON ?= python3
PNPM ?= pnpm
NODE ?= node
DEV_SERVER_ADDRESS ?= 127.0.0.1

SITE_DIR := site
CLEAN_MANIFEST := scripts/clean-manifest.txt
SITE_NODE_MODULES_DIR := $(SITE_DIR)/node_modules

.PHONY: all build rebuild serve preview test install clean distclean help

all: build

build:
	$(PYTHON) scripts/build_llms_txt.py
	$(PYTHON) scripts/sync_starlight.py
	$(PNPM) --dir $(SITE_DIR) exec astro build
	$(PYTHON) scripts/postprocess_site.py

rebuild: clean build

serve:
	$(PYTHON) scripts/build_llms_txt.py
	$(PYTHON) scripts/sync_starlight.py
	$(PNPM) --dir $(SITE_DIR) exec astro dev --host $(DEV_SERVER_ADDRESS)

preview: build
	$(PNPM) --dir $(SITE_DIR) exec astro preview

test: build
	$(NODE) --test $(SITE_DIR)/scripts/built-site.test.mjs

install:
	$(PNPM) --dir $(SITE_DIR) install

clean:
	$(PYTHON) scripts/clean_generated.py $(CLEAN_MANIFEST)

distclean: clean
	rm -rf $(SITE_NODE_MODULES_DIR)

help:
	@printf '%s\n' \
		'Targets:' \
		'  make build     Regenerate public LLM docs, sync Starlight content, and build site/dist.' \
		'  make rebuild   Clean generated site output, then run make build.' \
		'  make serve     Regenerate public LLM docs, sync Starlight content, and start Astro dev server.' \
		'  make preview   Build, then preview site/dist.' \
		'  make test      Build, then verify site/dist routes, LLM assets, and analytics.' \
		'  make install   Install site dependencies with pnpm.' \
		'  make clean     Remove generated outputs listed in scripts/clean-manifest.txt.' \
		'  make distclean Run clean and remove site/node_modules.'
