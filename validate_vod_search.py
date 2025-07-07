#!/usr/bin/env python3
"""
验证VOD搜索功能
"""
import os
import sys

# 添加项目路径
sys.path.append('.')

def test_imports():
    """测试模块导入"""
    try:
        print("📥 测试模块导入...")
        
        # 测试基础导入
        from updates.vod.searcher import VODSourceSearcher
        print("✅ VODSourceSearcher 导入成功")
        
        from updates.vod.searcher import search_and_update_vod_sources
        print("✅ search_and_update_vod_sources 导入成功")
        
        from updates.vod.request import update_vod_sources
        print("✅ update_vod_sources 导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_searcher_creation():
    """测试搜索器创建"""
    try:
        print("🔧 测试搜索器创建...")
        from updates.vod.searcher import VODSourceSearcher
        
        searcher = VODSourceSearcher()
        print("✅ 搜索器创建成功")
        
        # 测试社区源收集
        community_sources = searcher.get_community_sources()
        print(f"✅ 收集到 {len(community_sources)} 个社区源")
        
        # 显示前3个源
        print("📋 前3个社区源:")
        for i, source in enumerate(community_sources[:3]):
            print(f"   {i+1}. {source['name']}: {source['category']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 搜索器创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_file_generation():
    """测试配置文件生成"""
    try:
        print("💾 测试配置文件生成...")
        from updates.vod.searcher import VODSourceSearcher
        
        searcher = VODSourceSearcher()
        
        # 创建测试源
        test_sources = [
            {
                "url": "https://example.com/test1.json",
                "name": "测试源1",
                "category": "测试分类",
                "description": "这是一个测试源",
                "source_type": "test"
            },
            {
                "url": "https://example.com/test2.json", 
                "name": "测试源2",
                "category": "测试分类",
                "description": "这是另一个测试源",
                "source_type": "test"
            }
        ]
        
        # 生成配置文件
        test_config_file = "test_config_validation.txt"
        searcher.save_sources_to_config(test_sources, test_config_file)
        
        # 检查文件是否生成
        if os.path.exists(test_config_file):
            with open(test_config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ 配置文件生成成功，内容长度: {len(content)} 字符")
                
                # 显示前几行
                lines = content.split('\n')
                print("📋 配置文件前5行:")
                for i, line in enumerate(lines[:5]):
                    print(f"   {i+1}: {line}")
            
            # 清理测试文件
            os.remove(test_config_file)
            print("🧹 测试文件已清理")
            return True
        else:
            print("❌ 配置文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ 配置文件生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🔍 开始VOD搜索功能验证...")
    print("=" * 50)
    
    tests = [
        ("模块导入测试", test_imports),
        ("搜索器创建测试", test_searcher_creation), 
        ("配置文件生成测试", test_config_file_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} 通过")
        else:
            print(f"❌ {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"🎯 测试结果: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！VOD搜索功能验证成功")
        return True
    else:
        print("⚠️ 部分测试失败，需要检查问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
