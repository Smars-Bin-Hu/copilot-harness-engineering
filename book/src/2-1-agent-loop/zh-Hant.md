讀這一章，只需要你用過寫程式的 AI agent，例如 Copilot 的 agent 模式。

## 一句話 {#in-one-sentence}

agent 就是一個迴圈：模型決定要做什麼，外面的程式替它去做，結果再回到模型面前，讓它決定下一步。這個迴圈上有四個地方可以改，agent 出錯時，先找出該改哪一處，再考慮換模型或加 prompt。

## 給主管 {#for-leaders}

- **要做的決定**：agent 出了問題，先問該改四個地方裡的哪一個（它讀什麼、有哪些工具、呼叫之前的檢查、呼叫之後的檢查），再考慮換更貴的模型或寫更長的 prompt。
- **風險**：迴圈本身很少出問題，出問題的通常是它周圍的這四樣。寫在 prompt 裡的規則只是請求，模型不一定照做，而迴圈什麼時候停，看的是模型還要不要工具，不是事情有沒有真的做完，所以 agent 說「做完了」，不能直接當真。
- **做對的成本**：主要是設定的時間。最便宜的是改 agent 讀什麼，寫幾行規則就夠了。呼叫前後的檢查是程式碼，要有人維護。
- **可以問團隊**：「上一次結果不好，我們修的是上下文、工具清單，還是加了一道模型之外的檢查？」

## agent 出錯，先別急著怪模型 {#problem}

agent 犯錯的時候，大家通常會覺得是背後的大模型出了錯，於是繼續往 prompt 裡加句子來防，像是「小心」「不要做 XX」，或者換一個更聰明的模型，例如從 Sonnet 換到 Opus，再把推理強度開到最高。這些有時候有用，但碰不到根本原因，因為 agent 最後做出什麼事，不只看模型，還要看模型讀到了什麼、手上有哪些工具、呼叫工具的前後有沒有檢查，這些都在模型外面，換一個模型也改變不了。

AI agent 其實由兩部分組成：模型（LLM）和工具（Tool Calling）。你送出 prompt，模型開始思考，可是模型本身只是一顆大腦，沒有手，查檔案、改檔案、執行終端機指令、開瀏覽器，甚至用 Computer Use 從頭到尾操作你的電腦，這些它自己都做不到，要靠 Tool Calling。模型想好要做什麼，就透過提供給它的工具介面發出呼叫，由外面的程式真正去執行（Claude Code、Copilot 的 agent 模式都是這樣的程式），執行的結果再當成下一段輸入交回模型。模型拿到以後繼續思考，決定是再呼叫工具，還是任務已經完成，如果完成了，就回給你一段結果，也就是你看到的答案。

上面這個流程，就是所謂的 **Agent Loop**（迴圈）。

這個迴圈上有四個地方可以改：模型讀到什麼、給它哪些工具、呼叫工具之前的檢查、呼叫之後的檢查。這一章我想教你看懂這個迴圈，以後 agent 出錯時，先判斷該改哪一處，再考慮換模型或加 prompt。

## 迴圈怎麼轉，四個地方怎麼改 {#how-it-works}

::: figure 2-1-loop

### 每一輪，模型都要把 prompt 從頭讀一遍

繞迴圈走一圈，這本書叫一**輪**：程式把 prompt 組好送給模型，模型回一段文字，裡面可能帶著一個或幾個工具呼叫，程式執行這些工具、記下結果，再決定要不要繼續。VS Code 團隊介紹 Copilot 的迴圈時也是這樣切的，只是他們叫 round，而且說 prompt 每一輪都會重新組一次（[The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)）。模型在兩輪之間什麼都不記得，這一輪的 prompt 裡沒有的東西，對它來說就不存在，所以系統提示、規則、你說過的話、之前每一輪的工具呼叫和結果，每一輪都得重新放進去。看文件時要留意，Claude Code 和 Copilot 的文件說 turn，通常指從你送出一則訊息到它給出回答的整段過程，中間可以有很多輪。

從這個過程可以看出兩件事。第一，agent 的每個動作都是一次工具呼叫，因為模型沒有別的辦法做事，而工具是由模型外面的程式執行的，所以在執行之前可以把呼叫攔下來。**hook** 就放在這個位置，它是你寫的一支小程式，平台會在固定的時機執行它，例如每次工具呼叫之前和之後（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)）。第二，模型只看得到 prompt 裡的文字，你的螢幕、你的磁碟它都看不到，它以為專案長什麼樣子，全看上下文裡寫了什麼，而上下文有大小上限（[上下文是一份預算](3-1-context-budget.html)）。

hook 能不能管到所有呼叫，要看平台。Claude Code 的文件寫明了，子 agent 裡的工具呼叫和 MCP 工具都會觸發同樣的 hook（[Hooks reference](https://code.claude.com/docs/en/hooks)）。Copilot 的文件只說，在子 agent 裡觸發的 hook，輸入會多幾個欄位，列出來的工具名稱也都是內建工具，沒有提到 MCP（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)）。我在 Copilot 上看過內建工具和子 agent 的呼叫都會經過 hook，MCP 工具則沒有測過。另外有兩樣東西完全不走這條路。一樣是伺服器端工具，它們在供應商那邊執行，中間沒有你的程式碼（[Agent 用不好工具，先看工具的描述和錯誤訊息](1-2-tool-calling.html)）。另一樣是 Claude Code 裡用 `@` 引用的檔案，預設直接放進上下文，不經過工具呼叫，所以攔讀檔的 hook 根本不會觸發。

### 模型不再要工具，迴圈就停了

迴圈正常結束的條件只有一個，就是模型這一輪沒有要求工具。在 Anthropic 的 API 上，只要 `stop_reason` 是 `tool_use` 就繼續轉，等模型寫完回答、`stop_reason` 變成 `end_turn`，迴圈就結束（[How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)）。Copilot 也一樣，一輪裡沒有工具呼叫，這段文字就是最後的回答。所以迴圈停下來，只代表模型覺得做完了，不代表事情真的做完了，中間沒有任何東西替你檢查過結果。

另外兩種停法不是模型決定的。一種是你自己按停止，VS Code 的文件寫得很清楚，停止不會撤銷已經完成的動作，也不會撤銷對外部服務做過的改動（[Build with AI in VS Code](https://code.visualstudio.com/docs/agents/overview)）。另一種是平台的上限，VS Code 的 `chat.agent.maxRequests` 限制 agent 能送出多少次請求，預設是 25（[AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)）。

還有一種情況剛好相反：模型想停，卻被擋了回去。Copilot 的 `agentStop` 和 Claude Code 的 `Stop`，是模型寫完回答時執行的 hook，它可以回傳 `block` 加上一個原因，這個原因會當成新的 prompt 送回模型，迴圈就繼續轉。這個位置很好用。模型說做完了，hook 可以去看待辦清單或者跑一次測試，沒通過就回一句「還沒完，第 4 步還沒做」，agent 不用你在旁邊盯著，也能把一長串清單做完（[慎用子 agent](2-3-subagents.html)）。代價是它可能一直停不下來，而每轉一輪都要花錢，所以 Copilot CLI 和 Claude Code 都設了保險，連續擋 8 次以後就強制結束，hook 自己也能從 `stop_hook_active` 這個欄位看出，這一輪已經是被擋回來過的（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)、[Hooks reference](https://code.claude.com/docs/en/hooks)）。

### 迴圈上有四個地方可以改

模型怎麼思考，你改變不了，你能改的是它周圍的四樣東西。

1. **它讀什麼**。規則檔、skill、你指給它看的檔案，都是放進上下文的文字，這是用得最多、也最便宜的辦法，寫幾行規則，就能告訴它自己猜不到的事（[指令與 skill：只載入需要的](3-3-instructions-and-skills.html)）。短處是這些文字只是請求，模型可能不照做，而且對話一長，VS Code 和 Claude Code 都會把前面的內容壓縮成摘要，早期的細節和指示就可能不見了。
2. **有哪些工具**。模型只能呼叫你給它的工具，工具的描述和錯誤訊息，也是它認識這個工具的唯一管道（[Agent 用不好工具，先看工具的描述和錯誤訊息](1-2-tool-calling.html)）。想給某個角色固定一份比較短的工具清單，就用 custom agent（[Custom agent：固定模型和工具的角色](2-4-custom-agents.html)）。短處是工具能做的事常常比名字大，你拿掉了改檔案的工具，只要還留著終端機，它照樣能用指令改檔案。
3. **呼叫之前的檢查**。工具執行之前，hook 看得到工具名稱和參數，可以放行，也可以拒絕並說明原因，原因會送回給模型。hook 是平台執行的，模型跳不過去，所以這裡的規則是會執行的程式碼，不是請求。用程式碼守住規則也不只 hook 一種，工具清單、讓 agent 自我檢查的指令都算，只是涵蓋的範圍比較窄（[提示裡的規則只是請求](4-1-requests-and-rules.html)）。平台內建的批准規則也在這個位置，例如 VS Code 依指令文字比對的自動批准規則。短處是它看到的只有呼叫的文字，指令執行起來實際做了什麼，它看不到，VS Code 的文件也說，hook 不能取代強制執行的權限、沙箱或企業管控（[Security](https://code.visualstudio.com/docs/agents/run/security)）。
4. **呼叫之後的檢查**。工具執行之後，hook 看得到結果，可以留一筆紀錄，可以給模型補一段話，在 Copilot 和 Claude Code 裡還能改寫模型讀到的結果。短處是已經發生的事它撤銷不了，VS Code 的文件也是這樣寫的（[Hooks](https://code.visualstudio.com/docs/agent-customization/hooks)），所以要擋的動作，只能在呼叫之前擋。

這四處裡，第 1、4 處改變模型知道什麼，第 2、3 處改變它能做什麼。只寫在規則檔裡的東西，改變的只有它知道什麼。

沙箱是另一類，它不看呼叫，限制的是指令執行起來以後能碰到什麼，所以我沒有把它算進這四樣（[有些東西根本不給](4-5-least-privilege.html)）。

### 常見的錯，先看該改哪一處

迴圈本身很少出問題，Anthropic 的文件說，它的標準寫法就是一個依 `stop_reason` 判斷的 `while` 迴圈，沒幾行程式碼，出問題的幾乎都在上面這四處。下面這張表是我自己用 agent 時累積下來的，記的是我看過的情況，不是統計資料。

| 你看到的 | 通常的原因 | 先改哪裡 |
| --- | --- | --- |
| 它改了不該改的 | 它想的是怎麼把事做完，不是准不准它做 | 呼叫之前的檢查，或者縮小工具清單 |
| 它忘了前面說過的事 | 上下文被壓縮了，或者對話太長 | 它讀什麼：重要的東西放進檔案，不要只留在對話裡（[長對話會變差](3-2-long-sessions.html)） |
| 它檢查自己的成果，說沒問題 | 同一個模型、同樣的推理，有同樣的盲點 | 換個角度來查：另一個 agent，或者一條指令（[慎用子 agent](2-3-subagents.html)） |
| 它一直重試一個被拒絕的動作 | 它想把任務完成 | 拒絕的原因要寫清楚該改做什麼（[詢問不是限制](4-2-ask-vs-refuse.html)） |
| 它說「做完了」，其實沒有 | 迴圈只看模型還要不要工具，而模型又傾向回報成功 | 停下時的檢查，讓它自己跑測試（[讓 agent 能檢查自己的活](5-4-self-checks.html)） |

第三條和最後一條不只是我看過，Anthropic 也寫過。他們發現 agent 給自己的成果打分時總是偏高，品質普通也會很有自信地稱讚（[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)），Claude 也有沒好好測試就把功能標成完成的傾向（[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）。這幾條的原因很少是模型不夠聰明，所以換模型，應該排在這些都查過之後（[選模型，別只看 token 單價](1-1-models-and-cost.html)）。

### 自己看一次迴圈怎麼轉

想親眼看迴圈怎麼轉，什麼都不用裝。在 agent 的對話裡問一句「讀一下 README，告訴我這個專案是做什麼的」，回答出來之前，你會看到一行類似「Read README.md」的字，這就是一次工具呼叫。VS Code 預設把細節收起來，展開就看得到它的輸入和輸出（[Use tools with agents](https://code.visualstudio.com/docs/agents/run/tools)）。再問一個需要讀三個檔案的問題，你會看到三次呼叫，它們可能擠在同一輪裡，而這些結果現在都留在上下文裡了。想看模型每次到底收到了什麼，就在 VS Code 裡執行 **Developer: Show Chat Debug View**，它會依每一次和模型的互動，列出系統提示、prompt、上下文、回答，以及工具的輸入和輸出，一筆一筆翻過去，就能看到每一輪多了什麼（[Debug chat interactions](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view)）。這個畫面裡有你的程式碼和檔案路徑，分享之前要先看過一遍。

## 迴圈越轉越貴，而且它不是一份計畫 {#costs-and-traps}

迴圈的錢主要花在重讀上。每轉一輪，模型都要把整個上下文再讀一遍，裡面還多了上一輪的結果，所以讀的量比輪數漲得快。用[選模型，別只看 token 單價](1-1-models-and-cost.html)那個算例的數字，10 輪總共要讀 325,000 個 token，20 輪就是 1,150,000 個，大約 3.5 倍。prompt 快取能讓重讀便宜很多，Anthropic 讀快取的價格在大多數模型上是輸入價的十分之一，在 Opus 5.5 和 Sonnet 5.5 上是二十分之一（[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)）。但快取省下的只是錢，這些內容照樣占著上下文視窗，照樣分走模型的注意力，Anthropic 說上下文是「邊際收益遞減的有限資源」（[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)）。

在這些文字裡，最少人盯著的是工具結果。prompt 是你寫的，裡面有什麼你心裡有數，可是 agent 讀的檔案、指令印出來的紀錄，你可能從來沒看過，它們一樣占著視窗，模型也可能照著裡面的文字去行動（[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html)）。它們能占掉多少，Anthropic 有一個數字：在一個 100 輪的網頁搜尋評測裡，快到上限時自動清掉過期的工具結果，token 用量少了 84%（[Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)）。

讓模型自己決定下一步，本身也有代價。Anthropic 說 agent 是拿延遲和成本去換更好的任務表現，建議先找最簡單的辦法，需要時才增加複雜度（[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)）。如果一件事的步驟從來不變，一個在固定位置呼叫模型的腳本，可能比 agent 更適合你，它比較便宜，也比較好預測。

還有一個坑，是把迴圈當成一份計畫。模型不是先想好整條路再照著走，而是每一輪依這一輪的 prompt 決定下一步，就算它一開始寫了一份計畫，那也只是上下文裡的一段文字。所以它走上錯路，通常是前面某一輪的結果把它帶過去的，而那個結果還留在上下文裡，之後每一輪都會再讀到。

## 平台內建了，就可以刪掉自己的 hook {#when-to-delete-it}
{status: industry}

只要 agent 還是靠呼叫工具來做事，這個迴圈和這四個地方就不會過時，會過時的是我自己寫的那部分。我今天用 hook 擋呼叫、催 agent 繼續做，是因為平台留給我的就是這幾個位置，如果平台提供了原生的辦法來強制執行規則、預算或停止條件，我會改用它，不再用自己的 hook。這件事已經開始了。VS Code 的 Autopilot 會批准所有工具，推著 agent 一直做到任務完成，開啟 `chat.autopilot.advanced.enabled` 之後，還會由另一個模型來判斷請求有沒有完成（[Security](https://code.visualstudio.com/docs/agents/run/security)、[AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)），而 Claude Code 的 `/goal` 就是一個內建的停止 hook（[Hooks reference](https://code.claude.com/docs/en/hooks)）。

## 在你自己的環境試試 {#try-it}

::: prompt
讀這個專案的指令檔和設定。你找到的每條規則或限制，告訴我它在四個地方的哪一個起作用：agent 讀什麼、有哪些工具、工具呼叫前的檢查、工具呼叫後的檢查。把只是寫下來的請求、模型外面沒有任何東西強制執行的規則，每一條都標出來。列出五條一旦被破壞影響最大的規則。不要修改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Anthropic：[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，它把 agent 定義為「在迴圈裡自主使用工具的 LLM」
- Anthropic：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，講什麼時候固定的 workflow 就夠了
- Anthropic 文件：[How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)，迴圈的標準寫法
- VS Code 部落格：[The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)
- Claude Code 文件：[How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- VS Code 文件：[Set up a context engineering flow in VS Code](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## 在 harness 裡探索 {#explore}

迴圈在哪裡都一樣，但在我的 harness 裡，你可以從旁邊看每一輪往上下文裡放了什麼，hook 看到了哪次呼叫、又回答了什麼。

::: prompt
/harness-rookie-wondering 我讀完了「Agent 到底是怎麼做事的？」這一章。請教我這個 harness 怎麼站在迴圈的四個地方：它往上下文裡放了什麼、允許哪些工具，以及它的 hook 在呼叫前後做什麼。帶我打開真實的檔案，並畫出一輪是怎麼穿過它們的。
:::
