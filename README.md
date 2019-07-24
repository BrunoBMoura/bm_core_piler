# bm_core_piler ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)
Cminus compiler for the BM_CORE architecture designed using Python3 and Antlr4 used as the final project for the Laboratory of Compilers lecture.

## How to use it

1. Install [pipenv](https://github.com/pypa/pipenv)

2. Install [Antlr 4.7](https://github.com/BrunoBMoura/bm_core_piler/blob/master/howtodo.txt)

3. Clone this repository

4. `cd` into the repository

5. Execute `pipenv --python python3.6 install` to install the dependencies

6. Execute `antlr4 -Dlanguage=Python3 -visitor -o bm_core_piler/gen cminus.g4` to generate the grammar parser

7. Execute `pipenv run python -m bm_core_piler --<option> --file programs/<file_name>.cminus`

## Notes and options

The compiler runs as a Python module, so you always have to run `python -m bm_core_compiler` to execute it

To run the lexical analysis, use the option `--lex`

To run the syntactic analysis, use the option `--syn`

To run the semantic analysis, use the option `--sem`

To run the compiler over a file, use the option `--<file_name>`

## Synthesizing

To synthesize the Cminus language use the option `--synth`

To specifie the initial memory position from which data will start to be stored use the option `--mem <int_number>`

Once you run, for example: 

`pipenv run python -m bm_core_piler --synth --mem 100 --prog --file programs/PROGAM_FILES/prog_1_pow_net.cminus` 

or

`pipenv run python -m bm_core_piler --synth --file programs/SYSTEM_CODE/BM32OS.cminus` 

to finish translating the generated assembly to it's respective binary values, run:

`./bin_script.sh` 

## Notes

Finally, huge thanks to [Ivan](https://github.com/ivandardi) for helping on this project at it's early days.
