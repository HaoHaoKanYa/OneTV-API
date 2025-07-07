#!/usr/bin/env python3
"""
简单的VOD搜索功能测试
"""
import sys
import os

# 添加项目路径
sys.path.append('.')

def main():
    print("🔍 开始简单VOD搜索功能测试...")
    
    try:
        # 1. 测试导入
        print("1. 测试模块导入...")
        from updates.vod.searcher import VODSourceSearcher
        print("   ✅ VODSourceSearcher 导入成功")
        
        # 2. 创建搜索器
        print("2. 创建搜索器...")
        searcher = VODSourceSearcher()
        print("   ✅ 搜索器创建成功")
        
        # 3. 测试社区源收集
        print("3. 测试社区源收集...")
        community_sources = searcher.get_community_sources()
        print(f"   ✅ 收集到 {len(community_sources)} 个社区源")
        
        # 4. 显示统计信息
        print("4. 源分类统计:")
        categories = {}
        for source in community_sources:
            category = source.get("category", "未分类")
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            print(f"   - {category}: {count} 个")
        
        print(f"\n🎯 测试完成！总共发现 {len(community_sources)} 个社区VOD源")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print("=" * 50)
    if success:
        print("🎉 VOD搜索功能测试通过！")
    else:
        print("⚠️ VOD搜索功能测试失败！")
    sys.exit(0 if success else 1)
