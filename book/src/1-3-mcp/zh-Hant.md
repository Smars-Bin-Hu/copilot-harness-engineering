讀這一章，你需要知道什麼是工具。如果不知道，先讀 [Tool calling，和給 agent 設計工具](1-2-tool-calling.html)。

## 一句話 {#in-one-sentence}

MCP 不是新的能力。它是工具的標準插頭，會把別人的程式碼、權限和文字帶進你的 agent。

## 給主管 {#for-leaders}

- **要做的決定**：把每個 MCP server 當成一個要你批准的依賴，就像一個不是你寫的函式庫；如果一個普通的指令就能完成工作，優先用指令。
- **風險**：server 會帶進別人的程式碼、別人的權限，以及模型會讀、也會照做的文字。它的工具清單，還可能在你批准之後改變。hook 能不能像守內建工具那樣守 MCP 工具，我沒有測過。
- **做對的成本**：每個 server 做一次簡短的審查（誰寫的、能碰什麼、憑證放在哪裡），再定期重讀工具清單。
- **可以問團隊**：「接了哪些 server？每個是誰批准的？每個能碰什麼？」

## 問題 {#problem}

agent 的用處，取決於它有的工具。你可能想讓它讀你的問題追蹤系統、查資料庫，或操作瀏覽器。每個工具都得有人寫，而每個平台（VS Code Copilot、Claude Code、Codex）又各有自己接收工具的方式。

沒有共同的標準，工作量就會成倍增加。三個平台加三個工具，可能需要九個各自獨立的連接器。每個連接器都是有人要寫、要持續更新的程式碼，每多一個平台或工具，就多一列或一欄。

::: figure 1-3-mcp-plug

**Model Context Protocol（MCP**）就是解決這個問題的標準。一個工具寫一次，成為一個 **MCP server**。一個平台學一次這個協定。之後，任何 server 都能配合任何支援 MCP 的平台。想想 USB 插座：插頭是標準，而它對你插上去的是什麼，一個字也沒說。

### 先講三個詞

- **MCP server** 是用標準方式向 agent 提供能力的程式。它可以跑在你的機器上，也可以跑在別處。
- **MCP host** 是 AI 應用程式，例如 VS Code。它對連上的每個 server，各建一個 **client**。client 負責握住連線。
- **協定**是約定好的傳訊息的方式，讓不同人寫的兩個程式能一起工作。

這一章始終抓住一個想法。MCP 通常不會給 agent 一個它本來不可能有的能力（有自己登入機制的遠端服務是例外：它能提供你用別的辦法拿不到的存取）。它改變的是工具*怎麼接上去*。接下來各節說的，都由此而來。

## 原理 {#how-it-works}

### server 能提供什麼

協定定義了 server 可以公開的三樣東西。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）

- **Tools（工具**）：agent 可以呼叫來做事的函式：檔案操作、API 呼叫、資料庫查詢。大多數人說 MCP 指的就是這個，它和 [Tool calling，和給 agent 設計工具](1-2-tool-calling.html) 裡的工具是同一類。
- **Resources（資源**）：agent 可以讀來當上下文的資料，例如檔案內容或資料庫紀錄。
- **Prompts（提示**）：幫忙組織對話的可重複使用範本，例如 system prompt 或 few-shot 範例。

agent 這一邊，先問 server 有什麼（對工具來說，是一個 `tools/list` 請求），拿回每個工具的名字、描述和它接受的參數。模型要求一次呼叫時，host 會向對的 server 送出一個 `tools/call`，再把答案當文字放回對話。從模型的角度看，這和其他任何工具沒有兩樣。

### 本地和遠端

server 有兩種跑法。

- **本地（stdio**）。host 在你的機器上把 server 當成程式啟動，透過標準輸入和輸出（每個命令列程式都有的純文字管道）跟它說話。通常是一個 host 用它。
- **遠端（Streamable HTTP**）。server 跑在別處，host 透過普通的網路請求（HTTP）跟它說話，通常要登入。一個遠端 server 可以服務很多使用者。

兩種的協定是一樣的。差別在安全上很重要：本地 server 是在你的電腦上、以你的權限執行的程式碼，遠端的則是別人的服務，你要把資料送過去。

### 你把一個接上去，就把什麼帶進來了

這是這一章的重點。server 不是你打開的一個功能，而是一個**依賴**，像一個不是你寫的函式庫。它會帶進來四樣東西。

::: figure 1-3-what-comes-in

1. **別人的程式碼**。本地 server 在你的機器上執行。VS Code 自己的文件說：「本地 MCP server 可以在你的機器上執行程式碼，而工具可以用你的權限存取外部服務。」（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）
2. **別人的權限**。server 以你給它的任何存取權行動：你的資料庫登入、你的問題追蹤系統 token。agent 現在透過 server 擁有了那些存取權。
3. **別人的話，當成指令**。server 的工具描述，是模型會讀、也會當真的文字。而工具回傳的（問題的內文、網頁），是寫它的人寫的文字。模型讀到的文字，可能含有給它的命令。[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html) 講的就是這個。
4. **固定的成本**。每個工具的名字、描述和參數，每次呼叫都會送給模型。一個有很多你很少用的工具的 server，每一輪還是要花 token，而且工具一多，模型就更難選（[Tool calling，和給 agent 設計工具](1-2-tool-calling.html)）。協定自己的文件提到，連了很多 server 的 client，可以用漸進式的工具探索，不必一開始就載入所有工具。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）Anthropic 的文章 [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) 把工具定義塞滿上下文視窗，當成一個問題，並描述了只載入需要的工具，或讓 agent 透過程式碼呼叫 server。我在這裡只是指出它們。成本有多大，取決於你接了多少工具，所以數一數你自己的。

### 加一個之前要檢查什麼

四個問題，是我會問的順序。

- **誰寫的？誰持續更新它**？VS Code 的建議是，安裝或啟動 server 之前，先檢視「發布者、指令或端點，以及要求的存取權」。
- **它能碰什麼**？偏好只限於工作所需的 server。讀問題的 server，不該握有能刪除倉庫的 token。
- **憑證放在哪裡**？不放在對話裡，也不提交進你的專案。VS Code 警告不要把憑證貼進對話，也不要提交。
- **它回傳的能信嗎**？如果文字來自外面（公開的網路、任何人都能開的工單），當成不可信的輸入。

### 用 MCP，還是只用一個指令？

不是每個工具都需要 server。你的 agent 需要的很多東西，早就以命令列程式的形式存在了：`git`、測試執行器、雲端 CLI。能用終端機的 agent，完全不需要 server 就能用它們。

| 選 | 什麼時候 |
| --- | --- |
| 命令列程式 | 它已經存在、在本地執行，輸出又短又清楚。活動的部分更少 |
| MCP server | 你想在好幾個平台上用同一個工具，或者它需要結構化的輸入、可探索的能力清單，或登入遠端服務 |

我傾向先用指令，因為它在你的設定裡加的程式碼和權限比較少。等共用的插頭開始值得多出來的依賴時，再換成 MCP。

### 我沒測過的

在你測試過之前，不要指望 hook 能保護你不受 MCP 工具影響。我自己的 harness 沒有建任何 MCP server。公司會為自己的環境設定它們，有些公司環境禁止非官方的。MCP 工具呼叫會不會像內建工具呼叫那樣經過 hook，hook 看不看得到完整的參數，我**沒有測過**。如果你靠 hook 來守 MCP 工具，先用一個無害的 server 測一下。

### 測你自己的設定

對你接上的每個 server，**問三個問題**：

1. 我知道是誰寫的、它能碰什麼嗎？
2. 一個命令列程式能做同樣的工作嗎？
3. 它的工具，我真正用到幾個？

**一個不用安裝任何東西的檢查**。列出你的 agent 目前有的工具（大多數編輯器在對話的工具選擇器裡顯示；去哪看請查你編輯器的文件）。數一數。然後問自己，過去一週用過哪些。其餘的，是有成本、有風險，卻沒有好處。

## 代價和陷阱 {#costs-and-traps}

**插頭越多，被攻擊的面就越大**。每個 server 都是外面的文字和外面的程式碼，通向你的 agent 的一條路。你為了試試而加、後來忘了的 server，還在那裡。

**「官方」不代表對你安全**。受人敬重的公司發布的 server，一樣會拿到你的憑證，也一樣會回傳別人寫的文字。

**server 的工具清單可能變**。協定讓 server 可以通知 client，它的工具變了。你審查時沒問題的工具，下個月可能就不是你手上這個了。server 還可以在你批准之後改工具的描述，而描述是模型會照做的文字（這種攻擊常被叫做 rug pull 或 tool poisoning；[agent 讀到的文字可能在指揮它](4-6-untrusted-input.html) 講了這個想法）。不時重讀清單，能固定 server 的版本就固定。

**共同的標準，不等於共同的行為**。各平台支援協定的哪些部分、怎麼要求批准、設定存在哪裡，都不同。請查你的平台目前的文件。

## 業界怎麼說 {#industry}
{status: industry}

- **協定自己的文件**把 MCP 描述成交換上下文的協定，並說它「不規定 AI 應用程式怎麼使用 LLM，或怎麼管理提供的上下文」。載入什麼、怎麼問你，由 host 決定。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）
- **VS Code** 把 server 當成要審查的程式碼：看發布者和要求的存取權，只批准你看得懂的動作。（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）

兩者在分工上一致：協定讓接上去變容易，而決定接什麼，仍然是你的事。

## 什麼時候可以刪掉 {#when-to-delete-it}
{status: industry}

你不再用某個 server 的工具，或者一個普通指令就能做同樣的事，就把它移除。如果平台開始預設把 server 放進沙箱，讓壞的 server 做不了太大的壞事，這份謹慎也會放鬆。我仍然會在加之前，先檢查發布者和存取權。

## 在你自己的環境試試 {#try-it}

不用裝 harness。在你自己的倉庫裡打開 agent，貼上：

::: prompt
找出為這個專案或編輯器設定的每個 MCP server（看編輯器和專案的設定，以及任何 MCP 設定檔）。每一個都告訴我：誰發布的、在本地還是遠端執行、用什麼憑證、憑證存在哪裡、公開幾個工具，以及一個命令列程式能不能做同樣的工作。標出任何存在已提交檔案裡的憑證。不要印出機密的值，也不要改任何檔案。
:::

## 延伸閱讀 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code 文件：[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## 在 harness 裡探索 {#explore}

我的 harness 給 agent 三種工具：內建的、它自己的命令列，以及可選的 MCP。它本身沒有建任何 MCP server。harness 可以帶著真實的檔案，讓你看 MCP 會接在哪裡，以及其他工具是怎麼分類的。照上面的說明準備好之後，輸入：

::: prompt
/harness-rookie-wondering 我讀完了「MCP server：插工具的標準接口」這一章。請教我這個 harness 的三種工具，以及 MCP 接在哪裡。帶我打開真實的檔案，讓我看工具名稱是怎麼分成幾類的。
:::

它一次教一小塊，停下來確認你跟得上，然後和你一起打開檔案。
