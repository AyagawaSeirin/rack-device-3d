# 仓库归档与打开方法

本目录完整归档了本次Dell C6420制作资料：v002为最终写实重做；v001为已被用户退回的历史版本。原始任务见ORIGINAL-TASK-PROMPT.md。最终正面为24个正常2.5英寸热插拔硬盘托架，4个C6420节点、双2400W电源。

## 打开交付

- [可编辑Blender模型](v002/model/DELL-PowerEdge-C6420-4N-24SFF.blend)
- [GLB模型](v002/model/DELL-PowerEdge-C6420-4N-24SFF.glb)
- [多角度预览、实拍对照与旋转记录](v002/REVIEW.html)
- [质量检查和限制](v002/QA.md)
- [来源索引](v002/sources.csv)

大型.blend、.blend备份、.glb及.exr文件由本目录的.gitattributes通过Git LFS管理。克隆后在仓库执行：

```bash
git lfs install --local
git lfs pull
```

应打开拉取后的真实二进制模型，不能把Git LFS指针文本当模型。正常主文件约89MiB，GLB约56MiB。主.blend已打包使用中的纹理，可以直接从当前目录打开。

## 迁移记录与复现

原工作目录/root/Blender/DELL-C6420保持原样作为工作台副本。MIGRATION-MANIFEST.json逐文件保存原始SHA256和仓库SHA256，标记为迁移所做的文本适配。几何模型、原图、PDF、生图原始提示词、生成结果及历史QA数据均保留原始字节。

v002/scripts中的外部Python脚本已将旧项目绝对路径改为/root/Project/rack-device-3d/Dell-C6420-2.5inch。用这些外部脚本复现时先读v002/REPRODUCE.md；完整重建会清空当前Blender数据，必须先保存正在编辑的作品。

历史QA、生成来源、旧版脚本和.blend内的归档Text脚本可能仍记录工作台绝对路径，这是历史执行证据，不代表资产遗漏。运行时优先使用仓库中的外部v002/scripts；如克隆到不同路径，先统一修改项目根路径，再执行。MCP/桌面调用仍依赖本服务器的/root/Blender/README.md所述环境，环境调用器和Codex配置不属于模型资产，不复制凭据或整套运行环境。

本目录既有的被.gitignore忽略的node_modules、虚拟环境和其他旧工具缓存未纳入本次提交；本次完整制作项目位于v001/v002。仓库中无关的未提交文件不在此归档范围内。

GitHub大型文件规则：[官方说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。
