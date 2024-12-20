"""
Modern React Project Automator
-----------------------------
A professional-grade desktop application for automating React project creation
with advanced features and industry-standard practices.

Author: Melih Can Demir, Claude AI, ChatGPT and Other Pre-Trained Models
Version: 3.2.3
License: MIT
"""

import sys
import os
import subprocess
import shutil
import json
import git
import logging
import re
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
    QFileDialog, QInputDialog, QRadioButton, QStatusBar, QSizePolicy
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, QLinearGradient, QBrush, QIcon,
    QPainter, QPaintEvent, QFontDatabase, QTextCharFormat,
    QSyntaxHighlighter, QTextCursor, QKeySequence, QTextDocument, QDesktopServices
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QRect, QProcess, QSettings, QPoint, QRegExp, QUrl
)

from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet

from app_icon import AppIcon
from appicons import AppIcons

# Application Constants
APP_NAME = "Modern React Project Automator"
APP_VERSION = "3.2.3"
ORGANIZATION_NAME = "ReactAutomator"
SETTINGS_FILE = "config.json"

@dataclass
class AppTheme:
    """Theme configuration for the application"""
    name: str
    primary: str
    secondary: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    accent: str
    error: str
    success: str
    warning: str
    info: str
    border: str
    terminal_bg: str
    terminal_text: str
    
    @classmethod
    def light(cls) -> 'AppTheme':
        return cls(
            name="light",
            primary="#2563eb",
            secondary="#4b5563",
            background="#ffffff",
            surface="#f3f4f6",
            text_primary="#1f2937",
            text_secondary="#6b7280",
            accent="#3b82f6",
            error="#ef4444",
            success="#10b981",
            warning="#f59e0b",
            info="#3b82f6",
            border="#e5e7eb",
            terminal_bg="#1a1a1a",
            terminal_text="#00ff00"
        )
    
    @classmethod
    def dark(cls) -> 'AppTheme':
        return cls(
            name="dark",
            primary="#3b82f6",
            secondary="#9ca3af",
            background="#1f2937",
            surface="#374151",
            text_primary="#f9fafb",
            text_secondary="#d1d5db",
            accent="#60a5fa",
            error="#f87171",
            success="#34d399",
            warning="#fbbf24",
            info="#60a5fa", 
            border="#4b5563",
            terminal_bg="#000000",
            terminal_text="#00ff00"
        )

@dataclass
class ProjectConfig:
    """Configuration for React project creation"""
    name: str
    template: str
    dependencies: List[str]
    dev_dependencies: List[str]
    git_integration: bool
    testing: bool
    test_framework: Optional[str]
    styling_solution: str
    typescript: bool
    eslint: bool
    prettier: bool
    package_manager: str
    router: bool
    state_management: Optional[str]
    ci_cd: bool
    deployment_platform: Optional[str]
    
    @classmethod
    def create_default(cls) -> 'ProjectConfig':
        return cls(
            name="",
            template="react",
            dependencies=[],
            dev_dependencies=[],
            git_integration=True,
            testing=True,
            test_framework="vitest",
            styling_solution="Tailwind CSS",
            typescript=True,
            eslint=True,
            prettier=True,
            package_manager="npm",
            router=True,
            state_management="Redux Toolkit",
            ci_cd=True,
            deployment_platform="Vercel"
        )

class ModernButton(QPushButton):
    """Custom styled button component"""
    def __init__(
        self, 
        text: str, 
        parent=None, 
        primary: bool = False,
        icon: Optional[QIcon] = None,
        theme: Optional[AppTheme] = None
    ):
        super().__init__(text, parent)
        self.primary = primary
        if icon:
            self.setIcon(icon)

        self.theme = theme or AppTheme.light()
        self.setup_styles()
    
    def get_main_window(self):
        """Ana pencereyi bul"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ModernReactAutomator):
                return parent
            parent = parent.parent()
        return None
        
    def setup_styles(self):
        color = self.theme.primary if self.primary else self.theme.secondary
        hover_color = self.theme.accent if self.primary else self.theme.text_secondary
        text_color = "white"
        
        self.setStyleSheet(f"""
            ModernButton {{
                min-width: 100px;
                background-color: {color};
                color: {text_color};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }}
            ModernButton:hover {{
                background-color: {hover_color};
            }}
            ModernButton:pressed {{
                transform: translateY(1px);
            }}
            ModernButton:disabled {{
                background-color: {self.theme.border};
                color: {self.theme.text_secondary};
            }}
        """)

class DependencyManager(QWidget):
    """Widget for managing project dependencies"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.dependencies = []
        self.setup_ui()
    
    def add_package(self, package_name: str):
        """Yeni paket ekle"""
        if package_name not in self.dependencies:
            self.dependencies.append(package_name)
            # Terminal'e log ekle
            if hasattr(self.main_window, 'terminal'):
                self.main_window.terminal.append_output(
                    f"Package added: {package_name}",
                    "INFO"
                )
            # Paket listesini güncelle
            self.update_package_list()
    
    def remove_package(self, package_name: str):
        """Paketi kaldır"""
        if package_name in self.dependencies:
            self.dependencies.remove(package_name)
            if hasattr(self.main_window, 'terminal'):
                self.main_window.terminal.append_output(
                    f"Package removed: {package_name}",
                    "INFO"
                )
            self.update_package_list()
    
    def update_package_list(self):
        """Paket listesini güncelle"""
        self.package_list.clear()
        for pkg in self.dependencies:
            self.package_list.append(f"• {pkg}")
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Package search
        search_box = QLineEdit(self)
        search_box.setPlaceholderText("Search packages...")
        layout.addWidget(search_box)
        
        # Package list
        self.package_list = QTextEdit(self)
        self.package_list.setReadOnly(True)
        layout.addWidget(self.package_list)
        
        # Popular packages suggestions
        suggestions_group = QGroupBox("Popular Packages")
        suggestions_layout = QGridLayout()
        
        popular_packages = [
            "react-router-dom",
            "@reduxjs/toolkit",
            "axios",
            "react-query",
            "formik",
            "react-hook-form",
            "zod",
            "date-fns"
        ]
        
        row = 0
        col = 0
        for pkg in popular_packages:
            btn = ModernButton(
                pkg, 
                self, 
                theme=self.main_window.current_theme if self.main_window else None
            )
            btn.clicked.connect(lambda p=pkg: self.add_package(p))
            suggestions_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
                
        suggestions_group.setLayout(suggestions_layout)
        layout.addWidget(suggestions_group)
        
        # Add custom package section
        custom_group = QGroupBox("Add Custom Package")
        custom_layout = QHBoxLayout()
        
        self.custom_package = QLineEdit()
        self.custom_package.setPlaceholderText("Package name (@scope/name@version)")
        
        add_btn = ModernButton(
            "Add",
            self,
            primary=True,
            theme=self.main_window.current_theme if self.main_window else None
        )
        add_btn.clicked.connect(lambda: self.add_package(self.custom_package.text()))
        
        custom_layout.addWidget(self.custom_package)
        custom_layout.addWidget(add_btn)
        
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
    
class GitIntegration(QWidget):
    """Widget for Git repository configuration"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.current_worker = None
        self.selected_project = None
        self.setup_ui()
        self.update_button_states(initial=True)
    
    def closeEvent(self, event):
        """Widget kapatılırken çalışan worker'ı durdur"""
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
        super().closeEvent(event)
    
    def setup_ui(self):
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Scroll için içerik widget'ı
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Proje Seçimi
        project_group = QGroupBox("Project Selection")
        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(10, 15, 10, 10)
        
        self.project_path = QLineEdit()
        self.project_path.setPlaceholderText("Select a React project...")
        self.project_path.setReadOnly(True)
        
        select_btn = ModernButton(
            "Browse",
            self,
            icon=AppIcons.get_folder_icon()
        )
        select_btn.clicked.connect(self.select_project)
        select_btn.setFixedWidth(100)
        
        project_layout.addWidget(self.project_path)
        project_layout.addWidget(select_btn)
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Remote Repository Configuration
        remote_group = QGroupBox("Remote Repository")
        remote_layout = QGridLayout()
        remote_layout.setContentsMargins(10, 15, 10, 10)
        remote_layout.setSpacing(10)
        
        # URL Input
        url_label = QLabel("Remote URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://github.com/username/repo.git")
        
        # Branch Selection - Yatayda hizalama düzeltmesi
        branch_label = QLabel("Branch:")
        branch_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(["main", "master", "develop", "staging"])
        self.branch_combo.setEditable(True)
        
        # Grid'e widget'ları ekle
        remote_layout.addWidget(url_label, 0, 0)
        remote_layout.addWidget(self.url_input, 0, 1)
        remote_layout.addWidget(branch_label, 1, 0)
        remote_layout.addWidget(self.branch_combo, 1, 1)
        
        # Kolonların genişlik ayarı
        remote_layout.setColumnStretch(1, 1)  # URL input ve branch combo genişleyebilir
        
        remote_group.setLayout(remote_layout)
        layout.addWidget(remote_group)
        
        # Git Operations
        operations_group = QGroupBox("Git Operations")
        operations_layout = QVBoxLayout()
        operations_layout.setContentsMargins(10, 15, 10, 10)
        operations_layout.setSpacing(10)
        
        # Initialize Repository
        self.init_btn = ModernButton(
            "Initialize Repository",
            self,
            icon=AppIcons.get_git_init_icon(),
            theme=self.main_window.current_theme if self.main_window else None
        )
        self.init_btn.clicked.connect(self.init_repository)
        
        # Changed Files
        changes_label = QLabel("Changed Files:")
        self.changes_list = QTextEdit()
        self.changes_list.setReadOnly(True)
        self.changes_list.setPlaceholderText("No changes detected")
        self.changes_list.setMinimumHeight(100)
        self.changes_list.setMaximumHeight(150)
        
        # Commit Message
        commit_label = QLabel("Commit Message:")
        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Enter commit message...")
        
        self.commit_btn = ModernButton(
            "Commit Changes",
            self,
            icon=AppIcons.get_git_commit_icon(),
            theme=self.main_window.current_theme if self.main_window else None
        )
        self.commit_btn.clicked.connect(self.create_commit)
        
        # Push to Remote
        self.push_btn = ModernButton(
            "Push to Remote",
            self,
            icon=AppIcons.get_git_push_icon(),
            theme=self.main_window.current_theme if self.main_window else None
        )
        self.push_btn.clicked.connect(self.push_to_remote)
        
        # Add widgets to operations layout
        operations_layout.addWidget(self.init_btn)
        operations_layout.addWidget(changes_label)
        operations_layout.addWidget(self.changes_list)
        operations_layout.addWidget(commit_label)
        operations_layout.addWidget(self.commit_msg)
        operations_layout.addWidget(self.commit_btn)
        operations_layout.addWidget(self.push_btn)
        
        operations_group.setLayout(operations_layout)
        layout.addWidget(operations_group)
        
        # Add stretch at the bottom
        layout.addStretch()
        
        # Set the content widget to scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Set initial button states
        self.update_button_states(initial=True)
        
        # Style adjustments
        self.setStyleSheet("""
            QGroupBox {
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 5px;
                padding: 0 2px;
            }
            QLabel {
                min-width: 100px;
            }
        """)
    
    def select_project(self):
        """Select a project directory for Git operations"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Project Directory",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            # Validate if it's a valid Git repository or can be one
            if os.path.exists(os.path.join(directory, ".git")):
                self.selected_project = directory
                self.project_path.setText(directory)
                self.update_git_status()
                self.main_window.terminal.append_output(
                    f"Selected Git project: {directory}",
                    "INFO"
                )
            else:
                # Check if it's a valid project directory
                if os.path.exists(os.path.join(directory, "package.json")):
                    self.selected_project = directory
                    self.project_path.setText(directory)
                    self.init_btn.setEnabled(True)
                    self.main_window.terminal.append_output(
                        f"Selected project directory: {directory}",
                        "INFO"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Invalid Project",
                        "Selected directory is not a valid React project!"
                    )
    
    def update_git_status(self):
        """Update Git repository status"""
        if not self.selected_project:
            self.changes_list.setText("No project selected")
            return
            
        try:
            repo = git.Repo(self.selected_project)
            
            # List changes
            changes = []
            
            # Untracked files
            for item in repo.untracked_files:
                changes.append(f"New: {item}")
            
            # Modified files
            for item in repo.index.diff(None):
                changes.append(f"Modified: {item.a_path}")
                
            if changes:
                self.changes_list.setText("\n".join(changes))
            else:
                self.changes_list.setText("No changes detected")
                
            # Update button states
            self.update_button_states()
            
        except git.InvalidGitRepositoryError:
            self.changes_list.setText("Not a Git repository")
            self.update_button_states()
    
    def create_commit(self):
        """Create initial commit"""
        if not self.commit_msg.text():
            QMessageBox.warning(
                self, 
                "Hata", 
                "Lütfen bir commit mesajı girin!"
            )
            return
            
        if not self.selected_project:
            QMessageBox.warning(
                self,
                "Hata",
                "Lütfen önce bir proje seçin!"
            )
            return

        # Eğer hala çalışan bir worker varsa onu durdur
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            
        # Yeni worker'ı oluştur ve referansını sakla
        self.current_worker = GitWorker(
            repo_path=self.selected_project,
            operation='commit',
            commit_message=self.commit_msg.text()
        )
        self.current_worker.progress.connect(lambda msg: self.main_window.terminal.append_output(msg, "INFO"))
        self.current_worker.finished.connect(self.handle_git_operation)
        self.current_worker.start()
    
    def closeEvent(self, event):
        """Widget kapatılırken çalışan worker'ı durdur"""
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
        super().closeEvent(event)

    
    def update_button_states(self, initial=False):
        """Update Git operation button states"""
        if initial:
            self.init_btn.setEnabled(False)
            self.commit_btn.setEnabled(False)
            self.push_btn.setEnabled(False)
            return
            
        has_git = os.path.exists(os.path.join(self.selected_project, ".git")) if self.selected_project else False
        
        self.init_btn.setEnabled(not has_git and self.selected_project is not None)
        self.commit_btn.setEnabled(has_git)
        self.push_btn.setEnabled(has_git)
        
    def init_repository(self):
        """Initialize Git repository"""
        # First check if we have a valid project path
        project_path = None
        
        # Check for selected existing project
        if hasattr(self, 'selected_project') and self.selected_project:
            project_path = self.selected_project
        # Check main window's project directory
        elif hasattr(self.main_window, 'project_directory') and self.main_window.project_directory:
            project_path = os.path.join(
                self.main_window.project_directory,
                self.main_window.project_config.name
            ) if hasattr(self.main_window, 'project_config') else self.main_window.project_directory
            
        if not project_path:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a project directory first."
            )
            return
            
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            
        self.current_worker = GitWorker(project_path, 'init')
        self.current_worker.progress.connect(
            lambda msg: self.main_window.terminal.append_output(msg, "INFO")
        )
        self.current_worker.finished.connect(self.handle_git_operation)
        self.current_worker.start()

    def push_to_remote(self):
        """Push changes to remote repository"""
        if not self.selected_project:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a project directory first."
            )
            return
            
        remote_url = self.url_input.text().strip()
        if not remote_url:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter remote repository URL"
            )
            return
            
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            
        self.current_worker = GitWorker(
            self.selected_project,
            'push',
            remote_url=remote_url,
            branch=self.branch_combo.currentText()
        )
        self.current_worker.progress.connect(
            lambda msg: self.main_window.terminal.append_output(msg, "INFO")
        )
        self.current_worker.finished.connect(self.handle_git_operation)
        self.current_worker.start()

    def handle_git_operation(self, success: bool, message: str):
        """Handle Git operation completion"""
        if success:
            self.main_window.terminal.append_output(message, "SUCCESS")
            
            # İşlem başarılıysa bir sonraki butonu aktif et
            if "initialized" in message.lower():
                self.init_btn.setEnabled(False)
                self.commit_btn.setEnabled(True)
            elif "committed" in message.lower():
                self.commit_btn.setEnabled(False)
                self.push_btn.setEnabled(True)
            elif "pushed" in message.lower():
                self.push_btn.setEnabled(False)
        else:
            self.main_window.terminal.append_output(f"Git operation failed: {message}", "ERROR")
            QMessageBox.critical(self, "Error", f"Git operation failed: {message}")

class ProjectAnalytics(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Chart view area
        charts_container = QWidget()
        charts_layout = QHBoxLayout(charts_container)
        
        # Dependencies chart
        deps_chart = QChart()
        deps_chart.setAnimationOptions(QChart.SeriesAnimations)
        deps_chart.setTitle("Dependencies Distribution")
        
        deps_series = QPieSeries()
        deps_series.append("Runtime", 15)
        deps_series.append("Development", 8)
        deps_series.append("Peer", 3)
        
        deps_chart.addSeries(deps_series)
        deps_view = QChartView(deps_chart)
        deps_view.setRenderHint(QPainter.Antialiasing)
        charts_layout.addWidget(deps_view)
        
        # Bundle size chart
        bundle_chart = QChart()
        bundle_chart.setAnimationOptions(QChart.SeriesAnimations)
        bundle_chart.setTitle("Bundle Size Analysis")
        
        bundle_series = QBarSeries()
        bundle_set = QBarSet("Size (KB)")
        bundle_set.append([120, 45, 25, 15])
        bundle_series.append(bundle_set)
        
        bundle_chart.addSeries(bundle_series)
        bundle_view = QChartView(bundle_chart)
        bundle_view.setRenderHint(QPainter.Antialiasing)
        charts_layout.addWidget(bundle_view)
        
        layout.addWidget(charts_container)
        
        # Project statistics
        stats_group = QGroupBox("Project Statistics")
        stats_layout = QGridLayout()
        
        stats = [
            ("Total Dependencies:", "26"),
            ("Build Time:", "2.3s"),
            ("Last Updated:", "2 hours ago"),
            ("Bundle Size:", "205 KB"),
            ("Test Coverage:", "87%"),
            ("Contributors:", "3")
        ]
        
        row = 0
        col = 0
        for label, value in stats:
            label_widget = QLabel(label)
            value_widget = QLabel(value)
            stats_layout.addWidget(label_widget, row, col)
            stats_layout.addWidget(value_widget, row, col + 1)
            col += 2
            if col >= 4:
                col = 0
                row += 1
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Apply theme
        if hasattr(self.main_window, 'current_theme'):
            theme = self.main_window.current_theme
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme.background};
                    color: {theme.text_primary};
                }}
                QGroupBox {{
                    background-color: {theme.surface};
                    border: 1px solid {theme.border};
                    border-radius: 8px;
                    margin-top: 1em;
                    padding: 15px;
                }}
                QGroupBox::title {{
                    color: {theme.text_primary};
                }}
                QLabel {{
                    color: {theme.text_primary};
                }}
                QChart {{
                    background-color: {theme.surface};
                }}
                QChartView {{
                    background-color: {theme.surface};
                }}
            """)

            # Apply chart themes
            deps_chart.setTheme(QChart.ChartThemeDark if theme.name == "dark" else QChart.ChartThemeLight)
            bundle_chart.setTheme(QChart.ChartThemeDark if theme.name == "dark" else QChart.ChartThemeLight)

class ProjectWorker(QThread):
    """Worker thread for project creation tasks"""
    progress = pyqtSignal(int, str)
    terminal_output = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, config: ProjectConfig, npm_path: str, npx_path: str, project_directory: str):
        super().__init__()
        self.config = config
        self.npm_path = npm_path
        self.npx_path = npx_path
        self.project_directory = project_directory
        
    def emit_log(self, message: str, level: str = "INFO"):
        self.terminal_output.emit(message, level)
        
    def run_process(self, command: List[str], shell: bool = False) -> bool:
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        
        def handle_output():
            output = process.readAll().data().decode()
            self.terminal_output.emit(output, "INFO")
            
        process.readyReadStandardOutput.connect(handle_output)
        process.readyReadStandardError.connect(handle_output)
        
        if shell:
            process.start(command[0], command[1:])
        else:
            process.start(command[0], command[1:])
            
        process.waitForFinished()
        return process.exitCode() == 0

    def run(self):
        try:
            self.progress.emit(0, "Initializing project...")
            self.emit_log("Starting project creation...")

            os.chdir(self.project_directory)
            
            # Create project directory
            project_path = Path(self.project_directory) / self.config.name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize project
            self.progress.emit(20, "Creating project structure...")
            template_suffix = "-ts" if self.config.typescript else ""
            template = f"{self.config.template}{template_suffix}"
            
            if self.config.template == "next":
                create_cmd = [
                    "create-next-app",
                    self.config.name,
                    "--typescript" if self.config.typescript else "",
                    "--tailwind" if self.config.styling_solution == "Tailwind CSS" else "",
                    "--eslint" if self.config.eslint else "",
                    "--src-dir",
                    "--app"
                ]
            else:
                create_cmd = [
                    self.npx_path,
                    "create-vite@latest",
                    self.config.name,
                    "--template",
                    template
                ]
            
            success = self.run_process(create_cmd)
            if not success:
                raise Exception("Failed to create project structure")
            
            # Change to project directory
            os.chdir(project_path)
            
            # Install dependencies
            self.progress.emit(40, "Installing dependencies...")
            self.emit_log("Installing core dependencies...")
            
            install_cmd = [self.npm_path, "install"]
            success = self.run_process(install_cmd)
            if not success:
                raise Exception("Failed to install core dependencies")
            
            # Install additional features
            self.progress.emit(60, "Setting up project features...")
            self.setup_features()
            
            # Setup testing
            if self.config.testing:
                self.setup_testing()
            
            # Setup router
            if self.config.router:
                self.setup_router()
            
            # Setup state management
            if self.config.state_management:
                self.setup_state_management()
            
            # Setup CI/CD
            if self.config.ci_cd:
                self.setup_ci_cd()
            
            # Initialize git
            if self.config.git_integration:
                self.setup_git()
            
            self.progress.emit(100, "Project created successfully!")
            self.emit_log("Project setup completed successfully!", "SUCCESS")
            self.finished.emit(True, "Project created successfully!")
            
        except Exception as e:
            self.emit_log(f"Error: {str(e)}", "ERROR")
            self.finished.emit(False, str(e))
            
    def setup_features(self):
        """Setup additional project features"""
        try:
            # Setup TypeScript
            if self.config.typescript:
                self.setup_typescript()
            
            # Setup styling
            if self.config.styling_solution:
                self.setup_styling()
            
            # Setup linting
            if self.config.eslint or self.config.prettier:
                self.setup_linting()
                
        except Exception as e:
            self.emit_log(f"Error setting up features: {str(e)}", "ERROR")
            raise
            
    def setup_typescript(self):
        """Configure TypeScript"""
        self.emit_log("Setting up TypeScript...")
        
        ts_config = {
            "compilerOptions": {
                "target": "ESNext",
                "lib": ["DOM", "DOM.Iterable", "ESNext"],
                "allowJs": False,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "module": "ESNext",
                "moduleResolution": "Node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"]
                }
            },
            "include": ["src"],
            "references": [{ "path": "./tsconfig.node.json" }]
        }
        
        with open("tsconfig.json", "w") as f:
            json.dump(ts_config, f, indent=2)
            
    def setup_styling(self):
        """Configure styling solution"""
        self.emit_log(f"Setting up {self.config.styling_solution}...")
        
        if self.config.styling_solution == "Tailwind CSS":
            self.setup_tailwind()
        elif self.config.styling_solution == "Styled Components":
            self.setup_styled_components()
        elif self.config.styling_solution == "CSS Modules":
            self.setup_css_modules()
            
    def setup_tailwind(self):
        """Configure Tailwind CSS"""
        deps = ["tailwindcss", "postcss", "autoprefixer"]
        success = self.run_process([
            self.npm_path, "install", "-D",
            *deps
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
                "./src/**/*.{js,ts,jsx,tsx}",
            ],
            "theme": {
                "extend": {},
            },
            "plugins": [],
        }
        
        with open("tailwind.config.js", "w") as f:
            f.write(f"module.exports = {json.dumps(tailwind_config, indent=2)}")
            
        # Add Tailwind directives to CSS
        css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;
        """
        
        with open("src/index.css", "w") as f:
            f.write(css_content.strip())
            
    def setup_styled_components(self):
        """Configure Styled Components"""
        deps = ["styled-components"]
        if self.config.typescript:
            deps.append("@types/styled-components")
            
        success = self.run_process([
            self.npm_path, "install",
            *deps
        ])
        
        if not success:
            raise Exception("Failed to install Styled Components")
            
        # Create theme file
        theme = """
export const theme = {
    colors: {
        primary: '#2563eb',
        secondary: '#4b5563',
        background: '#ffffff',
        surface: '#f3f4f6',
        text: '#1f2937',
        accent: '#3b82f6',
    },
    breakpoints: {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
    },
    spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem',
    },
    typography: {
        h1: '2.25rem',
        h2: '1.875rem',
        h3: '1.5rem',
        body: '1rem',
        small: '0.875rem',
    },
}
        """
        
        os.makedirs("src/styles", exist_ok=True)
        with open("src/styles/theme.ts", "w") as f:
            f.write(theme.strip())
            
    def setup_css_modules(self):
        """Configure CSS Modules"""
        # Create example module
        example_module = """
.container {
    padding: 2rem;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    color: #2563eb;
}

.button {
    padding: 0.5rem 1rem;
    background-color: #2563eb;
    color: white;
    border-radius: 0.375rem;
    transition: background-color 0.2s;
}

.button:hover {
    background-color: #1d4ed8;
}
        """
        
        os.makedirs("src/styles", exist_ok=True)
        with open("src/styles/Example.module.css", "w") as f:
            f.write(example_module.strip())
            
    def setup_linting(self):
        """Configure ESLint and Prettier"""
        if self.config.eslint:
            self.emit_log("Setting up ESLint...")
            
            deps = [
                "eslint",
                "eslint-plugin-react",
                "eslint-plugin-react-hooks",
                "eslint-plugin-jsx-a11y",
                "@typescript-eslint/parser",
                "@typescript-eslint/eslint-plugin"
            ]
            
            success = self.run_process([
                self.npm_path, "install", "-D",
                *deps
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
                    "plugin:jsx-a11y/recommended",
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
                    "react-hooks",
                    "jsx-a11y",
                    "@typescript-eslint"
                ],
                "rules": {
                    "react/react-in-jsx-scope": "off",
                    "react/prop-types": "off"
                },
                "settings": {
                    "react": {
                        "version": "detect"
                    }
                }
            }
            
            with open(".eslintrc.json", "w") as f:
                json.dump(eslint_config, f, indent=2)
                
        if self.config.prettier:
            self.emit_log("Setting up Prettier...")
            
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
                "tabWidth": 2,
                "useTabs": False,
                "bracketSpacing": True,
                "jsxBracketSameLine": False
            }
            
            with open(".prettierrc", "w") as f:
                json.dump(prettier_config, f, indent=2)
                
    def setup_testing(self):
        """Configure testing framework"""
        self.emit_log("Setting up testing configuration...")
        
        if self.config.test_framework == "vitest":
            deps = [
                "vitest",
                "@testing-library/react",
                "@testing-library/user-event",
                "@testing-library/jest-dom",
                "jsdom"
            ]
        else:
            deps = [
                "jest",
                "@testing-library/react",
                "@testing-library/user-event",
                "@testing-library/jest-dom",
                "@types/jest"
            ]
            
        success = self.run_process([
            self.npm_path, "install", "-D",
            *deps
        ])
        
        if not success:
            raise Exception("Failed to install testing dependencies")
            
        # Create test setup
        if self.config.test_framework == "vitest":
            setup = """
import '@testing-library/jest-dom'
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

afterEach(() => {
    cleanup()
})
            """
            
            os.makedirs("src/test", exist_ok=True)
            with open("src/test/setup.ts", "w") as f:
                f.write(setup.strip())
                
            # Create example test
            example_test = """
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from '../App'

describe('App', () => {
    it('renders hello world', () => {
        render(<App />)
        expect(screen.getByText(/hello/i)).toBeInTheDocument()
    })
})
            """
            
            with open("src/test/App.test.tsx", "w") as f:
                f.write(example_test.strip())
                
    def setup_router(self):
        """Configure React Router"""
        self.emit_log("Setting up React Router...")
        
        success = self.run_process([
            self.npm_path, "install",
            "react-router-dom"
        ])
        
        if not success:
            raise Exception("Failed to install React Router")
            
        # Create router configuration
        router_config = """
import { createBrowserRouter } from 'react-router-dom'
import App from '../App'
import Home from '../pages/Home'
import About from '../pages/About'
import NotFound from '../pages/NotFound'

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {
                index: true,
                element: <Home />
            },
            {
                path: 'about',
                element: <About />
            },
            {
                path: '*',
                element: <NotFound />
            }
        ]
    }
])
        """
        
        os.makedirs("src/router", exist_ok=True)
        with open("src/router/index.tsx", "w") as f:
            f.write(router_config.strip())
            
        # Create page components
        pages = {
            "Home": """
export default function Home() {
    return (
        <div>
            <h1>Home Page</h1>
            <p>Welcome to our app!</p>
        </div>
    )
}
            """,
            "About": """
export default function About() {
    return (
        <div>
            <h1>About Page</h1>
            <p>Learn more about us.</p>
        </div>
    )
}
            """,
            "NotFound": """
export default function NotFound() {
    return (
        <div>
            <h1>404</h1>
            <p>Page not found.</p>
        </div>
    )
}
            """
        }
        
        os.makedirs("src/pages", exist_ok=True)
        for name, content in pages.items():
            with open(f"src/pages/{name}.tsx", "w") as f:
                f.write(content.strip())
                
    def setup_state_management(self):
        """Configure state management solution"""
        self.emit_log(f"Setting up {self.config.state_management}...")
        
        if self.config.state_management == "Redux Toolkit":
            self.setup_redux_toolkit()
        elif self.config.state_management == "Zustand":
            self.setup_zustand()
            
    def setup_redux_toolkit(self):
        """Configure Redux Toolkit"""
        deps = ["@reduxjs/toolkit", "react-redux"]
        
        success = self.run_process([
            self.npm_path, "install",
            *deps
        ])
        
        if not success:
            raise Exception("Failed to install Redux Toolkit")
            
        # Create store configuration
        store_config = """
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './slices/counterSlice'

export const store = configureStore({
    reducer: {
        counter: counterReducer
    }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
        """
        
        os.makedirs("src/store", exist_ok=True)
        with open("src/store/index.ts", "w") as f:
            f.write(store_config.strip())
            
        # Create example slice
        counter_slice = """
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CounterState {
    value: number
}

const initialState: CounterState = {
    value: 0
}

export const counterSlice = createSlice({
    name: 'counter',
    initialState,
    reducers: {
        increment: (state) => {
            state.value += 1
        },
        decrement: (state) => {
            state.value -= 1
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
            state.value += action.payload
        }
    }
})

export const { increment, decrement, incrementByAmount } = counterSlice.actions
export default counterSlice.reducer
        """
        
        os.makedirs("src/store/slices", exist_ok=True)
        with open("src/store/slices/counterSlice.ts", "w") as f:
            f.write(counter_slice.strip())
            
    def setup_zustand(self):
        """Configure Zustand"""
        success = self.run_process([
            self.npm_path, "install",
            "zustand"
        ])
        
        if not success:
            raise Exception("Failed to install Zustand")
            
        # Create store
        store = """
import create from 'zustand'

interface CounterState {
    count: number
    increment: () => void
    decrement: () => void
    reset: () => void
}

export const useStore = create<CounterState>((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    reset: () => set({ count: 0 })
}))
        """
        
        os.makedirs("src/store", exist_ok=True)
        with open("src/store/index.ts", "w") as f:
            f.write(store.strip())
            
    def setup_ci_cd(self):
        """Configure CI/CD workflow"""
        self.emit_log("Setting up CI/CD configuration...")
        
        if self.config.deployment_platform == "Vercel":
            self.setup_vercel_deployment()
        
        # Create GitHub Actions workflow
        workflow = """
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [16.x, 18.x]

    steps:
    - uses: actions/checkout@v2
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v2
      with:
        node-version: ${{ matrix.node-version }}
        
    - name: Install dependencies
      run: npm ci
      
    - name: Run tests
      run: npm test
      
    - name: Build
      run: npm run build
      
    - name: Lint
      run: npm run lint
        """
        
        os.makedirs(".github/workflows", exist_ok=True)
        with open(".github/workflows/ci.yml", "w") as f:
            f.write(workflow.strip())
            
    def setup_vercel_deployment(self):
        """Configure Vercel deployment"""
        vercel_config = """
{
    "version": 2,
    "builds": [
        {
            "src": "package.json",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "dist"
            }
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "/index.html"
        }
    ]
}
        """
        
        with open("vercel.json", "w") as f:
            f.write(vercel_config.strip())
            
    def setup_git(self):
        """Initialize Git repository"""
        self.emit_log("Initializing Git repository...")
        
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

# TypeScript
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Vercel
.vercel
            """
            
            with open(".gitignore", "w") as f:
                f.write(gitignore.strip())
                
            # Initial commit
            repo.index.add(["."])
            repo.index.commit("Initial commit: Project setup")
            
            self.emit_log("Git repository initialized successfully", "SUCCESS")
            
        except Exception as e:
            self.emit_log(f"Failed to initialize Git repository: {str(e)}", "ERROR")
            raise

class GitWorker(QThread):
    """Worker thread for Git operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, repo_path: str, operation: str, commit_message: str = None, remote_url: str = None, branch: str = None):
        super().__init__()
        self.repo_path = repo_path
        self.operation = operation
        self.commit_message = commit_message
        self.remote_url = remote_url
        self.branch = branch
        self._is_running = True
    
    def stop(self):
        self._is_running = False
        self.wait()
        
    def run(self):
        try:
            if not self._is_running:
                return
            
            if self.operation == 'init':
                self.progress.emit("Initializing repository...")
                repo = git.Repo.init(self.repo_path)
                self.finished.emit(True, "Repository initialized successfully")
                
            elif self.operation == 'commit':
                self.progress.emit("Creating commit...")
                repo = git.Repo(self.repo_path)
                
                # Add untracked files excluding node_modules
                repo.index.add([
                    item for item in repo.untracked_files 
                    if not item.startswith('node_modules/')
                ])
                
                # Add modified files
                changed_files = [item.a_path for item in repo.index.diff(None)]
                repo.index.add(changed_files)
                
                # Use provided commit message or fallback to default
                message = self.commit_message if self.commit_message else "Initial commit: Project setup"
                repo.index.commit(message)
                self.finished.emit(True, f"Changes committed successfully with message: {message}")
                
            elif self.operation == 'push':
                self.progress.emit("Pushing to remote...")
                repo = git.Repo(self.repo_path)
                
                # Add or update remote
                try:
                    origin = repo.remote('origin')
                    origin.set_url(self.remote_url)
                except ValueError:
                    origin = repo.create_remote('origin', self.remote_url)
                
                # Create and checkout branch if needed
                if self.branch not in repo.heads:
                    repo.create_head(self.branch)
                    
                repo.heads[self.branch].checkout()
                
                # Push changes
                origin.push(refspec=f'{self.branch}:refs/heads/{self.branch}')
                self.finished.emit(True, "Changes pushed to remote successfully")
                
        except Exception as e:
            if self._is_running:
                self.finished.emit(False, str(e))

# GitIntegration sınıfına eklenecek metodlar:
def init_repository(self):
    """Initialize Git repository"""
    worker = GitWorker(self.main_window.project_directory, 'init')
    worker.progress.connect(lambda msg: self.main_window.terminal.append_output(msg, "INFO"))
    worker.finished.connect(self.handle_git_operation)
    worker.start()

def create_commit(self):
    """Create initial commit"""
    worker = GitWorker(self.main_window.project_directory, 'commit')
    worker.progress.connect(lambda msg: self.main_window.terminal.append_output(msg, "INFO"))
    worker.finished.connect(self.handle_git_operation)
    worker.start()

def push_to_remote(self):
    """Push changes to remote repository"""
    remote_url = self.url_input.text()
    branch = self.branch_combo.currentText()
    
    if not remote_url:
        QMessageBox.warning(self, "Error", "Please enter remote repository URL")
        return
        
    worker = GitWorker(
        self.main_window.project_directory,
        'push',
        remote_url=remote_url,
        branch=branch
    )
    worker.progress.connect(lambda msg: self.main_window.terminal.append_output(msg, "INFO"))
    worker.finished.connect(self.handle_git_operation)
    worker.start()

def handle_git_operation(self, success: bool, message: str):
    """Handle Git operation completion"""
    if success:
        self.main_window.terminal.append_output(message, "SUCCESS")
    else:
        self.main_window.terminal.append_output(f"Git operation failed: {message}", "ERROR")
        QMessageBox.critical(self, "Error", f"Git operation failed: {message}")



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

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search text...")
        layout.addWidget(self.search_input)
        
        # Options
        options_group = QGroupBox("Search Options")
        options_layout = QVBoxLayout()
        
        self.case_sensitive = QCheckBox("Case sensitive")
        
        direction_group = QGroupBox("Direction")
        direction_layout = QHBoxLayout()
        self.forward_radio = QRadioButton("Forward")
        self.backward_radio = QRadioButton("Backward")
        self.forward_radio.setChecked(True)
        
        direction_layout.addWidget(self.forward_radio)
        direction_layout.addWidget(self.backward_radio)
        direction_group.setLayout(direction_layout)
        
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(direction_group)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

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
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 5px;
                padding: 3px;
                background: transparent;
            }
            QToolButton {
                border: none;
                border-radius: 4px;
                padding: 4px;
                background: transparent;
            }
            QToolButton:hover {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        
        # Modern save ikonu
        save_action = QAction(self)
        save_action.setIcon(AppIcons.get_save_icon())
        save_action.setToolTip("Save Output")
        save_action.triggered.connect(self.save_output)
        toolbar.addAction(save_action)
        
        # Modern search ikonu
        search_action = QAction(self)
        search_action.setIcon(AppIcons.get_search_icon())
        search_action.setToolTip("Search")
        search_action.triggered.connect(self.show_search_dialog)
        toolbar.addAction(search_action)
        
        # Modern clear ikonu
        clear_action = QAction(self)
        clear_action.setIcon(AppIcons.get_trash_icon())
        clear_action.setToolTip("Clear")
        clear_action.triggered.connect(self.clear_output)
        toolbar.addAction(clear_action)
        
        # Modern expand ikonu
        expand_action = QAction(self)
        expand_action.setIcon(AppIcons.get_expand_icon())
        expand_action.setToolTip("Expand Terminal")
        expand_action.triggered.connect(self.show_expanded_view)
        toolbar.addAction(expand_action)
        
        layout.addWidget(toolbar)
        
        # Terminal output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.highlighter = TerminalHighlighter(self.output.document())
        layout.addWidget(self.output)
        
    def setup_logging(self):
        self.logger = logging.getLogger("TerminalOutput")
        self.logger.setLevel(logging.DEBUG)
        
    def show_expanded_view(self):
        # Yeni bir dialog oluştur
        dialog = QDialog(self)
        dialog.setWindowTitle("Expanded Terminal")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 600)  # Daha geniş bir alan
        
        dialog_layout = QVBoxLayout(dialog)
        
        # Dialog içinde terminal çıktısını göstermek için bir QTextEdit oluşturun
        expanded_output = QTextEdit()
        expanded_output.setReadOnly(True)
        expanded_output.setText(self.output.toPlainText()) # Mevcut çıktıyı al
        dialog_layout.addWidget(expanded_output)
        
        # Kapatma butonları
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)
        
        dialog.exec_()

    def save_output(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Terminal Output",
            "",
            "Text Files (*.txt);;Log Files (*.log)"
        )
        
        if filename:
            try:
                content = self.output.toPlainText()
                print(f"Debug - Content length: {len(content)}")  # İçerik uzunluğu
                
                # Dosya izinlerini kontrol et
                if not os.access(os.path.dirname(filename), os.W_OK):
                    self.logger.error("No write permission for selected location")
                    return
                    
                with open(filename, 'w', encoding='utf-8') as f:  # encoding ekledik
                    f.write(content)
                    
                # Dosya içeriğini kontrol et
                with open(filename, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                    print(f"Debug - Saved content length: {len(saved_content)}")
                    
                self.logger.info(f"Output saved to {filename}")
                
            except Exception as e:
                self.logger.error(f"Failed to save output: {str(e)}")
                print(f"Debug - Exception details: {type(e).__name__}: {str(e)}")
                
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
        self.project_config = ProjectConfig.create_default()
        
        self.init_ui()
        self.setup_modern_icons()
        self.setup_npm_paths()
        self.load_settings()
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(self.size())
        
    def init_ui(self):
        """Initialize user interface"""

        # Ana widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Başlık
        title = QLabel("Modern React Project Automator")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2563eb;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 12px 24px;
                margin-right: 4px;
                border: none;
                background: #f3f4f6;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: #2563eb;
                color: white;
            }
        """)
        
        # Project Setup Tab
        setup_tab = QWidget()
        setup_layout = QVBoxLayout(setup_tab)

        setup_scroll = QScrollArea()
        setup_scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(10)

        setup_layout.addWidget(self.setup_run_controls())

        self.setup_project_form(setup_layout)
        self.tabs.addTab(setup_tab, "Project Setup")

        
        # Dependencies Tab
        deps_tab = DependencyManager(self)
        self.tabs.addTab(deps_tab, "Dependencies")
        
        # Git Integration Tab
        git_tab = GitIntegration(self)
        self.tabs.addTab(git_tab, "Git Integration")
        
        # Analytics Tab
        analytics_tab = ProjectAnalytics(self)
        self.tabs.addTab(analytics_tab, "Analytics")
        
        # CI/CD Tab
        cicd_tab = self.setup_cicd_tab()
        self.tabs.addTab(cicd_tab, "CI/CD")
        
        # Deployment Tab
        deployment_tab = self.setup_deployment_tab()
        self.tabs.addTab(deployment_tab, "Deployment")
        
        main_layout.addWidget(self.tabs)
        
        # Terminal alanı
        self.setup_terminal()
        main_layout.addWidget(self.terminal)
        # Mevcut kodun bir kısmı
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.terminal)

        # Örneğin üst kısma (tabs_container) 3 birim, terminale 1 birim verelim:
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        
        # Menu ve status bar
        self.setup_menu_bar()
        self.setup_status_bar()
    
    def setup_modern_icons(self):
        """Modern ikonları ayarla"""
        # Uygulama ikonu
        self.setWindowIcon(AppIcon.create_app_icon())
        
        # Run kontrolü için modern ikonlar
        self.run_btn.setIcon(AppIcons.get_play_icon())
        self.browser_btn.setIcon(AppIcons.get_browser_icon())
        
        # Play/Stop toggle için
        def update_run_icon(is_running: bool):
            if is_running:
                self.run_btn.setIcon(AppIcons.get_stop_icon())
            else:
                self.run_btn.setIcon(AppIcons.get_play_icon())
        
        # Run butonu tıklandığında ikonu güncelle
        self.run_btn.clicked.connect(lambda: update_run_icon(not hasattr(self, 'project_runner') or not self.project_runner.running))

    def setup_cicd_tab(self):
        """Create CI/CD configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # CI/CD Provider Selection
        provider_group = QGroupBox("CI/CD Provider")
        provider_layout = QVBoxLayout()
        
        self.cicd_provider = QComboBox()
        self.cicd_provider.addItems([
            "GitHub Actions",
            "GitLab CI",
            "CircleCI",
            "Jenkins",
            "Azure DevOps"
        ])
        
        provider_layout.addWidget(self.cicd_provider)
        provider_group.setLayout(provider_layout)
        layout.addWidget(provider_group)
        
        # Workflow Configuration
        workflow_group = QGroupBox("Workflow Configuration")
        workflow_layout = QGridLayout()
        
        # Build settings
        self.build_check = QCheckBox("Build")
        self.test_check = QCheckBox("Test")
        self.lint_check = QCheckBox("Lint")
        self.audit_check = QCheckBox("Security Audit")
        
        workflow_layout.addWidget(self.build_check, 0, 0)
        workflow_layout.addWidget(self.test_check, 0, 1)
        workflow_layout.addWidget(self.lint_check, 1, 0)
        workflow_layout.addWidget(self.audit_check, 1, 1)
        
        workflow_group.setLayout(workflow_layout)
        layout.addWidget(workflow_group)
        
        return tab

    def setup_deployment_tab(self):
        """Create deployment configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Platform Selection
        platform_group = QGroupBox("Deployment Platform")
        platform_layout = QVBoxLayout()
        
        self.deploy_platform = QComboBox()
        self.deploy_platform.addItems([
            "Vercel",
            "Netlify",
            "AWS Amplify",
            "GitHub Pages",
            "Custom Server"
        ])
        
        platform_layout.addWidget(self.deploy_platform)
        platform_group.setLayout(platform_layout)
        layout.addWidget(platform_group)
        
        # Environment Configuration
        env_group = QGroupBox("Environment Variables")
        env_layout = QVBoxLayout()
        
        self.env_editor = QTextEdit()
        self.env_editor.setPlaceholderText("KEY=value\nAPI_URL=https://api.example.com")
        
        env_layout.addWidget(self.env_editor)
        env_group.setLayout(env_layout)
        layout.addWidget(env_group)
        
        # Domain Configuration
        domain_group = QGroupBox("Domain Configuration")
        domain_layout = QGridLayout()
        
        domain_label = QLabel("Custom Domain:")
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("www.example.com")
        
        ssl_check = QCheckBox("Enable SSL")
        ssl_check.setChecked(True)
        
        domain_layout.addWidget(domain_label, 0, 0)
        domain_layout.addWidget(self.domain_input, 0, 1)
        domain_layout.addWidget(ssl_check, 1, 0)
        
        domain_group.setLayout(domain_layout)
        layout.addWidget(domain_group)
        
        return tab
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
        QApplication.desktop().cursor().pos()
        )
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def setup_terminal(self):
        """Setup terminal output area"""
        self.terminal = TerminalOutput(self)
        self.terminal.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.current_theme.terminal_bg};
                color: {self.current_theme.terminal_text};
                border: 1px solid {self.current_theme.border};
                border-radius: 4px;
                padding: 8px;
                font-family: "Consolas", monospace;
            }}
        """)
        window_height = self.height()
        terminal_height = int(window_height * 0.50)
        self.terminal.setMinimumHeight(terminal_height)
        self.terminal.setMaximumHeight(terminal_height)

        
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Project', self)
        new_action.setIcon(AppIcons.get_add_icon())
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.create_project)
        file_menu.addAction(new_action)
        
        save_action = QAction('&Save Terminal Output', self)
        save_action.setIcon(AppIcons.get_save_icon())
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.terminal.save_output)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('&Exit', self)
        exit_action.setIcon(AppIcons.get_exit_icon())
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        clear_action = QAction('&Clear Terminal', self)
        clear_action.setShortcut('Ctrl+L')
        clear_action.setIcon(AppIcons.get_clean_icon())
        clear_action.triggered.connect(self.terminal.clear_output)
        edit_menu.addAction(clear_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        theme_menu = view_menu.addMenu('&Theme')
        theme_menu.setIcon(AppIcons.get_theme_icon())
        
        light_action = QAction('&Light', self)
        light_action.triggered.connect(lambda: self.change_theme(AppTheme.light()))
        light_action.setIcon(AppIcons.get_light_icon())

        theme_menu.addAction(light_action)
        
        dark_action = QAction('&Dark', self)
        dark_action.triggered.connect(lambda: self.change_theme(AppTheme.dark()))
        dark_action.setIcon(AppIcons.get_dark_icon())

        theme_menu.addAction(dark_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about_dialog)
        about_action.setIcon(AppIcons.get_about_icon())
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup application status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add npm version
        try:
            version = subprocess.check_output(
                [self.npm_path, "-v"],
                text=True
            ).strip()
            self.status_bar.addPermanentWidget(
                QLabel(f"npm version: {version}")
            )
        except:
            pass
            
    def setup_project_form(self, layout: QVBoxLayout):
        """Setup project configuration form with fixed layout"""
        # Create a scroll area for the entire form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Create a container widget for the scroll area
        container = QWidget()
        form_layout = QVBoxLayout(container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # Project Configuration
        config_group = QGroupBox("Project Configuration")
        config_layout = QGridLayout()
        config_layout.setSpacing(10)
        
        # Project Name
        name_label = QLabel("Project Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("my-awesome-project")
        self.name_input.setMinimumWidth(300)
        self.name_input.textChanged.connect(self.update_project_config)
        
        # Template
        template_label = QLabel("Template:")
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "react",
            "next",
            "remix",
            "gatsby"
        ])
        self.template_combo.setMinimumWidth(300)
        self.template_combo.currentTextChanged.connect(self.update_project_config)
        
        # Package Manager
        pm_label = QLabel("Package Manager:")
        self.pm_combo = QComboBox()
        self.pm_combo.addItems([
            "npm",
            "yarn",
            "pnpm"
        ])
        self.pm_combo.setMinimumWidth(300)
        self.pm_combo.currentTextChanged.connect(self.update_project_config)
        
        # Add widgets to grid layout with proper spacing
        config_layout.addWidget(name_label, 0, 0, Qt.AlignRight)
        config_layout.addWidget(self.name_input, 0, 1)
        config_layout.addWidget(template_label, 1, 0, Qt.AlignRight)
        config_layout.addWidget(self.template_combo, 1, 1)
        config_layout.addWidget(pm_label, 2, 0, Qt.AlignRight)
        config_layout.addWidget(self.pm_combo, 2, 1)
        
        config_layout.setColumnStretch(1, 1)
        config_group.setLayout(config_layout)
        form_layout.addWidget(config_group)

        # Features
        features_group = QGroupBox("Features")
        features_layout = QGridLayout()
        features_layout.setSpacing(10)
        
        self.typescript_check = QCheckBox("TypeScript")
        self.eslint_check = QCheckBox("ESLint")
        self.prettier_check = QCheckBox("Prettier")
        self.testing_check = QCheckBox("Testing")
        self.router_check = QCheckBox("React Router")
        self.git_check = QCheckBox("Git Integration")
        self.ci_cd_check = QCheckBox("CI/CD Setup")
        
        for check in [
            self.typescript_check, self.eslint_check,
            self.prettier_check, self.testing_check,
            self.router_check, self.git_check,
            self.ci_cd_check
        ]:
            check.setChecked(False)
            check.stateChanged.connect(self.update_project_config)
        
        features_layout.addWidget(self.typescript_check, 0, 0)
        features_layout.addWidget(self.eslint_check, 0, 1)
        features_layout.addWidget(self.prettier_check, 1, 0)
        features_layout.addWidget(self.testing_check, 1, 1)
        features_layout.addWidget(self.router_check, 2, 0)
        features_layout.addWidget(self.git_check, 2, 1)
        features_layout.addWidget(self.ci_cd_check, 3, 0)
        
        features_group.setLayout(features_layout)
        form_layout.addWidget(features_group)

        # State Management
        state_group = QGroupBox("State Management")
        state_layout = QVBoxLayout()
        state_layout.setSpacing(10)
        
        self.state_combo = QComboBox()
        self.state_combo.addItems([
            "None",
            "Redux Toolkit",
            "Zustand",
            "Jotai",
            "Recoil"
        ])
        self.state_combo.setMinimumWidth(300)
        self.state_combo.currentTextChanged.connect(self.update_project_config)
        
        state_layout.addWidget(self.state_combo)
        state_group.setLayout(state_layout)
        form_layout.addWidget(state_group)

        # Styling
        styling_group = QGroupBox("Styling Solution")
        styling_layout = QVBoxLayout()
        styling_layout.setSpacing(10)
        
        self.styling_combo = QComboBox()
        self.styling_combo.addItems([
            "None",
            "Tailwind CSS",
            "Styled Components",
            "CSS Modules"
        ])
        self.styling_combo.setMinimumWidth(300)
        self.styling_combo.currentTextChanged.connect(self.update_project_config)
        
        styling_layout.addWidget(self.styling_combo)
        styling_group.setLayout(styling_layout)
        form_layout.addWidget(styling_group)

        # Deployment Platform
        deploy_group = QGroupBox("Deployment Platform")
        deploy_layout = QVBoxLayout()
        deploy_layout.setSpacing(10)
        
        self.deploy_combo = QComboBox()
        self.deploy_combo.addItems([
            "None",
            "Vercel",
            "Netlify",
            "GitHub Pages"
        ])
        self.deploy_combo.setMinimumWidth(300)
        self.deploy_combo.currentTextChanged.connect(self.update_project_config)
        
        deploy_layout.addWidget(self.deploy_combo)
        deploy_group.setLayout(deploy_layout)
        form_layout.addWidget(deploy_group)

        # Action Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        create_btn = ModernButton(
            "Create Project",
            self,
            primary=True,
            icon=AppIcons.get_terminal_icon()
        )
        create_btn.clicked.connect(self.create_project)
        create_btn.setMinimumWidth(150)
        
        clear_btn = ModernButton(
            "Clear Form",
            self,
            icon=AppIcons.get_refresh_icon()
        )
        clear_btn.clicked.connect(self.clear_form)
        clear_btn.setMinimumWidth(150)

        dir_label = QLabel("Project Directory:")
        dir_layout = QHBoxLayout()

        self.dir_input = QLineEdit()
        self.dir_input.setReadOnly(True)
        self.dir_input.setPlaceholderText("Select project directory...")
        self.dir_input.setMinimumWidth(300)

        select_dir_btn = ModernButton(
            "Browse",
            self,
            icon=AppIcons.get_folder_icon()
        )
        select_dir_btn.clicked.connect(self.select_directory)

        existing_group = QGroupBox("Open Existing Project")
        existing_layout = QHBoxLayout()
        
        self.existing_path = QLineEdit()
        self.existing_path.setPlaceholderText("Select an existing React project...")
        self.existing_path.setReadOnly(True)

        select_existing_btn = ModernButton(
            "Browse",
            self,
            icon=AppIcons.get_folder_icon()
        )
        select_existing_btn.clicked.connect(self.select_existing_project)
        
        existing_layout.addWidget(self.existing_path)
        existing_layout.addWidget(select_existing_btn)
        
        existing_group.setLayout(existing_layout)
        layout.addWidget(existing_group)

        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(select_dir_btn)

        config_layout.addWidget(dir_label, 3, 0, Qt.AlignRight)
        config_layout.addLayout(dir_layout, 3, 1)
            
        buttons_layout.addStretch()
        buttons_layout.addWidget(create_btn)
        buttons_layout.addWidget(clear_btn)
        form_layout.addLayout(buttons_layout)

        # Set the container as the scroll area's widget
        scroll.setWidget(container)
        
        # Add the scroll area to the main layout
        layout.addWidget(scroll)
    
    def select_existing_project(self):
        """Varolan bir React projesini seç"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select React Project",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            # package.json kontrolü
            package_json = os.path.join(directory, "package.json")
            if not os.path.exists(package_json):
                QMessageBox.warning(
                    self,
                    "Invalid Project",
                    "Selected directory is not a React project!"
                )
                return
                
            try:
                with open(package_json) as f:
                    package_data = json.load(f)
                    
                # React bağımlılığı kontrolü
                if not any(
                    dep.startswith("react")
                    for dep in package_data.get("dependencies", {})
                ):
                    raise ValueError("React dependency not found")
                    
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Invalid Project",
                    f"Error validating React project: {str(e)}"
                )
                return
                
            self.project_directory = directory
            self.existing_path.setText(directory)
            self.terminal.append_output(
                f"Opened existing project: {directory}",
                "INFO"
            )
            self.run_btn.setEnabled(True)
    

    def select_directory(self):
        directory = self.select_project_directory()
        if directory:
            self.dir_input.setText(directory)
        
    def update_project_config(self):
        """Update project configuration based on form values"""
        self.project_config = ProjectConfig(
            name=self.name_input.text(),
            template=self.template_combo.currentText(),
            dependencies=[],
            dev_dependencies=[],
            git_integration=self.git_check.isChecked(),
            testing=self.testing_check.isChecked(),
            test_framework="vitest" if self.testing_check.isChecked() else None,
            styling_solution=self.styling_combo.currentText(),
            typescript=self.typescript_check.isChecked(),
            eslint=self.eslint_check.isChecked(),
            prettier=self.prettier_check.isChecked(),
            package_manager=self.pm_combo.currentText(),
            router=self.router_check.isChecked(),
            state_management=self.state_combo.currentText() if self.state_combo.currentText() != "None" else None,
            ci_cd=self.ci_cd_check.isChecked(),
            deployment_platform=self.deploy_combo.currentText() if self.deploy_combo.currentText() != "None" else None
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
        
        if not hasattr(self, 'project_directory') or not self.project_directory:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select a project directory!"
            )
            return
            
        # Create worker thread
        self.project_worker = ProjectWorker(
            self.project_config,
            self.npm_path,
            self.npx_path,
            self.project_directory
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
        # Ana uygulama stilleri
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.current_theme.background};
            }}
            
            QScrollArea {{
                background-color: {self.current_theme.background};
                border: none;
            }}
            
            QScrollArea > QWidget > QWidget {{
                background-color: {self.current_theme.background};
            }}
            
            QScrollBar {{
                background-color: {self.current_theme.surface};
                border-radius: 4px;
            }}
            
            QScrollBar:vertical {{
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar:horizontal {{
                height: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle {{
                background-color: {self.current_theme.secondary};
                border-radius: 4px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:hover {{
                background-color: {self.current_theme.primary};
            }}
            
            QScrollBar::add-line, QScrollBar::sub-line {{
                height: 0px;
                width: 0px;
            }}
            
            QLabel {{
                color: {self.current_theme.text_primary};
                padding: 5px;
            }}
            
            QGroupBox {{
                background-color: {self.current_theme.surface};
                border: 1px solid {self.current_theme.border};
                border-radius: 6px;
                margin-top: 12px;
                padding: 10px;
                color: {self.current_theme.text_primary};
            }}
            
            QLineEdit, QComboBox, QTextEdit {{
                background-color: {self.current_theme.surface};
                color: {self.current_theme.text_primary};
                border: 1px solid {self.current_theme.border};
                border-radius: 4px;
                padding: 8px;
                selection-background-color: {self.current_theme.primary};
                selection-color: white;
            }}
            
            QWidget[objectName="scrollAreaContent"] {{
                background-color: {self.current_theme.background};
                color: {self.current_theme.text_primary};
            }}

            QCheckBox {{
            color: {self.current_theme.text_primary};
            spacing: 5px;
            }}

            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {self.current_theme.text_primary};
                border-radius: 3px;
            }}

            QCheckBox::indicator:checked {{
                background-color: {self.current_theme.primary};
                border-color: {self.current_theme.primary};
            }}

            QCheckBox::indicator:unchecked {{
                background-color: transparent;
            }}

            QComboBox {{
            color: {self.current_theme.text_primary};
            background-color: {self.current_theme.surface};
            border: 1px solid {self.current_theme.border};
            border-radius: 4px;
            padding: 5px 10px;
            min-width: 6em;
            }}
        
            QComboBox:hover {{
                border-color: {self.current_theme.primary};
            }}
            
            QComboBox:focus {{
                border-color: {self.current_theme.primary};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
                padding-right: 5px;
            }}
            
            QComboBox::down-arrow {{
                image: url(:/icons/down-arrow.svg);
                width: 12px;
                height: 12px;
            }}
            
            QComboBox QAbstractItemView {{
                color: {self.current_theme.text_primary};
                background-color: {self.current_theme.surface};
                border: 1px solid {self.current_theme.border};
                selection-background-color: {self.current_theme.primary};
                selection-color: white;
                outline: 0px;
            }}
            
            QComboBox QAbstractItemView::item {{
                min-height: 25px;
                padding: 5px;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background-color: {self.current_theme.border};
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
    
    def select_project_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Project Directory",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if directory:
            # Yazma izni kontrolü
            if not os.access(directory, os.W_OK):
                QMessageBox.warning(
                    self,
                    "Permission Error",
                    "No write permission in selected directory!"
                )
                return None
        
            # Boş dizin kontrolü (opsiyonel)
            if os.listdir(directory):
                response = QMessageBox.question(
                    self,
                    "Directory Not Empty",
                    "Selected directory is not empty. Continue?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if response == QMessageBox.No:
                    return None
            
            self.project_directory = directory
            self.terminal.append_output(f"Project directory selected: {directory}", "INFO")
            return directory
        return None
            
    def setup_fonts(self):
        """Setup application fonts"""
        app_font = QFont("Segoe UI", 10)  # Modern system font
        self.setFont(app_font)
        
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
        self.pm_combo.setCurrentIndex(0)
        self.typescript_check.setChecked(False)
        self.eslint_check.setChecked(False)
        self.prettier_check.setChecked(False)
        self.testing_check.setChecked(False)
        self.router_check.setChecked(False)
        self.git_check.setChecked(False)
        self.ci_cd_check.setChecked(False)
        self.state_combo.setCurrentIndex(0)
        self.styling_combo.setCurrentIndex(0)
        self.deploy_combo.setCurrentIndex(0)
        self.dir_input.clear()
        if hasattr(self, 'project_directory'):
            delattr(self, 'project_directory')
        
    def show_about_dialog(self):
        """Show themed about dialog"""
        icon_size = 128
        app_icon = AppIcon.create_app_icon().pixmap(icon_size, icon_size)
        
        about = ThemedMessageBox(self.current_theme, self)
        about.setWindowTitle("About")
        about.setIconPixmap(app_icon)
        
        about_text = f"""
        <div style='margin-left: 20px; margin-right: 20px;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <h2 style='font-size: 24px; margin: 0; color: {self.current_theme.text_primary};'>
                    {APP_NAME}
                </h2>
                <span style='font-size: 16px; margin-left: 10px; color: {self.current_theme.text_secondary};'>
                    v{APP_VERSION}
                </span>
            </div>
            
            <p style='font-size: 14px; line-height: 1.6; color: {self.current_theme.text_primary}; margin: 15px 0;'>
                A professional-grade tool for automating React project creation 
                with modern best practices and industry standards.
            </p>
            
            <div style='margin-top: 20px; border-top: 1px solid {self.current_theme.border}; padding-top: 15px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                    <span style='color: {self.current_theme.text_secondary};'>Author</span>
                    <span style='color: {self.current_theme.text_primary};'>Melih Can Demir</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: {self.current_theme.text_secondary};'>License</span>
                    <span style='color: {self.current_theme.text_primary};'>MIT</span>
                </div>
            </div>
        </div>
        """
        
        about.setText(about_text)
        about.setTextFormat(Qt.RichText)
        about.setStandardButtons(QMessageBox.Ok)
        
        ok_button = about.button(QMessageBox.Ok)
        if ok_button:
            ok_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.current_theme.primary};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 24px;
                    min-width: 100px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.current_theme.accent};
                }}
            """)
        
        about.exec_()

    def setup_run_controls(self):
        """Setup project run controls"""
        # Run controls group
        run_group = QGroupBox("Project Controls")
        run_layout = QHBoxLayout()
        
        # Run button
        self.run_btn = ModernButton(
            "Run Project",
            self,
            primary=True,
            icon=AppIcons.get_play_icon()
        )
        self.run_btn.clicked.connect(self.toggle_project_run)
        self.run_btn.setEnabled(False)
        
        # Open in browser button
        self.browser_btn = ModernButton(
            "Open in Browser",
            self,
            icon=AppIcons.get_browser_icon()
        )
        self.browser_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("http://localhost:5173")))
        self.browser_btn.setEnabled(False)
        
        run_layout.addWidget(self.run_btn)
        run_layout.addWidget(self.browser_btn)
        run_group.setLayout(run_layout)
        
        return run_group

    def toggle_project_run(self):
        """Toggle project run state"""
        if not hasattr(self, 'project_runner') or not self.project_runner.running:
            # Proje dizini kontrolü
            if not hasattr(self, 'project_directory') or not self.project_directory:
                QMessageBox.warning(self, "Error", "No project directory selected!")
                return
                
            project_path = os.path.join(self.project_directory, self.project_config.name)
            if not os.path.exists(project_path):
                project_path = self.project_directory  # Mevcut proje dizinini kullan
                
            # Runner'ı başlat
            self.project_runner = ProjectRunner(project_path, self.npm_path)
            self.project_runner.output_ready.connect(self.terminal.append_output)
            self.project_runner.error_occurred.connect(self.handle_run_error)
            self.project_runner.running_changed.connect(self.update_run_button_state)  # Yeni bağlantı
            self.project_runner.start()
            
        else:
            # Projeyi durdur
            self.project_runner.stop()
    
    def update_run_button_state(self, is_running: bool):
        """Update run button state based on project running status"""
        if is_running:
            self.run_btn.setText("Stop Project")
            self.run_btn.setIcon(AppIcons.get_stop_icon())
            self.browser_btn.setEnabled(True)
        else:
            self.run_btn.setText("Run Project")
            self.run_btn.setIcon(AppIcons.get_play_icon())
            self.browser_btn.setEnabled(False)

    def handle_run_error(self, error_message: str):
        """Handle project run errors"""
        QMessageBox.critical(self, "Error", f"Failed to run project: {error_message}")
        self.run_btn.setText("Run Project")
        self.run_btn.setIcon(AppIcons.get_play_icon())
        self.browser_btn.setEnabled(False)

    def handle_completion(self, success: bool, message: str):
        """Handle project creation completion"""
        self.progress_dialog.close()
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.save_settings()
            # Proje oluşturulduğunda Run butonunu aktif et
            self.run_btn.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error", f"Failed to create project: {message}")


class ProjectRunner(QThread):
    """Thread for running React projects"""
    output_ready = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)
    running_changed = pyqtSignal(bool)
    
    def __init__(self, project_path: str, npm_path: str):
        super().__init__()
        self.project_path = project_path
        self.npm_path = npm_path
        # node_modules/.bin dizinindeki vite yolunu belirle
        self.vite_path = os.path.join(project_path, "node_modules", ".bin", "vite")
        if os.name == "nt":  # Windows için .cmd uzantısını ekle
            self.vite_path += ".cmd"
        self.process = None
        self.running = False
    
    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, value):
        self._running = value
        self.running_changed.emit(value)
    
    def run(self):
        try:
            self.running = True
            os.chdir(self.project_path)
            
            # node_modules kontrolü
            if not os.path.exists(os.path.join(self.project_path, "node_modules")):
                self.output_ready.emit("Installing dependencies...", "INFO")
                if not self.install_dependencies():
                    raise Exception("Failed to install dependencies")
            
            # Vite kontrolü ve yükleme
            if not os.path.exists(self.vite_path):
                self.output_ready.emit("Installing Vite...", "INFO")
                if not self.install_vite():
                    raise Exception("Failed to install Vite")
            
            # Projeyi başlat
            self.output_ready.emit("Starting development server...", "INFO")
            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.handle_output)
            
            # Windows'ta npm run dev, diğer sistemlerde doğrudan vite
            if os.name == "nt":
                self.process.start(self.npm_path, ["run", "dev"])
            else:
                self.process.start(self.vite_path)
            
            self.process.waitForFinished(-1)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.running = False
    
    def install_dependencies(self) -> bool:
        """Install project dependencies"""
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.readyReadStandardOutput.connect(
            lambda: self.output_ready.emit(
                process.readAll().data().decode(), "INFO"
            )
        )
        
        process.start(self.npm_path, ["install"])
        process.waitForFinished(-1)
        return process.exitCode() == 0
    
    def install_vite(self) -> bool:
        """Install Vite dependency"""
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.readyReadStandardOutput.connect(
            lambda: self.output_ready.emit(
                process.readAll().data().decode(), "INFO"
            )
        )
        
        process.start(self.npm_path, ["install", "--save-dev", "vite"])
        process.waitForFinished(-1)
        return process.exitCode() == 0
    
    def handle_output(self):
        """Handle process output"""
        data = self.process.readAll().data().decode()
        cleaned_data = self.clean_ansi_codes(data)
        self.output_ready.emit(cleaned_data, "INFO")
    
    def stop(self):
        """Stop running project"""
        if self.process and self.running:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.processId())], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.process.kill()
            
            self.running = False
            self.output_ready.emit("Development server stopped.", "INFO")
    
    @staticmethod
    def clean_ansi_codes(text: str) -> str:
        """Clean ANSI escape codes from text"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def check_package_json(self):
        """Check and update package.json if needed"""
        try:
            with open("package.json", "r+") as f:
                data = json.load(f)
                updated = False
                
                if "scripts" not in data:
                    data["scripts"] = {}
                    updated = True
                
                if "dev" not in data["scripts"]:
                    data["scripts"]["dev"] = "vite"
                    updated = True
                
                if updated:
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    
        except Exception as e:
            self.error_occurred.emit(f"Failed to update package.json: {str(e)}")
    

class ThemedMessageBox(QMessageBox):
    def __init__(self, theme: AppTheme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme = theme
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.theme.background};
                color: {self.theme.text_primary};
                border: 1px solid {self.theme.border};
                border-radius: 12px;
                min-width: 480px;
            }}
            
            QMessageBox QLabel {{
                color: {self.theme.text_primary};
                font-size: 14px;
                border-radius: 8px;
            }}
            
            QMessageBox QPushButton {{
                background-color: {self.theme.primary};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 24px;
                min-width: 100px;
                font-weight: bold;
            }}
            
            QMessageBox QPushButton:hover {{
                background-color: {self.theme.accent};
            }}
        """)

        # İçerik hizalama
        for label in self.findChildren(QLabel):
            label.setAlignment(Qt.AlignLeft)
            label.setContentsMargins(5, 5, 5, 5)



    
def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application info
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORGANIZATION_NAME)
    
    # Create and show main window
    window = ModernReactAutomator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()