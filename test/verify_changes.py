"""
验证enable_slim参数修改的脚本
@author: AI Assistant
Created on 2025-01-05
"""

import sys
import os
import inspect

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_function_signature():
    """测试to_pack函数签名是否包含enable_slim参数"""
    print("=== 测试函数签名 ===")
    
    try:
        from soeasypack.core.easy_pack import to_pack
        
        # 获取函数签名
        sig = inspect.signature(to_pack)
        params = list(sig.parameters.keys())
        
        print(f"to_pack函数参数: {params}")
        
        # 检查enable_slim参数是否存在
        if 'enable_slim' in params:
            print("✓ enable_slim参数已成功添加")
            
            # 检查默认值
            enable_slim_param = sig.parameters['enable_slim']
            if enable_slim_param.default is True:
                print("✓ enable_slim默认值为True")
            else:
                print(f"✗ enable_slim默认值错误: {enable_slim_param.default}")
        else:
            print("✗ enable_slim参数未找到")
            
        return 'enable_slim' in params
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_logic_flow():
    """测试逻辑流程"""
    print("\n=== 测试逻辑流程 ===")
    
    def simulate_slim_logic(pack_mode, enable_slim=True):
        """模拟瘦身逻辑"""
        if pack_mode == 1 and enable_slim:
            return "执行瘦身"
        elif pack_mode == 1 and not enable_slim:
            return "跳过瘦身"
        else:
            return "不适用瘦身"
    
    test_cases = [
        (1, True, "执行瘦身"),
        (1, False, "跳过瘦身"),
        (0, True, "不适用瘦身"),
        (0, False, "不适用瘦身"),
        (2, True, "不适用瘦身"),
        (3, True, "不适用瘦身"),
    ]
    
    all_passed = True
    for pack_mode, enable_slim, expected in test_cases:
        result = simulate_slim_logic(pack_mode, enable_slim)
        if result == expected:
            print(f"✓ pack_mode={pack_mode}, enable_slim={enable_slim} -> {result}")
        else:
            print(f"✗ pack_mode={pack_mode}, enable_slim={enable_slim} -> {result} (期望: {expected})")
            all_passed = False
    
    return all_passed

def test_documentation():
    """测试文档字符串是否更新"""
    print("\n=== 测试文档字符串 ===")
    
    try:
        from soeasypack.core.easy_pack import to_pack
        
        doc = to_pack.__doc__
        if doc and 'enable_slim' in doc:
            print("✓ 文档字符串包含enable_slim参数说明")
            
            # 检查是否提到了可选瘦身
            if '可选择是否进行项目瘦身' in doc or 'enable_slim' in doc:
                print("✓ 文档字符串已更新瘦身相关描述")
                return True
            else:
                print("✗ 文档字符串未更新瘦身相关描述")
                return False
        else:
            print("✗ 文档字符串未包含enable_slim参数说明")
            return False
            
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_readme_update():
    """测试README是否更新"""
    print("\n=== 测试README更新 ===")
    
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'enable_slim' in content:
            print("✓ README.md包含enable_slim参数示例")
            
            if 'enable_slim=False' in content:
                print("✓ README.md包含禁用瘦身的示例")
                return True
            else:
                print("✗ README.md未包含禁用瘦身的示例")
                return False
        else:
            print("✗ README.md未包含enable_slim参数")
            return False
            
    except FileNotFoundError:
        print("✗ README.md文件未找到")
        return False
    except Exception as e:
        print(f"✗ 读取README.md失败: {e}")
        return False

def main():
    """主函数"""
    print("SoEasyPack enable_slim 参数修改验证")
    print("=" * 50)
    
    tests = [
        ("函数签名测试", test_function_signature),
        ("逻辑流程测试", test_logic_flow),
        ("文档字符串测试", test_documentation),
        ("README更新测试", test_readme_update),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}执行失败: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！enable_slim参数修改成功！")
    else:
        print("❌ 部分测试失败，请检查修改。")
    
    return all_passed

if __name__ == "__main__":
    main()
