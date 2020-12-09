=========
Tutorials
=========


``advance-search`` - advance search builder
===========================================

.. code:: console

    pypubmed advance-search

.. image:: https://suqingdong.github.io/pypubmed/src/advance-search.png


``search`` - search with term or pmid
=====================================

.. code:: console

    pypubmed search ngs -l 5

    pypubmed search '("NGS"[Title]) AND ("Disease"[Title/Abstract])' -o ngs_disease.xlsx


``citations`` - generate citations for given pmids
==================================================

.. code:: console

    pypubmed citations 1 2 3

    pypubmed citations 1 2 3 -f nlm

    pypubmed citations 1 2 3 -f nlm -o citations.txt
