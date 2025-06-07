"""
安装修改版 SoEasyPack 的脚本
支持 enable_slim 参数的版本

使用方法：
python install_modified_version.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}...")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
        else:
            print(f"❌ {description} 失败")
            if result.stderr.strip():
                print(f"错误: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ {description} 出错: {e}")
        return False
    
    return True

def check_git():
    """检查是否安装了 git"""
    try:
        result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git 已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git 未安装")
            return False
    except:
        print("❌ Git 未安装")
        return False

def verify_installation():
    """验证安装是否成功"""
    print("\n🔍 验证安装...")
    
    try:
        # 检查是否能导入
        import soeasypack
        print("✅ 成功导入 soeasypack")
        
        # 检查版本信息
        if hasattr(soeasypack, '__version__'):
            print(f"📦 版本: {soeasypack.__version__}")
        
        # 检查 enable_slim 参数
        from soeasypack import to_pack
        import inspect
        
        sig = inspect.signature(to_pack)
        if 'enable_slim' in sig.parameters:
            default_value = sig.parameters['enable_slim'].default
            print(f"✅ enable_slim 参数可用，默认值: {default_value}")
            return True
        else:
            print("❌ enable_slim 参数不可用")
            return False
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 验证出错: {e}")
        return False

def install_from_github():
    """从 GitHub 安装修改版本"""
    print("=" * 60)
    print("🚀 安装修改版 SoEasyPack")
    print("=" * 60)
    
    # 检查 git
    if not check_git():
        print("\n❌ 需要先安装 Git")
        print("请访问 https://git-scm.com/download/win 下载安装")
        return False
    
    # 卸载原版本
    if not run_command("pip uninstall soeasypack -y", "卸载原版本"):
        print("⚠️ 卸载失败，可能原本就没有安装")
    
    # 安装修改版本
    github_url = "git+https://github.com/lim12137/SoEasyPack.git@ahead"
    if not run_command(f"pip install {github_url}", "安装修改版本"):
        return False
    
    # 验证安装
    return verify_installation()

def install_dependencies():
    """安装可能缺失的依赖"""
    print("\n🔧 安装依赖包...")
    
    dependencies = ["Cython", "objectgraph"]
    
    for dep in dependencies:
        run_command(f"pip install {dep}", f"安装 {dep}")

def create_test_script():
    """创建测试脚本"""
    test_script = """
# test_soeasypack.py - 测试修改版 SoEasyPack
from soeasypack import to_pack
import tempfile
import os

def test_new_feature():
    print("🧪 测试 enable_slim 参数...")
    
    # 创建临时测试文件
    temp_dir = tempfile.mkdtemp()
    test_py = os.path.join(temp_dir, 'test.py')
    
    with open(test_py, 'w', encoding='utf-8') as f:
        f.write('''
print("Hello from SoEasyPack!")
import os
print(f"当前目录: {os.getcwd()}")
''')
    
    output_dir = os.path.join(temp_dir, 'output')
    
    print(f"测试文件: {test_py}")
    print(f"输出目录: {output_dir}")
    
    # 注意：实际打包需要在 Windows 环境下运行
    print("\\n可用的打包命令:")
    print("# 启用瘦身（默认）")
    print(f"to_pack('{test_py}', '{output_dir}', pack_mode=1, enable_slim=True)")
    
    print("\\n# 禁用瘦身（新功能）")
    print(f"to_pack('{test_py}', '{output_dir}', pack_mode=1, enable_slim=False)")
    
    print("\\n✅ 参数测试完成！")
    print("注意：实际打包需要在 Windows 系统上以管理员身份运行")

if __name__ == "__main__":
    test_new_feature()
"""
    
    with open("test_soeasypack.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ 已创建测试脚本: test_soeasypack.py")

def main():
    """主函数"""
    print("SoEasyPack 修改版安装工具")
    print("支持 enable_slim 可选瘦身参数")
    print("=" * 60)
    
    # 显示系统信息
    print(f"Python 版本: {sys.version}")
    print(f"操作系统: {os.name}")
    
    # 安装依赖
    install_dependencies()
    
    # 从 GitHub 安装
    if install_from_github():
        print("\n🎉 安装成功！")
        
        # 创建测试脚本
        create_test_script()
        
        print("\n📋 使用说明:")
        print("1. 运行 'python test_soeasypack.py' 测试功能")
        print("2. 在您的项目中使用新的 enable_slim 参数:")
        print("   to_pack(main_py_path, save_dir, pack_mode=1, enable_slim=False)")
        print("3. 注意：实际打包需要在 Windows 系统上运行")
        
    else:
        print("\n❌ 安装失败")
        print("\n🔧 手动安装方法:")
        print("1. 确保安装了 Git")
        print("2. 运行: pip uninstall soeasypack -y")
        print("3. 运行: pip install git+https://github.com/lim12137/SoEasyPack.git@ahead")

if __name__ == "__main__":
    main()
