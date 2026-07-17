#!/bin/sh
set -eu

usage() {
  echo "usage: $0 [--require-tag]" >&2
}

require_tag=0
case "${1-}" in
  "") ;;
  --require-tag) require_tag=1 ;;
  *) usage; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  usage
  exit 2
fi

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

python3 tools/check_release_metadata.py
python3 tools/register_schema.py --check
python3 tools/check_markdown_links.py

version=$(tr -d '\r\n' < VERSION)
tag="sop-v$version"

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

if git rev-parse --git-dir >/dev/null 2>&1; then
  if [ -n "$(git status --porcelain --untracked-files=all)" ]; then
    echo "ERROR: worktree contains tracked, staged, or untracked changes" >&2
    git status --short >&2
    exit 1
  fi

  if git ls-files | LC_ALL=C grep '[[:space:]]' >/dev/null 2>&1; then
    echo "ERROR: tracked paths containing whitespace are unsupported by SHA256SUMS policy" >&2
    exit 1
  fi

  git ls-files \
    | LC_ALL=C sed '/^checksums\/SHA256SUMS$/d' \
    | LC_ALL=C sort > "$tmp_dir/tracked"

  awk '
    length($1) != 64 || $1 !~ /^[0-9a-f]+$/ { bad = 1 }
    NF != 2 { bad = 1 }
    {
      path = $2
      sub(/^\.\//, "", path)
      print path
    }
    END { if (bad) exit 1 }
  ' checksums/SHA256SUMS | LC_ALL=C sort > "$tmp_dir/manifest" || {
    echo "ERROR: checksums/SHA256SUMS has an invalid record" >&2
    exit 1
  }

  if ! cmp -s "$tmp_dir/tracked" "$tmp_dir/manifest"; then
    echo "ERROR: checksum manifest does not exactly cover tracked release files" >&2
    diff -u "$tmp_dir/tracked" "$tmp_dir/manifest" >&2 || true
    exit 1
  fi
fi

sha256sum -c checksums/SHA256SUMS

if git rev-parse --git-dir >/dev/null 2>&1; then
  if git show-ref --verify --quiet "refs/tags/$tag"; then
    tag_type=$(git cat-file -t "refs/tags/$tag")
    if [ "$tag_type" != "tag" ]; then
      echo "ERROR: $tag is lightweight; an annotated tag is required" >&2
      exit 1
    fi
    tag_commit=$(git rev-parse "$tag^{}")
    head_commit=$(git rev-parse HEAD)
    if [ "$tag_commit" != "$head_commit" ]; then
      echo "ERROR: $tag points to $tag_commit, not HEAD $head_commit" >&2
      exit 1
    fi
  elif [ "$require_tag" -eq 1 ]; then
    echo "ERROR: required release tag $tag does not exist" >&2
    exit 1
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
