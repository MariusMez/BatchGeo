# BatchGeo

This script is for batch editing your geocaches on geocaching.com.

It takes codes of geocaches, your login credentials (or more) and
input file with content to be placed into "Long Description".

## Features
* use Mozilla Firefox
* can replace text just between some specific tags or all at once (by string specified in `--border` argument, or set to "False" for replacing all text)
* handle different users (try to edit the geocache by each user - ends when it succeed)
* logs everything into log file, so you don't use original text by mistake
* by default it only show changes but do not submit them (you have to pass `--submit` argument to submit changes)

## Examples

	python batchgeo.py --verbose --codes "GC4BV7M,GC40QGM,GC40QGQ,GC40QGX,GC584XV" --logins "Bob:bobpasswd,Julia:juliapasswd" --file "texttoinclude.html" --border "<!--DONTCHANGE-->"

This will try to edit geocaches with codes `GC4BV7M,GC40QGM,GC40QGQ,GC40QGX,GC584XV` as
users Bob and Julia. Content of `texttoinclude.html` will included between occurences of
`<!--DONTCHANGE-->` string, e.g.:

Long Description:

		Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
		et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
		aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
		cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
		sunt in culpa qui officia deserunt mollit anim id est laborum.
		<!--DONTCHANGE-->
		TEXT TO BE REPLACED BY CONTENT OF texttoinclude.html
		<!--DONTCHANGE-->
		Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
		et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
		aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
		cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
		sunt in culpa qui officia deserunt mollit anim id est laborum.

Changes will not be submitted. Firefox will stay open and you as a user can submit changes after review.
If you believe in the script, you can pass argument `--submit` for also submitting changes imediately.

If you set `--border "False"`, the text will be replaced completely.

## Requirements

Only `selenium (3.5.0)`, Python 3+ (`Python 3.6.*` tested), Firefox (version `54.0.1` tested)
Please read : http://selenium-python.readthedocs.io/installation.html to install the latest Selenium version and appropriate driver.

## Known issues
* you must use Firefox on fullscreen
* sometimes firefox throws some weird errors when inserting text into area code. It was because
of formatting of input html file. After using http://www.dirtymarkup.com/ it works.
