// 代码02 v2.0 — 多源竞品报告格式化
// HiAgent JavaScript 代码节点
// 输入: 代码01 输出的 searchResult JSON（含多源数据）
// 输出: 格式化的 Markdown 报告

function handler(params) {
    var input = params.input || '';
    var userQuery = params.user_query || '';

    var results = [];
    try {
        var raw = typeof input === 'string' ? input : JSON.stringify(input);
        var parsed = JSON.parse(raw);

        // 兼容多种包裹格式
        if (parsed.searchResult) {
            results = typeof parsed.searchResult === 'string'
                ? JSON.parse(parsed.searchResult)
                : parsed.searchResult;
        } else if (Array.isArray(parsed)) {
            results = parsed;
        } else {
            results = [parsed];
        }
    } catch (e) {
        return { output: '数据解析失败: ' + e.message + '\n原始数据前200字符: ' + String(input).substring(0, 200) };
    }

    if (!Array.isArray(results)) { results = [results]; }

    var now = new Date();
    var dateStr = now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日';

    // 统计
    var totalScrapeSuccess = 0, totalScrapeModels = 0;
    var totalEcomSuccess = 0, totalEcomProducts = 0;
    var totalNewsSuccess = 0, totalNewsArticles = 0;
    var brandsWithData = 0;

    for (var i = 0; i < results.length; i++) {
        var r = results[i];
        var hasData = false;
        if (r.scrape && r.scrape.status === 'success') { totalScrapeSuccess++; hasData = true; }
        if (r.scrape && r.scrape.models) { totalScrapeModels += r.scrape.models.length; }
        if (r.ecommerce && r.ecommerce.status === 'success') { totalEcomSuccess++; hasData = true; }
        if (r.ecommerce && r.ecommerce.products) { totalEcomProducts += r.ecommerce.products.length; }
        if (r.news && r.news.status === 'success') { totalNewsSuccess++; hasData = true; }
        if (r.news && r.news.articles) { totalNewsArticles += r.news.articles.length; }
        if (hasData) brandsWithData++;
    }

    // 构建报告
    var output = '## 海外冰箱竞品雷达\n\n';
    output += '> 查询: ' + userQuery + ' | 时间: ' + dateStr + '\n\n';

    // 概览表
    output += '| 指标 | 数值 |\n|------|------|\n';
    output += '| 查询品牌数 | ' + results.length + ' |\n';
    output += '| 有数据品牌 | ' + brandsWithData + ' |\n';
    output += '| 官网抓取成功 | ' + totalScrapeSuccess + ' 个品牌 (' + totalScrapeModels + ' 个型号) |\n';
    output += '| 电商数据 | ' + totalEcomSuccess + ' 个品牌 (' + totalEcomProducts + ' 个产品) |\n';
    output += '| 新闻搜索 | ' + totalNewsSuccess + ' 个品牌 (' + totalNewsArticles + ' 篇文章) |\n';
    output += '\n---\n\n';

    // 逐品牌展示
    for (var i = 0; i < results.length; i++) {
        var r = results[i];
        var brand = r.brand || ('品牌' + (i + 1));
        output += '### ' + brand + '\n\n';

        var hasAnyData = false;

        // === 官网数据 ===
        if (r.scrape) {
            var s = r.scrape;
            if (s.status === 'success' && s.models && s.models.length > 0) {
                hasAnyData = true;
                output += '**官网抓取** ✅ | 型号数: ' + s.models.length;
                if (s.page_info && s.page_info.total_shown) {
                    output += ' | 页面总计: ' + s.page_info.total_shown + ' 款';
                }
                output += '\n\n';
                output += '| 型号 |\n|------|\n';
                for (var k = 0; k < s.models.length; k++) {
                    output += '| ' + s.models[k] + ' |\n';
                }
                output += '\n';
            } else if (s.status === 'partial' && s.markdown_preview) {
                hasAnyData = true;
                output += '**官网抓取** ⚠️ 页面抓取成功但未提取到型号\n\n';
                output += '> ' + s.markdown_preview.replace(/\n/g, '\n> ').substring(0, 400) + '\n\n';
            } else if (s.error && s.error.indexOf('无可用官网URL') === -1) {
                output += '**官网抓取** ❌ ' + s.error + '\n\n';
            }
        }

        // === 电商数据 ===
        if (r.ecommerce) {
            var ec = r.ecommerce;
            if (ec.status === 'success' && ec.products && ec.products.length > 0) {
                hasAnyData = true;
                output += '**电商数据** ✅ | 产品数: ' + ec.products.length + '\n\n';
                output += '| 产品 | 价格 | 评分 |\n|------|------|------|\n';
                for (var j = 0; j < ec.products.length; j++) {
                    var p = ec.products[j];
                    output += '| ' + (p.name || '-').substring(0, 80) + ' | ' + (p.price || '-') + ' | ' + (p.rating || '-') + ' |\n';
                }
                output += '\n';
            } else if (ec.status === 'partial' && ec.markdown_preview) {
                hasAnyData = true;
                output += '**电商数据** ⚠️ 页面抓取成功但未提取到产品\n\n';
            } else if (ec.error && ec.error.indexOf('无可用电商URL') === -1) {
                output += '**电商数据** ❌ ' + ec.error + '\n\n';
            }
        }

        // === 新闻搜索 ===
        if (r.news) {
            var n = r.news;
            var articles = n.articles || [];

            if (articles.length > 0) {
                hasAnyData = true;
                output += '**新闻搜索** ✅ | 文章数: ' + articles.length + '\n\n';
                for (var m = 0; m < Math.min(articles.length, 5); m++) {
                    var a = articles[m];
                    output += '- **' + (a.title || '无标题') + '**\n';
                    if (a.snippet) output += '  ' + a.snippet + '\n';
                    if (a.url) output += '  ' + a.url + '\n';
                    if (a.date) output += '  ' + a.date + '\n';
                    output += '\n';
                }
            }
        }

        if (!hasAnyData) {
            output += '暂无数据\n\n';
        }
    }

    output += '---\n\n';
    output += '> 数据来源: 官网抓取 + Amazon电商 + Firecrawl新闻搜索\n';
    output += '> 海外冰箱竞品雷达 v2.0 自动生成\n';

    return { output: output };
}