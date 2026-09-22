# 更新在线静态资源网站内容

能力简介：

本能力支持用户基于已有的静态资源预览地址，一键完成线上内容替换与更新，无需重新发布、无需记忆内部资源 ID，实现「原链接、新内容」的无缝迭代体验。

用户只需传入此前部署成功时获得的公网预览 URL（如 https://ind.haierfhtech.com/fKK59/ ），系统将自动解析 URL 中的短链标识，精准匹配已部署的静态资源记录，并在此基础上完成内容覆盖。更新过程支持以下三种输入方式，与上传能力保持一致：

完整站点压缩包（.zip）：上传包含完整 HTML 站点目录结构的新版本压缩包，系统将自动解压并替换原站点内容，适用于整站改版、多页面联动更新等复杂场景；
单个 HTML 文件（.html）：直接上传新的 index.html 文件，系统自动完成目录替换与部署，适用于单页内容的快速修订、文案调整或样式更新；
原始 HTML 文本内容：直接传入新的 HTML 源码字符串，无需准备任何文件，平台自动完成内容替换，适用于由程序动态生成页面后的即时更新或在线编辑发布场景。
更新完成后，原预览地址保持不变，用户无需更换链接即可立即在浏览器中访问最新内容，原有分享链接、嵌入引用均可继续生效。同时，用户可按需同步更新资源名称、备注、分类等元数据信息。平台将返回更新后的资源信息（含原 shortLink、资源 ID 及元数据字段），便于调用方确认更新结果。

整个过程无需服务器运维介入，显著降低静态资源持续迭代与线上维护门槛，适用于产品展示页内容刷新、活动页热更新、原型快速验证等需要「固定链接、动态内容」的业务场景。

## Scope

能力市场提供的 API 服务。

## Authentication

此 API 通过 `X-Platform-Access-Key` 请求头进行认证，凭证已自动配置。

- **Header Name:** `X-Platform-Access-Key`
- **Access Key:** `pk_b1fb70c791093782097c3405bb9854cd18cccfe520714fa89932b20f8239f625`

## API Reference

### POST /

**Endpoint:** `https://market.haierfhtech.com/prod-api/capabilitymarket/api/v1/proxy/cap_6dc013392621440e927b0f4bcade5ca5`

**Body Parameters:**
- `previewUrl` (STRING, required): 待更新资源的公网预览地址。系统会自动解析 URL 中的短链标识进行匹配，支持以下格式： https://sit-ind.haierfhtech.com/fKK59/  https://ind.haierfhtech.com/fKK59 
- `resourceType` (STRING, required): 资源类型，取值 "file"（文件上传）或 "text"（文本内容），默认为 "file"
- `file` (File upload): 待上传的 HTML 资源文件或压缩包（当 resourceType == "file" 时必填），格式要求： 压缩包（.zip）：包内必须包含一个文件名必须是“index.html”的文件作为首页入口，目录结构应保持完整（CSS/JS/图片等资源需使用相对路径引用），不支持绝对路径或 ../ 跨目录引用； 单个 HTML 文件（.html）：可直接上传一个 html 文件，文件名必须是“index.html”，系统将自动为其生成基础站点目录结构并完成部署；文件内容需符合标准 HTML5 规范，内联或外链的 CSS/JS 引用路径需确保可公网访问；
- `userName` (STRING): 用户工号
- `htmlContent` (STRING): 原始 HTML 文本内容（当 resourceType == "text" 时必填）

## Guidelines

- 此服务由能力市场平台代理，认证凭证已自动配置
- 请求方法: POST
- 此 API 包含文件上传参数，请使用 multipart/form-data 格式

