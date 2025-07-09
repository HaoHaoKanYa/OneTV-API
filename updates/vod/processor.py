"""
OneTV-API 点播源处理器
VOD Source Processor Module
"""
import json
import os
from datetime import datetime
from typing import Dict

from utils.tools import resource_path


class VODProcessor:
    """点播源处理器"""
    
    def __init__(self):
        self.output_dir = resource_path("vod/output")
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_vod_json(self, vod_data: Dict) -> str:
        """生成点播源JSON文件 - 多仓库格式"""
        valid_sources = vod_data.get("valid_sources", [])
        total_sources = vod_data.get("total_sources", 0)

        if not valid_sources:
            print("❌ 没有有效的点播源数据!")
            return ""

        # 按质量评分排序，取前30个最优质源
        top_sources = sorted(valid_sources,
                            key=lambda x: x.get("quality_score", 0),
                            reverse=True)[:30]

        # 构建多仓库格式的JSON配置 - 带品牌识别
        multi_repo_config = {
            "storeHouse": [
                {
                    "sourceName": "OneTV影视仓库",
                    "sourceUrl": "https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-movie.json"
                }
            ],
            "urls": []
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

            url_config = {
                "url": source["url"],
                "name": f"{source['name']}{stars}"
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
