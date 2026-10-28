這個附錄是一個小模式的架子。每個模式有：一行的問題、幾行的模式、一個你可以照著抄的我的 harness 的真實檔案，以及解釋原因的章節。它們是讓你改寫的例子，不是讓你整份貼上的。這些檔案是釘住的 tag 上的真實檔案，所以比你的第一版應該有的更長、更具體。抄過去之後，在你自己的環境裡把每一個都檢查一遍。如果不知道從哪裡開始，先拿安全的模式（拒絕一個指令，把批准留給人），然後是省上下文的，再來是給長任務用的。每個模式都有一行**限制**，取自它連結的那一章。

## 把核心限制放在一頁上 {#core-limits}

**問題**。agent 亂猜路徑和指令，或者把你改過的檔案「整理」掉。

**模式**。保留一頁永遠載入的短頁面。只放沒有它模型就會做錯的東西，並放在最前面。開始時，兩條限制就夠了。

::: code harness AGENTS.md L44-L45 "出貨的規則頁裡的兩條核心限制：動手前先看，並保留使用者自己的改動。"

**限制**。越寫越長的頁面就不會被讀了；每一行都必須有存在的理由。

更多在 [指令與 skill：只載入需要的](3-3-instructions-and-skills.html) 和 [30 分鐘搭一個最小 harness](0-2-minimal-harness.html)。

## 只為適用的檔案載入規則 {#rules-by-file}

**問題**。只對某一種檔案重要的規則，在每個對話裡都占空間。

**模式**。把規則放進帶 `applyTo` 樣式的指令檔。agent 處理符合的檔案時才載入，其他時候不花任何東西。

::: code harness .github/instructions/skills.instructions.md L1-L4 "依檔案載入的指令的標頭：一段描述和一個 applyTo 樣式。"

**限制**。這是對模型的請求，不是平台強制的規則。

更多在 [指令與 skill：只載入需要的](3-3-instructions-and-skills.html)。

## 每個時刻共用一個 hook 入口 {#one-hook-entry}

**問題**。好幾個 hook 腳本，各有自己的逾時和 shell，很難保持一致。

**模式**。讓設定檔只說要在哪些時刻呼叫，並把每個時刻都指向同一個程式。由程式決定要做什麼。設定時間上限，並記得這個檔案是在視窗啟動時讀的。

::: code harness .github/hooks/harness.json L40-L51 "工具執行之前那個時刻的入口：它只指名程式和它的時間上限。"

**限制**。逾時的 hook 會被當成通過，所以要讓它快。

更多在 [Hooks：每次呼叫都會經過的執行點](2-2-hooks.html) 和 [把執行層當軟體來設計](4-4-enforcement-design.html)。

## 拒絕危險的指令，並附上原因 {#refuse-with-reason}

**問題**。造成的傷害無法復原的指令，例如遞迴刪除根目錄或家目錄，絕不該執行。

**模式**。每一條寫一個樣式和一句 `why`。agent 會讀這個原因，所以要說這個指令會做什麼。樣式要窄，因為錯誤的拒絕就是一個卡住的任務。它擋得住常見的寫法，不是每一種寫法。

::: code harness .harness/policies/gate.json L59-L62 "一條真實的拒絕規則：遞迴強制刪除根目錄、家目錄或目前的資料夾，附上 agent 讀得懂的原因。"

**限制**。這是減速丘，不是邊界：它擋住常見的寫法。對絕不能被碰的東西，不要交出去（[有些東西根本不給](4-5-least-privilege.html)）。

更多在 [詢問不是限制](4-2-ask-vs-refuse.html) 和 [Hooks：每次呼叫都會經過的執行點](2-2-hooks.html)。

## 把批准留給人的終端機 {#person-only-commands}

**問題**。如果 agent 能執行批准的指令，批准就沒有意義。

**模式**。在同一個 hook 裡，拒絕每一個授予權限的指令。原因要告訴 agent，請人在他自己的終端機裡執行。請 agent 執行其中一個，來測試它。

::: code harness .harness/policies/gate.json L83-L86 "對只有人才能執行的指令的拒絕：批准、豁免、開啟無人值守模式。"

**限制**。只有在 hook 執行、它的檔案被保護時才行得通。

更多在 [兩道門：人在哪裡批准](5-3-two-approvals.html) 和 [保護規則本身的檔案](4-3-guardrails.html)。

## 標記一個只有人能啟動的 skill {#user-only-skill}

**問題**。一個花錢或交出權限的 skill，不該因為模型覺得合適就啟動。

**模式**。設定 `disable-model-invocation: true`，並在描述裡說明 agent 不可以呼叫它。這限制的是誰來啟動 skill。它不限制 skill 啟動之後做什麼。

::: code harness .github/skills/harness-autorun/SKILL.md L1-L8 "一個只有使用者能啟動的 skill 的開頭：標頭裡的旗標，和描述裡的那句話。"

**限制**。它限制誰來啟動 skill，不限制 skill 做什麼。

更多在 [指令與 skill：只載入需要的](3-3-instructions-and-skills.html) 和 [無人值守：什麼時候必須停](5-7-when-to-stop.html)。

## 一個唯讀的幫手 {#read-only-helper}

**問題**。你想讓 agent 讀很多東西，卻不能改任何東西。

**模式**。建立一個 custom agent，它的 `tools` 清單只有讀和搜尋，而且不能呼叫別的 agent。工具清單是限制；內文裡的「不要」是請求。在內文裡說明這個幫手必須交回什麼。

::: code harness .github/agents/mapper.agent.md L1-L8 "一個唯讀的幫手：工具清單只有讀和搜尋，而且它不呼叫其他 agent。"

**限制**。每個幫手都從空的上下文開始，所以好幾個幫手的花費是一個 agent 的好幾倍。

更多在 [Custom agent：固定模型和工具的角色](2-4-custom-agents.html) 和 [慎用子 agent](2-3-subagents.html)。

## 給幫手一份它能單獨使用的簡報 {#helper-brief}

**問題**。幫手看不到你的對話，所以含糊的呼叫只會得到含糊的答案。

**模式**。寫下問題、要讀的範圍，和要交回的項目，附上長度限制，每個結論都要有來源。

::: code harness .github/skills/generic-mapreduce/templates/brief.md L5-L18 "給唯讀幫手的簡報：問題、範圍、要交什麼、長度和來源。"

更多在 [慎用子 agent](2-3-subagents.html)。

## 回答 PASS 或 FAIL 的檢查者 {#pass-fail-checker}

**問題**。寫長篇大論的檢查者，讓人沒有東西可數，腳本也沒有東西可讀。

**模式**。把第一行固定為 PASS 或 FAIL。每個發現都指名一個檔案和一行，以及它違反的規則。不給建議，不給修法，有長度限制。這樣腳本就可以數通過的次數，並丟掉沒有指向任何地方的發現。

::: code harness .github/agents/reviewer.agent.md L58-L76 "獨立檢查者的固定輸出：一行結論、附檔案和行號的發現、長度上限。"

**限制**。模型當檢查者還是會犯錯；錯誤的 FAIL 會讓作者去追一個不存在的問題。

更多在 [讓「通過」可信](5-5-counted-checks.html) 和 [模型能檢查模型嗎](5-6-model-checks-model.html)。

## 把需求寫在一頁上，並讓人確認 {#requirement-page}

**問題**。請求含糊又會變，之後沒有人說得出當初同意了什麼。

**模式**。agent 寫一頁：要做什麼、不要做什麼、什麼時候算做完，以及一份誠實的「還不清楚」清單。最上面一行記下人有沒有確認。

::: code harness .harness/contracts/templates/task/en/REQ.md L1-L42 "需求頁：要做什麼、不要做什麼、做完的條件、還不清楚的，和誰確認的。"

更多在 [需求由 agent 寫，人確認](5-2-requirements.html)。

## 給下一個會話的交接檔 {#handover-file}

**問題**。新的對話對舊對話裡做過的工作一無所知。

**模式**。保留一個新會話最先讀的短檔案：狀態、正在做什麼、下一步、要讀什麼，以及人做了什麼決定。每次停下來之前更新它。不要盲目相信它：是 agent 寫的。

::: code harness .harness/contracts/templates/task/en/TASK.md L1-L23 "任務的交接檔：狀態、現在在做什麼、下一步、要讀的檔案、決定、未解決的問題。"

**限制**。是 agent 寫的，所以可能是錯的；把重要的對照來源檢查。

更多在 [管任務，不管對話](5-1-tasks.html) 和 [跨會話的長任務](5-8-long-work.html)。

## 寫下人知道的那些使用 {#known-uses}

**問題**。模型或腳本產生的程式碼地圖看起來沒問題，而你沒有辦法知道它之後有沒有弄丟東西。

**模式**。人在抽取器出現之前，寫下幾個他知道存在的使用，一行一個。地圖的每次執行，都必須找到所有這些。

::: code harness .harness/examples/kb-toolkits/spring/facts.jsonl L4-L8 "Spring 範例的五個已知使用：一個物件、使用的種類、另一個物件。"

**限制**。一份短清單，說明地圖找得到一個使用。它不說明地圖全都找得到。

更多在 [Toolkit：用腳本畫出程式碼的地圖](8-2-kb-toolkit.html)。

## 每次都用同樣的方式報告抽查 {#audit-report}

**問題**。對模型輸出的檢查，最後變成一段文字，兩次抽查沒辦法比較。

**模式**。一份固定的報告：通過或失敗、每種類型的分數、每一處差異及其檔案和行號、規律、被修正的解讀。

::: code harness .github/skills/generic-kb-toolkit-audit/templates/audit.md L1-L36 "抽查報告的範本：結果、每種類型的分數、漏掉的、假的使用、規律、被修正的解讀。"

**限制**。小樣本只看得出大的差距。

更多在 [地圖對不對：盲抽查](8-3-kb-audit.html)。

## 讓一次停止自己說明原因 {#stop-reason}

**問題**。無人值守的執行以「遇到問題」停下來，讓人自己去弄清楚發生了什麼。

**模式**。告訴 agent 什麼時候該停、什麼時候不該停，以及原因必須包含什麼：哪一步卡住了、為什麼、人必須決定什麼。事實能顯示的停止，仍然由 hook 判斷。

::: code harness .github/skills/harness-autorun/references/when-to-stop.md L11-L36 "什麼時候自己停、什麼時候不停，以及怎麼為回來的人寫下原因。"

更多在 [無人值守：什麼時候必須停](5-7-when-to-stop.html)。
