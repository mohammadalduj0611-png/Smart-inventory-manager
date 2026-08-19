
# ============================================================
# pages/settings.py
# Smart Inventory Manager
# Settings Page
# ============================================================

import json
import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
)

from translations import tr, LANGUAGES


SETTINGS_FILE = "settings.json"


# ============================================================
# Settings Helpers
# ============================================================

def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        return {
            "language": "English"
        }

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            settings = json.load(file)

            if not isinstance(settings, dict):

                return {
                    "language": "English"
                }

            language = settings.get(
                "language",
                "English"
            )

            if language not in (
                "English",
                "Arabic"
            ):

                language = "English"

            settings["language"] = language

            return settings

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {
            "language": "English"
        }


def save_settings(settings):

    try:

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=4
            )

        return True

    except OSError:

        return False


# ============================================================
# Settings Page
# ============================================================

class SettingsPage(QWidget):

    language_changed = Signal(str)

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.settings = load_settings()

        self.current_language = self.settings.get(
            "language",
            "English"
        )

        self.setup_ui()

        self.load_current_settings()

        self.update_language()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            30,
            25,
            30,
            30
        )

        layout.setSpacing(
            20
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        self.title_label = QLabel()

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #172033;
            }
        """)

        layout.addWidget(
            self.title_label
        )

        self.subtitle_label = QLabel()

        self.subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #64748b;
            }
        """)

        layout.addWidget(
            self.subtitle_label
        )

        # ----------------------------------------------------
        # Language Card
        # ----------------------------------------------------

        self.language_card = QFrame()

        self.language_card.setObjectName(
            "languageCard"
        )

        card_layout = QVBoxLayout(
            self.language_card
        )

        card_layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        card_layout.setSpacing(
            15
        )

        self.language_title = QLabel()

        self.language_title.setStyleSheet("""
            QLabel {
                font-size: 19px;
                font-weight: bold;
                color: #172033;
            }
        """)

        card_layout.addWidget(
            self.language_title
        )

        self.language_description = QLabel()

        self.language_description.setWordWrap(
            True
        )

        self.language_description.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #64748b;
            }
        """)

        card_layout.addWidget(
            self.language_description
        )

        # ----------------------------------------------------
        # Language Row
        # ----------------------------------------------------

        language_row = QHBoxLayout()

        self.language_label = QLabel()

        self.language_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #172033;
            }
        """)

        language_row.addWidget(
            self.language_label
        )

        language_row.addStretch()

        self.language_combo = QComboBox()

        # English
        self.language_combo.addItem(
            LANGUAGES["English"],
            "English"
        )

        # Arabic
        self.language_combo.addItem(
            LANGUAGES["Arabic"],
            "Arabic"
        )

        self.language_combo.currentIndexChanged.connect(
            self.change_language
        )

        self.language_combo.setMinimumWidth(
            190
        )

        language_row.addWidget(
            self.language_combo
        )

        card_layout.addLayout(
            language_row
        )

        layout.addWidget(
            self.language_card
        )

        # ----------------------------------------------------
        # Save Button
        # ----------------------------------------------------

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.save_button = QPushButton()

        self.save_button.clicked.connect(
            self.save_current_settings
        )

        buttons.addWidget(
            self.save_button
        )

        layout.addLayout(
            buttons
        )

        layout.addStretch()

        self.apply_style()

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QWidget {
                background: #f3f6fa;
            }

            QFrame#languageCard {

                background: white;

                border: 1px solid #e5e7eb;

                border-radius: 14px;
            }

            QComboBox {

                background: white;

                border: 1px solid #d1d5db;

                border-radius: 8px;

                padding: 10px;

                font-size: 14px;

                color: #172033;
            }

            QComboBox:hover {

                border: 1px solid #2563eb;
            }

            QComboBox:focus {

                border: 2px solid #2563eb;
            }

            QComboBox QAbstractItemView {

                background: white;

                border: 1px solid #d1d5db;

                selection-background-color: #dbeafe;

                selection-color: #172033;
            }

            QPushButton {

                background: #2563eb;

                color: white;

                border: none;

                border-radius: 8px;

                padding: 11px 22px;

                font-weight: bold;
            }

            QPushButton:hover {

                background: #1d4ed8;
            }
        """)

    # ========================================================
    # Load Settings
    # ========================================================

    def load_current_settings(self):

        language = self.settings.get(
            "language",
            "English"
        )

        if language not in (
            "English",
            "Arabic"
        ):

            language = "English"

        self.current_language = language

        index = (
            self.language_combo.findData(
                language
            )
        )

        if index == -1:

            index = 0

        self.language_combo.blockSignals(
            True
        )

        self.language_combo.setCurrentIndex(
            index
        )

        self.language_combo.blockSignals(
            False
        )

    # ========================================================
    # Change Language
    # ========================================================

    def change_language(self):

        language = self.language_combo.currentData()

        if language not in (
            "English",
            "Arabic"
        ):

            return

        self.current_language = language

        self.settings["language"] = language

        save_settings(
            self.settings
        )

        # إرسال اللغة إلى MainWindow
        self.language_changed.emit(
            language
        )

        # تحديث صفحة Settings نفسها
        self.update_language()

    # ========================================================
    # Save
    # ========================================================

    def save_current_settings(self):

        language = self.language_combo.currentData()

        if language not in (
            "English",
            "Arabic"
        ):

            language = "English"

        self.current_language = language

        self.settings["language"] = language

        if save_settings(
            self.settings
        ):

            self.language_changed.emit(
                language
            )

            self.update_language()

    # ========================================================
    # Update Language
    # ========================================================

    def update_language(self):

        language = self.current_language

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        self.title_label.setText(
            tr(
                "settings_title",
                language
            )
        )

        self.subtitle_label.setText(
            tr(
                "settings_subtitle",
                language
            )
        )

        # ----------------------------------------------------
        # Language Card
        # ----------------------------------------------------

        self.language_title.setText(
            tr(
                "language",
                language
            )
        )

        self.language_description.setText(
            tr(
                "language_description",
                language
            )
        )

        self.language_label.setText(
            tr(
                "application_language",
                language
            )
        )

        # ----------------------------------------------------
        # Save Button
        # ----------------------------------------------------

        self.save_button.setText(
            tr(
                "save_settings",
                language
            )
        )

        # ----------------------------------------------------
        # RTL / LTR
        # ----------------------------------------------------

        from PySide6.QtCore import Qt

        if language == "Arabic":

            self.setLayoutDirection(
                Qt.RightToLeft
            )

        else:

            self.setLayoutDirection(
                Qt.LeftToRight
            )

    # ========================================================
    # External Refresh
    # ========================================================

    def refresh_language(self):

        self.settings = load_settings()

        self.current_language = self.settings.get(
            "language",
            "English"
        )

        self.load_current_settings()

        self.update_language()
