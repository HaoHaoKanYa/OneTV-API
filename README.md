<div align="center">
  <img src="./static/images/logo.png" alt="OneTV-API Logo"/>
  <h1 align="center">OneTV-API</h1>
</div>

<div align="center">
  <h3>🚀 智能IPTV直播源管理系统</h3>
  <p>基于Python开发的高效IPTV接口更新工具，专注于提供稳定、快速的直播源服务</p>
</div>

<br>

<p align="center">
  <a href="https://github.com/HaoHaoKanYa/OneTV-API/releases/latest">
    <img src="https://img.shields.io/github/v/release/HaoHaoKanYa/OneTV-API?style=flat-square&logo=github" alt="Latest Release"/>
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python" alt="Python Version"/>
  </a>
  <a href="https://github.com/HaoHaoKanYa/OneTV-API/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/HaoHaoKanYa/OneTV-API?style=flat-square" alt="License"/>
  </a>
  <a href="https://github.com/HaoHaoKanYa/OneTV-API/stargazers">
    <img src="https://img.shields.io/github/stars/HaoHaoKanYa/OneTV-API?style=flat-square&logo=github" alt="GitHub Stars"/>
  </a>
  <a href="https://github.com/HaoHaoKanYa/OneTV-API/network/members">
    <img src="https://img.shields.io/github/forks/HaoHaoKanYa/OneTV-API?style=flat-square&logo=github" alt="GitHub Forks"/>
  </a>
</p>

<p align="center">
  <a href="./README_en.md">English</a> |
  <a href="#快速开始">快速开始</a> |
  <a href="#功能特色">功能特色</a> |
  <a href="#使用文档">使用文档</a>
</p>

---

## 📖 项目简介

OneTV-API 是一个专业的IPTV直播源管理系统，旨在为用户提供高质量、稳定的电视直播服务。本项目采用现代化的技术架构，支持多种部署方式，能够自动获取、测试和优化直播源，确保最佳的观看体验。

### 🎯 设计理念

- **稳定性优先**：通过多重测试机制确保直播源的可用性和稳定性
- **用户体验**：简洁的配置方式，支持个性化定制
- **自动化运维**：GitHub Actions自动化更新，无需人工干预
- **开源透明**：完全开源，社区驱动的持续改进

## 📋 目录

- [🚀 快速开始](#快速开始)
- [✨ 功能特色](#功能特色)
- [📺 直播源获取](#直播源获取)
- [⚙️ 配置说明](#配置说明)
- [🛠️ 部署方式](#部署方式)
  - [GitHub Actions（推荐）](#github-actions推荐)
  - [本地运行](#本地运行)
  - [Docker部署](#docker部署)
- [📖 使用文档](#使用文档)
- [🤝 贡献指南](#贡献指南)
- [📄 许可证](#许可证)

## 🚀 快速开始

### 方式一：GitHub Actions（推荐）

1. **Fork 本项目**到您的 GitHub 账户
2. **启用 Actions**：进入仓库设置 → Actions → 允许所有操作
3. **自动运行**：每天北京时间 6:00 和 18:00 自动更新
4. **获取结果**：
   ```
   https://raw.githubusercontent.com/您的用户名/OneTV-API/main/output/onetv_api_result.m3u
   ```

### 方式二：一键部署

[![Deploy to GitHub](https://img.shields.io/badge/Deploy%20to-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/HaoHaoKanYa/OneTV-API/fork)

> [!TIP]
> 推荐使用 GitHub Actions 方式，无需本地环境配置，自动化程度高

## ✨ 功能特色

### 🎯 核心功能

| 功能模块               | 描述                                 | 状态 |
| ---------------------- | ------------------------------------ | ---- |
| 🔄**自动更新**   | GitHub Actions 定时自动更新直播源    | ✅   |
| 🚀**智能测速**   | 多线程并发测试，筛选最优直播源       | ✅   |
| 📺**多源聚合**   | 支持本地源、订阅源、组播源等多种来源 | ✅   |
| 🎨**个性定制**   | 自定义频道模板，支持频道别名         | ✅   |
| 📊**质量保证**   | 分辨率检测、速度过滤、稳定性验证     | ✅   |
| 🌐**多协议支持** | IPv4/IPv6 双栈支持，RTMP推流         | ✅   |

### 🛡️ 技术优势

- **高性能**：异步并发处理，支持大规模直播源测试
- **高可用**：多重容错机制，确保服务稳定运行
- **易部署**：支持 GitHub Actions、Docker、本地运行等多种部署方式
- **易维护**：模块化设计，配置文件化管理
- **跨平台**：支持 Windows、Linux、macOS 等操作系统

## 📺 直播源获取

### 🔗 在线播放列表

> [!NOTE]
> 以下链接为自动更新的直播源，每天北京时间 6:00 和 18:00 自动更新

#### 主要播放列表

| 类型               | 链接                                                                                         | 说明               |
| ------------------ | -------------------------------------------------------------------------------------------- | ------------------ |
| **推荐使用** | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/onetv_api_result.m3u` | 精选频道，质量优先 |
| 完整列表           | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/result.m3u`           | 包含所有可用频道   |

#### 分类播放列表

| 协议类型  | 链接                                                                                    | 适用场景      |
| --------- | --------------------------------------------------------------------------------------- | ------------- |
| IPv4 专用 | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/ipv4/result.m3u` | IPv4 网络环境 |
| IPv6 专用 | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/ipv6/result.m3u` | IPv6 网络环境 |

### 📱 使用方法

1. **复制播放列表链接**
2. **在IPTV播放器中添加**（如 VLC、Kodi、Perfect Player 等）
3. **开始观看**

### 🌍 CDN 加速

如果 GitHub 访问较慢，可以使用以下 CDN 加速地址：

```
https://cdn.jsdelivr.net/gh/HaoHaoKanYa/OneTV-API@main/output/onetv_api_result.m3u
```

## ⚙️ 配置说明

### 📝 配置文件

项目支持通过配置文件进行个性化定制，主要配置文件位于 `config/` 目录：

- `onetv_api_config.ini` - 主配置文件
- `onetv_api_demo.txt` - 频道模板文件
- `local.txt` - 本地直播源
- `whitelist.txt` - 白名单频道
- `subscribe.txt` - 订阅源列表

### 🔧 核心配置项

<details>
<summary>点击展开详细配置说明</summary>

#### 基础设置

| 配置项                 | 说明              | 默认值   | 推荐值   |
| ---------------------- | ----------------- | -------- | -------- |
| `open_speed_test`    | 启用测速功能      | `True` | `True` |
| `open_filter_speed`  | 启用速度过滤      | `True` | `True` |
| `min_speed`          | 最小速度要求(M/s) | `0.5`  | `1.0`  |
| `speed_test_timeout` | 测速超时时间(秒)  | `10`   | `15`   |

#### 网络设置

| 配置项       | 说明         | 默认值   | 推荐值   |
| ------------ | ------------ | -------- | -------- |
| `ipv_type` | IP协议类型   | `全部` | `全部` |
| `ipv4_num` | IPv4接口数量 | `5`    | `3`    |
| `ipv6_num` | IPv6接口数量 | `5`    | `3`    |

#### 源设置

| 配置项             | 说明           | 默认值    | 推荐值   |
| ------------------ | -------------- | --------- | -------- |
| `open_local`     | 启用本地源     | `True`  | `True` |
| `open_subscribe` | 启用订阅源     | `False` | `True` |
| `local_num`      | 本地源接口数量 | `10`    | `5`    |
| `subscribe_num`  | 订阅源接口数量 | `10`    | `5`    |

</details>

### 📋 频道模板配置

支持自定义频道模板，格式如下：

```
频道分组,#genre#
频道名称,频道链接
频道名称,频道链接

另一个分组,#genre#
频道名称,频道链接
```

### 🎯 个性化定制

1. **修改频道模板**：编辑 `config/onetv_api_demo.txt`
2. **添加本地源**：编辑 `config/local.txt`
3. **设置白名单**：编辑 `config/whitelist.txt`
4. **调整配置**：编辑 `config/onetv_api_config.ini`

## 🛠️ 部署方式

### GitHub Actions（推荐）

> [!TIP]
> 这是最简单、最稳定的部署方式，无需本地环境配置

#### 🚀 快速部署

1. **Fork 项目**

   ```bash
   # 点击页面右上角的 Fork 按钮
   # 或访问：https://github.com/HaoHaoKanYa/OneTV-API/fork
   ```
2. **启用 Actions**

   - 进入您的仓库
   - 点击 `Actions` 选项卡
   - 点击 `I understand my workflows, go ahead and enable them`
3. **配置权限**

   - 进入 `Settings` → `Actions` → `General`
   - 在 `Workflow permissions` 中选择 `Read and write permissions`
   - 保存设置
4. **手动触发首次运行**

   - 进入 `Actions` 选项卡
   - 选择 `Update OneTV-API` 工作流
   - 点击 `Run workflow` → `Run workflow`
5. **获取结果**

   ```
   https://raw.githubusercontent.com/您的用户名/OneTV-API/main/output/onetv_api_result.m3u
   ```

#### ⏰ 自动更新

- **定时运行**：每天北京时间 6:00 和 18:00
- **手动触发**：随时可在 Actions 页面手动运行
- **配置更新**：修改配置文件后自动运行

### 本地运行

#### 环境要求

- Python 3.11+
- Git

#### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/HaoHaoKanYa/OneTV-API.git
cd OneTV-API

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python main.py
```

#### 高级用法

```bash
# 使用 pipenv（推荐）
pip install pipenv
pipenv install --dev

# 启动更新
pipenv run dev

# 启动服务
pipenv run service

# GUI 界面
pipenv run ui
```

### Docker部署

#### 🐳 快速启动

```bash
# 拉取镜像
docker pull haohaokanya/onetv-api:latest

# 运行容器
docker run -d -p 8000:8000 --name onetv-api haohaokanya/onetv-api
```

#### 🔧 完整配置

```bash
# 创建配置目录
mkdir -p ~/onetv-api/{config,output}

# 运行容器（推荐）
docker run -d \
  --name onetv-api \
  -p 8000:8000 \
  -v ~/onetv-api/config:/onetv-api/config \
  -v ~/onetv-api/output:/onetv-api/output \
  -e APP_HOST="http://localhost" \
  -e APP_PORT=8000 \
  haohaokanya/onetv-api:latest
```

#### 🌐 访问服务

| 端点     | 描述            | 示例                          |
| -------- | --------------- | ----------------------------- |
| `/`    | 主页面          | `http://localhost:8000`     |
| `/m3u` | M3U格式播放列表 | `http://localhost:8000/m3u` |
| `/txt` | TXT格式播放列表 | `http://localhost:8000/txt` |
| `/log` | 运行日志        | `http://localhost:8000/log` |

#### 🚀 国内加速

```bash
# 使用镜像加速
docker pull docker.1ms.run/haohaokanya/onetv-api:latest
```

## 📖 使用文档

### 🎬 支持的播放器

| 播放器                     | 平台        | 推荐度     | 说明                 |
| -------------------------- | ----------- | ---------- | -------------------- |
| **VLC Media Player** | 全平台      | ⭐⭐⭐⭐⭐ | 免费开源，兼容性最佳 |
| **Kodi**             | 全平台      | ⭐⭐⭐⭐⭐ | 功能强大的媒体中心   |
| **Perfect Player**   | Android/iOS | ⭐⭐⭐⭐   | 专业IPTV播放器       |
| **IPTV Pro**         | Android/iOS | ⭐⭐⭐⭐   | 界面美观，功能丰富   |
| **PotPlayer**        | Windows     | ⭐⭐⭐     | 轻量级播放器         |

### 📱 移动端使用

1. **下载IPTV播放器**（推荐 Perfect Player 或 IPTV Pro）
2. **添加播放列表**：
   ```
   https://raw.githubusercontent.com/您的用户名/OneTV-API/main/output/onetv_api_result.m3u
   ```
3. **开始观看**

### 💻 电脑端使用

1. **下载 VLC 播放器**
2. **打开网络串流**：`媒体` → `打开网络串流`
3. **输入播放列表地址**
4. **选择频道观看**

### 📺 电视盒子使用

1. **安装 Kodi 或其他IPTV应用**
2. **添加 PVR 插件**
3. **配置播放列表地址**
4. **享受大屏观看体验**

## 🤝 贡献指南

### 🐛 问题反馈

如果您遇到问题或有改进建议，请：

1. **查看现有 Issues**：避免重复提交
2. **创建新 Issue**：详细描述问题或建议
3. **提供信息**：包括系统环境、错误日志等

### 🔧 参与开发

欢迎提交 Pull Request：

1. **Fork 项目**
2. **创建特性分支**：`git checkout -b feature/amazing-feature`
3. **提交更改**：`git commit -m 'Add some amazing feature'`
4. **推送分支**：`git push origin feature/amazing-feature`
5. **创建 Pull Request**

### 📋 开发规范

- 遵循 PEP 8 代码规范
- 添加必要的注释和文档
- 确保代码测试通过
- 保持提交信息清晰


## 🙏 致谢

### 原项目开发者

本项目基于开源项目进行学习和改进，特别感谢：

- **原项目开发者**: Govin
- **项目地址**: [iptv-api](https://github.com/Guovin/iptv-api)
- **微信公众号**: 搜索 "Govin" 获取更多技术分享

### 开源项目

感谢以下开源项目的支持：

- [iptv-org/iptv](https://github.com/iptv-org/iptv) - 全球IPTV频道收集
- [fanmingming/live](https://github.com/fanmingming/live) - 频道图标资源
- 其他贡献者和开源社区

## ⚠️ 免责声明

1. **学习用途**：本项目仅供学习交流使用，请勿用于商业用途
2. **内容来源**：所有直播源均来自互联网公开资源，本项目不存储任何视频内容
3. **版权声明**：如有内容侵犯您的权益，请联系删除
4. **使用风险**：使用本项目产生的任何问题由使用者自行承担

## 📄 许可证

本项目采用 [MIT License](./LICENSE) 开源协议

```
MIT License

Copyright (c) 2024 HaoHaoKanYa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/HaoHaoKanYa">HaoHaoKanYa</a></p>
</div>
