#!/bin/bash

HTML_PAGE_TITLE=$1
IIIF_MANIFEST_URL=$2
TEST_CANTALOUPE_HOSTNAME=$3
IMAGE_API_PATH=$4
HTML_IMG_WIDTH=$5
HTML_IMG_HEIGHT=$6

if [[ $* == *--bypass-cache* ]]
then
  IMAGE_QUERY_STRING='?cache=false'
else
  IMAGE_QUERY_STRING=''
fi

# TODO: detect the prod Cantaloupe hostname pettern from the manifest
PROD_CANTALOUPE_HOSTNAME_PATTERN='iiif\.sinaimanuscripts.library.ucla.edu'

# Output HTML.

echo \
"<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"UTF-8\">
    <title>${HTML_PAGE_TITLE}</title>
  </head>
  <body>"

# `jq` generates a HTML template that `sed` fills in with the command line arguments.
curl --silent ${IIIF_MANIFEST_URL} | \
  jq --raw-output '[
(. |
"    <h1>\(.label | @html)</h1><p><a href=\"\(."@id")\">\(."@id")</a></p>"
),
(.sequences[0].canvases[] |
"    <a    href=\"\(.images[0].resource.service."@id")\" class=\"img-link\">
      <img src=\"\(.images[0].resource.service."@id")/{IMAGE_API_PATH}{IMAGE_QUERY_STRING}\"
           alt=\"\(.label | @html)\"
           width=\"{HTML_IMG_WIDTH}\"
           height=\"{HTML_IMG_HEIGHT}\">
    </a>"
)
] | .[]' | \
  sed -e "s|${PROD_CANTALOUPE_HOSTNAME_PATTERN}|${TEST_CANTALOUPE_HOSTNAME}|g" \
      -e "s|{IMAGE_API_PATH}|${IMAGE_API_PATH}|g" \
      -e "s|{IMAGE_QUERY_STRING}|${IMAGE_QUERY_STRING}|g" \
      -e "s|{HTML_IMG_WIDTH}|${HTML_IMG_WIDTH}|g" \
      -e "s|{HTML_IMG_HEIGHT}|${HTML_IMG_HEIGHT}|g"

echo \
"    <!-- remove underline from links that contain images -->
    <style>.img-link { text-decoration: none; }</style>
  </body>
</html>"
