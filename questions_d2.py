# questions_d2.py
# Domain 2: System Prompt and Instruction Design & Genie Spaces (10 questions)

D2_QUESTIONS = [
    {
        "id": "Q11",
        "num": 11,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q11: Genie Space Precision Improvement via Trusted Assets",
        "question": "A finance team deploys a Databricks AI/BI Genie Space. When executives ask, 'What was our net MRR growth in Q3?', Genie generates an ad-hoc SQL query that performs a basic sum on the `billing` table, completely missing critical business rules for multi-currency conversions and promo discounts. How should the context engineer permanently improve Genie's response quality while minimizing token usage?",
        "options": [
            {
                "key": "A",
                "text": "Write a 60-line raw SQL query example directly inside the Genie Space text instructions",
                "verdict": "誤り。プロンプト内の長大な生SQLはトークンを圧迫し、モデルが毎回正確に再現できる保証もありません。"
            },
            {
                "key": "B",
                "text": "Encapsulate the verified net MRR logic into a Unity Catalog View or SQL UDF and register it as a 'Trusted Asset' in the Genie Space",
                "verdict": "正解！ 複雑なビジネス計算はプロンプトで長々と説明するのではなく、Unity Catalog 上で検証済みのビューや関数を作成し、Genie の「Trusted Asset」として登録するのが公式推奨のベストプラクティスです。"
            },
            {
                "key": "C",
                "text": "Add 50 variations of sample questions with identical text to the Genie Space",
                "verdict": "誤り。サンプル質問の乱発はトークンを浪費し、メンテナンス性を悪化させます。"
            },
            {
                "key": "D",
                "text": "Copy the SQL calculation into the comments of every column in the billing table",
                "verdict": "誤り。カラムコメントの肥大化を招き、実行の強制力も弱いです。"
            }
        ],
        "correct": "B",
        "explanation": "Genie Space のベストプラクティス：複雑・厳密なビジネス指標（MRR、解約率など）は、LLMに毎回アドホックなSQLを一から生成させるのではなく、Unity Catalog 内でガバナンスされた「集計ビュー」や「SQL UDF」として実装し、Genie の Trusted Asset（信頼できる資産）として紐付けます。これによりトークン消費を最小化し、ハルシネーションを確実に防止できます。",
        "rules": [
            "Genie Trusted Assets: 複雑なビジネスロジックはプロンプトではなく、UC View や SQL UDF として登録する",
            "メリット: トークン消費削減、100% 決定論的で監査可能な集計結果の担保"
        ]
    },
    {
        "id": "Q12",
        "num": 12,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q12: Marginal Contribution Principle in Few-Shot Selection",
        "question": "A context engineer is selecting few-shot examples for an agent system prompt. The model has a strict 4,000-token budget for instructions. The team has 12 potential candidate examples. Which selection strategy best adheres to the 'Marginal Contribution' principle?",
        "options": [
            {
                "key": "A",
                "text": "Include all 12 candidate examples by truncating their descriptions to 5 words each",
                "verdict": "誤り。必要な文脈が切り捨てられ、役に立たないノイズになります。"
            },
            {
                "key": "B",
                "text": "Select 2 to 3 highly diverse examples that demonstrate edge cases: one with missing parameters, one requiring a complex multi-tool path, and one with strict JSON schema constraints",
                "verdict": "正解！ Few-shotの選定基準は「限界貢献度（Marginal Contribution）」の最大化です。定型的な成功例を並べるのではなく、モデルが誤りやすいエッジケースや厳格な出力構造を示す少数の精鋭例に絞ります。"
            },
            {
                "key": "C",
                "text": "Select 10 standard, repetitive success cases to maximize model confidence",
                "verdict": "誤り。類似した標準ケースを並べても限界効用はほぼゼロであり、トークンバジェットを浪費します。"
            },
            {
                "key": "D",
                "text": "Eliminate all few-shot examples completely, as zero-shot is always cheaper and superior",
                "verdict": "誤り。エッジケースの誘導には適切なFew-shotが極めて有効です。"
            }
        ],
        "correct": "B",
        "explanation": "Few-shotサンプルの選定原則「Marginal Contribution（限界貢献度）」：すでにモデルがゼロショットで解ける定型例をいくら追加しても精度は向上しません。①ツールの失敗時フォールバック、②曖昧入力への確認、③厳格な構造化JSON出力など、モデルが自力で判断に迷いやすいエッジケースを厳選して2〜3例に絞り込むことで、最小のトークンで最大の効果を得ます。",
        "rules": [
            "Few-shot Selection: 標準例を並べるのではなく、エッジケース・厳格フォーマットに特化した2〜3例に絞る",
            "Marginal Contribution: トークン消費に対する追加的な精度向上価値を最大化する"
        ]
    },
    {
        "id": "Q13",
        "num": 13,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q13: Calibrating Over-Tooling and Stopping Criteria",
        "question": "An operational agent frequently enters endless loops, calling search tools 15 times for a single simple query, resulting in high latency and API throttling. An analysis of the system prompt shows it instructs: 'Search extensively until you are completely confident you have found everything.' How should this prompt be calibrated?",
        "options": [
            {
                "key": "A",
                "text": "Add: 'Be even more confident before stopping'",
                "verdict": "誤り。さらにループが悪化します。"
            },
            {
                "key": "B",
                "text": "Calibrate the prompt with explicit stopping criteria: specify a maximum of 2 search attempts, define an 'acceptable evidence threshold', and instruct the agent to ask clarifying questions if confidence remains low",
                "verdict": "正解！ 曖昧な定性的指示（'completely confident'）を排除し、明確な停止条件（最大試行回数、十分性の基準、聞き返しフォールバック）を明記することで過剰なツール呼出（Over-tooling）を防止します。"
            },
            {
                "key": "C",
                "text": "Revoke the agent's access to all search tools and force it to guess",
                "verdict": "誤り。ハルシネーションの原因になります。"
            },
            {
                "key": "D",
                "text": "Increase the model's top-p parameter to 1.0",
                "verdict": "誤り。出力のランダム性が増すだけでループは解消しません。"
            }
        ],
        "correct": "B",
        "explanation": "プロンプトのキャリブレーション不良（Poorly Calibrated Prompt）：『納得するまで徹底的に検索せよ』のようなオープンエンドな指示は、過剰なツール呼出（Over-tooling）や無限ループを引き起こします。対策として、①最大ツール実行回数（Max 2 calls）、②明確な停止基準（Sufficient criteria）、③確信度が低い場合の聞き返しプロトコルをプロンプトに定義します。",
        "rules": [
            "Prompt Calibration: 曖昧な表現を排し、明確な終了条件（Stopping Criteria）を定義する",
            "Over-tooling防止: 最大呼び出し回数と代替フォールバック行動を明示する"
        ]
    },
    {
        "id": "Q14",
        "num": 14,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q14: Evaluating Cost-Accuracy Trade-Offs in MLflow 3",
        "question": "A team uses MLflow 3 Experiment Tracking to compare two prompt variations: Prompt A (compact, 800 tokens) achieves 91% accuracy at $0.008 per request; Prompt B (verbose, 3,200 tokens with 8 few-shot examples) achieves 92% accuracy at $0.032 per request. Scaling to 100,000 requests per day, what is the architecturally sound recommendation?",
        "options": [
            {
                "key": "A",
                "text": "Deploy Prompt B immediately because production systems must always maximize raw benchmark accuracy regardless of cost",
                "verdict": "誤り。1%の精度のために4倍（日額数千ドル）のコスト増は正当化できません。"
            },
            {
                "key": "B",
                "text": "Deploy Prompt A, and use MLflow traces to inspect the 9% failure cases, addressing them via targeted Unity Catalog metadata annotations or tool parameter validation rather than prompt bloating",
                "verdict": "正解！ 費用対効果を評価し、プロンプトの肥大化ではなくメタデータ改善やツール側でのガードレールによって効率的に精度を底上げします。"
            },
            {
                "key": "C",
                "text": "Abandon both prompts and train a custom foundation model from scratch on Databricks GPU clusters",
                "verdict": "誤り。過剰投資であり非現実的です。"
            },
            {
                "key": "D",
                "text": "Deploy Prompt B on weekdays and Prompt A on weekends",
                "verdict": "誤り。論理的なエンジニアリング判断ではありません。"
            }
        ],
        "correct": "B",
        "explanation": "MLflow 3 実験追跡によるコスト・性能トレードオフ評価：プロンプトを4倍に肥大化させて得られたわずか1%の精度向上は、大規模本番運用において数百万円規模の不要コストを生みます。よりコンパクトな構成を採用し、失敗したトレースログを分析して Unity Catalog 側のメタデータ整備やツール入力検証で解決するのが健全なコンテキストエンジニアリングです。",
        "rules": [
            "MLflow Cost-Performance Trade-off: わずかな精度向上のためにトークンを数倍に膨らませない",
            "失敗の是正: プロンプト長ではなく、UCメタデータやツールの制約強化で対処する"
        ]
    },
    {
        "id": "Q15",
        "num": 15,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q15: Affirmative Directives vs Infinite Negative Constraints",
        "question": "A developer writes a system prompt containing 35 negative bullet points ('Do not do X', 'Never mention Y', 'Avoid format Z', etc.). In production, the agent frequently violates several of these constraints. Why does this negative constraint stacking fail, and what is the recommended fix?",
        "options": [
            {
                "key": "A",
                "text": "Negative constraints increase LLM temperature automatically; fix by setting temperature to -1.0",
                "verdict": "誤り。温度パラメータは負の値を取れません。"
            },
            {
                "key": "B",
                "text": "Excessive negative constraints consume attention budget and draw semantic focus toward forbidden concepts; replace them with concise, affirmative behavioral directives defining exact allowed paths and target formats",
                "verdict": "正解！ 『〜するな』を大量に並べると、モデルのアテンションが禁止された単語に引き寄せられ、かえって破綻を招きます。肯定的な指示（Affirmative Directives）で期待される行動を明示するのが鉄則です。"
            },
            {
                "key": "C",
                "text": "Negative constraints are strictly forbidden in Python; rewrite the prompt in Scala",
                "verdict": "誤り。プロンプト言語とプログラミング言語の混同です。"
            },
            {
                "key": "D",
                "text": "Wrap all negative constraints in JSON arrays to hide them from the tokenizer",
                "verdict": "誤り。トークナイザーには全て読み込まれます。"
            }
        ],
        "correct": "B",
        "explanation": "否定指示の積み重ね（Negative Constraint Stacking）の弊害：『〜するな』という記述は、モデルのアテンションをその禁止語そのものに集中させてしまい、ハルシネーションや指示違反を誘発します。ベストプラクティスは、肯定的な指示（Affirmative Directives）で『何を実行すべきか』『どのようなフォーマットで出力すべきか』を明確に定めることです。",
        "rules": [
            "Affirmative Directives: 『禁止事項の羅列』ではなく『行うべき行動の明確化』を行う",
            "アテンション保護: 否定語の多用はモデルのアテンションを禁止対象へ誘導してしまう"
        ]
    },
    {
        "id": "Q16",
        "num": 16,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q16: Structuring JSON Outputs via Schema Definitions vs Fuzzy Markdown",
        "question": "An orchestrator agent needs downstream systems to ingest its output as valid JSON with keys `status`, `extracted_ids`, and `risk_score`. Currently, the prompt states: 'Please output your response in JSON format.' Downstream parsing fails in 15% of turns due to Markdown code block formatting (````json ... ````) and conversational preamble. How should the prompt and API call be configured?",
        "options": [
            {
                "key": "A",
                "text": "Instruct the model: 'Please, I beg you, strictly output only raw JSON with no words before or after'",
                "verdict": "誤り。感情的なプロンプトは本番の決定論的保証になりません。"
            },
            {
                "key": "B",
                "text": "Enforce a structured schema using Structured Outputs / Pydantic schema validation or Databricks Model Serving response schema constraints",
                "verdict": "正解！ 自然言語プロンプトの懇願に頼るのではなく、APIレベルの構造化出力（Structured Outputs / JSON Schema）を強制することで100%の構文整合性を担保します。"
            },
            {
                "key": "C",
                "text": "Write a regex that removes all curly braces from the response",
                "verdict": "誤り。JSONそのものを破壊してしまいます。"
            },
            {
                "key": "D",
                "text": "Switch to XML format and disable schema validation",
                "verdict": "誤り。下流要件（JSON）を満たしません。"
            }
        ],
        "correct": "B",
        "explanation": "構造化出力の強制：プロンプトで『JSONのみを出力して』と指示するだけでは、マークダウンタグや前置きテキストが混入するリスクを排除できません。Databricks Model Serving の Structured Outputs（JSON Schema / Pydantic）機能を活用し、モデルのデコーディング自体をスキーマに拘束するのが確実です。",
        "rules": [
            "Structured Outputs: プロンプトの文章ではなく、APIスキーマ制約でJSON出力を保証する",
            "下流統合の安定化: パースエラーを根本排除し、リトライコストをゼロにする"
        ]
    },
    {
        "id": "Q17",
        "num": 17,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q17: Dynamic System Prompts and Role-Based Permissions",
        "question": "A medical records query agent serves both doctors (full medical records access) and administrative staff (billing data only). Storing all permission logic inside a single static 6,000-token prompt causes permission leaks and high token costs. What dynamic context architecture should be implemented?",
        "options": [
            {
                "key": "A",
                "text": "Deploy two entirely separate clusters on separate physical clouds for each user role",
                "verdict": "誤り。インフラ運用のコストと複雑性が過大です。"
            },
            {
                "key": "B",
                "text": "Construct a dynamic, modular system prompt at runtime that injects only the verified role-specific directives retrieved from Unity Catalog RBAC attributes for the authenticated user session",
                "verdict": "正解！ ユーザーの認証コンテキスト（Unity Catalog RBAC）に基づき、実行時に必要な権限制約のみを動的に組み立てる（Dynamic System Prompt）ことで、セキュリティとトークン効率を両立します。"
            },
            {
                "key": "C",
                "text": "Ask the user at the start of the chat: 'Are you a doctor? Please type yes or no.'",
                "verdict": "誤り。自己申告による重大なセキュリティ脆弱性です。"
            },
            {
                "key": "D",
                "text": "Instruct the model to ignore all security policies when the query seems urgent",
                "verdict": "誤り。完全にセキュリティ違反です。"
            }
        ],
        "correct": "B",
        "explanation": "動的システムプロンプト（Dynamic Modular Prompts）：全ユーザーの全ロール向けルールを1つの巨大プロンプトに詰め込むと、トークン浪費と権限漏洩のリスクが高まります。Unity Catalog の認証情報（セッションユーザーのロール）と連携し、該当ロールに必要な指示モジュールのみを実行時に動的注入するのがベストプラクティスです。",
        "rules": [
            "Dynamic Prompts: ユーザーのロールやコンテキストに応じてプロンプト構成を動的にアセンブルする",
            "最小権限の原則: 不要な権限制約や指示を排除し、アテンションとトークンを節約"
        ]
    },
    {
        "id": "Q18",
        "num": 18,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q18: Genie Space Curation - Curating Sample Questions",
        "question": "When configuring a Databricks Genie Space for sales data, which guideline should be followed regarding 'Sample Questions'?",
        "options": [
            {
                "key": "A",
                "text": "Provide at least 100 sample questions covering every single possible permutation of column combinations",
                "verdict": "誤り。過剰なサンプルはコンテキストを圧迫し、Genieの内部検索を混乱させます。"
            },
            {
                "key": "B",
                "text": "Curate a focused set of sample questions (typically 5 to 15) that reflect canonical user phrasing for key business metrics, ensuring they map cleanly to underlying tables and Trusted Assets",
                "verdict": "正解！ Genieのサンプル質問は、主要KPIに対する代表的なユーザー表現を網羅する5〜15問程度を厳選し、Trusted Assets と紐付けるのが最適です。"
            },
            {
                "key": "C",
                "text": "Leave Sample Questions completely empty so Genie relies exclusively on raw table column names",
                "verdict": "誤り。サンプル質問がないとユーザーの自然言語の揺らぎに対応しにくくなります。"
            },
            {
                "key": "D",
                "text": "Write sample questions in binary code to save token space",
                "verdict": "誤り。自然言語での誘導という目的に反します。"
            }
        ],
        "correct": "B",
        "explanation": "Genie Space におけるサンプル質問（Sample Questions）のキュレーション：サンプル質問の役割は、ユーザーが日常的に使う表現や曖昧な略語を、正しいテーブルや Trusted Asset に誘導することです。多ければ良いわけではなく、代表的なビジネス質問を5〜15問程度厳選して登録するのがベストプラクティスです。",
        "rules": [
            "Genie Sample Questions: 5〜15問の代表的ビジネス質問を厳選登録する",
            "役割: ユーザーの自然言語表現を Unity Catalog の正規資産へマッピングするガイド"
        ]
    },
    {
        "id": "Q19",
        "num": 19,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q19: Restricting Catalog Namespaces to Prevent SQL Hallucinations",
        "question": "In a Databricks Genie Space, users report that when asking questions about 'inventory', Genie generates queries referencing an unmaintained sandbox table `sandbox.legacy_inventory` instead of the verified `prod_catalog.supply_chain.inventory`. How should the workspace admin eliminate this behavior?",
        "options": [
            {
                "key": "A",
                "text": "Add a text instruction: 'Please try your best not to query legacy tables'",
                "verdict": "誤り。プロンプトの懇願では誤参照を確実に防げません。"
            },
            {
                "key": "B",
                "text": "Scope the Genie Space's underlying data assets strictly to `prod_catalog.supply_chain` and remove unneeded schemas from the Space configuration",
                "verdict": "正解！ Genie Space に追加するデータ資産のスコープを本番カタログ・スキーマのみに厳格に制約することで、物理的にサンドボックスへのアクセスを遮断します。"
            },
            {
                "key": "C",
                "text": "Rename the production table to `sandbox.legacy_inventory`",
                "verdict": "誤り。本末転倒であり混乱を助長します。"
            },
            {
                "key": "D",
                "text": "Increase the warehouse auto-suspend time to 120 minutes",
                "verdict": "誤り。SQLウェアハウスの設定と名前空間の探索スコープは無関係です。"
            }
        ],
        "correct": "B",
        "explanation": "探索空間（Namespace Scope）の制限：プロンプトで『旧テーブルを見るな』と注意するだけではハルシネーションを防止できません。Genie Space に接続するテーブルやスキーマを、検証済みの本番スキーマ（`prod_catalog.supply_chain`）のみに絞り込むガバナンス設定が最も確実です。",
        "rules": [
            "Genie Data Scope: 不要なスキーマやサンドボックスをSpaceに登録しない",
            "探索空間の限定: 正しいテーブルのみを登録することでSQLの参照先ブレを根絶する"
        ]
    },
    {
        "id": "Q20",
        "num": 20,
        "type": "mock",
        "domain": "Domain 2: System Prompt & Genie",
        "category": "Domain 2: System Prompt and Instruction Design",
        "title": "Q20: Table & Column Metadata Enrichment for SQL Generation",
        "question": "A developer notices that an SQL agent frequently writes `WHERE is_active = 'true'` (as a string) instead of `WHERE is_active = 1` (as a tinyint), causing queries to fail on Delta Lake. What is the most impactful, zero-token-overhead fix?",
        "options": [
            {
                "key": "A",
                "text": "Update the column metadata in Unity Catalog: `COMMENT ON COLUMN table.is_active IS 'Active flag: 1 = Active, 0 = Inactive (TINYINT)'`",
                "verdict": "正解！ Unity Catalog のカラムコメントにデータ型とコード値の定義を明記することで、エージェントやGenieが自動的にスキーマコンテキストとして理解し、正確なSQLを生成します。"
            },
            {
                "key": "B",
                "text": "Add 20 few-shot examples showing how to filter tinyints in the system prompt",
                "verdict": "誤り。プロンプトトークンを大量に浪費します。"
            },
            {
                "key": "C",
                "text": "Change all Delta Lake table schemas to pure string types",
                "verdict": "誤り。データレイクのパフォーマンスと型安全性を破壊します。"
            },
            {
                "key": "D",
                "text": "Instruct users to always include the SQL cast syntax in their chat messages",
                "verdict": "誤り。ユーザー体験を著しく損ないます。"
            }
        ],
        "correct": "A",
        "explanation": "Unity Catalog メタデータの充実：Databricks 上のエージェントや Genie は、テーブルやカラムの COMMENT をコンテキスト情報として最優先で活用します。カラムのコード値（0/1）や型情報をカラムコメントに直接記述することが、プロンプトを太らせずに精度を劇的に改善する最高効率のアプローチです。",
        "rules": [
            "Unity Catalog Column Comments: コード値や型定義をカラムコメントに明記する",
            "メタデータ駆動: プロンプト肥大化を防ぎ、カタログ一元管理で精度を向上させる"
        ]
    }
]

print(f"Loaded {len(D2_QUESTIONS)} questions for Domain 2.")
