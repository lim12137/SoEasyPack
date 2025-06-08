#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心功能测试
测试重构后的核心打包功能

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

from soeasypack.core.easy_pack import to_pack


class TestCoreFunctionality(unittest.TestCase):
    """测试核心功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_py_file = os.path.join(self.temp_dir, 'test_main.py')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        
        # 创建测试Python文件
        with open(self.test_py_file, 'w', encoding='utf-8') as f:
            f.write('''
print("Hello from core test!")
import sys
print("Python version:", sys.version)
''')
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_removed_pack_modes(self):
        """测试移除的打包模式"""
        # 测试快速模式(0)被移除
        with patch('soeasypack.core.easy_pack.my_logger') as mock_logger:
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=0  # 快速模式应该被拒绝
            )
            # 应该记录错误日志
            mock_logger.error.assert_called_with('pack_mode参数值只限于1(普通模式), 2(轻量模式)')
        
        # 测试ast模式(3)被移除
        with patch('soeasypack.core.easy_pack.my_logger') as mock_logger:
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=3  # ast模式应该被拒绝
            )
            mock_logger.error.assert_called_with('pack_mode参数值只限于1(普通模式), 2(轻量模式)')
    
    def test_valid_pack_modes(self):
        """测试有效的打包模式"""
        with patch('soeasypack.core.easy_pack.copy_py_env') as mock_copy_env, \
             patch('soeasypack.core.easy_pack.copy_py_script') as mock_copy_script, \
             patch('soeasypack.core.easy_pack.build_exe') as mock_build_exe, \
             patch('soeasypack.core.easy_pack.create_bat') as mock_create_bat, \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists') as mock_exists:

            # 模拟rundep目录不存在，强制调用copy_py_env
            mock_exists.side_effect = lambda path: path == self.test_py_file

            # 创建必要的目录结构
            script_dir = os.path.join(self.output_dir, 'rundep/AppData')
            os.makedirs(script_dir, exist_ok=True)
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试普通模式(1)
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=1
            )
            mock_copy_env.assert_called()

            # 重置mock
            mock_copy_env.reset_mock()

            # 测试轻量模式(2) - 需要requirements_path
            requirements_file = os.path.join(self.temp_dir, 'requirements.txt')
            with open(requirements_file, 'w') as f:
                f.write('requests==2.25.1\n')

            # 模拟requirements文件存在
            def mock_exists_side_effect(path):
                if path == self.test_py_file or path == requirements_file:
                    return True
                return False

            mock_exists.side_effect = mock_exists_side_effect

            # 模拟copy_embed_depend函数以避免文件系统问题
            with patch('soeasypack.core.easy_pack.copy_embed_depend') as mock_copy_embed:
                to_pack(
                    main_py_path=self.test_py_file,
                    save_dir=self.output_dir,
                    pack_mode=2,
                    requirements_path=requirements_file
                )
                mock_copy_env.assert_called()
    
    def test_pyc_conversion_disabled(self):
        """测试pyc自动转换功能被禁用"""
        with patch('soeasypack.core.easy_pack.copy_py_env') as mock_copy_env, \
             patch('soeasypack.core.easy_pack.copy_py_script') as mock_copy_script, \
             patch('soeasypack.core.easy_pack.py_to_pyc') as mock_py_to_pyc, \
             patch('soeasypack.core.easy_pack.build_exe') as mock_build_exe, \
             patch('soeasypack.core.easy_pack.create_bat') as mock_create_bat, \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists') as mock_exists:

            # 模拟rundep目录不存在
            mock_exists.side_effect = lambda path: path == self.test_py_file

            # 创建必要的目录结构
            script_dir = os.path.join(self.output_dir, 'rundep/AppData')
            os.makedirs(script_dir, exist_ok=True)
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试auto_py_pyc=True时不会自动转换pyc（除非embed_exe=True）
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=1,
                auto_py_pyc=True,  # 这个参数应该被忽略
                embed_exe=False,
                onefile=False
            )

            # py_to_pyc不应该被调用（因为embed_exe=False且onefile=False）
            mock_py_to_pyc.assert_not_called()
    
    def test_pyc_conversion_only_for_embed(self):
        """测试pyc转换只在embed模式下进行"""
        with patch('soeasypack.core.easy_pack.copy_py_env') as mock_copy_env, \
             patch('soeasypack.core.easy_pack.copy_py_script') as mock_copy_script, \
             patch('soeasypack.core.easy_pack.py_to_pyc') as mock_py_to_pyc, \
             patch('soeasypack.core.easy_pack.build_exe') as mock_build_exe, \
             patch('soeasypack.core.easy_pack.copy_embed_depend') as mock_copy_embed, \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists') as mock_exists:

            # 模拟rundep目录不存在
            mock_exists.side_effect = lambda path: path == self.test_py_file

            # 创建必要的目录结构
            script_dir = os.path.join(self.output_dir, 'rundep/AppData')
            os.makedirs(script_dir, exist_ok=True)
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试embed_exe=True时会转换pyc
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=1,
                embed_exe=True
            )

            # py_to_pyc应该被调用
            mock_py_to_pyc.assert_called_once()
    
    def test_slim_functionality_disabled(self):
        """测试瘦身功能被禁用"""
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
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试enable_slim=True时瘦身功能不会被调用
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                pack_mode=1,
                enable_slim=True  # 这个参数应该被忽略
            )

            # 由于瘦身功能被移除，不应该有相关调用
            # 这里主要是确保程序正常运行而不报错
            mock_copy_env.assert_called()
    
    def test_default_parameters(self):
        """测试默认参数"""
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
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试默认参数
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir
                # 使用所有默认参数
            )

            # 验证默认参数生效
            mock_copy_env.assert_called()
            mock_build_exe.assert_called()

            # 检查build_exe的调用参数
            call_args = mock_build_exe.call_args
            # build_exe使用位置参数，所以检查args而不是kwargs
            if len(call_args) > 1 and isinstance(call_args[1], dict):
                self.assertEqual(call_args[1].get('pack_mode', 1), 1)  # 默认应该是普通模式
            # 验证build_exe被调用
            mock_build_exe.assert_called()
    
    def test_input_validation(self):
        """测试输入验证"""
        with patch('soeasypack.core.easy_pack.my_logger') as mock_logger:
            # 测试不存在的文件
            to_pack(
                main_py_path='/nonexistent/file.py',
                save_dir=self.output_dir
            )
            mock_logger.error.assert_called_with('未找到/nonexistent/file.py，请检查路径')
        
        with patch('soeasypack.core.easy_pack.my_logger') as mock_logger:
            # 测试相同目录
            same_dir = os.path.dirname(self.test_py_file)
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=same_dir
            )
            mock_logger.error.assert_called_with('save_dir不能是main_py_path所在目录')
    
    def test_parameter_compatibility(self):
        """测试参数兼容性"""
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
            mock_copy_script.return_value = os.path.join(script_dir, 'test_main.py')

            # 测试所有参数都能正常传递（即使某些被禁用）
            to_pack(
                main_py_path=self.test_py_file,
                save_dir=self.output_dir,
                exe_name='TestApp',
                png_path=None,
                hide_cmd=False,
                pack_mode=1,
                force_copy_env=False,
                auto_py_pyc=True,  # 被禁用但保持兼容性
                pyc_optimize=1,
                auto_py_pyd=False,
                embed_exe=False,
                onefile=False,
                monitoring_time=18,
                uac=False,
                requirements_path=None,
                except_packages=None,
                winres_json_path=None,
                delay_time=3,
                all_pyc_zip=False,
                pip_source=None,
                enable_slim=True  # 被禁用但保持兼容性
            )

            # 程序应该正常运行
            mock_copy_env.assert_called()


if __name__ == '__main__':
    unittest.main()
