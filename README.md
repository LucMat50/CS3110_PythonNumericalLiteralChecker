<div align="center">

# 🐍 PYTHON NUMERICAL LITERAL CHECKER

**CS 3310.01 — Formal Languages & Automata**

### Team: <em>**Fine**ite Automa**freaks**</em>

</div>

---

## 🔖 Overview

Accept or reject **Python numerical literals** using automata theory. We designed NFAs for the specified literal families(decinteger, octinteger, hexinteger, and floating point) and implemented them in code from scratch.

---

## Team members
| # | Member | GitHub | Roles |
|---|--------|--------|--------------|
| 1 | Lucia Maturino Iniguez | [@LucMat50](https://github.com/LucMat50) | - Designed Decinteger NFA<br>- Coded NFA class following formal definition(states, transitions, alphabet, start state, accept state) <br>- NFA class performs transitions and runs input |
| 2 | Jeannette Ruiz | [@jeanrnette](https://github.com/jeanrnette) | - Designed OctInteger and Floating Point NFA<br>- Added epsilon-closure transitions<br>- Modified input reading to run input through multiple NFA's |
| 3 | Medha Swarnachandrabalaji  | [@MedhaS1](https://github.com/MedhaS1) | - Designed HexInteger NFA<br>-Coded HexInteger NFA |

---

## Task Completion
- [x] Task 1: Recognize Python Decinteger
- [x] Task 2: Expand your program to recognize Python octinteger and hexinteger
- [x] Extra Credit: Expand your program to recognize Python floating point literals

---

## Notes

- Our final program (meaning the final NFA including all decinteger, octinteger, hexinteger, and floating point literals) resides in the 'FINAL' directory.
- User is prompted with 3 menu options: (1)TEST INPUT FILE, (2)TEST USER INPUT, (3)EXIT PROGRAM.
- The program will continue to run while the user enters 'y'.

**If choosing Option 1 - Test Input File**
- In order for the program to run using an input file, the file must be named 'in.txt' and must be placed within the 'FINAL' folder as we specified the program to run using 'FINAL\in.txt' as the designated input file.
- The results will be printed in 'out.txt' located in the 'FINAL' directory, following this format: 
```
TEST INPUT: {user_input} | EXPECTED RESULT: {expected_result} | ACTUAL RESULT: {reject_or_accept} | NFA(S): {recognized_nfas} | PASS/FAIL: {pass_or_fail}
```
- A 'pass' indicates that the expected result matches the actual result.
- A 'fail' indicates they do not match.

**If choosing Option 2 - Test User Input**
- The user simply enters a string, and the result is printed as:
```
TEST INPUT: {user_input} | ACCEPT/REJECT: {reject_accept} | NFA(S): {recognized_nfas}
```

**If choosing Option 3 - Exit Program**
- The program will **terminate**.
