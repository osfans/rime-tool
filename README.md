## [trime]碼表製作工具

### 用法
- 環境: [python3] + [PyYAML]
- 命令: 參數為data目錄下的一個或多個方案名，如luna_pinyin。如不指定，則為"thaerv thaerv_ipa soutseu pinyin zhuyin"

  > <code>python3 trime-tool.py luna_pinyin</code>

- trime.db: 上述命令生成的trime.db碼表文件有如下三种用法：
  - 放到手機/sdcard根目錄下，在trime設置中導入碼表
  - 已root的手機可以直接<code>adb push trime.db/data/data/com.osfans.trime/databases/</code>
  - 放到trime的源代碼的assests目錄下，重新編譯生成新apk

### 目錄結構
- data/:
  - essay.txt: [Rime]中的【八股文】預設詞彙表
  - schema.yaml: 輸入法方案
  - dict.yaml: 輸入法詞典
- [opencc]/ : 繁簡轉換工具
- trime.apk: 輸入法主程序
- **trime-tool.py**: 碼表製作工具主程序

[trime]: https://github.com/osfans/trime
[python3]: https://www.python.org/downloads/release/python-340/
[PyYAML]: http://pyyaml.org/wiki/PyYAML
[opencc]: https://github.com/BYVoid/OpenCC
[Rime]: https://code.google.com/p/rimeime/
