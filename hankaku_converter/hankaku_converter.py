# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .resources import *
from .hankaku_converter_dialog import HankakuConverterDialog
import os.path

# 半角カタカナ → 全角カタカナ 基本マッピング
_HAN_TO_ZEN_KATA = {
    'ｦ': 'ヲ', 'ｧ': 'ァ', 'ｨ': 'ィ', 'ｩ': 'ゥ', 'ｪ': 'ェ', 'ｫ': 'ォ',
    'ｬ': 'ャ', 'ｭ': 'ュ', 'ｮ': 'ョ', 'ｯ': 'ッ', 'ｰ': 'ー',
    'ｱ': 'ア', 'ｲ': 'イ', 'ｳ': 'ウ', 'ｴ': 'エ', 'ｵ': 'オ',
    'ｶ': 'カ', 'ｷ': 'キ', 'ｸ': 'ク', 'ｹ': 'ケ', 'ｺ': 'コ',
    'ｻ': 'サ', 'ｼ': 'シ', 'ｽ': 'ス', 'ｾ': 'セ', 'ｿ': 'ソ',
    'ﾀ': 'タ', 'ﾁ': 'チ', 'ﾂ': 'ツ', 'ﾃ': 'テ', 'ﾄ': 'ト',
    'ﾅ': 'ナ', 'ﾆ': 'ニ', 'ﾇ': 'ヌ', 'ﾈ': 'ネ', 'ﾉ': 'ノ',
    'ﾊ': 'ハ', 'ﾋ': 'ヒ', 'ﾌ': 'フ', 'ﾍ': 'ヘ', 'ﾎ': 'ホ',
    'ﾏ': 'マ', 'ﾐ': 'ミ', 'ﾑ': 'ム', 'ﾒ': 'メ', 'ﾓ': 'モ',
    'ﾔ': 'ヤ', 'ﾕ': 'ユ', 'ﾖ': 'ヨ',
    'ﾗ': 'ラ', 'ﾘ': 'リ', 'ﾙ': 'ル', 'ﾚ': 'レ', 'ﾛ': 'ロ',
    'ﾜ': 'ワ', 'ﾝ': 'ン',
    'ﾞ': '゛', 'ﾟ': '゜',
}

# 半角カタカナ + 濁点 → 全角濁音（次文字がﾞのとき）
_HAN_KATA_DAKUTEN = {
    'ｶ': 'ガ', 'ｷ': 'ギ', 'ｸ': 'グ', 'ｹ': 'ゲ', 'ｺ': 'ゴ',
    'ｻ': 'ザ', 'ｼ': 'ジ', 'ｽ': 'ズ', 'ｾ': 'ゼ', 'ｿ': 'ゾ',
    'ﾀ': 'ダ', 'ﾁ': 'ヂ', 'ﾂ': 'ヅ', 'ﾃ': 'デ', 'ﾄ': 'ド',
    'ﾊ': 'バ', 'ﾋ': 'ビ', 'ﾌ': 'ブ', 'ﾍ': 'ベ', 'ﾎ': 'ボ',
    'ｳ': 'ヴ',
}

# 半角カタカナ + 半濁点 → 全角半濁音（次文字がﾟのとき）
_HAN_KATA_HANDAKUTEN = {
    'ﾊ': 'パ', 'ﾋ': 'ピ', 'ﾌ': 'プ', 'ﾍ': 'ペ', 'ﾎ': 'ポ',
}

# 全角カタカナ → 半角カタカナ（濁音・半濁音は2文字に展開）
_ZEN_TO_HAN_KATA = {
    'ヲ': 'ｦ', 'ァ': 'ｧ', 'ィ': 'ｨ', 'ゥ': 'ｩ', 'ェ': 'ｪ', 'ォ': 'ｫ',
    'ャ': 'ｬ', 'ュ': 'ｭ', 'ョ': 'ｮ', 'ッ': 'ｯ', 'ー': 'ｰ',
    'ア': 'ｱ', 'イ': 'ｲ', 'ウ': 'ｳ', 'エ': 'ｴ', 'オ': 'ｵ',
    'カ': 'ｶ', 'キ': 'ｷ', 'ク': 'ｸ', 'ケ': 'ｹ', 'コ': 'ｺ',
    'サ': 'ｻ', 'シ': 'ｼ', 'ス': 'ｽ', 'セ': 'ｾ', 'ソ': 'ｿ',
    'タ': 'ﾀ', 'チ': 'ﾁ', 'ツ': 'ﾂ', 'テ': 'ﾃ', 'ト': 'ﾄ',
    'ナ': 'ﾅ', 'ニ': 'ﾆ', 'ヌ': 'ﾇ', 'ネ': 'ﾈ', 'ノ': 'ﾉ',
    'ハ': 'ﾊ', 'ヒ': 'ﾋ', 'フ': 'ﾌ', 'ヘ': 'ﾍ', 'ホ': 'ﾎ',
    'マ': 'ﾏ', 'ミ': 'ﾐ', 'ム': 'ﾑ', 'メ': 'ﾒ', 'モ': 'ﾓ',
    'ヤ': 'ﾔ', 'ユ': 'ﾕ', 'ヨ': 'ﾖ',
    'ラ': 'ﾗ', 'リ': 'ﾘ', 'ル': 'ﾙ', 'レ': 'ﾚ', 'ロ': 'ﾛ',
    'ワ': 'ﾜ', 'ン': 'ﾝ',
    '゛': 'ﾞ', '゜': 'ﾟ',
    'ガ': 'ｶﾞ', 'ギ': 'ｷﾞ', 'グ': 'ｸﾞ', 'ゲ': 'ｹﾞ', 'ゴ': 'ｺﾞ',
    'ザ': 'ｻﾞ', 'ジ': 'ｼﾞ', 'ズ': 'ｽﾞ', 'ゼ': 'ｾﾞ', 'ゾ': 'ｿﾞ',
    'ダ': 'ﾀﾞ', 'ヂ': 'ﾁﾞ', 'ヅ': 'ﾂﾞ', 'デ': 'ﾃﾞ', 'ド': 'ﾄﾞ',
    'バ': 'ﾊﾞ', 'ビ': 'ﾋﾞ', 'ブ': 'ﾌﾞ', 'ベ': 'ﾍﾞ', 'ボ': 'ﾎﾞ',
    'ヴ': 'ｳﾞ',
    'パ': 'ﾊﾟ', 'ピ': 'ﾋﾟ', 'プ': 'ﾌﾟ', 'ペ': 'ﾍﾟ', 'ポ': 'ﾎﾟ',
}


def _han_kata_to_zen(text):
    """半角カタカナ → 全角カタカナ（濁点・半濁点の結合を考慮）"""
    result = []
    i = 0
    while i < len(text):
        c = text[i]
        if c in _HAN_TO_ZEN_KATA:
            if i + 1 < len(text):
                next_c = text[i + 1]
                if next_c == 'ﾞ' and c in _HAN_KATA_DAKUTEN:
                    result.append(_HAN_KATA_DAKUTEN[c])
                    i += 2
                    continue
                elif next_c == 'ﾟ' and c in _HAN_KATA_HANDAKUTEN:
                    result.append(_HAN_KATA_HANDAKUTEN[c])
                    i += 2
                    continue
            result.append(_HAN_TO_ZEN_KATA[c])
        else:
            result.append(c)
        i += 1
    return ''.join(result)


def _zen_kata_to_han(text):
    """全角カタカナ → 半角カタカナ（濁音・半濁音は2文字に展開）"""
    return ''.join(_ZEN_TO_HAN_KATA.get(c, c) for c in text)


class HankakuConverter:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')
        if locale is not None:
            locale = locale[0:2]
        else:
            locale = 'en'
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'HankakuConverter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Hankaku Converter')
        self.toolbar = self.iface.addToolBar(u'HankakuConverter')
        self.toolbar.setObjectName(u'HankakuConverter')

    def tr(self, message):
        return QCoreApplication.translate('HankakuConverter', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Hankaku Converter'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg = HankakuConverterDialog(self.iface.mainWindow())
        self.dlg.accepted.connect(self._on_accepted)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Hankaku Converter'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar
        self.dlg.close()

    def run(self):
        if not self.dlg.isVisible():
            layer = self.iface.activeLayer()
            self.dlg.mMapLayerComboBox.setLayer(layer)
            self.dlg.mFieldComboBox.setLayer(layer)
        self.dlg.show()
        self.dlg.raise_()
        self.dlg.activateWindow()

    def _on_accepted(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        if layer is None:
            return

        convert_to_half = self.dlg.radioButton_ZtoH.isChecked()
        include_katakana = self.dlg.checkBox_katakana.isChecked()
        selected_only = self.dlg.checkBox_selected.isChecked()
        field_name = self.dlg.mFieldComboBox.currentField() or None

        if selected_only and layer.selectedFeatureCount() == 0:
            self.iface.messageBar().pushWarning(
                'Hankaku Converter', '選択地物がありません。')
            return

        self._convert_characters(layer, convert_to_half, include_katakana, field_name, selected_only)

    def _convert_characters(self, layer, convert_to_half, include_katakana, field_name, selected_only):
        if convert_to_half:
            trans_table = str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
        else:
            trans_table = str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})

        def convert_value(value):
            result = value.translate(trans_table)
            if include_katakana:
                if convert_to_half:
                    result = _zen_kata_to_han(result)
                else:
                    result = _han_kata_to_zen(result)
            return result

        was_editing = layer.isEditable()
        if not was_editing:
            if not layer.startEditing():
                return

        try:
            features = layer.selectedFeatures() if selected_only else layer.getFeatures()
            fields = [layer.fields().field(field_name)] if field_name else list(layer.fields())

            for feature in features:
                changed = False
                for field in fields:
                    value = feature[field.name()]
                    if isinstance(value, str) and value:
                        new_value = convert_value(value)
                        if new_value != value:
                            feature.setAttribute(field.name(), new_value)
                            changed = True
                if changed:
                    layer.updateFeature(feature)

        except Exception as e:
            if not was_editing:
                layer.rollBack()
            self.iface.messageBar().pushCritical(
                'Hankaku Converter', f'エラーが発生しました: {e}')
            return

        if not was_editing:
            layer.commitChanges()
