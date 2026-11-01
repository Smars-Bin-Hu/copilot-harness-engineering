讀這一章，只需要知道寫程式的 AI agent 能讀檔案、跑指令。

## 一句話 {#in-one-sentence}

模型只負責提出工具呼叫，真正執行工具的是它外面的程式，而模型要用工具，能依靠的只有工具的名字、描述和錯誤訊息，所以這些文字寫得好不好，決定了工具能不能被用好。

## 給主管 {#for-leaders}

- **要做的決定**：把給 agent 的工具當成產品來做，描述和錯誤訊息都要有人負責；另外也要決定，哪些固定的步驟做成指令，不寫進 prompt。
- **風險**：模型只能靠工具的名字和描述去猜，含糊的工具會被用錯，或者根本沒人用。寫在 prompt 裡的規則只是請求，而由指令完成的步驟，只要走這條路徑，就跳不過去。
- **做對的成本**：重寫描述和錯誤訊息花不了多少功夫。指令是程式碼，要有人維護和測試。
- **可以問團隊**：「如果只看每個工具的名字和描述，你知道什麼時候該用它嗎？它的錯誤訊息又是怎麼寫的？」

## 模型自己碰不到你的檔案 {#problem}

看 agent 改檔案，你會以為是模型改的，其實模型只是一個讀文字、寫文字的程式，自己打不開檔案，也跑不了指令。它能做的，是寫出一段結構化的請求，意思是「呼叫工具 `read_file`，路徑是 `src/app.py`」，這就是一次**工具呼叫**（tool call）。模型外面的程式（[什麼是 Harness Engineering？](0-1-the-gap-and-the-map.html)裡第一種意思的 harness）讀到這個請求，才真的去讀檔案，再把內容當成**工具結果**放回對話，模型讀完再決定下一步。讀檔案、搜尋、改檔案、執行指令、抓取網頁，這些 agent 能要求做的動作都叫**工具**。

這件事有兩個後果。第一，agent 的每個動作都要經過一次呼叫，而呼叫是在模型外面執行的，所以程式可以檢查、拒絕或者修改它，你能對 agent 強制執行規則，靠的就是這一點。第二，模型用工具的時候，手上只有工具的名字、描述和參數清單，它不是看過文件、能問同事的程式設計師，而是一個靠這幾行字來猜的使用者，所以這幾行字寫得好不好，直接決定工具能不能被用好。

### 一次來回

::: figure 1-2-tool-call

拿 Anthropic 的 API 來說，模型要用工具時，回覆的 `stop_reason` 是 `tool_use`，裡面帶著寫明工具名和參數的 `tool_use` 區塊，你的程式碼執行這個工具，再用 `tool_result` 區塊把結果送回去（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。這種在你這邊執行的叫用戶端工具，編輯器裡的 agent 做的事，大部分都是這樣在你的機器上執行的。另外還有一類**伺服器端工具**，例如 Anthropic 的 `web_search`，它在供應商那邊執行，結果直接回傳，中間沒有你的程式碼，所以你沒辦法在它執行之前或之後插手。

## 能在哪裡插手，工具又該怎麼寫 {#how-it-works}

### 你能在哪裡插手

只要是用戶端工具，程式就夾在請求和動作之間，所以有兩個地方可以插手。工具執行之前，程式可以放行、拒絕或者修改這次呼叫，常用的辦法是 hook，拒絕時給的原因會送回給 agent（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)）。工具執行之後，程式可以在模型讀到結果之前，先把結果精簡、過濾或者補充一下。放在這裡的規則是會執行的程式碼，而寫在 prompt 裡的規則只是請求（[提示裡的規則只是請求](4-1-requests-and-rules.html)）。但是 hook 只能判斷模型已經發出的呼叫，模型能不能把呼叫發對，要看它呼叫之前看到了什麼、呼叫之後拿回了什麼，這兩樣都是你寫的文字。

### 模型只能靠你寫的文字來用工具

人用命令列，可以看文件、問同事，還能察覺哪裡不對勁。模型手上只有工具的名字、一段描述和參數清單，它靠這些決定什麼時候用，靠上下文去猜參數，工具沒告訴它的事它一概不知道，回傳的結果它也都當普通文字讀，結果有多大，就占掉多少上下文視窗。所以它會猜錯，Anthropic 的文件舉的例子是，`get_weather` 需要地點，你問「天氣怎麼樣？」卻沒說在哪，Opus 比較可能回頭問你，Sonnet 可能自己填一個 New York（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

反過來說，改這幾行字的回報很高。Anthropic 說「就算只是對工具描述做很小的改進，也能帶來顯著的提升」，Claude Sonnet 3.5 在 SWE-bench Verified 評測上拿到當時最好的成績，就是在精確地修改工具描述之後（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。下面五條規則，按一次呼叫經過的順序排。

### 1. 描述要寫得像給新進同事的交接說明

呼叫之前，描述是模型了解工具用途的唯一地方，所以要寫清楚這個工具做什麼、什麼時候用、什麼時候不用，寫得含糊，工具就會被用錯，或者沒人用。參數的名字也一樣，Anthropic 的例子是別叫 `user`，要叫 `user_id`，因為 `user` 可能是名字，也可能是電子郵件或者 ID。如果兩個工具看起來很像，每個工具的描述裡都要說清楚它和另一個有什麼不同。

### 2. 錯誤訊息要寫給 agent 看

呼叫出了錯，模型接下來讀到的就是錯誤訊息。人看到堆疊追蹤會停下來想一想，模型則是拿到文字就接著往下走，如果錯誤訊息只有 `Error 400`，它就只能猜，而且往往又猜回同一個錯的值，如果訊息說明了哪裡不對、接下來該試什麼，它就能把呼叫改對。拒絕也一樣，要說明應該改做什麼（[詢問不是限制](4-2-ask-vs-refuse.html)）。

### 3. 輸出要短，還要能分頁

呼叫成功了，模型讀到的是輸出。工具回傳的所有東西都會放進上下文視窗（[上下文是一份預算](3-1-context-budget.html)），而且之後每一輪都要再讀一遍（[選模型，別只看 token 單價](1-1-models-and-cost.html)），所以如果 agent 只想要一行，工具卻把一個大檔案整個回傳，不但浪費 token，還可能把有用的東西擠出視窗。辦法是給結果設限制，例如預設的上限、分頁、範圍選擇或者過濾器。Claude Code 預設把工具的回應限制在 25,000 個 token 以內，不管上限定在哪裡，截斷的時候都要說一聲，並且告訴 agent 怎麼縮小查詢範圍。Anthropic 還有一個做法，是加一個 `response_format` 參數，讓 agent 自己選簡潔或詳細，他們的例子裡詳細回應是 206 個 token，簡潔回應是 72 個，只有三分之一（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

### 4. 工具少，選得更準

多一個工具不是沒有壞處。工具只要載入了，它的名字、描述和參數每次呼叫都要送給模型，工具越多，花的 token 越多，選錯的機會也越多，功能重疊的時候尤其如此。Claude Code 和 VS Code（Claude Sonnet 4.5、Opus 4.5 以上）預設用工具搜尋，一部分工具先不載入，用到時才搜出來，這能省下定義占的 token，但是模型還是要靠名字和描述才搜得到它（[接 MCP server 之前，要想清楚什麼？](1-3-mcp.html)）。VS Code 還有一個硬上限，一次請求最多啟用 128 個工具，用不上的可以在工具選擇器裡關掉（[Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)）。所以優先用一小組明顯不同的工具，能合併的就合併，Anthropic 的例子是做一個 `search_contacts` 而不是 `list_contacts`，做一個 `schedule_event` 把查空檔和建立行程合在一起。工具很多的時候，把相關的工具歸到同一個名字前綴下也能幫 agent 分清楚，不過前綴和後綴哪種好，Anthropic 說不同模型效果不一樣，要用自己的評測來決定（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

### 5. 固定的步驟做成指令，不寫進 prompt

這是五條裡我最想強調的一條。有些工作的步驟每次都一樣，而且有對錯之分，例如替新任務建資料夾、複製檔案、算一個雜湊值、寫入紀錄、寫回之前檢查一切就緒。你可以把這些步驟寫進指令檔讓 agent 照著做，它大多數時候也會照做，但是也可以一次寫成一個**指令**（command），也就是 agent 當作工具來執行的一個小程式，由指令自己完成這些步驟、檢查前置條件，最後回傳一個簡短的結果。走指令這條路徑時，agent 跳不過任何一步，也寫不出錯誤的狀態，因為狀態根本不是它寫的。

::: figure 1-2-prompt-vs-command

這適合不需要判斷的步驟，如果某一步需要 agent 拿主意，就把那部分留給它，指令只做周圍那些固定的事。我的 harness 就是這麼做的，一個命令列工具負責建任務資料夾（[管任務，不管對話](5-1-tasks.html)）、取檔案、算 diff、統計檢查，模型只要執行指令、讀結果。進度是最好的例子，任務清單讀的是指令寫入的資料檔，不是 agent 手寫的 Markdown 筆記，因為手寫的進度會漏打勾，也會寫錯。

指令的輸出最好能說明下一步做什麼，這樣 agent 就不用猜了。同一個指令既有人在終端機裡看，也有腳本透過管線讀，所以可以在終端機裡印出對齊的文字，接到管線上時印出 JSON，兩種輸出的欄位一樣。

指令的弱點是 agent 真的去用它才有用，而且它只守得住經過它的東西，如果 agent 能用別的辦法做同樣的事，例如手動改檔案，指令就只是圖個方便，算不上限制（[提示裡的規則只是請求](4-1-requests-and-rules.html)）。

### 怎麼檢查你自己的工具

對你給 agent 的任何一個工具，先問三個問題。只看名字和描述，你知道什麼時候該用、什麼時候不該用嗎？它失敗的時候，訊息有沒有告訴 agent 接下來做什麼？它的輸出最大能有多大，如果很大，上下文會怎麼樣？

最快的實驗什麼都不用裝：讓 agent 用一種你明知不對的方式呼叫你的某個工具，看看回傳了什麼，假如你就是那個 agent，這條訊息能不能讓你知道該怎麼辦，如果不能，要重寫的就是這條訊息。

如果你自己做工具，Anthropic 的方法是同一個想法的放大版：根據真實的使用情境寫出任務，執行它們，讀原始紀錄（呼叫和結果，不只是最後的答案），然後在 agent 出錯的地方改描述和錯誤訊息。他們還把這些紀錄貼給 Claude Code，讓它來改工具，文章裡大部分的建議就是這麼來的（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

## 好工具也有代價，模型選的參數也不能全信 {#costs-and-traps}

描述寫得再好也要花 token，因為工具只要載入了，描述每次呼叫都要送一遍，所以只寫模型選擇和使用這個工具需要的內容，長的說明放進檔案，讓 agent 需要時再讀。指令的代價不一樣，它是要維護的程式碼，專案一變就可能出錯，而且是 prompt 不會有的那種錯，所以每個指令都要保持小，並且寫測試。

工具呼叫也不能當成使用者的意願，因為參數是模型選的，而它選之前讀到的文字可能來自任何地方（[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html)）。Anthropic 的 API 上加 `strict: true` 能保證呼叫符合工具的 schema，但這只保證格式，值還是模型選的（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

還有一個很實際的陷阱，工具名在不同版本之間會變，如果你的規則或 hook 按工具名來比對，就把這份對應關係放在同一個地方，改名時只改一處。

## 模型供應商也把工具的文字當介面 {#industry}
{status: industry}

Anthropic 的兩份資料說的是同一件事：工具是一個介面，它的文字也是介面的一部分。講怎麼寫工具的那篇把工具設計當成工作的一部分，認為描述和錯誤訊息值得像程式碼一樣測試（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。工具使用文件說用戶端工具由你的應用程式執行，再把結果送回去，還提醒模型「可能會猜出你沒提供的值」（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

## 什麼時候可以刪掉指令 {#when-to-delete-it}
{status: industry}

最可能過時的是指令，因為檢查前置條件的指令是圍著模型的弱點搭起來的鷹架，如果模型在遵循多步驟的說明上變得夠可靠，指令也許就不再比一個好的 prompt 強。即使到了那一天，那些每次都必須完全一樣、或者需要留下紀錄的事，我還是會用指令。描述和錯誤訊息的道理不一樣，只要模型還在讀文字，它就一直成立。

## 在你自己的環境試試 {#try-it}

::: prompt
找出這個倉庫裡每一個預期由 agent 執行的工具、指令或腳本（看 agent 檔、腳本、任務執行器和指令檔）。每一個從四方面判斷：名字和描述是否說清楚什麼時候該用、什麼時候不該用；錯誤訊息有沒有說明接下來做什麼；輸出最大能有多大；指令檔裡描述的某個固定的多步驟流程，是否應該改成指令。列出最差的三個，並說明各自怎麼修。不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Anthropic：[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Anthropic 文件：[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- VS Code 文件：[Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)

## 在 harness 裡探索 {#explore}

我的 harness 給了 agent 一個命令列工具，用來做那些必須確定的步驟，還有一個守在每次工具呼叫前面的 hook。harness 可以和你一起打開真實的檔案，從裡面帶你看這兩樣。

::: prompt
/harness-rookie-wondering 我讀完了「Agent 用不好工具，先看工具的描述和錯誤訊息」這一章。請教我這個 harness 給了 agent 哪些工具：內建的，和它自己的命令列工具。帶我打開真實的檔案，讓我看一次拒絕和它的原因，並畫出一次工具呼叫是怎麼走的。
:::
