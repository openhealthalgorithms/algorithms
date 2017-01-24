## Overview

* There will be one single file for each algorithm in `OpenHealthAlgorithm` package.
* Each file will have a class containing only one public method which will return the risk score.
* There can be as many helping method as necessary, but all of them will be private, meaning they will not be exposed for public use.

## Preparing development environment

#### use virtual environment (optional)

go into the project directory and run the following command in terminal:

    $ pip install virtualenv
    $ virtualenv venv/oha

    # activate the virtualenv
    $ source venv/oha/bin/activate

    # to deactivate
    $ deactivate

#### install requirements

go into the project directory and run the following command in terminal:

    $ pip install -r requirements/dev.txt

## Coding Guideline

* __Document the code__:
 ```python
 class Algorithm():
     """
     What is the purpose of the Algorithm

     Example
     -------
        Give a complete example of its usage

        >>> from OpenHealthAlgorithms.Algorithm import Algorithm
        >>> params = {
        ...    'param1': 'value1', 'param2': 'value2',
        ... }
        >>> risk_score = Algorithm().public_method(params)
        >>> print risk_score
     """

     def public_method(params):
         """
         What does this method do

         Parameters
         ----------
         params: type_of_params(list, dict etc.)
             Description of the 'params' parameter.

         Example
         -------
            Example usage:

            >>> params = {
            ...    'param1': 'value1',
            ...    'param2': 'value2',
            ... }
            >>> public_method(params)

         Returns
         -------
         return_type(int, string etc.)
            What does the method return
         """
         pass
  ```
* __Code Quality and Readability__: use flake8 to maintain code quality and readability
 * run flake8: `flake8 OpenHealthAlgorithms`
* __Test Code__: Write testcode in the `tests` package. Test file name should be `test_(name of the algorithm).py` ex: `test_diabetes.py`
 * use nose to run the tests: `nosetests tests`
 * make sure tests cover 100% of the code. (run test with coverage `nosetests tests --with-coverage`)