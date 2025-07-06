#!/usr/bin/env python3
"""
Nomouse - A transparent overlay grid for quick mouse positioning

Features:
- Press Ctrl+; to show overlay
- Type two-letter codes to move mouse to grid cells
- Press Escape to close overlay
- Always-on-top transparent window
- Blocks input to underlying applications
"""

import sys
import string
import math
from typing import Dict, Tuple, Optional
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QKeyEvent
import keyboard
import pyautogui
from pynput.keyboard import Key, Listener


class GridOverlay(QWidget):
    """Transparent overlay window that displays a grid of two-letter codes"""
    
    def __init__(self, grid_size: int = 32):
        super().__init__()
        self.grid_size = 26  # Always use 32x32 grid
        self.codes = self._generate_codes()
        self.cell_size = None
        self.cell_centers = {}
        self.current_input = ""
        self.input_timer = QTimer()
        self.input_timer.setSingleShot(True)
        self.input_timer.timeout.connect(self._clear_input)
        
        # Window setup
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        # Get screen size and position window
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Calculate cell size and centers
        self._calculate_layout()
        
        # Setup keyboard listener for input
        self.listener = None
        self._setup_keyboard_listener()
        
        # Focus the window to receive keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
    
    def _generate_codes(self) -> Dict[str, Tuple[int, int]]:
        """Generate two-letter codes for the grid"""
        codes = {}
        letters = string.ascii_uppercase
        code_index = 0
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Generate two-letter codes: AA, AB, AC, ..., AZ, BA, BB, ...
                first_letter = letters[code_index // 26]
                second_letter = letters[code_index % 26]
                code = f"{first_letter}{second_letter}"
                codes[code] = (row, col)
                code_index += 1
        
        return codes
    
    def _calculate_layout(self):
        """Calculate cell sizes and center positions"""
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Calculate cell dimensions
        self.cell_width = screen_width // self.grid_size
        self.cell_height = screen_height // self.grid_size
        
        # Calculate center positions for each cell
        self.cell_centers = {}
        for code, (row, col) in self.codes.items():
            center_x = col * self.cell_width + self.cell_width // 2
            center_y = row * self.cell_height + self.cell_height // 2
            self.cell_centers[code] = (center_x, center_y)
    
    def _setup_keyboard_listener(self):
        """Setup keyboard listener for input when overlay is active"""
        self.listener = Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            if hasattr(key, 'char') and key.char:
                # Add character to current input
                self.current_input += key.char.upper()
                self.input_timer.start(2000)  # Clear input after 2 seconds
                self.update()  # Redraw to show input
                
                # Check if we have a complete code
                if len(self.current_input) == 2:
                    self._process_code(self.current_input)
                    
        except AttributeError:
            # Special keys
            if key == Key.esc:
                self.close()
            elif key == Key.backspace:
                self.current_input = self.current_input[:-1] if self.current_input else ""
                self.update()
    
    def _on_key_release(self, key):
        """Handle key release events"""
        pass
    
    def _process_code(self, code: str):
        """Process a two-letter code and move mouse if valid"""
        if code in self.codes:
            center_x, center_y = self.cell_centers[code]
            # Click even lower to match the text visually
            click_x = center_x
            click_y = center_y + 18  # Increased offset for lower click
            pyautogui.moveTo(click_x, click_y)
            pyautogui.click(click_x, click_y)
            self.close()
        else:
            self.current_input = ""
            self.update()
    
    def _clear_input(self):
        """Clear current input after timeout"""
        self.current_input = ""
        self.update()
    
    def paintEvent(self, event):
        """Paint the grid overlay"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up font for codes
        font_size = min(self.cell_width, self.cell_height) // 4
        font = QFont("Arial", font_size, QFont.Bold)
        painter.setFont(font)
        
        # Set up color for codes (red)
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        
        # Draw codes at cell centers
        for code, (row, col) in self.codes.items():
            center_x, center_y = self.cell_centers[code]
            
            # Draw the two-letter code
            text_rect = painter.fontMetrics().boundingRect(code)
            text_x = center_x - text_rect.width() // 2
            text_y = center_y + text_rect.height() // 2
            painter.drawText(text_x, text_y, code)
        
        # Draw current input if any
        if self.current_input:
            # Draw input in a different color (yellow) and larger
            input_font = QFont("Arial", font_size * 2, QFont.Bold)
            painter.setFont(input_font)
            painter.setPen(QPen(QColor(255, 255, 0), 3))
            
            # Position input at center of screen
            screen_center_x = self.width() // 2
            screen_center_y = self.height() // 2
            
            input_rect = painter.fontMetrics().boundingRect(self.current_input)
            input_x = screen_center_x - input_rect.width() // 2
            input_y = screen_center_y + input_rect.height() // 2
            painter.drawText(input_x, input_y, self.current_input)
    
    def closeEvent(self, event):
        """Clean up when closing"""
        if self.listener:
            self.listener.stop()
        event.accept()


class NomouseApp:
    """Main application class that manages the hotkey and overlay"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.overlay = None
        self.grid_size = 10  # Default 10x10 grid
        
        # Setup global hotkey
        keyboard.add_hotkey('ctrl+;', self._show_overlay)
        
        print("Nomouse started! Press Ctrl+; to show the overlay.")
        print("Press Ctrl+C to exit.")
    
    def _show_overlay(self):
        """Show the grid overlay"""
        if self.overlay is None or not self.overlay.isVisible():
            self.overlay = GridOverlay(self.grid_size)
            self.overlay.show()
            self.overlay.raise_()
            self.overlay.activateWindow()
    
    def run(self):
        """Run the application"""
        try:
            sys.exit(self.app.exec_())
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


def main():
    """Main entry point"""
    app = NomouseApp()
    app.run()


if __name__ == "__main__":
    main()