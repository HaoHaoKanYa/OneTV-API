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
        """生成点播源JSON文件"""
        valid_sources = vod_data.get("valid_sources", [])
        
        if not valid_sources:
            print("❌ 没有有效的点播源数据!")
            return ""
        
        # 构建TVBox格式的JSON配置
        tvbox_config = {
            "spider": "https://gh-proxy.com/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/jar/custom_spider.jar;md5;a8b2e5b2b1b1b1b1b1b1b1b1b1b1b1b1",
            "wallpaper": "http://www.kf666888.cn/api/tvbox/img",
            "lives": [
                {
                    "name": "OneTV-API直播源",
                    "type": 0,
                    "url": "https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/onetv_api_result.m3u",
                    "epg": "https://live.fanmingming.com/e.xml",
                    "logo": "https://live.fanmingming.com/tv/{name}.png"
                }
            ],
            "sites": [],
            "parses": [
                {
                    "name": "Json并发",
                    "type": 2,
                    "url": "Parallel"
                },
                {
                    "name": "Json轮询",
                    "type": 2,
                    "url": "Sequence"
                }
            ],
            "flags": [
                "youku", "qq", "iqiyi", "qiyi", "letv", "sohu", "tudou", "pptv", "mgtv", "wasu"
            ],
            "ijk": [
                {
                    "group": "软解码",
                    "options": [
                        {"category": 4, "name": "opensles", "value": "0"},
                        {"category": 4, "name": "overlay-format", "value": "842225234"},
                        {"category": 4, "name": "framedrop", "value": "1"},
                        {"category": 4, "name": "soundtouch", "value": "1"},
                        {"category": 4, "name": "start-on-prepared", "value": "1"},
                        {"category": 1, "name": "http-detect-range-support", "value": "0"},
                        {"category": 1, "name": "fflags", "value": "fastseek"},
                        {"category": 2, "name": "skip_loop_filter", "value": "48"},
                        {"category": 4, "name": "reconnect", "value": "1"},
                        {"category": 4, "name": "enable-accurate-seek", "value": "0"},
                        {"category": 4, "name": "mediacodec", "value": "0"},
                        {"category": 4, "name": "mediacodec-auto-rotate", "value": "0"},
                        {"category": 4, "name": "mediacodec-handle-resolution-change", "value": "0"},
                        {"category": 4, "name": "mediacodec-hevc", "value": "0"},
                        {"category": 1, "name": "dns_cache_timeout", "value": "600000000"}
                    ]
                }
            ],
            "ads": [
                "mimg.0c1q0l.cn",
                "www.googletagmanager.com",
                "www.google-analytics.com",
                "mc.usihnbcq.cn",
                "mg.g1mm3d.cn",
                "mscs.svaeuzh.cn",
                "cnzz.hhurm.cn",
                "tp.vinuxhome.com",
                "cnzz.mmstat.com",
                "www.baihuillq.com",
                "s23.cnzz.com",
                "z3.cnzz.com",
                "c.cnzz.com",
                "stj.v1vo.top",
                "z12.cnzz.com",
                "img.mosflower.cn",
                "tips.gamevvip.com",
                "ehwe.yhdtns.com",
                "xdn.cqqc3.com",
                "www.jixunkyy.cn",
                "sp.chemacid.cn",
                "hm.baidu.com",
                "s9.cnzz.com",
                "z6.cnzz.com",
                "um.cavuc.com",
                "mav.mavuz.com",
                "wofwk.aoidf3.com",
                "z5.cnzz.com",
                "xc.hubeijieshikj.cn",
                "tj.tianwenhu.com",
                "xg.gars57.cn",
                "k.jinxiuzhilv.com",
                "cdn.bootcss.com",
                "ppl.xunzhuo123.com",
                "xomk.jiangjunmh.top",
                "img.xunzhuo123.com",
                "z1.cnzz.com",
                "s13.cnzz.com",
                "xg.huataisangao.cn",
                "z7.cnzz.com",
                "xg.huataisangao.cn",
                "z2.cnzz.com",
                "s96.cnzz.com",
                "q11.cnzz.com",
                "thy.dacedsfa.cn",
                "xg.whsbpw.cn",
                "s19.cnzz.com",
                "z8.cnzz.com",
                "s4.cnzz.com",
                "f5w.as12df.top",
                "ae01.alicdn.com",
                "www.92424.cn",
                "k.wudejia.com",
                "vivovip.mmszxc.top",
                "qiu.xixiqiu.com",
                "cdnjs.hnfenxun.com",
                "cms.qdwght.com"
            ]
        }
        
        # 按分类组织点播源
        categories = {}
        for source in valid_sources:
            category = source.get("category", "未分类")
            if category not in categories:
                categories[category] = []
            categories[category].append(source)
        
        # 为每个分类创建站点配置
        site_id = 1
        for category, sources in categories.items():
            for source in sources:
                site_config = {
                    "key": f"vod_{site_id}",
                    "name": source["name"],
                    "type": 3,
                    "api": source["url"],
                    "searchable": 1,
                    "quickSearch": 1,
                    "filterable": 1,
                    "ext": source["url"]
                }
                tvbox_config["sites"].append(site_config)
                site_id += 1
        
        # 生成文件
        output_file = os.path.join(self.output_dir, "onetv-api-movie.json")
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(tvbox_config, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 点播源JSON文件生成成功: {output_file}")
            print(f"📊 包含 {len(valid_sources)} 个优质点播源")
            print(f"📂 分类统计: {dict((k, len(v)) for k, v in categories.items())}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ 生成点播源JSON文件失败: {str(e)}")
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
