# 外网访问指南

## 方案一：ngrok（推荐）

### 优点
- 简单易用，无需配置
- 免费版可用
- 支持HTTPS

### 安装步骤

1. **下载ngrok**
   - 访问 https://ngrok.com/download
   - 下载对应系统的版本
   - 解压到任意目录

2. **注册账号**
   - 访问 https://dashboard.ngrok.com/signup
   - 注册免费账号

3. **获取authtoken**
   - 登录 https://dashboard.ngrok.com
   - 复制 Your Authtoken

4. **配置authtoken**
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

5. **启动游戏**
   ```bash
   cd game
   python run_web.py
   ```

6. **启动内网穿透**（新终端）
   ```bash
   ngrok http 5000
   ```

7. **获取公网地址**
   - 查看 Terminal 中的 Forwarding 地址
   - 类似：`https://xxxx.ngrok-free.app`
   - 把这个地址分享给朋友

---

## 方案二：localtunnel

### 优点
- 无需注册
- 一行命令启动

### 安装步骤

1. **安装Node.js**
   - 访问 https://nodejs.org 下载安装

2. **安装localtunnel**
   ```bash
   npm install -g localtunnel
   ```

3. **启动游戏**
   ```bash
   cd game
   python run_web.py
   ```

4. **启动内网穿透**（新终端）
   ```bash
   lt --port 5000
   ```

5. **获取公网地址**
   - Terminal 会显示 `your url is: https://xxx.loca.lt`
   - 把这个地址分享给朋友

---

## 方案三：Cloudflare Tunnel

### 优点
- 稳定可靠
- 免费使用
- 全球CDN加速

### 安装步骤

1. **下载cloudflared**
   - 访问 https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
   - 下载对应系统的版本

2. **启动内网穿透**
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

3. **获取公网地址**
   - Terminal 会显示类似 `https://xxx.trycloudflare.com`
   - 把这个地址分享给朋友

---

## 方案四：frp（需要公网服务器）

### 优点
- 完全自主控制
- 稳定可靠
- 可自定义域名

### 缺点
- 需要有公网服务器
- 配置相对复杂

### 安装步骤

1. **在公网服务器上安装frps**
   ```bash
   # 下载frp
   wget https://github.com/fatedier/frp/releases/download/v0.58.0/frp_0.58.0_linux_amd64.tar.gz
   tar -xzf frp_0.58.0_linux_amd64.tar.gz
   cd frp_0.58.0_linux_amd64
   ```

2. **配置frps.toml**
   ```toml
   bindPort = 7000
   ```

3. **启动frps**
   ```bash
   ./frps -c frps.toml
   ```

4. **在本地安装frpc**
   - 下载对应的Windows版本
   - 解压到任意目录

5. **配置frpc.toml**
   ```toml
   serverAddr = "你的服务器IP"
   serverPort = 7000
   
   [[proxies]]
   name = "game"
   type = "tcp"
   localIP = "127.0.0.1"
   localPort = 5000
   remotePort = 5000
   ```

6. **启动frpc**
   ```bash
   ./frpc -c frpc.toml
   ```

7. **访问游戏**
   - 使用 `http://你的服务器IP:5000` 访问

---

## 使用一键启动脚本

```bash
cd game
python run_public.py
```

脚本会自动：
1. 初始化数据库
2. 启动游戏服务器
3. 引导你选择内网穿透方案

---

## 常见问题

### Q: 为什么朋友访问不了？
A: 请检查：
1. 游戏是否已启动（http://localhost:5000 本地能访问）
2. 内网穿透是否成功（查看输出的公网地址）
3. 防火墙是否阻止了相关端口

### Q: ngrok 免费版有什么限制？
A: 免费版限制：
- 每月有流量限制
- 域名会随机变化
- 一次只能运行一个隧道

### Q: 如何让地址固定不变？
A: 可以：
1. 使用ngrok付费版，获得固定域名
2. 使用Cloudflare Tunnel，配置自定义域名
3. 使用frp，配置自定义域名

### Q: 游戏很卡怎么办？
A: 可能原因：
1. 网络延迟（选择距离近的服务器）
2. 服务器带宽不足
3. 使用CDN加速（如Cloudflare）
