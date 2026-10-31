讀這一章，需要你在自己的專案裡用過 Copilot 的 agent 模式，並且讀過[什麼是 Harness Engineering？](0-1-the-gap-and-the-map.html)，或者知道「harness」這個詞。

## 一句話 {#in-one-sentence}

先寫一頁規則，加一個 skill，再寫一個擋危險指令的 hook，其他功能等遇到真實的痛點再加。

## 給主管 {#for-leaders}

- **要做的決定**：先搭最小的一組（一頁規則、一個 skill、一個擋危險指令的 hook），之後每加一樣功能，都要說得出它解決的是哪個真實的痛點。
- **風險**：一口氣搭出來的大 harness 維護成本高，也說不清哪一部分起了作用。最小的這一組也不是萬無一失：規則和 skill 只是請求，模型可以不照做；hook 模型繞不過去，但它只擋得住它認得的指令寫法。
- **做對的成本**：如果已經在 VS Code 裡打開了專案，一個人大約半小時能搭完。之後團隊要像審程式碼一樣審規則檔和 hook 檔。
- **可以問團隊**：「我們的設定裡，哪些部分來自真實的失敗，哪些是從範本抄來的？」

## 不要一開始就想完美 {#problem}

讀完上一章的七層架構，很容易讓人想一次搭建全部的功能：任務看板、知識庫、human in the loop（review 和 approve）、子 agent、圍欄（guardrails）、權限管理、沙箱……你其實不需要一口氣吃成大胖子，我個人的經驗是先從一個最小的功能開始迭代，一點一點遇到問題或者痛點，再考慮要不要加功能，而且我也遇過偽需求，比如有些功能一開始加上去，後來發現是錯誤的偽需求，所以之後還刪掉過。

Anthropic 給做 agent 的團隊的建議也是這樣：「先找盡可能簡單的方案，只在需要時才增加複雜度」，而且「只有在它明顯改善了結果時」才值得加。（[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)）

總之，跟著這篇文章，先學會搭一個最小的 demo，然後了解 harness 到底是什麼。這篇文章，我想教你先設計一頁規則 `.md` 檔，再加一個 skill，最後寫一個 hook，感受一下這三層。如果你已經在 VS Code 裡打開了專案，全部搭完大約要半小時。

## 三步搭出最小的一組 {#how-it-works}

::: figure 0-2-grow-by-pain

### 為什麼先規則，再 skill，最後 hook

這三樣約束 agent 的力度一樣比一樣緊，搭起來的成本也一樣比一樣高，所以從最便宜的開始。

常見的規則檔就是 `AGENTS.md`（比如 Codex、Copilot）、`CLAUDE.md`（Claude Code）或者 `.github/copilot-instructions.md`（Copilot），前兩個一般在你的專案倉庫根目錄下建立就好了，第三個放在 `.github/` 資料夾裡。規則只要寫幾分鐘，不用寫程式，就能告訴 agent 它自己猜不到的事：專案怎麼建置、測試怎麼跑、什麼東西不能碰。每次會話開始，agent 都會自動尋找有沒有這個檔案，如果有的話，就會載入到上下文裡。它只是請求，模型可以不理；依我的經驗，寫下來的東西它大多數時候會照做，但是如果上下文過長，有時候模型就會忽略一些規則，所以規則檔不能 100% 保證。

skill 是一個資料夾，Copilot 放在 `.github/skills/` 下面，Claude Code 放在 `.claude/skills/` 下面，Codex 放在 `.agents/skills/` 下面，裡面有一個 `SKILL.md`，開頭寫名字和描述，下面寫某一類工作的具體步驟，比如怎麼發布版本、怎麼新增一張資料表。這些長的操作步驟不適合放進規則檔，因為規則檔每次都要整份載入，步驟一多，每次都要為它付 token（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)），放進 skill 以後，agent 平時只看到每個 skill 的名字和描述，需求對得上了才去讀全文。它的短板是比規則多了一層不確定：除了同樣只是請求，用不用這個 skill 也是 agent 自己判斷的，描述寫得不好，它就想不起來用。

hook 是平台在固定時機呼叫的一個你自己寫的小程式，比如每次執行工具之前，平台會把這次呼叫的內容（用哪個工具、參數是什麼）交給它，由它決定放行還是拒絕。規則和 skill 都是寫給模型看的，模型可以不照做，hook 不一樣，做判斷的是模型外面的程式，它說不，模型繞不過去，所以那幾件絕對不能發生的事要交給它。它放在最後，是因為它是程式碼，要寫、要測、要維護，而且它只看得到這一次呼叫，看不到指令執行起來之後做了什麼（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)），所以只擋得住它認得的寫法，同一個指令換一種寫法就可能漏過去。

### 第 1 步：寫一頁規則（約 10 分鐘）

在專案根目錄建一個 `AGENTS.md`，如果你不確定用哪個檔案，就用它，因為 Copilot 和 Codex 都讀，Claude Code 在沒有 `CLAUDE.md` 的時候也讀。檔案裡只寫模型會搞錯或者會漏掉的東西，也就是你專案自己的指令、限制和陷阱，它本來就懂的不用寫，比如在你用的語言裡怎麼寫迴圈。規則越短越好，第一版寫五到十行就夠了，Claude Code 的文件也建議每個檔案控制在 200 行以內，因為檔案越長，占的上下文越多，模型照做得也越差（[How Claude remembers your project](https://code.claude.com/docs/en/memory)）。

有一行值得早點加上：改完之後要跑的指令（測試、lint），再加一句「通過之前不准說做完了」，這是最便宜的檢查（[讓 agent 能檢查自己的活](5-4-self-checks.html)）。

我設定裡的真實檔案要長一些，核心的兩條限制是這樣的：

::: code harness AGENTS.md L44-L45 "隨附的規則檔裡的兩條核心限制：動手之前先看，保留使用者自己的改動。"

寫完要確認它生效了。開一個新對話，問一個只有你的規則才答得出的問題，比如「這個專案怎麼跑測試？」，它照著規則回答，說明檔案載入了，如果它在猜，就檢查檔名和位置。在 VS Code 裡也可以展開回答下面的 References，或者在命令選擇區裡執行 **Chat: Open Customizations**，看這個檔案在不在清單裡。

### 第 2 步：加一個 skill（約 10 分鐘）

挑一件你跟 agent 解釋過不只一次的工作，在 `.github/skills/` 下面給它建一個資料夾，裡面放一個 `SKILL.md`，開頭寫名字和描述。名字只能用小寫字母、數字和連字號，並且要和資料夾同名，描述最多 1024 個字元。

最要緊的是描述，因為 agent 平時只看得到這一段，能不能在該用的時候想起這個 skill，全看它寫得好不好。VS Code 的建議是把「做什麼」和「什麼時候用」都寫具體，我還會寫上使用者可能會說的詞。

::: code harness .github/skills/generic-code-standards/SKILL.md L1-L6 "真實 skill 的開頭：agent 最先看到的是名字和描述。"

開頭下面寫步驟，步驟後面列一小段陷阱，也就是 agent 通常會出錯的地方。以後每看到它失敗一次就加一條，這是我知道的寫 skill 最有用的習慣（[把團隊的做法寫成 skill](3-4-skills-and-workflows.html)）。

寫完同樣要確認。在對話框裡輸入 `/`，這個 skill 應該出現在清單裡，然後提一個符合描述、但不點名這個 skill 的需求，看 agent 會不會用上它。如果它一直不選這個 skill，問題通常出在描述上。

### 第 3 步：寫一個擋危險指令的 hook（約 10 分鐘）

終端機是 agent 手裡最厲害的工具，所以第一個 hook 就從這裡下手，擋那些損害無法復原的指令，比如遞迴刪除一個資料夾，或者下載一個腳本後一行指令直接執行。

hook 分兩部分，設定檔告訴平台在哪個事件上呼叫哪個程式，程式負責判斷。VS Code 從倉庫的 `.github/hooks/*.json` 讀設定，我的設定裡，每個事件都指向同一個程式：

::: code harness .github/hooks/harness.json L40-L51 "工具執行之前那個時機的設定：它只是寫明了要呼叫哪個程式。"

每次執行工具之前，平台把這次呼叫交給程式，如果指令符合你要擋的某個樣式，程式就回傳拒絕（把 `permissionDecision` 設成 `deny`），並附上原因。原因要寫明應該改做什麼，因為 agent 看得到它，不寫的話 agent 還會再試同樣的事（[詢問不是限制](4-2-ask-vs-refuse.html)）。下面是我的一條樣式，寫得這麼長，是因為同一個指令有很多種寫法，你第一天不需要這麼大的檔案，先寫三、四條樣式就夠了。

::: code harness .harness/policies/gate.json L59-L62 "一條真實的拒絕規則：對根目錄、家目錄或目前資料夾做遞迴強制刪除，並附上 agent 讀得懂的原因。"

測試 hook 不能拿真正危險的指令。先加一條無害的規則，比如拒絕指令 `echo hook-test`，再讓 agent 去跑，你應該會看到一個帶著你寫的原因的拒絕，測完把這條規則刪掉。

hook 有三個坑，我都踩過：

- hook 程式啟動不了（比如找不到直譯器），這次呼叫會被當作拒絕，GitHub 的文件也是這樣寫的：preToolUse 的指令出錯，就拒絕這次工具呼叫。結果是 agent 一個工具都用不了，畫面上卻只顯示 hook 出錯，所以在依賴它之前先測一次。
- hook 逾時（我的設定是 30 秒），平台就當它沒表態，按正常的權限規則處理這次呼叫。如果這個指令平時是自動批准的，它就照常執行，等於沒有 hook，所以程式要快。
- 在我的設定裡，hook 的設定是視窗啟動時讀的，改完要重新載入 VS Code 視窗。

### 你需要多大的 harness？

這三樣夠不夠，取決於 agent 出錯時誰會受影響。

| 你是 | 大概夠用的 | 原因 |
| --- | --- | --- |
| 一個人，做自己的專案 | 上面這三樣 | 每處改動你都看得到，出錯的代價只有你自己扛 |
| 小團隊，共用一個倉庫 | 這三樣，規則檔和 hook 檔像程式碼一樣審，再加一個記錄 agent 做了什麼的地方 | 別人會承接 agent 的錯誤，而「誰改了規則」會成為一個問題（[落地與治理](7-4-rollout-and-governance.html)） |
| 大團隊，或者有合規義務的程式碼 | 以上這些，再按你的風險需要加[批准點](5-3-two-approvals.html)、[可計數的檢查](5-5-counted-checks.html)和報告 | 出錯的代價由別人承擔，而且你得拿得出發生了什麼 |

大多數讀者屬於第一列，兩道批准、任務看板這些都可以以後再說。

### 接下來按痛點加什麼

三樣都搭好以後，不用把這本書從頭讀到尾，哪裡痛了，再去讀對應的那一章。

| 痛點 | 讀 |
| --- | --- |
| agent 一次又一次不理某條規則 | [4.1](4-1-requests-and-rules.html) |
| 一個指令跳了一百次批准，你不看就按「允許」 | [4.2](4-2-ask-vs-refuse.html) |
| 它說「做完了」，測試卻是失敗的 | [5.4](5-4-self-checks.html) |
| 長對話越聊越差，它還會忘事 | [3.2](3-2-long-sessions.html) |
| 帳單比預想的高 | [1.1](1-1-models-and-cost.html) |
| 你想把工作分給多個 agent | [2.3](2-3-subagents.html) |
| 你說不清它做了什麼 | [6.1](6-1-observe.html) |

### 怎麼知道變好了沒有？

每加一樣東西，你都想知道它有沒有用，但是感覺靠不住。辦法是挑幾個你知道正確答案的任務，每次改動前後各跑一遍，用同樣的方式打分（方法見[第 6 部](6-3-eval-tasks.html)）。粗糙的版本也比猜強：五個任務，加一份執行之前就寫好的「什麼算對」的清單，每個任務多跑幾次，因為一次執行的結果可能只是運氣（[一次運行證明不了什麼](6-4-variance.html)）。

## 規則檔會越寫越長，hook 會讓人太放心 {#costs-and-traps}

規則檔最先出問題。每出一次事故就加一行，過一陣子它就很長了，有些條目還互相矛盾，模型也就不再照做了，所以要定期刪減，讓每條規則只出現在一個地方。

hook 的問題更隱蔽，它讓人太放心。因為它只擋它認得的寫法，所以別說「agent 刪不了東西」，要說「agent 跑不了這幾個特定的指令」。

## 什麼時候可以把每一樣刪掉 {#when-to-delete-it}
{status: industry}

這套入門設定裡的每一樣，平台都在慢慢內建。等平台自己的權限系統開箱就能拒絕同樣的危險指令，就刪掉你的 hook；等它自己學會了你專案的指令，就縮短你的規則檔。每次大的模型升級之後，都重讀一遍規則（[模型升級了，就要刪](6-5-model-upgrades.html)），因為為舊模型寫的那些行，可能已經成了累贅。

## 在你自己的環境試試 {#try-it}

::: prompt
用一個最小設定的三部分來檢查這個倉庫：一頁簡短的規則、一個 skill、一個會擋指令的 hook。每一部分都說明有沒有、在哪裡、能不能用。規則的部分，列出太長、過期或互相矛盾的行，並說明缺了哪些模型猜不到的指令和限制。hook 的部分，列出哪些不可逆的指令（例如遞迴刪除）沒有任何東西擋住。不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Anthropic：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- VS Code 文件：[Create and manage agent customizations](https://code.visualstudio.com/docs/copilot/customization/overview)
- VS Code 文件：[Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)、[Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- VS Code 文件：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Claude Code 文件：[How Claude remembers your project](https://code.claude.com/docs/en/memory)

## 在 harness 裡探索 {#explore}

我自己的設定，就是這一章的成熟版：一頁規則、很多 skill，還有一個守著每次工具呼叫的 hook。harness 可以從裡面帶你逐個看，也能幫你設定自己的。

::: prompt
/harness-rookie-wondering 我讀完了「30 分鐘搭一個最小 harness」這一章。請教我這個 harness 怎麼做它的規則頁、skill 和 hook。每一項都帶我打開真實的檔案，讓我看 hook 怎麼拒絕一個指令，並幫我看出哪些可以抄進自己的專案。
:::
