# -*- coding: utf-8 -*-
import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "\U0001f4f0 \u6bcf\u65e5\u65b0\u95fb\u64ad\u62a5 | 2026\u5e744\u670829\u65e5",
                "content": [
                    [{"tag": "text", "text": "\u4e00\u3001\u56fd\u5185\u8981\u95fb"}],
                    [{"tag": "text", "text": "1. \u4e60\u8fd1\u5e73\u5728\u4e2d\u592e\u653f\u6cbb\u5c40\u7b2c\u4e8c\u5341\u4e94\u6b21\u96c6\u4f53\u5b66\u4e60\u65f6\u5f3a\u8c03\uff1a\u7740\u529b\u63d0\u9ad8\u9632\u8303\u5e94\u5bf9\u81ea\u7136\u707e\u5bb3\u80fd\u529b\uff0c\u5207\u5b9e\u7ef4\u62a4\u4eba\u6c11\u7fa4\u4f17\u751f\u547d\u8d22\u4ea7\u5b89\u5168"}],
                    [{"tag": "text", "text": "2. \u4e60\u8fd1\u5e73\u5411\u4e0a\u6d77\u5408\u4f5c\u7ec4\u7ec7\u7eff\u8272\u548c\u53ef\u6301\u7eed\u53d1\u5c55\u8bba\u575b\u81f4\u8d3a\u4fe1"}],
                    [{"tag": "text", "text": "3. \u4e01\u859b\u7965\u51fa\u5e2d\u7b2c\u4e5d\u5c4a\u6570\u5b57\u4e2d\u56fd\u5efa\u8bbe\u5cf0\u4f1a\u5f00\u5e55\u5f0f\u5e76\u53d1\u8868\u4e3b\u65e8\u8bb2\u8bdd"}],
                    [{"tag": "text", "text": "4. \u97e9\u6b63\u4f1a\u89c1\u7b2c80\u5c4a\u8054\u5408\u56fd\u5927\u4f1a\u4e3b\u5e2d\u8d1d\u5c14\u4f2f\u514b"}],
                    [{"tag": "text", "text": "5. \u4e00\u5b63\u5ea6\u6211\u56fd\u7269\u6d41\u8fd0\u884c\u5b9e\u73b0\u826f\u597d\u5f00\u5c40\uff0c\u6587\u5316\u670d\u52a1\u4e1a\u8425\u4e1a\u6536\u5165\u540c\u6bd4\u589e\u957f9.9%"}],
                    [{"tag": "text", "text": "6. \u300a\u5173\u4e8e\u63a8\u52a8\u4e92\u52a9\u6027\u517b\u8001\u670d\u52a1\u53d1\u5c55\u7684\u610f\u89c1\u300b\u51fa\u53f0"}],
                    [{"tag": "text", "text": "7. \u56fd\u5185\u9996\u6761\u8de8\u6cb8\u6d77\u65e0\u4eba\u673a\u7269\u6d41\u822a\u7ebf\u901a\u822a"}],
                    [{"tag": "text", "text": "8. \u957f\u4e09\u89d2\u9996\u53f0\u201c\u534e\u9f99\u4e00\u53f7\u201d\u6838\u7535\u673a\u7ec4\u6295\u4ea7\u53d1\u7535"}],
                    [{"tag": "text", "text": "9. \u5e02\u573a\u76d1\u7ba1\u603b\u5c40\u542f\u52a8\u7f51\u7edc\u98df\u54c1\u9500\u552e\u865a\u5047\u5ba3\u4f20\u4e13\u9879\u6574\u6cbb\u884c\u52a8"}],
                    [{"tag": "text", "text": "10. \u201c\u4e94\u4e00\u201d\u5047\u671f\u4e34\u8fd1\uff0c\u5404\u5730\u51fa\u53f0\u60e0\u6c11\u4e3e\u63aa\u5e26\u52a8\u6587\u65c5\u6d88\u8d39\uff0c\u4fdd\u969c\u5e02\u573a\u4f9b\u5e94"}],
                    [{"tag": "text", "text": ""}],
                    [{"tag": "text", "text": "\u4e8c\u3001\u56fd\u9645\u8981\u95fb"}],
                    [{"tag": "text", "text": "1. \u7f8e\u79f0\u51c6\u5907\u5ef6\u957f\u5bf9\u4f0a\u6717\u5c01\u9501\uff0c\u4f0a\u6717\u79f0\u5c06\u4e25\u5389\u56de\u5e94\uff1b\u970d\u5c14\u6728\u5179\u6d77\u5ce1\u8239\u8236\u901a\u884c\u91cf\u5927\u964d\uff0c\u6b27\u6d32\u539f\u6cb9\u4ef7\u683c\u5927\u6da8"}],
                    [{"tag": "text", "text": "2. \u963f\u8054\u914b\u5ba3\u5e03\u5c06\u9000\u51fa\u6b27\u4f69\u514b\u53ca\u201c\u6b27\u4f69\u514b+\u201d"}],
                    [{"tag": "text", "text": "3. \u4e16\u884c\u9884\u6d4b\u4eca\u5e74\u5168\u7403\u80fd\u6e90\u4ef7\u683c\u5c06\u4e0a\u6da824%"}],
                    [{"tag": "text", "text": "4. \u7f8e\u53c2\u9662\u672a\u901a\u8fc7\u9650\u5236\u603b\u7edf\u5bf9\u53e4\u5df4\u52a8\u6b66\u8bae\u6848"}],
                    [{"tag": "text", "text": "5. \u7f8e\u5a92\u79f0\u7f8e\u56fd\u56fd\u5bb6\u79d1\u5b66\u59d4\u5458\u4f1a\u5168\u5458\u906d\u89e3\u96c7"}],
                    [{"tag": "text", "text": ""}],
                    [{"tag": "text", "text": "\u2014\u2014 \u5c0f\u76c8 \u00b7 \u6bcf\u65e5\u65b0\u95fb\u64ad\u62a5 \u2014\u2014"}],
                ]
            }
        }
    }
}

response = requests.post(webhook_url, json=payload)
result = response.json()
print(json.dumps(result, indent=2))

if result.get("code") == 0 or result.get("StatusCode") == 0:
    print("\n\u6d88\u606f\u53d1\u9001\u6210\u529f\uff01")
else:
    print(f"\n\u53d1\u9001\u5931\u8d25: {result}")
