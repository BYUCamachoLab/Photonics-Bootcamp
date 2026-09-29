book:
	jupyter book build book

serve:
	cd book/_build/html && python -m http.server
