# 外觀：Offbeat 設計語言

> `/dashboard` 與 `/demo` 的外觀規範。全域規則見 [AGENTS.md](../AGENTS.md)，分層見 [architecture.md](architecture.md)。
> 內容是刻意的設計決策與踩過的坑（⚠️ 標記），改動對應程式前請先讀完相關段落。

## 風格

**Offbeat** 是 lazyrhythm 的個人設計語言（與「無感記帳」App 的 Offbeat 主題同一套）：**Nord × Brutalism**。
冷靜的北歐苔原色票（Nord Palette）＋ 刻意的結構暴力感（偏移陰影、2px 裸邊框、直角）——有稜角但不刺眼，有個性但不吵鬧。
色值與規則以 lazyrhythm 的 **Offbeat 設計系統（tokens v1）** 為唯一標準，與 Driftread、Lazyrhythm、LazyEmbed、無感記帳共用；本檔只記 WorldPane 怎麼套用它。

命名來源：偏移陰影（**off**set）＋ 反拍節奏（**offbeat**）——結構刻意錯開，落點不在正拍上。

WorldPane 的網頁是工具型介面（監視牆、管理表單、回放控制），旋鈕設在 `STRUCTURE_WEIGHT 6 / MOTION_INTENSITY 3`：
直角（Web 一律 `--radius: 0`；裝置畫面裡的窗是模擬螢幕內容，維持 2px）、偏移 `offset-sm` 3px、幾乎不做動畫（只有角色呼吸與按鈕按下的位移，且尊重 `prefers-reduced-motion`）。

## 檔案與內嵌方式

- **`worldpane-server/src/worldpane_server/static/offbeat.css` 是網頁顏色的唯一來源**：Nord 色碼只出現在這個檔案，
  其餘元件（面板、按鈕、輸入框、分頁、chip、表格、dialog、toast、裝置畫面的天空）也在這裡定義
- 每個頁面的 `<style>` 第一行是 `/*__OFFBEAT_CSS__*/` 佔位註解，`worldpane_server/theme.py` 的 `with_offbeat()` 在送出前把整份 CSS 內嵌進去
- **刻意內嵌而不是 `<link>` 一個 `/static/offbeat.css`** ⚠️：`scripts/build_demo_html.py` 會把 `/demo` 寫成一個可以單獨打開的 HTML 檔，
  外連樣式表在離線檔案裡會失效；內嵌也讓兩個頁面都維持「一個請求就拿到完整畫面」
- 頁面裡只放版面（grid、尺寸、位置）與頁面專屬元件，**顏色一律用語意 token**

## Token 分兩層

| 層 | 例子 | 誰可以用 |
|----|------|----------|
| Nord 色票與衍生值 | `--nord-polar0`、`--nord-frost1`、`--nord-red`、`--nord-dim-ink`、`--nord-red-ink-dark` | **只有 `offbeat.css` 自己** |
| 語意 token | `--bg`、`--panel`、`--line`、`--line-control`、`--ink`、`--muted`、`--accent`、`--accent-fill`、`--ok`／`--ok-ink`、`--warn`／`--warn-ink`、`--danger`／`--danger-ink`、`--home`、`--sky-day`、`--look-1` | 頁面 CSS 與 JS |

**頁面不寫色碼、也不直接引用 `--nord-*`** ⚠️：頁面以「這是面板的底」「這是次要文字」「這是危險操作」表達意圖，由 `offbeat.css` 決定它是哪個顏色。
要調整外觀（甚至日後換一套色票）只改 `offbeat.css` 的對應，兩個頁面零改動——與無感記帳「頁面不判斷主題身分、只讀主題提供的能力」同一個原則。
JS 需要顏色時也一樣：字串寫成 `var(--look-xiaobai)`、`var(--home)`，或設 `data-sky="day"` 讓 CSS 對應，不寫 `#xxxxxx`。

`worldpane-server/tests/test_theme.py` 擋下頁面（HTML、CSS、JS）裡的 hex／`rgb()` 色碼，並檢查 `offbeat.css` 的每一個色碼都來自 Nord 色票或設計系統的衍生值、偏移陰影都是實色、`--radius` 是 0。

## 用色規則

**對比原則**：Nord 原色負責「被看見」（填色、邊框、圓點、左邊條、偏移陰影），`*-ink` 負責「被讀懂」（文字）。
每個文字 token 在 polar0／polar1／polar2 三層上都 ≥ 4.5:1，字放在面板、標題欄或頁面底上都不必再判斷。

| 用途 | token | 色值 |
|------|-------|------|
| 頁面底 | `--bg` | polar0 `#2E3440`（永遠最深，不用純黑） |
| 面板、卡片、裝置外框 | `--panel`、`--bezel` | polar1 `#3B4252` |
| 標題欄、hover、選中的列與分頁 | `--panel-head` | polar2 `#434C5E` |
| 面板裡的輸入框 | `--field` | polar0（比面板深一階才分得出來） |
| 結構邊框、分隔線（裝飾性） | `--line` | polar3 `#4C566A` |
| 控制項外框（按鈕、chip、checkbox） | `--line-control` | `#838EA6`（≥ 3:1） |
| 主要文字／標題／最亮 | `--ink`／`--ink-strong`／`--ink-bright` | snow0／snow1／snow2 |
| 次要文字、placeholder、表頭 | `--muted` | dim-ink `#B8BDC8`（6.63／5.34／4.58） |
| 強調文字、連結、時鐘、focus | `--accent` | frost-ink `#93C6D4`（6.70／5.40／4.63） |
| 主按鈕底、checkbox、選中分頁的底線 | `--accent-fill` + 字 `--accent-ink` | frost1 `#88C0D0` + polar0（6.24:1） |
| 危險按鈕 | `--danger-fill`／`--danger-fill-hover` + snow2 字 | `#A54049`（5.31:1）／`#8F3A42`（6.39:1） |
| 成功／警告／危險（標記） | `--ok`／`--warn`／`--danger` | Aurora green／orange／red |
| 成功／警告／危險（文字） | `--ok-ink`／`--warn-ink`／`--danger-ink` | `#B0CB98`／`#F3AE95`／`#F4ABB2` |
| 資訊／注意 | `--info`／`--notice` | frost2、Aurora yellow（黃在三層上都 ≥ 5.5:1，可直接當字） |

- **任何 Nord 原色都不直接當文字色** ⚠️：舊版的 dim `#9AA0AD` 在 polar1 只有 3.84:1、frost1 在 polar2 只有 4.31:1、Aurora red 在 polar1 只有 2.46:1。字一律用上表的文字 token；`test_theme.py` 擋下 `color: var(--danger)`
- **字不放在 frost3 或 Aurora 原色填色上** ⚠️：snow2 疊在 frost3 只有 3.50:1。主按鈕是 frost1 底配 polar0 字；選中的分頁是 polar2 底 + `--accent` 字 + 4px frost1 底線
- **Aurora 只作語意點綴，不作大面積背景**：狀態用 `.pill` 的字（`*-ink`）與邊框（原色）表現；錯誤訊息 `.err` 是 `--danger-ink` 字＋4px 紅色左邊條
- 不用純白背景、不用純白文字（最亮是 snow2）
- **陰影一律是 Nord 色的實色塊（無模糊、不半透明）**，不用 `rgba(…)` 陰影；dialog 背後的遮罩 `--scrim` 是黑 55%，它調暗頁面而不是陰影，是唯一的黑色半透明
- 同一個畫面最多兩個強調色同時出現（frost 系 + 一個 Aurora 語意色）

### 場景類別色

時間軸色條、圖例與裝置畫面的地板共用同一組 token，三者必須一致：

| 類別 | token | 色票 |
|------|-------|------|
| 家裡 | `--home` | Aurora orange |
| 學校 | `--school` | Aurora green |
| 公司 | `--office` | frost2 |
| 外出 | `--out` | Aurora purple |
| 發呆（idle） | `--idle` | polar3 |

時間軸色條上的字用 `--bg`（深字疊在 Aurora／Frost 的淺色上），共同事件的白框是 `--ink-bright`。

## Brutalism 結構

- **偏移陰影**：`box-shadow: var(--offset) var(--offset) 0 var(--shadow)`（frost3 實色，`--offset` 3px）。一般按鈕的陰影色同邊框（`--shadow-ghost`）、危險按鈕用紅；按下時元素位移 `--offset` 落進自己的陰影、陰影歸零（90ms）
- **偏移會溢出元素外框** ⚠️：放面板的 grid 要留 ≥12px 的 gap，容器右下要留出 `--offset` 的 padding（`.wall`、`.detail`、`/demo` 的 section 都有），否則陰影被相鄰元素或捲動容器截掉
- **2px 裸邊框**：面板、分頁是 2px `--line`；按鈕與 chip 用 `--line-control`；輸入框左側是 4px frost1 accent bar，focus 換成 `--accent`；選中的清單項目加 4px 左側 accent bar
- **直角**：`--radius` 0（Offbeat 的 Web 介面在所有 STRUCTURE 下都是直角，圓角 4px 只屬於行動 App）；只有裝置畫面裡模擬螢幕的窗與徽章保留 2px

## 字型

- 內文與標題：`--font-body`（system-ui、Segoe UI、Roboto 在前，Noto Sans TC 等 CJK 字型在後；標題 900、按鈕 700）
- 時鐘、時間、ID、狀態列、標籤：`--font-mono`（JetBrains Mono 有裝就用，沒裝退到系統等寬），數字一律 `tabular-nums`
- **不載入任何 webfont**：字族先列拉丁字型、後列 CJK，避免拉丁字母掉進 CJK 字型裡難看的比例字；帶字距的標籤（表頭、`h1 small`）字重不低於 700

## 只有深色

Offbeat 是深色設計語言，**頁面固定 `color-scheme: dark`，不再跟隨系統切換淺色**。舊版的淺色／深色兩組變數已移除：
Offbeat 的禁忌清單明確排除白底，而維護兩組顏色正是讓頁面寫死色碼、兩邊漂移的原因。

## 裝置畫面

`/demo` 與監視牆裡的「窗」是在模擬 ESP32 螢幕的內容，不是介面外框，但同樣只用 token：

- 天空依時段（`night`／`dawn`／`day`／`dusk`／`evening`）設在 `.sky` 的 `data-sky`，漸層由 `offbeat.css` 的 `--sky-*` 決定
- 地板是 `.room` 的 `--k`，等於該場景類別的 token（發呆時是 `--idle`）
- 角色身體色是 `--look-<appearance key>`；沒有對應的 key 依序取 `--look-1`～`--look-6`
- 文字疊在半透明 polar0 的 `--screen-cap` 上，用 `--screen-ink`（snow2）

日後 ESP32 韌體要畫同樣的畫面時，從 `offbeat.css` 的 Nord 色票換算成裝置的色彩格式（例如 RGB565），不要另外調一組顏色。
