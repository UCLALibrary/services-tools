# iiif-thumbnail-gallery-view-static

This script generates a static HTML page that simulates the gallery view of a IIIF viewer, for the purpose of load-testing Cantaloupe.

Supports IIIF Presentation API 2.

## Installation

Requires `bash`, `curl`, `sed`, and `jq`. Tested with these versions:

    $ bash --version
    GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu)
    ...

    $ curl --version
    curl 7.58.0 (x86_64-pc-linux-gnu) libcurl/7.58.0 OpenSSL/1.1.1 zlib/1.2.11 libidn2/2.0.4 libpsl/0.19.1 (+libidn2/2.0.4) nghttp2/1.30.0 librtmp/2.3
    Release-Date: 2018-01-24
    ...

    $ sed --version
    sed (GNU sed) 4.4
    ...

    $ jq --version
    jq-1.5-1-a5b5cbe
    ...

## Usage

Run something like this:

    ./iiif-thumbnail-gallery-view-static.sh \
        "Cantaloupe load test, server-side caching - thumbnail gallery view" \
        https://iiif.library.ucla.edu/ark%3A%2F21198%2Fz1ns1z7t/manifest \
        stage-iiif.library.ucla.edu \
        full/120,/0/default.jpg \
        36 48 \
     > index.html

Running with the `--bypass-cache` flag will [append `cache=false` to the query string of each image URL](https://cantaloupe-project.github.io/manual/4.0/endpoints.html#Bypassing%20the%20Caches), so that Cantaloupe's cache is bypassed:

    ./iiif-thumbnail-gallery-view-static.sh \
        "Cantaloupe load test, no server-side caching - thumbnail gallery view" \
        https://iiif.library.ucla.edu/ark%3A%2F21198%2Fz1ns1z7t/manifest \
        stage-iiif.library.ucla.edu \
        full/120,/0/default.jpg \
        36 48 \
        --bypass-cache \
    > index.html
