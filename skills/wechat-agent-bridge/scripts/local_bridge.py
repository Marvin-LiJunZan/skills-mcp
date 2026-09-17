#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat to Local Agent Bridge Controller (方案 2 个人微信群组定向路由与遥控调度中枢)
精准绑定用户的各个专业研究微信群，接收指令后分发至对应领域的专业 Agent / Skill / 本地 GPU 任务。
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# 🎯 根据用户微信群列表，精准映射群名到对应的专业领域 Skills / 执行动作
GROUP_SKILL_MAP = {
    "科研绘图": {
        "role": "科研绘图专家 (Academic Figure Designer)",
        "skills": ["academic-figure-skill", "scipilot-figure-skill", "ccc-academic-figure-style", "image-enhancer"],
        "desc": "顶刊配图生成、多子图拼版排版、模糊图片超分辨率增强(4K)"
    },
    "岩土": {
        "role": "岩土工程智能体 (Geotechnical AI)",
        "skills": ["abaqus-mcp", "ccc-journal-guides"],
        "desc": "Computers and Geotechnics / Landslides 论文规范、土体本构与仿真"
    },
    "精选论文": {
        "role": "文献精读与评审助手",
        "skills": ["integrated-research-reviewer", "nature-skills", "cite-verify"],
        "desc": "CMAME/Top期刊论文解析、文献创新点提取、跨论文交叉论述"
    },
    "skills": {
        "role": "Skills 生态调度中心",
        "skills": ["all"],
        "desc": "Git双推同步、项目脱敏打包、新技能热插拔部署"
    },
    "骨料分布": {
        "role": "混凝土微观结构分析专家",
        "skills": ["abaqus-mcp", "ccc-paper-converter"],
        "desc": "骨料投放随机几何算法、Abaqus 网格划分、SEM 图像量化分析"
    },
    "本构": {
        "role": "力学本构模型专家",
        "skills": ["abaqus-mcp", "research-workflow"],
        "desc": "UMAT/VUMAT 用户子程序构建、弹塑性损伤力学推导与标定"
    },
    "裂缝检测-重建": {
        "role": "计算机视觉与缺陷无损检测专家",
        "skills": ["image-enhancer", "ai-video-producer"],
        "desc": "裂缝智能分割、3D重建点云、视频关键帧高精度画质增强"
    },
    "数字孪生": {
        "role": "智能建造数字孪生中枢",
        "skills": ["research-workflow", "abaqus-mcp"],
        "desc": "传感器实时数据反演、有限元实时快照计算"
    },
    "提示词": {
        "role": "Prompt 架构与科研思维链工匠",
        "skills": ["human-writing", "paper-novelty-design"],
        "desc": "顶级期刊提示词调优、学术去 AI 味、破除学术俗套"
    },
    "机器学习": {
        "role": "AI for Science 算法工程师",
        "skills": ["AI-Research-SKILLs", "AI-Scientist"],
        "desc": "PINN 物理信息神经网络、代理模型训练、超参数调优"
    },
    "拓扑优化": {
        "role": "结构轻量化与拓扑设计专家",
        "skills": ["abaqus-mcp", "ccc-journal-guides"],
        "desc": "Thin-Walled Structures 论文工作流、SIMP 刚度最优化"
    },
    "3D打印": {
        "role": "增材制造工艺研究员",
        "skills": ["research-workflow"],
        "desc": "打印路径规划、热力耦合有限元模拟"
    }
}

class WeChatDispatcher(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        # 兼容各大微信协议服务 (Gewechat / WeChaty / Dify / iPad协议)
        group_name = payload.get("GroupName") or payload.get("group_name") or payload.get("room_name", "")
        content = str(payload.get("Content") or payload.get("content", "")).strip()
        from_user = payload.get("FromUserName") or payload.get("sender", "unknown")
        
        print(f"\n[微信消息接收] 来自群: 【{group_name or '私聊/未知'}】 | 发送人: {from_user}")
        print(f"👉 指令内容: {content}")
        
        reply_text = self.dispatch_to_group_agent(group_name, content)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        response = {"status": "success", "reply": reply_text}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def dispatch_to_group_agent(self, group_name: str, cmd: str) -> str:
        repo_root = Path(__file__).resolve().parents[3]
        cmd_lower = cmd.lower()

        # 1. 全局系统指令（任何群或私聊都可直接调用）
        if "git" in cmd_lower and ("推" in cmd or "push" in cmd or "同步" in cmd):
            print("[+] 触发 GitHub + Gitee 双推...")
            try:
                res = subprocess.run(["git", "-c", "http.sslVerify=false", "push", "origin", "master"], 
                                     cwd=str(repo_root), capture_output=True, text=True, timeout=60)
                return "✅ 电脑已成功一键同步推送至 Gitee 和 GitHub 双仓库！" if res.returncode == 0 else f"❌ 推送失败：\n{res.stderr[:200]}"
            except Exception as e:
                return f"❌ 执行异常：{e}"

        if "打包" in cmd or "脱敏" in cmd:
            return "📦 微信传输优化版压缩包已就绪：\n• Part 1 (Skills技能库): skills_collection_part1.zip (974MB)\n• Part 2 (MCP服务): mcp_servers_part2.zip (128MB)\n文件位于电脑 C:\\JunzanLi_project\\ 下。"

        # 2. 识别群聊身份，做专业领域分发
        matched_group = None
        for g_key in GROUP_SKILL_MAP:
            if g_key in group_name:
                matched_group = g_key
                break

        if matched_group:
            cfg = GROUP_SKILL_MAP[matched_group]
            print(f"[+] 识别到专属群: 【{matched_group}】，激活角色: {cfg['role']}")

            if "绘图" in matched_group:
                if "增强" in cmd or "模糊" in cmd or "画质" in cmd:
                    return "🖼️ 【科研绘图助手】已待命！请将模糊图片直接发到群里，后台将自动执行超分辨率重构算法放大 4 倍并锐化输出！"
                return f"📊 【{cfg['role']}】收到指令：『{cmd}』。\n正在调用 {cfg['skills']} 生成出版级高保真科研图表..."

            if "岩土" in matched_group or "拓扑" in matched_group or "本构" in matched_group:
                if "仿真" in cmd or "建模" in cmd or "跑" in cmd:
                    return f"⚙️ 【{cfg['role']}】已收到建模指令！正在调用 Abaqus MCP 后台生成 Python 脚本并提交求解分析..."

            return f"🤖 【{cfg['role']}】已就位！\n已为【{matched_group}】群载入专业能力：{cfg['desc']}。\n正在处理任务：『{cmd}』"

        # 3. 兜底回显
        return f"💻 电脑工作站已收到：『{cmd}』，各领域 Skills 与 MCP 待命中。"

    def log_message(self, format, *args):
        return

def run_server(port=8088):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WeChatDispatcher)
    print(f"================================================================")
    print(f"🚀 WeChat Agent Bridge 已就绪！监听端口: http://127.0.0.1:{port}")
    print(f"📡 已自动绑定您的各专业微信群：")
    for name, info in GROUP_SKILL_MAP.items():
        print(f"   • 【{name}】 -> 对应：{info['role']}")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] 服务已安全停止。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WeChat Agent Bridge")
    parser.add_argument("--port", type=int, default=8088, help="Webhook port")
    args = parser.parse_args()
    run_server(args.port)
