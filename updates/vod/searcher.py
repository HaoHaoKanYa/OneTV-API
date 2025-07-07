"""
VOD Source Search Engine
全网VOD源搜索引擎
"""
import asyncio
import aiohttp
import json
from typing import List, Dict
from datetime import datetime


class VODSourceSearcher:
    """VOD源全网搜索引擎"""
    
    def __init__(self):
        self.found_sources = []
        self.processed_urls = set()
        self.search_keywords = [
            "tvbox", "catvodspider", "影视", "点播", "vod", "json",
            "饭太硬", "肥猫", "菜妮丝", "拾光", "欧歌", "高天流云",
            "南风", "俊佬", "骚零", "青宁", "猫TV", "FongMi"
        ]
        
    async def search_all_sources(self) -> List[Dict]:
        """执行全网VOD源搜索"""
        print("🔍 开始全网VOD源搜索...")

        # 并行执行多种搜索方式
        search_tasks = [
            self.search_github_repositories(),
            self.search_known_domains(),
            self.search_community_sources(),
            self.search_backup_mirrors(),
            self.search_api_endpoints()
        ]

        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        # 合并所有搜索结果
        all_sources = []
        for result in results:
            if isinstance(result, list):
                all_sources.extend(result)
            elif isinstance(result, Exception):
                print(f"⚠️ 搜索任务异常: {result}")

        # 添加社区已知优质源
        community_sources = self.get_community_sources()
        all_sources.extend(community_sources)

        # 去重和清理
        unique_sources = self.deduplicate_sources(all_sources)

        print(f"🎯 全网搜索完成，发现 {len(unique_sources)} 个独特VOD源")
        return unique_sources
    
    def get_community_sources(self) -> List[Dict]:
        """获取社区已知的优质VOD源"""
        print("� 收集社区优质源...")

        # 社区已知的优质VOD源
        community_sources = [
            # 拾光路线系列
            {"url": "http://xmbjm.fh4u.org/ck.txt", "name": "拾光趣乐屋", "category": "综合影视", "description": "拾光路线主力源"},
            {"url": "https://qixing.myhkw.com/DC.txt", "name": "拾光多仓", "category": "多仓配置", "description": "拾光多仓聚合"},
            {"url": "http://xmbjm.fh4u.org/tv.txt", "name": "拾光电视", "category": "直播点播", "description": "拾光电视版"},

            # 欧歌路线系列
            {"url": "https://xn--xkkx-rp5imh.v.nxog.top/api.php?id=3", "name": "欧歌单线路", "category": "专业线路", "description": "欧歌官方接口"},
            {"url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/mcp2016/TVBox/main/backup/多多┃欧歌线路.json", "name": "多多欧歌线路", "category": "欧歌备用", "description": "GitHub加速版"},

            # 饭太硬系列
            {"url": "http://饭太硬.top/tv", "name": "饭太硬官方", "category": "综合影视", "description": "饭太硬官方源"},
            {"url": "http://fan.xxooo.cf/tv", "name": "饭太硬备用", "category": "综合影视", "description": "饭太硬备用源"},
            {"url": "http://rihou.cc:55/饭太硬/日后魔改", "name": "日后魔改饭太硬", "category": "魔改版本", "description": "日后魔改版"},

            # 肥猫系列
            {"url": "http://我不是.肥猫.love:63/接口", "name": "肥猫官方", "category": "综合影视", "description": "肥猫官方源"},
            {"url": "http://肥猫.live", "name": "肥猫备用", "category": "综合影视", "description": "肥猫备用源"},
            {"url": "http://rihou.cc:55/肥猫/日后魔改", "name": "日后魔改肥猫", "category": "魔改版本", "description": "日后魔改版"},

            # 菜妮丝系列
            {"url": "https://tvbox.cainisi.cf", "name": "菜妮丝官方", "category": "综合影视", "description": "菜妮丝官方源"},
            {"url": "http://rihou.cc:55/菜妮丝/日后魔改", "name": "日后魔改菜妮丝", "category": "魔改版本", "description": "日后魔改版"},

            # 高天流云系列
            {"url": "https://raw.githubusercontent.com/gaotianliuyun/gao/master/0707.json", "name": "高天流云Fengmi", "category": "Fengmi专用", "description": "Fengmi影视多线"},
            {"url": "https://raw.githubusercontent.com/gaotianliuyun/gao/master/0821.json", "name": "高天流云增强", "category": "大而全配置", "description": "增强版配置"},
            {"url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/gaotianliuyun/gao/master/0821.json", "name": "高天流云加速", "category": "GitHub加速", "description": "运输车加速版"},

            # 专业维护源
            {"url": "https://agit.ai/Yoursmile7/TVBox/raw/branch/master/XC.json", "name": "南风线路", "category": "专业维护", "description": "南风专业维护"},
            {"url": "http://home.jundie.top:81/top98.json", "name": "俊佬线路", "category": "专业维护", "description": "俊佬专业线路"},
            {"url": "https://100km.top/0", "name": "骚零线路", "category": "专业维护", "description": "骚零专业源"},

            # 特色专用源
            {"url": "http://tv.rihou.cc/天天开心", "name": "天天开心", "category": "综合影视", "description": "天天开心源"},
            {"url": "http://rihou.cc:88/荷城茶秀", "name": "荷城茶秀", "category": "综合影视", "description": "荷城茶秀源"},
            {"url": "https://agit.ai/hu/hcr/raw/branch/master/短剧.json", "name": "短剧频道", "category": "短剧专用", "description": "短剧专门频道"},
            {"url": "https://jihulab.com/ymz1231/xymz/-/raw/main/ymshaoer", "name": "少儿频道", "category": "少儿专用", "description": "少儿专门频道"},

            # 小米系列
            {"url": "http://xhww.fun/小米/DEMO.json", "name": "小米官方", "category": "综合影视", "description": "小米官方源"},

            # 多仓聚合源
            {"url": "https://raw.githubusercontent.com/tongxunlu/tvbox-tvb-gd/master/0707.json", "name": "Fengmi影视多线", "category": "多线配置", "description": "Fengmi影视专用"},
            {"url": "https://raw.githubusercontent.com/tongxunlu/tvbox-tvb-gd/master/0821.json", "name": "大而全配置", "category": "综合配置", "description": "大而全聚合配置"},

            # GitHub优质源
            {"url": "https://raw.githubusercontent.com/Zhou-Li-Bin/Tvbox-QingNing/main/api.json", "name": "青宁线路", "category": "GitHub维护", "description": "青宁专业维护"},
            {"url": "https://mirror.ghproxy.com/https://raw.githubusercontent.com/Zhou-Li-Bin/Tvbox-QingNing/main/api.json", "name": "青宁加速", "category": "GitHub加速", "description": "青宁加速版"},

            # 备用稳定源
            {"url": "https://notabug.org/laoo1976/maotv/raw/master/test.json", "name": "猫TV测试", "category": "测试配置", "description": "猫TV测试源"},
            {"url": "https://gitee.com/tvboxjk/tvbox/raw/master/api.json", "name": "码云备用", "category": "码云托管", "description": "码云备用源"},

            # 海外优质源
            {"url": "https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/config.json", "name": "FongMi官方", "category": "海外维护", "description": "FongMi官方配置"},
            {"url": "https://github.moeyy.xyz/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/config.json", "name": "FongMi加速", "category": "海外加速", "description": "FongMi加速版"},
        ]

        return community_sources

    async def search_github_repositories(self) -> List[Dict]:
        """搜索GitHub上的VOD源仓库"""
        print("📂 搜索GitHub仓库...")
        sources = []

        # GitHub搜索API (无需认证的公开搜索)
        github_queries = [
            "tvbox json",
            "catvodspider config",
            "影视 json",
            "vod config json",
            "tvbox 配置"
        ]

        async with aiohttp.ClientSession() as session:
            for query in github_queries:
                try:
                    # 使用GitHub搜索API
                    search_url = f"https://api.github.com/search/repositories?q={query}&sort=updated&per_page=20"

                    async with session.get(search_url, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()

                            for repo in data.get('items', []):
                                # 搜索仓库中的JSON配置文件
                                repo_sources = await self.search_repo_contents(session, repo)
                                sources.extend(repo_sources)

                except Exception as e:
                    print(f"⚠️ GitHub搜索异常 ({query}): {e}")

                await asyncio.sleep(1)  # 避免API限制

        return sources

    async def search_repo_contents(self, session: aiohttp.ClientSession, repo: Dict) -> List[Dict]:
        """搜索单个仓库的内容"""
        sources = []

        try:
            # 获取仓库内容
            contents_url = f"https://api.github.com/repos/{repo['full_name']}/contents"

            async with session.get(contents_url, timeout=10) as response:
                if response.status == 200:
                    contents = await response.json()

                    for item in contents:
                        if item['type'] == 'file' and item['name'].endswith('.json'):
                            # 构建原始文件URL
                            raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{item['name']}"

                            source = {
                                "url": raw_url,
                                "name": f"{repo['name']}-{item['name']}",
                                "category": "GitHub维护",
                                "description": f"来自GitHub仓库: {repo['full_name']}",
                                "source_type": "github",
                                "repo_info": {
                                    "stars": repo.get('stargazers_count', 0),
                                    "updated": repo.get('updated_at', ''),
                                    "language": repo.get('language', '')
                                }
                            }
                            sources.append(source)

        except Exception as e:
            print(f"⚠️ 仓库内容搜索异常: {e}")

        return sources

    async def search_known_domains(self) -> List[Dict]:
        """搜索已知的VOD源域名"""
        print("🌐 收集已知域名源...")
        sources = []

        # 已知的VOD源域名和路径组合
        known_urls = [
            # 饭太硬系列变体
            {"url": "http://饭太硬.top/tv", "name": "饭太硬官方TV", "category": "综合影视", "description": "饭太硬官方TV接口"},
            {"url": "http://饭太硬.top/api", "name": "饭太硬官方API", "category": "综合影视", "description": "饭太硬官方API接口"},
            {"url": "http://fan.xxooo.cf/tv", "name": "饭太硬备用TV", "category": "综合影视", "description": "饭太硬备用TV接口"},
            {"url": "http://fan.xxooo.cf/api", "name": "饭太硬备用API", "category": "综合影视", "description": "饭太硬备用API接口"},

            # 肥猫系列变体
            {"url": "http://我不是.肥猫.love:63/接口", "name": "肥猫官方接口", "category": "综合影视", "description": "肥猫官方接口"},
            {"url": "http://肥猫.live", "name": "肥猫Live", "category": "综合影视", "description": "肥猫Live源"},
            {"url": "http://肥猫.live/api", "name": "肥猫Live API", "category": "综合影视", "description": "肥猫Live API接口"},

            # 菜妮丝系列变体
            {"url": "https://tvbox.cainisi.cf", "name": "菜妮丝TVBox", "category": "综合影视", "description": "菜妮丝TVBox源"},
            {"url": "https://tvbox.cainisi.cf/api", "name": "菜妮丝API", "category": "综合影视", "description": "菜妮丝API接口"},

            # 其他知名源变体
            {"url": "http://xmbjm.fh4u.org/ck.txt", "name": "拾光趣乐屋CK", "category": "综合影视", "description": "拾光趣乐屋CK版"},
            {"url": "http://xmbjm.fh4u.org/tv.txt", "name": "拾光电视TXT", "category": "直播点播", "description": "拾光电视TXT版"},
            {"url": "https://qixing.myhkw.com/DC.txt", "name": "拾光多仓DC", "category": "多仓配置", "description": "拾光多仓DC版"},
            {"url": "http://home.jundie.top:81/top98.json", "name": "俊佬Top98", "category": "专业维护", "description": "俊佬Top98配置"},
            {"url": "https://100km.top/0", "name": "骚零主线", "category": "专业维护", "description": "骚零主线配置"},
            {"url": "http://tv.rihou.cc/天天开心", "name": "天天开心TV", "category": "综合影视", "description": "天天开心TV源"},
            {"url": "http://rihou.cc:88/荷城茶秀", "name": "荷城茶秀88", "category": "综合影视", "description": "荷城茶秀88端口"},
            {"url": "http://xhww.fun/小米/DEMO.json", "name": "小米Demo", "category": "综合影视", "description": "小米Demo配置"},
        ]

        for source_info in known_urls:
            if source_info["url"] not in self.processed_urls:
                self.processed_urls.add(source_info["url"])
                sources.append({
                    "url": source_info["url"],
                    "name": source_info["name"],
                    "category": source_info["category"],
                    "description": source_info["description"],
                    "source_type": "known_domain"
                })

        return sources
    
    async def search_community_sources(self) -> List[Dict]:
        """搜索社区分享的VOD源"""
        print("👥 搜索社区源...")
        sources = []

        # 社区分享平台的API
        community_urls = [
            ("https://api.github.com/search/repositories?q=tvbox&sort=updated&per_page=30", "github"),
            ("https://gitee.com/api/v5/search/repositories?q=tvbox&sort=updated&per_page=20", "gitee"),
        ]

        async with aiohttp.ClientSession() as session:
            for url, platform in community_urls:
                try:
                    async with session.get(url, timeout=15) as response:
                        if response.status == 200:
                            data = await response.json()

                            # 根据不同平台解析数据
                            if platform == "github":
                                sources.extend(self.parse_github_search_results(data))
                            elif platform == "gitee":
                                sources.extend(self.parse_gitee_results(data))

                except Exception as e:
                    print(f"⚠️ 社区搜索异常 ({platform}): {e}")

        return sources

    def parse_github_search_results(self, data: Dict) -> List[Dict]:
        """解析GitHub搜索结果"""
        sources = []

        for repo in data.get('items', []):
            # 构建可能的配置文件URL
            possible_files = ['config.json', 'api.json', 'tv.json', 'main.json', '0707.json', '0821.json']

            for filename in possible_files:
                url = f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{filename}"

                source = {
                    "url": url,
                    "name": f"GitHub-{repo['name']}-{filename}",
                    "category": "社区分享",
                    "description": f"来自GitHub仓库: {repo['full_name']}",
                    "source_type": "github_community",
                    "repo_info": {
                        "stars": repo.get('stargazers_count', 0),
                        "updated": repo.get('updated_at', ''),
                        "language": repo.get('language', '')
                    }
                }
                sources.append(source)

        return sources

    def parse_gitee_results(self, data: List) -> List[Dict]:
        """解析Gitee搜索结果"""
        sources = []
        
        for repo in data:
            # 构建可能的配置文件URL
            possible_files = ['config.json', 'api.json', 'tv.json', 'main.json']
            
            for filename in possible_files:
                url = f"https://gitee.com/{repo['full_name']}/raw/master/{filename}"
                
                source = {
                    "url": url,
                    "name": f"Gitee-{repo['name']}-{filename}",
                    "category": "社区分享", 
                    "description": f"来自Gitee仓库: {repo['full_name']}",
                    "source_type": "gitee"
                }
                sources.append(source)
        
        return sources
    
    async def search_backup_mirrors(self) -> List[Dict]:
        """搜索备用镜像源"""
        print("🔄 搜索镜像源...")
        sources = []
        
        # GitHub镜像服务
        mirror_services = [
            "https://github.moeyy.xyz/",
            "https://mirror.ghproxy.com/",
            "https://ghproxy.com/",
            "https://github.com.cnpmjs.org/"
        ]
        
        # 知名的GitHub VOD仓库
        popular_repos = [
            "gaotianliuyun/gao",
            "FongMi/CatVodSpider", 
            "tongxunlu/tvbox-tvb-gd",
            "Zhou-Li-Bin/Tvbox-QingNing"
        ]
        
        for mirror in mirror_services:
            for repo in popular_repos:
                # 常见的配置文件名
                config_files = [
                    "master/config.json",
                    "master/api.json", 
                    "master/0707.json",
                    "master/0821.json",
                    "main/config.json",
                    "main/api.json"
                ]
                
                for config_file in config_files:
                    url = f"{mirror}https://raw.githubusercontent.com/{repo}/{config_file}"
                    
                    source = {
                        "url": url,
                        "name": f"镜像-{repo.split('/')[-1]}-{config_file.split('/')[-1]}",
                        "category": "镜像加速",
                        "description": f"GitHub镜像: {repo}",
                        "source_type": "mirror"
                    }
                    sources.append(source)
        
        return sources
    
    async def search_api_endpoints(self) -> List[Dict]:
        """搜索API接口源"""
        print("🔌 搜索API接口...")
        sources = []
        
        # API接口模式
        api_patterns = [
            "https://xn--xkkx-rp5imh.v.nxog.top/api.php?id=3",
            "https://xn--xkkx-rp5imh.v.nxog.top/api.php?id=1", 
            "https://xn--xkkx-rp5imh.v.nxog.top/api.php?id=2",
        ]
        
        for i, url in enumerate(api_patterns):
            source = {
                "url": url,
                "name": f"欧歌API-{i+1}",
                "category": "API接口",
                "description": "欧歌官方API接口",
                "source_type": "api"
            }
            sources.append(source)
        
        return sources

    async def search_known_domains(self) -> List[Dict]:
        """搜索已知域名的VOD源"""
        print("🌐 搜索已知域名...")
        sources = []

        # 已知的VOD托管域名
        known_domains = [
            "raw.githubusercontent.com",
            "gitee.com",
            "agit.ai",
            "gitlab.com",
            "coding.net",
            "jihulab.com"
        ]

        # 常见的路径模式
        path_patterns = [
            "/master/config.json",
            "/master/api.json",
            "/master/tv.json",
            "/master/main.json",
            "/main/config.json",
            "/main/api.json",
            "/main/tv.json",
            "/main/main.json"
        ]

        # 已知的用户/组织
        known_accounts = [
            "gaotianliuyun/gao",
            "FongMi/CatVodSpider",
            "tongxunlu/tvbox-tvb-gd",
            "Zhou-Li-Bin/Tvbox-QingNing",
            "takagen99/Box",
            "q215613905/TVBoxOS"
        ]

        for domain in known_domains:
            for account in known_accounts:
                for pattern in path_patterns:
                    if domain == "raw.githubusercontent.com":
                        url = f"https://{domain}/{account}{pattern}"
                    elif domain == "gitee.com":
                        url = f"https://{domain}/{account}/raw/master{pattern.replace('/master', '').replace('/main', '')}"
                    else:
                        url = f"https://{domain}/{account}/raw/branch/master{pattern.replace('/master', '').replace('/main', '')}"

                    source = {
                        "url": url,
                        "name": f"已知域名-{account.split('/')[-1]}-{pattern.split('/')[-1]}",
                        "category": "已知域名",
                        "description": f"来自已知域名: {domain}/{account}",
                        "source_type": "known_domain"
                    }
                    sources.append(source)

        return sources

    def deduplicate_sources(self, sources: List[Dict]) -> List[Dict]:
        """去重VOD源"""
        seen_urls = set()
        unique_sources = []
        
        for source in sources:
            url = source["url"]
            if url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append(source)
        
        return unique_sources
    
    def save_sources_to_config(self, sources: List[Dict], config_file: str):
        """将搜索到的源保存到配置文件"""
        print(f"💾 保存 {len(sources)} 个源到配置文件...")
        
        # 按分类分组
        categories = {}
        for source in sources:
            category = source.get("category", "未分类")
            if category not in categories:
                categories[category] = []
            categories[category].append(source)
        
        # 生成配置文件内容
        config_content = [
            "# OneTV-API 点播源配置文件 (自动生成)",
            "# VOD Sources Configuration File (Auto Generated)",
            f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"# 总源数量: {len(sources)}",
            "# 格式: URL|名称|分类|备注",
            ""
        ]
        
        # 按分类写入源
        for category, category_sources in categories.items():
            config_content.append(f"# === {category} ({len(category_sources)}个) ===")
            
            for source in category_sources:
                line = f"{source['url']}|{source['name']}|{source['category']}|{source.get('description', '')}"
                config_content.append(line)
            
            config_content.append("")
        
        # 添加说明
        config_content.extend([
            "# 配置说明:",
            "# 1. 以#开头的行为注释", 
            "# 2. 格式: URL|名称|分类|备注",
            "# 3. 本文件由全网搜索系统自动生成和更新",
            "# 4. 系统会自动验证所有源的可用性和质量",
            ""
        ])
        
        # 写入文件
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                f.write("\n".join(config_content))
            print(f"✅ 配置文件已更新: {config_file}")
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")


async def search_and_update_vod_sources(config_file: str = "vod/config/vod_sources.txt") -> int:
    """搜索并更新VOD源配置文件"""
    searcher = VODSourceSearcher()
    
    # 执行全网搜索
    sources = await searcher.search_all_sources()
    
    # 保存到配置文件
    searcher.save_sources_to_config(sources, config_file)
    
    return len(sources)


if __name__ == "__main__":
    # 测试搜索功能
    asyncio.run(search_and_update_vod_sources())
