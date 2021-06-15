default_theme = """
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

dhalu_theme = """
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


whatsapp_green = """
                    QPushButton
                    {
                        color: rgb(6, 210, 83);
                        background-color: white;
                        outline: none;
                        font-size: 16px;
                        font-weight: 400;
                        padding: 7px 15px 7px 15px;
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



simple_box_theme = """



        """



testing_theme = """QPushButton {
    background-color: palegoldenrod;
    border-width: 2px;
    border-color: darkkhaki;
    border-style: solid;
    border-radius: 5;
    padding: 3px;
    min-width: 9ex;
    min-height: 2.5ex;
}

QPushButton:hover {
   background-color: khaki;
}

/* Increase the padding, so the text is shifted when the button is
   pressed. */
QPushButton:pressed {
    padding-left: 5px;
    padding-top: 5px;
    background-color: #d0d67c;
}

QLabel, QAbstractButton {
    font: bold;
}
"""

# Try to apply this QMenu css to only tray qmenu and rename this style to tray_menu
QMenu = """
            QMenu {
                background-color: rgba(255, 255, 255, 255);
                border: none;
                border-radius: 10px;
                /*font: 18px;*/
            }

            QMenu::item {
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

qmenu_danger = """
            QMenu::item:selected {
                color: white;
                /*font-weight: bold;*/
                background-color: rgb(255, 0, 12);
            }
"""

qmenu_warning = """
            QMenu::item:selected {
                color: black;
                /*font-weight: bold;*/
                background-color: rgb(249, 229, 6);
            }
"""