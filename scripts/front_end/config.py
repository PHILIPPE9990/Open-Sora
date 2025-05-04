

#Dimension
height = 700
width = 700
#Menu
action_menu_label = "Action"
action_menu_action_return = "Return to main menu"
#Label
desc = "Description"
video_length = "Video duration"
two_second = "2s"
four_second = "4s"
eight_second = "8s"
sixteen_second = "16s"
resolution = "Resolution"
og_prompt = "Please enter a subject:"
re_prompt = "AI Suggestions, Operated by Meta Llama2:"
dia_label = "Welcome to OpenSora"
dia_button = "🚀 Start"
dia_load = "Loading may take a few seconds. AI-generated content may contain errors—please regenerate if the result seems incorrect."
_144p = "144p"
_240p = "240p"
_360p = "360p"
_480p = "480p"
_720p = "720p"
submit = "🎬Submit"
reset = "🧹Reset"
download = "Download"
prompt = "✨AI Prompt Suggestion✨"
regenerate = "🔄Regenerate"
select = "✅Use"
Error_prompt = "Invalid input detected. Please follow the instructions carefully and try again."
Error_desc1 = "Error: Prompt should only contain english \ncharacters and numbers!"
Error_desc2 = "Error: Prompt length must be at least 5 words\n and at most 100 words!"
Error_option = "Error: Please select an option!"
#Color
resetColor = "#ff6666"
submitColor = "#85e085"
#Message
download_success_title = "Download successful"
download_success_message = "The file saved to:"
Generated_success_title = "Generate successful"
Generated_success_message = "Video generate successful!"
#Model
models = {
    "OpenSora v1.2 (High quality, low speed)": "opensora-v1-2",
    "OpenSora v1.1 (Medium quality, speed)": "opensora-v1-1",
    "OpenSora vA.B (Low quality, high speed)": "opensora-vA-B"
}
default_model = "OpenSora v1.2 (High quality, low speed)"
#Style
label_style = '''
'''
prompt_style = '''
'''
original_style = '''
'''
global_style = """
    QWidget {
        background-color: #2d2d2d;  /* Dark grey background */
        color: #ffffff;            /* Light grey text */
        font-weight: bold;
        selection-background-color: #6a0dad;
        selection-color: white;
    }
    
    /* Group Boxes */
    QGroupBox {
        border: 1px solid #2d2d2d;  
        border-radius: 4px;
        margin-top: 1ex;
        background-color: #383838;  /* Slightly lighter grey */
        padding: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: #ffffff;  /* Light grey */
        font-size: 12px;
    }

    QGroupBox QLabel {
        color: #ffffff;  /* Light grey */
        font-weight: bold;
        font-size: 14px;
        padding: 5px;
        background-color: #383838;
    }

    QComboBox {
        background-color: #383838;
        color: white;
        font-weight: bold;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px;
        min-width: 100px;
    }
    
    QComboBox:hover {
        border: 1px solid #777;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 1px;
        border-left-color: #555;
        border-left-style: solid;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    
    QComboBox::down-arrow {
        image: url(../../image/down_arrow.png);  /* Optional: replace with your own arrow icon */
        width: 12px;
        height: 12px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #383838;
        color: white;
        selection-background-color: #2a82da;
        border: 1px solid #555;
    }
    
    QComboBox QScrollBar:vertical {
        background: #383838;
        width: 10px;
    }
    
    /* Text Inputs */
    QTextEdit, QLineEdit {
        background-color: #383838;
        border: 1px solid #ffffff;
        color: #ffffff;
        padding: 5px;
        border-radius: 3px;
    }
    
    /* Buttons - Purple Accent */
    QPushButton {
        background-color: #8310d5;  /* Purple background */
        border: 1px solid #4b0082;   /* Dark purple border */
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #6a0dad;  /* Slightly brighter purple */
    }
    
    QPushButton:pressed {
        background-color: #4a148c;  /* Darker purple */
    }
    
    QPushButton:disabled {
        background-color: #3e3e3e;
        color: #808080;
    }
    
    /* Radio Buttons */
    QRadioButton {
        color: #ffffff;
        spacing: 6px;
        background: #383838;
    }
    
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid #666666;
        background: #383838;
    }
    
    QRadioButton::indicator:checked {
        background-color: #00ff99;
        border-color: #4b0082;
        border: 1px solid #4b0082;
    }
    
    /* Slider */
    QGroupBox QSlider{
        border: 0px solid #ffffff;  
        border-radius: 4px;
        margin-top: 1ex;
        background-color: #383838;  
        padding: 10px;
    }

    QSlider::groove:horizontal {
        border: 2px solid #444444;
        height: 6px;
        background: #666666;
        margin: 2px 0;
        border-radius: 3px;
    }
    
    QSlider::handle:horizontal {
        background: #00ff99;
        border: 1px solid #4b0082;
        width: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }
    
    /* Scroll Bars */
    QScrollBar:vertical {
        border: none;
        background: #383838;
        width: 10px;
    }
    
    QScrollBar::handle:vertical {
        background: #555555;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #6a0dad;
    }
    
    /* Menu */
    QMenu {
        background-color: #383838;
        border: 1px solid #444444;
        color: #ffffff;
    }
    
    QMenu::item:selected {
        background-color: #6a0dad;
    }
    
    /* List Widgets */
    QListWidget {
        background-color: #383838;
        border: 1px solid #444444;
        color: #ffffff;
        show-decoration-selected: 1;
    }
    
    QListWidget::item:selected {
        background-color: #6a0dad;
    }
"""
dialog_label = '''
QLabel {
    color: #e0e0e0;
    font-weight: bold;
    font-size: 32px;
    padding-bottom:30px;
}
'''
dialog_button = '''
QPushButton {
    background-color: #8310d5;  /* Purple background */
    border: 1px solid #ffffff;   /* Dark purple border */
    color: #ffffff;
    font-weight: bold;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #6a0dad;
}
QPushButton:pressed {
    background-color: #4a148c;  /* Darker purple */
}
'''
