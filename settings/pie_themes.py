from dotmap import DotMap

pie_themes = DotMap()
pie_selection_theme = DotMap()
tray_theme = DotMap()

theme = pie_themes # alias


pie_themes.default_theme = """
        QPushButton
        {
            color: white;
            background-color: rgb(255, 0, 68);
            outline: none;
            font-size: 16px;
            font: "Segoe UI";
            text-decoration: none;
            font-weight: 400;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 15px;
            padding-right: 15px;
            min-width: 10px;
            min-height: 10px;
            border-radius: 6px;
        }
        QPushButton[hover=true]
        {
            background-color: #f9e506;
            color: #000;
        }
        QPushButton:pressed, QPushButton[pressed=true]
        {
            background-color: #F2FC82;
        }
        
    """

theme.dhalu_theme = """
        QPushButton
        {
            color: white;
            background-color: rgb(75, 116, 255);
            outline: none;
            font-size: 16px;
            font: "Comic Sans MS";
            text-decoration: none;
            font-weight: 400;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 15px;
            padding-right: 15px;
            min-width: 10px;
            min-height: 10px;
            border-radius: 10px;
        }
        QPushButton[hover=true]
        {
            background-color: rgb(255, 0, 68);
            color: white;
        }
        QPushButton:pressed, QPushButton[pressed=true]
        {
            background-color: #F2FC82;
        }

    """


theme.partial_invisible = """
    QPushButton
            {
                color: white;
                /*background-color: rgb(255, 0, 68); this is comment is css*/
                outline: none;
                font-size: 16px;
                font: "Segoe UI";
                text-decoration: none;
                font-weight: 400;
                padding-top: 5px;
                padding-bottom: 5px;
                padding-left: 15px;
                padding-right: 15px;
                min-width: 10px;
                min-height: 10px;
                border-radius: 6px;
                border: 0px solid;
            }
            QPushButton[hover=true]
            {
                background-color: #f9e506;
                color: #000;
            }
            QPushButton:pressed, QPushButton[pressed=true]
            {
                background-color: #F2FC82;
            }
    """


theme.whatsapp_green = """
        QPushButton
        {
            color: rgb(6, 210, 83);
            background-color: white;
            outline: none;
            font-size: 19px;
            font-weight: 400;
            padding: 3px 15px 3px 15px;
            min-width: 10px;
            min-height: 10px;
            border: 1px solid rgb(6, 210, 83);
            border-radius: 4px;
        }
        QPushButton[hover=true]
        {
            color: white;
            background-color: rgb(6, 210, 83);
        }
        QPushButton:pressed, QPushButton[pressed=true]
        {
            background-color:rgb(6, 210, 83);
        }

    """



theme.simple_box_theme = """ """


# Inner circle and line theme
pie_selection_theme.default = {
    "bg_circle": "#f9e506",
    "fg_circle": "#FF0044",
    "thickness": 8
}

pie_selection_theme.whatsapp_green = {
    "bg_circle": "#ffffff",
    "fg_circle": "#00e106",
    "thickness": 8
}

# Testing and debugging themes
theme.testing_theme = """
        QPushButton
        {
            color: black;
            outline: none;
            font-size: 16px;
            font: "Segoe UI";
            text-decoration: none;
            font-weight: 400;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 15px;
            padding-right: 15px;
            min-width: 10px;
            min-height: 10px;
            border-radius: 6px;
            border: 0px solid;
            background-image: url("C:\/Users\/S\/Pictures\/2.png");
        }
        QPushButton[hover=true]
        {
            color: white;
            background: none;
            background-color: #5051FB;
        }
        QPushButton:pressed, QPushButton[pressed=true]
        {
            background-color: #F2FC82;
        }
        QPushButton::icon {
            padding-left: 55px;
            padding-right: 55px;
        }
    """




# Tray icon themes
tray_theme.QMenu = """
            QMenu {
                background-color: rgba(255, 255, 255, 255);
                border: none;
                border-radius: 10px;
                /*font: 18px;*/
            }

            QMenu::item {
                color: black;
                padding: 8px 78px 8px 26px;
                background-color: transparent;
                margin: 6px 0 6px 0;
            }
            QMenu::item:selected {
                background-color: rgba(75, 116, 255, 130);
            }
            QMenu::item:disabled {
                background-color: transparent;
            }
            QMenu::icon {
                left: 15px;
            }
            QMenu::separator {
                height: 2px;
                background-color: rgb(232, 236, 243);
            }
"""

tray_theme.danger = """
            QMenu::item:selected {
                color: white;
                /*font-weight: bold;*/
                background-color: rgb(255, 0, 12);
            }
"""

tray_theme.warning = """
            QMenu::item:selected {
                color: black;
                /*font-weight: bold;*/
                background-color: rgb(249, 229, 6);
            }
"""