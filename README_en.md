<div align="center">
  <img src="./static/images/logo.png" alt="OneTV-API Logo"/>
  <h1 align="center">OneTV-API</h1>
</div>

<div align="center">
  <h3>🚀 Intelligent IPTV Live Source Management System</h3>
  <p>A high-performance IPTV interface update tool developed with Python, focused on providing stable and fast live streaming services</p>
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
  <a href="./README.md">中文</a> |
  <a href="#quick-start">Quick Start</a> |
  <a href="#features">Features</a> |
  <a href="#documentation">Documentation</a>
</p>

---

## 📖 Project Overview

OneTV-API is a professional IPTV live source management system designed to provide users with high-quality, stable television live streaming services. This project adopts modern technical architecture, supports multiple deployment methods, and can automatically acquire, test, and optimize live sources to ensure the best viewing experience.

### 🎯 Design Philosophy

- **Stability First**: Ensure the availability and stability of live sources through multiple testing mechanisms
- **User Experience**: Simple configuration with support for personalized customization
- **Automated Operations**: GitHub Actions automated updates without manual intervention
- **Open Source Transparency**: Completely open source with community-driven continuous improvement

## 📋 Table of Contents

- [🚀 Quick Start](#quick-start)
- [✨ Features](#features)
- [📺 Live Source Access](#live-source-access)
- [⚙️ Configuration](#configuration)
- [🛠️ Deployment Methods](#deployment-methods)
  - [GitHub Actions (Recommended)](#github-actions-recommended)
  - [Local Running](#local-running)
  - [Docker Deployment](#docker-deployment)
- [📖 Documentation](#documentation)
- [🤝 Contributing](#contributing)
- [📄 License](#license)

## 🚀 Quick Start

### Method 1: GitHub Actions (Recommended)

1. **Fork this project** to your GitHub account
2. **Enable Actions**: Go to repository settings → Actions → Allow all actions
3. **Auto-run**: Automatically updates at 6:00 and 18:00 Beijing time daily
4. **Get results**:
   ```
   https://raw.githubusercontent.com/YourUsername/OneTV-API/main/output/onetv_api_result.m3u
   ```

### Method 2: One-Click Deploy

[![Deploy to GitHub](https://img.shields.io/badge/Deploy%20to-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/HaoHaoKanYa/OneTV-API/fork)

> [!TIP]
> GitHub Actions method is recommended for its high automation and no local environment configuration required

## ✨ Features

### 🎯 Core Features

| Feature Module | Description | Status |
|----------------|-------------|--------|
| 🔄 **Auto Update** | GitHub Actions scheduled automatic live source updates | ✅ |
| 🚀 **Smart Speed Test** | Multi-threaded concurrent testing, filtering optimal live sources | ✅ |
| 📺 **Multi-Source Aggregation** | Support for local sources, subscription sources, multicast sources, etc. | ✅ |
| 🎨 **Personalized Customization** | Custom channel templates with channel alias support | ✅ |
| 📊 **Quality Assurance** | Resolution detection, speed filtering, stability verification | ✅ |
| 🌐 **Multi-Protocol Support** | IPv4/IPv6 dual-stack support, RTMP streaming | ✅ |

### 🛡️ Technical Advantages

- **High Performance**: Asynchronous concurrent processing, supporting large-scale live source testing
- **High Availability**: Multiple fault tolerance mechanisms ensuring stable service operation
- **Easy Deployment**: Support for GitHub Actions, Docker, local running and other deployment methods
- **Easy Maintenance**: Modular design with configuration file management
- **Cross-Platform**: Support for Windows, Linux, macOS and other operating systems

## 📺 Live Source Access

### 🔗 Online Playlists

> [!NOTE]
> The following links are automatically updated live sources, updated daily at 6:00 and 18:00 Beijing time

#### Main Playlists

| Type | Link | Description |
|------|------|-------------|
| **Recommended** | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/onetv_api_result.m3u` | Curated channels, quality first |
| Complete List | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/result.m3u` | Contains all available channels |

#### Categorized Playlists

| Protocol Type | Link | Use Case |
|---------------|------|----------|
| IPv4 Only | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/ipv4/result.m3u` | IPv4 network environment |
| IPv6 Only | `https://raw.githubusercontent.com/HaoHaoKanYa/OneTV-API/main/output/ipv6/result.m3u` | IPv6 network environment |

### 📱 How to Use

1. **Copy playlist link**
2. **Add to IPTV player** (such as VLC, Kodi, Perfect Player, etc.)
3. **Start watching**

### 🌍 CDN Acceleration

If GitHub access is slow, you can use the following CDN acceleration address:

```
https://cdn.jsdelivr.net/gh/HaoHaoKanYa/OneTV-API@main/output/onetv_api_result.m3u
```

## ⚙️ Configuration

### 📝 Configuration Files

The project supports personalized customization through configuration files, main configuration files are located in the `config/` directory:

- `onetv_api_config.ini` - Main configuration file
- `onetv_api_demo.txt` - Channel template file
- `local.txt` - Local live sources
- `whitelist.txt` - Whitelist channels
- `subscribe.txt` - Subscription source list

### 🔧 Core Configuration Items

<details>
<summary>Click to expand detailed configuration instructions</summary>

#### Basic Settings

| Configuration Item | Description | Default Value | Recommended Value |
|-------------------|-------------|---------------|-------------------|
| `open_speed_test` | Enable speed testing | `True` | `True` |
| `open_filter_speed` | Enable speed filtering | `True` | `True` |
| `min_speed` | Minimum speed requirement (M/s) | `0.5` | `1.0` |
| `speed_test_timeout` | Speed test timeout (seconds) | `10` | `15` |

#### Network Settings

| Configuration Item | Description | Default Value | Recommended Value |
|-------------------|-------------|---------------|-------------------|
| `ipv_type` | IP protocol type | `全部` | `全部` |
| `ipv4_num` | IPv4 interface count | `5` | `3` |
| `ipv6_num` | IPv6 interface count | `5` | `3` |

#### Source Settings

| Configuration Item | Description | Default Value | Recommended Value |
|-------------------|-------------|---------------|-------------------|
| `open_local` | Enable local sources | `True` | `True` |
| `open_subscribe` | Enable subscription sources | `False` | `True` |
| `local_num` | Local source interface count | `10` | `5` |
| `subscribe_num` | Subscription source interface count | `10` | `5` |

</details>

### 📋 Channel Template Configuration

Support for custom channel templates, format as follows:

```
Channel Group,#genre#
Channel Name,Channel Link
Channel Name,Channel Link

Another Group,#genre#
Channel Name,Channel Link
```

### 🎯 Personalized Customization

1. **Modify channel template**: Edit `config/onetv_api_demo.txt`
2. **Add local sources**: Edit `config/local.txt`
3. **Set whitelist**: Edit `config/whitelist.txt`
4. **Adjust configuration**: Edit `config/onetv_api_config.ini`

## 🛠️ Deployment Methods

### GitHub Actions (Recommended)

> [!TIP]
> This is the simplest and most stable deployment method, requiring no local environment configuration

#### 🚀 Quick Deployment

1. **Fork Project**
   ```bash
   # Click the Fork button in the top right corner of the page
   # Or visit: https://github.com/HaoHaoKanYa/OneTV-API/fork
   ```

2. **Enable Actions**
   - Go to your repository
   - Click the `Actions` tab
   - Click `I understand my workflows, go ahead and enable them`

3. **Configure Permissions**
   - Go to `Settings` → `Actions` → `General`
   - In `Workflow permissions` select `Read and write permissions`
   - Save settings

4. **Manually Trigger First Run**
   - Go to `Actions` tab
   - Select `Update OneTV-API` workflow
   - Click `Run workflow` → `Run workflow`

5. **Get Results**
   ```
   https://raw.githubusercontent.com/YourUsername/OneTV-API/main/output/onetv_api_result.m3u
   ```

#### ⏰ Automatic Updates

- **Scheduled Runs**: Daily at 6:00 and 18:00 Beijing time
- **Manual Trigger**: Can be manually run anytime on the Actions page
- **Configuration Updates**: Automatically runs after modifying configuration files

### Local Running

> [!NOTE]
> Suitable for users who need custom configurations or local debugging

#### 📋 Prerequisites

- **Python**: Version 3.11 or higher
- **Git**: For cloning the repository
- **Network**: Stable internet connection

#### 🔧 Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/HaoHaoKanYa/OneTV-API.git
   cd OneTV-API
   ```

2. **Install Dependencies**
   ```bash
   # Use Python 3.11
   py -3.11 -m pip install -r requirements.txt

   # Or use pip directly
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   ```bash
   # Edit configuration file
   notepad config/onetv_api_config.ini

   # Edit channel template
   notepad config/onetv_api_demo.txt
   ```

4. **Run Program**
   ```bash
   # Use Python 3.11
   py -3.11 main.py

   # Or use python directly
   python main.py
   ```

5. **Get Results**
   - Generated files are in the `output/` directory
   - Main result file: `output/onetv_api_result.m3u`

#### 🎯 Advanced Usage

- **Custom Configuration**: Modify `config/onetv_api_config.ini`
- **Add Local Sources**: Edit `config/local.txt`
- **Set Whitelist**: Edit `config/whitelist.txt`
- **Modify Template**: Edit `config/onetv_api_demo.txt`

### Docker Deployment

> [!TIP]
> Docker deployment provides consistent environment and easy management

#### 🐳 Quick Start

```bash
# Pull image
docker pull haohaokanye/onetv-api:latest

# Run container
docker run -d \
  --name onetv-api \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/output:/app/output \
  haohaokanye/onetv-api:latest
```

#### 🔧 Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  onetv-api:
    image: haohaokanye/onetv-api:latest
    container_name: onetv-api
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./output:/app/output
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

#### 📊 Container Management

```bash
# View logs
docker logs onetv-api

# Enter container
docker exec -it onetv-api bash

# Stop container
docker stop onetv-api

# Remove container
docker rm onetv-api
```

## 📖 Documentation

### 📱 Supported Players

OneTV-API generated playlists are compatible with various IPTV players:

| Player | Platform | Support Level | Notes |
|--------|----------|---------------|-------|
| **VLC Media Player** | Windows/Mac/Linux | ✅ Full | Recommended, best compatibility |
| **Kodi** | Multi-platform | ✅ Full | Perfect for media centers |
| **Perfect Player** | Android/iOS | ✅ Full | Mobile device preferred |
| **IPTV Smarters** | Android/iOS | ✅ Full | Feature-rich mobile app |
| **TiviMate** | Android TV | ✅ Full | Android TV optimized |
| **GSE Smart IPTV** | iOS/Apple TV | ✅ Full | Apple ecosystem preferred |

### 🔧 Usage Instructions

1. **Get Playlist URL**
   ```
   https://raw.githubusercontent.com/YourUsername/OneTV-API/main/output/onetv_api_result.m3u
   ```

2. **Add to Player**
   - Open your IPTV player
   - Add new playlist/source
   - Paste the URL above
   - Save and refresh

3. **Enjoy Watching**
   - Browse channel categories
   - Select channels to watch
   - Enjoy high-quality live streams

### 📊 Channel Categories

The generated playlist includes the following channel groups:

- **公众号【壹来了】** - Featured channels
- **地方频道** - Local channels
- **电竞频道** - Esports channels
- **体育频道** - Sports channels
- **香港频道** - Hong Kong channels
- **澳门频道** - Macau channels
- **台湾频道** - Taiwan channels

## 🤝 Contributing

We welcome community contributions! Here's how you can help improve OneTV-API:

### 🐛 Bug Reports

If you encounter any issues:

1. **Check existing issues** first to avoid duplicates
2. **Create detailed bug report** with:
   - Operating system and version
   - Python version
   - Error messages and logs
   - Steps to reproduce

### 💡 Feature Requests

Have ideas for new features?

1. **Open an issue** with the `enhancement` label
2. **Describe the feature** in detail
3. **Explain the use case** and benefits

### 🔧 Development

Want to contribute code?

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following our coding standards
4. **Test thoroughly** to ensure stability
5. **Submit pull request** with detailed description

### 📝 Development Standards

- **Code Style**: Follow PEP 8 Python style guide
- **Documentation**: Update README and comments for new features
- **Testing**: Ensure all tests pass before submitting
- **Commit Messages**: Use clear, descriptive commit messages

### 🙏 Acknowledgments

This project is based on the excellent work of the original [IPTV-API](https://github.com/Guovin/iptv-api) project by **Guovin**. We extend our sincere gratitude for their foundational contribution to the IPTV management community.

**Original Developer**: Guovin
**WeChat Public Account**: 【古欧文】
**Original Repository**: https://github.com/Guovin/iptv-api

While this OneTV-API project has been significantly customized and enhanced for personal use, we acknowledge and respect the original developer's innovative work that made this project possible.

## 📄 License

### Copyright Notice

**Copyright © 2024 OneTV-API Project**
**Repository**: https://github.com/HaoHaoKanYa/OneTV-API
**Maintainer**: HaoHaoKanYa

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Acknowledgments

This project incorporates and builds upon the following open-source projects:

- **Original IPTV-API**: [Guovin/iptv-api](https://github.com/Guovin/iptv-api) - Foundation framework
- **Python Libraries**: Various Python packages listed in requirements.txt
- **Community Contributions**: Channel sources and testing feedback from the community

### Usage Rights

✅ **Permitted**:
- Personal use and modification
- Educational and research purposes
- Commercial use with proper attribution
- Distribution and redistribution

❌ **Prohibited**:
- Removing copyright notices
- Using for illegal content distribution
- Claiming original authorship
- Warranty or liability claims

---

## ⚠️ Disclaimer

### Legal Notice

> [!IMPORTANT]
> **Please read this disclaimer carefully before using OneTV-API**

### 🔒 Content Responsibility

1. **No Content Ownership**: OneTV-API does not host, store, or distribute any video content
2. **Aggregation Tool**: This software only aggregates publicly available streaming links
3. **User Responsibility**: Users are solely responsible for the content they access
4. **Legal Compliance**: Users must comply with local laws and regulations

### 🛡️ Service Limitations

1. **No Guarantees**: No warranty for service availability, accuracy, or reliability
2. **Third-Party Sources**: All streaming sources are provided by third parties
3. **Service Interruption**: Service may be interrupted or discontinued without notice
4. **Data Accuracy**: No guarantee for the accuracy of channel information

### ⚖️ Legal Compliance

1. **Copyright Respect**: Users must respect intellectual property rights
2. **Local Laws**: Comply with broadcasting and copyright laws in your jurisdiction
3. **Personal Use**: Recommended for personal, non-commercial use only
4. **Content Filtering**: Users should implement appropriate content filtering

### 🚫 Limitation of Liability

The developers and contributors of OneTV-API shall not be liable for:
- Any direct, indirect, incidental, or consequential damages
- Loss of data, profits, or business interruption
- Legal issues arising from content access
- Third-party service failures or interruptions

### 📞 Contact

For questions about this disclaimer or the project:
- **GitHub Issues**: [Report Issues](https://github.com/HaoHaoKanYa/OneTV-API/issues)
- **Repository**: https://github.com/HaoHaoKanYa/OneTV-API

---

**By using OneTV-API, you acknowledge that you have read, understood, and agree to be bound by this disclaimer.**
