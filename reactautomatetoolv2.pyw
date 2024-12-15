"""
Modern React Project Automator
-----------------------------
A professional-grade desktop application for automating React project creation
with advanced features and industry-standard practices.

Author: Assistant
Version: 2.0.0
License: MIT
"""

import sys
import os
import subprocess
import shutil
import json
import git
import logging
from enum import Enum
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, 
    QLabel, QWidget, QMessageBox, QComboBox, QFileDialog, QHBoxLayout, 
    QFrame, QProgressDialog, QTabWidget, QScrollArea, QGridLayout,
    QGroupBox, QSpinBox, QCheckBox, QTextEdit, QSplitter, QMenuBar,
    QMenu, QAction, QStyle, QToolBar, QDialog, QDialogButtonBox,
    QFileDialog, QInputDialog
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, QLinearGradient, QBrush, QIcon,
    QPainter, QPaintEvent, QFontDatabase, QTextCharFormat,
    QSyntaxHighlighter, QTextCursor, QKeySequence
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QRect, QProcess, QSettings, QPoint, QRegExp
)
from dataclasses import dataclass


# Application Constants
APP_NAME = "Modern React Project Automator"
APP_VERSION = "2.0.0"
ORGANIZATION_NAME = "ReactAutomator"
SETTINGS_FILE = "config.json"

@dataclass
class AppTheme:
    """Theme configuration for the application"""
    name: str
    background: str
    text: str
    primary: str
    secondary: str
    accent: str
    terminal_background: str
    terminal_text: str
    
    @classmethod
    def light(cls) -> 'AppTheme':
        return cls(
            name="light",
            background="#ffffff",
            text="#1f2937",
            primary="#2563eb",
            secondary="#4b5563",
            accent="#3b82f6",
            terminal_background="#1a1a1a",
            terminal_text="#00ff00"
        )
    
    @classmethod
    def dark(cls) -> 'AppTheme':
        return cls(
            name="dark",
            background="#1f2937",
            text="#ffffff",
            primary="#3b82f6",
            secondary="#9ca3af",
            accent="#60a5fa",
            terminal_background="#000000",
            terminal_text="#00ff00"
        )

class LogLevel(Enum):  # LogLevel tanımlaması
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    DEBUG = "DEBUG"

@dataclass
class ProjectConfig:
    """Configuration for React project creation"""
    name: str
    template: str
    dependencies: List[str]
    dev_dependencies: List[str]
    git_integration: bool
    test_framework: str
    styling_solution: str
    typescript: bool
    eslint: bool
    prettier: bool
    
    @classmethod
    def create_default(cls) -> 'ProjectConfig':
        return cls(
            name="",
            template="react",
            dependencies=[],
            dev_dependencies=[],
            git_integration=True,
            test_framework="jest",
            styling_solution="Tailwind CSS",
            typescript=True,
            eslint=True,
            prettier=True
        )

class ProjectWorker(QThread):
    """Worker thread for project creation tasks"""
    progress = pyqtSignal(int, str)
    terminal_output = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, config: ProjectConfig, npm_path: str, npx_path: str):
        super().__init__()
        self.config = config
        self.npm_path = npm_path
        self.npx_path = npx_path
        self.logger = logging.getLogger("ProjectWorker")

    def emit_log(self, message: str, level: str):
        self.terminal_output.emit(message, level)
        
    def run_process(self, command: List[str], shell: bool = False) -> bool:
        """Run a process and capture its output"""
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        
        def handle_output():
            output = process.readAll().data().decode()
            self.terminal_output.emit(output, LogLevel.INFO)
            
        process.readyReadStandardOutput.connect(handle_output)
        process.readyReadStandardError.connect(handle_output)
        
        if shell:
            process.start(command[0], command[1:])
        else:
            process.start(command[0], command[1:])
            
        process.waitForFinished()
        return process.exitCode() == 0

    def run(self):
        """Main worker thread execution"""
        try:
            self.progress.emit(0, "Initializing project...")
            self.terminal_output.emit("Starting project creation...", "INFO") 
            
            # Create project directory
            project_path = Path.cwd() / self.config.name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create Vite project
            self.progress.emit(20, "Creating Vite project...")
            self.terminal_output.emit(
                "Creating Vite project structure...",
                LogLevel.INFO
            )
            
            template_suffix = "-ts" if self.config.typescript else ""
            template = f"{self.config.template}{template_suffix}"
            
            success = self.run_process([
                self.npx_path,
                "create-vite@latest",
                self.config.name,
                "--template",
                template
            ])
            
            if not success:
                raise Exception("Failed to create Vite project")
            
            # Change to project directory
            os.chdir(project_path)
            
            # Install dependencies
            self.progress.emit(40, "Installing dependencies...")
            self.terminal_output.emit(
                "Installing project dependencies...",
                LogLevel.INFO
            )
            
            success = self.run_process([self.npm_path, "install"])
            if not success:
                raise Exception("Failed to install dependencies")
            
            # Setup additional features
            self.progress.emit(60, "Setting up additional features...")
            self.terminal_output.emit(
                "Configuring project features...",
                LogLevel.INFO
            )
            
            self.setup_features()
            
            # Finalize setup
            self.progress.emit(80, "Finalizing setup...")
            self.terminal_output.emit(
                "Finalizing project setup...",
                LogLevel.INFO
            )
            
            self.setup_project_config()
            
            # Git initialization
            if self.config.git_integration:
                self.setup_git()
            
            self.progress.emit(100, "Project created successfully!")
            self.terminal_output.emit(
                "Project created successfully!",
                LogLevel.SUCCESS
            )
            self.finished.emit(True, "Project created successfully!")
            
        except Exception as e:
            self.terminal_output.emit(str(e), LogLevel.ERROR)
            self.finished.emit(False, str(e))
            
    def setup_features(self):
        """Setup additional project features"""
        try:
            if self.config.typescript:
                self.setup_typescript()
                
            if self.config.test_framework:
                self.setup_testing()
                
            if self.config.styling_solution:
                self.setup_styling()
                
            if self.config.eslint or self.config.prettier:
                self.setup_linting()
                
        except Exception as e:
            self.terminal_output.emit(
                f"Error setting up features: {str(e)}",
                LogLevel.ERROR
            )
            raise
            
    def setup_typescript(self):
        """Configure TypeScript"""
        self.terminal_output.emit(
            "Setting up TypeScript configuration...",
            LogLevel.INFO
        )
        
        tsconfig = {
            "compilerOptions": {
                "target": "ESNext",
                "useDefineForClassFields": True,
                "lib": ["DOM", "DOM.Iterable", "ESNext"],
                "allowJs": False,
                "skipLibCheck": True,
                "esModuleInterop": False,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "module": "ESNext",
                "moduleResolution": "Node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx"
            },
            "include": ["src"],
            "references": [{ "path": "./tsconfig.node.json" }]
        }
        
        with open("tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)
            
    def setup_testing(self):
        """Configure testing framework"""
        self.terminal_output.emit(
            "Setting up testing configuration...",
            LogLevel.INFO
        )
        
        # Install testing dependencies
        test_deps = [
            "@testing-library/react",
            "@testing-library/jest-dom",
            "@testing-library/user-event",
            "vitest",
            "jsdom",
        ]
        
        success = self.run_process([
            self.npm_path, "install", "-D",
            *test_deps
        ])
        
        if not success:
            raise Exception("Failed to install testing dependencies")
            
        # Create test setup file
        test_setup = """
        import '@testing-library/jest-dom'
        import { expect, afterEach } from 'vitest'
        import { cleanup } from '@testing-library/react'
        
        afterEach(() => {
            cleanup()
        })
        """
        
        os.makedirs("test", exist_ok=True)
        with open("test/setup.ts", "w") as f:
            f.write(test_setup.strip())
            
    def setup_styling(self):
        """Configure styling solution"""
        self.terminal_output.emit(
            f"Setting up {self.config.styling_solution}...",
            LogLevel.INFO
        )
        
        if self.config.styling_solution == "Tailwind CSS":
            self.setup_tailwind()
        elif self.config.styling_solution == "Styled Components":
            self.setup_styled_components()
            
    def setup_tailwind(self):
        """Configure Tailwind CSS"""
        success = self.run_process([
            self.npm_path, "install", "-D",
            "tailwindcss",
            "postcss",
            "autoprefixer"
        ])
        
        if not success:
            raise Exception("Failed to install Tailwind CSS")
            
        success = self.run_process([
            self.npx_path, "tailwindcss", "init", "-p"
        ])
        
        if not success:
            raise Exception("Failed to initialize Tailwind CSS")
            
        # Update tailwind.config.js
        tailwind_config = {
            "content": [
                "./index.html",
                "./src/**/*.{js,ts,jsx,tsx}"
            ],
            "theme": {
                "extend": {}
            },
            "plugins": []
        }
        
        with open("tailwind.config.js", "w") as f:
            f.write(f"module.exports = {json.dumps(tailwind_config, indent=2)}")
            
    def setup_styled_components(self):
        """Configure Styled Components"""
        success = self.run_process([
            self.npm_path, "install",
            "styled-components"
        ])
        
        if not success:
            raise Exception("Failed to install Styled Components")
            
        if self.config.typescript:
            success = self.run_process([
                self.npm_path, "install", "-D",
                "@types/styled-components"
            ])
            
            if not success:
                raise Exception("Failed to install Styled Components types")
                
        # Create theme file
        theme_file = """
        export const theme = {
            colors: {
                primary: '#2563eb',
                secondary: '#4b5563',
                background: '#ffffff',
                text: '#1f2937',
            },
            breakpoints: {
                sm: '640px',
                md: '768px',
                lg: '1024px',
                xl: '1280px',
            },
        }
        """
        
        os.makedirs("src/styles", exist_ok=True)
        with open("src/styles/theme.ts", "w") as f:
            f.write(theme_file.strip())
            
    def setup_linting(self):
        """Configure ESLint and Prettier"""
        if self.config.eslint:
            self.terminal_output.emit(
                "Setting up ESLint...",
                LogLevel.INFO
            )
            
            eslint_deps = [
                "eslint",
                "eslint-plugin-react",
                "eslint-plugin-react-hooks",
                "@typescript-eslint/parser",
                "@typescript-eslint/eslint-plugin"
            ]
            
            success = self.run_process([
                self.npm_path, "install", "-D",
                *eslint_deps
            ])
            
            if not success:
                raise Exception("Failed to install ESLint")
                
            eslint_config = {
                "env": {
                    "browser": True,
                    "es2021": True
                },
                "extends": [
                    "eslint:recommended",
                    "plugin:react/recommended",
                    "plugin:react-hooks/recommended",
                    "plugin:@typescript-eslint/recommended"
                ],
                "parser": "@typescript-eslint/parser",
                "parserOptions": {
                    "ecmaFeatures": {
                        "jsx": True
                    },
                    "ecmaVersion": 12,
                    "sourceType": "module"
                },
                "plugins": [
                    "react",
                    "@typescript-eslint"
                ],
                "rules": {
                    "react/react-in-jsx-scope": "off"
                }
            }
            
            with open(".eslintrc.json", "w") as f:
                json.dump(eslint_config, f, indent=2)
                
        if self.config.prettier:
            self.terminal_output.emit(
                "Setting up Prettier...",
                LogLevel.INFO
            )
            
            success = self.run_process([
                self.npm_path, "install", "-D",
                "prettier"
            ])
            
            if not success:
                raise Exception("Failed to install Prettier")
                
            prettier_config = {
                "semi": True,
                "trailingComma": "es5",
                "singleQuote": True,
                "printWidth": 80,
                "tabWidth": 2
            }
            
            with open(".prettierrc", "w") as f:
                json.dump(prettier_config, f, indent=2)
                
    def setup_git(self):
        """Initialize Git repository"""
        self.terminal_output.emit(
            "Initializing Git repository...",
            LogLevel.INFO
        )
        
        try:
            repo = git.Repo.init()
            
            # Create .gitignore
            gitignore = """
            # Dependencies
            node_modules
            .pnp
            .pnp.js
            
            # Testing
            coverage
            
            # Production
            build
            dist
            
            # Misc
            .DS_Store
            .env.local
            .env.development.local
            .env.test.local
            .env.production.local
            
            # Debug
            npm-debug.log*
            yarn-debug.log*
            yarn-error.log*
            
            # Editor
            .idea
            .vscode
            *.sublime-workspace
            *.sublime-project
            """
            
            with open(".gitignore", "w") as f:
                f.write(gitignore.strip())
                
            # Initial commit
            repo.index.add(["."])
            repo.index.commit("Initial commit")
            
            self.terminal_output.emit(
                "Git repository initialized successfully",
                LogLevel.SUCCESS
            )
            
        except Exception as e:
            self.terminal_output.emit(
                f"Failed to initialize Git repository: {str(e)}",
                LogLevel.ERROR
            )
            raise

class TerminalHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for terminal output"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
        
    def setup_formats(self):
        """Initialize text formats for different log levels"""
        self.formats = {
            "INFO": self.create_format("#ffffff"),
            "WARNING": self.create_format("#fbbf24"),
            "ERROR": self.create_format("#ef4444"),
            "SUCCESS": self.create_format("#10b981"),
            "DEBUG": self.create_format("#8b5cf6")
        }
    
    def create_format(self, color: str) -> QTextCharFormat:
        """Create text format with specified color"""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        return fmt
    
    def highlightBlock(self, text: str):
        """Highlight text block based on log level"""
        for level, fmt in self.formats.items():
            pattern = f"^\\[{level}\\].*$"
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class TerminalOutput(QWidget):
    """Advanced terminal output widget with search and logging capabilities"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_logging()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QToolBar()
        
        # Save action
        save_action = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton),
            "Save Output",
            self
        )
        save_action.triggered.connect(self.save_output)
        toolbar.addAction(save_action)
        
        # Search action
        search_action = QAction(
            self.style().standardIcon(QStyle.SP_FileDialogContentsView),
            "Search",
            self
        )
        search_action.triggered.connect(self.show_search_dialog)
        toolbar.addAction(search_action)
        
        # Clear action
        clear_action = QAction(
            self.style().standardIcon(QStyle.SP_TrashIcon),
            "Clear",
            self
        )
        clear_action.triggered.connect(self.clear_output)
        toolbar.addAction(clear_action)
        
        layout.addWidget(toolbar)
        
        # Terminal output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.highlighter = TerminalHighlighter(self.output.document())
        layout.addWidget(self.output)
        
    def setup_logging(self):
        self.logger = logging.getLogger("TerminalOutput")
        self.logger.setLevel(logging.DEBUG)
        
    def save_output(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Terminal Output",
            "",
            "Text Files (*.txt);;Log Files (*.log)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output.toPlainText())
                self.logger.info(f"Output saved to {filename}")
            except Exception as e:
                self.logger.error(f"Failed to save output: {str(e)}")
                
    def show_search_dialog(self):
        dialog = SearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.search_text(
                dialog.search_input.text(),
                dialog.case_sensitive.isChecked(),
                dialog.forward_radio.isChecked()
            )
    
    def append_output(self, text: str, level: str = "INFO"):
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output.setTextCursor(cursor)
        
        # Format message with log level
        formatted_text = f"[{level}] {text}"
        self.output.insertPlainText(formatted_text + "\n")
        
        # Scroll to bottom
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )
    
    def clear_output(self):
        self.output.clear()
        self.logger.info("Terminal output cleared")
        
    def search_text(self, text: str, case_sensitive: bool, forward: bool):
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if not forward:
            flags |= QTextDocument.FindBackward
            
        cursor = self.output.textCursor()
        found = self.output.find(text, flags)
        
        if found:
            self.logger.info(f"Found text: {text}")
        else:
            self.logger.warning(f"Text not found: {text}")


class ModernReactAutomator(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.settings = QSettings(ORGANIZATION_NAME, APP_NAME)
        self.current_theme = AppTheme.light()
        self.init_ui()
        self.setup_npm_paths()
        self.project_config = ProjectConfig.create_default()
        self.load_settings()

        # UI initialization
        self.terminal = None  # Terminal değişkenini önce tanımla
        self.init_ui()  # Sonra UI'ı başlat
        self.setup_npm_paths()
        self.load_settings()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setMinimumSize(1200, 800)
        self.setup_fonts()
        
        # Ana widget'ı oluştur
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Splitter oluştur
        splitter = QSplitter(Qt.Vertical)
        
        # Üst widget (proje konfigürasyonu)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        self.setup_project_form(top_layout)
        splitter.addWidget(top_widget)
        
        # Terminal widget'ı oluştur
        self.terminal = TerminalOutput()
        splitter.addWidget(self.terminal)
        
        # Splitter boyutlarını ayarla
        splitter.setSizes([600, 200])
        
        # Ana layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(splitter)
        
        # Menu bar'ı en son ekle
        self.setup_menu_bar()
        
        self.apply_theme()

    def setup_fonts(self):
        """Setup application fonts"""
        default_font = QFont()
        default_font.setPointSize(10)
        self.setFont(default_font)
        
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Project', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.create_project)
        file_menu.addAction(new_action)
        
        save_action = QAction('&Save Terminal Output', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.terminal.save_output)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        search_action = QAction('&Search Terminal', self)
        search_action.setShortcut('Ctrl+F')
        search_action.triggered.connect(self.terminal.show_search_dialog)
        edit_menu.addAction(search_action)
        
        clear_action = QAction('&Clear Terminal', self)
        clear_action.setShortcut('Ctrl+L')
        clear_action.triggered.connect(self.terminal.clear_output)
        edit_menu.addAction(clear_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        theme_menu = view_menu.addMenu('&Theme')
        
        light_action = QAction('&Light', self)
        light_action.triggered.connect(lambda: self.change_theme(AppTheme.light()))
        theme_menu.addAction(light_action)
        
        dark_action = QAction('&Dark', self)
        dark_action.triggered.connect(lambda: self.change_theme(AppTheme.dark()))
        theme_menu.addAction(dark_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def setup_main_widget(self):
        """Setup main application widget"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create vertical splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Top widget (project configuration)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        self.setup_project_form(top_layout)
        splitter.addWidget(top_widget)
        
        # Bottom widget (terminal)
        self.terminal = TerminalOutput()
        splitter.addWidget(self.terminal)
        
        # Set initial splitter sizes
        splitter.setSizes([600, 200])
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(splitter)
        
    def setup_project_form(self, layout: QVBoxLayout):
        """Setup project configuration form"""
        # Project Configuration
        config_group = QGroupBox("Project Configuration")
        config_layout = QGridLayout()
        
        # Project Name
        name_label = QLabel("Project Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("my-awesome-project")
        self.name_input.textChanged.connect(self.update_project_config)
        
        config_layout.addWidget(name_label, 0, 0)
        config_layout.addWidget(self.name_input, 0, 1)
        
        # Template
        template_label = QLabel("Template:")
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "react", "next", "remix", "gatsby"
        ])
        self.template_combo.currentTextChanged.connect(self.update_project_config)
        
        config_layout.addWidget(template_label, 1, 0)
        config_layout.addWidget(self.template_combo, 1, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Features
        features_group = QGroupBox("Features")
        features_layout = QGridLayout()
        
        self.typescript_check = QCheckBox("TypeScript")
        self.eslint_check = QCheckBox("ESLint")
        self.prettier_check = QCheckBox("Prettier")
        self.testing_check = QCheckBox("Testing")
        
        for check in [self.typescript_check, self.eslint_check,
                     self.prettier_check, self.testing_check]:
            check.stateChanged.connect(self.update_project_config)
        
        features_layout.addWidget(self.typescript_check, 0, 0)
        features_layout.addWidget(self.eslint_check, 0, 1)
        features_layout.addWidget(self.prettier_check, 1, 0)
        features_layout.addWidget(self.testing_check, 1, 1)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Styling
        styling_group = QGroupBox("Styling Solution")
        styling_layout = QVBoxLayout()
        
        self.styling_combo = QComboBox()
        self.styling_combo.addItems([
            "Tailwind CSS",
            "Styled Components",
            "CSS Modules",
            "None"
        ])
        self.styling_combo.currentTextChanged.connect(self.update_project_config)
        
        styling_layout.addWidget(self.styling_combo)
        styling_group.setLayout(styling_layout)
        layout.addWidget(styling_group)
        
        # Git Integration
        git_group = QGroupBox("Git Integration")
        git_layout = QVBoxLayout()
        
        self.git_check = QCheckBox("Initialize Git repository")
        self.git_check.setChecked(True)
        self.git_check.stateChanged.connect(self.update_project_config)
        
        git_layout.addWidget(self.git_check)
        git_group.setLayout(git_layout)
        layout.addWidget(git_group)
        
        # Action Buttons
        buttons_layout = QHBoxLayout()
        
        create_btn = QPushButton("Create Project")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        create_btn.clicked.connect(self.create_project)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addWidget(create_btn)
        layout.addLayout(buttons_layout)
        
    def update_project_config(self):
        """Update project configuration based on form values"""
        self.project_config = ProjectConfig(
            name=self.name_input.text(),
            template=self.template_combo.currentText(),
            dependencies=[],
            dev_dependencies=[],
            git_integration=self.git_check.isChecked(),
            test_framework="jest" if self.testing_check.isChecked() else None,
            styling_solution=self.styling_combo.currentText(),
            typescript=self.typescript_check.isChecked(),
            eslint=self.eslint_check.isChecked(),
            prettier=self.prettier_check.isChecked()
        )
        
    def create_project(self):
        """Start project creation process"""
        if not self.project_config.name:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Project name is required!"
            )
            return
            
        # Create worker thread
        self.project_worker = ProjectWorker(
            self.project_config,
            self.npm_path,
            self.npx_path
        )
        
        # Connect signals
        self.project_worker.progress.connect(self.update_progress)
        self.project_worker.terminal_output.connect(self.terminal.append_output)
        self.project_worker.finished.connect(self.handle_completion)
        
        # Show progress dialog
        self.progress_dialog = QProgressDialog(
            "Creating project...",
            None,
            0,
            100,
            self
        )
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.show()
        
        # Start worker
        self.project_worker.start()
        
    def update_progress(self, value: int, message: str):
        """Update progress dialog"""
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.setValue(value)
        
    def handle_completion(self, success: bool, message: str):
        """Handle project creation completion"""
        self.progress_dialog.close()
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.save_settings()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create project: {message}"
            )
            
    def change_theme(self, theme: AppTheme):
        """Change application theme"""
        self.current_theme = theme
        self.apply_theme()
        self.save_settings()
        
    def apply_theme(self):
        """Apply current theme to application"""
        # Main window styles
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.current_theme.background};
                color: {self.current_theme.text};
            }}
            QLabel {{
                color: {self.current_theme.text};
            }}
            QGroupBox {{
                color: {self.current_theme.text};
                border: 1px solid {self.current_theme.secondary};
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
        """)
        
        # Update terminal colors
        self.terminal.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.current_theme.terminal_background};
                color: {self.current_theme.terminal_text};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        
    def load_settings(self):
        """Load application settings"""
        theme_name = self.settings.value("theme", "light")
        self.change_theme(
            AppTheme.dark() if theme_name == "dark" else AppTheme.light()
        )
        
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("theme", self.current_theme.name)
        
    def show_about_dialog(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "A professional-grade tool for automating React project creation"
        )
        
    def setup_npm_paths(self):
        """Setup npm and npx paths"""
        self.npm_path = shutil.which('npm')
        self.npx_path = shutil.which('npx')
        
        if not all([self.npm_path, self.npx_path]):
            QMessageBox.critical(
                self,
                "Error",
                "Node.js and npm must be installed and in PATH"
            )
            sys.exit(1)
            
    def clear_form(self):
        """Clear form inputs"""
        self.name_input.clear()
        self.template_combo.setCurrentIndex(0)
        self.typescript_check.setChecked(False)
        self.eslint_check.setChecked(False)
        self.prettier_check.setChecked(False)
        self.testing_check.setChecked(False)
        self.styling_combo.setCurrentIndex(0)
        self.git_check.setChecked(True)

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application info
    app.setApplicationName("React Automation Tool")
    app.setApplicationVersion("v2.0")
    app.setOrganizationName("Melih Can Demir")
    
    # Create and show main window
    window = ModernReactAutomator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()