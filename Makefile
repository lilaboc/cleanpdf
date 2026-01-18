install:
	uv tool install -e .

run:
	uv tool run cleanpdf

run-combine:
	uv tool run combinepdf

sync:
	uv tool install -e .

clean:
	@-rm -rf .venv
	@-rm -rf cleanpdf.egg-info
	uv tool uninstall cleanpdf
