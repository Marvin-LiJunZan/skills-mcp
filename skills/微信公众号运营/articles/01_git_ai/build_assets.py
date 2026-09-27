from pathlib import Path
import html, re, subprocess
BASE=Path(__file__).parent
T=BASE.parent.parent/'templates'
S=BASE.parent.parent/'scripts'

def rep(src, out, pairs):
    s=(T/src).read_text(encoding='utf-8')
    for a,b in pairs: s=s.replace(a,b)
    (BASE/out).write_text(s,encoding='utf-8')

rep('cover.html','cover.html', [('研究生生存栈','研究生生存栈 01'),('超级搜索','Git × GitHub × Gitee'),('把搜索这件事交给 AI','学会 6 个概念，剩下的交给 AI')])
rep('flow.html','images/01_timeline.html', [('流程图大标题','别再复制“最终版”'),('一句副标题','Git 给科研项目一条可回看的时间线'),('第一步名称','Baseline'),('这一步做什么、怎么做','模型首次稳定运行'),('第二步名称','Commit'),('第三步名称','新 Loss'),('第四步名称','AI 重构'),('第五步名称','恢复 / 对比'),('底部一句话总结','每一次有效修改，都留下清楚的版本节点')])
rep('flow.html','images/02_push_pull.html', [('流程图大标题','Clone · Pull · Push'),('一句副标题','先看懂方向，再让 AI 帮你操作'),('第一步名称','Repository'),('这一步做什么、怎么做','一个被 Git 管理的科研项目'),('第二步名称','Clone'),('第三步名称','Pull'),('第四步名称','Commit'),('第五步名称','Push'),('底部一句话总结','本地 Git 管版本，GitHub / Gitee 管远程同步')])
rep('flow.html','images/03_template.html', [('流程图大标题','Research Project Template'),('一句副标题','开箱即用的 AI 科研项目目录'),('第一步名称','paper/'),('这一步做什么、怎么做','Elsevier LaTeX 论文与投稿图'),('第二步名称','src/ + scripts/'),('第三步名称','data/'),('第四步名称','results/'),('第五步名称','AGENTS.md'),('底部一句话总结','目录先规范，AI 才知道文件应该放在哪里')])
rep('flow.html','images/04_ai_git.html', [('流程图大标题','以后直接对 AI 说人话'),('一句副标题','Git 操作交给 AI，关键动作由你确认'),('第一步名称','开始工作'),('这一步做什么、怎么做','检查状态并 Pull 最新版本'),('第二步名称','让 AI 修改'),('第三步名称','检查 diff'),('第四步名称','Commit'),('第五步名称','Push'),('底部一句话总结','删除、回滚、强推之前，先让 AI 解释影响')])

# markdown -> simple inline WeChat HTML
md=(BASE/'article.md').read_text(encoding='utf-8')
lines=md.splitlines(); out=[]; incode=False; code=[]
for ln in lines:
    if ln.startswith('# '): continue
    if ln.startswith('```'):
        if incode:
            txt=html.escape('\n'.join(code)); out.append(f'<section style="margin:18px 0;padding:14px 16px;background:#F4F7FB;border-radius:8px;font-family:Consolas,monospace;font-size:13px;line-height:1.65;white-space:pre-wrap;color:#3A3F4B;">{txt}</section>'); code=[]
        incode=not incode; continue
    if incode: code.append(ln); continue
    if ln.startswith('## '): out.append(f'<h2 style="font-size:18px;color:#D4A93C;margin:34px 0 14px;">◆ {html.escape(ln[3:])}</h2>'); continue
    if re.fullmatch(r'\{\{IMG[1-4]\}\}',ln.strip()):
        n=re.search(r'\d',ln).group(); out.append(f'<p style="text-align:center;margin:25px 0;"><img src="{{{{IMG{n}}}}}" style="max-width:100%;border-radius:8px;" /></p>'); continue
    if not ln.strip(): continue
    x=html.escape(ln)
    x=re.sub(r'\*\*(.+?)\*\*',r'<strong style="color:#D4A93C;">\1</strong>',x)
    x=re.sub(r'`(.+?)`',r'<code style="background:#F4F7FB;padding:2px 5px;border-radius:4px;">\1</code>',x)
    out.append(f'<p style="margin:14px 0;">{x}</p>')
body='<section style="font-family:-apple-system,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;font-size:15px;color:#3A3F4B;line-height:1.75;letter-spacing:.5px;padding:10px 5px;">'+''.join(out)+'</section>'
(BASE/'content.html').write_text(body,encoding='utf-8')
print('assets source + content.html ready')
