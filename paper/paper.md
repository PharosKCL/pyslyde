---
title: 'PySlyde: A Lightweight, Open-Source Toolkit for Pathology Preprocessing'
tags:
  - Python
  - computational pathology
  - whole-slide images
  - digital pathology
  - image preprocessing
  - foundation models
authors:
  - name: Chima Eke
    equal-contrib: true
    affiliation: 1
  - name: Anthony Baptista
    equal-contrib: true
    affiliation: "1, 2"
  - name: Holly Rafique
    equal-contrib: true
    affiliation: 1
  - name: Elizabeth Ing-Simmons
    equal-contrib: true
    affiliation: "1, 3"
  - name: Enrico Parisini
    affiliation: "1, 3"
  - name: Mengyuan Li
    affiliation: "1, 3"
  - name: Fathima Mohamed
    affiliation: 1
  - name: Ananya Bhalla
    affiliation: "1, 5"
  - name: Lucy Ryan
    affiliation: 1
  - name: Michael Pitcher
    affiliation: "1, 3"
  - name: Concetta Piazzese
    affiliation: "3, 6"
  - name: Fan Zhang
    affiliation: "3, 7"
  - name: James Graham
    affiliation: "3, 4"
  - name: Dinis Pedro Calado
    affiliation: 5
  - name: Christopher R.S. Banerji
    affiliation: "1, 2"
  - name: Anita Grigoriadis
    corresponding: true
    affiliation: "1, 3"
  - name: Gregory Verghese
    corresponding: true
    affiliation: "1, 3"
affiliations:
  - name: Cancer Bioinformatics, School of Cancer and Pharmaceutical Sciences, Faculty of Life Sciences and Medicine, King's College London, London, UK
    index: 1
  - name: The Alan Turing Institute, The British Library, London, UK
    index: 2
  - name: PharosAI, London, UK
    index: 3
  - name: eResearch, King's College London, London, UK
    index: 4
  - name: The Francis Crick Institute, London, UK
    index: 5
  - name: Barts Life Sciences, Barts Health NHS Trust, London, UK
    index: 6
  - name: University of Cambridge, Cambridge, UK
    index: 7
date: 27 October 2026
bibliography: paper.bib
---

# Summary

Artificial intelligence (AI) represents a transformative opportunity for precision medicine, with the potential to radically improve patient outcomes [@Verghese2023ComputationalPI; @Song2023ArtificialIF]. Advances in computational pathology are enabling the analysis of complex histopathological data at unprecedented scale and depth. By combining modern computer vision, machine learning, and pathology, researchers can predict quantitative, molecular [@Dey2025GeneratingCG] and digital biomarkers, detect morphological and tissue patterns [@chen_normal_2026], and develop predictive models for diagnostics, prognosis [@Verghese2023MultiscaleDL] and treatment response to complement human expertise [@vanderLaak2021DeepLI].

Whole slide images (WSIs), resulting from the digitisation of histopathology slides, offer valuable spatial and morphological insights that can deepen our understanding of cancer biology. However, their size (gigapixel-scale), complexity, and variability introduce significant computational and standardisation challenges for downstream tasks [@mcgenity_artificial_2024]. Preprocessing WSIs, including by tissue detection, tessellation (splitting into smaller tiled images), stain normalisation [@Vahadane2016StructurePreservingCN; @Macenko2009AMF] and annotation parsing are essential steps before any downstream AI analysis can occur [@Pocock2022TIAToolboxAA]. Building robust, and reproducible pipelines for WSI preprocessing is fundamental to computational pathology research. However, existing workflows often rely on ad hoc proprietary scripts, fragmented tools, and inconsistent formats, making standardisation and reproducibility difficult.

PySlyde is a lightweight, open-source Python toolkit built on top of OpenSlide [@GOODE201327], designed to address this gap and provide an intuitive approach to quickly preprocess WSIs. It provides a simple API to perform WSI loading, annotation handling, tissue detection, tile generation, and feature extraction with support for the latest histopathology foundation models. PySlyde aims to lower the barrier to entry for computational pathology researchers, standardise preprocessing workflows, and accelerate the development of AI-ready datasets for computational pathology research, enabling researchers to focus on model development and other downstream tasks.

![Schematic overview of the WSI processing workflow supported by PySlyde, illustrating the core functionalities across the main classes and modules `Slide`, `WSIParser`, `FeatureGenerator` and `IO`. Top row, from left to right: (i) WSI loading using compatible formats through OpenSlide; (ii) annotation mask generation with support for QuPath or ImageJ formats; and (iii) preprocessing steps such as tissue detection. Bottom row, from left to right: (iv) tessellation of WSIs into tissue tiles using the `WSIParser` class; (v) feature extraction from tiles with support for pretrained encoders such as Virchow2, H-optimus, Gigapath, or UNI; and (vi) structured storage of tile embeddings and metadata using RocksDB (via Rocksdict), NumPy, or LMDB.\label{fig:workflow}](fig1.png){ width=100% }

# Statement of Need

WSI preprocessing is a foundational but time-consuming step in computational pathology. Common tasks, such as annotation parsing, binary and annotation mask generation, stain normalisation, and tessellation often involve custom scripts, multiple packages and ad hoc pipelines built for a single dataset or project. This fragmentation hinders reproducibility, increases technical debt, and slows the development and translation of AI methods into clinical workflows. The lack of standardised preprocessing practices thus remains one of the key barriers preventing the seamless integration of AI into diagnostic pathology [@bilal2025foundationmodelscomputationalpathology].

While powerful frameworks exist for model training and inference, with others providing distinct sections of the pipeline, few provide a simple, consistent interface for preparing WSIs at scale. In particular there is limited capability to integrate contributions from clinicians (such as pathologist annotations) into the computational pathology research pipeline. PySlyde directly addresses this unmet need by providing a modular, well-documented, and extensible preprocessing toolkit that integrates seamlessly with existing ecosystems, including OpenSlide, PyTorch, and modern foundation models enabling researchers to build reproducible, scalable pipelines with minimal code.

# State of the Field

Several open-source tools support WSI analysis in computational pathology. At the foundational level, OpenSlide [@GOODE201327] provides low-level image access and metadata retrieval across vendor-specific formats, underpinning higher-level preprocessing libraries. TIAToolbox [@Pocock2022TIAToolboxAA] provides a broad collection of tissue image analysis tools, including WSI reading, tissue masking, patch extraction, stain normalisation, model inference and visualisation. It supports annotation storage and GeoJSON import, and foundation model feature extraction. PathML [@Rosenthal2022; @Omar2025] supports diverse pathology imaging formats and modular preprocessing pipelines, including tissue detection, stain normalisation, tile masks, metadata and parallel processing. Slideflow [@Dolezal2024] combines WSI preprocessing with model training, multiple-instance learning and feature extraction using seven documented pathology-specific pretrained encoders. PySlyde provides capability for additional encoders to be incorporated as the state of the art evolves. Specialised tools address distinct stages of this workflow: TRIDENT [@zhang2025standardizing] focuses on large-scale tissue segmentation, patch extraction and foundation-model embeddings, while HistoQC [@Janowczyk2019HistoQCAO] provides tissue quality assessment, artefact masks and cohort-level quality review. In contrast, PySlyde is designed specifically as a modular preprocessing layer, focusing on efficient data preparation for downstream machine learning workflows.

PySlyde's contribution is a focused, modular workflow combining annotation-aware preprocessing, configurable tiling, feature extraction and storage. It supports annotations from QuPath [@Bankhead2017QuPathOS] and ImageJ [@Schneider2012NIHIT], together with externally generated masks from tools such as HistoQC, allowing labelled regions to guide mask generation and tile selection. Slide-level spatial coordinates enable interoperability with geospatial libraries such as GeoPandas and Shapely, facilitating spatial analysis workflows that extend beyond traditional image processing pipelines. Extensible encoder interfaces incorporate pathology foundation models such as Virchow2 [@Zimmermann2024Virchow2SS], H-optimus [@hoptimus2024], and UNI [@Chen2024TowardsAG], while file outputs, LMDB [@lmdb] and RocksDB [@rocksdb] accommodate different downstream access patterns. PySlyde addresses a specific gap in the current ecosystem: providing a minimal, modular preprocessing backbone that integrates complex histopathology, WSI annotation handling, geospatial representations, foundation model feature extraction and efficient storage within a single lightweight framework.

# Software Design

## Architecture

PySlyde is a lightweight and modular WSI preprocessing framework that separates slide access, annotation handling, spatial sampling, encoder inference and persistence (\autoref{fig:workflow}). Rather than providing a tightly coupled end-to-end pipeline, PySlyde enables researchers to integrate specific preprocessing stages into existing machine learning workflows.

The `Slide` class represents a single WSI with its annotations and metadata, providing spatial masking and region extraction. It inherits directly from OpenSlide, avoiding reimplementation of vendor-specific readers; format support depends on the installed OpenSlide version. The `Annotations` class parses supported annotation formats into labelled coordinate sequences for mask generation.

The `WSIParser` class manages spatial partitioning, tile selection and extraction. Separating sampling from slide representation allows a slide to be processed using different boundaries, tile dimensions, strides and pyramid levels, enabling gigapixel images to be processed efficiently under different region-selection and magnification strategies.

The `FeatureGenerator` class encapsulates model construction, checkpoint loading, image transforms and embedding generation behind a common encoder interface. `WSIParser` coordinates feature extraction through this interface, keeping model-specific operations outside the tiling logic.

The IO module provides persistence through file-based outputs and key–value stores, including LMDB [@lmdb] and RocksDB [@rocksdb]. Storage-specific operations are delegated to writer components, allowing extraction outputs to be directed to different backends.

## Data Flow

A typical processing workflow begins with a WSI and optional annotations or externally generated label masks (\autoref{fig:workflow}). Annotations can be rasterised into masks, while annotation boundaries, tissue detection, or user-specified regions define the processing area. The `pyslyde.masks` interface provides access to rasterised masks stored at full or reduced resolution through a common level-0 coordinate system. Within the selected area, `WSIParser` first generates and stores tile coordinates according to the sampling configuration. These locations can be filtered using mask-label coverage or reduced by random sampling. Alternatively, `WSIParser.filter_by_func` reads candidate tiles and applies a user-supplied rejection function, for example, to exclude tiles with entropy below a threshold or mean pixel intensity above a threshold. The parser retains the selected coordinates rather than caching the images.

Following selection, `WSIParser.extract_tiles` reads the retained image regions on demand at the configured resolution and yields each RGB tile with its coordinates. Optional preprocessing includes tile-level masking and stain normalisation. `WSIParser.extract_masks` separately yields the corresponding regions from a supplied mask. For feature extraction, `WSIParser.extract_features` reads each retained tile and passes it to `FeatureGenerator`, which applies encoder-specific image transforms, runs inference, and validates the resulting embedding. Each embedding is yielded with its source coordinates. These methods yield tiles, masks, and embeddings through separate generators with a shared coordinate–array output structure. Storage writers consume these pairs incrementally, saving images or arrays to the selected backend without first collecting all tiles or embeddings in memory. Optional embedding postprocessing is provided by `pyslyde.util.pca`, which supports incremental PCA fitting in batches from generated or stored embeddings. The utility returns a fitted PCA model, which the user can then apply to reduce embedding dimensionality and save the resulting vectors. `Stitching` enables users to reconstruct a processed slide region from saved image or mask patches using their spatial coordinates. This optional utility supports visual inspection, with configurable overlap handling and output resizing.

## Design choices and trade-offs

Several architectural trade-offs guided this design. PySlyde prioritises modularity over a monolithic pipeline structure. While tightly integrated frameworks simplify end-to-end workflows, they constrain researchers to predefined processing stages. PySlyde separates spatial sampling, encoder inference and persistence to allow these stages to be configured independently. This flexibility requires consistent handling of coordinates and model-specific input requirements across component boundaries. PySlyde builds on OpenSlide [@GOODE201327] for WSI access. This reduces maintenance overhead and improves interoperability with existing pathology infrastructure. Annotation parsers convert supported inputs into a common representation of labelled coordinate sequences. This allows downstream mask generation and region selection to operate independently of the annotation source, enabling collaboration with a diverse clinical team; however, each format requires a maintained parser and explicit handling of its coordinate conventions, and geometry types. PySlyde supports both file-based outputs and key-value storage through LMDB and RocksDB, accommodating different downstream access patterns but introducing backend dependencies and maintenance requirements. The core installation has a small dependency set, deep-learning and storage backends (PyTorch, TensorFlow, RocksDB) are optional extras installed only when needed.

# Research Impact Statement

PySlyde has been used in multiple ongoing computational pathology projects within the Cancer Bioinformatics Team at King's College London (London, UK), including multimodal outcome prediction studies in breast, head and neck and pan-cancer cohorts, with several manuscripts currently under review or in preparation. It is also used within the PharosAI Research Ventures Catalyst programme for large-scale histopathology data curation across collaborating institutions including Guy's and St Thomas' NHS Foundation Trust, Queen Mary University of London, Barts Health NHS Trust, and King's College London. These applications, alongside a poster at the *ESMO AI Congress, Berlin 2025*, demonstrate its immediate research utility and support expectations for wider adoption within computational pathology workflows.

# AI Usage Disclosure

AI-assisted development tools (e.g., Cursor [@cursor]) were used to support limited refactoring and code maintenance tasks. AI-assisted changes were reviewed through standard code review and Continuous Integration/Continuous Delivery (CI/CD) validation processes on GitHub to ensure correctness and reliability. OpenAI Codex [@codex] was used to assist with generating and debugging code for the core mathematical operations of the Macenko and Vahadane stain normalisation methods. The authors reviewed, modified, and tested the generated code and take responsibility for the final implementation and results. Generative AI tools were also used to support the writing, reviewing and editing of this manuscript, with all final content verified and edited by the authors.

# Maintenance and Availability

PySlyde is actively maintained by contributors from PharosAI, King's College London, The Alan Turing Institute, The Francis Crick Institute and Barts Health NHS Trust. The project is hosted on GitHub under an MIT license and follows open development practices, including community issue tracking and pull request review. Continuous integration is implemented via GitHub Actions, with automated testing across supported Python versions to ensure reliability and stability. The codebase includes unit tests and example workflows to support reproducibility and long-term maintainability. Source code, installation instructions, and documentation are freely available at [https://github.com/PharosKCL/pyslyde](https://github.com/PharosKCL/pyslyde). Users and contributors are encouraged to submit issues, propose enhancements, and extend the toolkit to support emerging pathology and biomedical imaging analysis.

# Author Contributions

G.V. developed the original PySlyde framework and initial codebase. C.E. subsequently undertook substantial architectural refactoring and extension of the software, including slide-processing and masking components, annotation and data I/O functionality, feature-extraction and model-loading infrastructure, input validation, stitching and error handling, and associated unit and integration testing. A.Baptista, H.R., E.P., M.L., A.Bhalla, F.M. and M.P. extended the functionality through annotation handling, preprocessing, stain normalisation, encoder integration, error handling testing and documentation. M.P., E.P. and C.P. developed and executed the unit tests. E.IS., C.P., J.G. and F.Z assisted with troubleshooting and software review. L.R. provided pathologist insight. G.V., A.B., C.E., H.R. wrote the manuscript, and A.G., C.B. and D.PC reviewed it.

# Acknowledgements

We thank members of the King's College London Cancer Bioinformatics Team, the PharosAI Programme, and collaborators at The Alan Turing Institute, The Francis Crick Institute and Barts Life Sciences for feedback, testing, and support. Holly Rafique, Pre-Doctoral Fellow NIHR303406, is funded by the NIHR, Anita Grigoriadis, Gregory Verghese, Mengyuan Li, Elizabeth Ing-Simmons, Concetta Piazzese, Fan Zhang and Enrico Parisini are funded by the UK government, Research Ventures Catalyst Programme, Department of Science Innovation and Technology, and the Guy's Cancer Charity under PharosAI for this research project. Anthony Baptista, Chima Eke and Anita Grigoriadis acknowledge support from the CRUK City of London Centre Award [CTRQQR-2021/100004]. Christopher R.S. Banerji is supported by a King's College London AI+ Fellowship. Dinis Pedro Calado acknowledges support from The Francis Crick Institute, which receives core funding from Cancer Research UK (CC2078), the UK Medical Research Council (CC2078) and the Wellcome Trust (CC2078). Dinis Pedro Calado and Anita Grigoriadis acknowledge support from the UK Medical Research Council (MR/W025221/1). Lucy Ryan is funded by the Pathological Society of Great Britain and Ireland and the Jean Shanks Foundation (JSPS CPF 1023 05). The views expressed in this publication are those of the author(s) and not necessarily those of the NIHR.

# References
