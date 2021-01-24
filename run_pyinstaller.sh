#!/bin/bash

set -x

# always do a clean build
rm -rf build dist *.spec

pyinstaller \
  --clean \
  --noconfirm \
  --onefile \
  --name sakrament_epub_reader \
  --console \
  --add-data="data:data" \
  ./sakrament_epub_reader/__main__.py
