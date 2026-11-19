# 建筑拆解与构件再用数据

主子方向为数仓与数据湖。材料再用团队把试拆与现场测量、材料复检、装配记录和接收方的尺寸要求转成可交接的数据。初始数据可用一层虚构建筑拆出的门套、格栅、石材和梁段，配合人工测量表和加工记录。

这是可运行的最小数据基线，只实现下表列明的能力。尺寸、试拆和检测清单为合成数据。可用长度和检测关系供数据核对，不等于构件安全认证。

| 数据链 | 基线能力 | 离线样例 | 可核验结果 |
|---|---|---|---|
| `assembly-origin` | 区分原装构件、可用替代候选和没有位置证据的拆出件。 | [输入](examples/assembly-origin.json) | [结果](tests/expected/assembly-origin.json) |
| `clear-lengths` | 从构件轴向范围扣除已知损伤和未测范围，交付确认连续可用的长度。 | [输入](examples/clear-lengths.json) | [结果](tests/expected/clear-lengths.json) |
| `trial-recovery` | 分固定方式和位置计算试拆完整率，对无试拆分组不作外推。 | [输入](examples/trial-recovery.json) | [结果](tests/expected/trial-recovery.json) |
| `layer-certificates` | 只把材质检测结论附给取样构件的对应层材。 | [输入](examples/layer-certificates.json) | [结果](tests/expected/layer-certificates.json) |
| `grille-pairing` | 将可相接且侧面做法相同的左右格栅配对，不重复使用构件。 | [输入](examples/grille-pairing.json) | [结果](tests/expected/grille-pairing.json) |

## 运行

在仓库根目录使用 Python 3.11 及以上版本，无需安装运行依赖：

```sh
python3 -m architectural_salvage_evidence assembly-origin examples/assembly-origin.json
python3 -m architectural_salvage_evidence assembly-origin examples/assembly-origin.json --sqlite facts.sqlite
python3 -m unittest discover -s tests -v
```

每个输入文件包含 `records` 数组，记录的 `id` 在批内唯一。各数据链校验自己的业务字段，输出按 `fact_id` 标识的事实。起止范围若无另行说明均为左闭右开；日期、深度、金额和持续时间等单位由字段标明。

加上 `--sqlite` 时，`runs` 表保存规范化的来源 JSON 与 SHA-256，`facts` 表保存同一批次的事实。原样重放不新增事实；写入失败回滚整批。既有数据库不会被自动改写为不同版本的处理结果。JSON 接口和入库只是数据处理的运行入口，不是仓库的业务主体。
