#!/usr/bin/env python3
"""
VOD统计信息生成脚本
用于GitHub Actions工作流中生成统计摘要
"""
import json
import sys
import os

def generate_summary():
    """生成VOD统计摘要"""
    try:
        # 检查统计文件是否存在
        stats_file = "vod/output/vod_statistics.json"
        if not os.path.exists(stats_file):
            print("⚠️ 统计信息文件未生成")
            return
        
        # 读取统计数据
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        summary = stats.get('summary', {})
        categories = stats.get('categories', {})
        
        # 输出基本统计
        print("### 📊 更新统计")
        print(f"- **配置源数量**: {summary.get('total_configured', 0)}")
        print(f"- **有效源数量**: {summary.get('valid_sources', 0)}")
        print(f"- **成功率**: {summary.get('success_rate', '0%')}")
        print(f"- **平均质量评分**: {summary.get('average_quality_score', '0')}")
        print(f"- **平均响应时间**: {summary.get('average_response_time', '0s')}")
        print("")
        
        # 输出分类统计
        print("### 📂 分类统计")
        for category, count in categories.items():
            print(f"- **{category}**: {count} 个源")
            
    except Exception as e:
        print(f"统计信息读取失败: {str(e)}")

if __name__ == "__main__":
    generate_summary()
