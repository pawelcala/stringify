# stringify.py

Stringify is a python tool for exporting localized strings files for Android and iOS (swift) projects from Google Docs spreadsheet.

## Installation steps:

1. Install [**gspread**](https://github.com/burnash/gspread):
```
pip install gspread
```

2. Install [**oauth2client**](https://github.com/google/oauth2client):
```
pip install oauth2client
```

3. Head to [**Google Developers Console**](https://console.developers.google.com/project) and create a new project
4. Enable _Drive API_
5. Create credentials and copy _CLIENT_ID_ and _CLIENT_SECRET_
6. You are ready to go

## How to use:
##### Basic use:
```
./stringify.py -n spreadsheet_name
```
You will be asked to login in to google docs on the first run. Copy token from redirected path ```http://localhost/code=TOKEN``` and press enter. TOKEN will be stored in ```.credentials``` file.


##### More info:
```
./stringify.py -h

optional arguments:
  -h, --help            show this help message and exit
  -d DEFAULT_LANG, --default-lang DEFAULT_LANG
                        Android default language
  -n SPREADSHEET_NAME, --spreadsheet-name SPREADSHEET_NAME
                        Google Spreadsheet name
  -p EXPORT_PATH, --export-path EXPORT_PATH
                        Localized strings destination path
  -x EXPORT_XML_NAME, --export-xml-name EXPORT_XML_NAME
                        Android xml name. Default: strings.xml
  -m MODE, --mode MODE  Available modes: EXPORT_IOS - exports ios strings,
                        EXPORT_ANDROID - exports android strings,
                        IMPORT_ANDROID - import Android strings and create
                        Google Spreadsheet, IMPORT_IOS - import iOS strings
                        and create Google Spreadsheet, EXPORT_ALL (default) -
                        exports both Android and iOS
  -o LOGS_OFF, --logs-off LOGS_OFF
                        Turns progress logs off

```

## Sample spreadsheet:

  ![Sample spreadsheet](http://i.imgur.com/R7GRFA2.png)

* sample_spreadsheet is SPREADSHEET_NAME
* first row cells corespond strings languages
* first column cells are strings variable names

###### Example: Export Android strings
```
./stringify.py -n sample_spreadsheet -m EXPORT_ANDROID -x welcome.xml -p app/src/main/res
```

_Result:_

![Export Android](http://imgur.com/IzEEtFX.png)

## Other

Why there is no abstraction, no classes, etc? I wanted to create one-filer so it can be easy to distribute and fast to use.

Feel free to ask me a question, report a bug(s), send request for new feature.




