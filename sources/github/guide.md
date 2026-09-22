# GitHub

GitHub REST API 数据源，提供代码仓库、Issues、Pull Requests、用户信息等数据的只读访问。

## Scope

- 当前登录用户的仓库、Issues、Pull Requests、组织
- 公开仓库的 Issues、PRs、Commits、Releases
- 搜索代码、用户、仓库

## Guidelines

- 所有 API 请求通过 Bearer Token 认证
- 遵循 GitHub API 速率限制（认证用户：5000 次/小时）
- 使用 GET 请求进行只读操作
- POST/PATCH 仅限 Issue/PR 创建和更新操作

## API Reference

### GET /user
获取当前用户信息

### GET /user/repos
获取当前用户的仓库列表

### GET /repos/{owner}/{repo}
获取指定仓库信息

### GET /repos/{owner}/{repo}/issues
获取仓库的 Issues

### GET /repos/{owner}/{repo}/pulls
获取仓库的 Pull Requests

### GET /search/issues
搜索 Issues 和 PRs

### GET /search/repositories
搜索仓库

### GET /search/code
搜索代码

### GET /notifications
获取通知列表
