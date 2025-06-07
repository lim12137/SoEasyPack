# SoEasyPack - Ahead 分支说明

## 🚀 分支特性

这是 SoEasyPack 的 `ahead` 分支，包含了尚未发布到 PyPI 的新功能：

### 🆕 主要新功能

#### 可选瘦身功能 (`enable_slim` 参数)

- **新增参数**: `enable_slim: bool = True`
- **作用范围**: 仅在 `pack_mode=1`（普通模式）时有效
- **默认行为**: 保持向后兼容，默认启用瘦身
- **新功能**: 可以通过 `enable_slim=False` 禁用瘦身，提高打包速度

```python
# 启用瘦身（默认行为）
to_pack(main_py_path, save_dir, pack_mode=1, enable_slim=True)

# 禁用瘦身（新功能 - 更快的打包速度）
to_pack(main_py_path, save_dir, pack_mode=1, enable_slim=False)
```

## 📦 如何安装此版本

### 方法1：直接从 GitHub 安装（推荐）

```bash
# 卸载原版本
pip uninstall soeasypack -y

# 安装 ahead 分支版本
pip install git+https://github.com/lim12137/SoEasyPack.git@ahead
```

### 方法2：使用自动安装脚本

```bash
# 下载并运行安装脚本
python install_modified_version.py
```

### 方法3：本地开发安装

```bash
git clone https://github.com/lim12137/SoEasyPack.git
cd SoEasyPack
git checkout ahead
pip install -e .
```

## 📚 文档和指南

本分支包含完整的使用文档：

| 文件 | 说明 |
|------|------|
| `快速入门.md` | 5分钟快速上手指南 |
| `使用指南.md` | 详细的功能介绍和使用方法 |
| `安装修改版本指南.md` | 如何安装和使用此修改版本 |
| `快速安装命令.md` | 一键安装命令 |
| `examples/basic_usage.py` | 完整的代码示例 |
| `install_modified_version.py` | 自动安装脚本 |

## 🧪 测试和验证

### 验证安装

```python
from soeasypack import to_pack
import inspect

# 检查新参数是否可用
sig = inspect.signature(to_pack)
if 'enable_slim' in sig.parameters:
    print("✅ 安装成功！支持 enable_slim 参数")
    print(f"默认值: {sig.parameters['enable_slim'].default}")
else:
    print("❌ 安装的是原版本")
```

### 运行测试

```bash
# 运行单元测试
python -m pytest test/test_enable_slim.py -v

# 运行验证脚本
python test/verify_changes.py
```

## 🔄 与主分支的差异

### 代码变更

1. **soeasypack/core/easy_pack.py**
   - 添加 `enable_slim: bool = True` 参数
   - 修改瘦身逻辑：`if pack_mode == 1 and enable_slim:`
   - 更新函数文档说明

2. **README.md**
   - 添加新参数的使用示例
   - 更新普通模式的描述

### 新增文件

- 完整的测试套件 (`test/`)
- 详细的使用文档和指南
- 代码示例和安装脚本
- `.gitignore` 文件

## 🎯 使用场景

### 何时使用 `enable_slim=False`

- ✅ 需要快速打包，不在意体积
- ✅ 调试阶段，频繁打包测试
- ✅ 确定所有依赖都是必需的
- ✅ 网络环境差，不想等待瘦身分析

### 何时使用 `enable_slim=True`（默认）

- ✅ 生产环境打包
- ✅ 需要最小体积
- ✅ 虚拟环境中有很多无用包
- ✅ 分发给最终用户

## ⚠️ 注意事项

1. **系统要求**: 仅支持 Windows 系统
2. **权限要求**: 建议以管理员身份运行
3. **Git 依赖**: 从 GitHub 安装需要 Git
4. **兼容性**: 完全向后兼容，现有代码无需修改

## 🔮 未来计划

- [ ] 发布到 PyPI（等待主分支合并）
- [ ] 添加更多打包选项
- [ ] 优化瘦身算法
- [ ] 支持更多 Python 版本

## 🤝 贡献

如果您发现问题或有改进建议：

1. 在此分支上创建 Issue
2. 提交 Pull Request 到 `ahead` 分支
3. 参与讨论和测试

## 📞 支持

如果在使用过程中遇到问题：

1. 查看相关文档和指南
2. 运行 `python test/verify_changes.py` 验证安装
3. 检查是否在 Windows 环境下运行
4. 确认以管理员身份运行

---

**感谢使用 SoEasyPack ahead 分支！您的反馈对我们很重要。**
