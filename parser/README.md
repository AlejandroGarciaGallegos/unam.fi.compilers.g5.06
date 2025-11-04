# Syntax Analyzer with PLY and SDT

This project implements a lexical and syntax analyzer using the **PLY (Python Lex-Yacc)** library.  
It recognizes basic variable declarations, arithmetic expressions, and print statements, and applies **Syntax-Directed Translation (SDT)** rules for basic semantic validation.

## Features

- Supports statements such as:
  - `int x = 10;`
  - `float y = 3.14 + 2 * 5;`
  - `print("Hello world");`
- Data types: `int` and `float`.
- Evaluates arithmetic expressions with operator precedence.
- Includes SDT rules for:
  - Type checking.
  - Detection of semantic errors (e.g., division by zero).
- Handles:
  - **Lexical errors:** illegal characters.
  - **Syntax errors:** malformed statements.
  - **Semantic errors:** type mismatch or division by zero.

## Project Structure

| File | Description |
|------|--------------|
| `lexer.py` | Defines tokens and handles lexical errors. |
| `parser.py` | Contains grammar rules and SDT semantic actions. |
| `main.py` | Entry point for running and testing the analyzer. |

## Example Usage

```bash
$ python main.py
>> int x = 10;
Parsing Success!
SDT Verified!

>> int y = 4.5;
Parsing Success!
SDT error...

>> print("Hello world");
Output: Hello world
Parsing Success!
SDT Verified!
```
