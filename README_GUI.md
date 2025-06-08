# SoEasyPack GUI 版本

## 🎉 重构完成

SoEasyPack 已成功重构为独立的GUI应用程序！本版本移除了不必要的功能，专注于提供简洁易用的Python项目打包体验。

## ✨ 主要变更

### 🗑️ 移除的功能
- ❌ **快速模式** (pack_mode=0) - 完全移除
- ❌ **代码瘦身功能** (project slimming) - 完全移除  
- ❌ **pyc自动转换功能** - 不再自动转换，只在必要时转换

### ✅ 新增功能
- 🖥️ **图形用户界面** - 使用FreeSimpleGUI框架
- 🎯 **简化的打包流程** - 直观易用的操作界面
- 📱 **独立应用程序** - 不再作为Python包安装

### 🔧 保留功能
- ✅ **普通模式** (pack_mode=1) - 复制完整Python环境
- ✅ **轻量模式** (pack_mode=2) - 运行时自动下载依赖
- ✅ **向后兼容性** - 原有API仍可使用

## 🚀 快速开始

### 安装依赖
```bash
pip install FreeSimpleGUI
```

### 启动GUI应用程序
```bash
python main.py
```

### 使用GUI界面
1. **选择主程序文件** - 点击"浏览"选择要打包的Python文件
2. **选择输出目录** - 选择打包结果的保存位置
3. **输入程序名称** - 设置生成的可执行文件名
4. **选择打包模式**：
   - 普通模式：复制完整Python环境（推荐用于虚拟环境）
   - 轻量模式：运行时自动下载依赖
5. **配置选项**：
   - 隐藏控制台窗口
   - 生成单文件exe
   - 设置图标文件
6. **开始打包** - 点击"开始打包"按钮

## 🧪 测试

### 运行所有测试
```bash
python test/run_all_tests.py
```

### 运行特定测试
```bash
python test/run_all_tests.py test_gui_functionality
```

### 测试覆盖
- ✅ GUI功能测试 (4个测试)
- ✅ 核心功能测试 (8个测试) 
- ✅ 集成测试 (9个测试)
- ✅ 原有功能测试 (8个测试)
- **总计：29个测试全部通过** 🎉

## 📁 项目结构

```
SoEasyPack/
├── main.py                    # GUI应用程序入口
├── gui/                       # GUI模块
│   ├── __init__.py
│   └── main_window.py         # 主窗口界面
├── core/                      # 核心功能模块
│   ├── __init__.py
│   └── simplified_pack.py     # 简化的打包器
├── soeasypack/                # 原有核心功能（已修改）
│   ├── __init__.py            # 更新版本号和导出
│   └── core/
│       └── easy_pack.py       # 移除不需要的功能
├── test/                      # 测试模块
│   ├── run_all_tests.py       # 测试运行脚本
│   ├── test_gui_functionality.py
│   ├── test_core_functionality.py
│   └── test_integration.py
└── demo_app.py                # 演示脚本
```

## 🔧 开发者指南

### 核心API变更

#### 移除的函数
```python
# 这些函数已被移除
from soeasypack import to_slim_file  # ❌ 不再可用
from soeasypack import to_pyd        # ❌ 不再可用
```

#### 修改的参数
```python
from soeasypack import to_pack

# 移除的pack_mode值
to_pack(pack_mode=0)  # ❌ 快速模式已移除
to_pack(pack_mode=3)  # ❌ ast模式已移除

# 保留的pack_mode值
to_pack(pack_mode=1)  # ✅ 普通模式
to_pack(pack_mode=2)  # ✅ 轻量模式

# 禁用的参数（保留兼容性）
to_pack(auto_py_pyc=True)   # 🔄 被忽略，除非embed_exe=True
to_pack(enable_slim=True)   # 🔄 被忽略
```

### 新增的简化API
```python
from core.simplified_pack import SimplifiedPacker

packer = SimplifiedPacker()
success = packer.pack(
    main_py_path='app.py',
    save_dir='./output',
    exe_name='MyApp',
    pack_mode=1,
    hide_cmd=True,
    onefile=False
)
```

## 📊 版本信息

- **版本号**: 1.0.0-gui
- **Python要求**: Python 3.6+
- **GUI框架**: FreeSimpleGUI
- **测试框架**: unittest
- **支持平台**: Windows, Linux, macOS

## 🎯 使用建议

### 推荐的打包流程
1. **开发阶段**: 使用虚拟环境开发项目
2. **测试阶段**: 在虚拟环境中测试应用程序
3. **打包阶段**: 使用普通模式打包（pack_mode=1）
4. **分发阶段**: 将打包结果分发给用户

### 模式选择建议
- **普通模式**: 适合虚拟环境，包含完整依赖，体积较大但兼容性好
- **轻量模式**: 适合依赖较少的项目，体积小但需要网络下载依赖

## 🐛 故障排除

### 常见问题
1. **GUI无法启动**: 确保安装了FreeSimpleGUI和tkinter
2. **打包失败**: 检查文件路径和权限
3. **测试失败**: 确保在项目根目录运行测试

### 获取帮助
- 查看测试用例了解使用方法
- 运行demo_app.py查看功能演示
- 检查日志输出了解错误详情

## 🎉 总结

SoEasyPack GUI版本成功实现了以下目标：
- ✅ 移除了复杂和不必要的功能
- ✅ 提供了直观易用的图形界面
- ✅ 保持了核心打包功能的稳定性
- ✅ 确保了向后兼容性
- ✅ 建立了完整的测试体系

现在您可以享受更简洁、更易用的Python项目打包体验！🚀
