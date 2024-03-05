#!/usr/bin/env bash

if [[ -f version.txt ]]; then
  version=$(cat version.txt | sed 's/[+-]b0//')
else
  version=${BRANCH_NAME:-$(git branch --show-current)}
  version=${version:-DETACHED}
fi

if grep -s '+' version.txt > /dev/null 2>&1; then
  joiner='+'
else
  joiner='-'
fi

if [[ -n $YB_RELEASE_BUILD_NUMBER ]]; then
  build="${YB_RELEASE_BUILD_NUMBER}"
  joiner="${joiner}b"
else
  build="$(git rev-parse --short HEAD)"
  joiner="${joiner}SHA"
fi

echo ${version}${joiner}${build}
echo $version
echo $build
