#!/bin/bash
# 用 Edge/Chrome 无头模式把 HTML 模板渲染成 2 倍清晰度 PNG。
# 用法: bash render_images.sh 宽x高 输入.html 输出.png [宽x高 输入2.html 输出2.png ...]
# 例:  bash render_images.sh 900x383 cover.html cover.png 1080x660 compare.html compare.png
set -e

EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
[ -f "$EDGE" ] || EDGE="/c/Program Files/Google/Chrome/Application/chrome.exe"
[ -f "$EDGE" ] || { echo "未找到 Edge 或 Chrome"; exit 1; }

if [ $# -lt 3 ] || [ $(($# % 3)) -ne 0 ]; then
  echo "用法: bash render_images.sh 宽x高 输入.html 输出.png [可重复多组]"
  exit 1
fi

while [ $# -ge 3 ]; do
  SIZE="$1"; HTML_IN="$2"; PNG_OUT="$3"; shift 3
  W="${SIZE%x*}"; H="${SIZE#*x}"
  ABS_HTML="$(cd "$(dirname "$HTML_IN")" && pwd)/$(basename "$HTML_IN")"
  ABS_PNG="$(cd "$(dirname "$PNG_OUT")" && pwd)/$(basename "$PNG_OUT")"
  MIX_HTML=$(cygpath -m "$ABS_HTML" 2>/dev/null || echo "$ABS_HTML")
  WIN_PNG=$(cygpath -w "$ABS_PNG" 2>/dev/null || echo "$ABS_PNG")
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size="$W,$H" \
    --screenshot="$WIN_PNG" "file:///$MIX_HTML"
  [ -f "$ABS_PNG" ] || { echo "渲染失败: $ABS_PNG"; exit 1; }
  echo "已生成: $ABS_PNG (${W}x${H} @2x)"
done

echo "全部完成，请肉眼检查 PNG 效果。"
