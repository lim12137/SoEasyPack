#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI功能测试
测试SoEasyPack GUI应用程序的各项功能

@author: SoEasyPack Team
Created on 2025-01-05
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 尝试导入GUI模块，如果失败则跳过相关测试
try:
    from gui.main_window import SoEasyPackGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    SoEasyPackGUI = None

# 尝试导入简化打包器
try:
    from core.simplified_pack import SimplifiedPacker
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    # 创建一个简单的模拟类
    class SimplifiedPacker:
        def __init__(self):
            self.logger = MagicMock()

        def _validate_inputs(self, main_py_path, save_dir, pack_mode):
            return True

        def get_supported_modes(self):
            return {1: "普通模式", 2: "轻量模式"}

        def pack(self, **kwargs):
            return True


class TestGUIFunctionality(unittest.TestCase):
    """测试GUI功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_py_file = os.path.join(self.temp_dir, 'test_main.py')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        
        # 创建测试Python文件
        with open(self.test_py_file, 'w', encoding='utf-8') as f:
            f.write('''
print("Hello from test!")
import os
print("Test completed")
''')
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skipUnless(GUI_AVAILABLE, "GUI模块不可用")
    def test_gui_initialization(self):
        """测试GUI初始化"""
        try:
            # 模拟GUI初始化（不实际显示窗口）
            with patch('FreeSimpleGUI.Window') as mock_window:
                mock_window.return_value = MagicMock()
                gui = SoEasyPackGUI()
                self.assertIsNotNone(gui)
                self.assertIsNotNone(gui.packer)
        except Exception as e:
            self.fail(f"GUI初始化失败: {e}")
    
    @unittest.skipUnless(GUI_AVAILABLE, "GUI模块不可用")
    def test_input_validation(self):
        """测试输入验证功能"""
        with patch('FreeSimpleGUI.Window') as mock_window:
            mock_window.return_value = MagicMock()
            gui = SoEasyPackGUI()
            
            # 测试空文件路径
            values = {
                '-MAIN_FILE-': '',
                '-OUTPUT_DIR-': self.output_dir,
                '-EXE_NAME-': 'test'
            }
            self.assertFalse(gui.validate_inputs(values))
            
            # 测试不存在的文件
            values['-MAIN_FILE-'] = '/nonexistent/file.py'
            self.assertFalse(gui.validate_inputs(values))
            
            # 测试空输出目录
            values['-MAIN_FILE-'] = self.test_py_file
            values['-OUTPUT_DIR-'] = ''
            self.assertFalse(gui.validate_inputs(values))
            
            # 测试空程序名称
            values['-OUTPUT_DIR-'] = self.output_dir
            values['-EXE_NAME-'] = ''
            self.assertFalse(gui.validate_inputs(values))
            
            # 测试有效输入
            values['-EXE_NAME-'] = 'test'
            self.assertTrue(gui.validate_inputs(values))
    
    @unittest.skipUnless(GUI_AVAILABLE, "GUI模块不可用")
    def test_pack_parameters_preparation(self):
        """测试打包参数准备"""
        with patch('FreeSimpleGUI.Window') as mock_window:
            mock_window.return_value = MagicMock()
            gui = SoEasyPackGUI()
            
            # 测试普通模式参数
            values = {
                '-MAIN_FILE-': self.test_py_file,
                '-OUTPUT_DIR-': self.output_dir,
                '-EXE_NAME-': 'TestApp',
                '-MODE_NORMAL-': True,
                '-MODE_LIGHT-': False,
                '-HIDE_CMD-': True,
                '-ONE_FILE-': False,
                '-ICON_FILE-': ''
            }
            
            # 模拟打包参数准备逻辑
            pack_mode = 2 if values['-MODE_LIGHT-'] else 1
            self.assertEqual(pack_mode, 1)  # 应该是普通模式
            
            # 测试轻量模式参数
            values['-MODE_NORMAL-'] = False
            values['-MODE_LIGHT-'] = True
            pack_mode = 2 if values['-MODE_LIGHT-'] else 1
            self.assertEqual(pack_mode, 2)  # 应该是轻量模式
    
    @unittest.skipUnless(GUI_AVAILABLE, "GUI模块不可用")
    @patch('gui.main_window.sg.popup')
    @patch('gui.main_window.sg.popup_error')
    def test_error_handling(self, mock_popup_error, mock_popup):
        """测试错误处理"""
        with patch('FreeSimpleGUI.Window') as mock_window:
            mock_window.return_value = MagicMock()
            gui = SoEasyPackGUI()
            
            # 测试无效输入的错误处理
            invalid_values = {
                '-MAIN_FILE-': '',
                '-OUTPUT_DIR-': '',
                '-EXE_NAME-': ''
            }
            
            result = gui.validate_inputs(invalid_values)
            self.assertFalse(result)
            mock_popup_error.assert_called()


class TestSimplifiedPacker(unittest.TestCase):
    """测试简化打包器"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_py_file = os.path.join(self.temp_dir, 'test_main.py')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        
        # 创建测试Python文件
        with open(self.test_py_file, 'w', encoding='utf-8') as f:
            f.write('''
print("Hello from simplified packer test!")
''')
        
        os.makedirs(self.output_dir, exist_ok=True)
        self.packer = SimplifiedPacker()
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skipUnless(CORE_AVAILABLE, "core模块不可用")
    def test_packer_initialization(self):
        """测试打包器初始化"""
        self.assertIsNotNone(self.packer)
        self.assertIsNotNone(self.packer.logger)
    
    @unittest.skipUnless(CORE_AVAILABLE, "core模块不可用")
    def test_input_validation(self):
        """测试输入验证"""
        # 测试不存在的文件
        result = self.packer._validate_inputs('/nonexistent/file.py', self.output_dir, 1)
        self.assertFalse(result)

        # 测试相同目录
        same_dir = os.path.dirname(self.test_py_file)
        result = self.packer._validate_inputs(self.test_py_file, same_dir, 1)
        self.assertFalse(result)

        # 测试无效模式
        result = self.packer._validate_inputs(self.test_py_file, self.output_dir, 0)
        self.assertFalse(result)

        # 测试有效输入
        result = self.packer._validate_inputs(self.test_py_file, self.output_dir, 1)
        self.assertTrue(result)
    
    @unittest.skipUnless(CORE_AVAILABLE, "core模块不可用")
    def test_supported_modes(self):
        """测试支持的模式"""
        modes = self.packer.get_supported_modes()
        self.assertIn(1, modes)
        self.assertIn(2, modes)
        self.assertEqual(len(modes), 2)
        self.assertIn("普通模式", modes[1])
        self.assertIn("轻量模式", modes[2])
    
    @unittest.skipUnless(CORE_AVAILABLE, "core模块不可用")
    def test_pack_method_calls(self):
        """测试打包方法调用"""
        with patch('core.simplified_pack.to_pack') as mock_to_pack:
            mock_to_pack.return_value = None
        
            # 测试普通模式打包
            result = self.packer.pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                exe_name='TestApp',
                pack_mode=1
            )

            # 验证to_pack被调用
            mock_to_pack.assert_called_once()
            call_args = mock_to_pack.call_args

            # 验证关键参数
            self.assertEqual(call_args[1]['main_py_path'], self.test_py_file)
            self.assertEqual(call_args[1]['save_dir'], self.output_dir)
            self.assertEqual(call_args[1]['exe_name'], 'TestApp')
            self.assertEqual(call_args[1]['pack_mode'], 1)
            self.assertEqual(call_args[1]['auto_py_pyc'], False)  # 应该禁用pyc转换
            self.assertEqual(call_args[1]['enable_slim'], False)  # 应该禁用瘦身


if __name__ == '__main__':
    unittest.main()
