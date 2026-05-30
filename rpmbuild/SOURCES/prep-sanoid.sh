#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
spec_file="$script_dir/../SPECS/sanoid.spec"

if [[ ! -f "$spec_file" ]]; then
  echo "error: spec file not found: $spec_file" >&2
  exit 1
fi

VERSION="${1:-${VERSION:-$(awk '
  /^%global[[:space:]]+upstream_version[[:space:]]+/ { print $3; found=1; exit }
  /^Version:[[:space:]]+/ && !found { print $2; exit }
' "$spec_file")}}"

if [[ -z "${VERSION}" || "${VERSION}" == *%* ]]; then
  echo "error: VERSION is empty or unresolved; pass a version or define upstream_version/Version in sanoid.spec" >&2
  exit 1
fi

version="${VERSION#v}"
tag="v${version}"

cd "$script_dir"

archive_url="https://github.com/jimsalterjrs/sanoid/archive/${tag}/sanoid-${version}.tar.gz"
output_tar="sanoid-${version}.tar.gz"
tmp_tar="${output_tar}.tmp"

echo "Downloading sanoid ${version}"
wget -O "$tmp_tar" "$archive_url"
mv "$tmp_tar" "$output_tar"

echo "Created $output_tar"
