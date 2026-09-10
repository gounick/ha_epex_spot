# Changelog

All notable changes to this fork of `ha_epex_spot` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New source: EnergyZero (Netherlands, public REST API, hourly and quarter-hourly intervals).
- HACS validation workflow.
- pytest integration tests that verify public source URLs do not return 404.
- `AGENTS.md` instructions for `uv`/`uvx` development environment.
- Updated `LICENSE` with fork copyright.
- GitHub Actions release workflows that update `CHANGELOG.md` and `manifest.json` on release (manual or automatic).
- Security scanning workflows with Gitleaks and Kingfisher.
- Kingfisher pre-commit hook.
- Renovate configuration.

### Fixed

- Fixed `average_marketdata` when the requested duration is finer than the API resolution (e.g. hourly data requested as 15-minute intervals).
- Updated `requires-python` to `>=3.14.2` and `homeassistant` dev dependency to `>=2026.9.1`, aligning tests with the latest Home Assistant version.
- HACS Action workflow now ignores repository topics and issues checks until the repository settings are updated.
- Tibber source now handles missing or empty `currentSubscription.priceInfo` responses gracefully instead of raising `NoneType` errors.
- Added missing Energyforecast market areas: DK1, DK2, PL.
- Options flow now coerces the duration value to `int`, matching the initial config flow and fixing the dropdown display.
- Config-entry migration now persists `data["version"]` and migrates the removed `EPEX Spot Web Scraper` source to `Energy-Charts.info`.
- Removed unsupported market areas from SMARD.de mapping (only `DE-LU` and `AT` are currently provided by SMARD, others caused HTTP 404).
- Removed `DE-AT-LU` from Energy-Charts bidding zones (API returns 404 for this zone).

### Changed

- Updated `manifest.json` to set `integration_type` to `service` and removed unused `beautifulsoup4` requirement.
