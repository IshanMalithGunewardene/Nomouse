#!/bin/bash

# Nomouse Installation Script
echo "Installing Nomouse - Transparent Grid Overlay"

# Check if Python 3 is installede
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Installation completed successfully!"
    echo ""
    echo "To run the application:"
    echo "  xhost +SI:localuser:root"
    echo "  sudo python3 nomouse.py"
    echo ""
    echo "Usage:"
    echo "  - Press Ctrl+; to show the overlay"
    echo "  - Type a two-letter code to move mouse to that cell"
    echo "  - Press Escape to close the overlay"
    echo "  - Press Ctrl+C to exit the application"
else
    echo "Error: Failed to install dependencies. Please check your Python/pip installation."
    exit 1
fi

# As your normal user (not sudo)
xdotool mousemove 500 500 click 1

# Restart the service
sudo systemctl restart nomouse

# Or stop and start
sudo systemctl stop nomouse
sudo systemctl start nomouse

# Check status
sudo systemctl status nomouse

# Set grid size
self.grid_size = 26

def _calculate_layout(self):
    screen = QApplication.primaryScreen().geometry()
    screen_width = screen.width()
    screen_height = screen.height()
    self.cell_width = screen_width // self.grid_size
    self.cell_height = screen_height // self.grid_size
    self.cell_centers = {}
    for code, (row, col) in self.codes.items():
        center_x = col * self.cell_width + self.cell_width // 2
        center_y = row * self.cell_height + self.cell_height // 2
        self.cell_centers[code] = (center_x, center_y)

def _draw_codes(self, painter):
    for code, (row, col) in self.codes.items():
        center_x, center_y = self.cell_centers[code]
        text_rect = painter.fontMetrics().boundingRect(code)
        text_x = center_x - text_rect.width() // 2
        text_y = center_y + text_rect.height() // 2
        painter.drawText(text_x, text_y, code)

def _generate_codes(self) -> Dict[str, Tuple[int, int]]:
    """Generate two-letter codes for the grid (AA-ZZ, 26x26)"""
    codes = {}
    letters = string.ascii_uppercase
    for row in range(self.grid_size):
        for col in range(self.grid_size):
            code = f"{letters[row]}{letters[col]}"
            codes[code] = (row, col)
    return codes

def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    font_size = min(self.cell_width, self.cell_height) // 4
    font = QFont("Arial", font_size, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QPen(QColor(255, 0, 0), 2))
    for code, (row, col) in self.codes.items():
        center_x, center_y = self.cell_centers[code]
        text_rect = painter.fontMetrics().boundingRect(code)
        text_x = center_x - text_rect.width() // 2
        text_y = center_y + text_rect.height() // 2
        painter.drawText(text_x, text_y, code)
    # (rest of your paintEvent for current input, unchanged) 