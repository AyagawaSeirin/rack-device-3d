# Cisco N9K-C9336C-FX2 独立建模会话入口

本次交付是**可独立执行的完整建模提示词、Dell经验总结和官方资料核验入口**。此目录尚未开始Cisco模型制作，没有把提示词或资料链接当成已生成模型。

在新会话发送：

```text
请完整阅读并执行：
/root/Project/rack-device-3d/Cisco-N9KC9336C-FX2/TASK-PROMPT.md

目标固定为Cisco Nexus N9K-C9336C-FX2完整交换机。按写实风格实际完成资料下载、官方尺寸核验、imagegen全部参考、Blender MCP与桌面协同建模、检查修复、导出、归档、提交和推送。重点检查左右挂耳真开孔、孔壁厚度、金属不透明、文字和UV镜像、旋转闪烁与GLB重导入。不要再次改写提示词或只给方案，现在开始。
```

也可以将[TASK-PROMPT.md](TASK-PROMPT.md)全文直接粘贴到新会话。它已包含完整目标、操作环境、资料入口、建模与质量标准、超时恢复、路径规范及Git授权，不需要该会话知道之前的Dell聊天记录。

- [完整任务提示词](TASK-PROMPT.md)
- [本次Dell建模经验与踩坑总结](LESSONS-FROM-DELL.md)
- [Cisco官方事实与资料访问状态](SOURCE-SEED.md)
- [资料入口机器可读索引](source-seed/index.json)

型号规范PID为N9K-C9336C-FX2；目录按用户指定使用Cisco-N9KC9336C-FX2。后续模型放本目录的新版本子目录，保留本次提示词资料。当前.gitattributes已限定在本设备目录管理大型模型文件的Git LFS属性。
