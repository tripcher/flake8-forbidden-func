# flake8-forbidden-func

An extension for flake8 that forbids some functions in some modules.

## Installation

```terminal
pip install flake8-forbidden-func
```

## Example

```python

# users/views.py
from users import User
import datetime


def test_view():
    print(datetime.datetime.now())
    faz = User.objects.all().annotate().filter(a=2)
    baz = bar_func()

    if faz == baz:
        fuz = q.filter(a=1)
        return fuz.bar()
```

```
# setup.cfg
[flake8]
forbidden-functions =
    *.views: *.filter, views module should not use ORM filter
    *: datetime.datetime.now, we use django utils
allowed-functions =
    *.selectors: *.objects.*, only selectors module should use ORM
```

Usage:

```terminal
$ flake8 users/views.py
users/views.py:6:11: CFF001 datetime.datetime.now call is forbidden,since we use django utils.
users/views.py:7:11: CFF001 *.objects.* call is forbidden, since only selectors module should use ORM.
users/views.py:7:11: CFF001 *.objects.* call is forbidden, since only selectors module should use ORM.
users/views.py:7:11: CFF001 *.objects.* call is forbidden, since only selectors module should use ORM.
users/views.py:11:15: CFF001 *.filter call is forbidden, since views module should not use ORM filter.
```

Tested on Python 3.7+ and flake8 4.0+.

## Error codes

| Error code |                     Description          |
|:----------:|:----------------------------------------:|
|   CFF001   | call is forbidden, since reason |
