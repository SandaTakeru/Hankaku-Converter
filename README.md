# Hankaku-Converter

A QGIS plugin that converts string attribute values between full-width (Zenkaku) and half-width (Hankaku) characters.

このプラグインは、指定したベクタレイヤで String 型の属性値を全角・半角で相互変換する QGIS プラグインです。

## Features / 特徴

- Converts alphanumeric characters, symbols, and Katakana. / アルファベット・数字・記号・カタカナに対応。
- Convert a specific field only, or all string fields (leave the field blank). / 変換するフィールドを個別指定、または空欄で全フィールド対象。
- Convert selected features only. / 選択地物のみの変換に対応。
- Works on layers in edit mode. / 編集モード中のレイヤにも対応。
- Non-modal dialog: operate the map canvas while the dialog is open. / 非モーダルダイアログのため、マップキャンバスと同時に操作可能。

## Usage / 使い方

1. Select the target vector layer. / 対象のベクタレイヤを選択します。
2. (Optional) Specify the field to convert. Leave blank to convert all string fields. / 変換するフィールドを指定します（空欄で全フィールド）。
3. (Optional) Enable "selected features only" and/or "include Katakana". / 「選択地物のみ」「カタカナを含む」のオプションを設定します。
4. Choose the conversion direction (to full-width / to half-width) and run. / 変換方向（全角化／半角化）を選んで実行します。

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
