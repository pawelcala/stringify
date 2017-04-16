# stringify.py

Stringify is a python tool for exporting localized strings files for Android and iOS (swift) projects from Google Docs spreadsheet.

## Installation steps:

1. Install python 3
1. Install dependencies: [**gspread**](https://github.com/burnash/gspread) and [**oauth2client**](https://github.com/google/oauth2client) with:
```
pip install -r requirements.txt
```
1. Head to [**Google Developers Console**](https://console.developers.google.com/project) and create a new project
1. Enable _Drive API_
1. Create credentials and copy _CLIENT_ID_ and _CLIENT_SECRET_
1. You are ready to go

## How to use:

You will be asked to login in to google docs on the first run. Copy token from redirected path ```http://localhost/code=TOKEN``` and press enter. TOKEN will be stored in ```.credentials``` file.


##### More info:
```
./stringify.py -h

optional arguments:
  -h, --help            show this help message and exit
  -d DEFAULT_LANG, --default-lang DEFAULT_LANG
                        Android default language. Default language sets values
                        folder without language postfix. If left 'en' is set.
  -n SPREADSHEET_NAME, --spreadsheet-name SPREADSHEET_NAME
                        Google Spreadsheet name.
  -p DEST_PATH, --dest-path DEST_PATH
                        Localized strings destination path. Should point on
                        project/module directory (Used in both modes - IMPORT
                        and EXPORT).
  -x XML_FILENAME, --xml-filename XML_FILENAME
                        Android xml or swift strings filename. Default:
                        strings.xml (Android), Localizable.strings (iOS)
  -m MODE, --mode MODE  Available modes: export_ios - exports/uploads ios
                        strings, export_android - exports/uploads android
                        strings, import_android - import/download Android
                        strings and create Google Spreadsheet, import_ios -
                        import/download iOS strings and create Google
                        Spreadsheet
  -o LOGS_OFF, --logs-off LOGS_OFF
                        Turns progress debug logs off
  -u OAUTH_CREDENTIALS_LOCATION, --oauth-credentials-location OAUTH_CREDENTIALS_LOCATION
                        oauth credentials location. Default: .credentials

```

## Sample spreadsheet:

  ![Sample spreadsheet](http://i.imgur.com/R7GRFA2.png)

* sample_spreadsheet is SPREADSHEET_NAME
* first row cells corespond strings languages
* first column cells are strings variable names

###### Example: Download Android strings
```
./stringify.py -n sample_spreadsheet -m import_android -x welcome.xml -p app/src/main/res
```

_Result:_

![Export Android](http://imgur.com/IzEEtFX.png)

###### Example: Download iOS strings
```
./stringify.py -n sample_spreadsheet -m import_ios -p resources
```

_Result:_

![Export iOS](http://imgur.com/ydxXr9z.png)

## Other:

Feel free to ask me a question, report a bug(s), send request for new feature.




