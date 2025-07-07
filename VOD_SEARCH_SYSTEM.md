# OneTV-API 动态VOD源搜索系统

## 🎯 系统概述

OneTV-API 动态VOD源搜索系统是一个全自动的点播源发现和管理系统，能够从全网搜索并发现高质量的VOD配置源，大幅提升点播源的数量和质量。

## ✨ 核心功能

### 1. 多策略搜索引擎
- **GitHub仓库搜索**: 使用GitHub API搜索TVBox、CatVod相关仓库
- **社区分享源**: 内置30+高质量社区维护的VOD源
- **备用镜像搜索**: 支持GitHub加速服务和镜像站点
- **API接口搜索**: 包含欧歌等专业API接口
- **已知域名搜索**: 覆盖主流代码托管平台

### 2. 智能源管理
- **自动去重**: 基于URL的智能去重算法
- **分类管理**: 按来源和类型自动分类
- **质量评估**: 预评估源的可用性和质量
- **动态更新**: 自动更新配置文件，无需手动维护

### 3. 无缝集成
- **现有流程兼容**: 与现有VOD验证流程完全兼容
- **配置文件更新**: 自动更新vod_sources.txt配置文件
- **统计报告**: 详细的搜索和验证统计信息

## 🔧 技术架构

### 核心类: VODSourceSearcher

```python
class VODSourceSearcher:
    async def search_all_sources() -> List[Dict]
    async def search_github_repositories() -> List[Dict]
    async def search_community_sources() -> List[Dict]
    async def search_backup_mirrors() -> List[Dict]
    async def search_api_endpoints() -> List[Dict]
    async def search_known_domains() -> List[Dict]
    def get_community_sources() -> List[Dict]
    def deduplicate_sources() -> List[Dict]
    def save_sources_to_config() -> None
```

### 搜索策略详解

#### 1. GitHub仓库搜索
- 搜索关键词: "tvbox json", "catvodspider config", "影视 json"
- 目标文件: config.json, api.json, tv.json, main.json等
- 支持多分支: master, main
- 获取仓库元信息: stars, 更新时间, 语言

#### 2. 社区分享源 (30+高质量源)
```
拾光路线系列:
- 拾光趣乐屋, 拾光多仓, 拾光电视版

欧歌路线系列:
- 欧歌官方API, 多多欧歌线路

饭太硬系列:
- 饭太硬官方, 饭太硬备用, 日后魔改版

肥猫系列:
- 肥猫官方, 肥猫备用, 日后魔改版

专业维护源:
- 南风线路, 俊佬线路, 骚零线路

... 等30+个高质量源
```

#### 3. 备用镜像搜索
- GitHub镜像服务: github.moeyy.xyz, mirror.ghproxy.com等
- 知名仓库: gaotianliuyun/gao, FongMi/CatVodSpider等
- 多配置文件: 0707.json, 0821.json, config.json等

#### 4. API接口搜索
- 欧歌API系列: 多个官方API接口
- 动态接口发现: 支持参数化API搜索

#### 5. 已知域名搜索
- 代码托管平台: GitHub, Gitee, GitLab等
- 知名账户: 高天流云, FongMi, 通讯录等
- 路径模式匹配: 多种常见配置文件路径

## 📊 预期效果

### 数量提升
- **搜索前**: 32个静态配置源
- **搜索后**: 数百个动态发现源
- **增长倍数**: 10-20倍源数量增长

### 质量提升
- **成功率**: 从21.9%提升到预期60%+
- **覆盖面**: 全网最新最全的VOD源
- **时效性**: 自动发现最新更新的源

### 维护效率
- **自动化**: 无需手动添加和维护源
- **实时性**: 每周自动全网搜索更新
- **智能化**: 自动去重和分类管理

## 🚀 使用方法

### 自动运行 (推荐)
系统已集成到GitHub Actions工作流中，每周日自动运行:
```yaml
# .github/workflows/update-vod.yml
- cron: '0 16 * * 0'  # 每周日24点执行
```

### 手动触发
在GitHub Actions页面手动触发"🎬 Update VOD Sources"工作流

### 本地测试
```bash
# 运行搜索功能测试
python test_vod_search_simple.py

# 运行完整集成测试
python test_vod_integration.py
```

## 📈 监控和统计

### 搜索统计
- 发现源数量
- 各类别源分布
- 搜索耗时统计

### 验证统计
- 有效源数量和比例
- 平均质量评分
- 平均响应时间

### 上传统计
- Supabase上传状态
- 公共访问地址
- 文件大小和更新时间

## 🔗 访问地址

生成的VOD配置文件可通过以下地址访问:
```
https://sjlmgylmcxrapwxjfzhy.supabase.co/storage/v1/object/public/vod-sources/onetv-api-movie.json
```

## 🎉 总结

OneTV-API动态VOD源搜索系统实现了从静态配置到动态发现的重大升级，通过多策略搜索引擎和智能管理系统，大幅提升了VOD源的数量、质量和时效性，为用户提供更丰富、更稳定的点播体验。
