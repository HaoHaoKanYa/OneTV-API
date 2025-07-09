"""
OneTV-API 点播源处理器
VOD Source Processor Module
"""
import json
import os
from datetime import datetime
from typing import Dict, List

from utils.tools import resource_path


class VODProcessor:
    """点播源处理器"""
    
    def __init__(self):
        self.output_dir = resource_path("vod/output")
        self.whitelist_sources = self._load_whitelist()
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _load_whitelist(self) -> List[Dict]:
        """加载白名单源"""
        whitelist_file = resource_path("vod/config/vod_whitelist.txt")
        whitelist_sources = []

        if not os.path.exists(whitelist_file):
            print("⚠️ 白名单文件不存在，跳过白名单加载")
            return whitelist_sources

        try:
            with open(whitelist_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split("|")
                    if len(parts) >= 4:
                        source = {
                            "url": parts[0].strip(),
                            "name": parts[1].strip(),
                            "category": parts[2].strip(),
                            "description": parts[3].strip(),
                            "quality_score": 100,  # 白名单源默认最高评分
                            "source": "whitelist"
                        }
                        whitelist_sources.append(source)

            print(f"✅ 加载白名单源: {len(whitelist_sources)} 个")
            return whitelist_sources

        except Exception as e:
            print(f"❌ 加载白名单失败: {str(e)}")
            return []

    def _normalize_source_name(self, source: Dict) -> str:
        """规范化源名称"""
        name = source.get("name", "未知源")
        url = source.get("url", "")
        source_type = source.get("source_type", "search")

        # 白名单源保持原名（已经有图标和序号）
        if source_type == "whitelist":
            return name

        # 搜索源规范化命名
        # 移除常见的技术性前缀
        name = name.replace("GitHub-", "").replace("已知域名-", "").replace("镜像-", "")
        name = name.replace("社区-", "").replace("API-", "").replace("config", "配置")

        # 根据URL特征优化命名
        if "gaotianliuyun" in url or "gao" in url:
            if "js.json" in url:
                return "🌟高天流云JS版"
            elif "0821" in url:
                return "🌟高天流云增强版"
            elif "XC.json" in url:
                return "🌟高天流云XC版"
            elif "0707" in url:
                return "🌟高天流云经典版"
            else:
                return "🌟高天流云"
        elif "dudu526" in url or "alan" in url:
            if "X.json" in url:
                return "📚Alan综合仓库"
            elif "jsm.json" in url:
                return "📚Alan精简仓库"
            else:
                return "📚Alan仓库"
        elif "fongmi" in url.lower() or "fengmi" in name.lower():
            return "🎯FongMi影视"
        elif any(keyword in name.lower() for keyword in ["饭太硬", "肥猫", "菜妮丝", "欧歌", "南风"]):
            # 知名开发者源保持原名但添加图标
            if "饭太硬" in name:
                return f"🍚{name}"
            elif "肥猫" in name:
                return f"🐱{name}"
            elif "菜妮丝" in name:
                return f"🥬{name}"
            elif "欧歌" in name:
                return f"🎵{name}"
            elif "南风" in name:
                return f"🌪{name}"
            else:
                return name
        else:
            # 通用规范化
            name = name.replace('.json', '').replace('-', '·').replace('_', '·')
            # 添加适当的图标
            if any(keyword in name.lower() for keyword in ["影视", "电影", "tv", "movie"]):
                return f"🎬{name}"
            elif any(keyword in name.lower() for keyword in ["直播", "live"]):
                return f"📡{name}"
            elif any(keyword in name.lower() for keyword in ["网盘", "云盘", "pan"]):
                return f"☁️{name}"
            elif "tvbox" in name.lower():
                return f"📺{name}"
            elif "config" in name.lower():
                return f"⚙️{name}"
            elif "api" in name.lower():
                return f"🔌{name}"
            else:
                return f"🔗{name}"
    
    def generate_vod_json(self, vod_data: Dict) -> str:
        """生成点播源JSON文件 - 多仓库格式"""
        valid_sources = vod_data.get("valid_sources", [])
        total_sources = vod_data.get("total_sources", 0)

        # 合并白名单源和搜索到的源 - 修复逻辑确保搜索源被包含
        all_sources = []

        # 首先添加白名单源，但降低其评分优势
        for source in self.whitelist_sources:
            # 白名单源评分设为85分，给搜索源留出空间
            source["quality_score"] = 85
            source["source_type"] = "whitelist"
            all_sources.append(source)

        # 添加搜索到的源，排除已在白名单中的URL
        whitelist_urls = {source["url"] for source in self.whitelist_sources}
        search_sources_added = 0
        for source in valid_sources:
            if source["url"] not in whitelist_urls:
                source["source_type"] = "search"
                all_sources.append(source)
                search_sources_added += 1

        if not all_sources:
            print("❌ 没有有效的点播源数据!")
            return ""

        # 按质量评分排序，但确保搜索源和白名单源混合
        # 取前30个源，但至少包含10个搜索源（如果有的话）
        sorted_sources = sorted(all_sources,
                               key=lambda x: x.get("quality_score", 0),
                               reverse=True)

        # 智能选择：确保搜索源和白名单源的平衡
        whitelist_sources_final = [s for s in sorted_sources if s.get("source_type") == "whitelist"][:15]
        search_sources_final = [s for s in sorted_sources if s.get("source_type") == "search"][:15]

        # 合并并按评分重新排序
        top_sources = (whitelist_sources_final + search_sources_final)[:30]
        top_sources = sorted(top_sources, key=lambda x: x.get("quality_score", 0), reverse=True)

        print(f"📊 源统计: 白名单 {len(self.whitelist_sources)} 个, 搜索发现 {search_sources_added} 个")
        print(f"📊 最终选择: 白名单 {len(whitelist_sources_final)} 个, 搜索 {len(search_sources_final)} 个, 总计 {len(top_sources)} 个")

        # 构建多仓库格式的JSON配置 - 基于alan仓库标准优化
        multi_repo_config = {
            "spider": "https://gh.tryxd.cn/https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/spider/pg.jar",
            "wallpaper": "https://深色壁纸.xxooo.cf/",
            "logo": "https://gh.tryxd.cn/https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/logo.png",
            "storeHouse": [
                {
                    "sourceName": "OneTV影视仓库",
                    "sourceUrl": "https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-movie.json"
                }
            ],
            "urls": [],
            "doh": [
                {
                    "name": "Google",
                    "url": "https://dns.google/dns-query",
                    "ips": ["8.8.4.4", "8.8.8.8"]
                },
                {
                    "name": "Cloudflare",
                    "url": "https://cloudflare-dns.com/dns-query",
                    "ips": ["1.1.1.1", "1.0.0.1"]
                }
            ],
            "rules": [
                {
                    "name": "proxy",
                    "hosts": ["raw.githubusercontent.com", "googlevideo.com", "cdn.v82u1l.com"]
                }
            ]
        }

        # 将有效源转换为多仓库格式
        for source in top_sources:
            # 根据质量评分添加星级标识
            quality_score = source.get("quality_score", 0)
            if quality_score >= 95:
                stars = "⭐⭐⭐⭐⭐"
            elif quality_score >= 85:
                stars = "⭐⭐⭐⭐"
            elif quality_score >= 75:
                stars = "⭐⭐⭐"
            elif quality_score >= 65:
                stars = "⭐⭐"
            else:
                stars = "⭐"

            # 规范化源名称
            formatted_name = self._normalize_source_name(source)

            url_config = {
                "url": source["url"],
                "name": f"{formatted_name}{stars}"
            }
            multi_repo_config["urls"].append(url_config)

        # 保存JSON文件
        output_file = os.path.join(self.output_dir, "onetv-api-movie.json")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(multi_repo_config, f, ensure_ascii=False, indent=4)

            print(f"✅ 多仓库配置文件已生成: {output_file}")
            print(f"📊 包含 {len(top_sources)} 个优质源 (从 {total_sources} 个源中筛选)")
            print(f"🏆 平均质量评分: {sum(s['quality_score'] for s in top_sources) / len(top_sources):.1f}")

            # 显示分类统计
            categories = {}
            for source in top_sources:
                category = source.get("category", "未分类")
                categories[category] = categories.get(category, 0) + 1
            print(f"📂 分类统计: {categories}")

            return output_file

        except Exception as e:
            print(f"❌ 生成JSON文件失败: {str(e)}")
            return ""
    
    def generate_statistics(self, vod_data: Dict) -> Dict:
        """生成统计信息"""
        valid_sources = vod_data.get("valid_sources", [])
        total_sources = vod_data.get("total_sources", 0)
        
        # 分类统计
        categories = {}
        quality_distribution = {"优秀(90+)": 0, "良好(80-89)": 0, "及格(70-79)": 0}
        
        for source in valid_sources:
            # 分类统计
            category = source.get("category", "未分类")
            categories[category] = categories.get(category, 0) + 1
            
            # 质量分布
            score = source.get("quality_score", 0)
            if score >= 90:
                quality_distribution["优秀(90+)"] += 1
            elif score >= 80:
                quality_distribution["良好(80-89)"] += 1
            else:
                quality_distribution["及格(70-79)"] += 1
        
        # 响应时间统计
        response_times = [s.get("response_time", 0) for s in valid_sources]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        statistics = {
            "summary": {
                "total_configured": total_sources,
                "valid_sources": len(valid_sources),
                "success_rate": f"{(len(valid_sources) / total_sources * 100):.1f}%" if total_sources > 0 else "0%",
                "average_quality_score": f"{vod_data.get('average_score', 0):.1f}",
                "average_response_time": f"{avg_response_time:.2f}s",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "categories": categories,
            "quality_distribution": quality_distribution,
            "top_sources": sorted(valid_sources, key=lambda x: x.get("quality_score", 0), reverse=True)[:10]
        }
        
        return statistics
    
    def save_statistics(self, statistics: Dict) -> str:
        """保存统计信息"""
        stats_file = os.path.join(self.output_dir, "vod_statistics.json")
        
        try:
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(statistics, f, ensure_ascii=False, indent=2)
            
            print(f"📊 统计信息已保存: {stats_file}")
            return stats_file
            
        except Exception as e:
            print(f"❌ 保存统计信息失败: {str(e)}")
            return ""


def process_vod_sources(vod_data: Dict) -> Dict:
    """处理点播源数据的主函数"""
    processor = VODProcessor()
    
    # 生成JSON文件
    json_file = processor.generate_vod_json(vod_data)
    
    # 生成统计信息
    statistics = processor.generate_statistics(vod_data)
    stats_file = processor.save_statistics(statistics)
    
    return {
        "json_file": json_file,
        "statistics_file": stats_file,
        "statistics": statistics
    }
