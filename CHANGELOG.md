# Changelog

All notable changes to this fork of `ha_epex_spot` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New source: EnergyZero (Netherlands, public REST API, hourly and quarter-hourly intervals).

### Fixed

- Tibber source now handles missing or empty `currentSubscription.priceInfo` responses gracefully instead of raising `NoneType` errors.
- Added missing Energyforecast market areas: DK1, DK2, PL.
- Options flow now coerces the duration value to `int`, matching the initial config flow and fixing the dropdown display.
- Config-entry migration now persists `data["version"]` and migrates the removed `EPEX Spot Web Scraper` source to `Energy-Charts.info`.
- Removed unsupported market areas from SMARD.de mapping (only `DE-LU` and `AT` are currently provided by SMARD, others caused HTTP 404).

### Added

- HACS validation workflow.
- pytest integration tests that verify public source URLs do not return 404.
- `AGENTS.md` instructions for `uv`/`uvx` development environment.
- Updated `LICENSE` with fork copyright.
- GitHub Actions release workflows that update `CHANGELOG.md` and `manifest.json` on release (manual or automatic).

### Changed

- Updated `manifest.json` to set `integration_type` to `service` and removed unused `beautifulsoup4` requirement.
