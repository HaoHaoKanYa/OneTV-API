#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OneTV-API VOD源整合器
整合本地解密的VOD源到工作流中
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class VODIntegrator:
    """VOD源整合器"""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.integrated_file = self.base_dir / "vod/output/onetv-api-movie-integrated.json"
        
    def load_integrated_config(self) -> Dict[str, Any]:
        """加载整合后的配置文件"""
        if not self.integrated_file.exists():
            logger.warning(f"整合配置文件不存在: {self.integrated_file}")
            return {}
            
        try:
            with open(self.integrated_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"成功加载整合配置，包含 {len(config.get('sites', []))} 个站点")
            return config
        except Exception as e:
            logger.error(f"加载整合配置失败: {e}")
            return {}
    
    def extract_sources_from_config(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """从配置文件中提取源信息"""
        sources = []
        
        for site in config.get('sites', []):
            if not isinstance(site, dict):
                continue
                
            source = {
                'url': site.get('api', ''),
                'name': site.get('name', '未知源'),
                'category': '本地整合',
                'note': f"来源: 本地解密 | API: {site.get('api', '')} | 类型: {site.get('type', 3)}",
                'quality_score': 85,  # 给本地源较高的默认评分
                'response_time': 0.5,  # 默认响应时间
                'searchable': site.get('searchable', 1),
                'filterable': site.get('filterable', 1),
                'ext': site.get('ext', {}),
                'playerType': site.get('playerType', 1),
                'timeout': site.get('timeout', 30)
            }
            
            # 只添加有效的API
            if source['url'] and source['url'] != '':
                sources.append(source)
        
        logger.info(f"从整合配置中提取 {len(sources)} 个源")
        return sources
    
    def get_integrated_sources(self) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """获取整合后的源和基础配置"""
        config = self.load_integrated_config()
        if not config:
            return [], {}
            
        sources = self.extract_sources_from_config(config)
        return sources, config
    
    def create_final_config(self, base_config: Dict[str, Any], valid_sources: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建最终的配置文件"""
        if not base_config:
            # 如果没有基础配置，创建默认配置
            return self._create_default_config(valid_sources or [])
        
        # 使用基础配置并更新必要字段
        final_config = base_config.copy()
        
        # 更新直播源链接
        final_config['lives'] = [
            {
                "name": "OneTV-API直播源",
                "type": 0,
                "url": "https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/onetv_api_result.m3u",
                "epg": "https://live.fanmingming.com/e.xml",
                "logo": "https://live.fanmingming.com/tv/{name}.png"
            }
        ]
        
        # 如果有额外的有效源，可以添加到sites中
        if valid_sources:
            existing_sites = final_config.get('sites', [])
            # 这里可以添加逻辑来合并新发现的源
            logger.info(f"基础配置包含 {len(existing_sites)} 个站点")
        
        return final_config
    
    def _create_default_config(self, valid_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建默认配置"""
        sites = []
        for i, source in enumerate(valid_sources[:50]):  # 限制50个源
            site = {
                "key": f"onetv_{i+1}",
                "name": source.get('name', f'影视源{i+1}'),
                "type": 3,
                "api": source.get('url', ''),
                "searchable": source.get('searchable', 1),
                "quickSearch": 1,
                "filterable": source.get('filterable', 1)
            }
            
            # 添加扩展配置
            if source.get('ext'):
                site['ext'] = source['ext']
            if source.get('playerType'):
                site['playerType'] = source['playerType']
            if source.get('timeout'):
                site['timeout'] = source['timeout']
                
            sites.append(site)
        
        return {
            "spider": "https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1751548979136/PandaQ250703b.jpg;md5;6ea33c17933c910130d2905dd23f248d",
            "wallpaper": "https://bing.img.run/uhd.php",
            "logo": "https://live.fanmingming.com/tv/{name}.png",
            "lives": [
                {
                    "name": "OneTV-API直播源",
                    "type": 0,
                    "url": "https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/onetv_api_result.m3u",
                    "epg": "https://live.fanmingming.com/e.xml",
                    "logo": "https://live.fanmingming.com/tv/{name}.png"
                }
            ],
            "sites": sites,
            "parses": [
                {
                    "name": "OneTV解析",
                    "type": 1,
                    "url": "https://jx.xmflv.com/?url="
                }
            ],
            "flags": ["youku", "qq", "iqiyi", "qiyi", "letv", "sohu", "pptv", "mgtv"],
            "ads": [
                "mimg.0c1q0l.cn",
                "www.googletagmanager.com",
                "www.google-analytics.com"
            ]
        }

def integrate_local_vod_sources():
    """整合本地VOD源的主函数"""
    integrator = VODIntegrator()
    return integrator.get_integrated_sources()

def create_integrated_config(base_config: Dict[str, Any], valid_sources: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """创建整合后的配置文件"""
    integrator = VODIntegrator()
    return integrator.create_final_config(base_config, valid_sources)
