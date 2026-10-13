.PHONY: book serve clean

book:
	cd book && jupyter book build --html

serve:
	cd book && jupyter book start

clean:
	cd book && jupyter book clean --all --yes
