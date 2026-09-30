# questions_d567.py
# Domain 5 (Q41-Q50), Domain 6 (Q51-Q60), Domain 7 (Q61-Q70)

D567_QUESTIONS = [
    # --- DOMAIN 5: TOOL & ACTION DESIGN WITH MCP (10 questions) ---
    {
        "id": "Q41",
        "num": 41,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q41: MCP Progressive Disclosure to Reduce Baseline Tokens",
        "question": "An enterprise agent is integrated with 80 corporate MCP tools across SAP, Salesforce, and Databricks. Including full JSON schemas for all 80 tools bloats the initial system prompt to 38,000 tokens before any user message is processed. How does the 'Progressive Disclosure' pattern solve this problem?",
        "options": [
            {
                "key": "A",
                "text": "Provide only a lightweight tool index (tool name and a 1-sentence summary) in the initial prompt, and provide a meta-tool allowing the agent to dynamically fetch the full parameter schema JIT when it decides to invoke a specific tool",
                "verdict": "正解！ Progressive Disclosure（段階的情報開示）では、初期プロンプトにはツール名と1行概要のインデックスのみを提示し、エージェントが必要と判断したツールのみメタツール経由で詳細スキーマを動的ロードします。"
            },
            {
                "key": "B",
                "text": "Delete 70 of the 80 tools permanently from the corporate network",
                "verdict": "誤り。ビジネス要件（80種類の連携）を満たせなくなります。"
            },
            {
                "key": "C",
                "text": "Strip all parameter descriptions and allow the model to guess argument types",
                "verdict": "誤り。引数エラーやハルシネーションが頻発します。"
            },
            {
                "key": "D",
                "text": "Encode all tool schemas into base64 strings so the tokenizer ignores them",
                "verdict": "誤り。トークン数はむしろ増加します。"
            }
        ],
        "correct": "A",
        "explanation": "MCP Progressive Disclosure（段階的情報開示）：大量のツールが存在する場合、最初から全ツールの完全な JSON Schema を常駐させると、それだけでコンテキストウィンドウの大部分を浪費します。名前と1行要約のカタログのみを初期プロンプトに含め、モデルがそのツールを使いたいと判断した瞬間に詳細スキーマを動的取得（JIT Schema Fetching）することで、ベースライントークンを80%以上削減できます。",
        "rules": [
            "MCP Progressive Disclosure: 初期は名前と1行概要のみ開示 → 必要時に動的スキーマ取得",
            "トークン最適化: 常時消費されるベースライントークンを大幅に削減"
        ]
    },
    {
        "id": "Q42",
        "num": 42,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q42: Tool Disambiguation to Prevent Context Confusion",
        "question": "An agent has access to `fetch_active_subscribers` and `fetch_subscriber_history`. The agent frequently calls `fetch_subscriber_history` when users simply want the current status, returning 500 historical rows instead of 1. How should the tool definitions be refactored?",
        "options": [
            {
                "key": "A",
                "text": "Disambiguate the tools by updating their Description fields to explicitly state exact use-cases, input preconditions, and contrasting boundaries (e.g., 'Use ONLY for historical timeline analysis; do NOT use for current active status checks')",
                "verdict": "正解！ 類似ツールの使い分けの混乱（Context Confusion）を防ぐには、Description において『どのような場面で使うべきか』『どのような場面で使ってはならないか』の境界条件を対比して明記（Disambiguation）します。"
            },
            {
                "key": "B",
                "text": "Merge both tools into a single tool called `do_everything_with_subscribers` with 40 optional arguments",
                "verdict": "誤り。引数の複雑性が増し、さらに混同が悪化します。"
            },
            {
                "key": "C",
                "text": "Rely on the user to specify the exact Python function name in their prompt",
                "verdict": "誤り。エンドユーザーに内部コードの指定を強いるのは不適切です。"
            },
            {
                "key": "D",
                "text": "Increase the model's sampling temperature to 2.0",
                "verdict": "誤り。ランダム性が増して挙動がさらに壊れます。"
            }
        ],
        "correct": "A",
        "explanation": "ツールの曖昧性解消（Tool Disambiguation）：類似した責務を持つツール群に対しては、ツール名だけでなく Description（説明文）において『いつ使うべきか（When to use）』および『いつ使ってはならないか（When NOT to use）』を明確に対比して記載します。これにより Context Confusion を防止し、適切なツールの選択率を向上させます。",
        "rules": [
            "Tool Disambiguation: 類似ツールの用途境界（When to use / When NOT to use）をDescriptionで対比明記",
            "Context Confusion 根絶: 境界条件をはっきりさせることでツールの誤呼出を防ぐ"
        ]
    },
    {
        "id": "Q43",
        "num": 43,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q43: Pruning Raw Intermediate Tool Outputs",
        "question": "In turn 2 of a session, an agent invokes an inventory API that returns 6,000 lines of raw JSON. In turn 3, the agent extracts the single critical number needed: `total_backordered_units = 42`. As the conversation reaches turn 8, the 6,000 lines of raw JSON remain in the message history, crowding out context space. What is the recommended remediation?",
        "options": [
            {
                "key": "A",
                "text": "Prune the intermediate tool response: replace the raw 6,000-line JSON payload in the conversational message history with a compact semantic summary or reference pointer, retaining only the extracted values",
                "verdict": "正解！ 必要な情報（42件）の抽出が完了した過去の中間生データ（Raw output）は、後続ターンでは無意味なノイズとなるため、履歴から要約またはポインタに置き換えてプルーニング（Pruning）します。"
            },
            {
                "key": "B",
                "text": "Keep all 6,000 lines untouched forever to guarantee historical cryptographic integrity",
                "verdict": "誤り。推論コンテキストに生ログを残し続けると Context Distraction とウィンドウ枯渇を招きます。"
            },
            {
                "key": "C",
                "text": "Delete all past conversational turns including the user's initial question",
                "verdict": "誤り。会話の前提やゴールが失われてしまいます。"
            },
            {
                "key": "D",
                "text": "Ask the user to copy and paste the 6,000 lines into an email",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "中間生出力のプルーニング（Intermediate Raw Output Pruning）：APIツールが返した巨大な未加工レスポンス（生JSONや生HTML）は、モデルが必要な値を取り出した後は単なるコンテキストの圧迫要因となります。会話履歴内のツール結果メッセージを、抽出された要約値（例: `{backordered: 42}`）に上書き・プルーニングすることで、健全なウィンドウ容量を維持します。",
        "rules": [
            "Tool Output Pruning: 抽出完了後の巨大な生データは要約やポインタに置換する",
            "Context Distraction 防止: 過去の中間ダンプが現在のアテンションを阻害するのを防ぐ"
        ]
    },
    {
        "id": "Q44",
        "num": 44,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q44: Agent Skills Packaging for Rare Troubleshooting Routines",
        "question": "A system prompt contains 3,500 tokens detailing an obscure, rarely used disaster-recovery rollback script for a specific legacy database. This script is used in less than 0.5% of sessions, yet consumes token budget in 100% of user sessions. How should this operational knowledge be refactored?",
        "options": [
            {
                "key": "A",
                "text": "Package the recovery procedure into a discrete 'Agent Skill' (e.g., an executable script or Unity Catalog SQL function with an on-demand instruction file) that is loaded dynamically only when disaster recovery is invoked",
                "verdict": "正解！ めったに使われない専門知識や特殊手順は、常時プロンプトに常駐させず「Agent Skill」として外部ファイルや関数にカプセル化し、必要時にのみオンデマンドでロードするのがベストプラクティスです。"
            },
            {
                "key": "B",
                "text": "Permanently discard the disaster recovery script and accept data loss when outages occur",
                "verdict": "誤り。事業継続性を損ないます。"
            },
            {
                "key": "C",
                "text": "Hardcode the script into the client's web browser cookies",
                "verdict": "誤り。技術的に的外れです。"
            },
            {
                "key": "D",
                "text": "Duplicate the prompt text 5 times to ensure the agent memorizes it",
                "verdict": "誤り。トークン浪費をさらに加速させます。"
            }
        ],
        "correct": "A",
        "explanation": "Agent Skills へのカプセル化（Skills Packaging）：発生頻度の低い特殊な手順書やスクリプトをシステムプロンプトに常駐させると、平常時のすべての対話で無駄なトークンコストと遅延が発生します。これらは独立した「Agent Skill（モジュール化された手順と実行ツール）」として定義し、トリガーされた時だけコンテキストに引き込む設計にします。",
        "rules": [
            "Agent Skills: 低頻度の高度手順は常駐させず、オンデマンドなスキルとして外部化する",
            "常駐トークンの最小化: 日常会話でのプロンプトオーバーヘッドを大幅に削減"
        ]
    },
    {
        "id": "Q45",
        "num": 45,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q45: Idempotency and Side-Effect Safety in Action Design",
        "question": "An agent has two tools: `preview_invoice_adjustments` (read-only calculation) and `commit_invoice_adjustments` (writes permanent updates to financial ledgers). During network retries, the agent mistakenly re-executes `commit_invoice_adjustments`, resulting in double billing. What architectural controls must be established?",
        "options": [
            {
                "key": "A",
                "text": "Enforce idempotency keys on write tools, explicitly tag tools with side-effect metadata in their MCP schema, and introduce an affirmative Human-in-the-Loop (HITL) confirmation gate before executing irreversible mutations",
                "verdict": "正解！ 破壊的変更を伴うツールには、①同一リクエストの重複実行を防ぐ冪等性キー（Idempotency Key）、②読み取り専用と書き込みの明示的タグ付け、③実行前の人間による承認ゲート（HITL）を設けるのが不可欠です。"
            },
            {
                "key": "B",
                "text": "Remove the read-only preview tool so the agent only executes write operations directly",
                "verdict": "誤り。安全性がさらに悪化します。"
            },
            {
                "key": "C",
                "text": "Instruct the model: 'Please be very careful when writing data'",
                "verdict": "誤り。プロンプトによる精神論ではネットワーク再試行による二重課金は防げません。"
            },
            {
                "key": "D",
                "text": "Configure the database to automatically double all numbers to match",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "副作用を伴うツールの安全性設計：財務更新やデータ削除のような副作用（Side-effects）を持つツールには、①リトライ時の多重実行を防ぐ冪等性（Idempotency）、②MCP 定義での明示的な Read/Write 区別、③実行前の確認ステップ（Human-in-the-Loop）をアーキテクチャとして組み込みます。",
        "rules": [
            "Idempotency Keys: ネットワークや推論のリトライ時における意図しない二重実行を防止",
            "HITL Confirmation: 不可逆な書き込みアクション前には明示的な承認ゲートを配置"
        ]
    },
    {
        "id": "Q46",
        "num": 46,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q46: Self-Describing Validation Feedback for Tool Error Recovery",
        "question": "An agent passes an argument `date = '2024/05/01'` to a tool that requires ISO 8601 format (`YYYY-MM-DD`). Currently, the tool returns a generic error string: `Error: 500 Internal Server Error`. The agent gives up and hallucinates an answer. How should the tool response be engineered to enable self-correction?",
        "options": [
            {
                "key": "A",
                "text": "Return a structured, self-describing validation error specifying: `{\"error\": \"InvalidDateFormat\", \"expected\": \"YYYY-MM-DD\", \"received\": \"2024/05/01\", \"suggestion\": \"Format string as '2024-05-01'\"}`",
                "verdict": "正解！ ツールエラー時に『期待される形式』『受け取った値』『具体的な修正提案』を構造化した自己記述的フィードバック（Self-describing error）を返すことで、エージェントが自律的に引数を自己修正してリトライできます。"
            },
            {
                "key": "B",
                "text": "Terminate the agent session immediately and lock the user's account",
                "verdict": "誤り。単なる引数フォーマット違反に対する過剰反応です。"
            },
            {
                "key": "C",
                "text": "Suppress all error messages and return a fake success code",
                "verdict": "誤り。データの不整合やハルシネーションを招きます。"
            },
            {
                "key": "D",
                "text": "Print the entire Linux kernel source code into the error message",
                "verdict": "誤り。無意味なトークン浪費です。"
            }
        ],
        "correct": "A",
        "explanation": "ツールの自己記述的エラーフィードバック（Self-describing Validation Errors）：ツール実行エラー時に不親切な汎用エラー（HTTP 500など）を返すと、モデルは何が間違っていたのか理解できず推論が停止します。期待するスキーマと具体的な修正方法を明記したエラーオブジェクトを返すことで、エージェントが次ステップで正しく自己修正（Self-correction）してリトライできるようになります。",
        "rules": [
            "Self-describing Errors: エラー内容、期待フォーマット、修正提案を構造化して返す",
            "自律的自己修正（Self-correction）: モデルが自律的に引数を直して再実行できるようにする"
        ]
    },
    {
        "id": "Q47",
        "num": 47,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q47: MCP Resource vs MCP Tool vs MCP Prompt",
        "question": "Under the Model Context Protocol (MCP) specification, what is the architectural distinction between an 'MCP Resource' and an 'MCP Tool'?",
        "options": [
            {
                "key": "A",
                "text": "Resources are passive, readable data sources (like files or database records) designed for direct context injection; Tools are active executable functions with potential side-effects that take arguments and return computed results",
                "verdict": "正解！ MCP Resource はファイルやスキーマのような受動的・読取専用のデータ提供者（コンテキスト注入用）、MCP Tool は引数を取って能動的に処理を実行する関数（計算・副作用用）です。"
            },
            {
                "key": "B",
                "text": "Resources are written in Java, whereas Tools are written in HTML",
                "verdict": "誤り。実装言語の定義ではありません。"
            },
            {
                "key": "C",
                "text": "Tools can only be called once per calendar year, while Resources are unlimited",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "There is no difference; they are exact synonyms in the MCP spec",
                "verdict": "誤り。MCP仕様上明確に区別されています。"
            }
        ],
        "correct": "A",
        "explanation": "Model Context Protocol (MCP) の基本概念：\n- **MCP Resource**: 静的または受動的なデータソース（ドキュメント、テーブルスナップショット等）。アプリケーション側からコンテキストとして安全に読み取られます。\n- **MCP Tool**: モデルが自律的に決定して呼び出す実行可能関数。引数を受け取り、外部API呼び出しやDB更新などの処理（副作用）を実行します。\n- **MCP Prompt**: 事前定義された再利用可能なプロンプトテンプレート。",
        "rules": [
            "MCP Resource: 受動的な読取専用データ（コンテキスト注入用）",
            "MCP Tool: 能動的な実行関数（計算、API呼出、副作用を伴うアクション用）"
        ]
    },
    {
        "id": "Q48",
        "num": 48,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q48: Tool Call Batching and Multi-Tool Parallel Execution",
        "question": "An analytics agent needs to retrieve current stock levels across 10 independent warehouse locations. Executing sequential single-location tool calls (`get_stock(loc='NY')`, `get_stock(loc='LA')`, etc.) takes 10 turns and 45 seconds. How should this action design be optimized?",
        "options": [
            {
                "key": "A",
                "text": "Enable parallel tool calling / batch tool execution, allowing the agent to emit all 10 independent tool calls in a single inference step or providing a bulk parameter `get_stocks(locations=[\"NY\", \"LA\", ...])`",
                "verdict": "正解！ 独立した同一ツールの呼び出しは、マルチツール並列呼出（Parallel Tool Calling）またはバルク引数を許容するバッチ設計にすることで、推論ターン数とレイテンシを大幅に削減できます。"
            },
            {
                "key": "B",
                "text": "Instruct the agent to guess the stock for 9 locations and only query 1",
                "verdict": "誤り。重大なハルシネーションです。"
            },
            {
                "key": "C",
                "text": "Reduce the network bandwidth of the Databricks cluster to force slower execution",
                "verdict": "誤り。逆効果です。"
            },
            {
                "key": "D",
                "text": "Consolidate all 10 warehouses into a single physical building",
                "verdict": "誤り。現実世界を勝手に変えることはできません。"
            }
        ],
        "correct": "A",
        "explanation": "ツール呼び出しのバッチ化と並列化：10個の独立したデータ取得を1ターンずつ順次実行するのは、推論往復回数（Round trips）とトークン消費の大きな無駄です。並列ツール呼び出し（Parallel Tool Calling）をサポートするか、配列を受け取れる一括取得API（Batch Tool）を提供することで、1ターンで全データを効率的に取得します。",
        "rules": [
            "Parallel / Batch Tool Calling: 独立した取得処理を1ターンにまとめて並列実行する",
            "レイテンシ削減: 複数ターンの往復オーバーヘッドを解消"
        ]
    },
    {
        "id": "Q49",
        "num": 49,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q49: Handling 429 Rate Limits and Exponential Backoff",
        "question": "A tool calling an external weather API receives an HTTP 429 (Rate Limited) response. Without error handling, the agent hallucinates: 'The weather in Chicago is 72°F and sunny.' How should the MCP tool client handle this condition?",
        "options": [
            {
                "key": "A",
                "text": "Implement automatic retries with exponential backoff and jitter at the tool execution layer, and if limits persist, return a clean deterministic error indicating service unavailability so the agent can inform the user truthfully",
                "verdict": "正解！ レートリミット（HTTP 429）はツール層において指数バックオフ（Exponential Backoff）で透過的にリトライし、それでも失敗した場合は事実に基づいたエラーを返すことでハルシネーションを防止します。"
            },
            {
                "key": "B",
                "text": "Instruct the model to invent realistic fictional temperatures whenever an error occurs",
                "verdict": "誤り。ハルシネーションを肯定するアンチパターンです。"
            },
            {
                "key": "C",
                "text": "Crash the entire Databricks workspace immediately",
                "verdict": "誤り。破壊的です。"
            },
            {
                "key": "D",
                "text": "Send 10,000 requests per millisecond to overwhelm the rate limiter",
                "verdict": "誤り。DoS攻撃となり完全にブロックされます。"
            }
        ],
        "correct": "A",
        "explanation": "ツール層での耐障害性とリトライ：一時的なレート制限（HTTP 429）やネットワーク瞬断は、LLMに直接エラーを見せる前に、ツール実行レイヤーで指数バックオフとジッター（Exponential Backoff with Jitter）を伴う自動リトライを行います。復旧不能な場合は明確なステータスを返し、モデルが嘘の数値をでっち上げるのを防ぎます。",
        "rules": [
            "Exponential Backoff & Jitter: ツール実行層で一時的障害（429/503）を透過的にリトライ",
            "真実性の維持: 復旧不能時は利用不可を明示し、捏造回答を防ぐ"
        ]
    },
    {
        "id": "Q50",
        "num": 50,
        "type": "mock",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool and Action Design with MCP",
        "title": "Q50: Secure Credential Management for Agent MCP Connections",
        "question": "An agent needs to connect to an external Salesforce instance via an MCP server. A junior engineer embeds the API client secret directly into the tool description inside the system prompt. Why is this a severe security violation, and what Databricks mechanism should be used?",
        "options": [
            {
                "key": "A",
                "text": "System prompts are logged in MLflow traces and visible in LLM outputs; credentials should instead be secured using Databricks Secrets and Unity Catalog Connection objects, injected strictly into the tool execution environment at runtime",
                "verdict": "正解！ プロンプトにシークレットを記載すると、MLflow トレースやユーザーへの回答生成で漏洩する致命的なリスクがあります。Databricks Secrets / Unity Catalog Connections を用い、ツールのバックエンド実行環境にのみセキュアに渡します。"
            },
            {
                "key": "B",
                "text": "Salesforce API keys only work when written in uppercase hexadecimal in the user message",
                "verdict": "誤り。事実無根です。"
            },
            {
                "key": "C",
                "text": "Secrets in prompts are safe as long as the model temperature is set below 0.2",
                "verdict": "誤り。温度とセキュリティは無関係です。"
            },
            {
                "key": "D",
                "text": "Embedding secrets in prompts is the recommended standard in Databricks documentation",
                "verdict": "誤り。重大なアンチパターンです。"
            }
        ],
        "correct": "A",
        "explanation": "ツールのシークレット管理（Credential Security）：プロンプト内に API キーやパスワードを絶対に含めてはなりません。推論ログ（MLflow Tracing）に平文で記録され、プロンプトインジェクション等で外部に漏洩します。認証情報は Databricks Secrets または Unity Catalog Connections で管理し、MCP ツールの実行コンテナ側でのみ環境変数として参照します。",
        "rules": [
            "プロンプトへのシークレット混入禁止: 漏洩リスク（Traceログ・モデル出力）が極めて高い",
            "Databricks Secrets / UC Connections: 実行時ツール環境へのセキュアな認証情報注入"
        ]
    },

    # --- DOMAIN 6: COMPRESSION & COMPACTION STRATEGIES (10 questions) ---
    {
        "id": "Q51",
        "num": 51,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q51: The Golden Rule of Compaction: 'Recall First, Precision Second'",
        "question": "An architect is evaluating a compaction prompt designed to summarize conversational history when the context window reaches 80% capacity. In initial testing, the compressed summary is beautifully concise, but downstream calculations fail because the user's initial constraint ('Exclude test accounts and filter by APAC region') was dropped from the summary. How should the compaction prompt be adjusted?",
        "options": [
            {
                "key": "A",
                "text": "Apply the 'Recall First, Precision Second' principle: instruct the compaction prompt to preserve 100% of user-defined constraints, negative filters, and critical entity identifiers before attempting any stylistic compression",
                "verdict": "正解！ コンパクションチューニングの絶対原則は「Recall First, Precision Second」です。まずは制約や除外ルール、確定IDを漏れなく確実に抽出し（Recall）、その後に冗長な言葉を削ります（Precision）。"
            },
            {
                "key": "B",
                "text": "Reduce the summary to a maximum of 20 tokens to force even higher precision",
                "verdict": "誤り。重要な前提がさらに失われます。"
            },
            {
                "key": "C",
                "text": "Abandon compaction and let the context window overflow to trigger an unhandled exception",
                "verdict": "誤り。システム障害を引き起こします。"
            },
            {
                "key": "D",
                "text": "Instruct the model that APAC region no longer exists",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "コンパクションの鉄則「Recall First, Precision Second」：コンテキスト圧縮において最も危険なのは、簡潔さを求めるあまり「ユーザーの前提条件」「除外ルール」「確定ID」を切り落としてしまうことです。まず必要な情報を100%取りこぼさない（Recall優先）プロンプト設計を行い、情報漏れがゼロであることを確認した上で、不要なノイズを削ぎ落とします。",
        "rules": [
            "Recall First, Precision Second: 制約条件・除外ルール・エンティティIDの完全抽出を最優先",
            "前提喪失の防止: 美しい要約よりも、ルールの正確な存続が命"
        ]
    },
    {
        "id": "Q52",
        "num": 52,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q52: Safe Purge Targets vs Mandatory Preserved State",
        "question": "When configuring an automated context compaction engine for long-horizon agent workflows, which category of elements is safe to permanently purge?",
        "options": [
            {
                "key": "A",
                "text": "The primary user goal and business constraints",
                "verdict": "誤り。絶対に保持しなければなりません。"
            },
            {
                "key": "B",
                "text": "Intermediate raw tool outputs that have already been synthesized, resolved error stack traces from retried failures, and conversational pleasantries",
                "verdict": "正解！ 既に集計・抽出が完了した中間の巨大な生JSONや、リトライによって解決済みのエラースタックトレース、挨拶などの雑談は、下流の推論に不要であるため安全に破棄（Purge）できます。"
            },
            {
                "key": "C",
                "text": "Resolved customer UUIDs and order tracking numbers",
                "verdict": "誤り。確定した識別子を消すと後続のDBクエリが実行できなくなります。"
            },
            {
                "key": "D",
                "text": "The system prompt's core safety directives",
                "verdict": "誤り。安全制約の破棄は重大事故につながります。"
            }
        ],
        "correct": "B",
        "explanation": "安全に破棄できるコンテキスト要素（Safe Purge Targets）：\n- **破棄して良いもの**: ①抽出完了後の生ツール出力（Raw JSON）、②リトライ済みの古いエラートレース、③挨拶や相槌などの会話フィラー。\n- **保持すべきもの**: ①ユーザーの最終ゴールと制約、②確定したエンティティID（CustomerID等）、③現在の完了ステータスと未完了タスク。",
        "rules": [
            "Safe Purge Targets: 完了済み生ログ、解決済みエラートレース、会話の挨拶",
            "Must Preserve: 目的、制約条件、確定ID、完了/未完了ステータス"
        ]
    },
    {
        "id": "Q53",
        "num": 53,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q53: Trimming (FIFO Sliding Window) vs Compaction Trade-offs",
        "question": "A developer replaces LLM-based compaction with a simple sliding window that drops the oldest 10 messages whenever token limits are approached (FIFO Trimming). Under which workflow will this approach consistently fail catastrophically?",
        "options": [
            {
                "key": "A",
                "text": "Single-turn FAQ retrieval where only the last question matters",
                "verdict": "誤り。単発QAでは影響は軽微です。"
            },
            {
                "key": "B",
                "text": "Multi-day analytical workflows where the foundational business constraints and target KPI definitions were stated in the very first user message",
                "verdict": "正解！ FIFOトリミングでは最も古いメッセージから順に消去されるため、最初のターンで定義された『大前提・ビジネス制約・分析目標』が最初に消滅し、エージェントの行動が破綻します。"
            },
            {
                "key": "C",
                "text": "Casual chat sessions with no factual requirements",
                "verdict": "誤り。雑談なら破綻しません。"
            },
            {
                "key": "D",
                "text": "Workflows where all context fits within 50 tokens",
                "verdict": "誤り。50トークンならそもそもトリミングされません。"
            }
        ],
        "correct": "B",
        "explanation": "Trimming（FIFO切り捨て）の致命的欠点：FIFO（先入れ先出し）で古いメッセージを削除すると、ユーザーが最初に提示した「全体ゴール」「守るべき制約」「対象年度や地域」などの根幹ルールが真っ先に失われます。長期タスクやビジネス分析では、単なる切り捨てではなく、初期の制約を保持して要約する「Compaction」が必須です。",
        "rules": [
            "FIFO Trimming のリスク: 最初に入力された最重要ルール・前提が真っ先に消去される",
            "長期ワークフロー: 初期の制約条件を蒸留・保存する Compaction が不可欠"
        ]
    },
    {
        "id": "Q54",
        "num": 54,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q54: Mitigating Recursive Compaction Information Decay (Telephone Game)",
        "question": "In a 50-turn workflow, context is compacted every 10 turns. By turn 45, the agent exhibits severe drift, misquoting original requirements. Analysis reveals that summarizing the previous summary 4 consecutive times caused subtle inaccuracies to compound (the 'Telephone Game' effect). How can this recursive degradation be mitigated?",
        "options": [
            {
                "key": "A",
                "text": "Anchor compaction against an immutable Canonical State Object: always reference the original immutable user prompt and persistent Lakebase state rather than daisy-chaining recursive lossy summaries",
                "verdict": "正解！ 要約の要約を繰り返す（Recursive Compaction）と伝言ゲームのように情報が歪みます。初期の不変プロンプトや Lakebase 上の単一の真実（Canonical State）を常にアンカーとして参照し、最新の差分のみを要約します。"
            },
            {
                "key": "B",
                "text": "Increase the frequency of compaction to every 2 turns",
                "verdict": "誤り。伝言ゲームのステップ数が増え、劣化がさらに加速します。"
            },
            {
                "key": "C",
                "text": "Switch to a model with zero context window",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "Instruct the model that summarizing causes no information loss",
                "verdict": "誤り。精神論では情報理論の損失は防げません。"
            }
        ],
        "correct": "A",
        "explanation": "再帰的要約による情報の劣化（Telephone Game Effect）：要約文をさらに要約することを繰り返すと、小さなニュアンスの欠落が累積し、最終的に前提が大きく変質します。対策として、最初のユーザー指示や Lakebase の状態オブジェクトを『不変のアンカー（Canonical State）』として常に保持し、要約対象を直近ターンの差分に限定します。",
        "rules": [
            "Canonical State Anchor: 初期の重要指示と確定状態を不変資産として固定する",
            "再帰的要約の回避: 『要約の要約』を重ねる伝言ゲームを構造的に防ぐ"
        ]
    },
    {
        "id": "Q55",
        "num": 55,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q55: Determining Token Capacity Thresholds for Compaction Triggers",
        "question": "At what context window utilization threshold should an agent proactively trigger compaction, and why?",
        "options": [
            {
                "key": "A",
                "text": "At 100% capacity, waiting until the model returns a context-length exceeded error",
                "verdict": "誤り。リクエストが例外で失敗し、ユーザー体験が破壊されます。"
            },
            {
                "key": "B",
                "text": "At 70% to 80% capacity, leaving sufficient headroom for the compaction prompt itself, tool generation outputs, and subsequent reasoning steps without hitting hard limits",
                "verdict": "正解！ コンパクション自体にもプロンプトと生成トークンを消費するため、70〜80%の容量に達した段階で予防的に発火させ、ヘッドルーム（余裕）を常に確保するのが標準的です。"
            },
            {
                "key": "C",
                "text": "At 5% capacity, compacting after every word",
                "verdict": "誤り。コストと遅延が膨大になります。"
            },
            {
                "key": "D",
                "text": "Only when the underlying Databricks workspace storage is 99% full",
                "verdict": "誤り。ストレージ容量とLLMのコンテキストウィンドウの混同です。"
            }
        ],
        "correct": "B",
        "explanation": "コンパクションのトリガー閾値：ハードリミット（100%）に到達してからでは、要約を生成するための出力トークン枠すらなくなり、APIエラーで強制終了します。一般的にコンテキストウィンドウの 70%〜80% に達した段階でプロアクティブに要約を発火させ、安全なマージン（Headroom）を確保します。",
        "rules": [
            "Trigger Threshold: コンテキスト消費量 70%〜80% でプロアクティブに発火",
            "ヘッドルーム確保: 要約処理自体のトークン枠と次ターンの推論枠を残す"
        ]
    },
    {
        "id": "Q56",
        "num": 56,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q56: Structured Schema Enforcement for Compacted Context",
        "question": "To ensure downstream agents can predictably consume a compacted context summary, how should the compaction output format be structured?",
        "options": [
            {
                "key": "A",
                "text": "As poetic prose with extensive metaphors",
                "verdict": "誤り。機械的な解釈が困難になります。"
            },
            {
                "key": "B",
                "text": "Using a strict structured schema (such as JSON or typed Markdown sections) with deterministic keys: `{original_goal, active_constraints, completed_steps, pending_subgoals, resolved_entities}`",
                "verdict": "正解！ 自由形式の文章ではなく、決定論的なキー（ゴール、制約、完了ステップ、保留タスク、確定エンティティ）を持つ構造化スキーマで要約を出力させることで、後続の推論での情報の欠落を機械的に防止できます。"
            },
            {
                "key": "C",
                "text": "As raw binary machine code",
                "verdict": "誤り。LLMが理解できません。"
            },
            {
                "key": "D",
                "text": "Leaving it empty to save tokens",
                "verdict": "誤り。文脈が全消去されます。"
            }
        ],
        "correct": "B",
        "explanation": "構造化コンパクションスキーマ（Structured Compaction Schema）：コンパクションの出力を自由形式の自然言語に任せると、重要な変数が省かれがちです。`original_goal`（目標）、`active_constraints`（制約）、`completed_steps`（完了済み）、`pending_tasks`（未完了）、`resolved_entities`（確定ID）といった明確なキーを持つ構造化フォーマットを強制するのが最も堅牢です。",
        "rules": [
            "Structured Compaction: 定型スキーマ（ゴール・制約・確定エンティティ等）で要約を出力",
            "機械的検証: 下流エージェントが決定論的に文脈を復元できるようにする"
        ]
    },
    {
        "id": "Q57",
        "num": 57,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q57: Automated Assertion Checks on Compacted Output",
        "question": "A production context pipeline compacts customer interaction traces. Before replacing the active history with the new summary, what automated assertion check should the context engineering layer perform?",
        "options": [
            {
                "key": "A",
                "text": "An entity preservation assertion: verify programmatically that critical identifiers (e.g., OrderIDs, CustomerIDs) and negative constraints present in the pre-compaction state exist in the compacted text",
                "verdict": "正解！ 要約適用前に、元の会話に存在した重要なID（OrderID等）や否定制約が要約後にも残っているかを正規表現やアサーションで自動検証し、欠落していた場合はコンパクションをリトライまたはロールバックします。"
            },
            {
                "key": "B",
                "text": "Check that the compacted summary is exactly 10,000 words long",
                "verdict": "誤り。圧縮になっていません。"
            },
            {
                "key": "C",
                "text": "Verify that all vowels have been removed from the text",
                "verdict": "誤り。意味不明です。"
            },
            {
                "key": "D",
                "text": "Ensure the summary contains no punctuation whatsoever",
                "verdict": "誤り。不適切なアサーションです。"
            }
        ],
        "correct": "A",
        "explanation": "コンパクションの自動アサーション検証（Compaction Assertion Checks）：要約によって重要な注文IDや制約条件が欠落していないかをプログラムで自動検証（Entity Preservation Check）します。確定エンティティのリストが要約に含まれていることを確認してからコンテキストを置き換えることで、情報のサイレントロストを防ぎます。",
        "rules": [
            "Entity Preservation Assertion: 要約後に重要IDや制約が残っているかをコードで検証",
            "サイレントロスト防止: 検証失敗時は再要約またはフォールバックを行う"
        ]
    },
    {
        "id": "Q58",
        "num": 58,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q58: Handling Multi-Turn Constraint Updates in Compaction",
        "question": "In turn 1, a user specifies: 'Only analyze European transactions.' In turn 12, the user updates: 'Change of plans: include North America as well, but exclude Canada.' How should the compaction module handle constraint mutations?",
        "options": [
            {
                "key": "A",
                "text": "Apply state reconciliation: maintain an explicit 'Active Constraints' ledger that records the latest mutated state ('Europe + US, excluding Canada'), explicitly noting the override of earlier constraints to prevent Context Clash",
                "verdict": "正解！ ユーザーの制約変更（Constraint Mutation）に対しては、要約台帳（Active Constraints Ledger）上で最新の確定ルールに上書き更新し、古いルールとの衝突（Context Clash）を解消して保持します。"
            },
            {
                "key": "B",
                "text": "Keep only turn 1 and completely ignore turn 12",
                "verdict": "誤り。ユーザーの最新指示を無視することになります。"
            },
            {
                "key": "C",
                "text": "Keep both conflicting statements simultaneously without reconciliation",
                "verdict": "誤り。Context Clash を引き起こします。"
            },
            {
                "key": "D",
                "text": "Ban the user from modifying requirements",
                "verdict": "誤り。対話型システムの要件を満たしません。"
            }
        ],
        "correct": "A",
        "explanation": "制約の変更とコンパクション（Constraint Reconciliation）：長期対話では途中で要件が変更・追加されることが日常茶飯事です。コンパクションモジュールは、過去の古い制約と最新の指示を調停（Reconcile）し、現在有効な『アクティブ制約リスト』として一本化して要約に記載することで、新旧指示の衝突（Context Clash）を防ぎます。",
        "rules": [
            "Constraint Reconciliation: ユーザーによる要件の変更を検知し、最新の有効制約に調停",
            "Context Clash 防止: 古いルールと新しいルールの併存による混乱を排除"
        ]
    },
    {
        "id": "Q59",
        "num": 59,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q59: Semantic Deduplication in Long Conversational Histories",
        "question": "An agent repeats similar status check queries across 15 turns. The transcript contains 15 nearly identical messages: 'Checking database... Status is still in progress.' How should semantic deduplication be applied during context compression?",
        "options": [
            {
                "key": "A",
                "text": "Collapse repetitive polling loops into a single statement: 'Poll attempts 1-15: status remained IN_PROGRESS between 14:00 and 14:15 UTC; last check at 14:15 UTC confirmed ready'",
                "verdict": "正解！ 繰り返されたポーリングやステータス確認ログは、個々のターンを保持するのではなく、期間と最終結果を示す単一の記述に集約（Collapse）することで、大量のトークンを安全に削減できます。"
            },
            {
                "key": "B",
                "text": "Repeat each of the 15 messages 3 additional times",
                "verdict": "誤り。トークン浪費です。"
            },
            {
                "key": "C",
                "text": "Delete the entire conversation history and start an unrelated task",
                "verdict": "誤り。タスク破綻です。"
            },
            {
                "key": "D",
                "text": "Convert the polling messages into high-resolution PNG images",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "意味的重複排除（Semantic Deduplication）：ループ処理や定期ポーリングで発生した同一内容の反復メッセージ群は、1件ずつ記録する価値がありません。『試行1〜15回：状態は進行中のままであったが14:15に完了』のように1行に折りたたむ（Collapse）ことで、推論価値を損なわずに劇的なトークン削減を達成します。",
        "rules": [
            "Polling Collapse: 反復的なステータス確認ログを1行の概要に統合",
            "トークン大幅削減: 無駄な同一パターンの繰り返しを排除"
        ]
    },
    {
        "id": "Q60",
        "num": 60,
        "type": "mock",
        "domain": "Domain 6: Compression & Compaction",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "Q60: Prompt-Aware Chunk Compaction vs Blind String Truncation",
        "question": "A developer writes a custom Python script that truncates any message exceeding 2,000 characters by slicing `text[:2000]`. During an agent run, an SQL query `SELECT * FROM tbl WHERE status = 'ACTIVE' AND account_id = 'A991'` is sliced into `SELECT * FROM tbl WHERE status = 'ACT`. The query fails with a syntax error. What is the fundamental flaw of blind string truncation?",
        "options": [
            {
                "key": "A",
                "text": "Blind character/token slicing disregards semantic boundaries and code syntax, producing broken tokens and corrupt payloads; compaction must be structure-aware and validate syntactic completeness",
                "verdict": "正解！ 単純な文字数・トークン数による機械的スライス（Blind Truncation）は、SQLやJSONなどの構文境界を無視して途中で切断するため、構文エラーやデータの破損を確実に引き起こします。"
            },
            {
                "key": "B",
                "text": "2,000 characters is too large for Python strings to handle in memory",
                "verdict": "誤り。Pythonのメモリ管理とは無関係です。"
            },
            {
                "key": "C",
                "text": "SQL queries cannot be executed on Databricks if they contain the letter 'A'",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "The script should have sliced at character 5 instead",
                "verdict": "誤り。さらに壊れます。"
            }
        ],
        "correct": "A",
        "explanation": "構文を無視した単純スライス（Blind String Truncation）の危険性：文字数やトークン数で機械的に `text[:N]` とぶった切ると、SQLのクォート閉じ忘れ、JSONの括弧不整合、引数の切断などが発生し、次ステップの実行が即座にクラッシュします。コンテキストの圧縮やトリミングは、構文木やメッセージ単位を意識した構造認識型（Structure-aware）でなければなりません。",
        "rules": [
            "Blind Truncation の禁止: 文字数スライスはコードやJSONの構文破壊を招く",
            "Structure-aware Compaction: 構文境界（メッセージ単位・ブロック単位）を保って圧縮する"
        ]
    },

    # --- DOMAIN 7: MULTI-AGENT SYSTEMS & LONG-HORIZON TASKS (10 questions) ---
    {
        "id": "Q61",
        "num": 61,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q61: Preventing Parent Trace Leakage to Subagents",
        "question": "An orchestrator agent that has accumulated 18 turns of reasoning trace launches a specialized subagent to validate the syntax of a specific SQL query. How should the orchestrator construct the context payload for the subagent?",
        "options": [
            {
                "key": "A",
                "text": "Pass its own entire 18-turn conversational history and all previous tool outputs to the subagent",
                "verdict": "誤り。子のコンテキストが即座に飽和し、Context Distraction を招きます。"
            },
            {
                "key": "B",
                "text": "Isolate the subagent's context: pass only the specific task objective, the target SQL string, and relevant table schemas, shielding the subagent from the parent's unneeded historical traces",
                "verdict": "正解！ 親エージェントの全履歴を子に垂れ流す（Trace Leakage）のを防ぎ、サブタスク達成に必要なパラメータと対象データのみを切り出して渡すのがマルチエージェントの鉄則です。"
            },
            {
                "key": "C",
                "text": "Provide no instructions and let the subagent guess the SQL query",
                "verdict": "誤り。タスクが成立しません。"
            },
            {
                "key": "D",
                "text": "Serialize the orchestrator's RAM into a disk image and mount it on the subagent",
                "verdict": "誤り。不適切なアーキテクチャです。"
            }
        ],
        "correct": "B",
        "explanation": "親トレース漏洩の防止（Parent Trace Leakage Prevention）：サブエージェントに親の全思考ログや無関係な過去ツール履歴をそのまま渡すと、子のコンテキストウィンドウが初期から圧迫され、注意散漫（Context Distraction）を引き起こします。サブエージェントには、その専門タスクに必要な入力データと指示のみを厳密にスコープ分離して渡す必要があります。",
        "rules": [
            "Trace Leakage 防止: 親の雑多な思考ログを子エージェントに伝播させない",
            "スコープ分離: サブタスクに必要な最小限の指示とペイロードのみを切り出して渡す"
        ]
    },
    {
        "id": "Q62",
        "num": 62,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q62: Preventing Orchestrator Context Saturation via Delta Lake References",
        "question": "A worker subagent completes an extensive log analysis scanning 2 million records, producing a 45 MB structured result dataset. The worker needs to report back to the parent orchestrator agent. How should this data transfer be architected to prevent orchestrator context saturation?",
        "options": [
            {
                "key": "A",
                "text": "Write the 45 MB dataset to a managed Unity Catalog Delta table, and return only a high-level summary and the Delta table URI pointer to the parent orchestrator",
                "verdict": "正解！ 大規模な分析結果はストレージ（Delta Lake）に退避させ、エージェント間の通信は『軽量なサマリー ＋ Delta テーブルのURIポインタ』にとどめることで、オーケストレーターのコンテキスト飽和（Saturation）を防止します。"
            },
            {
                "key": "B",
                "text": "Paste all 45 MB of text directly into the return message string",
                "verdict": "誤り。オーケストレーターのコンテキスト上限を瞬時にオーバーフローさせます。"
            },
            {
                "key": "C",
                "text": "Split the 45 MB into 10,000 separate user messages sent in rapid succession",
                "verdict": "誤り。オーケストレーターがパンクします。"
            },
            {
                "key": "D",
                "text": "Discard the 45 MB without saving and tell the orchestrator everything looked good",
                "verdict": "誤り。データ喪失です。"
            }
        ],
        "correct": "A",
        "explanation": "オーケストレーターのコンテキスト飽和防止（Context Saturation Prevention）：マルチエージェントシステムにおいて、サブエージェントが重い生データ（数MB〜数GB）をメッセージ本文で親に返信すると、親のコンテキストは即座に枯渇・クラッシュします。データの実体は Unity Catalog の Delta テーブルに書き出し、親には『構造化サマリー ＋ Delta URI ポインタ』のみを返す参照渡し（Pass-by-Reference）パターンを採用します。",
        "rules": [
            "Pass-by-Reference パターン: 実データは Delta Lake に保存し、URIポインタを親に返す",
            "Orchestrator Saturation 回避: 親のコンテキストを軽量サマリーに保ち、全体統制に専念させる"
        ]
    },
    {
        "id": "Q63",
        "num": 63,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q63: Agent Boundary Placement Trade-Offs",
        "question": "A team is designing a multi-agent workflow. An architect proposes decomposing a customer service workflow into 20 micro-subagents (e.g., GreetingAgent, NameExtractorAgent, OrderLookupAgent, AddressVerifierAgent, etc.). What is the primary operational penalty of excessively fine-grained agent boundaries?",
        "options": [
            {
                "key": "A",
                "text": "Compounding handoff overhead, latency inflation from inter-agent context serialization, and loss of conversational coherence across micro-boundaries",
                "verdict": "正解！ エージェントの境界を細かく刻みすぎると、エージェント間の引継ぎ（Handoff）に伴う要約・通信オーバーヘッドとレイテンシが爆発し、伝言ゲームのように一貫性が低下します。"
            },
            {
                "key": "B",
                "text": "Unity Catalog will refuse to create more than 3 agents per workspace",
                "verdict": "誤り。Unity Catalog にそのような制限はありません。"
            },
            {
                "key": "C",
                "text": "The token consumption drops to zero, triggering billing alerts",
                "verdict": "誤り。通信オーバーヘッドでむしろトークンは増加します。"
            },
            {
                "key": "D",
                "text": "Micro-agents are only supported in C++, not Python",
                "verdict": "誤り。無関係です。"
            }
        ],
        "correct": "A",
        "explanation": "エージェント境界の設計（Boundary Placement）：エージェントの分割粒度が粗すぎると単一エージェントのコンテキストがパンクしますが、逆に細かすぎる『マイクロエージェント構成』にすると、エージェント間のハンドオフ（引継ぎ処理、コンテキストのシリアライズ、通信往復）によるレイテンシとオーバーヘッドが激増し、全体の一貫性が劣化します。凝集度の高い責務ごとに適度な粒度で分割するのがベストプラクティスです。",
        "rules": [
            "細かすぎる境界の弊害: ハンドオフオーバーヘッド、通信遅延、文脈の劣化",
            "粗すぎる境界の弊害: 単一エージェントのコンテキスト飽和とアテンション分散"
        ]
    },
    {
        "id": "Q64",
        "num": 64,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q64: Stateful Checkpointing for Long-Horizon Workflows",
        "question": "An enterprise ETL agent executes a pipeline across 8 sequential stages on Databricks. Stage 5 encounters a transient network timeout connecting to an external REST endpoint. Which architectural pattern ensures the agent resumes from stage 5 rather than restarting from stage 1?",
        "options": [
            {
                "key": "A",
                "text": "Persist intermediate step artifacts, state variables, and execution status into a Delta-backed State table at the completion of each stage (Stateful Checkpointing)",
                "verdict": "正解！ 各ステージ完了時に Delta テーブルへ状態をコミットする「Stateful Checkpointing」を実装することで、障害発生時に最後の成功ステージからシームレスに再開（Resume）できます。"
            },
            {
                "key": "B",
                "text": "Keep all intermediate progress in the driver node's temporary RAM disk",
                "verdict": "誤り。クラスタ障害時にデータが失われます。"
            },
            {
                "key": "C",
                "text": "Disable error raising in Python so the agent ignores failures and declares success",
                "verdict": "誤り。重大なデータ不整合を招きます。"
            },
            {
                "key": "D",
                "text": "Instruct the model in natural language: 'Please never crash'",
                "verdict": "誤り。耐障害性になりません。"
            }
        ],
        "correct": "A",
        "explanation": "長期タスクのステートフルチェックポインティング（Stateful Checkpointing）：多段階の長期ワークフローでは、途中の障害（APIタイムアウト、クラスタ再起動）で最初からやり直すコストを避けるため、ステージ完了ごとに状態（中間成果物、完了フラグ、コンテキスト要約）を Delta テーブルに永続化します。リカバリ時はそのテーブルを照会し、未完了のステージから安全に再開します。",
        "rules": [
            "Stateful Checkpointing: ステージごとに状態をDeltaテーブルへコミット",
            "耐障害性（Fault Tolerance）: 障害発生時の途中再開を可能にし、計算コストを保護"
        ]
    },
    {
        "id": "Q65",
        "num": 65,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q65: Asynchronous Subagent Execution and Barrier Synchronization",
        "question": "An orchestrator needs to collect competitor intelligence across 5 different websites simultaneously. How should the execution and context joining be structured?",
        "options": [
            {
                "key": "A",
                "text": "Launch 5 subagent tasks asynchronously in parallel, wait at a barrier synchronization checkpoint until all tasks report completion to their Delta state tables, and aggregate the structured summaries into the orchestrator context",
                "verdict": "正解！ 独立した情報収集タスクは非同期・並列（Asynchronous Parallel）にサブエージェントをディスパッチし、同期バリア（Barrier Synchronization）で全タスクの完了を待ってから結果を集約するのが最も低遅延で効率的です。"
            },
            {
                "key": "B",
                "text": "Run all 5 tasks sequentially on a single thread with a 5-minute pause between each",
                "verdict": "誤り。レイテンシが不必要に長くなります。"
            },
            {
                "key": "C",
                "text": "Combine all 5 websites into one URL and query it once",
                "verdict": "誤り。無効なURLになります。"
            },
            {
                "key": "D",
                "text": "Prompt the model to imagine what the competitors would say without browsing",
                "verdict": "誤り。ハルシネーションです。"
            }
        ],
        "correct": "A",
        "explanation": "非同期サブエージェント実行とバリア同期（Barrier Synchronization）：独立したサブタスク群（5つの競合サイト調査など）は、並列にサブエージェントをディスパッチして同時に実行します。オーケストレーターは同期バリアで待機し、全サブエージェントが Delta 状態テーブルに結果をコミットした段階で、サマリーを一括集約して最終回答を作成します。",
        "rules": [
            "Asynchronous Parallel Execution: 独立タスクを並列ディスパッチしてレイテンシ短縮",
            "Barrier Synchronization: 全サブエージェントの完了を待ってから親コンテキストに統合"
        ]
    },
    {
        "id": "Q66",
        "num": 66,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q66: Standardized Context Handoff Protocols Between Peer Agents",
        "question": "In a peer-to-peer multi-agent system (Triage Agent -> Specialist Agent -> Fulfillment Agent), conversational context degrades as each agent hands off to the next. What protocol ensures context fidelity during handoffs?",
        "options": [
            {
                "key": "A",
                "text": "A standardized Context Handoff Envelope containing: `{origin_agent, target_agent, canonical_intent, customer_entity_state, unfulfilled_requirements, audit_trace_id}`",
                "verdict": "正解！ ピアエージェント間での引き継ぎには、発信元、対象、意図、顧客状態、未達成要件、監査IDなどを規定した「標準化ハンドオフエンベロープ（Handoff Envelope）」を使用し、伝言ゲームによる情報劣化を防ぎます。"
            },
            {
                "key": "B",
                "text": "Passing an empty string and forcing the next agent to query the user from scratch",
                "verdict": "誤り。ユーザー体験を破壊します。"
            },
            {
                "key": "C",
                "text": "Writing the context on a physical whiteboard in the office",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "Having the agents speak to each other via acoustic audio tones over speakerphones",
                "verdict": "誤り。意味不明です。"
            }
        ],
        "correct": "A",
        "explanation": "標準化ハンドオフプロトコル（Standardized Handoff Protocol）：エージェント間でタスクを引き継ぐ際、自由な雑談テキストで渡すと必要事項が抜け落ちます。送信元、受信先、確定した意図、顧客の属性状態、残タスク、監査IDを構造化した「ハンドオフエンベロープ（Handoff Envelope）」を規約化することで、文脈の正確な伝達（Context Fidelity）を担保します。",
        "rules": [
            "Handoff Envelope: 意図・状態・未完了要件を標準フォーマットでピアエージェントに引継ぎ",
            "Context Fidelity: 引き継ぎ時の情報の脱落や伝言ゲームを防止"
        ]
    },
    {
        "id": "Q67",
        "num": 67,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q67: Detecting Deadlocks and Circular Delegation Loops",
        "question": "Agent A delegates a complex question to Agent B. Agent B decides it lacks permission and delegates back to Agent A. Agent A receives it as a new request and delegates back to Agent B, creating an infinite circular delegation loop that burns thousands of dollars in tokens. What mechanism must be implemented?",
        "options": [
            {
                "key": "A",
                "text": "A hop counter and trace call-stack inside the handoff metadata: enforce a maximum recursion depth (e.g., max 3 hops) and detect cycle patterns in agent delegation, throwing a controlled fallback if a loop occurs",
                "verdict": "正解！ 循環委譲ループ（Circular Delegation）を防ぐには、ハンドオフメタデータに呼び出しスタック（Call Stack）とホップ数カウンター（Hop Counter）を保持し、上限（例: 3ホップ）を超えた場合に自動検知してフォールバックします。"
            },
            {
                "key": "B",
                "text": "Instruct Agent A that Agent B does not exist",
                "verdict": "誤り。協調動作そのものが破綻します。"
            },
            {
                "key": "C",
                "text": "Let the loop run indefinitely because models will eventually get bored",
                "verdict": "誤り。LLMは飽きることなく無限にトークンを浪費し続けます。"
            },
            {
                "key": "D",
                "text": "Reduce the token price in Databricks settings",
                "verdict": "誤り。技術的に不可能です。"
            }
        ],
        "correct": "A",
        "explanation": "循環委譲ループ（Circular Delegation / Deadlock）の防止：マルチエージェント協調では、エージェント同士がお互いにタスクを押し付け合う無限ループのリスクがあります。メタデータにホップ数（Max Hops）と委譲経路（Delegation History / Call Stack）を記録し、同一エージェントへの循環を検知した時点で実行をインターセプトして人間にエスカレーションします。",
        "rules": [
            "Hop Counter & Call Stack: 委譲深度の上限（Max Hops）と循環検知を実装",
            "無限ループ防止: トークン暴走とデッドロックを未然に防ぐガードレール"
        ]
    },
    {
        "id": "Q68",
        "num": 68,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q68: Human-in-the-Loop (HITL) Interruption and State Pausing",
        "question": "A fraud remediation agent prepares to execute an irreversible asset freeze on a suspicious account. The system architecture mandates human compliance officer review before execution. How should the multi-agent system handle this pause in execution?",
        "options": [
            {
                "key": "A",
                "text": "Keep the LLM reasoning thread in a busy-waiting `while True: sleep(1)` loop on an active GPU node",
                "verdict": "誤り。GPUリソースとコストの莫大な無駄遣いです。"
            },
            {
                "key": "B",
                "text": "Persist the complete workflow state and pending action payload to a Delta Lake state table with status 'AWAITING_HUMAN_APPROVAL', release compute resources, and resume upon receiving an approval callback webhook",
                "verdict": "正解！ 人間のレビュー待ちは数時間〜数日に及ぶ可能性があるため、状態をDeltaテーブルに保存してコンピュートを解放（Pause）し、Webhookや承認イベントをトリガーに復帰（Resume）させるのがクラウド標準のアーキテクチャです。"
            },
            {
                "key": "C",
                "text": "Bypass human review and freeze the assets anyway",
                "verdict": "誤り。コンプライアンス違反です。"
            },
            {
                "key": "D",
                "text": "Terminate the entire company database",
                "verdict": "誤り。論外です。"
            }
        ],
        "correct": "B",
        "explanation": "Human-in-the-Loop (HITL) による状態一時停止と復帰：人間の承認待ちは数分で終わることもあれば数日かかることもあります。この間コンピュートを稼働させ続けるのは非効率です。状態を Delta テーブルに `AWAITING_APPROVAL` として保存してプロセスを終了し、承認 webhook が届いた時点でステートフルに再開します。",
        "rules": [
            "HITL State Pausing: 承認待ち状態をDeltaに永続化し、コンピュートリソースを解放",
            "イベント駆動復帰: Webhookや承認シグナルを受けてチェックポイントから安全に再開"
        ]
    },
    {
        "id": "Q69",
        "num": 69,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q69: Shared Global State vs Local Message Passing",
        "question": "When designing a collaborative multi-agent system on Databricks involving 6 specialized agents, what is the architectural risk of relying exclusively on a shared, unpartitioned global context blackboard without local agent scoping?",
        "options": [
            {
                "key": "A",
                "text": "Rapid context explosion, race conditions on shared memory keys, and massive Context Distraction as every agent's intermediate chatter floods every other agent's prompt",
                "verdict": "正解！ 共有黒板（Shared Global Blackboard）に全エージェントの全出力を集約すると、コンテキストが瞬時に爆発し、他エージェントの無関係な雑談による注意散漫（Context Distraction）や状態の競合が発生します。"
            },
            {
                "key": "B",
                "text": "Delta Lake will automatically shut down",
                "verdict": "誤り。Delta Lakeの挙動とは無関係です。"
            },
            {
                "key": "C",
                "text": "The models will become conscious and resign",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "Python packages cannot be loaded in multi-agent environments",
                "verdict": "誤り。事実に反します。"
            }
        ],
        "correct": "A",
        "explanation": "共有黒板（Shared Global State）の落とし穴：全員が同じコンテキスト空間に書き込む設計は、エージェント数が増えると急激に破綻します。各エージェントの推論トレースが他の全エージェントのコンテキストを圧迫し、深刻な Context Distraction を引き起こします。ローカルメッセージパッシング（限定されたスコープ）と構造化された状態管理を併用するのが鉄則です。",
        "rules": [
            "共有黒板の危険性: 全員が同じプロンプトに相乗りすると瞬時にコンテキストが飽和する",
            "局所的メッセージング: 各エージェントには必要な情報のみを個別に届ける"
        ]
    },
    {
        "id": "Q70",
        "num": 70,
        "type": "mock",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "Q70: Auditability and Lineage in Multi-Agent Execution Chains",
        "question": "A regulated financial institution requires end-to-end auditability of decisions made by a 4-agent credit evaluation pipeline. How does MLflow 3 Tracing fulfill this governance mandate?",
        "options": [
            {
                "key": "A",
                "text": "MLflow 3 automatically captures hierarchical span graphs recording exact inputs, outputs, prompts, tool executions, and latency metrics across the entire multi-agent call tree, linked by a unified root trace ID",
                "verdict": "正解！ MLflow 3 Tracing は、親オーケストレーターから子エージェント、個々のツール実行に至るまでの全ステップを階層的な Span グラフとして自動記録し、単一の Root Trace ID で紐付けて完全な監査性を実現します。"
            },
            {
                "key": "B",
                "text": "MLflow 3 takes physical screenshots of the computer monitor and saves them as BMP files",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "C",
                "text": "MLflow 3 deletes all traces immediately after execution to maintain secrecy",
                "verdict": "誤り。監査性の目的に反します。"
            },
            {
                "key": "D",
                "text": "MLflow only supports logging single numbers, not multi-agent calls",
                "verdict": "誤り。MLflow 3 はエージェントの階層的トレースに完全対応しています。"
            }
        ],
        "correct": "A",
        "explanation": "MLflow 3 によるマルチエージェントの監査性と系統管理（Auditability & Lineage）：複雑なマルチエージェントシステムでは、誰が・どのプロンプトで・どのツールを呼び・なぜその結論を出したのかを追跡できなければ規制要件をクリアできません。MLflow 3 Tracing は、階層的なスパングラフ（Span Graph）により、親エージェントから子エージェントのツール呼び出しまでの全経路を同一の Trace ID で完全に可視化・監査可能にします。",
        "rules": [
            "MLflow 3 Tracing: エージェントの全推論・ツール呼出を階層的 Span グラフで可視化",
            "Root Trace ID: 分散したマルチエージェントの意思決定プロセスを一元的に監査追跡可能にする"
        ]
    }
]

print(f"Loaded {len(D567_QUESTIONS)} questions for Domains 5, 6, 7.")
