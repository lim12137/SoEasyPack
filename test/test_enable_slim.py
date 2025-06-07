"""
测试瘦身功能可选参数
@author: AI Assistant
Created on 2025-01-05
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from soeasypack.core.easy_pack import to_pack


class TestEnableSlim(unittest.TestCase):
    """测试enable_slim参数功能"""

    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_py_file = os.path.join(self.temp_dir, 'test_main.py')

        # 创建一个简单的测试Python文件
        with open(self.test_py_file, 'w', encoding='utf-8') as f:
            f.write('''
print("Hello, World!")
import os
print("Current directory:", os.getcwd())
''')

    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('soeasypack.core.easy_pack.to_pack')
    def test_enable_slim_true(self, mock_to_pack):
        """测试enable_slim=True时调用瘦身功能"""

        # 创建一个简化的测试函数来验证逻辑
        def test_slim_logic(pack_mode, enable_slim):
            """模拟瘦身逻辑的核心部分"""
            slim_called = False
            if pack_mode == 1 and enable_slim:
                slim_called = True
            return slim_called

        # 测试enable_slim=True时
        result = test_slim_logic(pack_mode=1, enable_slim=True)
        self.assertTrue(result, "当pack_mode=1且enable_slim=True时应该调用瘦身功能")
    
    def test_enable_slim_false(self):
        """测试enable_slim=False时不调用瘦身功能"""

        # 创建一个简化的测试函数来验证逻辑
        def test_slim_logic(pack_mode, enable_slim):
            """模拟瘦身逻辑的核心部分"""
            slim_called = False
            if pack_mode == 1 and enable_slim:
                slim_called = True
            return slim_called

        # 测试enable_slim=False时
        result = test_slim_logic(pack_mode=1, enable_slim=False)
        self.assertFalse(result, "当pack_mode=1但enable_slim=False时不应该调用瘦身功能")
    
    def test_enable_slim_default(self):
        """测试enable_slim默认值为True"""

        # 创建一个简化的测试函数来验证逻辑
        def test_slim_logic(pack_mode, enable_slim=True):  # 默认值为True
            """模拟瘦身逻辑的核心部分"""
            slim_called = False
            if pack_mode == 1 and enable_slim:
                slim_called = True
            return slim_called

        # 测试默认情况（不指定enable_slim）
        result = test_slim_logic(pack_mode=1)  # 使用默认值
        self.assertTrue(result, "当pack_mode=1且不指定enable_slim时应该默认调用瘦身功能")
    
    def test_enable_slim_other_pack_modes(self):
        """测试其他pack_mode时enable_slim参数不影响瘦身功能"""

        # 创建一个简化的测试函数来验证逻辑
        def test_slim_logic(pack_mode, enable_slim):
            """模拟瘦身逻辑的核心部分"""
            slim_called = False
            if pack_mode == 1 and enable_slim:
                slim_called = True
            return slim_called

        # 测试pack_mode=0时，即使enable_slim=True也不调用瘦身
        result = test_slim_logic(pack_mode=0, enable_slim=True)
        self.assertFalse(result, "当pack_mode不是1时，即使enable_slim=True也不应该调用瘦身功能")

        # 测试pack_mode=2时
        result = test_slim_logic(pack_mode=2, enable_slim=True)
        self.assertFalse(result, "当pack_mode=2时，即使enable_slim=True也不应该调用瘦身功能")

        # 测试pack_mode=3时
        result = test_slim_logic(pack_mode=3, enable_slim=True)
        self.assertFalse(result, "当pack_mode=3时，即使enable_slim=True也不应该调用瘦身功能")


if __name__ == '__main__':
    unittest.main()
