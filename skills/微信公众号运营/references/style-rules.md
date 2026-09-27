# 文风硬规则 + 正文 HTML 内联样式规范

## 文风硬规则（写文章时逐条执行）

### 段落与句式
- 每段 1 到 3 句，手机上一段最多 4 行。
- 段落之间恰好空一行。
- 短句为主，长短句交错，允许偶尔一句一段。
- 用具体数字、具体场景、具体动作说话，少用抽象名词。

### 禁区（出现即重写）
- 破折号（—— 和 — 都不行），改用逗号、句号或「：」。
- 否定框架强调句式：「不是 X，而是 Y」「这无关 X，这关乎 Y」「少点 X，多点 Y」。一律改成正面直述。
- AI 腔词汇：值得注意的是、众所周知、在当今时代、赋能、抓手、闭环、生态化反、深度赋能、不容错过、震撼、颠覆认知。
- 机械连接词连续开头：首先、其次、再次、最后。
- 句末叠用标点；感叹号全篇不超过 2 个。
- 标题党词：震惊、必看、不看后悔、疯狂转发。

### 格式
- 数字一律阿拉伯数字（3 篇、2 小时、80%）。
- 中文与英文单词、数字之间加一个空格（用 Git 管理 3 个版本）。
- 强调用加粗，加粗处渲染为品牌金；引号用「」。
- 小节标题用短句，不超过 12 字。

### 收尾自检清单（写完必跑，结果附在文末）
- 违禁词命中：0
- 否定框架句式：0
- 破折号：0
- 超 3 句段落：0
- 开头 3 到 5 行有明确钩子：是
- 结尾有关注 CTA + 留言问题 + 转发钩子：是

## 正文 HTML 内联样式规范（推草稿箱用）

微信会过滤 `<style>` 标签，所有样式必须写在 `style=""` 里。骨架：

```html
<section style="font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; font-size: 15px; color: #3A3F4B; line-height: 1.75; letter-spacing: 0.5px; padding: 10px 5px;">
  <p style="margin: 14px 0;">正文段落</p>
  <h2 style="font-size: 18px; color: #D4A93C; margin: 34px 0 14px;">◆ 小节标题</h2>
  <p style="margin: 14px 0;">强调用 <strong style="color: #D4A93C;">金色加粗</strong>。</p>
  <p style="text-align: center; margin: 25px 0;"><img src="{{IMG1}}" style="max-width: 100%; border-radius: 8px;" /></p>
  <p style="text-align: center; font-size: 12px; color: #8A93A6; margin: 0 0 20px;">图注一句话</p>
  <p style="margin: 28px 0 14px; padding: 14px 16px; background: #F4F7FB; border-left: 3px solid #0C2242; color: #5A6274;">文末互动框：留言问题 + 转发钩子</p>
</section>
```

注意：
- 图片 `src` 先用占位符 `{{IMG1}}`、`{{IMG2}}`，推送脚本会自动替换为上传后的 mmbiz URL。正文图只能用微信域名，外部图床会被屏蔽。
- 标题（title）、摘要（digest）、作者走脚本参数，不写进 HTML。
