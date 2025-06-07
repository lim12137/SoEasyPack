"""
SoEasyPack 基本使用示例
这个脚本展示了如何使用 SoEasyPack 打包 Python 项目

使用前请确保：
1. 已安装 SoEasyPack: pip install soeasypack
2. 在 Windows 系统上运行
3. 以管理员身份运行（推荐）
"""

import os
import tempfile
from pathlib import Path

# 注意：在实际使用时取消注释下面这行
# from soeasypack import to_pack

def create_sample_project():
    """创建一个示例项目用于演示"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "sample_project"
    project_dir.mkdir(exist_ok=True)
    
    # 创建主程序文件
    main_py = project_dir / "main.py"
    main_py.write_text('''
import os
import sys
import json
from datetime import datetime

def main():
    print("=" * 50)
    print("欢迎使用 SoEasyPack 打包的程序！")
    print("=" * 50)
    
    # 显示系统信息
    print(f"Python 版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 简单的功能演示
    data = {
        "name": "SoEasyPack Demo",
        "version": "1.0.0",
        "features": ["快速打包", "体积小", "依赖精确"]
    }
    
    print("\\n程序功能演示:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    # 用户交互
    print("\\n请输入你的名字:")
    try:
        name = input("> ")
        print(f"\\n你好, {name}! 感谢使用 SoEasyPack!")
    except:
        print("\\n程序运行完成!")
    
    print("\\n按任意键退出...")
    try:
        input()
    except:
        pass

if __name__ == "__main__":
    main()
''', encoding='utf-8')
    
    # 创建 requirements.txt（用于轻量模式）
    requirements_txt = project_dir / "requirements.txt"
    requirements_txt.write_text("# 这个示例项目没有外部依赖\\n# 实际项目中在这里列出你的依赖包\\n")
    
    return str(project_dir), str(main_py)

def example_quick_pack():
    """示例1: 快速打包模式（推荐新手）"""
    print("\\n" + "="*60)
    print("示例1: 快速打包模式")
    print("="*60)
    
    project_dir, main_py_path = create_sample_project()
    output_dir = os.path.join(project_dir, "dist_quick")
    
    print(f"项目目录: {project_dir}")
    print(f"主程序: {main_py_path}")
    print(f"输出目录: {output_dir}")
    
    # 打包参数
    pack_config = {
        'main_py_path': main_py_path,
        'save_dir': output_dir,
        'exe_name': 'QuickDemo',
        'pack_mode': 0,          # 快速模式
        'hide_cmd': False,       # 显示控制台（便于调试）
        'monitoring_time': 15,   # 监控时间15秒
    }
    
    print("\\n打包配置:")
    for key, value in pack_config.items():
        print(f"  {key}: {value}")
    
    print("\\n开始打包...")
    print("注意: 实际使用时需要取消注释 to_pack 调用")
    
    # 实际打包调用（示例中注释掉）
    # try:
    #     to_pack(**pack_config)
    #     print(f"✓ 快速打包完成！")
    #     print(f"  可执行文件: {output_dir}\\\\{pack_config['exe_name']}.exe")
    # except Exception as e:
    #     print(f"✗ 打包失败: {e}")
    
    return project_dir, pack_config

def example_normal_pack_with_slim():
    """示例2: 普通模式 + 启用瘦身"""
    print("\\n" + "="*60)
    print("示例2: 普通模式 + 启用瘦身")
    print("="*60)
    
    project_dir, main_py_path = create_sample_project()
    output_dir = os.path.join(project_dir, "dist_normal_slim")
    
    pack_config = {
        'main_py_path': main_py_path,
        'save_dir': output_dir,
        'exe_name': 'NormalSlimDemo',
        'pack_mode': 1,          # 普通模式
        'enable_slim': True,     # 启用瘦身（默认）
        'hide_cmd': False,
        'monitoring_time': 20,
        'auto_py_pyc': True,     # 转换为pyc
        'pyc_optimize': 1,       # 优化级别
    }
    
    print(f"项目目录: {project_dir}")
    print(f"输出目录: {output_dir}")
    print("\\n打包配置:")
    for key, value in pack_config.items():
        print(f"  {key}: {value}")
    
    print("\\n特点:")
    print("  - 复制完整Python环境")
    print("  - 启用项目瘦身，移除无用文件")
    print("  - 适合虚拟环境使用")
    
    # 实际打包调用（示例中注释掉）
    # try:
    #     to_pack(**pack_config)
    #     print(f"✓ 普通模式打包完成！")
    # except Exception as e:
    #     print(f"✗ 打包失败: {e}")
    
    return project_dir, pack_config

def example_normal_pack_without_slim():
    """示例3: 普通模式 + 禁用瘦身"""
    print("\\n" + "="*60)
    print("示例3: 普通模式 + 禁用瘦身")
    print("="*60)
    
    project_dir, main_py_path = create_sample_project()
    output_dir = os.path.join(project_dir, "dist_normal_no_slim")
    
    pack_config = {
        'main_py_path': main_py_path,
        'save_dir': output_dir,
        'exe_name': 'NormalNoSlimDemo',
        'pack_mode': 1,          # 普通模式
        'enable_slim': False,    # 禁用瘦身
        'hide_cmd': False,
        'monitoring_time': 20,
    }
    
    print(f"项目目录: {project_dir}")
    print(f"输出目录: {output_dir}")
    print("\\n打包配置:")
    for key, value in pack_config.items():
        print(f"  {key}: {value}")
    
    print("\\n特点:")
    print("  - 复制完整Python环境")
    print("  - 禁用项目瘦身，保留所有文件")
    print("  - 打包速度更快，但体积较大")
    
    return project_dir, pack_config

def main():
    """主函数"""
    print("SoEasyPack 使用示例")
    print("="*60)
    print("本示例展示了 SoEasyPack 的各种打包模式")
    print("注意: 实际打包需要在 Windows 系统上运行")
    print("="*60)
    
    examples = [
        ("快速打包模式", example_quick_pack),
        ("普通模式+启用瘦身", example_normal_pack_with_slim),
        ("普通模式+禁用瘦身", example_normal_pack_without_slim),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\\n✗ {name} 示例执行失败: {e}")
    
    print("\\n" + "="*60)
    print("所有示例展示完成！")
    print("\\n要实际使用 SoEasyPack，请:")
    print("1. 取消注释 'from soeasypack import to_pack'")
    print("2. 取消注释各个示例中的 to_pack() 调用")
    print("3. 在 Windows 系统上以管理员身份运行")
    print("="*60)

if __name__ == "__main__":
    main()
