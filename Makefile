release:
	# Update __init__.__version__
	# Tag.
	git clean -fxd
	pip install build twine
	python -m build --sdist
	echo "twine upload dist/*tar.gz"
