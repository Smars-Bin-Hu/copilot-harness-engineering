讀這一章，需要知道什麼是工具呼叫。如果還不知道，先讀[Agent 用不好工具，先看工具的描述和錯誤訊息](1-2-tool-calling.html)。

## 一句話 {#in-one-sentence}

MCP 是把工具接到 agent 上的標準協定，它通常不會讓 agent 多出新能力，但每接一個 server，別人的程式碼、你的權限、別人寫的文字和一筆 token 成本都會跟著進來，所以接之前先看一條指令夠不夠，接了就當成依賴來管。

## 給主管 {#for-leaders}

- **要做的決定**：把每個 MCP server 都當成一個要批准的依賴，就像一個不是你們寫的函式庫；一條普通指令做得到的事，優先用指令。
- **風險**：server 會帶進來別人的程式碼、你們的權限，以及模型會信以為真的文字，而且批准之後它還可能變，npm 上就出現過前 15 個版本都正常、到 1.0.16 才加後門的 server。hook 管不管得住 Copilot 裡的 MCP 工具，文件沒有寫，我也沒有測過。
- **做對的成本**：每個 server 做一次簡短的審查（誰寫的、能碰什麼、憑證放在哪、版本固定了沒有），再隔一段時間重讀一遍工具清單。
- **可以問團隊**：「現在連著哪些 server？每個是誰批准的，能碰什麼，版本固定了嗎？」

## 沒有 MCP，每個工具都要為每個平台寫一遍 {#problem}

這篇文章，我想教你在接 MCP server 之前想清楚三件事：它到底改變了什麼，接上以後有什麼東西跟著進來，什麼時候一條指令就夠了。

agent 能做多少事，要看它手上有哪些工具，遲早你會想讓它讀問題追蹤系統、查資料庫或者操作瀏覽器，而這些工具總要有人來寫。每個平台（VS Code Copilot、Claude Code、Codex）接工具的方式都不一樣，所以沒有共同標準的話，三個平台、三個工具可能就要九個連接器，每多一個平台或一個工具，要寫和要維護的程式碼都按乘法往上加。

::: figure 1-3-mcp-plug

**Model Context Protocol**（MCP）就是解決這件事的標準，Anthropic 在 2024 年 11 月把它開源。它規定 AI 應用程式和工具之間用什麼格式傳訊息，這樣一個工具只要寫一次，寫成一個 **MCP server**，一個平台也只要實作一次這個協定，之後任何 server 都能接到任何支援 MCP 的平台上，九個連接器就變成了三加三，官方文件打的比方是 USB-C 連接埠。現在 VS Code、Claude Code、Codex、Cursor 和 ChatGPT 都支援它。（[What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro)）

協定裡還有兩個角色要知道。**MCP host** 是 AI 應用程式本身，例如 VS Code 或 Claude Code，host 每連一個 server 就建立一個 **MCP client**，由這個 client 維持和這個 server 的連線。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）

你可能會以為接上 MCP，agent 就多了新能力，其實通常沒有。MCP 改變的是工具怎麼接上去，server 能做的事，agent 用一條指令或者呼叫一個 API 多半也做得到。例外是託管在廠商那邊、自帶登入的遠端 server，它可能給你別的辦法拿不到的存取權。所以接 server 的時候，不用先想它能多給你什麼，要先想除了工具，還有什麼跟著進來了。

## 接上一個 server，到底接進來了什麼 {#how-it-works}

接上一個 server，等於在你的設定裡加了一個不是你寫的依賴，它有自己的程式碼和更新節奏，用著你給的權限，還會往模型的上下文裡寫東西。

### server 能提供三樣東西

協定定義了 server 可以提供的三樣東西，差別在於由誰決定用。**工具**（Tools）是模型自己決定呼叫的函式，例如操作檔案、呼叫 API、查資料庫，多數人說 MCP，指的就是它。**資源**（Resources）是唯讀的資料，例如檔案內容或資料庫 schema，由應用程式決定要不要放進上下文。**提示**（Prompts）是可重複使用的範本，由使用者明確呼叫。（[Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts)）

host 連上 server 以後發一個 `tools/list` 請求，拿回每個工具的名字、描述和參數，再把所有 server 的工具合成一張表交給模型，模型要用某個工具時，host 向對應的 server 發一個 `tools/call`，再把結果放回對話。所以在模型看來，MCP 工具和內建工具沒有差別，它還是只能靠名字、描述和錯誤訊息來用工具，上一章的規則全都適用，只是這些文字現在是別人寫的。

### 本機 server 跑在你的機器上，遠端 server 跑在別人那裡

server 有兩種執行方式，用的是同一套訊息。**本機** server 走 stdio 傳輸，host 在你的機器上啟動一個處理程序，透過它的標準輸入和輸出溝通，所以設定裡寫的其實就是一條啟動指令，例如 VS Code 文件裡 Playwright 的例子是 `npx -y @playwright/mcp@latest`。**遠端** server 走 Streamable HTTP 傳輸，執行在別人的機器上，host 透過 HTTP 和它溝通，通常要登入，同一個 server 通常服務很多使用者，例如 Sentry 官方的 server。

這個差別決定了你要防什麼。本機 server 是用你的權限、在你電腦上執行的程式碼，要防的是它在你機器上做什麼；遠端 server 是別人的服務，要防的是你傳給它的資料，和你交給它的帳號權限。

### 接上一個 server，有四樣東西跟著進來

::: figure 1-3-what-comes-in

1. 別人的程式碼。本機 server 就是執行在你機器上的一支程式，一啟動就在跑，不用等模型呼叫工具。VS Code 的文件說得很直接：「本機 MCP server 可以在你的機器上執行程式碼，工具可以用你的權限存取外部服務。」（[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)）
2. 你的權限。server 用你給它的存取權限做事，例如你的資料庫帳號、你在問題追蹤系統裡的 token，agent 透過這個 server 也就拿到了這些權限，所以 token 的範圍有多大，agent 出錯或被騙的時候，損失就可能有多大。
3. 別人寫的文字。工具的描述是別人寫的，模型會讀、會當真，工具回傳的內容（一個 issue 的內文、一個網頁）也是別人寫的，這些文字裡可能藏著給模型的命令（[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html)）。
4. 一筆固定的 token 成本。工具的名字、描述和參數都算模型的輸入，如果 host 把它們全送給模型，每次請求都要帶上，快取能讓錢少花一些，但占掉的上下文視窗一點也沒少，工具一多，模型也更容易選錯。

第四樣成本可以很大。Anthropic 舉過一個五個 server 的例子，GitHub 的 35 個工具約 26K token，Slack 的 11 個約 21K，再加上 Sentry、Grafana 和 Splunk，一共 58 個工具，對話還沒開始就占了約 55K token（[Introducing advanced tool use for Claude](https://www.anthropic.com/engineering/advanced-tool-use)）。host 這邊的辦法是工具搜尋，先不把工具定義送給模型，只給它一個搜尋工具，用到的時候才載入完整定義。Claude Code 預設就這麼做，會話開始時只載入工具名稱和 server 的說明（[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)）。VS Code 在 Claude Sonnet 4.5、Opus 4.5 以上的模型上也預設開啟，只留讀寫檔案、執行指令這樣一小組核心工具常駐，它的團隊做過線上實驗，用 Claude 模型時，中位使用者一整個會話的 token 用量降了約 18%（[Improving token efficiency for GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot)）。所以這筆成本到底有多大，要看你用的 host、模型和連了多少工具，最好數一數你自己的。

### 先看一條指令夠不夠

agent 需要的很多東西本來就是命令列程式，例如 `git`、`gh`、測試執行器、雲端平台的命令列工具，只要 agent 能用終端機，不接任何 server 就能用上它們。我傾向先用指令，因為它加進你設定裡的程式碼和權限都比較少，等多個平台共用一個工具的好處抵得過多出來的那個依賴，再換成 MCP 也不遲。

工具的廠商自己也這麼建議。VS Code 的文件一開頭就說，現有的工具夠用的話，就不需要再加 server。Claude Code 的文件建議優先用 `gh`、`aws`、`gcloud` 這些命令列工具，因為它們不會往上下文裡加工具清單（[Manage costs effectively](https://code.claude.com/docs/en/costs)）。微軟的 Playwright MCP 的 README 也告訴用 coding agent 的讀者，CLI 加 skill 可能更合適，MCP 留給需要保持瀏覽器狀態的長循環（[Playwright MCP](https://github.com/microsoft/playwright-mcp)）。

不過省多少 token 要看具體的工作。Checkly 的 Stefan Judis 在 2026 年 7 月用 Claude Code 把同一個瀏覽器任務各跑了三遍，用 Playwright MCP 結束時的上下文約 48K 到 50K，用 `playwright-cli` 約 45K 到 48K，差別很小，他的解釋是工具定義現在是延遲載入的（[CLIs are more token-efficient than MCP. Or are they?](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)）。所以在有工具搜尋的 host 上，指令的好處主要是依賴和權限比較少，不在 token 上。

MCP 也有指令比不上的地方。它的每個工具都有名字和參數 schema，host 可以按工具來批准，而 agent 一旦能用終端機，就能跑任何指令，hook 讀到的也只是指令的文字（[Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)）。所以替一個寫入操作很多的內部系統做介面時，幾個窄的 MCP 工具可能比一個什麼都能做的命令列程式更好管。

| 選 | 什麼時候 |
| --- | --- |
| 命令列程式 | 它已經有了，在本機執行，輸出又短又清楚，agent 又能用終端機 |
| MCP server | 你想在多個平台上共用同一個工具，需要結構化的輸入，要登入一個遠端服務，想按工具來批准，或者 agent 執行的地方沒有終端機 |

### 接之前問五個問題

既然 server 是依賴，對任何依賴該問的問題，對它也都該問，下面五個按我會問的順序排。

- 誰寫的，誰在持續更新？VS Code 的建議是，在安裝或啟動之前先看「發布者、指令或端點，以及它請求的存取權限」（[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)）。上架了也不等於審查過，MCP 官方的 Registry 只存中繼資料、驗證發布者的命名空間，安全掃描交給 npm 這樣的套件倉庫和下游的市集（[The MCP Registry](https://modelcontextprotocol.io/registry/about)）。
- 它能碰什麼？優先選只限於任務所需的 server，例如一個讀 issue 的 server，就不該拿著一個能刪倉庫的 token。
- 憑證放在哪？別放在對話裡，也別提交進專案，VS Code 的文件還提醒，個人設定檔也不是存機密的地方（[MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)）。
- 版本固定了嗎？啟動指令裡寫著 `@latest` 的話，套件一更新，之後啟動跑的就可能是新程式碼，所以要寫死一個看過的版本。
- 它回傳的東西可信嗎？如果文字來自外部，例如公開的網頁、任何人都能開的工單，就當成不可信的。

### hook 管不管得住 MCP 工具，各家不一樣

Claude Code 的文件寫明了，MCP 工具在 `PreToolUse`、`PostToolUse` 這些事件裡和一般工具一樣出現，名字是 `mcp__<server>__<tool>`（[Hooks reference](https://code.claude.com/docs/en/hooks)）。Copilot 這邊沒有寫，GitHub 的 hook 參考只說 `preToolUse` 在「每個工具執行之前」觸發，列出來的工具名稱都是內建工具，VS Code 的 hook 文件也沒有提到 MCP（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)）。我自己的 harness 沒有搭任何 MCP server，這類 server 是公司依自己的環境設定的，有的公司還禁止非官方的，所以 MCP 工具在 Copilot 上是不是經過 hook、hook 能不能看到完整的參數，我沒有測過。

想靠 hook 的話，先用一個無害的 server 測一次，寫一個只記錄輸入的 hook，呼叫一次 MCP 工具，看記錄裡有沒有這次呼叫、參數全不全。就算經過了 hook，它看到的也只是這次呼叫的參數，server 收到以後做了什麼，它看不到。

### 接上以後怎麼查

已經連上的 server 也要回頭看，對每一個問三個問題：

1. 我知道它是誰寫的、能碰什麼嗎？
2. 命令列程式能做同樣的事嗎？
3. 它的工具裡，我真正用到的有幾個？

第三個問題不用安裝任何東西就能回答。在 VS Code 裡打開 **Chat: Open Customizations** 的 Tools 頁，能看到每組工具啟用了幾個、一共幾個，在 Claude Code 裡用 `/context` 看是什麼在占上下文。數完再想想上週用過其中哪些，其餘的都是有成本、有風險，卻沒有收益的，可以把工具關掉，或者把整個 server 停用。

## 官方的 server 也會出事，審查過的 server 也會變 {#costs-and-traps}

每個 server 都是外部文字和外部程式碼通往 agent 的一條路，接得越多，能出問題的地方就越多，而且不只在用的才算，當初為了試試加上、後來忘掉的 server 也一直在那裡。

名氣大也不是跳過審查的理由。Invariant Labs 在 2025 年 5 月公開過一個例子，攻擊者在一個公開倉庫裡開一個 issue，裡面藏著給 agent 的指示，使用者只是讓 agent 看看這個倉庫的 issue，而 agent 連著官方的 GitHub MCP server，又有權限讀使用者的私有倉庫，結果它把私有倉庫的內容寫進了公開倉庫的一個 pull request。Invariant 說這不是 server 程式碼的缺陷，GitHub 光改 server 修不好，他們的建議是收窄權限，例如一個會話只讓 agent 碰一個倉庫（[GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)）。不可信的文字、私有資料和對外的出路，這三樣在這裡全湊齊了（[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html)）。「官方」只告訴你程式碼是誰寫的，它拿著你的憑證，照樣會讀到別人寫的文字。

就算是你仔細審查過的 server，也可能在你不知情的時候變了，變的地方有三處。

- 工具清單變了。協定允許 server 更新工具，再通知 client 重新抓取清單，所以 server 可以在你批准之後改掉某個工具的描述，這種做法叫 rug pull。描述裡能藏什麼，Invariant Labs 示範過，叫工具投毒（tool poisoning），一個看起來只做加法的 `add` 工具，描述裡藏著一段話，要模型讀 `~/.ssh/id_rsa`，再把內容放進一個參數傳回去（[Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)）。
- 程式碼變了。npm 上的 `postmark-mcp` 冒用 Postmark 的名字，前 15 個版本都正常，到 1.0.16 才加上後門，把郵件偷偷用密件副本寄到外部伺服器（[Security Alert: Malicious 'postmark-mcp' npm Package](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)）。
- 設定變了。VS Code 裡工作區的 `.mcp.json` 和 `.vscode/mcp.json` 跟著 Workspace Trust 走，在受信任的工作區裡，設定改了也不會再單獨問你，而設定裡寫的是一條會執行的指令，所以改這些檔案的 pull request 要當成改程式碼來審（[Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers)）。

所以要隔一段時間重讀一遍工具清單，能固定版本就固定。

另一個陷阱是以為標準一樣，行為也就一樣。協定只統一了 host 和 server 之間的訊息，設定放在哪、支援協定的哪些部分、怎麼批准，都是各家自己定的，光 VS Code 就有兩種設定格式，頂層鍵一個是 `mcpServers`，一個是 `servers`，不能直接互相複製，各家的設定放在哪，可以查[擴充點速查表](a-extension-points.html)。協定本身也還在變，目前的版本是 2026-07-28，這一版拿掉了連線時的交握和會話，還把 sampling、roots 和 logging 標成棄用，距離上一版只有八個月（[Key Changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)）。只是用別人的 server，這些變化你多半感覺不到，自己寫 server 的話，就要留出跟版本的時間。

## 協定和 VS Code 都把決定權留給了你 {#industry}
{status: industry}

協定的文件說，MCP 只管交換上下文，「不規定 AI 應用程式如何使用 LLM，也不規定如何管理所提供的上下文」（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）。規格要求 host 呼叫任何工具之前都要得到使用者明確的同意，同時也承認 MCP 自己沒辦法在協定層面強制這些原則（[Specification](https://modelcontextprotocol.io/specification/latest)）。VS Code 就是這樣一個 host，它讓你看發布者和請求的存取權限，只批准你理解的操作，給組織的是 `ChatMCP` 政策，可以把 server 限制在一份 registry 裡，不過這個政策管不到 Copilot 執行環境自己發現的 server（[Secure AI-assisted development in VS Code](https://code.visualstudio.com/docs/agents/run/security)）。所以兩邊的分工是一致的，協定讓接入變容易，決定接入什麼仍然是你的事。

## 什麼時候可以刪掉一個 server {#when-to-delete-it}
{status: industry}

不再用某個 server 的工具了，或者一條普通指令就能完成任務了，就把它移除。

這份謹慎什麼時候能放鬆，要看平台。如果平台預設把本機 server 關進沙箱，壞的 server 能做的事就少很多，但是寫這一章的時候還沒到這一步，VS Code 的 Copilot 會話沙箱預設是關的，打開以後也預設不擋對外網路連線（[Sandbox Copilot agent sessions](https://code.visualstudio.com/docs/agents/run/agent-sandboxing)）。沙箱也只管得住 server 這個處理程序，管不了你交給它的遠端帳號，也管不了它回傳給模型的文字，所以就算有了沙箱，我還是會在新增之前檢查發布者和存取權限。

## 在你自己的環境試試 {#try-it}

::: prompt
找出為這個專案或編輯器設定的每一個 MCP server（看編輯器和專案的設定，以及所有 MCP 設定檔）。每一個，告訴我：誰發布的、在本機還是遠端執行、啟動指令有沒有固定版本、用什麼憑證以及存在哪裡、提供了多少個工具、一個普通的命令列程式能不能做同樣的事。把存在已提交檔案裡的憑證標出來。不要印出任何機密的值，也不要修改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)、[Specification](https://modelcontextprotocol.io/specification/latest)、[Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices)、[Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- VS Code 文件：[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)、[Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers)、[MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)，讓 agent 寫程式碼來呼叫 server，中間結果不進模型的上下文，代價是要有一個安全的沙箱
- Invariant Labs：[Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)、[GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)

## 在 harness 裡探索 {#explore}

我的 harness 給 agent 三類工具：內建工具、它自己的命令列工具，還有可選的 MCP，它自己沒有搭任何 MCP server。harness 可以和你一起打開真實的檔案，帶你看 MCP 會接在哪裡，其他工具又是怎麼分類的。

::: prompt
/harness-rookie-wondering 我讀完了「接 MCP server 之前，要想清楚什麼？」這一章。請教我這個 harness 裡的三類工具，以及 MCP 放在哪裡。帶我打開真實的檔案，讓我看工具名稱是怎麼分到各類裡的。
:::
