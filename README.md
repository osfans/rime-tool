## [trime]碼表製作工具

### 用法
- 環境: [python3] + [PyYAML]
- 命令: 參數為一個或多個方案文件名，如brise/preset/luna_pinyin.schema.yaml。

  > `python3 trime-tool.py brise/preset/luna_pinyin.schema.yaml`

- trime.db: 上述命令生成的trime.db碼表文件有如下幾种用法：
  - 放到手機/sdcard下，在trime設置中導入碼表
  - 已root的手機可以直接`adb push trime.db/data/data/com.osfans.trime/databases/`
  - 放到trime的源代碼的assets目錄下，重新編譯生成新apk
  - 替換apk中的assets目錄中的同名文件，重新打包生成新apk

- [碼表格式說明](data/README.md)

### 目錄結構
- data/:
  - *.schema.yaml: 輸入法方案
  - *.dict.yaml: 輸入法詞典
- [OpenCC]/ : 開放中文繁簡轉換工具
- [trime.apk](trime.apk): 輸入法主程序
- **trime-tool.py**: 碼表製作工具主程序

[trime]: https://github.com/osfans/trime
[python3]: https://www.python.org/downloads/release/python-340/
[PyYAML]: http://pyyaml.org/wiki/PyYAML
[opencc]: https://github.com/BYVoid/OpenCC
[Rime]: https://code.google.com/p/rimeime/
