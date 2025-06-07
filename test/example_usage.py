"""
演示enable_slim参数的使用示例
@author: AI Assistant
Created on 2025-01-05
"""

import os
import tempfile
# from soeasypack import to_pack  # 注释掉，仅用于演示

def create_sample_project():
    """创建一个示例项目"""
    temp_dir = tempfile.mkdtemp()
    main_py_path = os.path.join(temp_dir, 'main.py')
    
    # 创建一个简单的Python项目
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write('''
import os
import sys

def main():
    print("Hello from SoEasyPack!")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # 简单的计算
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    print(f"Sum of {numbers} = {total}")

if __name__ == "__main__":
    main()
''')
    
    return temp_dir, main_py_path

def example_with_slim():
    """示例：启用瘦身功能的打包"""
    print("=== 示例1：启用瘦身功能的打包 ===")
    
    temp_dir, main_py_path = create_sample_project()
    save_dir = os.path.join(temp_dir, 'output_with_slim')
    
    print(f"项目路径: {main_py_path}")
    print(f"输出路径: {save_dir}")
    print("打包模式: pack_mode=1, enable_slim=True (默认)")
    
    # 注意：这里只是演示参数，实际运行需要Windows环境和相关依赖
    print("调用: to_pack(main_py_path, save_dir, pack_mode=1, enable_slim=True)")
    print("结果: 将会执行项目瘦身，移除不必要的文件")
    
    return temp_dir, main_py_path, save_dir

def example_without_slim():
    """示例：禁用瘦身功能的打包"""
    print("\n=== 示例2：禁用瘦身功能的打包 ===")
    
    temp_dir, main_py_path = create_sample_project()
    save_dir = os.path.join(temp_dir, 'output_without_slim')
    
    print(f"项目路径: {main_py_path}")
    print(f"输出路径: {save_dir}")
    print("打包模式: pack_mode=1, enable_slim=False")
    
    # 注意：这里只是演示参数，实际运行需要Windows环境和相关依赖
    print("调用: to_pack(main_py_path, save_dir, pack_mode=1, enable_slim=False)")
    print("结果: 将跳过项目瘦身步骤，保留所有复制的文件")
    
    return temp_dir, main_py_path, save_dir

def example_other_modes():
    """示例：其他打包模式"""
    print("\n=== 示例3：其他打包模式 ===")
    
    temp_dir, main_py_path = create_sample_project()
    
    print(f"项目路径: {main_py_path}")
    
    # 快速打包模式
    save_dir_fast = os.path.join(temp_dir, 'output_fast')
    print(f"\n快速打包模式 (pack_mode=0):")
    print(f"输出路径: {save_dir_fast}")
    print("调用: to_pack(main_py_path, save_dir, pack_mode=0)")
    print("结果: 快速打包，不执行瘦身（无论enable_slim设置如何）")
    
    # 轻量模式
    save_dir_light = os.path.join(temp_dir, 'output_light')
    print(f"\n轻量模式 (pack_mode=2):")
    print(f"输出路径: {save_dir_light}")
    print("调用: to_pack(main_py_path, save_dir, pack_mode=2, requirements_path='requirements.txt')")
    print("结果: 轻量打包，不执行瘦身（无论enable_slim设置如何）")
    
    return temp_dir, main_py_path

def main():
    """主函数"""
    print("SoEasyPack enable_slim 参数使用示例")
    print("=" * 50)
    
    try:
        # 示例1：启用瘦身
        example_with_slim()
        
        # 示例2：禁用瘦身
        example_without_slim()
        
        # 示例3：其他模式
        example_other_modes()
        
        print("\n=== 总结 ===")
        print("1. enable_slim 参数只在 pack_mode=1 时有效")
        print("2. enable_slim=True (默认): 执行项目瘦身")
        print("3. enable_slim=False: 跳过项目瘦身")
        print("4. 其他 pack_mode (0,2,3) 不受 enable_slim 影响")
        print("\n注意：以上示例仅演示参数使用，实际打包需要Windows环境")
        
    except Exception as e:
        print(f"示例运行出错: {e}")

if __name__ == "__main__":
    main()
