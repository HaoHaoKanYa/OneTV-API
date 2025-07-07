"""
OneTV-API 点播源更新模块
VOD (Video On Demand) Source Update Module
"""
import asyncio
import os
import configparser
from time import time
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional

import aiohttp
from tqdm.asyncio import tqdm as tqdm_asyncio

from utils.tools import get_pbar_remaining, resource_path


class VODSourceManager:
    """点播源管理器"""
    
    def __init__(self):
        self.config = self.load_vod_config()
        self.sources = []
        self.valid_sources = []
        self.quality_scores = {}
        
    def load_vod_config(self) -> configparser.ConfigParser:
        """加载点播源配置"""
        config = configparser.ConfigParser()
        config_path = resource_path("vod/config/vod_config.ini")
        
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        else:
            # 默认配置
            config.add_section('VOD_Settings')
            config.set('VOD_Settings', 'request_timeout', '15')
            config.set('VOD_Settings', 'max_concurrent', '10')
            config.set('VOD_Settings', 'min_quality_score', '70')
            
        return config
    
    def load_vod_sources(self) -> List[Dict]:
        """加载点播源列表"""
        sources_file = resource_path("vod/config/vod_sources.txt")
        sources = []
        
        if not os.path.exists(sources_file):
            print("❌ 点播源配置文件不存在!")
            return sources
        
        try:
            with open(sources_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # 跳过注释和空行
                    if not line or line.startswith('#'):
                        continue
                    
                    # 解析格式: URL|名称|分类|备注
                    parts = line.split('|')
                    if len(parts) >= 2:
                        source = {
                            "url": parts[0].strip(),
                            "name": parts[1].strip(),
                            "category": parts[2].strip() if len(parts) > 2 else "未分类",
                            "description": parts[3].strip() if len(parts) > 3 else "",
                            "line_number": line_num
                        }
                        sources.append(source)
                        
        except Exception as e:
            print(f"❌ 读取点播源配置失败: {str(e)}")
            
        return sources
    
    async def validate_vod_source(self, session: aiohttp.ClientSession, source: Dict) -> Optional[Dict]:
        """验证单个点播源"""
        try:
            url = source["url"]
            name = source["name"]
            
            # 设置超时时间
            timeout = aiohttp.ClientTimeout(
                total=int(self.config.get('VOD_Settings', 'request_timeout', fallback='15'))
            )
            
            start_time = time()
            
            async with session.get(url, timeout=timeout) as response:
                response_time = time() - start_time
                
                if response.status == 200:
                    content = await response.text()
                    
                    # 内容验证
                    quality_score = self.calculate_quality_score(
                        content, response_time, response.status
                    )
                    
                    if quality_score >= int(self.config.get('VOD_Settings', 'min_quality_score', fallback='70')):
                        return {
                            "url": url,
                            "name": name,
                            "category": source.get("category", "未分类"),
                            "description": source.get("description", ""),
                            "status": "valid",
                            "response_time": round(response_time, 2),
                            "quality_score": quality_score,
                            "content_size": len(content),
                            "validated_at": datetime.now().isoformat()
                        }
                    else:
                        print(f"⚠️  {name}: 质量评分不足 ({quality_score}/100)")
                        return None
                else:
                    print(f"❌ {name}: HTTP {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            print(f"⏰ {source['name']}: 请求超时")
            return None
        except Exception as e:
            print(f"❌ {source['name']}: {str(e)}")
            return None
    
    def calculate_quality_score(self, content: str, response_time: float, status_code: int) -> int:
        """计算质量评分"""
        score = 0
        
        # 连通性评分 (40分)
        if status_code == 200:
            score += 40
        elif status_code in [301, 302]:
            score += 35
        
        # 响应时间评分 (20分)
        if response_time < 3:
            score += 20
        elif response_time < 5:
            score += 15
        elif response_time < 10:
            score += 10
        
        # 内容质量评分 (25分)
        content_lower = content.lower()
        if any(field in content_lower for field in ['sites', 'spider', 'lives']):
            score += 15
        if content.strip().startswith('{') and content.strip().endswith('}'):
            score += 10
        
        # 内容大小评分 (15分)
        if len(content) > 10000:
            score += 15
        elif len(content) > 5000:
            score += 10
        elif len(content) > 1000:
            score += 5
        
        return min(score, 100)
    
    async def get_vod_sources(self, callback=None) -> Dict:
        """获取和验证点播源"""
        self.sources = self.load_vod_sources()
        sources_len = len(self.sources)
        
        if sources_len == 0:
            print("❌ 没有找到点播源配置!")
            return {"valid_sources": [], "total_sources": 0}
        
        print(f"🎬 开始验证 {sources_len} 个点播源...")
        
        pbar = tqdm_asyncio(
            total=sources_len,
            desc="Processing VOD sources",
        )
        start_time = time()
        
        if callback:
            callback(f"正在验证点播源, 共{sources_len}个点播源", 0)
        
        valid_sources = []
        max_concurrent = int(self.config.get('VOD_Settings', 'max_concurrent', fallback='10'))
        
        # 创建信号量限制并发数
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def validate_with_semaphore(session, source):
            async with semaphore:
                return await self.validate_vod_source(session, source)
        
        # 并发验证所有点播源
        async with aiohttp.ClientSession() as session:
            tasks = [validate_with_semaphore(session, source) for source in self.sources]
            
            for task in asyncio.as_completed(tasks):
                result = await task
                pbar.update(1)
                
                if result:
                    valid_sources.append(result)
                    print(f"✅ {result['name']}: 验证通过 (评分: {result['quality_score']}/100)")
                
                # 更新进度
                remain = sources_len - pbar.n
                if callback:
                    callback(
                        f"正在验证点播源, 剩余{remain}个点播源待验证, 预计剩余时间: {get_pbar_remaining(n=pbar.n, total=pbar.total, start_time=start_time)}",
                        int((pbar.n / sources_len) * 100),
                    )
        
        pbar.close()
        
        # 按质量评分排序
        valid_sources.sort(key=lambda x: x['quality_score'], reverse=True)
        
        valid_count = len(valid_sources)
        print(f"🎯 点播源验证完成: {valid_count}/{sources_len} 个源可用")
        
        return {
            "valid_sources": valid_sources,
            "total_sources": sources_len,
            "validation_time": time() - start_time,
            "average_score": sum(s['quality_score'] for s in valid_sources) / valid_count if valid_count > 0 else 0
        }


async def get_vod_sources(callback=None):
    """获取点播源的主函数"""
    manager = VODSourceManager()
    return await manager.get_vod_sources(callback)


def get_vod_sources_info():
    """获取点播源信息统计"""
    manager = VODSourceManager()
    sources = manager.load_vod_sources()

    categories = defaultdict(int)
    for source in sources:
        categories[source.get('category', '未分类')] += 1

    return {
        "total": len(sources),
        "categories": dict(categories),
        "sources": [{"name": s["name"], "url": s["url"], "category": s.get("category", "未分类")} for s in sources]
    }


async def update_vod_sources(callback=None):
    """更新点播源的完整流程 - 包含全网搜索"""
    from .processor import process_vod_sources
    from .uploader import upload_vod_to_supabase
    from .searcher import search_and_update_vod_sources

    print("🎬 开始OneTV-API点播源更新流程...")

    try:
        # 0. 全网搜索并更新配置文件
        print("🔍 第0步: 全网搜索VOD源...")
        config_file = "vod/config/vod_sources.txt"
        search_count = await search_and_update_vod_sources(config_file)
        print(f"🎯 全网搜索完成，发现并更新了 {search_count} 个VOD源到配置文件")

        # 1. 获取和验证点播源 (现在基于更新后的配置文件)
        print("📡 第1步: 验证所有发现的点播源...")
        vod_data = await get_vod_sources(callback)

        if not vod_data.get("valid_sources"):
            print("❌ 没有获取到有效的点播源!")
            return False

        # 2. 处理点播源数据
        print("🔄 第2步: 处理点播源数据...")
        process_result = process_vod_sources(vod_data)

        if not process_result.get("json_file"):
            print("❌ 点播源JSON文件生成失败!")
            return False

        # 3. 上传到Supabase
        print("☁️  第3步: 上传到Supabase...")
        upload_result = upload_vod_to_supabase(process_result["json_file"])

        if upload_result["success"]:
            print("✅ 点播源更新流程完成!")
            print(f"🌐 公共访问地址: {upload_result['public_url']}")

            # 显示统计信息
            stats = process_result.get("statistics", {}).get("summary", {})
            print(f"📊 更新统计:")
            print(f"   - 搜索发现源数量: {search_count}")
            print(f"   - 配置源数量: {stats.get('total_configured', 0)}")
            print(f"   - 有效源数量: {stats.get('valid_sources', 0)}")
            print(f"   - 成功率: {stats.get('success_rate', '0%')}")
            print(f"   - 平均质量评分: {stats.get('average_quality_score', '0')}")
            print(f"   - 平均响应时间: {stats.get('average_response_time', '0s')}")

            return True
        else:
            print(f"❌ 上传失败: {upload_result['message']}")
            return False

    except Exception as e:
        print(f"❌ 点播源更新流程失败: {str(e)}")
        return False
