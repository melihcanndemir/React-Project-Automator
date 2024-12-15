import sys
import os
import subprocess
import shutil
import json
import git
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, 
    QLabel, QWidget, QMessageBox, QComboBox, QFileDialog, QHBoxLayout, 
    QFrame, QProgressDialog, QTabWidget, QScrollArea, QGridLayout,
    QGroupBox, QSpinBox, QCheckBox, QTextEdit, QSplitter
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, QLinearGradient, QBrush, QIcon,
    QPainter, QPaintEvent, QFontDatabase
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QRect
)
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet

@dataclass
class ProjectConfig:
    name: str
    template: str
    dependencies: List[str]
    dev_dependencies: List[str]
    git_integration: bool
    test_framework: str
    styling_solution: str
    
class ModernButton(QPushButton):
    def __init__(self, text: str, parent=None, primary: bool = False):
        super().__init__(text, parent)
        self.primary = primary
        self.setup_styles()
        
    def setup_styles(self):
        color = "#2563eb" if self.primary else "#4b5563"
        hover_color = "#1d4ed8" if self.primary else "#374151"
        self.setStyleSheet(f"""
            ModernButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }}
            ModernButton:hover {{
                background-color: {hover_color};
            }}
            ModernButton:pressed {{
                transform: translateY(1px);
            }}
        """)

class ProjectAnalytics(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Dependency Chart
        dep_chart = QChart()
        dep_series = QPieSeries()
        dep_series.append("Runtime", 15)
        dep_series.append("Development", 8)
        dep_series.append("Peer", 3)
        dep_chart.addSeries(dep_series)
        dep_chart.setTitle("Dependencies Distribution")
        
        chart_view = QChartView(dep_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

class DependencyManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
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
        
        # Add package button
        add_btn = ModernButton("Add Package", self, primary=True)
        layout.addWidget(add_btn)

class GitIntegration(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Repository URL
        self.repo_url = QLineEdit(self)
        self.repo_url.setPlaceholderText("Repository URL")
        layout.addWidget(self.repo_url)
        
        # Branch selection
        self.branch_combo = QComboBox(self)
        self.branch_combo.addItems(["main", "develop", "feature"])
        layout.addWidget(self.branch_combo)
        
        # Git operations
        git_ops_group = QGroupBox("Git Operations", self)
        git_ops_layout = QVBoxLayout()
        
        init_btn = ModernButton("Initialize Repository")
        commit_btn = ModernButton("Commit Changes")
        push_btn = ModernButton("Push Changes")
        
        git_ops_layout.addWidget(init_btn)
        git_ops_layout.addWidget(commit_btn)
        git_ops_layout.addWidget(push_btn)
        
        git_ops_group.setLayout(git_ops_layout)
        layout.addWidget(git_ops_group)

class ModernReactAutomator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern React Project Automator")
        self.init_ui()
        self.setup_npm_paths()
        self.project_config = None
        
    def init_ui(self):
        self.setMinimumSize(1200, 800)
        self.setup_fonts()
        self.setup_styles()
        
        # Central widget and main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Header
        header = QLabel("Modern React Project Automator")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
            margin: 24px 0;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
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
        self.setup_project_form(setup_layout)
        tabs.addTab(setup_tab, "Project Setup")
        
        # Dependencies Tab
        deps_tab = DependencyManager()
        tabs.addTab(deps_tab, "Dependencies")
        
        # Git Integration Tab
        git_tab = GitIntegration()
        tabs.addTab(git_tab, "Git Integration")
        
        # Analytics Tab
        analytics_tab = ProjectAnalytics()
        tabs.addTab(analytics_tab, "Analytics")
        
        main_layout.addWidget(tabs)
        
    def setup_fonts(self):
        QFontDatabase.addApplicationFont(":/fonts/Inter-Regular.ttf")
        QFontDatabase.addApplicationFont(":/fonts/Inter-Bold.ttf")
        self.setFont(QFont("Inter", 10))
        
    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }
            QLineEdit, QComboBox {
                padding: 12px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #2563eb;
            }
        """)
        
    def setup_project_form(self, layout: QVBoxLayout):
        # Project Name
        name_group = QGroupBox("Project Configuration")
        name_layout = QGridLayout()
        
        name_label = QLabel("Project Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("my-awesome-project")
        
        template_label = QLabel("Template:")
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "react", "react-ts", "next", "next-ts",
            "remix", "remix-ts", "gatsby"
        ])
        
        name_layout.addWidget(name_label, 0, 0)
        name_layout.addWidget(self.name_input, 0, 1)
        name_layout.addWidget(template_label, 1, 0)
        name_layout.addWidget(self.template_combo, 1, 1)
        
        name_group.setLayout(name_layout)
        layout.addWidget(name_group)
        
        # Features
        features_group = QGroupBox("Features")
        features_layout = QGridLayout()
        
        self.typescript = QCheckBox("TypeScript")
        self.eslint = QCheckBox("ESLint")
        self.prettier = QCheckBox("Prettier")
        self.testing = QCheckBox("Testing Setup")
        
        features_layout.addWidget(self.typescript, 0, 0)
        features_layout.addWidget(self.eslint, 0, 1)
        features_layout.addWidget(self.prettier, 1, 0)
        features_layout.addWidget(self.testing, 1, 1)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Styling Solution
        styling_group = QGroupBox("Styling Solution")
        styling_layout = QVBoxLayout()
        
        self.styling_combo = QComboBox()
        self.styling_combo.addItems([
            "Tailwind CSS",
            "Styled Components",
            "Emotion",
            "CSS Modules"
        ])
        
        styling_layout.addWidget(self.styling_combo)
        styling_group.setLayout(styling_layout)
        layout.addWidget(styling_group)
        
        # Action Buttons
        buttons_layout = QHBoxLayout()
        
        create_btn = ModernButton("Create Project", primary=True)
        create_btn.clicked.connect(self.create_project)
        
        clear_btn = ModernButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addWidget(create_btn)
        
        layout.addLayout(buttons_layout)
        
    def create_project(self):
        # Project configuration oluştur
        self.project_config = ProjectConfig(
            name=self.name_input.text(),
            template=self.template_combo.currentText(),
            dependencies=[],
            dev_dependencies=[],
            git_integration=True,
            test_framework="jest" if self.testing.isChecked() else None,
            styling_solution=self.styling_combo.currentText()
        )
        
        # Progress dialog göster
        progress = QProgressDialog("Creating project...", None, 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        # Proje oluşturma işlemini başlat
        self.create_project_steps(progress)
        
    def create_project_steps(self, progress):
        try:
            # 1. Proje dizini oluştur
            progress.setValue(10)
            project_path = Path.cwd() / self.project_config.name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # 2. Vite projesi oluştur
            progress.setValue(30)
            subprocess.run([
                self.npx_path, "create-vite@latest",
                self.project_config.name,
                "--template", self.project_config.template
            ], check=True)
            
            # 3. Dependencies yükle
            progress.setValue(50)
            os.chdir(project_path)
            subprocess.run([self.npm_path, "install"], check=True)
            
            # 4. Additional dependencies
            progress.setValue(70)
            self.install_additional_dependencies()
            
            # 5. Git entegrasyonu
            progress.setValue(90)
            if self.project_config.git_integration:
                self.setup_git()
            
            progress.setValue(100)
            QMessageBox.information(self, "Success", "Project created successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")
            progress.close()
            
    def install_additional_dependencies(self):
        deps = []
        dev_deps = []
        
        # Styling solution
        if self.project_config.styling_solution == "Tailwind CSS":
            dev_deps.extend(["tailwindcss", "postcss", "autoprefixer"])
        elif self.project_config.styling_solution == "Styled Components":
            deps.append("styled-components")
            
        # TypeScript
        if self.typescript.isChecked():
            dev_deps.extend(["typescript", "@types/react", "@types/react-dom"])
            
        # Linting
        if self.eslint.isChecked():
            dev_deps.extend([
                "eslint",
                "eslint-plugin-react",
                "eslint-plugin-react-hooks"
            ])
            
        # Testing
        if self.testing.isChecked():
            dev_deps.extend([
                "jest",
                "@testing-library/react",
                "@testing-library/jest-dom"
            ])
            
        # Install dependencies
        if deps:
            subprocess.run([self.npm_path, "install", *deps], check=True)
        if dev_deps:
            subprocess.run([self.npm_path, "install", "-D", *dev_deps], check=True)
            
    def setup_git(self):
        repo = git.Repo.init()
        
        # Create .gitignore
        gitignore = """
        node_modules
        dist
        .env
        .env.local
        .DS_Store
        coverage
        """
        
        with open(".gitignore", "w") as f:
            f.write(gitignore.strip())
            
        # Initial commit
        repo.index.add(["."])
        repo.index.commit("Initial commit")
    
    def clear_form(self):
        self.name_input.clear()
        self.template_combo.setCurrentIndex(0)
        self.typescript.setChecked(False)
        self.eslint.setChecked(False)
        self.prettier.setChecked(False)
        self.testing.setChecked(False)
        self.styling_combo.setCurrentIndex(0)

    def setup_npm_paths(self):
        """Dinamik olarak npm ve npx yollarını belirle"""
        self.npm_path = shutil.which('npm')
        self.npx_path = shutil.which('npx')
        
        if not all([self.npm_path, self.npx_path]):
            QMessageBox.critical(self, "Error", "Node.js and npm must be installed and in PATH")
            sys.exit(1)

class ProjectWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, config: ProjectConfig, npm_path: str, npx_path: str):
        super().__init__()
        self.config = config
        self.npm_path = npm_path
        self.npx_path = npx_path
        
    def run(self):
        try:
            self.progress.emit(0, "Initializing project...")
            
            # Create project directory
            project_path = Path.cwd() / self.config.name
            project_path.mkdir(parents=True, exist_ok=True)
            
            self.progress.emit(20, "Creating Vite project...")
            subprocess.run([
                self.npx_path, "create-vite@latest",
                self.config.name,
                "--template", self.config.template
            ], check=True)
            
            # Change to project directory
            os.chdir(project_path)
            
            self.progress.emit(40, "Installing dependencies...")
            subprocess.run([self.npm_path, "install"], check=True)
            
            self.progress.emit(60, "Setting up additional features...")
            self.setup_features()
            
            self.progress.emit(80, "Finalizing setup...")
            self.setup_project_config()
            
            self.progress.emit(100, "Project created successfully!")
            self.finished.emit(True, "Project created successfully!")
            
        except Exception as e:
            self.finished.emit(False, str(e))
            
    def setup_features(self):
        """Setup additional project features based on configuration"""
        # Create necessary config files
        if "typescript" in self.config.template:
            self.setup_typescript()
            
        if self.config.test_framework:
            self.setup_testing()
            
        self.setup_styling()
        self.setup_linting()
        
    def setup_typescript(self):
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
        jest_config = {
            "transform": {
                "^.+\\.(t|j)sx?$": "babel-jest"
            },
            "testEnvironment": "jsdom",
            "setupFilesAfterEnv": [
                "@testing-library/jest-dom/extend-expect"
            ]
        }
        
        with open("jest.config.js", "w") as f:
            f.write(f"module.exports = {json.dumps(jest_config, indent=2)}")
            
    def setup_styling(self):
        if self.config.styling_solution == "Tailwind CSS":
            self.setup_tailwind()
        elif self.config.styling_solution == "Styled Components":
            self.setup_styled_components()
            
    def setup_tailwind(self):
        subprocess.run([
            self.npx_path, "tailwindcss", "init", "-p"
        ], check=True)
        
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
        # Add styled-components theme
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
        eslint_config = {
            "env": {
                "browser": True,
                "es2021": True
            },
            "extends": [
                "eslint:recommended",
                "plugin:react/recommended",
                "plugin:react-hooks/recommended"
            ],
            "parserOptions": {
                "ecmaFeatures": {
                    "jsx": True
                },
                "ecmaVersion": 12,
                "sourceType": "module"
            },
            "plugins": ["react"],
            "rules": {
                "react/react-in-jsx-scope": "off"
            }
        }
        
        with open(".eslintrc.json", "w") as f:
            json.dump(eslint_config, f, indent=2)
            
    def setup_project_config(self):
        """Create a project configuration file"""
        config = {
            "name": self.config.name,
            "version": "0.1.0",
            "private": True,
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint src",
                "test": "jest"
            }
        }
        
        with open("package.json", "w") as f:
            json.dump(config, f, indent=2)

def main():
    app = QApplication(sys.argv)
    
    # Varsayılan stil ayarları
    app.setStyle("Fusion")
    
    # Dark mode palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    
    # Light mode palette
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    light_palette.setColor(QPalette.Link, QColor(0, 100, 200))
    light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Varsayılan olarak light mode kullan
    app.setPalette(light_palette)
    
    # Ana pencereyi oluştur ve göster
    window = ModernReactAutomator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()