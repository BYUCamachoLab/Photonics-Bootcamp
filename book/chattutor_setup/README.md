# Building

From the root folder of the app run:
```sh
jupyter-book build --all book
python3 ./book/chattutor_setup/install.py # adding the chattutor script to all the html files
```

CORS needs to allow the url to make requests!!
For now this can only be tested locally.

# Testing locally

Checkout chattutor.config.js

- Start an instance of the main branch at port `5000` at `localhost`
- Go to config and set **TEST_MODE** to true and **SERVER_PORT** to `5000`
- Run the following commands to build the notebook and to add chattutor
one in venv (checkout main README for info on that)
```sh
jupyter-book build --all book
python3 ./book/chattutor_setup/install.py # adding the chattutor script to all the html files
```