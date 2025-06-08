#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试
测试整个应用程序的集成功能

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


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_py_file = os.path.join(self.temp_dir, 'test_app.py')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        
        # 创建一个更复杂的测试Python文件
        with open(self.test_py_file, 'w', encoding='utf-8') as f:
            f.write('''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试应用程序
"""

import os
import sys
import json

def main():
    print("SoEasyPack 测试应用程序")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 测试一些基本功能
    data = {"message": "Hello from SoEasyPack!", "version": "1.0.0"}
    print(f"JSON数据: {json.dumps(data, ensure_ascii=False)}")
    
    print("应用程序运行成功！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
''')
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_removed_features_integration(self):
        """测试移除功能的集成"""
        # 验证快速模式、瘦身功能、pyc自动转换功能确实被移除
        
        # 1. 测试快速模式不可用
        from soeasypack.core.easy_pack import to_pack
        with patch('soeasypack.core.easy_pack.my_logger') as mock_logger:
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=0  # 快速模式
            )
            mock_logger.error.assert_called_with('pack_mode参数值只限于1(普通模式), 2(轻量模式)')
        
        # 2. 测试瘦身功能导入被移除
        try:
            from soeasypack import to_slim_file
            self.fail("瘦身功能应该已被移除")
        except ImportError:
            pass  # 预期的行为
        
        # 3. 测试PYD转换功能导入被移除
        try:
            from soeasypack import to_pyd
            self.fail("PYD转换功能应该已被移除")
        except ImportError:
            pass  # 预期的行为
    
    def test_gui_core_integration(self):
        """测试GUI与核心功能的集成"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            from gui.main_window import SoEasyPackGUI
            from core.simplified_pack import SimplifiedPacker
        except ImportError:
            self.skipTest("GUI或core模块不可用")
        
        with patch('FreeSimpleGUI.Window') as mock_window:
            mock_window.return_value = MagicMock()
            
            # 创建GUI实例
            gui = SoEasyPackGUI()
            
            # 验证GUI使用简化打包器
            self.assertIsInstance(gui.packer, SimplifiedPacker)
            
            # 测试参数验证集成
            valid_values = {
                '-MAIN_FILE-': self.test_py_file,
                '-OUTPUT_DIR-': self.output_dir,
                '-EXE_NAME-': 'TestApp'
            }
            self.assertTrue(gui.validate_inputs(valid_values))
    
    def test_simplified_packer_integration(self):
        """测试简化打包器的集成"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            from core.simplified_pack import SimplifiedPacker
        except ImportError:
            self.skipTest("core模块不可用")
        
        packer = SimplifiedPacker()
        
        # 测试支持的模式
        modes = packer.get_supported_modes()
        self.assertEqual(len(modes), 2)
        self.assertIn(1, modes)
        self.assertIn(2, modes)
        
        # 测试输入验证
        self.assertTrue(packer._validate_inputs(self.test_py_file, self.output_dir, 1))
        self.assertFalse(packer._validate_inputs(self.test_py_file, self.output_dir, 0))  # 快速模式不支持
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流程"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            from core.simplified_pack import SimplifiedPacker
        except ImportError:
            self.skipTest("core模块不可用")

        with patch('core.simplified_pack.to_pack') as mock_to_pack:
        
            mock_to_pack.return_value = None
            packer = SimplifiedPacker()

            # 模拟完整的打包流程
            result = packer.pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                exe_name='IntegrationTest',
                pack_mode=1,
                hide_cmd=False,
                onefile=False
            )

            # 验证to_pack被正确调用
            mock_to_pack.assert_called_once()
            call_args = mock_to_pack.call_args[1]

            # 验证关键参数
            self.assertEqual(call_args['main_py_path'], self.test_py_file)
            self.assertEqual(call_args['save_dir'], self.output_dir)
            self.assertEqual(call_args['exe_name'], 'IntegrationTest')
            self.assertEqual(call_args['pack_mode'], 1)
            self.assertEqual(call_args['auto_py_pyc'], False)  # 应该禁用
            self.assertEqual(call_args['enable_slim'], False)  # 应该禁用
    
    def test_version_update(self):
        """测试版本更新"""
        import soeasypack
        
        # 验证版本号已更新为GUI版本
        self.assertEqual(soeasypack.__version__, '1.0.0-gui')
    
    def test_import_structure(self):
        """测试导入结构"""
        # 测试主要功能仍可导入
        from soeasypack import to_pack
        self.assertIsNotNone(to_pack)
        
        # 测试移除的功能不可导入
        with self.assertRaises(ImportError):
            from soeasypack import to_slim_file
        
        with self.assertRaises(ImportError):
            from soeasypack import to_pyd
    
    def test_backward_compatibility(self):
        """测试向后兼容性"""
        from soeasypack.core.easy_pack import to_pack

        with patch('soeasypack.core.easy_pack.copy_py_env') as mock_copy_env, \
             patch('soeasypack.core.easy_pack.copy_py_script') as mock_copy_script, \
             patch('soeasypack.core.easy_pack.build_exe') as mock_build_exe, \
             patch('soeasypack.core.easy_pack.create_bat') as mock_create_bat, \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists') as mock_exists:

            # 模拟rundep目录不存在
            mock_exists.side_effect = lambda path: path == self.test_py_file

            # 创建必要的目录结构
            script_dir = os.path.join(self.output_dir, 'rundep/AppData')
            os.makedirs(script_dir, exist_ok=True)
            mock_copy_script.return_value = os.path.join(script_dir, 'test_app.py')

            # 测试旧的API调用仍然工作（但某些参数被忽略）
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=1,
                auto_py_pyc=True,  # 被忽略
                enable_slim=True   # 被忽略
            )

            # 应该正常执行
            mock_copy_env.assert_called()
    
    def test_error_propagation(self):
        """测试错误传播"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            from core.simplified_pack import SimplifiedPacker
        except ImportError:
            self.skipTest("core模块不可用")
        
        packer = SimplifiedPacker()
        
        # 测试错误情况
        with patch('core.simplified_pack.to_pack', side_effect=Exception("测试错误")):
            result = packer.pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                exe_name='ErrorTest',
                pack_mode=1
            )
            
            # 应该返回False表示失败
            self.assertFalse(result)
    
    def test_gui_thread_safety(self):
        """测试GUI线程安全性"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            from gui.main_window import SoEasyPackGUI
        except ImportError:
            self.skipTest("GUI模块不可用")
        
        with patch('FreeSimpleGUI.Window') as mock_window:
            mock_window_instance = MagicMock()
            mock_window.return_value = mock_window_instance
            
            gui = SoEasyPackGUI()
            
            # 模拟打包参数
            values = {
                '-MAIN_FILE-': self.test_py_file,
                '-OUTPUT_DIR-': self.output_dir,
                '-EXE_NAME-': 'ThreadTest',
                '-MODE_NORMAL-': True,
                '-MODE_LIGHT-': False,
                '-HIDE_CMD-': True,
                '-ONE_FILE-': False,
                '-ICON_FILE-': ''
            }
            
            # 测试线程中的打包逻辑（不实际启动线程）
            with patch.object(gui.packer, 'pack', return_value=True) as mock_pack:
                gui.pack_in_thread(values)
                
                # 验证打包方法被调用
                mock_pack.assert_called_once()
                
                # 验证GUI状态更新
                mock_window_instance.__getitem__.assert_called()


if __name__ == '__main__':
    unittest.main()
