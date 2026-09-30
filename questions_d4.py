# questions_d4.py
# Domain 4: Memory Architecture with Lakebase and MLflow (10 questions)

D4_QUESTIONS = [
    {
        "id": "Q31",
        "num": 31,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q31: In-context Scratchpad vs Delta-backed State Object",
        "question": "An engineering team is building a long-running batch reconciliation agent on Databricks that executes across a 48-hour period with multiple human approvals and potential compute cluster restarts. Why is an In-context Scratchpad insufficient, making a Delta-backed State Object mandatory?",
        "options": [
            {
                "key": "A",
                "text": "In-context scratchpads consume zero tokens, which violates Databricks billing rules",
                "verdict": "誤り。インコンテキストメモはトークンを消費します。"
            },
            {
                "key": "B",
                "text": "In-context scratchpad memory is volatile and lost upon session termination or compute preemption, whereas a Delta-backed State Object provides durable persistence, auditability, and fault-tolerant resumption across cluster restarts",
                "verdict": "正解！ プロンプト内の作業メモリ（In-context scratchpad）はセッション終了やクラスタの再起動で揮発して消滅します。長時間に及ぶワークフローや耐障害性が求められる場合は、Delta テーブルによる状態の永続化が必須です。"
            },
            {
                "key": "C",
                "text": "Delta Lake can only store binary audio files, not JSON state",
                "verdict": "誤り。Delta Lake は構造化・半構造化データを自在に保存できます。"
            },
            {
                "key": "D",
                "text": "The foundation model automatically deletes its scratchpad every 5 seconds",
                "verdict": "誤り。事実に反します。"
            }
        ],
        "correct": "B",
        "explanation": "エージェント状態管理の選択基準：プロンプト内スクラッチパッド（In-context Scratchpad）は推論中の一時計算には便利ですが、コンピュートの停止やセッション切断で消失する揮発性メモリです。数日間に及ぶタスク、人間の承認待ち、クラスタ障害からの復旧（Fault Tolerance）を担保するには、Delta Lake や Lakebase を用いた永続的な状態オブジェクト（Delta-backed State）が不可欠です。",
        "rules": [
            "In-context Scratchpad: 単一推論ターンの一時的・揮発的な計算メモ",
            "Delta-backed State: 永続的、耐障害性（セッション再開可能）、完全な監査証跡を持つ"
        ]
    },
    {
        "id": "Q32",
        "num": 32,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q32: Resolving Pronouns via Intent Resolution Before External Memory Lookup",
        "question": "A customer in a chat session says: 'Regarding the second option you mentioned earlier, could you cancel that one?' Instead of inspecting the immediate session dialog, the agent runs a semantic vector search against the external Lakebase order table and mistakenly attempts to cancel an order placed 2 years ago. What architectural stage is missing?",
        "options": [
            {
                "key": "A",
                "text": "An Intent Resolution stage that parses conversational pronouns and co-references against the local short-term Session History before initiating external memory or database queries",
                "verdict": "正解！ 『先ほどの2つ目』のような指示代名詞（Pronouns）は、外部の長期記憶を検索する前に、直前の会話履歴（Session History）を参照して実体を確定させる「意図解決（Intent Resolution）」ステージが必要です。"
            },
            {
                "key": "B",
                "text": "A GPU cache flushing script that wipes the customer profile table",
                "verdict": "誤り。キャッシュのフラッシュでは代名詞解決の問題は解けません。"
            },
            {
                "key": "C",
                "text": "A rule forbidding customers from using pronouns in their chats",
                "verdict": "誤り。ユーザーに対話を強要することはできません。"
            },
            {
                "key": "D",
                "text": "Increasing the external vector search Top-K to 50",
                "verdict": "誤り。外部検索を強化しても直前の会話の指示代名詞は解決しません。"
            }
        ],
        "correct": "A",
        "explanation": "意図解決（Intent Resolution）とメモリ階層：指示代名詞（これ、それ、先ほどの件）の解決は、外部の長期メモリ（Lakebase）ではなく、直前の短期記憶（Session History）の責務です。外部検索を実行する前に、クエリ内の代名詞を具体的なエンティティ（例: 『ORD-5541』）に書き換える Intent Resolution ステージを挟むことで、過去の誤った注文へのアクセスを防ぎます。",
        "rules": [
            "Intent Resolution: 外部メモリ検索前に、短期セッション履歴で代名詞・照応表現を確定させる",
            "メモリの役割分担: 直近の会話の流れは Session History、永続的エンティティは Lakebase"
        ]
    },
    {
        "id": "Q33",
        "num": 33,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q33: Structured Query vs Semantic Vector Search in Lakebase",
        "question": "An agent needs to load a user's persistent configuration profile from Lakebase using an exact user identifier `user_id = 'USR-90210'`. Which retrieval pattern must be used?",
        "options": [
            {
                "key": "A",
                "text": "A structured query (exact SQL filter / Key-Value lookup) targeting the primary key",
                "verdict": "正解！ 一意のキー（Primary Key）や確定した属性値に基づく情報取得には、確定的な構造化クエリ（SQL / Key-Value Lookup）を使用するのが正確・高速かつ安全です。"
            },
            {
                "key": "B",
                "text": "A high-dimensional vector search using cosine similarity on the string 'USR-90210'",
                "verdict": "誤り。一意キーに対してベクトル類似度検索を使うと、似た文字列の別ユーザーがヒットする危険があります。"
            },
            {
                "key": "C",
                "text": "A full-table scan loading all 5 million user profiles into the context window",
                "verdict": "誤り。トークン制限とコストの面で完全に不可能です。"
            },
            {
                "key": "D",
                "text": "Generating a random user profile using model hallucination",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "検索メカニズムの使い分け：一意の識別子（UserID、OrderID、UUIDなど）に完全一致するエンティティを取得する場合、ベクトル類似度検索（Vector Similarity Search）を使ってはなりません。ベクトル空間では類似した英数字が誤ヒットするリスクがあります。確定キーには常に「構造化クエリ（Structured SQL Query / KV Lookup）」を用います。",
        "rules": [
            "確定キー（ID・コード）の取得: 構造化クエリ（SQL / Key-Value lookup）を用いる",
            "意味・概念の探索: ベクトル類似度検索（Vector Search）を用いる"
        ]
    },
    {
        "id": "Q34",
        "num": 34,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q34: Over-Retrieval and Context Pollution Risks in Long-Term Memory",
        "question": "An engineer designs an agent that retrieves all past chat sessions from Lakebase for a returning user and injects the raw transcripts into the prompt. The user asks: 'Where should I eat lunch today in Tokyo?' The agent replies recommending a restaurant in London because it read transcripts from a trip the user took three years ago. What context engineering defect occurred?",
        "options": [
            {
                "key": "A",
                "text": "The Tokyo restaurant database was corrupted by Delta Lake compaction",
                "verdict": "誤り。Delta compaction はストレージ最適化でありデータ破損は起こしません。"
            },
            {
                "key": "B",
                "text": "Over-retrieval leading to Context Pollution: uncurated, stale historical memories flooded the prompt and polluted the active reasoning state",
                "verdict": "正解！ 過去の全チャットを生のまま過剰取得（Over-retrieval）したことで、古い無関係な情報がコンテキストを汚染（Context Pollution）し、現在の場所の前提を上書きしてしまった典型例です。"
            },
            {
                "key": "C",
                "text": "The foundation model was trained exclusively on European geography",
                "verdict": "誤り。不適切なコンテキスト供給が原因です。"
            },
            {
                "key": "D",
                "text": "The agent was missing a GPS sensor on the Databricks driver node",
                "verdict": "誤り。的外れな推測です。"
            }
        ],
        "correct": "B",
        "explanation": "長期記憶の過剰取得とコンテキスト汚染（Context Pollution）：過去の履歴を無差別に取得してプロンプトに流し込むと、陳腐化した情報（3年前のロンドン旅行など）が現在の文脈と衝突し、誤った推論を誘発します。長期メモリは生の会話ダンプではなく、最新の嗜好や確定事項を抽出・要約したエンティティとして構造化管理し、時間的な減衰（Temporal Decay）やスコープ限定を行う必要があります。",
        "rules": [
            "Over-retrieval & Context Pollution: 過去の生会話をそのまま流し込むと古い文脈が現在の推論を汚染する",
            "対策: エンティティ要約、時間フィルタリング、直近のコンテキストを最優先する設計"
        ]
    },
    {
        "id": "Q35",
        "num": 35,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q35: Periodic Fact Extraction and Durable Lakebase Entity Sync",
        "question": "To prevent conversational transcripts from bloating long-term memory, an architect implements a background task that runs at the end of each session. What is the recommended function of this background task?",
        "options": [
            {
                "key": "A",
                "text": "Extract durable semantic facts, user preferences, and entity state updates into structured Lakebase tables, discarding conversational filler and transient pleasantries",
                "verdict": "正解！ 会話全体のトークンをそのまま残すのではなく、永続的な価値のある事実（ユーザーの好み、確定した設定、ステータス）のみを抽出してLakebaseの構造化エンティティに同期し、不要な雑談は破棄するのがベストプラクティスです。"
            },
            {
                "key": "B",
                "text": "Permanently encrypt the entire workspace and mail the key to the user",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "C",
                "text": "Duplicate the entire raw chat history into 100 Delta tables for redundancy",
                "verdict": "誤り。ストレージとトークンの無駄を助長します。"
            },
            {
                "key": "D",
                "text": "Translate all user chats into Shakespearean English",
                "verdict": "誤り。意味がありません。"
            }
        ],
        "correct": "A",
        "explanation": "メモリ抽出・同期パイプライン（Fact Extraction Pipeline）：セッション終了時に、対話ログから「永続的に保持すべき事実・嗜好・決定事項」のみを構造化JSONとして抽出し、Lakebase (Delta Lake) に保存します。次回以降のセッションでは、数千行の生ログではなく、この洗練されたプロファイルエンティティ（数十トークン）のみを注入することで、最小限のコストでパーソナライズを実現します。",
        "rules": [
            "Fact Extraction: 生の対話から永続的事実（Durable Facts）のみを抽出してLakebaseに蓄積",
            "トークン節約: 次回以降は要約されたプロファイルのみを読み込む"
        ]
    },
    {
        "id": "Q36",
        "num": 36,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q36: Handling Compute Failures with Checkpointed Delta State",
        "question": "A data engineering agent is orchestrating a 10-step Delta Live Tables pipeline. At step 6, the underlying single-user compute instance undergoes spot node preemption and terminates. When the agent is relaunched on a new cluster, how should it recover?",
        "options": [
            {
                "key": "A",
                "text": "Restart the entire pipeline from step 1 and re-run all previous expensive calculations",
                "verdict": "誤り。計算リソースと時間の膨大な浪費です。"
            },
            {
                "key": "B",
                "text": "Rehydrate its execution state by querying the Delta-backed checkpoint table for the workflow ID, resuming execution directly from step 6 without repeating steps 1 to 5",
                "verdict": "正解！ 各ステップの完了時に状態をDeltaテーブルにチェックポインティングしておくことで、障害発生時にも最新のチェックポイントからシームレスに再開（Resume）できます。"
            },
            {
                "key": "C",
                "text": "Mark the entire dataset as permanently failed and delete the source tables",
                "verdict": "誤り。破壊的な対応です。"
            },
            {
                "key": "D",
                "text": "Pretend step 6 was successful and output an empty file",
                "verdict": "誤り。データ品質を損ないます。"
            }
        ],
        "correct": "B",
        "explanation": "Delta-backed State による耐障害性（Fault Tolerance）：長時間のタスクを実行するエージェントは、ステップ完了ごとに中間ステータスと生成変数を Delta テーブルに書き込んでチェックポイントを作成します。クラスタのプリエンプションやネットワーク障害が発生した場合、新セッションは Delta から直前の状態をロード（Rehydrate）し、未完了のステップから安全に再開できます。",
        "rules": [
            "Checkpointed State: ステップごとにDeltaテーブルへ状態を保存",
            "Fault Tolerance: クラスタ障害や再起動時に、途中から安全にリトライ・再開可能"
        ]
    },
    {
        "id": "Q37",
        "num": 37,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q37: Read-After-Write Consistency in Agentic Memory Updates",
        "question": "An agent executes a tool that updates a customer's shipping address in Lakebase. In the very next reasoning step, the agent invokes an order placement tool. Why is strict read-after-write consistency required in Lakebase for this workflow?",
        "options": [
            {
                "key": "A",
                "text": "To prevent the order placement tool from reading the stale, pre-update address from eventual-consistency replica caches",
                "verdict": "正解！ エージェントがメモリを更新した直後に後続ツールを実行する場合、結果整合性による遅延があると、更新前の古い住所を参照して誤配送を起こすリスクがあります。厳格な Read-After-Write 一貫性が必要です。"
            },
            {
                "key": "B",
                "text": "Because Delta Lake cannot write data unless a human reviewer clicks confirm",
                "verdict": "誤り。Delta Lake はプログラマティックに確定書き込みが可能です。"
            },
            {
                "key": "C",
                "text": "To compress the address string into a 64-bit integer",
                "verdict": "誤り。一貫性の目的とは無関係です。"
            },
            {
                "key": "D",
                "text": "To ensure the LLM's prompt length drops to zero",
                "verdict": "誤り。事実に反します。"
            }
        ],
        "correct": "A",
        "explanation": "エージェントメモリにおける書込後読込一貫性（Read-After-Write Consistency）：マルチステップのエージェントでは、あるステップでの状態更新（例: 住所変更）が、直後のステップ（例: 注文確定）の入力として使われます。もしメモリシステムが遅延同期（Eventual Consistency）の場合、直前に書き込んだはずの最新データが読めず、陳腐なデータに基づいた誤動作を引き起こします。",
        "rules": [
            "Read-After-Write Consistency: ツールによる書込結果が次の推論ステップで直ちに可視化される保証",
            "不整合リスク: 結果整合性の遅延による古いデータの参照を防止"
        ]
    },
    {
        "id": "Q38",
        "num": 38,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q38: Temporal Decay and Memory Eviction Strategies",
        "question": "A shopping assistant agent stores user search preferences in Lakebase. A user searched for 'baby strollers' 14 months ago for a friend's baby shower, but today is looking for 'hiking boots'. The agent continues to recommend strollers alongside boots. How should the memory architecture incorporate temporal dynamics?",
        "options": [
            {
                "key": "A",
                "text": "Implement Temporal Decay scoring and TTL (Time-To-Live) eviction: discount memory relevance based on elapsed time and categorize ephemeral interests separately from enduring preferences",
                "verdict": "正解！ 時間の経過とともに記憶のスコアを減衰させる「時間的減衰（Temporal Decay）」と、一時的な興味と恒久的な好みを区別して古い記憶を退避・削除するTTLポリシーを導入します。"
            },
            {
                "key": "B",
                "text": "Delete all memories every midnight regardless of user identity",
                "verdict": "誤り。永続的な好みの保持ができなくなります。"
            },
            {
                "key": "C",
                "text": "Instruct the user that they must purchase baby strollers to continue using the platform",
                "verdict": "誤り。論外です。"
            },
            {
                "key": "D",
                "text": "Convert the shopping assistant into an aviation autopilot",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "記憶の時間的減衰（Temporal Decay）と退避（Eviction）：すべての記憶を永久に同等の重みで保持すると、一過性の検索（ギフト購入など）がいつまでも現在のアテンションを邪魔します。メモリレコードにタイムスタンプを付与し、経過時間に応じた減衰率（Decay Factor）を適用するか、一定期間アクセスのない一時記憶を自動破棄するTTLを設定します。",
        "rules": [
            "Temporal Decay: 時間の経過に伴って過去の興味・履歴のスコアを低下させる",
            "一時的興味 vs 永続的属性: ギフトや単発検索が現在の推薦を歪めるのを防ぐ"
        ]
    },
    {
        "id": "Q39",
        "num": 39,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q39: User Privacy Compliance in Agent Memory (Right-to-be-Forgotten)",
        "question": "A consumer invokes their GDPR 'Right to be Forgotten' and requests complete deletion of all their personal data. What must the Databricks context engineering team do regarding the agent's memory architecture?",
        "options": [
            {
                "key": "A",
                "text": "Instruct the LLM in the system prompt to ignore that specific user's name in future conversations",
                "verdict": "誤り。データがストレージに物理的に残っているため法的なGDPR要件を満たしません。"
            },
            {
                "key": "B",
                "text": "Execute deterministic DELETE / VACUUM operations across all Lakebase Delta tables, remove the user's vector embeddings from AI Search indexes, and ensure raw session trace logs in MLflow are purged of the user's PII",
                "verdict": "正解！ 忘れられる権利の遵守には、Delta Lake の物理削除（DELETE / VACUUM）、Vector Search インデックスからの除外、MLflow トレースログ内の個人特定可能情報（PII）のパージを包括的に実行する必要があります。"
            },
            {
                "key": "C",
                "text": "Ignore the request because AI agents are legally exempt from privacy laws",
                "verdict": "誤り。重大な法的リスクを招きます。"
            },
            {
                "key": "D",
                "text": "Retrain the foundation model from zero weights on all historical internet data",
                "verdict": "誤り。外部メモリシステムの削除要件に対する誤解です。"
            }
        ],
        "correct": "B",
        "explanation": "エージェントメモリにおけるプライバシーガバナンス（GDPR / 削除要求）：プロンプトで『このユーザーを忘れるように』と指示するだけではコンプライアンス違反です。Lakebase 上の Delta テーブルから該当レコードを DELETE し、`VACUUM` で過去バージョンをパージし、Vector Search インデックスおよび MLflow トレース内の PII を確実に消去するパイプラインが必要です。",
        "rules": [
            "プライバシーガバナンス: Delta Lake (DELETE/VACUUM) ＋ Vector Index ＋ MLflow Trace の包括パージ",
            "プロンプト指示の無効性: プロンプトでの忘却命令は法的データ削除の代替にならない"
        ]
    },
    {
        "id": "Q40",
        "num": 40,
        "type": "mock",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "Q40: Ephemeral Scratchpad Scoping Between Sub-Goals",
        "question": "During a multi-step financial audit, an agent calculates a complex sub-total for subsidiary A across 15 intermediate steps, storing formulas and provisional numbers in its scratchpad. The agent is now moving on to audit subsidiary B. What should the context management layer do with the scratchpad?",
        "options": [
            {
                "key": "A",
                "text": "Retain all 15 calculation steps for subsidiary A permanently in active context to maximize prompt length",
                "verdict": "誤り。不要なトークンでウィンドウが圧迫され、次タスクで混同が生じます。"
            },
            {
                "key": "B",
                "text": "Commit the final verified sub-total for subsidiary A to the persistent state object, and clear the transient calculation scratchpad to allocate clean attention budget for subsidiary B",
                "verdict": "正解！ サブゴールが完了したら、確定した結論のみを永続状態オブジェクトに記録し、途中計算のスクラッチパッドをクリアすることで、後続タスクのためのアテンションバジェットをリフレッシュします。"
            },
            {
                "key": "C",
                "text": "Corrupt the calculation for subsidiary A with random noise",
                "verdict": "誤り。データ破壊です。"
            },
            {
                "key": "D",
                "text": "Terminate the entire agent process and ask the user to start a new company",
                "verdict": "誤り。ナンセンスです。"
            }
        ],
        "correct": "B",
        "explanation": "サブゴール間でのスクラッチパッドのスコープ管理：サブタスクの途中計算やスクラッチパッドをずっと保持し続けると、コンテキストが肥大化し後続タスクの推論が妨げられます（Context Distraction / Drift）。確定した成果物（サマリーや数値）のみを状態オブジェクトにコミットし、一時的なスクラッチパッドは破棄するのがコンテキスト管理の鉄則です。",
        "rules": [
            "Scratchpad Scoping: サブゴール達成時に中間メモを破棄し、確定成果物のみを永続化する",
            "アテンションリフレッシュ: 後続タスクへの不要な干渉を防ぐ"
        ]
    }
]

print(f"Loaded {len(D4_QUESTIONS)} questions for Domain 4.")
