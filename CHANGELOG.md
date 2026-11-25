# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0]

First stable release. Marks the point where `main` is brought in line with
`dev` and becomes the default branch going forward.

### Added
- Support for loading feature-extractor models from local weights/directories, not just Hugging Face/timm hub downloads (#63).

### Fixed
- Logo not rendering correctly on the PyPI project page (#82).

## [0.2.1] - 2026-10-30

Fixes `import pyslyde` failing in 0.2.0 on Python 3.8/3.9 and with scikit-image < 0.25.

### Changed
- Now requires Python >= 3.10 (3.8 and 3.9 are no longer supported) (#74).
- Now requires scikit-image >= 0.25 (#74).

## [0.2.0] - 2026-10-28

First release following the JOSS review. Addressed packaging, dependency, and
documentation/reproducibility issues raised during review, alongside several
feature and refactoring contributions.

### Added
- Overhauled `FeatureGenerator` with a unified interface over pathology foundation models (#32).
- New `normalization` package with Macenko, Vahadane, and Reinhard stain normalizers (#38).
- Storage-agnostic mask API (`BaseMask`, `Level0Mask`, `MappedMask`), allowing external masks to be used for tile filtering without pre-upsampling to level 0 (#49).
- PCA utilities to fit PCA over features stored on disk, LMDB, RocksDB, or held in memory (#48).
- `DiskRead` IO backend (#48).
- CI workflow to automatically run tests and linting on PRs (#28).

### Changed
- Restructured `slide` and `slide_parser` modules; improved error handling in `Slide` and `WSIParser` (#34, #43, #48).
- Qualified the core dependency set and introduced optional dependency groups (`feature-extractor`, `tensorflow`, `geospatial`, `rocksdb`), so the base install stays lightweight (#61).
- Fixed setuptools package discovery so that subpackages (`io`, `masks`, `normalization`, `encoders`, `util`) are actually included in built distributions — previously only the top-level `pyslyde` package was packaged, producing broken PyPI releases (#64).
- Publishing a GitHub Release now builds the package and uploads it to PyPI automatically via Trusted Publishing (#73).
- Expanded unit and integration test coverage, including memory guards to avoid OOM when running large-model integration tests (#33, #44).
- Corrected Quick Start docs and updated contributor documentation following the JOSS review (#57, #58, #65, #46).

### Fixed
- Tile masks are now resized to match downsampled image tiles (#67).
- LMDB write buffer flushing (#48).

### Removed
- Stray `dist/` build artifacts and `.ipynb_checkpoints` files that had been committed to version control (#62).
- Unused dependencies (#61).
- `environment.yml`, superseded by `pyproject.toml` optional dependency groups (#69).

## [0.1.0]

Initial release. Superseded by 0.2.0 — the published PyPI wheel for this
version was broken: `pyproject.toml` package discovery only included the
top-level `pyslyde` package, so subpackages were silently missing from the
installed package.

[1.0.0]: https://github.com/PharosKCL/pyslyde/compare/v0.2.1...v1.0.0
[0.2.1]: https://github.com/PharosKCL/pyslyde/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/PharosKCL/pyslyde/commits/v0.2.0
[0.1.0]: https://github.com/PharosKCL/pyslyde/releases/tag/v0.1.0
