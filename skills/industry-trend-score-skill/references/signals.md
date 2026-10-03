# 当日买卖信号

## 命令

```bash
python scripts/signals.py --config config/strategy.json
```

## 输出约定

- 先用通俗语言说明本策略看什么、如何排序和如何分配资金，再输出信号。
- 信号包含数据日期、当前信号值、目标仓位/动作，并明确标注这是基于最新数据计算，不构成收益承诺。
- 输出当日应持有的行业/基金，并说明持有行业数及各行业的中期强弱评分。
- 本 skill 不生成下单命令。

## 下一步按钮

信号输出后必须继续展示至少 2~4 个可点击按钮，例如：

- `run_default_backtest`｜查看默认回测
- `explain_strategy`｜查看策略详细运行逻辑
- `tune_parameters`｜调整策略参数
- `setup_trade_plan`｜设置交易计划
- `view_latest_signal`｜重新计算最新信号

按钮必须绑定明确 prompt，点击后直接执行，不得只提示“还可以继续”。
