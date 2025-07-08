# OneTV-API 影视仓库配置文件

## 文件说明

### 主要配置文件

1. **onetv-api-movie.json** - 完整版影视仓库配置
   - 包含229个影视源
   - 分为10个系列：豆瓣推荐、ONETV主线路、欧歌系列、肥猫系列、南风系列、俊佬系列、不良帅系列、巧儿系列、刘备系列、菜妮丝系列、香雅情系列
   - 适用于TVBOX等播放器

2. **onetv-api-movie-simple.json** - 简化版影视仓库配置
   - 包含精选影视源
   - 结构简化，加载更快
   - 适用于性能较低的设备

### 仓库索引文件

3. **onetv-api-storehouse.json** - 多仓库配置
   - 包含多个仓库源的索引
   - 用于TVBOX的多仓库模式

4. **onetv-api-single.json** - 单仓库配置
   - 包含多个配置文件的索引
   - 用于TVBOX的单仓库模式

## 使用方法

### TVBOX配置

#### 方法1：直接使用完整配置
```
https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-movie.json
```

#### 方法2：使用多仓库模式
```
https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-storehouse.json
```

#### 方法3：使用单仓库模式
```
https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-single.json
```

#### 方法4：使用简化版（推荐低配设备）
```
https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/refs/heads/main/vod/output/onetv-api-movie-simple.json
```

## 功能特点

- ✅ 支持TVBOX完整菜单结构（主页、热门电影、热播剧集、热播综艺、电影筛选、电视筛选、电影榜单、电视剧榜单）
- ✅ 正确识别为"OneTV-API影视仓库"
- ✅ 显示229个影视源，按系列分组
- ✅ 包含豆瓣推荐、欧歌、肥猫、南风、俊佬、不良帅、巧儿、刘备、菜妮丝、香雅情等系列
- ✅ 支持搜索、快速搜索、筛选功能
- ✅ 内置广告过滤规则
- ✅ 优化的播放器配置

## 更新说明

- 版本：2.0.0
- 更新时间：2025年1月8日
- 更新内容：修复TVBOX识别问题，优化配置结构，添加多种配置模式

## 注意事项

1. 本项目为免费开源项目，严禁商业用途
2. 所有影视资源来源于网络，仅供学习交流使用
3. 请支持正版影视内容
4. 如有侵权，请联系删除

## 技术支持

- GitHub: https://github.com/HaoHaoKanYa/OneTV-API
- 问题反馈: https://github.com/HaoHaoKanYa/OneTV-API/issues
