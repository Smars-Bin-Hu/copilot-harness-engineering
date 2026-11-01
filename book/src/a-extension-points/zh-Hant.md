這個附錄是一張查詢表。哪天你想知道「這個東西該放哪裡、agent 什麼時候看得到、能不能強制」，就在這裡找到對應的那一列，再順著連結去讀講清楚原因的那一章。

## 照著哪一列做之前 {#read-first}

**確認日期：2026-10-27**。那一天我為這一頁讀了 VS Code、Claude Code 和 Codex 的官方文件。名稱、資料夾、設定和 Preview 標籤常常改，所以這一頁遲早會過期。日期寫在這裡，就是為了讓你在靠哪一列做決定之前先查一查。表和文件對不上時，以文件為準。

有兩件事，決定了這些列該怎麼讀。

- **VS Code 現在要你先選一個 harness**。這裡的 harness 是 VS Code 自己的叫法，指 Copilot harness、Local harness 這樣的選項。照文件的說法，選哪一個，決定了哪些格式和位置行得通。文件的原話是：「建立一個檔案，不代表選定的 harness 能載入或執行它。」下面有些列寫著「只有 Local harness」，就是這個緣故。
- **這裡的「強制」只有一個意思**。只有平台硬性要求 agent 服從、模型沒有選擇餘地的，才算強制。照這個標準，幾乎每一列都只是對模型的請求，例外只有兩樣：拒絕呼叫的 hook，和把工具拿掉的工具清單。這個差別為什麼重要，是 [提示裡的規則只是請求](4-1-requests-and-rules.html) 這一章的主題。

如果你知道自己要什麼，卻不知道它該歸到哪一列，可以先看這裡：

- 每個任務都適用的規則：永遠載入的指令。
- 只對某些檔案適用的規則：依檔案的指令。
- agent 在合適時啟動的做法：skill。
- 不同的一組工具，或唯讀的幫手：custom agent。
- 必須被拒絕的事：hook，或把工具拿掉。

## VS Code Copilot {#copilot}

表裡每一列依次回答開頭那三個問題：它是什麼，agent 什麼時候看得到，能不能強制。

| 擴充點 | 它是什麼 | 什麼時候載入 | 強制？ | 章節 |
| --- | --- | --- | --- | --- |
| 指令，永遠載入 | 倉庫根目錄的 `.github/copilot-instructions.md` 和 `AGENTS.md`。`CLAUDE.md` 只有 Local harness 讀，而且要開啟 `chat.useClaudeMdFile`。 | 自動加進 agent 的上下文。巢狀的 `AGENTS.md` 是實驗性的，預設關閉（Local harness）。 | 不強制，是請求。文件說適用的各個來源是疊加的，所以別指望靠順序來化解衝突。 | [指令與 skill：只載入需要的](3-3-instructions-and-skills.html) |
| 指令，依檔案 | `.github/instructions` 裡的 `*.instructions.md`（Claude 格式：`.claude/rules`）。 | 正在改的檔案符合 `applyTo` glob 時附上，或 `description` 符合任務時按需載入。 | 不強制，是請求。 | [指令與 skill：只載入需要的](3-3-instructions-and-skills.html) |
| Prompt 檔 | `.github/prompts`（或你的使用者設定檔）裡的 `*.prompt.md`。一個存起來的 prompt，標頭可以視需要帶 `agent`、`model` 和 `tools`。 | 只有你執行它的時候：輸入 `/` 和它的名字。只在 Chat 檢視裡的 Local harness 會話。不會自動套用。 | 不強制，它就是一個 prompt。不過它的 `tools` 清單，優先於它指名的那個 agent 的工具清單。 | 沒有章節涵蓋 prompt 檔。請看你所用工具的官方文件。 |
| Skills | 一個帶 `SKILL.md` 的資料夾，放在 `.github/skills/`、`.claude/skills/` 或 `.agents/skills/`（你的家目錄下也一樣）。 | 三層：先是名稱和描述；請求符合或你輸入 `/name` 時載入內文；其他檔案只在內文指向它們時載入。 | 不強制，要不要用由模型決定。`disable-model-invocation: true` 讓模型不能啟動它，這限制的是誰來啟動，不是它做什麼。 | [指令與 skill：只載入需要的](3-3-instructions-and-skills.html)、[把團隊的做法寫成 skill](3-4-skills-and-workflows.html) |
| Custom agent | `.github/agents`（Claude 格式：`.claude/agents`）裡的 `*.agent.md`，有標頭和一段指令內文。 | 你在 Agent 下拉選單選它時，或別的 agent 把它當子 agent 執行時。在 Copilot harness 裡，它的指令加進你的自訂指令，衝突時以它為準。 | `tools` 清單強制：文件說「只有那些工具可用」。內文，例如「不要做 X」，是請求。 | [Custom agent：固定模型和工具的角色](2-4-custom-agents.html)、[慎用子 agent](2-3-subagents.html) |
| Hooks | `.github/hooks/` 裡的 JSON 檔，或設定檔裡的 `hooks` 對照表。事件包括 `sessionStart`、`userPromptSubmitted`、`preToolUse`、`postToolUse`、`subagentStart`、`subagentStop`、`agentStop`。 | 由平台在那些時刻執行。在 Local harness，`chat.useHooks` 控制是否執行。hook 檔在視窗啟動時讀取。 | 強制，限於它看得到的：`preToolUse` 可以回傳附原因的拒絕。逾時的話，會退回正常的權限檢查。文件標為 Preview。 | [Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)、[把執行層當軟體來設計](4-4-enforcement-design.html) |
| MCP server | 新增工具的 server。個人：`~/.copilot/mcp-config.json`。共用：專案根目錄的 `.mcp.json`（實驗性的 `chat.mcp.workspaceRootConfig.enabled` 只決定 **MCP: Add Server** 要不要提供這個位置，關掉時現有的檔案仍然可用）。較舊的：`.vscode/mcp.json`。 | 依使用者或工作區設定。送出訊息時，VS Code 可以啟動 server 來探索工具：實驗性的 `chat.mcp.autostart` 預設是 `newAndOutdated`，會啟動從沒執行過或設定改過的 server。登入和工具批准出現時，由你審查。 | server 做什麼不強制，不過你的組織可以限制哪些 server 可用。 | [接 MCP server 之前，要想清楚什麼？](1-3-mcp.html) |
| 工具組和工具清單 | 對話裡的工具挑選器（Copilot harness：Customizations 編輯器的 Tools 分頁；Local harness：Configure Tools）。輸入 `#` 來指名一個工具。一個請求最多可以有 128 個工具。 | 依設定檔或依請求選擇。 | 是：沒有啟用的工具不能呼叫。不過，啟用一個工具並不會跳過它的批准。 | [Agent 用不好工具，先看工具的描述和錯誤訊息](1-2-tool-calling.html)、[Custom agent：固定模型和工具的角色](2-4-custom-agents.html) |
| 設定 | 開關以上各項的 VS Code 設定，例如 `chat.useHooks`、`chat.useAgentsMdFile`、`chat.useClaudeMdFile`、`chat.includeApplyingInstructions`、`chat.useCustomizationsInParentRepositories`。 | 由 VS Code 讀取。Copilot CLI 和 Copilot app 不繼承編輯器的設定，所以文件建議不要依賴自訂位置的設定。 | 不是給模型的規則。這些是主機端的設定。企業管控可以開關 hook，而企業管理的 Copilot 設定生效時，Claude 和 Codex harness 會被停用。 | [30 分鐘搭一個最小 harness](0-2-minimal-harness.html) |

關於工具組，再補一句。VS Code 文件說，使用者定義的工具組（`.jsonc` 檔）已經棄用，Copilot harness 也不支援。想要一套可以重複使用的工具選擇，文件建議的是帶 `tools` 清單的 custom agent。所以我把工具組當成舊有功能。

## Claude Code 和 Codex 裡的同樣幾點 {#counterparts}

如果你也用 Claude Code 或 Codex，下面是同樣這幾列在它們那邊的樣子。這兩欄我自己沒有跑過，因為這本書的例子都來自 Copilot 這一邊的同一套設定。這兩欄依據的是各廠商文件在上面那個日期的說法。官方頁面上確認不了的地方，我沒有猜，格子裡一律寫「未確認」。

| 擴充點 | Claude Code | Codex |
| --- | --- | --- |
| 指令，永遠載入 | `CLAUDE.md`（專案、使用者、組織）。它也可以讀倉庫的 `AGENTS.md` 來代替 `CLAUDE.md`。文件稱它為「上下文，不是強制的設定」。 | 從專案根目錄一路往下到目前資料夾，每個目錄的 `AGENTS.md`，以及需要取代某一個時用的 `AGENTS.override.md`。這串檔案每次執行時合併一次，合併後的大小上限是 `project_doc_max_bytes`（預設 32 KiB）。 |
| 指令，依檔案 | 帶 `paths` 標頭的 `.claude/rules/*`。 | 更靠近工作的巢狀 `AGENTS.md` 檔。依檔案樣式的標頭：未確認。 |
| Prompt 檔 | `.claude/commands/*.md` 仍然行得通，但 command 已經合併進 skill。同名的 skill 優先。 | `~/.codex/prompts/` 裡有自訂 prompt，但已棄用，改用 skill。以 `/prompts:name` 執行。不透過倉庫共用。 |
| Skills | `.claude/skills/<name>/SKILL.md`（專案）、`~/.claude/skills/`（個人）。描述永遠在上下文裡；內文在被呼叫時才載入。 | `.agents/skills`（倉庫，從目前資料夾一路到根目錄）、`$HOME/.agents/skills`、`/etc/codex/skills`。同樣的三層載入。`agents/openai.yaml` 裡的 `allow_implicit_invocation: false` 會讓模型不能自行啟動它。 |
| Custom agent | `.claude/agents/*.md`，有 `tools`（允許清單）、`disallowedTools` 和 `model`。 | `.codex/agents/*.toml`（專案）或 `~/.codex/agents/`，一個檔案一個 agent，有 `name`、`description`、`developer_instructions` 和選用的模型設定。子 agent 繼承父層的沙箱、批准政策和 MCP server。每個 agent 的工具允許清單：未確認。 |
| Hooks | `.claude/settings.json`、`.claude/settings.local.json` 或 `~/.claude/settings.json` 裡的 `hooks`。結束碼 2，或 JSON 的 `permissionDecision` 為 `deny`，會在 `PreToolUse` 擋下。預設情況下，失敗或逾時的 hook 不會擋。 | `~/.codex/` 或 `<repo>/.codex/` 裡的 `hooks.json`，或 `config.toml` 裡的 `[hooks]`。`PreToolUse` 可以拒絕。專案的 hook 只在受信任的專案載入，而且必須先審查。文件稱 hook 是護欄，不是完整的強制邊界。hook 逾時會怎樣：未確認。 |
| MCP server | 專案裡的 `.mcp.json`（共用）、`~/.claude.json`（本機和使用者範圍）。專案的 server 在互動式會話裡要求批准。 | `~/.codex/config.toml` 裡的 `[mcp_servers.<name>]`，或受信任專案的 `.codex/config.toml`。`codex mcp add` 和 `codex mcp list`。 |
| 工具組 | 未確認有這樣一個獨立功能。我找到最接近的，是子 agent 的 `tools` 允許清單。 | 未確認。 |
| 設定 | `settings.json`（使用者、專案、本機，和受管理的政策）。我只對 hook 檢查過。 | `~/.codex/config.toml` 和 `.codex/config.toml`，有 `approval_policy` 和 `sandbox_mode`。`requirements.toml` 可以在受管理的機器上限制它們。 |

## 怎麼用這一頁 {#how-to-use}

有兩個習慣，能讓這張表派上用場。

- **把規則放在夠用的、最輕的那一點**。這幾個點分量不同：永遠載入的指令每一輪都占空間，skill 只在用到時才占，hook 要花的是寫程式碼的功夫。誰輕誰重、為什麼，見 [上下文是一份預算](3-1-context-budget.html) 和 [提示裡的規則只是請求](4-1-requests-and-rules.html)。
- **先查 harness，再查檔案**。一個檔案好像被忽略了，先問問你選的 harness 到底能不能載入這種檔案。如果問題不出在 harness 上，[排錯](b-troubleshooting.html) 會從你看到的症狀查起。
