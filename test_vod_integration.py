#!/usr/bin/env python3
"""
测试VOD搜索功能集成
"""
import asyncio
import sys
import os
import traceback

# 添加项目路径
sys.path.append('.')

async def test_vod_integration():
    """测试VOD搜索功能集成"""
    try:
        print("🔍 测试VOD搜索功能集成...")
        
        # 1. 测试导入
        print("📥 1. 测试模块导入...")
        from updates.vod.searcher import VODSourceSearcher, search_and_update_vod_sources
        from updates.vod.request import update_vod_sources
        print("✅ 模块导入成功")
        
        # 2. 测试搜索器创建
        print("🔧 2. 测试搜索器创建...")
        searcher = VODSourceSearcher()
        print("✅ 搜索器创建成功")
        
        # 3. 测试社区源收集
        print("👥 3. 测试社区源收集...")
        community_sources = searcher.get_community_sources()
        print(f"✅ 收集到 {len(community_sources)} 个社区源")
        
        # 4. 测试镜像源搜索
        print("🔄 4. 测试镜像源搜索...")
        mirror_sources = await searcher.search_backup_mirrors()
        print(f"✅ 收集到 {len(mirror_sources)} 个镜像源")
        
        # 5. 测试API接口搜索
        print("🔌 5. 测试API接口搜索...")
        api_sources = await searcher.search_api_endpoints()
        print(f"✅ 收集到 {len(api_sources)} 个API源")
        
        # 6. 测试已知域名搜索
        print("🌐 6. 测试已知域名搜索...")
        known_sources = await searcher.search_known_domains()
        print(f"✅ 收集到 {len(known_sources)} 个已知域名源")
        
        # 7. 测试去重功能
        print("🔄 7. 测试去重功能...")
        all_sources = community_sources + mirror_sources + api_sources + known_sources
        unique_sources = searcher.deduplicate_sources(all_sources)
        print(f"✅ 去重前: {len(all_sources)} 个源，去重后: {len(unique_sources)} 个源")
        
        # 8. 测试配置文件生成
        print("💾 8. 测试配置文件生成...")
        test_config_file = "test_vod_sources_integration.txt"
        searcher.save_sources_to_config(unique_sources[:10], test_config_file)  # 只保存前10个用于测试
        
        if os.path.exists(test_config_file):
            with open(test_config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                print(f"✅ 配置文件生成成功，共 {len(lines)} 行")
                print("📋 前5行内容:")
                for i, line in enumerate(lines[:5]):
                    print(f"   {i+1}: {line}")
        else:
            print("❌ 配置文件生成失败")
        
        # 9. 显示源分类统计
        print("📊 9. 源分类统计:")
        categories = {}
        for source in unique_sources:
            category = source.get("category", "未分类")
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            print(f"   - {category}: {count} 个")
        
        print(f"\n🎯 集成测试完成！总共发现 {len(unique_sources)} 个独特VOD源")
        
        # 清理测试文件
        if os.path.exists(test_config_file):
            os.remove(test_config_file)
            print("🧹 测试文件已清理")
            
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_vod_integration())
