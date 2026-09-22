function handler(params) {
    var input = params.input || '';
    var userQuery = params.user_query || '';

    // 解析输入 - 可能是字符串或已解析的数组
    var results = [];
    try {
        results = typeof input === 'string' ? JSON.parse(input) : input;
    } catch (e) {
        return { output: '解析输入数据失败: ' + e.message };
    }
    if (!Array.isArray(results)) {
        results = [results];
    }

    var now = new Date();
    var dateStr = now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日';

    var isListQuery = /列表|列出|有哪些|产品|什么产品|哪些|所有|全部/.test(userQuery);
    var isNewQuery = /新品|上市|发布|新上|有无|有没有|最近/.test(userQuery);

    var output = '## 海外冰箱竞品雷达\n\n';
    output += '> 查询: ' + userQuery + ' | 时间: ' + dateStr + '\n\n';

    for (var i = 0; i < results.length; i++) {
        var r = results[i];
        var brand = r.brand || ('品牌' + (i + 1));
        output += '### ' + brand + '\n\n';

        if (r.error) {
            output += '状态: ' + r.error + '\n\n';
        }

        // 处理 fallback_search (Bocha 搜索结果)
        if (r.fallback_search) {
            var fs = r.fallback_search;
            try {
                if (typeof fs === 'string') { fs = JSON.parse(fs); }
            } catch (e) {}

            var webPages = (fs && fs.data && fs.data.webPages && fs.data.webPages.value) || [];

            if (webPages.length > 0) {
                output += '来源: 搜索引擎\n\n';
                for (var j = 0; j < Math.min(webPages.length, 5); j++) {
                    var p = webPages[j];
                    var title = (p.name || '').replace(/\\\\/g, '');
                    var snippet = (p.snippet || '').replace(/\\\\/g, '').substring(0, 200);
                    output += '- **' + title + '**\n';
                    output += '  ' + snippet + '\n';
                    if (p.url) {
                        output += '  ' + p.url + '\n';
                    }
                    output += '\n';
                }
            } else {
                output += '未获取到相关搜索结果\n\n';
            }
        }

        // 处理有型号的情况
        if (r.models && r.models.length > 0) {
            output += '提取到型号: ' + r.models.join(', ') + '\n\n';
        }

        // 处理 Firecrawl 抓取结果
        if (r.markdown) {
            output += '官网内容预览:\n>' + r.markdown.substring(0, 300).replace(/\n/g, '\n> ') + '\n\n';
        }
    }

    output += '---\n\n> 海外冰箱竞品雷达 自动生成\n';

    return { output: output };
}