讀這一章，請先讀過[慎用子 agent](2-3-subagents.html)，或至少知道子 agent 是什麼。

## 一句話 {#in-one-sentence}

只有在必須換模型、或縮小工具時，才建立 custom agent。如果要改的只是它知道什麼、怎麼做事，用 skill 或指令檔就夠了。

## 給主管 {#for-leaders}

- **要做的決定**：只有 custom agent 改變了別的方式共用不了的東西時才批准：它的工具、它的模型，或一個用來做獨立檢查的獨立上下文。
- **風險**：一個角色 agent 如果只改了語氣和做事的訣竅，就只是多一個要同步維護的檔案，裡面卻沒有任何一樣是平台強制執行的。角色各自作為獨立的 agent 執行時，用量也會增加，Anthropic 就量過，他們的多 agent 研究系統用的 token 約是聊天的 15 倍。
- **做對的成本**：每一種真正的限制對應一個 agent 檔，像任何規則一樣走 code review 來改。我的設定只留了一個唯讀的幫手和一個檢查者。
- **可以問團隊**：「這個 agent 檔有列出工具或模型嗎？沒有的話，為什麼不是 skill？」

## 想要另一個 agent 時，到底要做出什麼？ {#problem}

[慎用子 agent](2-3-subagents.html)問的是要不要把工作分給多個 agent。真的想要另一個 agent 時，很多設定接下來的做法是做角色：「SQL 專家」「程式碼 reviewer」「文件作者」，每個都是一個 agent 檔，感覺像在整理。可這到底算不算整理，得先弄清楚這種檔案是什麼。**custom agent** 是一個為 agent 定義角色的檔案，在 VS Code Copilot 裡就是副檔名為 `.agent.md` 的檔案：上面一段簡短的檔頭（名稱、描述、設定），下面一段指令正文。和它相對的是**預設 agent**，也就是你什麼都不選時對話的那個普通 agent。

可是再看一看這種檔案裡有什麼，你會發現大部分內容，用別的方式也能交給預設 agent。換句話說，一個角色如果只是換了語氣、加了些做事的訣竅，就是一件戲服：它多了一個要維護的東西，裡面卻沒有任何一樣是平台強制執行的。那麼，除了戲服，檔案裡還有什麼？

## agent 檔裡，哪些東西不只是戲服？ {#how-it-works}

### agent 檔裡有什麼

這個答案要從檔頭找起，因為設定都放在那裡。照 VS Code 文件和我自己的檔案來看，重要的只有幾個。

名稱和描述是寫給呼叫者看的。描述告訴模型什麼時候該呼叫這個 agent，所以裡面要說明這個 agent 是做什麼的、需要被告知什麼。子 agent 從空的上下文開始（[慎用子 agent](2-3-subagents.html)），呼叫訊息一含糊，它就無從下手。

其餘的設定，決定這個 agent 用什麼做事、誰可以呼叫它。檔頭如果給了一份工具清單，這個 agent 就只能用清單裡的工具。模型是可選的，也可以是一個依偏好排序的清單，第一個用不了，就試下一個。誰可以呼叫它，由兩個設定來管，作用各不相同。`user-invocable: false` 讓這個 agent 不出現在下拉清單裡（VS Code 文件稱之為 picker visibility）；另一個設定 `disable-model-invocation`，管的是模型能不能把它當子 agent 呼叫。它們各有擋不住的呼叫，見後面的「隱藏不等於禁止」。

檔頭下面的正文就是文字，寫的是這個角色做什麼、怎麼做、不能做什麼、交回什麼。

### 只有 agent 檔能做的事

::: figure 2-4-what-differs

把這些設定放在一起，一項一項地問：這樣東西，預設 agent 能不能用別的方式拿到？

知道什麼、怎麼做事，這些預設 agent 都拿得到。指令檔和 skill 對任何 agent 都有效，所以 SQL 風格指南、review 清單、這裡的命名習慣，都可以放進 skill 或指令檔（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)）。這樣預設 agent 就能做這份工作，不用新的 agent。

工具就不同了，它沒有別的方式可以給。一個 agent 有的就是它的檔案列出的工具，平台會強制執行這份清單，所以沒有編輯工具的 agent，怎麼要求都改不了檔案。而寫在檔案正文裡的規則，例如「不要編輯檔案」，就沒有這樣的效力。它和別的規則一樣，只是請求。

同樣，模型也只能在 agent 檔裡定，不管是讓簡單的工作用便宜的模型，還是讓難的思考用強的。使用者可以在下拉清單裡為預設 agent 切換模型，但子 agent 的模型是在它的檔案裡設定的。

工具和模型都寫在檔案裡。獨立的上下文不一樣，它根本不寫在檔案裡。作為子 agent 執行時，它從空的上下文開始，只有它的報告會交回來，這來自「作為子 agent 執行」這件事，而不是檔案裡寫了什麼。想要獨立檢查時，這就是做一個的理由，[慎用子 agent](2-3-subagents.html)講的就是這種情況。

所以我用的規則很短。**至少有一樣共用不了時，才建立 custom agent：工具不同、模型不同，或需要一個不能看到呼叫者思路的上下文**。其他情況，用預設 agent，把做事的訣竅寫下來。

有一個快速的判斷，能讓這條規則更好用。如果你能把它說成「做 X 的時候，這樣做」，它就是 skill；如果你能說成「這份工作不能有工具 Y」或「這份工作要用模型 Z」，它就是 agent。真要加一個之前，我還是會問兩個問題：它防的是哪種失敗？預設 agent 為什麼做不到同樣的事？

VS Code 的上下文工程指南也是這樣劃線的。它建議，「按多輪流程、用特定工具來走的 workflow」可以用 agent，它的範例規劃 agent 正好符合這一點：那份簡短的唯讀工具清單是限制，那句不要動手實作的指令是請求。

### 一個例子：reviewer

在我的設定裡，有一個 custom agent 是我最想留下的，那就是 reviewer。它是一個只看需求和結果的檢查者，下面是它檔案的開頭：

::: code harness .github/agents/reviewer.agent.md L1-L8 "reviewer 的檔頭：tools 那一行是限制，model 那一行是備用清單，描述是對呼叫它的模型的請求。"

`tools` 那一行給了它讀取、搜尋和執行指令的工具，卻沒有改檔案的工具，所以它不能「順手修掉」。`agents: []` 表示它不能再開別的子 agent，模型則是一份備用清單。（每個選擇的理由在[慎用子 agent](2-3-subagents.html)。）這裡要看的是，檔頭裡每一行會改變行為的，不是工具限制，就是模型，或是上下文的邊界。相較之下，描述只是請求，正文則大多在說看什麼、交回什麼。

不過，我碰到的事並不都這麼乾淨俐落。

### 三件讓我吃過虧的事

第一件是，「隱藏」不等於「禁止」。讓 agent 不出現在下拉清單的設定，擋不住另一個 agent 把它當子 agent 呼叫；不讓模型使用它的那個設定，也一樣擋不住。「誰可以呼叫誰」如果重要，就要由 hook 來決定（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)），不能靠這兩個設定。

可是 hook 自己也有盲點：它看不到目前是哪個 agent。hook 收到的事件裡沒有主 agent 的名字（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)），所以權限不能交給「admin agent」：任何 agent 都能冒充它。權限只能跟著會話走，例如在我的設定裡，admin 開關是由使用者在終端機裡打開的（[保護規則本身的檔案](4-3-guardrails.html)）。我曾經有過一個 admin agent，後來撤掉了。

最後一件是，檢查可能被悄悄跳過：子 agent 的模型比主模型高一個等級時，平台不執行它，也不說一聲。這種情況我只見過一次，可是正因為它不說一聲，「檢查到底有沒有做」，要由不是模型的東西來確認，例如一個把 reviewer 的回答存到磁碟的 hook。

### 測一測你自己的設定

現在回到那條規則，拿它來測一測你自己的角色 agent。挑一個你有的，例如「SQL 專家」或「文件作者」，看它的檔案有沒有列出工具或模型。都沒有的話，把它的正文搬進 skill（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)），再把同一個任務交給預設 agent，分別在有 skill 和沒有 skill 時做，然後比較。看不出差別，這個 agent 就是戲服；不過每種都多跑幾次，再相信你看到的。

## 多留一個 agent 要付出什麼 {#costs-and-traps}

最直接的代價是維護。每個檔案都有模型名稱、工具清單和一段會過期的正文。就拿模型名稱來說，它會變，而名稱一旦和下拉清單對不上，這個 agent 就壞了。agent 檔設定的是限制，所以在團隊裡，也要像任何規則一樣走 code review 來改。

還有，切換 agent 可能會丟掉對話。VS Code 文件說，選定的 agent 會一直用在你的請求上，直到你切換為止；至於單純切換一次之後對話紀錄會怎樣，文件沒說，所以要緊的東西，存進檔案（[長對話會變差](3-2-long-sessions.html)）。

最後是用量。算下來，你需要的角色其實比你想的少。每個作為獨立 agent 執行的角色，都要自己讀、自己寫，這些加起來有多少，Anthropic 在他們的研究系統裡量過：agent 用的 token 約是聊天的 4 倍，多 agent 系統約是 15 倍（[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)）。在我早期的設定裡，有三個按職位分工的 agent，一個協調、一個實作、一個檢查，最後只留了檢查者，原因見[慎用子 agent](2-3-subagents.html)。

## 什麼時候可以刪掉 agent 檔 {#when-to-delete-it}
{status: industry}

只要 agent 檔還強制執行著 skill 做不到的東西，也就是工具清單或模型，它就值得留著。有些平台已經讓 skill 帶工具設定。在 Claude Code 裡，skill 的 `allowed-tools` 只是預先批准工具，並不限制工具；移除工具靠的是另一個設定 `disallowed-tools`，它會在 skill 啟用期間把工具拿掉（[Skills](https://code.claude.com/docs/en/skills)）。這樣的設定在你的平台上有沒有強制執行，要自己去查，有的話，很多 agent 檔就不需要了。至於內容只有「表現得像 X 的專家」的 agent，今天就可以刪掉。

## 在你自己的環境試試 {#try-it}

::: prompt
找出這個專案裡所有的 custom agent 檔。每一個回報：檔頭有沒有限制工具、設定模型，還是兩者都沒有；描述的寫法，是否讓呼叫者知道什麼時候用它、要說什麼；正文的哪幾行只是請求。沒有工具限制、也沒有模型設定的 agent，標成可能是戲服，並說明哪個 skill 或指令檔可以取代它。不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- VS Code 文件：[Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code 文件：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic：[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [指令與 skill：只載入需要的](3-3-instructions-and-skills.html)：改變 agent 行為的另一種方式

## 在 harness 裡探索 {#explore}

harness 裡的 custom agent 是刻意只留了很少的一組：一個唯讀的幫手和一個檢查者。你可以打開這兩個檔案，把每一行和上面的表對照。

::: prompt
/harness-rookie-wondering 我讀完了「Custom agent：固定模型和工具的角色」這一章。請教我這個 harness 的 agent 檔裡有什麼：工具清單、模型清單，哪幾行會改變行為、哪幾行只是請求。每一項都帶我打開真實的檔案，並告訴我為什麼 agent 這麼少。
:::
