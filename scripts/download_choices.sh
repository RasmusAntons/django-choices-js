#!/bin/bash

CHOICES_VERSION=v11.0.2
CHOICES_ARCHIVE="/tmp/choices-js-${CHOICES_VERSION}.tar.gz"
CHOICES_TARGET="$(dirname "$0")/../django_choices_js/static/choices-js"
rm "${CHOICES_TARGET}/*"
curl -Lo "${CHOICES_ARCHIVE}" "https://github.com/Choices-js/Choices/archive/refs/tags/${CHOICES_VERSION}.tar.gz"
tar -xf "${CHOICES_ARCHIVE}" --no-anchored --strip-components=4 -C "${CHOICES_TARGET}" \
  "public/assets/scripts/choices.js" \
  "public/assets/scripts/choices.min.js" \
  "public/assets/styles/choices.css" \
  "public/assets/styles/choices.min.css" \
  "public/assets/styles/choices.css.map"
tar -xf "${CHOICES_ARCHIVE}" --no-anchored --strip-components=1 -C "${CHOICES_TARGET}" \
  "LICENSE"
rm "${CHOICES_ARCHIVE}"
