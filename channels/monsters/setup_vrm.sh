#!/bin/sh
# Installs the VRM Add-on for Blender (MIT/GPL, pinned v4.10.3) where Blender can find it. Then render with:
#   BLENDER_USER_SCRIPTS=/home/user/tools/blender_scripts blender -b -y -P <script>
# -y (auto-run scripts) is required: the VRM face expressions are drivers.
set -e
D=/home/user/tools/blender_scripts
mkdir -p $D/addons /home/user/tools/src
[ -d /home/user/tools/src/VRM-Addon-for-Blender ] || \
  git clone -q --depth 1 --branch v4.10.3 https://github.com/saturday06/VRM-Addon-for-Blender /home/user/tools/src/VRM-Addon-for-Blender
ln -sfn /home/user/tools/src/VRM-Addon-for-Blender/src/io_scene_vrm $D/addons/io_scene_vrm
echo "VRM add-on ready: BLENDER_USER_SCRIPTS=$D"
