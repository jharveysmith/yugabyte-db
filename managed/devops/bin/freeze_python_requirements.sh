#!/bin/bash
#
# Copyright 2019 YugaByte, Inc. and Contributors
#
# Licensed under the Polyform Free Trial License 1.0.0 (the "License"); you
# may not use this file except in compliance with the License. You
# may obtain a copy of the License at
#
# https://github.com/YugaByte/yugabyte-db/blob/master/licenses/POLYFORM-FREE-TRIAL-LICENSE-1.0.0.txt

set -euo pipefail

. "${BASH_SOURCE%/*}"/common.sh

if [[ ! ${1:-} =~ ^(-y|--yes)$ ]]; then
  echo >&2 "This will remove and re-create the entire virtualenv from ${virtualenv_dir} in order"
  echo >&2 "to re-generate 'frozen' python dependency versions. It is only necessary to run this"
  echo >&2 "script once in a while, when we want to upgrade versions of some third-party Python"
  echo >&2 "modules."
  echo >&2
  echo >&2 "The frozen Python requirements file will be generated at: $FROZEN_REQUIREMENTS_FILE"
  echo >&2 -n "Continue? [y/N] "

  read confirmation

  if [[ ! $confirmation =~ ^(y|Y|yes|YES)$ ]]; then
    log "Operation canceled."
    exit 1
  fi
fi

cd "$yb_devops_home"
export YB_VERBOSE=true
export YB_RECREATE_VIRTUALENV=true
rm -f "requirements_frozen.txt"
activate_virtualenv

log_empty_line
log "Changes for $FROZEN_REQUIREMENTS_FILE"
git --no-pager diff "requirements_frozen.txt"
log_empty_line
log "Requirements successfully frozen"

