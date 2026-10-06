Running the tests
=================

Install the development extras, then run ``pytest`` from the repository root:

.. code-block:: bash

   pip install -e ".[all,dev]"
   pytest                                   # unit + integration tests

The suite is split with pytest markers:

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Selection
     - What runs
     - Needs
   * - ``pytest -m "not integration and not models"``
     - Unit tests (mocked, fast)
     - nothing
   * - ``pytest -m integration``
     - End-to-end tests on the :doc:`example dataset <example_data>`: every
       annotation format, masks, regions, saving, component detection, and
       the :doc:`quickstart` code blocks
     - network on the first run only (1.9 MB slide plus torchvision ResNet-18
       weights), then cached
   * - ``RUN_NETWORK_TESTS=1 pytest -m "models and not gated and not bigmem"``
     - Real feature-extractor weights and forward passes for the openly
       available models (ResNet, VGG, ...)
     - network, a few GB of disk
   * - ``RUN_NETWORK_TESTS=1 HUGGINGFACE_TOKEN=... pytest -m models``
     - All real-model tests, including gated Hugging Face models (``gated``)
       and very large models (``bigmem``, ≥ 24 GB RAM/VRAM by default)
     - network, token, large machine
   * - ``pytest --nbmake docs/examples/*.ipynb``
     - Executes the tutorial notebooks end to end
     - ``pip install nbmake``

With the example dataset available, ``pytest -m integration`` is expected to
report **0 skipped** tests. Optional backends that are not installed (e.g.
``rocksdict`` for the RocksDB writer) are skipped with a reason.

Integration data
----------------

By default the integration tests use the example dataset. Other data can be
supplied as a directory (or ``.zip`` / ``.tar.gz``) containing ``wsi/`` and
``annotations/``:

.. code-block:: bash

   PYSLYDE_IT_DATA_DIR=/path/to/data pytest -m integration
   PYSLYDE_IT_DATA_URL=https://.../data.zip PYSLYDE_IT_DATA_SHA256=<sha256> pytest -m integration

A checksum is mandatory for remote archives. If the data cannot be obtained
(for example, no network on the first run), the integration tests are
skipped with the reason. Set ``PYSLYDE_IT_STRICT=1`` to make them fail
instead; continuous integration runs in strict mode.

Feature-extractor tests
-----------------------

``MIN_CPU_AVAIL_GB`` and ``MIN_FREE_VRAM_GB`` (default 24) set the memory
needed before a ``bigmem`` model is loaded. A gated model that is already in
the local Hugging Face cache loads without ``HUGGINGFACE_TOKEN``.
