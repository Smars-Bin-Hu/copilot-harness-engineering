讀這一章，請先讀過[慎用子 agent](2-3-subagents.html)，或至少知道子 agent 是什麼。

## 一句話 {#in-one-sentence}

只有在必須換模型、或縮小工具時，才做 custom agent。要改它知道什麼、怎麼做事，用 skill 或指令檔就夠了。

## 給主管 {#for-leaders}

- **要做的決定**：只有 custom agent 改變了別的方式共用不了的東西時才批准：它的工具、它的模型，或一個不能看到呼叫者思路的上下文。
- **風險**：一個角色如果只是換了語氣、加了些做事的訣竅，它就只是一件戲服：多一個要同步維護的檔案，平台並不會強制執行它。在我早期的設定裡，三個按職位分工的 agent，在四個小任務上（每個只跑一次）用量約是一個 agent 的 4.5 倍，結果沒有更好。
- **做對的成本**：每一種真正的限制一個 agent 檔，像任何規則一樣走 code review 來改。我的只留了一個唯讀的幫手和一個檢查者。
- **可以問團隊**：「這個 agent 檔有列出工具或模型嗎？沒有的話，為什麼不是 skill？」

## 問題 {#problem}

[慎用子 agent](2-3-subagents.html)問的是要不要把工作分給多個 agent。這一章問一個小一點的問題：你想要另一個 agent 時，到底要做出什麼？

很多設定一開始就做角色：「SQL 專家」「程式碼 reviewer」「文件作者」，每個都是一個 agent 檔。這感覺像在整理。但看一看 agent 檔裡有什麼，你會發現大部分內容，用別的方式也能給預設 agent。一個角色如果只是換了語氣、加了些做事的訣竅，它就是一件戲服。它多了一個要維護的東西，卻沒有任何平台強制執行的東西。

先說兩個詞。

- **custom agent** 是一個檔案，為 agent 定義一個角色。在 VS Code Copilot 裡，它是副檔名為 `.agent.md` 的檔案。它有一段簡短的檔頭（名稱、描述、設定）和一段指令正文。
- **預設 agent** 是你什麼都不選時對話的那個普通 agent。

## 原理 {#how-it-works}

### agent 檔裡有什麼

檔頭放幾個設定。以下是重要的幾個，來自 VS Code 文件和我自己的檔案：

- **名稱和描述**。描述告訴模型什麼時候該呼叫這個 agent。要為呼叫者寫：說明這個 agent 是做什麼的、需要被告知什麼。子 agent 從空的上下文開始（[慎用子 agent](2-3-subagents.html)），所以含糊的呼叫訊息讓它無從下手。
- **工具清單**。檔案裡給了清單，這個 agent 就只能用清單裡的工具。
- **模型**，可選。可以是一個依偏好排序的清單：第一個用不了，就試下一個。
- **誰可以呼叫它**。有兩個設定，作用不同。`user-invocable: false` 讓這個 agent 不出現在下拉清單裡（VS Code 文件稱之為 picker visibility）。另一個設定 `disable-model-invocation` 管的是模型能不能把它當子 agent 呼叫。見下面的「隱藏不等於禁止」。

正文是文字：這個角色做什麼、怎麼做、不能做什麼、交回什麼。

### 只有 agent 檔能做的事

::: figure 2-4-what-differs

把這些設定放在一起，問一句：哪些我可以用別的方式交給預設 agent？

- **怎麼做事、知道什麼**。指令檔和 skill 對任何 agent 都有效。SQL 風格指南、review 清單、這裡的命名習慣：放進 skill 或指令檔（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)）。這樣預設 agent 就能做這份工作，不用新的 agent。
- **有哪些工具**。這沒有別的方式可以給。一個 agent 有它的檔案列出的工具，平台會強制執行這份清單。沒有編輯工具的 agent，怎麼要求都改不了檔案。這是 agent 檔能給你的硬限制。（寫在檔案正文裡的規則，「不要編輯檔案」，和別的規則一樣只是請求。）
- **用哪個模型**。這也只有 agent 檔能做。簡單的工作用便宜的模型，難的思考用強的。使用者可以在下拉清單裡為預設 agent 切換模型，但子 agent 的模型是在它的檔案裡設定的。
- **獨立的上下文**。作為子 agent 執行時，它從空的上下文開始，只有它的報告會交回來。這不是檔案的性質，而是子 agent 的性質。想要獨立檢查時，這就是做一個的理由，[慎用子 agent](2-3-subagents.html)講過。

所以我用的規則很短。**至少有一樣共用不了時，才做 custom agent：工具不同、模型不同，或需要一個不能看到呼叫者思路的上下文**。其他情況，用預設 agent，把做事的訣竅寫下來。一個快速的判斷：如果你能把它說成「做 X 的時候，這樣做」，它就是 skill。如果你能說成「這份工作不能有工具 Y」或「這份工作要用模型 Z」，它就是 agent。

加一個之前，我問兩個問題：它防的是哪種失敗？預設 agent 為什麼做不到同樣的事？

VS Code 的上下文工程指南建議，「按多輪流程、用特定工具來走的 workflow」可以用 agent，它的範例規劃 agent 有一份簡短的唯讀工具清單，和一句不要動手實作的指令。形狀是一樣的：工具清單是限制，指令是請求。

### 一個例子：reviewer

在我的設定裡，有一個 custom agent 我最想留：reviewer。它是一個只看需求和結果的檢查者。下面是它檔案的開頭：

::: code harness .github/agents/reviewer.agent.md L1-L8 "reviewer 的檔頭：tools 那一行是限制，model 那一行是備用清單，描述是對呼叫它的模型的請求。"

`tools` 那一行給了它讀取、搜尋和執行指令的工具，沒有改檔案的工具。所以它不能「順手修掉」。`agents: []` 表示它不能再開別的子 agent。模型是一份備用清單，第一個用不了，就用下一個。每個選擇的理由在[慎用子 agent](2-3-subagents.html)。這裡要看的是：檔頭裡每一行會改變行為的，不是工具限制，就是模型，或是上下文的邊界。描述只是請求。正文大多是在說看什麼、交回什麼。

### 三件讓我吃過虧的事

**「隱藏」不等於「禁止**」。讓 agent 不出現在下拉清單的設定，擋不住另一個 agent 把它當子 agent 呼叫。不讓模型使用它的那個設定也一樣。「誰可以呼叫誰」如果重要，要由 hook 來決定（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)），不是這兩個設定。

**hook 看不到目前是哪個 agent**。hook 收到的事件裡，沒有主 agent 的名字（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)），所以不能把權限交給「admin agent」：任何 agent 都能冒充它。權限只能跟著會話走，就像我的設定：admin 開關由使用者在終端機裡打開（[保護規則本身的檔案](4-3-guardrails.html)）。我曾經有過一個 admin agent，後來撤掉了。

**比呼叫者高一級的模型，可能被悄悄跳過**。我見過一次，沒有再測：子 agent 的模型比主模型高一個等級時，平台不執行它，也不說一聲。所以「檢查到底有沒有做」，要由不是模型的東西來確認，例如一個把 reviewer 的回答存到磁碟的 hook。檢查如果對你重要，就留一份它執行過的紀錄。

### 測一測你自己的設定

拿一個你有的角色 agent（「SQL 專家」「文件作者」）。它的檔案有列出工具或模型嗎？都沒有的話，把它的正文搬進 skill（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)），同一個任務給預設 agent，分別在有 skill 和沒有 skill 時做，然後比較。看不出差別，這個 agent 就是戲服。每種多跑幾次，再相信你看到的。

## 代價和陷阱 {#costs-and-traps}

**agent 越多，要同步維護的越多**。每個檔案都有模型名稱、工具清單和一段會過期的正文。模型名稱會變。名稱和下拉清單對不上，這個 agent 就壞了。agent 檔設定的是限制，所以在團隊裡，要像任何規則一樣走 code review 來改。

**切換可能會丟掉對話**。VS Code 文件說，選定的 agent 會一直用在你的請求上，直到你切換。切換時對話紀錄會怎樣，文件沒說，我也沒測過。要緊的東西存進檔案（[長對話會變差](3-2-long-sessions.html)）。

**角色可能感覺像限制，其實只是請求**。正文寫著「不要做 X」，agent 還是做了 X。只有工具清單是限制。

**角色比你想的要少**。在我早期的設定裡，有三個按職位分工的 agent（一個協調、一個實作、一個檢查）。在四個小任務上，它們的用量約是一個 agent 的 4.5 倍，結果沒有更好（[慎用子 agent](2-3-subagents.html)）。我只留了檢查者。這是四個任務、各跑一次：證據很弱，不是結論。Anthropic 在不同的規模上報告了同樣的方向：在他們的研究系統裡，agent 用的 token 約是聊天的 4 倍，多 agent 系統約是 15 倍（[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)）。我的數字和他們的量的是不同的東西，所以只比較方向。

## 什麼時候可以刪掉 {#when-to-delete-it}
{status: industry}

只要 agent 檔強制執行了 skill 做不到的東西：工具清單或模型，它就該留著。有些平台已經讓 skill 帶工具設定。在 Claude Code 裡，skill 的 `allowed-tools` 只是預先批准工具，並不限制工具；另有一個 `disallowed-tools`，在 skill 啟用期間移除工具（[Skills](https://code.claude.com/docs/en/skills)）。這樣的設定在你的平台上有沒有強制執行，要自己去查。有的話，很多 agent 檔就不需要了。而任何內容只有「表現得像 X 的專家」的 agent，今天就可以刪掉。

## 在你自己的環境試試 {#try-it}

不用裝 harness。在你自己的倉庫裡打開 agent，貼上：

::: prompt
找出這個專案裡所有的 custom agent 檔。每一個回報：檔頭有沒有限制工具、設定模型，還是兩者都沒有；描述的寫法，是否讓呼叫者知道什麼時候用它、要說什麼；正文的哪幾行只是請求。沒有工具限制、也沒有模型設定的 agent，標成可能是戲服，並說明哪個 skill 或指令檔可以取代它。不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- VS Code 文件：[Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code 文件：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic：[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [指令與 skill：只載入需要的](3-3-instructions-and-skills.html)：改變 agent 行為的另一種方式

## 在 harness 裡探索 {#explore}

harness 裡刻意只放了很少的 custom agent：一個唯讀的幫手和一個檢查者。你可以打開這兩個檔案，把每一行和上面的表對照。照上面的說明準備好之後，輸入：

::: prompt
/harness-rookie-wondering 我讀完了「Custom agent：固定模型和工具的角色」這一章。請教我這個 harness 的 agent 檔裡有什麼：工具清單、模型清單，哪幾行會改變行為、哪幾行只是請求。每一項都帶我打開真實的檔案，並告訴我為什麼 agent 這麼少。
:::

它一次教一小塊，停下來確認你跟得上，然後和你一起打開檔案。
