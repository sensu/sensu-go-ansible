# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

### Changed

### Fixed

## [0.2.0] - 2019-07-29

### Changed
- Added annotation and label support to `sensu_go_event`.

### Fixed
- Fixed broken documentation in `sensu_go_entity`, `sensu_go_event`,
  `sensu_go_filter`, and `sensu_go_silence_info`.

- `sensu_go_silence_info` would accept specifying multiple parameters that
  limited retrieved entries, then silently pick one to honor while ignoring
  the rest.

## [0.1.0] - 2019-07-28

Initial Release
