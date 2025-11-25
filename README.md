# Clues by Sam Solver

An automated solver for the logic puzzle game [Clues by Sam](https://cluesbysam.com).

**Check out the project landing page here:** [Clues by Sam Solver](https://safina57.github.io/clues-by-sam-solver/)

## Overview

This project implements an autonomous agent that plays "Clues by Sam". It combines browser automation, natural language processing, and formal logic to solve the puzzle.

The system operates on a **Observe -> Parse -> Deduce -> Act** loop:
1.  **Observe**: Uses Playwright to scrape the game grid and visible clues.
2.  **Parse**: Uses an LLM (GPT-4o) to translate natural language clues into formal logic constraints.
3.  **Deduce**: Uses the Z3 Theorem Prover to determine which characters are definitely Innocent or Criminal based on the accumulated knowledge.
4.  **Act**: Automatically clicks the game board to mark the deduced statuses.

## Architecture
See [Workflow Design](docs/workflow.md).

## Setup

1.  **Install dependencies:**
    This project uses [Poetry](https://python-poetry.org/) for dependency management.
    ```bash
    poetry install
    poetry run playwright install
    ```

2.  **Configure Environment:**
    Copy the example environment file and configure your API keys.
    ```bash
    cp .env.example .env
    ```
    Edit `.env` with your Azure OpenAI credentials.

    *Note: You can change the model (e.g., to a different GPT version) by modifying the `ClueTranslator` class in `src/translator/translator.py` depending on your preferences.*

## Usage
Run the main solver loop using the `poe` task runner:
```bash
poetry run poe start
```
