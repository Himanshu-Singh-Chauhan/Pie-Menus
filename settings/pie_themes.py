from dotmap import DotMap
import os

pie_themes = DotMap()
pie_selection_theme = DotMap()
tray_theme = DotMap()

theme = pie_themes # alias

script_dir = os.path.dirname(__file__)
pie_bgs = os.path.join(os.path.split(script_dir)[0], "resources/pie_bgs/")

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


theme.layan = """
QPushButton
        {{
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
            background-image: url("{0}");
        }}
        QPushButton[hover=true]
        {{
            color: white;
            background: none;
            background-color: #5051FB;
        }}
        QPushButton:pressed, QPushButton[pressed=true]
        {{
            background-color: #5051FB;
        }}
    """.format(os.path.join(pie_bgs, "layan.png").replace("\\", "\/").replace("/", "\/"))

    
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


theme.windows_11 = """
        QPushButton
        {{
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
            background-image: url("{0}");
        }}
        QPushButton[hover=true]
        {{
            color: #363437;
        }}
        QPushButton:pressed, QPushButton[pressed=true]
        {{
            background-color: #5051FB;
        }}
    """.format(os.path.join(pie_bgs, "windows11.png").replace("\\", "\/").replace("/", "\/"))


# SELECTION THEMES
# Inner circle and line theme and svg hovers
pie_selection_theme.default = {
    # ------ these three should be defined together 
    # or else this default selection theme will be used.
    "bg_circle": "#f9e506",
    "fg_circle": "#FF0044",
    "thickness": 8
    # ------ these above three --------------------
}

pie_selection_theme.whatsapp_green = {
    "bg_circle": "#ffffff",
    "fg_circle": "#00e106",
    "thickness": 8
}

pie_selection_theme.windows_11 = {
    "bg_circle": "#D9246A",
    "fg_circle": "#D4608E",
    "thickness": 8,
    "svg_nohover_hover"      : "#ffffff_#000000"
}




# --------------- TESTING THEME ----------------------
# Testing and debugging themes

pie_selection_theme.testing_theme = {
    "bg_circle": "#D9246A",
    "fg_circle": "#D4608E",
    "thickness": 8,
    "svg_nohover_hover"      : "#ffffff_#000000"
}

theme.testing_theme = """
        QPushButton
        {{
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
            background-image: url("{0}");
        }}
        QPushButton[hover=true]
        {{
            color: #363437;
        }}
        QPushButton:pressed, QPushButton[pressed=true]
        {{
            background-color: #5051FB;
        }}
    """.format(os.path.join(pie_bgs, "windows11.png").replace("\\", "\/").replace("/", "\/"))

# -----------/END TESTING THEME ----------------------





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