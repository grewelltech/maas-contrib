#!/bin/bash
# Manage the upstream subtrees in this repo.
#
#   scripts/subtree.sh pull <name> [<name>...]      merge latest upstream into <name>/
#   scripts/subtree.sh pull --all                   merge latest upstream into every subtree
#   scripts/subtree.sh split <name> <branch>        extract <name>/ history on the current
#                                                   branch into local branch <branch>, with
#                                                   commits rewritten to upstream layout
#   scripts/subtree.sh push <name> <branch>         split, then push <branch> to the fork
#                                                   listed in scripts/upstreams.conf
#
# Typical patch workflow:
#   git checkout -b curtin/fix-foo
#   ... edit files under curtin/, commit ...
#   scripts/subtree.sh push curtin fix-foo
#   open a PR from grewelltech/curtin:fix-foo against canonical/curtin
set -euo pipefail

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
conf="$root/scripts/upstreams.conf"
cd "$root"

lookup() {
  local name=$1
  awk -v n="$name" '$1 == n { print $2, $3, $4 }' "$conf"
}

names() {
  awk '!/^#/ && NF { print $1 }' "$conf"
}

pull_one() {
  local name=$1
  read -r url branch _ <<<"$(lookup "$name")"
  [ -n "${url:-}" ] || { echo "unknown subtree: $name" >&2; exit 1; }
  echo "=== pull $name from $url $branch"
  git subtree pull --prefix="$name" "$url" "$branch" -m "Merge upstream $name ($branch)"
}

split_one() {
  local name=$1 branch=$2
  read -r url _ _ <<<"$(lookup "$name")"
  [ -n "${url:-}" ] || { echo "unknown subtree: $name" >&2; exit 1; }
  echo "=== split $name/ into branch $branch"
  git subtree split --prefix="$name" -b "$branch"
}

push_one() {
  local name=$1 branch=$2
  read -r _ _ fork <<<"$(lookup "$name")"
  split_one "$name" "$branch"
  echo "=== push $branch to $fork"
  git push -f "$fork" "$branch:$branch"
}

cmd=${1:-}
shift || true
case "$cmd" in
  pull)
    if [ "${1:-}" = "--all" ]; then
      for n in $(names); do pull_one "$n"; done
    else
      [ $# -ge 1 ] || { echo "usage: $0 pull <name>... | --all" >&2; exit 1; }
      for n in "$@"; do pull_one "$n"; done
    fi
    ;;
  split)
    [ $# -eq 2 ] || { echo "usage: $0 split <name> <branch>" >&2; exit 1; }
    split_one "$1" "$2"
    ;;
  push)
    [ $# -eq 2 ] || { echo "usage: $0 push <name> <branch>" >&2; exit 1; }
    push_one "$1" "$2"
    ;;
  *)
    sed -n '2,/^set -euo/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
