#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoEasyPack 主窗口GUI界面

@author: SoEasyPack Team
Created on 2025-01-05
"""

import os
import sys
import threading
from pathlib import Path
import FreeSimpleGUI as sg

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 尝试导入简化打包器，如果失败则使用原始打包器
try:
    from core.simplified_pack import SimplifiedPacker
except ImportError:
    # 如果core模块不可用，创建一个简单的包装器
    class SimplifiedPacker:
        def __init__(self):
            from soeasypack.core.my_logger import my_logger
            self.logger = my_logger

        def pack(self, **kwargs):
            from soeasypack.core.easy_pack import to_pack
            try:
                to_pack(**kwargs)
                return True
            except Exception as e:
                self.logger.error(f"打包失败: {str(e)}")
                return False


class SoEasyPackGUI:
    """SoEasyPack GUI主窗口类"""
    
    def __init__(self):
        """初始化GUI"""
        self.window = None
        self.packer = SimplifiedPacker()
        self.setup_theme()
        self.create_layout()
    
    def setup_theme(self):
        """设置GUI主题"""
        sg.theme('LightBlue3')
        sg.set_options(font=('Microsoft YaHei', 10))
    
    def create_layout(self):
        """创建GUI布局"""
        # 文件选择区域
        file_frame = [
            [sg.Text('主程序文件:', size=(12, 1)), 
             sg.Input(key='-MAIN_FILE-', size=(50, 1)), 
             sg.FileBrowse('浏览', file_types=(('Python Files', '*.py'),))],
            [sg.Text('输出目录:', size=(12, 1)), 
             sg.Input(key='-OUTPUT_DIR-', size=(50, 1)), 
             sg.FolderBrowse('浏览')],
            [sg.Text('程序名称:', size=(12, 1)), 
             sg.Input('MyApp', key='-EXE_NAME-', size=(20, 1))]
        ]
        
        # 打包选项区域
        options_frame = [
            [sg.Text('打包模式:'), 
             sg.Radio('普通模式', 'PACK_MODE', key='-MODE_NORMAL-', default=True),
             sg.Radio('轻量模式', 'PACK_MODE', key='-MODE_LIGHT-')],
            [sg.Checkbox('隐藏控制台窗口', key='-HIDE_CMD-', default=True)],
            [sg.Checkbox('生成单文件exe', key='-ONE_FILE-', default=False)],
            [sg.Text('图标文件:', size=(12, 1)), 
             sg.Input(key='-ICON_FILE-', size=(35, 1)), 
             sg.FileBrowse('浏览', file_types=(('Icon Files', '*.ico'),))]
        ]
        
        # 按钮区域
        button_frame = [
            [sg.Button('开始打包', key='-PACK-', size=(12, 2), button_color=('white', 'green')),
             sg.Button('清空日志', key='-CLEAR_LOG-', size=(12, 2)),
             sg.Button('退出程序', key='-EXIT-', size=(12, 2), button_color=('white', 'red'))]
        ]
        
        # 日志显示区域
        log_frame = [
            [sg.Text('打包日志:')],
            [sg.Multiline('', key='-LOG-', size=(80, 15), autoscroll=True, disabled=True)]
        ]
        
        # 主布局
        layout = [
            [sg.Frame('文件设置', file_frame, font=('Microsoft YaHei', 10, 'bold'))],
            [sg.Frame('打包选项', options_frame, font=('Microsoft YaHei', 10, 'bold'))],
            [sg.Frame('操作', button_frame, font=('Microsoft YaHei', 10, 'bold'))],
            [sg.Frame('日志输出', log_frame, font=('Microsoft YaHei', 10, 'bold'))]
        ]
        
        self.window = sg.Window('SoEasyPack - Python项目打包工具', layout, 
                               finalize=True, resizable=True, icon=None)
    
    def log_message(self, message):
        """在日志区域显示消息"""
        if self.window:
            self.window['-LOG-'].print(message)
    
    def validate_inputs(self, values):
        """验证用户输入"""
        if not values['-MAIN_FILE-']:
            try:
                sg.popup_error('请选择主程序文件！')
            except:
                pass  # 在测试环境中可能无法显示弹窗
            return False

        if not os.path.exists(values['-MAIN_FILE-']):
            try:
                sg.popup_error('主程序文件不存在！')
            except:
                pass  # 在测试环境中可能无法显示弹窗
            return False

        if not values['-OUTPUT_DIR-']:
            try:
                sg.popup_error('请选择输出目录！')
            except:
                pass  # 在测试环境中可能无法显示弹窗
            return False

        if not values['-EXE_NAME-'].strip():
            try:
                sg.popup_error('请输入程序名称！')
            except:
                pass  # 在测试环境中可能无法显示弹窗
            return False

        return True
    
    def pack_in_thread(self, values):
        """在后台线程中执行打包"""
        try:
            # 确定打包模式
            pack_mode = 2 if values['-MODE_LIGHT-'] else 1
            
            # 准备打包参数
            pack_params = {
                'main_py_path': values['-MAIN_FILE-'],
                'save_dir': values['-OUTPUT_DIR-'],
                'exe_name': values['-EXE_NAME-'].strip(),
                'pack_mode': pack_mode,
                'hide_cmd': values['-HIDE_CMD-'],
                'onefile': values['-ONE_FILE-'],
                'png_path': values['-ICON_FILE-'] if values['-ICON_FILE-'] else None
            }
            
            self.log_message("=" * 50)
            self.log_message("开始打包...")
            self.log_message(f"主程序: {pack_params['main_py_path']}")
            self.log_message(f"输出目录: {pack_params['save_dir']}")
            self.log_message(f"程序名称: {pack_params['exe_name']}")
            self.log_message(f"打包模式: {'轻量模式' if pack_mode == 2 else '普通模式'}")
            self.log_message("=" * 50)
            
            # 执行打包
            success = self.packer.pack(**pack_params)
            
            if success:
                self.log_message("✅ 打包完成！")
                try:
                    sg.popup('打包成功！', '打包已完成，请检查输出目录。', title='成功')
                except:
                    pass  # 在测试环境中可能无法显示弹窗
            else:
                self.log_message("❌ 打包失败！")
                try:
                    sg.popup_error('打包失败！请查看日志了解详情。')
                except:
                    pass  # 在测试环境中可能无法显示弹窗
                
        except Exception as e:
            error_msg = f"打包过程中发生错误: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            try:
                sg.popup_error(error_msg)
            except:
                pass  # 在测试环境中可能无法显示弹窗
        finally:
            # 重新启用打包按钮
            self.window['-PACK-'].update(disabled=False)
            self.window['-PACK-'].update(text='开始打包')
    
    def run(self):
        """运行GUI主循环"""
        self.log_message("🎉 欢迎使用 SoEasyPack!")
        self.log_message("📝 请选择要打包的Python文件和输出目录")
        
        while True:
            event, values = self.window.read()
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            
            elif event == '-PACK-':
                if self.validate_inputs(values):
                    # 禁用打包按钮，防止重复点击
                    self.window['-PACK-'].update(disabled=True)
                    self.window['-PACK-'].update(text='打包中...')
                    
                    # 在后台线程中执行打包
                    pack_thread = threading.Thread(target=self.pack_in_thread, args=(values,))
                    pack_thread.daemon = True
                    pack_thread.start()
            
            elif event == '-CLEAR_LOG-':
                self.window['-LOG-'].update('')
                self.log_message("日志已清空")
        
        self.window.close()
