# python-ire

Python wrapper around the IRE Irator API.

## Usage

To setup the pre-commit hooks, run `make develop` after cloning the repository.

Next, rename the `python_stub` directory to your module name. Make sure that it conforms to module
naming requirements (i.e. no dashes).

Then, replace all the references to `python-stub` in the following files:

1. `setup.py`
2. `tox.ini`
3. `tests/test_sanity.py`

## Writing and Running Tests

To run the tests, run the command `make test`.
