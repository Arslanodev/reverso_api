# Project Description

Simple library for scraping data from "Context Reverso" asynchronously

### Usage example
```python
from reverso_api import ReversoContextAPI

api = ReversoContextAPI(
    source_texts= ["sprechen", "vorweisen"],
    source_lang= "de",
    target_lang= "en",
    )

data = api.get_data()

for translations, examples in data:
    print(translations)
    print(examples)
```

## How to install
This package has not been uploaded to pypy.org so that's why you will need to install it from github repository

Simply run command:
```bash
pip3 install git+https://github.com/Arslanodev/reverso_api.git
```

This project is in development stage. But you can use this package in your projects.