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
  # If we are using a - (non-semvar), then we add a 'b' before the build number
  # In semvar, the build number follows immediately after the +
  if [[ "${joiner}" == "-" ]]; then
    joiner="${joiner}b"
  fi
else
  # + is only used before a buildnumber.  If no build number if available we use the short SHA
  # with a -
  build="$(git rev-parse --short HEAD)"
  joiner="-SHA"
fi

echo ${version}${joiner}${build}
echo $version
echo $build
