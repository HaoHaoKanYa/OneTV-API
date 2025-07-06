# 🌐 OneTV-API 接口文档

## 📋 接口概览

OneTV-API 提供了丰富的HTTP接口，支持多种格式的IPTV播放列表获取，包括标准格式、协议分离、推流服务等功能。

### 基础信息
- **基础URL**: `http://localhost:8000`
- **协议**: HTTP/HTTPS
- **格式**: M3U, TXT
- **编码**: UTF-8
- **协议支持**: IPv4, IPv6

## 🎯 核心接口

### 1. 默认播放列表

#### GET `/`
获取默认格式的播放列表

**请求示例:**
```bash
curl http://localhost:8000/
```

**响应格式:**
- 如果开启RTMP推流: 返回推流版本播放列表
- 如果开启M3U格式: 返回M3U格式
- 否则: 返回TXT格式

**响应示例:**
```
#EXTM3U x-tvg-url="https://example.com/epg.gz"
#EXTINF:-1 tvg-name="CCTV1" tvg-logo="https://example.com/logo.png" group-title="📺央视频道",CCTV-1
http://example.com/cctv1.m3u8
#EXTINF:-1 tvg-name="CCTV2" tvg-logo="https://example.com/logo.png" group-title="📺央视频道",CCTV-2
http://example.com/cctv2.m3u8
```

### 2. M3U格式接口

#### GET `/m3u`
获取M3U格式播放列表

**特点:**
- 包含EPG信息
- 支持频道图标
- 支持分组显示
- 兼容大多数播放器

**请求示例:**
```bash
curl http://localhost:8000/m3u
```

### 3. TXT格式接口

#### GET `/txt`
获取TXT格式播放列表

**特点:**
- 纯文本格式
- 兼容性最好
- 文件体积小
- 易于解析

**请求示例:**
```bash
curl http://localhost:8000/txt
```

**响应示例:**
```
📺央视频道,#genre#
CCTV-1,http://example.com/cctv1.m3u8
CCTV-2,http://example.com/cctv2.m3u8
📡卫视频道,#genre#
湖南卫视,http://example.com/hunan.m3u8
浙江卫视,http://example.com/zhejiang.m3u8
```

## 🌐 协议分离接口

### IPv4专用接口

#### GET `/ipv4`
获取IPv4协议的默认格式播放列表

#### GET `/ipv4/txt`
获取IPv4协议的TXT格式播放列表

#### GET `/ipv4/m3u`
获取IPv4协议的M3U格式播放列表

**请求示例:**
```bash
curl http://localhost:8000/ipv4/m3u
```

### IPv6专用接口

#### GET `/ipv6`
获取IPv6协议的默认格式播放列表

#### GET `/ipv6/txt`
获取IPv6协议的TXT格式播放列表

#### GET `/ipv6/m3u`
获取IPv6协议的M3U格式播放列表

**请求示例:**
```bash
curl http://localhost:8000/ipv6/m3u
```

## 📺 RTMP推流接口

### Live推流接口

#### GET `/live`
获取Live推流的默认格式播放列表

#### GET `/live/txt`
获取Live推流的TXT格式播放列表

#### GET `/live/m3u`
获取Live推流的M3U格式播放列表

#### GET `/live/ipv4/txt`
获取Live推流的IPv4 TXT格式播放列表

#### GET `/live/ipv4/m3u`
获取Live推流的IPv4 M3U格式播放列表

#### GET `/live/ipv6/txt`
获取Live推流的IPv6 TXT格式播放列表

#### GET `/live/ipv6/m3u`
获取Live推流的IPv6 M3U格式播放列表

**推流地址格式:**
```
rtmp://localhost:1935/live/频道名称
```

### HLS推流接口

#### GET `/hls`
获取HLS推流的默认格式播放列表

#### GET `/hls/txt`
获取HLS推流的TXT格式播放列表

#### GET `/hls/m3u`
获取HLS推流的M3U格式播放列表

#### GET `/hls/ipv4/txt`
获取HLS推流的IPv4 TXT格式播放列表

#### GET `/hls/ipv4/m3u`
获取HLS推流的IPv4 M3U格式播放列表

#### GET `/hls/ipv6/txt`
获取HLS推流的IPv6 TXT格式播放列表

#### GET `/hls/ipv6/m3u`
获取HLS推流的IPv6 M3U格式播放列表

**HLS地址格式:**
```
http://localhost:8080/hls/频道名称.m3u8
```

## 📊 管理接口

### 1. 内容查看接口

#### GET `/content`
获取播放列表的纯文本内容

**请求示例:**
```bash
curl http://localhost:8000/content
```

### 2. 日志查看接口

#### GET `/log`
获取测速和更新日志

**请求示例:**
```bash
curl http://localhost:8000/log
```

**响应示例:**
```
=== OneTV-API 更新日志 ===
更新时间: 2024-01-01 12:00:00
总频道数: 1500
测速完成: 1200
有效频道: 800
平均响应时间: 1.2s
平均速率: 2.5M/s

=== 频道统计 ===
📺央视频道: 20个
📡卫视频道: 35个
🏀体育频道: 15个
...
```

### 3. 静态资源接口

#### GET `/favicon.ico`
获取网站图标

## 🔧 推流管理接口

### 推流状态监控

#### GET `http://localhost:8080/stat`
查看RTMP推流状态统计（需要开启RTMP功能）

**响应格式:** XML
```xml
<?xml version="1.0" encoding="utf-8" ?>
<rtmp>
    <server>
        <application>
            <name>live</name>
            <live>
                <stream>
                    <name>CCTV1</name>
                    <time>12345</time>
                    <bw_in>1024000</bw_in>
                    <bw_out>2048000</bw_out>
                    <bytes_in>1048576</bytes_in>
                    <bytes_out>2097152</bytes_out>
                </stream>
            </live>
        </application>
    </server>
</rtmp>
```

## 📝 响应格式说明

### M3U格式详解
```
#EXTM3U x-tvg-url="EPG地址"
#EXTINF:-1 tvg-name="频道名" tvg-logo="图标地址" group-title="分组名",显示名称
播放地址
```

**字段说明:**
- `x-tvg-url`: EPG电子节目指南地址
- `tvg-name`: 频道标识名称
- `tvg-logo`: 频道图标URL
- `group-title`: 频道分组名称
- `显示名称`: 播放器中显示的名称

### TXT格式详解
```
分组名称,#genre#
频道名称,播放地址
频道名称,播放地址
```

**字段说明:**
- `#genre#`: 分组标识符
- `频道名称`: 频道显示名称
- `播放地址`: 直播流URL

## 🔍 接口参数

### 通用参数
目前接口不支持额外参数，所有配置通过配置文件控制。

### 缓存机制
- 接口响应会根据更新频率自动缓存
- 缓存时间与配置的更新间隔一致
- 强制刷新需要重新运行更新程序

## 📱 客户端集成示例

### JavaScript
```javascript
// 获取M3U播放列表
fetch('http://localhost:8000/m3u')
  .then(response => response.text())
  .then(data => {
    console.log('播放列表:', data);
    // 解析M3U内容
    parseM3U(data);
  });

function parseM3U(content) {
  const lines = content.split('\n');
  const channels = [];
  
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('#EXTINF:')) {
      const info = lines[i];
      const url = lines[i + 1];
      
      // 提取频道信息
      const name = info.split(',').pop();
      const logo = info.match(/tvg-logo="([^"]+)"/)?.[1];
      const group = info.match(/group-title="([^"]+)"/)?.[1];
      
      channels.push({ name, url, logo, group });
      i++; // 跳过URL行
    }
  }
  
  return channels;
}
```

### Python
```python
import requests
import re

def get_channels():
    """获取频道列表"""
    response = requests.get('http://localhost:8000/m3u')
    content = response.text
    
    channels = []
    lines = content.split('\n')
    
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF:'):
            info = lines[i]
            url = lines[i + 1] if i + 1 < len(lines) else ''
            
            # 提取信息
            name = info.split(',')[-1]
            logo_match = re.search(r'tvg-logo="([^"]+)"', info)
            group_match = re.search(r'group-title="([^"]+)"', info)
            
            channel = {
                'name': name,
                'url': url,
                'logo': logo_match.group(1) if logo_match else '',
                'group': group_match.group(1) if group_match else ''
            }
            channels.append(channel)
    
    return channels

# 使用示例
channels = get_channels()
for channel in channels:
    print(f"{channel['name']}: {channel['url']}")
```

### Shell/Bash
```bash
#!/bin/bash

# 获取播放列表
get_playlist() {
    local format=${1:-"m3u"}
    curl -s "http://localhost:8000/${format}"
}

# 获取频道数量
get_channel_count() {
    get_playlist "txt" | grep -c "http"
}

# 测试接口可用性
test_api() {
    local status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
    if [ "$status" = "200" ]; then
        echo "API服务正常"
        echo "频道数量: $(get_channel_count)"
    else
        echo "API服务异常: $status"
    fi
}

# 运行测试
test_api
```

## ⚠️ 注意事项

### 1. 接口限制
- 无并发限制，但建议合理使用
- 大文件传输可能需要较长时间
- 建议使用缓存机制减少请求频率

### 2. 错误处理
- HTTP 404: 接口不存在
- HTTP 500: 服务器内部错误
- 空响应: 可能是更新中或配置错误

### 3. 最佳实践
- 定期检查接口可用性
- 实现客户端缓存机制
- 处理网络异常情况
- 解析播放列表时注意格式兼容性

---

> **提示**: 更多接口使用示例和集成方案，请参考项目的示例代码或联系开发者。
