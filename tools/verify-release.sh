#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

version=$(tr -d '\r\n' < VERSION)
case "$version" in
  [0-9]*.[0-9]*.[0-9]*) ;;
  *) echo "ERROR: VERSION is not MAJOR.MINOR.PATCH: $version" >&2; exit 1 ;;
esac

grep -Fq "version: \"$version\"" docs/SOP.md || {
  echo "ERROR: docs/SOP.md front matter does not match VERSION" >&2
  exit 1
}

grep -Fq "| 版 | $version |" docs/SOP.md || {
  echo "ERROR: docs/SOP.md document-control table does not match VERSION" >&2
  exit 1
}

grep -Fq "## [$version]" CHANGELOG.md || {
  echo "ERROR: CHANGELOG.md has no entry for $version" >&2
  exit 1
}

sha256sum -c checksums/SHA256SUMS

if git rev-parse --git-dir >/dev/null 2>&1; then
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: tracked files have uncommitted changes" >&2
    exit 1
  fi

  tag="sop-v$version"
  if git rev-parse "$tag^{commit}" >/dev/null 2>&1; then
    tag_commit=$(git rev-parse "$tag^{commit}")
    head_commit=$(git rev-parse HEAD)
    if [ "$tag_commit" != "$head_commit" ]; then
      echo "ERROR: $tag points to $tag_commit, not HEAD $head_commit" >&2
      exit 1
    fi
  else
    echo "NOTICE: release tag $tag has not yet been created" >&2
  fi
fi

printf 'SOP_VERSION=%s\n' "$version"
printf 'SOP_FILE_SHA256=%s\n' "$(sha256sum docs/SOP.md | awk '{print $1}')"
if git rev-parse HEAD >/dev/null 2>&1; then
  printf 'SOP_COMMIT=%s\n' "$(git rev-parse HEAD)"
fi
printf 'VERIFICATION=PASS\n'
