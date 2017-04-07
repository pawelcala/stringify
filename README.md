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

```
./stringify.py 
--name SPREADSHEET_NAME 
--default ANDROID_DEFAULT_LANGUAGE 
--path ANDROID_STRINGS_EXPORT_PATH 
--ipath IOS_EXPORT_PATH
```
You will be asked to login in to google docs on the first run. Copy token from redirected path ```http://localhost/code=TOKEN``` and press enter. TOKEN will be stored in ```.credentials``` file.

All parameters are optional except for SPREADSHEET_NAME.

## Sample spreadsheet:

  ![Sample spreadsheet](http://i.imgur.com/R7GRFA2.png)

* sample_spreadsheet is SPREADSHEET_NAME
* first row cells corespond strings languages
* first column cells are strings variable names


## Other

Why there is no abstraction, no classes, etc? I wanted to create one-filer so it can be easy to distribute and fast to use.

Feel free to ask me a question, report a bug(s), send request for new feature.




