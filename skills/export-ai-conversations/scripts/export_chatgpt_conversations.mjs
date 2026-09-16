#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import process from "node:process";
import { pathToFileURL } from "node:url";
import { spawn, execFileSync } from "node:child_process";
import { chromium } from "playwright";

const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1"));
const REPO_ROOT = path.resolve(SCRIPT_DIR, "../../..");
const DEFAULT_OUTPUT = path.join(REPO_ROOT, "chats");
const DEFAULT_PROFILE = path.join(os.homedir(), ".chatgpt-export-profile");
const DEFAULT_BASE_URL = "https://chatgpt.com";

function argValue(args, name, fallback = undefined) {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function hasArg(args, name) {
  return args.includes(name);
}

function safeFileName(value) {
  return String(value || "未命名对话")
    .replace(/[\\/:*?"<>|\r\n\t]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 80) || "未命名对话";
}

function localDate(value) {
  if (!value) return "未知时间";
  const date = new Date(typeof value === "number" ? value * 1000 : value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString("zh-CN", { hour12: false });
}

function textFromContent(content) {
  if (!content) return "";
  if (typeof content === "string") return content;
  if (Array.isArray(content.parts)) return content.parts.map((part) => typeof part === "string" ? part : JSON.stringify(part)).join("\n");
  if (Array.isArray(content.text)) return content.text.join("\n");
  return content.text || content.result || "";
}

export function extractMessages(conversation) {
  const mapping = conversation?.mapping || {};
  const nodes = Object.entries(mapping).map(([id, node]) => ({ id, ...node }));
  const current = conversation.current_node || nodes.at(-1)?.id;
  const chain = [];
  const seen = new Set();
  let node = mapping[current];
  while (node && !seen.has(node)) {
    seen.add(node);
    const message = node.message;
    if (message?.content) {
      const role = message.author?.role || "unknown";
      if (["user", "assistant", "system"].includes(role)) {
        chain.push({ role, text: textFromContent(message.content), time: message.create_time });
      }
    }
    node = node.parent ? mapping[node.parent] : null;
  }
  return chain.reverse().filter((item) => item.text.trim());
}

export function normalizeConversation(summary, detail) {
  const source = detail || summary || {};
  return {
    id: String(source.conversation_id || source.id || summary?.id || "unknown"),
    title: source.title || summary?.title || "未命名对话",
    create_time: source.create_time || summary?.create_time,
    update_time: source.update_time || summary?.update_time,
    messages: extractMessages(source),
  };
}

export function renderMarkdown(conversation) {
  const lines = [
    `# [ChatGPT] 对话记录: ${conversation.title}`,
    "",
    "- **平台 / 应用**: `ChatGPT 网页版`",
    `- **会话 ID**: \`${conversation.id}\``,
    `- **创建时间**: ${localDate(conversation.create_time)}`,
    `- **更新时间**: ${localDate(conversation.update_time)}`,
    "",
    "---",
    "",
  ];
  for (const message of conversation.messages) {
    const label = message.role === "user" ? "👤 用户" : message.role === "assistant" ? "🤖 ChatGPT" : "⚙️ 系统";
    lines.push(`## ${label} (${localDate(message.time)})`, "", message.text, "", "---", "");
  }
  return lines.join("\n");
}

const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";

async function waitForCdp(port) {
  const endpoint = `http://127.0.0.1:${port}/json/version`;
  const deadline = Date.now() + 20000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(endpoint);
      if (response.ok) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error("普通 Edge 未能开启本地 CDP 端口。");
}

async function launchNormalEdge(profile, port, visible, url = DEFAULT_BASE_URL) {
  const args = [`--user-data-dir=${profile}`, "--profile-directory=Default", `--remote-debugging-port=${port}`, "--no-first-run", "--no-default-browser-check", url];
  if (!visible) args.push("--headless=new", "--disable-gpu");
  const child = spawn(EDGE, args, { detached: true, stdio: "ignore" });
  child.unref();
  await waitForCdp(port);
  return child.pid;
}

function stopProcessTree(pid) {
  if (!pid) return;
  try { execFileSync("taskkill", ["/PID", String(pid), "/T", "/F"], { stdio: "ignore" }); } catch {}
}

async function apiJson(page, endpoint, accessToken) {
  return page.evaluate(async ({ url, token }) => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await fetch(url, { credentials: "include", headers });
    if (!response.ok) {
      if (response.status === 401 || response.status === 403) {
        throw new Error("ChatGPT 登录态不可用或被拒绝。请先用 --setup 完成登录，再运行每日导出。");
      }
      throw new Error(`${response.status} ${response.statusText} for ${url}`);
    }
    return response.json();
  }, { url: endpoint, token: accessToken });
}

async function fetchConversations(page, since, accessToken) {
  const summaries = [];
  for (let offset = 0; ; offset += 100) {
    const payload = await apiJson(page, `/backend-api/conversations?offset=${offset}&limit=100&order=updated&is_archived=false&is_starred=false&hide_snorlax=true`, accessToken);
    const items = payload.items || [];
    summaries.push(...items);
    if (items.length < 100 || (payload.total && summaries.length >= payload.total)) break;
  }
  const cached = await page.evaluate(() => {
    const result = [];
    for (const key of Object.keys(localStorage).filter((item) => item.includes("conversation-history"))) {
      try {
        const stored = JSON.parse(localStorage.getItem(key) || "{}").value;
        for (const page of stored?.pages || []) {
          for (const item of page.items || []) result.push(item);
        }
      } catch {}
    }
    return result;
  });
  const sidebar = await page.evaluate(() => [...document.querySelectorAll('a[href*="/c/"]')]
    .map((link) => ({
      href: link.getAttribute("href") || "",
      title: (link.getAttribute("aria-label") || link.textContent || "").trim(),
    }))
    .filter((item) => item.href));
  const byId = new Map(summaries.map((item) => [item.id || item.conversation_id, item]));
  for (const item of cached) {
    const id = item.id || item.conversation_id;
    if (id && !byId.has(id)) byId.set(id, item);
  }
  for (const item of sidebar) {
    const match = item.href.match(/\/c\/([^/?#]+)/);
    if (!match || byId.has(match[1])) continue;
    byId.set(match[1], {
      id: match[1],
      title: item.title.replace(/\s+—\s+项目\s+.+?\s+中的聊天(?:（未读）)?$/, "").trim() || "未命名对话",
    });
  }
  const cutoff = since ? new Date(`${since}T00:00:00`) : null;
  return [...byId.values()].filter((item) => {
    if (!cutoff) return true;
    const value = item.update_time || item.create_time || 0;
    const date = typeof value === "number" ? new Date(value * 1000) : new Date(value);
    return date >= cutoff;
  });
}

export async function exportAll({ output, profile, profileDirectory, headed, since, baseUrl = DEFAULT_BASE_URL, cdpPort }) {
  await fs.mkdir(output, { recursive: true });
  let browser;
  let context;
  let spawnedPid;
  if (cdpPort) {
    spawnedPid = await launchNormalEdge(profile, cdpPort, headed, baseUrl);
    browser = await chromium.connectOverCDP(`http://127.0.0.1:${cdpPort}`);
    context = browser.contexts()[0];
  } else {
    context = await chromium.launchPersistentContext(profile, {
      headless: !headed,
      channel: "msedge",
      args: profileDirectory ? [`--profile-directory=${profileDirectory}`] : [],
      viewport: { width: 1440, height: 1000 },
    });
  }
  try {
    const page = context.pages()[0] || await context.newPage();
    await page.goto(baseUrl, { waitUntil: "domcontentloaded" });
    await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);
    if (headed && !cdpPort) {
      console.log("请在打开的浏览器窗口中完成 ChatGPT 登录；完成后回到终端按 Enter。\n");
      await new Promise((resolve) => process.stdin.once("data", resolve));
    } else if (page.url().includes("/auth/")) {
      throw new Error("当前浏览器登录态不可用。先用 --setup 打开登录窗口并完成登录。");
    }
    const accessToken = cdpPort ? await page.evaluate(async () => {
      const response = await fetch("/api/auth/session", { credentials: "include" });
      if (!response.ok) return null;
      const session = await response.json();
      return session.accessToken || null;
    }) : null;
    if (cdpPort && !accessToken) throw new Error("当前浏览器登录态没有可用的 ChatGPT 访问令牌。请重新运行 --setup 登录。");
    const summaries = await fetchConversations(page, since, accessToken);
    let count = 0;
    for (const summary of summaries) {
      const detail = await apiJson(page, `/backend-api/conversation/${encodeURIComponent(summary.id)}`, accessToken);
      const conversation = normalizeConversation(summary, detail);
      if (!conversation.messages.length) continue;
      const rawTime = conversation.update_time || conversation.create_time;
      const stamp = rawTime ? new Date(rawTime * 1000).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z") : "unknown";
      const base = `ChatGPT_${stamp}_${safeFileName(conversation.title)}_${conversation.id.slice(0, 8)}`;
      await fs.writeFile(path.join(output, `${base}.md`), renderMarkdown(conversation), "utf8");
      await fs.writeFile(path.join(output, `${base}.json`), JSON.stringify(conversation, null, 2), "utf8");
      count += 1;
    }
    return { found: summaries.length, exported: count, output };
  } finally {
    if (browser) await browser.close();
    else await context.close();
    stopProcessTree(spawnedPid);
  }
}

async function setupProfile(profile) {
  await fs.mkdir(profile, { recursive: true });
  const port = 9333;
  const pid = await launchNormalEdge(profile, port, true);
  console.log("请在普通 Edge 窗口中完成 ChatGPT 登录；完成后回到终端按 Enter。\n");
  await new Promise((resolve) => process.stdin.once("data", resolve));
  stopProcessTree(pid);
}

async function main() {
  const args = process.argv.slice(2);
  const profile = path.resolve(argValue(args, "--profile", DEFAULT_PROFILE));
  if (hasArg(args, "--setup")) {
    await setupProfile(profile);
    return;
  }
  const result = await exportAll({
    output: path.resolve(argValue(args, "--output", DEFAULT_OUTPUT)),
    profile,
    profileDirectory: argValue(args, "--profile-directory"),
    headed: hasArg(args, "--setup") || hasArg(args, "--headed"),
    since: argValue(args, "--since"),
    baseUrl: argValue(args, "--base-url", DEFAULT_BASE_URL),
    cdpPort: Number(argValue(args, "--cdp-port", "9223")),
  });
  console.log(JSON.stringify(result, null, 2));
}

if (import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
