<div align="center">

# ⚡ TinyCompiler

**A lightweight, single-pass compiler that translates a custom imperative source language directly into optimized target C code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)]()

[Architecture](#-architecture--pipeline) •
[Features](#-key-features) •
[Getting Started](#-getting-started) •
[Language Specification](#-language-specification) •
[Roadmap](#-roadmap)

</div>

---

## 📌 Overview

**TinyCompiler** is an end-to-end compiler designed to transform custom high-level code into executable binaries via target C generation. It features a complete frontend and backend pipeline built from scratch, handling tokenization, syntax validation, variable state tracking, and source-to-source C translation.

### Core Compiler Concepts Demonstrated:
* **Lexical Analysis:** Custom scanner for tokenizing source code streams while filtering noise and comments.
* **Recursive Descent Parsing:** Grammar-driven syntax verification without third-party parser generators.
* **Symbol Table Management:** Compile-time scope and variable declaration validation.
* **C Code Generation:** Direct emission of portable, structured C code targeting standard C execution runtimes.

---

## 🏗 Architecture & Pipeline

The compilation pipeline converts custom source files into compiled native binaries through three distinct phases:

┌──────────────────┐      ┌──────────────────┐      ┌───────────────────┐      ┌─────────────────┐
│   Source Code    │ ───> │  Lexical         │ ───> │  Recursive        │ ───> │  C Code         │
│   (*.tiny)       │      │  Analyzer        │      │  Descent Parser   │      │  Emitter        │
└──────────────────┘      └──────────────────┘      └───────────────────┘      └─────────────────┘
                                                                                       │
                                                                                       ▼
                                                                             ┌─────────────────┐
                                                                             │ Native Binary   │
                                                                             │ (via GCC/Clang) │
                                                                             └─────────────────┘

### 1. Lexical Analyzer (`lexer.py`)
Scans raw source text character-by-character, recognizes language primitives (keywords, variables, literal values, and comparison operators), and streams strongly-typed tokens to the parser.

### 2. Parser & Symbol Table (`parser.py`)
Executes a deterministic recursive-descent parsing strategy. It enforces strict grammatical syntax and maintains an internal symbol table to detect undeclared variable references at compile time.

### 3. Code Emitter (`emitter.py`)
Generates standardized target C source code (`out.c`), wrapping logic within native function structures and standard I/O includes.

---

## ✨ Key Features

* **Zero External Dependencies:** Built using core standard libraries—no external lexer/parser generators like Flex or Bison.
* **Single-Pass Compilation:** Rapid code generation from source directly to target code in a single execution pass.
* **Portable Output:** Generates clean, standard C output compatible with any standard C compiler (`gcc`, `clang`, `msvc`).
* **Precise Error Diagnostics:** Custom error handling pinpointing invalid syntax and unexpected tokens during build time.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+ (or your primary language runtime)
* Any C compiler (`gcc`, `clang`, or `gcc` via MinGW on Windows)

### Installation & Usage

1. Clone the Repository:
   git clone https://github.com/your-username/tiny-compiler.git
   cd tiny-compiler

2. Compile a Source File:
   python compiler.py main.tiny

3. Build and Run the Output Binary:
   gcc out.c -o program
   ./program

---

## 📜 Language Specification

The compiler processes imperative syntax structured as follows:

# Program: Print numbers from 1 to 5
PRINT "Starting loop..."
LET x = 1
WHILE x <= 5 DO
    PRINT x
    LET x = x + 1
ENDWHILE

### Supported Grammar Primitives
* **Control Flow:** `IF ... THEN ... ENDIF`, `WHILE ... DO ... ENDWHILE`
* **Input / Output:** `PRINT` (strings and expressions), `INPUT`
* **Variables & Expressions:** `LET` assignments, integer literals, standard arithmetic (`+`, `-`, `*`, `/`)
* **Conditional Operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`

---

## 🛣 Roadmap

- [x] Lexer, Parser, and C Target Code Generator
- [x] Variable scope tracking and syntax error detection
- [ ] Support for float and boolean data types
- [ ] User-defined functions and parameters
- [ ] Abstract Syntax Tree (AST) visualization tool
