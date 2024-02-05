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