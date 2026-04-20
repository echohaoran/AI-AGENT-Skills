---
title: wps
excerpt: A skill for WPS Office in Chinese office scenarios, covering document writing, spreadsheet processing, presentation creation, format compatibility, and delivery export.
date: 2026-04-09
---

SKILL.md
WPS Office

WPS skill for Chinese office scenarios, covering document writing, spreadsheet processing, presentation creation, format compatibility, and delivery export.

When to Use

    User explicitly mentions WPS/WPS Office, WPS Writer/Calculate/Presentation.
    Need to convert between .docx/.xlsx/.pptx and WPS common formats, or troubleshoot compatibility issues.
    Need to handle Chinese typography issues, such as font size and line spacing, paragraph spacing, Chinese punctuation, pagination, and TOC.
    Need "deliverable version", such as exporting PDF, print version, or comment review version.

When NOT to Use

    Pure code development, database queries, server operations.
    Only involves Google Docs/Notion and other online collaboration tools without needing WPS.
    Need to execute local GUI click operations but current environment has no desktop session.

Default Workflow

    Clarify goal: Confirm document type (Writer/Calculate/Presentation), delivery format (source file/PDF), and deadline.
    Collect input: Confirm original file, template, font requirements, margins, and paper size (A4/Letter).
    Provide minimal steps: Prioritize reproducible short processes, ensure deliverability first, then beautify.
    Compatibility check: Focus on font substitution, pagination drift, chart misalignment, formula compatibility.
    Delivery note: Output "completed items + pending items + rollback plan".

High-Frequency Task Templates
1) WPS Writer

    Chinese long-form: First unify styles (Heading 1/2/3, Body, Quote), then insert TOC.
    Contracts or official documents: Prioritize locking page settings, headers/footers, and paragraph grid, finally handle numbering.
    Review process: Recommend enabling track changes + comments, avoid directly overwriting original text.

2) WPS Calculate

    Data cleaning: First backup copy, then do text-to-columns, deduplication, format standardization.
    Summary analysis: Prioritize using pivot tables, reduce manual copy-paste.
    Pre-delivery check: Formula reference range, number format, freeze panes, print area.

3) WPS Presentation

    First set master slide and fonts, then batch apply templates; avoid manual alignment page by page.
    For mixed text and images, prioritize using guides and alignment/distribution tools.
    Before export, check font embedding and animation compatibility, export PDF as fallback if necessary.

Compatibility and Troubleshooting

    Layout messed up after opening: First confirm missing fonts, then check paragraph styles and page breaks.
    Excel/WPS formula inconsistency: Confirm function differences and range reference methods.
    Blurry images: Prioritize replacing original images, avoid repeated screenshot compression.
    Print pagination abnormal: Fix paper and margins, reset print area before preview.

For detailed format differences and troubleshooting order, see WPS Reference.

Security Boundaries

    Without user consent, do not overwrite original files; default to saving as new version.
    Do not process or expose real sensitive information (ID numbers, phone numbers, contract amounts, etc.), use placeholders for all examples.
    When software installation, online template downloads, or macro plugins are needed, explain risks and sources first.

OpenClaw and clawhub.ai Specifications

    Only output reproducible, auditable operation steps, avoid depending on personal device paths.
    Use generic placeholder filenames for all examples (e.g., Contract Draft-v2.docx).
