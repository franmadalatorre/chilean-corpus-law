# Corpus for chilean law
 Repository for different corpus extracted from chilean law (constitution, laws, specific codes)
 
Use the command below to install the packages according to the configuration file requirements.txt.

```console
$ pip install -r requirements.txt
 ```
 
 ## Extracting laws from the National congress library of Chile (https://www.bcn.cl/leychile/)
 
 To extact up to the law N°`X`, modify the variable to `MAX_LAW_NUMBER = X` in the file law_scraper.py and then run in terminal <br>
 ```console
 $ python law_scraper.py
 ```
