# TODO

## EDR

- Instance should be file/date? Show only available date, or fetch others if asked?

## Code

- Move to github
- Config? Or just use parameters? Filename is currently hardcoded.
- Clean old datafiles
- Replace deprecated cgi module
- Something is sub-optimal as code runs fine with `uvicorn app.main:app`, but pylint and vs code default debugging complains on module imports.
