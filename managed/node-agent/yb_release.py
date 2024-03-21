#!/usr/bin/env python3
# Copyright (c) YugaByte, Inc.

import argparse
from distutils.command.build import build
import json
import logging
import os
import shutil
import subprocess
import tarfile

from ybops.utils import init_env, log_message, get_release_file
from ybops.common.exceptions import YBOpsRuntimeError

"""This script packages the node agent binaries for all supported platforms.
"""


def filter_function(version, filename):
    exclude_folders = ["{}/devops/venv".format(version)]
    for exclude_folder in exclude_folders:
        if filename.startswith(exclude_folder):
            logging.info("Skipping {}".format(filename))
            return False
    return True


def get_release_version(source_dir):
    cp = subprocess.run(f"{os.environ['yb_devops_home']}/bin/yb_build_string.sh", check=True,
                        shell=True, capture_output=True)
    return str(cp.stdout.decode('utf-8').strip())


targets = set(["linux/amd64", "linux/arm64"])
parser = argparse.ArgumentParser()
parser.add_argument('--source_dir', help='Source code directory.', required=True)
parser.add_argument('--destination', help='Copy release to Destination directory.', required=True)
parser.add_argument('--pre_release', help='Generate pre-release packages.', action='store_true')
parser.add_argument('--include_pex', help='Include pex env for node agent', action='store_true')
parser.add_argument('--target', help='Which architecture to build for', action='extend', nargs="+",
                    type=str)
args = parser.parse_args()
if args.target:
    targets = set(args.target)


if args.pre_release:
    devops_home = os.getenv('DEVOPS_HOME')
    if not devops_home:
        raise RunTimeError("DEVOPS_HOME ENV variable is required for pre_release builds")
    if not os.path.exists(devops_home):
        raise RunTimeError(f"DEVOPS_HOME is defined but does not exist: {devops_home}")


try:
    init_env(logging.INFO)
    if not os.path.exists(args.destination):
        raise YBOpsRuntimeError("Destination {} not a directory.".format(args.destination))

    version, v, b = get_release_version(args.source_dir).split()
    with open('version_metadata.json', 'w') as f:
        f.write(json.dumps({'version': v, 'build': b}))
    build_script = os.path.join(args.source_dir, "build.sh")
    for platform in targets:
        process_env = os.environ.copy()
        process_env["NODE_AGENT_PLATFORMS"] = platform
        subprocess.check_call([build_script, 'clean', 'build', 'package', version], env=process_env)

        #parts = platform.split("/")
        #packaged_file = os.path.join(args.source_dir, "build",
        #                             "node_agent-{}-{}-{}.tar.gz"
        #                             .format(version, parts[0], parts[1]))
        # Devops cannot parse names separated by dashes.
        #release_file = get_release_file(args.source_dir,
        #                                "node_agent", os_type=parts[0], arch_type=parts[1])
        #shutil.copyfile(packaged_file, release_file)
        if args.pre_release:
            # Pre-release is for local testing only.
            release_file = packaged_file
            if args.include_pex:
                logging.info("Rebuilding pex for node agent.")
                build_pex_script = os.path.join(devops_home, "bin", "build_ansible_pex.sh")
                subprocess.check_call([build_pex_script, '--force'])
                repackaged_file = os.path.join(args.source_dir, "build",
                                               "node_agent-{}-{}-{}-repackaged.tar.gz"
                                               .format(version, parts[0], parts[1]))
                with tarfile.open(repackaged_file, "w|gz") as repackaged_tarfile:
                    with tarfile.open(release_file, "r|gz") as tarfile:
                        for member in tarfile:
                            repackaged_tarfile.addfile(member, tarfile.extractfile(member))

                    repackaged_tarfile.add(devops_home, arcname="{}/devops".format(version),
                                           filter=lambda x: x if filter_function(version, x.name)
                                           else None)

                    thirdparty_folder = "/opt/third-party/"
                    for file in os.listdir(thirdparty_folder):
                        # Skip Packaging alertmanager with NodeAgent.
                        # TODO: Make a list of packages that are actually needed.
                        if "alertmanager" in file:
                            continue
                        filepath = os.path.join(thirdparty_folder, file)
                        if os.path.isfile(filepath):
                            repackaged_tarfile.add(filepath,
                                                   "{}/thirdparty/{}".format(version, file))

                shutil.move(repackaged_file, packaged_file)

        logging.info("Copying file {} to {}".format(release_file, args.destination))
        shutil.copy(release_file, args.destination)
    # Delete ansible only pex.
    if args.pre_release and args.include_pex:
        logging.info("Deleting ansible only pex after packaging.")
        pex_path = os.path.join(devops_home, "pex", "pexEnv")
        if os.path.isdir(pex_path):
            shutil.rmtree(pex_path)

except (OSError, shutil.SameFileError) as e:
    log_message(logging.ERROR, e)
    raise e
