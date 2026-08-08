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
