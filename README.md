# **Scheme Interpreter**

A lightweight **Scheme interpreter** implemented in **Python**, designed as part of the **MIT 6.101: Fundamentals of Programming** course.  
This project demonstrates skills in **interpreter design, recursion, functional programming, error handling, and Python software engineering**.

---

## **Key Features**

- **Interactive REPL** – Write and evaluate Scheme code interactively.  
- **Variable Management** – Definitions, scoped frames, reassignment, and deletion.  
- **Functions** – Support for arithmetic, logic, user-defined functions, and lambdas.  
- **Error Handling** – Detects invalid syntax with informative error messages.  
- **Conditionals** – Includes `if`, `cond`, boolean logic (`#t`, `#f`), and comparison operators (`=`, `<`, `>`, `not`, etc.).  
- **Lists & Pairs** – Full support for `cons`, `car`, `cdr`, linked lists, and the empty list `()`.  
- **Built-in List Functions** – Standard utilities like `length`, `append`, `map`, `filter`, and `reduce`.  
- **Sequence Evaluation** – Execute multiple expressions in order with `begin`.  
- **File Input** – Load and run Scheme programs from `.scm` files.  
- **Command-Line Interface** – Run Scheme expressions directly from the terminal.  
- **Higher-Order Functions** – Functional constructs (`map`, `filter`, `reduce`) with lambda support.  

---

## **Technical Highlights**

- Written in **Python 3** using modular, testable code.  
- Implements **recursive evaluation** of Scheme expressions.  
- Demonstrates **functional programming concepts** in both Scheme and Python.  
- Robust **error handling and exception reporting** for invalid syntax.  
- Hands-on experience with **language parsing** and building interpreters from scratch.  

---

## **Repository Structure**

- `lab.py` – Entry point for the interpreter (REPL).  
- `scheme repl.py` – Core evaluation logic.  
- `web.py` – Web interface support.  
- `test_files/`, `test_inputs/`, `test_outputs/` – Test cases and example programs.  

---

## **Running the Interpreter**

1. **Clone this repository**:  
   ```bash
   git clone https://github.com/<47Alain>/LISP-interpreter-.git
   cd LISP-interpreter-

## **Launch the Interpreter**
```bash
   python3 lab.py

