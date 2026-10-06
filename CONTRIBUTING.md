# Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Development tooling setup

Clone the repository and install the necessary development extras.

```sh
pip install -e ".[all,dev,docs]"
```

### Testing

Run the test suite from the repository root:

```sh
pytest                          # unit + integration tests
```

The tests are grouped with pytest markers:

| Command | What runs | Needs |
|---|---|---|
| `pytest -m "not integration and not models"` | unit tests (mocked, fast) | nothing |
| `pytest -m integration` | end-to-end tests on the example dataset: every annotation format, masks, regions, saving, and the documentation code snippets | network on the first run only (cached afterwards) |
| `RUN_NETWORK_TESTS=1 pytest -m "models and not gated and not bigmem"` | real feature-extractor weights for the open models | network |
| `RUN_NETWORK_TESTS=1 HUGGINGFACE_TOKEN=... pytest -m models` | all real-model tests, including gated (`gated`) and very large (`bigmem`) models | token, large machine |
| `pytest --nbmake docs/examples/*.ipynb` | executes the tutorial notebooks | `pip install nbmake` |

With the example dataset available, `pytest -m integration` should report
**0 skipped** tests.

#### Integration data

The integration tests use the PySlyde example dataset (`pyslyde.datasets`):

- the CC0-licensed OpenSlide slide `CMU-1-Small-Region.svs`, downloaded once,
  checked against a pinned SHA-256 and cached in `~/.cache/pyslyde`
  (`PYSLYDE_CACHE_DIR` overrides the location);
- synthetic annotations in all six formats, shipped in
  `pyslyde/datasets/annotations` and regenerated with
  `python scripts/make_example_annotations.py`.

You do not need to configure anything. To test other data, use a directory
or archive laid out as `wsi/` + `annotations/`:

```sh
PYSLYDE_IT_DATA_DIR=/path/to/data pytest -m integration
PYSLYDE_IT_DATA_URL=<archive_url> PYSLYDE_IT_DATA_SHA256=<sha256> pytest -m integration
```

A checksum is required for remote archives. If the data cannot be obtained
(e.g. offline on the first run), the integration tests are skipped with the
reason. Set `PYSLYDE_IT_STRICT=1` to make them fail instead; CI runs in strict
mode.

#### Feature-extractor (real model) tests

Gated Hugging Face models need `HUGGINGFACE_TOKEN` unless the weights are
already in the local cache. Very large models are skipped unless enough memory
is available; adjust the thresholds with `MIN_CPU_AVAIL_GB` and
`MIN_FREE_VRAM_GB` (default 24 GB).

### Documentation

The documentation (Sphinx, in `docs/`) is built with warnings as errors in CI
and on Read the Docs:

```sh
pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

The tutorial notebooks in `docs/examples/` are rendered with their stored
outputs. After changing one, re-execute it top to bottom before committing,
e.g. with `jupyter execute --inplace docs/examples/<name>.ipynb`.

### Linting and formatting

We use [`ruff`](https://docs.astral.sh/ruff/) to lint and format code.

To lint files in the current directory, run:

```sh
ruff check 
```

This will report any errors, e.g. unused imports.
You can run `ruff check --fix` to automatically fix errors where possible.

To format files in the current directory, run:

```sh
ruff format
```

This will automatically update formatting where needed.
If you just want to see the suggested changes, run `ruff format --diff`.
