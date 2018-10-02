SHELL := /usr/bin/env bash

default: help ;

venv: venv/bin/activate
venv/bin/activate:
	test -e venv/bin/activate || virtualenv -p python3 --prompt "(ipc-demo) " --distribute venv
	touch venv/bin/activate

devbuild: venvinfo/devreqs~
venvinfo/devreqs~: venv
	( \
		source venv/bin/activate; \
		pip install jupyter; \
		pip install lightlab; \
	)
	@mkdir -p venv/venvinfo
	touch venv/venvinfo/devreqs~

clean:
	rm -rf venv;

jupyter: devbuild
	( \
		source venv/bin/activate; \
		jupyter notebook; \
	)

jupyter-password: devbuild
	( \
		source venv/bin/activate; \
		jupyter notebook password;
	)

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "--- development ---"
	@echo "  devbuild          install dev dependencies, build lightlab, and install inside venv"
	@echo "  jupyter           start a jupyter notebook for development"
	@echo "  jupyter-password  change your jupyter notebook user password"


.PHONY: help default jupyter-password
