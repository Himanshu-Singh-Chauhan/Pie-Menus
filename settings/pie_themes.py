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


# Try to apply this QMenu css to only tray qmenu and rename this style to tray_menu
QMenu = """
            QMenu {
                background-color: rgba(255, 255, 255, 255);
                border: none;
                border-radius: 10px;
            }

            QMenu::item {
                border-radius: 4px;
                padding: 8px 48px 8px 36px;
                background-color: transparent;
                margin: 10px;
            }
            QMenu::item:selected {
                border-radius: 10px;
                background-color: rgba(232, 232, 232, 232);
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