# Pollinations AI 图像生成

免费、开源的 AI 文生图服务。无需注册，无需 API Key，直接通过 GET 请求生成图片。

## 特点

- **100% 免费**：无需注册，无需 API Key
- **隐私保护**：零数据存储，完全匿名
- **两个模型**：`flux`（快速）和 `turbo`（高质量）
- **支持参数**：尺寸、种子、增强等

## API 参考

### GET /prompt/{prompt}

生成一张 AI 图片。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | 必填 | 图片描述（建议英文，需 URL 编码） |
| `model` | string | `flux` | 模型：`flux` 或 `turbo` |
| `width` | number | 1024 | 图片宽度（256-2048） |
| `height` | number | 1024 | 图片高度（256-2048） |
| `seed` | number | 随机 | 随机种子，用于复现结果 |
| `nologo` | boolean | false | 设为 `true` 去掉右下角 logo |
| `enhance` | boolean | false | 设为 `true` 启用提示词增强 |

**示例：**
```
GET /prompt/a%20sunset%20over%20mountains,%20digital%20art?width=1024&height=768&model=flux&nologo=true
```

## Guidelines

- 提示词建议使用**英文**，中文识别度较低
- 推荐尺寸：1024x576（16:9）、1024x1024（正方形）
- 生成的是图片（image/png），返回二进制流，可直接用 `<img>` 标签或 markdown 展示
- 提示词长度限制：约 500 字符
- 无速率限制，但请合理使用