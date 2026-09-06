# 编辑与复现

建议直接打开model/DELL-PowerEdge-C6420-4N-24SFF.blend。最终网格可以独立编辑，24盘架/4节点/2PSU各有父级；重复部件共享网格以减小文件，单独修改时使用Object → Relations → Make Single User。主要结构已经应用小倒角、实体厚度和法线修正，保留的是可编辑实网格。托架拉手有父级和铰链位置元数据，未交付动作动画。

所有建模修改均在原有GUI Blender 4.0.2中通过Blender MCP执行。桌面观察通过server_desktop MCP实际鼠标/键盘输入完成。后台Blender只做独立预览/QA渲染。CPU，Cycles关闭use_denoising及use_preview_denoising。

scripts目录为本轮实际执行的参数化脚本和QA脚本。若需要完全重建，先复制整个v002目录为新的版本，并把脚本常量P改到该副本。请先保存当前Blender文件：stage1会清空当前数据，不能在其他未保存作品中直接运行。原始v001/v002历史文件不要覆盖。

按以下顺序通过MCP分段运行，每段完成后再继续，不要在MCP超时后盲目重发创建指令：

1. 在终端运行procedural_pbr_maps.py和refined_pbr_maps.py生成确定性PBR数据，依赖Python3、numpy、Pillow。目录已经附带纹理，可跳过重算。
2. 在Blender中建立独立字典ns，exec(build_c6420_v2.py, ns)，将ns保存到bpy.app.driver_namespace['C6420_V2']；依次运行ns['stage1']()、ns['stage2']()。
3. 执行studio_v2.py、refine_studio_materials.py。向ns加载rear_v2.py并调用stage3_nodes；加载normal_carriers_v2.py并调用replace_front_with_normal_carriers。这个历史替换步骤移除stage2的旧填充件并生成24个最终正常盘架。
4. 向ns加载psu_and_labels_v2.py并调用stage4_psu_labels；加载finish_external_v2.py并调用finish_external。
5. 独立执行prepare_geometry_v2.py；向ns加载material_review_v2.py并调用review_materials；独立执行finalize_mesh_v2.py、clear_real_labels_v2.py、repair_label_uv_v2.py。repair_label_uv_v2.py修复Blender UV层删除导致引用失效的问题，不能省略；随后执行repair_cheek_normals_v2.py修正前部金属孔板的平面法线。
6. 执行audit_scene.py、audit_orientation_v2.py、audit_reimport_geometry.py；运行export_deliverables.py。最终导出排除90_STUDIO和相机灯光。
7. 运行reimport_glb.py，在独立场景重新导入GLB，重复方向和几何检查。用render_v2.py / render_glb_check.py在后台生成预览，不用于创建模型。

MCP调用协议脚本与server_desktop参数见/root/Blender/README.md。不要硬编码DISPLAY，也不要创建新的远程桌面实例。脚本内数据量较大，在软件OpenGL下应先切Solid再保存/修改；Material Preview使用Scene World及Scene Lights，避免默认暗HDR环境令金属呈现过暗效果。

第一次参考生成和后续纠错均实际使用内置imagegen，提示词、输入照片和产物来源见references/manifest.json、prompts、provenance。AI参考不是精确CAD；最终尺寸取自DIMENSIONS.md中的官方毫米值，底面和部分隐蔽细节为推测。
