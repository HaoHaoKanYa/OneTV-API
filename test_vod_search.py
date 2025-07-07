#!/usr/bin/env python3
"""
测试VOD源搜索功能
"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.append('.')

from updates.vod.searcher import search_and_update_vod_sources

async def test_search():
    """测试VOD源搜索"""
    try:
        print("🔍 开始测试VOD源搜索功能...")
        
        # 测试搜索并更新配置文件
        config_file = "test_vod_sources.txt"
        count = await search_and_update_vod_sources(config_file)
        
        print(f"✅ 搜索完成，发现 {count} 个VOD源")
        
        # 检查生成的文件
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                print(f"📄 配置文件已生成，共 {len(lines)} 行")
                print("📋 前10行内容:")
                for i, line in enumerate(lines[:10]):
                    print(f"   {i+1}: {line}")
        else:
            print("❌ 配置文件未生成")
            
    except Exception as e:
        print(f"❌ 搜索异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search())
