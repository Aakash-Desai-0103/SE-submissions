
# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) Before Fix | Description | Fix Approach |
|---|---|---|---|---|
| Insecure temporary file creation | Security — Medium | 40 | Bandit B306 flagged the use of `tempfile.mktemp()`, which can cause a race condition. | Replaced it with `tempfile.NamedTemporaryFile()` and `delete=False`. |
| Assertion used for runtime validation | Security — Low | 61 | Bandit B101 warned that assertions may be removed when Python runs in optimized mode. | Replaced the assertion with an explicit `if` condition and `ValueError`. |
| Mutable default argument | Code quality | 10 | Pylint W0102 flagged `logs=[]` as a dangerous mutable default. | Changed the default to `None` and initialized the list inside the function. |
| Bare exception | Reliability | 18 | Pylint W0702 and Flake8 E722 flagged a bare `except:` that could hide unrelated errors. | Caught the expected `ValueError` and handled unknown asset IDs explicitly. |
| Unused import | Code quality | 2 | Pylint W0611 and Flake8 F401 flagged the unused `logging` import. | Removed the unused import. |
| File handling without context managers | Code quality | 34–43 | Pylint flagged file operations without context managers and explicit encoding. | Used `with` statements and UTF-8 encoding. |
| Missing docstrings | Code quality | Multiple | Pylint reported missing module and function docstrings. | Added descriptive docstrings. |
| Incorrect function naming | Style | 46 | Pylint C0103 flagged `printAlerts()` for not following snake_case. | Renamed it to `print_alerts()`. |
| Formatting violations | Style | Multiple | Flake8 reported missing blank lines, a long line, and a trailing blank line. | Corrected spacing, wrapped long lines, and removed extra trailing blank lines. |
| Empty asset ID | Functional bug | 53 | The original program accepted an empty asset ID. | Added validation to reject empty or whitespace-only IDs. |
| Duplicate asset registration | Functional bug | 54 | Registering an existing asset overwrote its original record. | Reject duplicate IDs to preserve the existing record. |
| Invalid service date | Functional bug | 55–60 | Invalid dates could be stored and cause later parsing errors. | Validate the date before updating the asset record. |
| Negative inspection interval | Functional bug | 57 | A negative interval made inspection checks unreliable. | Require a positive integer and use a valid 90-day interval. |

