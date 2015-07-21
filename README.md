# qa_commissions
Various scripts for testing commissions importers.

## Installation
```sh
$ git clone https://github.com/JoeFoulkes/qa_commissions.git
$ cd qa_commissions
$ mkvirtualenv qa_commissions {only make it once, use 'workon' thereafter}
$ pip install -r requirements.txt
```

## Environment Variables
A couple of environment variables are required before you can run the script...
 * GALVATRON_USER {this should be the user that connects to the galvatron database}
 * GALVATRON_PASS {this should be the above users password}
... if your password contains odd characters, you might need to wrap it in double-quotes.

## Usage Examples...
### Groupon
This script takes a couple of arguements, '--from' and '--to' for the to/from dates to test. If omitted it will use todays date for both, but bear in mind the importer needs to have been run on the specified date
```sh
$ py.test -q groupon/test.py --from=2015-07-02 --to=2015-07-02
```

## Output
Standard pytest output, depends on the params you pass.
