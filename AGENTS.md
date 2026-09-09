# AGENTS.md

This file provides guidance to compatible agentic tools when generating or reviewing code in this repository.

**Note:** This file is for AI assistant use only. For human developers, refer to the project's contribution guide.

---

## ⚠️ IMPORTANT: Always Start Here

**BEFORE generating or modifying any code:**

1. **Read this file first** — Do not work from memory or assumptions
2. **Scan the existing codebase** — Identify functions, utilities, and helpers already available
3. **Follow the principles below** — They are non-negotiable
4. **Self-check before responding** — Use the checklist at the bottom of this file

---

## Core Principles

### Use English Everywhere

- **Always use English** for code, comments, documentation, and user-facing messages (CLI output, logs, prompts). No French or other languages.
- The exception is the French translation of the documentation. When you modify the English documentation, keep the French part in sync.

### DRY — Don't Repeat Yourself

- **Never duplicate logic.** Before writing a block of code, check if an existing function already handles it.
- If similar logic exists elsewhere, **reuse or extend it** rather than copying it.
- If the same logic is needed in 2+ places, **extract it into a shared function**.

### KISS — Keep It Simple, Stupid

- Prefer the **simplest readable solution** over clever or over-engineered ones.
- Avoid premature abstraction.

### Documentation & Changelog

- **Always update the documentation** when adding or changing features.
- **Always add an entry to `CHANGELOG.md` at the repository root** when making a change that impacts the user or the codebase.

---

## Before Writing Any Code

Follow these steps **in order**:

1. **Scan existing utilities** — Look for helper functions, services, or modules that already handle the required logic.
2. **Check for similar patterns** — Search the codebase for comparable implementations.
3. **Reuse before creating** — If a function exists that can be reused or slightly adapted, do that.

---

## Code Style

- Keep functions short and focused (ideally under 20–30 lines).
- Use explicit and descriptive names — avoid abbreviations.
- No dead code — remove unused functions, variables, or imports.
- No commented-out code blocks left behind.
- Trailing whitespace must always be cleaned up.
- **Always write and align docstrings in the Sphinx format** (`:param name:`, `:type name:`, `:return:`, `:rtype:`). Ensure the parameters and closing `"""` are indented perfectly to match the opening `"""`.

---

## Detecting and Reporting Duplication

If you identify duplicated logic during a review or generation task:

1. **Point it out explicitly**, referencing the file(s) and line(s) involved.
2. **Propose a refactoring** — suggest a shared function name, location, and signature.
3. **Do not silently add more duplication** on top of existing issues.

Example report format:

```
⚠️ Duplication detected:
- `src/orders/helpers.py` lines 42–58
- `src/cart/utils.py` lines 17–33
Both blocks handle discount calculation with identical logic.
Suggested fix: extract into `src/shared/pricing.py → calculate_discount(price, rate)`.
```

---

## Summary

| Principle          | Rule                                             |
| ------------------ | ------------------------------------------------ |
| DRY                | Never duplicate logic — reuse existing functions |
| KISS               | Simplest solution wins                           |
| Reuse first        | Always scan before creating                      |
| Report duplication | Flag it, don't ignore it                         |

---

## Project Architecture & Patterns

### Repository layout

```
custom_components/epex_spot/
├── __init__.py          # HA setup, config-entry migration, coordinator, base entity
├── config_flow.py       # Config flow + options flow
├── const.py             # Domain constants, source identifiers, default values
├── sensor.py            # Sensor platform entities
├── common.py            # Shared Marketprice dataclass + helpers
├── SourceShell.py       # Wrapper around a selected source
├── EPEXSpot/            # One package per data source
│   ├── Awattar/
│   ├── EnergyCharts/
│   ├── Energyforecast/
│   ├── ENTSOE/
│   ├── HoferGruenstrom/
│   ├── SMARD/
│   ├── smartENERGY/
│   ├── Tibber/
│   └── EnergyZero/      # public REST, NL-only
└── test_*.py            # standalone async smoke tests for each source
```

### Source pattern

Every data source is a package under `EPEXSpot/<Name>/__init__.py` exposing a class with these public attributes/methods:

- `URL`: API endpoint.
- `MARKET_AREAS`: sequence of supported market area identifiers.
- `SUPPORTED_DURATIONS`: sequence of supported interval durations in minutes (e.g. `(15, 60)`).
- `name`: human-readable source name.
- `market_area`, `duration`, `currency`: current configuration.
- `marketdata`: list of `Marketprice` objects after `fetch()`.
- `async def fetch()`: fetch data from the API and populate `marketdata`.

`SourceShell` instantiates the right source class based on `config_entry.data[CONF_SOURCE]` and provides shared helpers (total price, extreme intervals). When adding a new source, wire it in:

1. `const.py` — add `CONF_SOURCE_<NAME>`.
2. `SourceShell.py` — add the constructor branch.
3. `config_flow.py` — add to `CONF_SOURCE_LIST` and `getParametersForSource()`.
4. `EPEXSpot/<Name>/__init__.py` — implement the source class.
5. `test_<name>.py` — add a smoke test.
6. `README.md` — document the new source.
7. `CHANGELOG.md` — add an entry.

### Home Assistant conventions

- Follow HA's async-first patterns; all source `fetch()` methods must be async.
- Prefer `ConfigEntryNotReady` over broad exception swallowing in `async_setup_entry`.
- When changing persisted config-entry `data` or `options`, bump `CONFIG_VERSION` and implement a migration in `async_migrate_entry`.
- Keep the integration free of third-party requirements unless strictly necessary; public REST sources should use `aiohttp` directly.

---

## 🧪 Unit Tests & Quality Checks

- **ALWAYS run `prek run -a`** before considering a change complete. Fix all failures.
- **ALWAYS run `python3 -m py_compile <modified_files>`** to catch syntax errors quickly.
- **ALWAYS update or add unit tests** when you modify existing logic or add new features.
- For new sources, add a standalone `test_<source>.py` script that creates the source, calls `fetch()`, and prints a few price entries.

### Development environment with uv

This project uses `uv` to manage the Python environment and dependencies.

```bash
# Sync dev dependencies (lint/test tools).
uv sync --extra test

# Run tests.
uv run pytest tests/ -v

# Run pre-commit hooks.
uvx pre-commit run --all-files

# Compile changed Python files for syntax checks.
uv run python3 -m py_compile <modified_files>
```

---

## Self-Check Before Submitting

Before finalizing any generated code, answer these questions:

```
□ Is there an existing function that already handles this logic?
□ Am I duplicating code that exists elsewhere in the project?
□ Is this the simplest solution that works?
□ Did I remove all unused code and trailing whitespace?
□ Have I added code without corresponding unit tests ?
```

If the answer to any of these questions is **yes**, revise before submitting.
