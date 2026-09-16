import assert from "node:assert/strict";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import fs from "node:fs/promises";
import { extractMessages, normalizeConversation, renderMarkdown, exportAll } from "./export_chatgpt_conversations.mjs";

const fixture = {
  id: "conv-123",
  title: "每日复盘",
  create_time: 1710000000,
  update_time: 1710000100,
  current_node: "a2",
  mapping: {
    root: { message: null, parent: null, children: ["a1"] },
    a1: { parent: "root", message: { author: { role: "user" }, create_time: 1710000001, content: { parts: ["今天完成了什么？"] } } },
    a2: { parent: "a1", message: { author: { role: "assistant" }, create_time: 1710000002, content: { parts: ["完成了导出器测试。"] } } },
  },
};

const messages = extractMessages(fixture);
assert.deepEqual(messages.map((message) => message.role), ["user", "assistant"]);
assert.equal(messages[1].text, "完成了导出器测试。");

const normalized = normalizeConversation({ id: fixture.id, title: fixture.title }, fixture);
assert.equal(normalized.id, "conv-123");
assert.match(renderMarkdown(normalized), /每日复盘/);
assert.match(renderMarkdown(normalized), /完成了导出器测试/);

const server = http.createServer((request, response) => {
  response.setHeader("content-type", "application/json");
  if (request.url === "/") return response.end("<html><body>mock ChatGPT</body></html>");
  if (request.url.startsWith("/backend-api/conversations")) return response.end(JSON.stringify({ items: [{ id: "conv-123", title: "每日复盘", update_time: 1710000100 }], total: 1 }));
  if (request.url === "/backend-api/conversation/conv-123") return response.end(JSON.stringify(fixture));
  response.statusCode = 404;
  response.end(JSON.stringify({ error: "not found" }));
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const address = server.address();
const root = await fs.mkdtemp(path.join(os.tmpdir(), "chatgpt-export-e2e-"));
const output = path.join(root, "output");
const profile = path.join(root, "profile");
try {
  const result = await exportAll({ output, profile, headed: false, baseUrl: `http://127.0.0.1:${address.port}` });
  assert.deepEqual({ found: result.found, exported: result.exported }, { found: 1, exported: 1 });
  const files = await fs.readdir(output);
  assert.equal(files.filter((file) => file.endsWith(".md")).length, 1);
  assert.equal(files.filter((file) => file.endsWith(".json")).length, 1);
  console.log("ChatGPT export parser/render/e2e mock test passed");
} finally {
  server.close();
  await fs.rm(root, { recursive: true, force: true });
}
