讀這一章，你需要知道什麼是工具。如果不知道，先讀 [Tool calling，和給 agent 設計工具](1-2-tool-calling.html)。

## 一句話 {#in-one-sentence}

MCP 不是新的能力，而是工具的標準插頭；插上它，別人的程式碼、權限和文字也跟著進了你的 agent。

## 給主管 {#for-leaders}

- **要做的決定**：把每個 MCP server 當成一個要你批准的依賴，就像一個不是你寫的函式庫；一個普通的指令就能完成的工作，優先用指令。
- **風險**：server 會帶進別人的程式碼、別人的權限，以及模型會讀、也會照做的文字，而且在你批准之後，它的工具清單還可能改變。hook 能不能像守內建工具那樣守住 MCP 工具，我沒有測過。
- **做對的成本**：每個 server 做一次簡短的審查（誰寫的、能碰什麼、憑證放在哪裡），再隔一段時間重讀一次工具清單。
- **可以問團隊**：「接了哪些 server？每個是誰批准的？每個能碰什麼？」

## 工具為什麼需要一個標準插頭？ {#problem}

agent 有多少用處，取決於它手上有哪些工具。遲早你會想讓它讀你的問題追蹤系統、查資料庫，或操作瀏覽器，而這些工具都得有人寫。麻煩的是，每個平台（VS Code Copilot、Claude Code、Codex）接收工具的方式都不一樣。

所以，沒有共同的標準，工作量就會成倍增加。三個平台加三個工具，可能需要九個各自獨立的連接器，每一個都是有人要寫、寫完還要持續更新的程式碼。每多一個平台，就多一列；每多一個工具，就多一欄。

::: figure 1-3-mcp-plug

**Model Context Protocol**（MCP）就是解決這個問題的標準。它給兩頭定了同一套**協定**，也就是一種約定好的傳訊息的方式。有了它，不同人寫的兩個程式也能一起工作。這樣一來，一個工具只要寫一次，寫成一個 **MCP server**；一個平台也只要學一次這個協定。之後，任何 server 都能配合任何支援 MCP 的平台。想想 USB 插座就懂了：插頭是標準，至於你插上去的是什麼，它一概不管。

在工具這一頭，MCP server 是用標準方式向 agent 提供能力的程式，可以跑在你的機器上，也可以跑在別處。另一頭是 **MCP host**，也就是 AI 應用程式，例如 VS Code。它對連上的每個 server 各建一個 **client**，由這個 client 負責維持連線。

那麼，一個標準插頭會不會讓 agent 多出新的本事？一般不會（有自己登入機制的遠端服務是例外，它能提供你用別的辦法拿不到的存取）。MCP 改變的是工具*怎麼接上去*。既然改的只是接法，真正該問的就是：跟著工具一起，還有什麼從這個插頭進來了。

## 你接進來的到底是什麼 {#how-it-works}

### server 能提供什麼

要看清進來了什麼，得先知道 server 能往這邊送些什麼。協定定義了 server 可以公開的三樣東西。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）大多數人說 MCP，指的是其中的 **Tools**（工具），也就是 agent 可以呼叫來做事的函式，例如檔案操作、API 呼叫、資料庫查詢，它和 [Tool calling，和給 agent 設計工具](1-2-tool-calling.html) 裡的工具是同一類。除了工具，server 還可以提供 **Resources**（資源），也就是 agent 可以讀來當上下文的資料，例如檔案內容或資料庫紀錄；以及 **Prompts**（提示），也就是可重複使用的範本，用來幫忙組織對話，例如 system prompt 或 few-shot 範例。

在用到這些之前，agent 這一邊會先問 server 有什麼。對工具來說，這是一個 `tools/list` 請求，拿回來的是每個工具的名字、描述和它接受的參數。之後模型要求呼叫某個工具，host 就向對的 server 送出一個 `tools/call`，再把答案當文字放回對話。所以從模型的角度看，MCP 工具和其他任何工具沒有兩樣。

### 本地和遠端

server 有兩種跑法，兩種用的是同一個協定。**本地（stdio）** server 由 host 在你的機器上當成程式啟動，host 透過它的標準輸入和輸出（每個命令列程式都有的純文字管道）跟它說話。通常也只有這一個 host 在用它。**遠端（Streamable HTTP）** server 跑在別處，host 透過普通的網路請求（HTTP）跟它說話，通常要登入。一個遠端 server 可以服務很多使用者。

這個差別在安全上很重要，因為本地 server 是在你的電腦上、以你的權限執行的程式碼；遠端的則是別人的服務，你得把資料送過去。

### 接上一個，就帶進來什麼

不過，不管本地還是遠端，server 都不是打開就好的功能，而是一個**依賴**，像一個不是你寫的函式庫。接上它，會帶進來四樣東西。

::: figure 1-3-what-comes-in

1. 它帶進別人的程式碼，因為本地 server 就在你的機器上執行。VS Code 自己的文件說：「本地 MCP server 可以在你的機器上執行程式碼，而工具可以用你的權限存取外部服務。」（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）
2. 它帶進別人的權限。server 以你給它的存取權行動，例如你的資料庫登入、你在問題追蹤系統的 token，於是 agent 透過 server，也擁有了那些存取權。
3. 它帶進別人的話，而模型會把這些話當成指令。server 的工具描述，是模型會讀、也會當真的文字；工具回傳的內容（issue 的內文、網頁），也是寫它的人寫的文字。模型讀到的文字，可能含有給它的命令，[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html) 講的就是這個。
4. 它帶進一筆固定的成本。每個工具的名字、描述和參數，每次呼叫都會送給模型，所以一個工具很多、你卻很少用的 server，每一輪還是要花 token；而且工具一多，模型就更難選（[Tool calling，和給 agent 設計工具](1-2-tool-calling.html)）。繞開的辦法是有的，這裡只點到為止。協定自己的文件提到，連了很多 server 的 client，可以用漸進式的工具探索，不必一開始就載入所有工具（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）。Anthropic 的文章 [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) 則把工具定義塞滿上下文視窗當成一個問題，並描述了只載入需要的工具，或讓 agent 透過程式碼呼叫 server 的做法。成本有多大，取決於你接了多少工具，所以數一數你自己的。

### 加一個之前要檢查什麼

既然 server 是一個依賴，任何依賴該問的問題，它都該問。下面是四個，照我會問的順序排。

- 誰寫的？誰持續更新它？VS Code 的建議是，安裝或啟動 server 之前，先檢視「發布者、指令或端點，以及要求的存取權」。
- 它能碰什麼？盡量用只限於工作所需的 server，例如讀 issue 的 server，就不該握有能刪除倉庫的 token。
- 憑證放在哪裡？別放在對話裡，也別提交進專案，VS Code 的文件也是這樣提醒的。
- 它回傳的能信嗎？如果文字來自外面，例如公開的網路、任何人都能開的工單，就當成不可信的輸入。

### 用 MCP，還是只用一個指令？

在這四個問題之前，其實還有一個問題：這個工具真的需要 server 嗎？你的 agent 需要的很多東西，早就以命令列程式的形式存在了，例如 `git`、測試執行器、雲端 CLI。只要 agent 能用終端機，完全不需要 server 就能用它們。

| 選 | 什麼時候 |
| --- | --- |
| 命令列程式 | 它已經存在、在本地執行，輸出又短又清楚。牽涉的環節更少 |
| MCP server | 你想在好幾個平台上用同一個工具，或者它需要結構化的輸入、可探索的能力清單，或登入遠端服務 |

我傾向先用指令，因為它在你的設定裡加的程式碼和權限比較少。等共用插頭的好處開始值得多出來的那個依賴，再換成 MCP。

### hook 守得住 MCP 工具嗎？

你也許希望，hook 能像擋下一次糟糕的內建工具呼叫那樣，擋下一次糟糕的 MCP 呼叫。這一點我沒辦法向你保證。我自己的 harness 沒有建任何 MCP server（這類 server 是公司照自己的環境設定的，有些公司環境還禁止非官方的），所以 MCP 工具呼叫會不會像內建工具呼叫那樣經過 hook、hook 看不看得到完整的參數，我**沒有測過**。在你自己用一個無害的 server 測試過之前，不要指望 hook 能替你守住 MCP 工具。

### 怎麼檢查你自己的設定

已經接上的 server，也值得回頭看一看。對每一個，問三個問題：

1. 我知道是誰寫的、它能碰什麼嗎？
2. 一個命令列程式能做同樣的工作嗎？
3. 它的工具，我真正用到幾個？

第三個問題，不用安裝任何東西就能回答。列出你的 agent 目前有的工具（大多數編輯器在對話的工具選擇器裡顯示，確切在哪要看編輯器，查一下它的文件），數一數，再問自己過去一週用過其中哪些。其餘的，就是有成本、有風險，卻沒有好處。

## 插頭多了，會在哪裡出問題 {#costs-and-traps}

風險先從 server 本身說起。每個 server 都是外面的文字和外面的程式碼通向你的 agent 的一條路，所以每多接一個插頭，攻擊面就大一些。而且不只是正在用的才算，那些當初為了試試而加、後來忘掉的 server，也一直在那裡。

名氣大，也不是跳過審查的理由。受人敬重的公司發布的 server 是「官方」的，可它一樣會拿到你的憑證，也一樣會回傳別人寫的文字。官方不代表對你安全。

就算是你仔細審查過的 server，也可能在你不知道的時候變了。協定讓 server 可以通知 client，它的工具變了，所以你審查時沒問題的工具，下個月可能就不是你手上這個了。server 還可以在你批准之後改工具的描述，而描述是模型會照做的文字（這種攻擊常被叫做 rug pull 或 tool poisoning，[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html) 講了這個想法）。所以要不時重讀清單，能固定 server 的版本就固定。

最後一個陷阱，是以為標準一樣，行為也就一樣。各平台支援協定的哪些部分、怎麼要求批准、設定存在哪裡，都不同，所以請查你的平台目前的文件。

## 協定和 VS Code 也這麼看嗎？ {#industry}
{status: industry}

協定自己的文件把 MCP 描述成交換上下文的協定，並說它「不規定 AI 應用程式怎麼使用 LLM，或怎麼管理提供的上下文」。換句話說，載入什麼、怎麼問你，由 host 決定。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）VS Code 正是這樣的一個 host，它把 server 當成要審查的程式碼：看發布者和要求的存取權，只批准你看得懂的動作。（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）

所以兩者在分工上是一致的。協定讓接上去變容易，而決定接什麼，仍然是你的事。

## 什麼時候可以刪掉一個 server {#when-to-delete-it}
{status: industry}

決定接什麼，也包括決定拔掉什麼。你不再用某個 server 的工具，或者一個普通指令就能做同樣的事，就把它移除。如果平台開始預設把 server 放進沙箱，讓壞的 server 做不了太大的壞事，這份謹慎本身也可以放鬆一些。即使這樣，我還是會在加之前，先檢查發布者和存取權。

## 在你自己的環境試試 {#try-it}

::: prompt
找出為這個專案或編輯器設定的每個 MCP server（看編輯器和專案的設定，以及任何 MCP 設定檔）。每一個都告訴我：誰發布的、在本地還是遠端執行、用什麼憑證、憑證存在哪裡、公開幾個工具，以及一個命令列程式能不能做同樣的工作。標出任何存在已提交檔案裡的憑證。不要印出機密的值，也不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code 文件：[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## 在 harness 裡探索 {#explore}

我的 harness 給 agent 三種工具：內建的、它自己的命令列工具，以及可選的 MCP。它本身沒有建任何 MCP server。harness 可以和你一起打開真實的檔案，帶你看 MCP 會接在哪裡，以及其他工具是怎麼分類的。

::: prompt
/harness-rookie-wondering 我讀完了「MCP server：插工具的標準接口」這一章。請教我這個 harness 的三種工具，以及 MCP 接在哪裡。帶我打開真實的檔案，讓我看工具名稱是怎麼分成幾類的。
:::
