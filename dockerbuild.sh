#!/bin/bash

# 获取当前日期，格式为 YYYYMMDD
DATE=$(date +%Y%m%d)
# 获取最新的 Git commit 哈希值的前 7 位
COMMIT_HASH=$(git rev-parse HEAD | cut -c 1-7)

# 构建 full 版本的镜像
docker buildx build --platform linux/amd64 -t chunyeah/fish-speech:latest .
# 为同一个镜像添加带日期的标签
docker tag chunyeah/fish-speech:latest chunyeah/fish-speech:dev-$DATE
# 为同一个镜像添加带当前代码库Commit哈希值的标签
docker tag chunyeah/fish-speech:latest chunyeah/fish-speech:dev-$COMMIT_HASH