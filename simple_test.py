#!/usr/bin/env python3
"""
简单测试VOD搜索功能
"""
import sys
sys.path.append('.')

try:
    print("1. 导入模块...")
    from updates.vod.searcher import VODSourceSearcher
    print("✅ 模块导入成功")
    
    print("2. 创建搜索器...")
    searcher = VODSourceSearcher()
    print("✅ 搜索器创建成功")
    
    print("3. 测试社区源收集...")
    community_sources = searcher.get_community_sources()
    print(f"✅ 收集到 {len(community_sources)} 个社区源")
    
    print("4. 显示前5个源:")
    for i, source in enumerate(community_sources[:5]):
        print(f"   {i+1}. {source['name']}: {source['url']}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
