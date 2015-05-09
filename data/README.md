## 碼表格式說明
- trime碼表由多套輸入方案構成。
- 每套輸入方案包含一個「方案定義」和一個「詞典」文件。不同方案可公用詞典文件。
- 推薦詞典文件使用正體中文，輸入法可設置輸出簡體。
- 在拼音方案不唯一的情況下，詞典文件推薦使用國際音標方案編碼。

### 相關知識
- [yaml]：一種數據描述語言，「方案定義」和「詞典」文件均使用該語言編寫而成。
- [正則表達式]：用於音節切分和各種規則轉換。java中使用的是ICU實現的正則表達式。


[yaml]: http://yaml.org/
[正則表達式]: http://developer.android.com/reference/java/util/regex/Pattern.html
[Rime的詞典文件]: https://github.com/rime/home/wiki/RimeWithSchemata#碼表與詞典 
