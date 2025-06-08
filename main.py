#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoEasyPack GUI Application
独立的Python项目打包工具 - 图形界面版本

@author: SoEasyPack Team
Created on 2025-01-05
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main_window import SoEasyPackGUI

def main():
    """主程序入口"""
    try:
        # 创建并运行GUI应用程序
        app = SoEasyPackGUI()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
