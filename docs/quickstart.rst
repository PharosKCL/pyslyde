Quick Start
===========

This page walks through a complete PySlyde workflow on the
:doc:`example dataset <example_data>`: a small, openly licensed slide plus
annotations in every supported format. All code blocks on this page run in
order, as written, in a fresh Python session (they are executed by the test
suite, see :doc:`testing`).

Get the example data
--------------------

.. code-block:: python

   from pyslyde.datasets import example_data_dir

   data = example_data_dir()   # downloads the slide once (1.9 MB), then uses the cache
   slide_path = str(data / "wsi" / "CMU-1-Small-Region.svs")
   annotation_path = str(data / "annotations" / "example.geojson")

To use your own data, replace ``slide_path`` and ``annotation_path`` with the
paths to your files.

Load a slide
------------

:class:`~pyslyde.slide.Slide` is a subclass of :class:`openslide.OpenSlide`,
so every OpenSlide attribute is available as well:

.. code-block:: python

   from pyslyde import Slide

   slide = Slide(slide_path)
   print(slide.name)               # CMU-1-Small-Region.svs
   print(slide.dims)               # (2220, 2967) - level-0 (width, height)
   print(slide.level_count)        # 1
   print(slide.level_dimensions)   # ((2220, 2967),)

Load annotations
----------------

:class:`~pyslyde.slide.Annotations` reads six formats, selected with
``source``. The example dataset provides the same polygons in each of them:

.. code-block:: python

   from pyslyde import Annotations

   ann_dir = data / "annotations"
   annotations = Annotations(annotation_path, source="geojson")
   csv_ann = Annotations(str(ann_dir / "example.csv"), source="csv")
   qupath_ann = Annotations(str(ann_dir / "example_qupath.json"), source="qupath")
   asap_ann = Annotations(str(ann_dir / "example_asap.xml"), source="asap")
   imagej_ann = Annotations(str(ann_dir / "example_imagej.xml"), source="imagej")
   json_ann = Annotations(str(ann_dir / "example_custom.json"), source="json")

   print(annotations.class_key)    # {'epithelium': 1, 'tissue': 2}

Attach the annotations to the slide (alternatively pass
``annotations_path=...`` and ``source=...`` directly to ``Slide``):

.. code-block:: python

   slide = Slide(slide_path, annotations=annotations)

Generate masks
--------------

:meth:`~pyslyde.slide.Slide.generate_mask` rasterises the annotations into an
integer mask (0 = background, otherwise the class ID from ``class_key``).
Give either an output ``size`` (width, height) or a pyramid ``level``:

.. code-block:: python

   mask = slide.generate_mask(size=(555, 742))                 # downsampled mask
   epithelium = slide.generate_mask(size=(555, 742), labels=["epithelium"])
   mask_level0 = slide.generate_mask(level=0)                   # full resolution

   print(mask.shape)          # (742, 555) - (height, width)
   print(mask_level0.shape)   # (2967, 2220)

Calling ``generate_mask()`` without ``size`` or ``level`` raises an error
unless ``full_res=True``, to avoid accidentally allocating a gigapixel array.

Extract regions
---------------

:meth:`~pyslyde.slide.Slide.generate_region` returns an RGB region and the
matching annotation mask. Coordinates are level-0 pixels; give either
``(start, end)`` ranges or a start point plus ``x_size`` / ``y_size``:

.. code-block:: python

   region, region_mask = slide.generate_region(level=0, x=(600, 1600), y=(1200, 2200))
   print(region.shape, region_mask.shape)   # (1000, 1000, 3) (1000, 1000)

   patch, patch_mask = slide.generate_region(level=0, x=600, y=1200, x_size=512, y_size=512)
   print(patch.shape)                       # (512, 512, 3)

Save the mask, a visualisation and the metadata in one call:

.. code-block:: python

   outputs = slide.save("quickstart_output/slide", size=(555, 742), overwrite=True)
   print(sorted(outputs))   # ['mask', 'meta', 'vis']

Detect tissue
-------------

:class:`~pyslyde.util.utilities.TissueDetect` finds tissue without any
annotations:

.. code-block:: python

   from pyslyde.util.utilities import TissueDetect

   detector = TissueDetect(slide_path)
   tissue_mask = detector.detect_tissue()   # full-resolution binary mask
   border = detector.border()               # ((x_min, x_max), (y_min, y_max))
   thumbnail = detector.tissue_thumbnail    # RGB image for display

   print(tissue_mask.shape, border)

Tile the slide
--------------

:class:`~pyslyde.slide_parser.WSIParser` tiles a slide inside a border, here
the bounding box of the annotations:

.. code-block:: python

   from pyslyde import WSIParser

   parser = WSIParser(
       slide=slide,
       tile_dim=256,                # tile size in pixels
       border=slide.get_border(),   # [(x_min, x_max), (y_min, y_max)]
       level=0,                     # pyramid level to read tiles from
   )
   n_tiles = parser.tiler(stride=256)
   print(f"Generated {n_tiles} tiles")

Filter tiles with any function that takes a tile and returns ``True`` for
tiles to drop. :func:`pyslyde.util.filters.tile_intensity` drops bright,
mostly-background tiles:

.. code-block:: python

   from pyslyde.util import filters

   parser.filter_by_func(filters.tile_intensity, threshold=220)
   print(f"{parser.number} tiles left after filtering")

   parser.sample_tiles(n=8, seed=0)     # keep a small random subset for this example

Extract features
----------------

:meth:`~pyslyde.slide_parser.WSIParser.extract_features` yields
``((x, y), feature_vector)`` for each tile. It needs the deep-learning
dependencies (``pip install "pyslyde[feature-extractor]"``, see
:doc:`installation`). Torchvision models such as ``resnet18`` and
``resnet50`` download their ImageNet weights on first use. Gated pathology
foundation models (UNI, Virchow, ...) also need a Hugging Face token.

.. code-block:: python

   for (x, y), features in parser.extract_features(model_name="resnet18"):
       print((x, y), features.shape)   # e.g. (1536, 2816) (512,)

Save tiles
----------

.. code-block:: python

   # PNG files on disk
   parser.save_tiles(tile_path="quickstart_output/tiles")

   # or an LMDB database
   parser.to_lmdb(
       parser.extract_tiles(),
       db_path="quickstart_output/tiles.lmdb",
       map_size=1024**3,   # 1 GB
   )

Next steps
----------

* :doc:`examples/index` - end-to-end tutorial notebooks
* :doc:`api/index` - full API reference
* :doc:`example_data` - what the example dataset contains and how it is built
