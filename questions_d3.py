# questions_d3.py
# Domain 3: Knowledge Retrieval and Genie Configuration (10 questions)

D3_QUESTIONS = [
    {
        "id": "Q21",
        "num": 21,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q21: Selecting Optimal Chunking Strategy for Code & Technical Docs",
        "question": "An engineering team is building a RAG agent backed by Databricks AI Search to query internal API specifications, software architecture manuals, and code samples. Developers frequently ask pinpoint questions like: 'What is the exact parameter signature for `submit_batch_job`?' and 'What does error code ERR_4092 mean?' The current fixed-size chunking (1,000 tokens with no overlap) returns huge irrelevant paragraphs, degrading Faithfulness. What is the optimal chunking strategy?",
        "options": [
            {
                "key": "A",
                "text": "Increase chunk size to 4,000 tokens to ensure entire architectural chapters fit within a single chunk",
                "verdict": "誤り。チャンクサイズを大きくすると無関係な情報がさらに混入し、Context Distraction が悪化します。"
            },
            {
                "key": "B",
                "text": "Implement Markdown-aware structural chunking with small chunk sizes (256 to 512 tokens), preserving parent document headers as metadata",
                "verdict": "正解！ ピンポイントな引数定義やエラーコードの検索には、マークダウンの構造（見出し・コードブロック）を意識した小さなチャンク（256〜512トークン）が最適です。親文書のメタデータを付与することで文脈も失われません。"
            },
            {
                "key": "C",
                "text": "Abolish chunking completely and feed the entire raw repository directly into the LLM on every query",
                "verdict": "誤り。トークンコストが爆発し、レイテンシも許容不能になります。"
            },
            {
                "key": "D",
                "text": "Use single-character chunking (1 character per chunk) for maximum granularity",
                "verdict": "誤り。意味的文脈（Semantic Context）が完全に破壊されます。"
            }
        ],
        "correct": "B",
        "explanation": "技術ドキュメントやコード仕様のチャンキング戦略：関数仕様やエラーコードのようなピンポイントな情報取得には、「Markdown構造化チャンキング（Markdown-aware Chunking）」かつ比較的小さなチャンクサイズ（256〜512トークン）が最適です。これにより不要な周辺トークン（Context Distraction）を排除し、親ヘッダーのメタデータで位置づけを補正します。",
        "rules": [
            "Technical/API Chunking: Markdown構造を認識させた256〜512トークンの小チャンクが有効",
            "Context Distraction排除: ピンポイント照会に大チャンクを使うと無関係な情報でアテンションが分散する"
        ]
    },
    {
        "id": "Q22",
        "num": 22,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q22: Pre-inference Retrieval vs Just-in-Time (JIT) Agentic Retrieval",
        "question": "A context engineer is designing an agent that must inspect incoming telemetry alerts, decide whether an anomaly is present, and if so, dynamically run SQL queries against live Delta Lake tables to aggregate the past hour of device metrics before rendering an incident report. Which retrieval pattern must be utilized?",
        "options": [
            {
                "key": "A",
                "text": "Pre-inference Retrieval: embedding all Delta Lake tables and dumping top-50 rows into the prompt before the model reads the alert",
                "verdict": "誤り。何を集計すべきか推論前に決定できないため、静的な先読み（Pre-inference）では対応できません。"
            },
            {
                "key": "B",
                "text": "Just-in-Time (JIT) Agentic Retrieval: providing the agent with SQL query tools, allowing it to inspect schemas and dynamically fetch aggregated metrics only when an anomaly is confirmed",
                "verdict": "正解！ 多段階の推論や動的な条件分岐、最新データの集計が必要なユースケースには、エージェントが推論の途中で自律的にツールを呼び出す JIT (Just-in-Time) Agentic Retrieval が必須です。"
            },
            {
                "key": "C",
                "text": "Static Hardcoded Answers: baking all historical device metrics directly into the foundation model weights",
                "verdict": "誤り。リアルタイムデータの照会ができません。"
            },
            {
                "key": "D",
                "text": "Manual User Upload: asking the operator to run SQL in a terminal and paste CSVs into the chat",
                "verdict": "誤り。自律型エージェントの目的に反します。"
            }
        ],
        "correct": "B",
        "explanation": "検索パターンの使い分け：静的なドキュメントQAには推論前にチャンクを注入する「Pre-inference Retrieval」がシンプルで高速ですが、推論の途中で状況判断を行ったり、動的なSQL集計が必要な場合は、ツール呼び出しを介して必要なデータのみを動的に取得する「Just-in-Time (JIT) Agentic Retrieval」が最適です。",
        "rules": [
            "Pre-inference: ユーザー入力直後に固定件数を先読みする方式（静的FAQ向け）",
            "JIT Agentic Retrieval: 推論の途中で動的にツールやクエリを実行する方式（動的集計・多段階調査向け）"
        ]
    },
    {
        "id": "Q23",
        "num": 23,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q23: Hybrid Search Tuning for Domain-Specific Acronyms",
        "question": "In a Databricks AI Search vector index containing aircraft maintenance logs, technicians frequently query specific part serial numbers (e.g., 'SN-8820-X') and fault codes (e.g., 'FAULT_HYD_402'). Dense vector semantic search alone frequently returns generic hydraulic manuals rather than the exact maintenance record. How should the search index be optimized?",
        "options": [
            {
                "key": "A",
                "text": "Configure Hybrid Search in Databricks AI Search, combining dense semantic embeddings with sparse keyword search (BM25 / lexical matching)",
                "verdict": "正解！ 型番やエラーコード、固有のシリアル番号には、意味的類似度（Dense）よりも完全一致・単語一致（Sparse/BM25）が圧倒的に有効です。ハイブリッド検索によって両方の強みを統合します。"
            },
            {
                "key": "B",
                "text": "Lower the embedding dimension from 1024 to 64 to make it more tolerant of typos",
                "verdict": "誤り。次元数を下げると表現力が低下し、精度がさらに悪化します。"
            },
            {
                "key": "C",
                "text": "Delete all dense vector indexes and rely strictly on fuzzy regex matching across parquet files",
                "verdict": "誤り。意味的検索のメリットを完全に失ってしまいます。"
            },
            {
                "key": "D",
                "text": "Convert all aircraft part numbers into random Japanese emojis",
                "verdict": "誤り。意味不明なナンセンスです。"
            }
        ],
        "correct": "A",
        "explanation": "ハイブリッド検索（Hybrid Search）の必要性：埋め込みベクトル（Dense Vector）は概念の類似性を捉えるのが得意ですが、特定の部品番号（SN-8820-X）やエラーコードのような希少な識別子ではスコアが埋もれがちです。Databricks AI Search のハイブリッド検索（Dense + Sparse/BM25）を有効にすることで、キーワードの完全一致と概念のセマンティック検索を両立できます。",
        "rules": [
            "Hybrid Search: 密ベクトル（概念・意味）＋疎ベクトル/BM25（型番・コード・固有名詞）の統合",
            "活用場面: 部品番号、エラーコード、専門略語が混在するコーパス"
        ]
    },
    {
        "id": "Q24",
        "num": 24,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q24: Unity Catalog Governance for Agent Search Space",
        "question": "A production agent is querying an internal knowledge base. A developer accidentally creates a sandbox table `sandbox.test_contracts` containing fake customer discounts, which gets indexed into Databricks Vector Search. The agent begins quoting these fake discounts to real customers. How should Unity Catalog governance be applied to permanently prevent this?",
        "options": [
            {
                "key": "A",
                "text": "Instruct the agent in the system prompt: 'Please verify if the discount seems realistic before speaking'",
                "verdict": "誤り。プロンプトによる曖昧な主観的判断では事故を防止できません。"
            },
            {
                "key": "B",
                "text": "Enforce Unity Catalog catalog-level isolation and tag-based filtering: grant the agent's Service Principal READ access strictly to the `prod_catalog` and configure Vector Search pipelines to ingest only tables tagged with `governance_status = 'Authoritative'`",
                "verdict": "正解！ 物理的な権限モデル（Service Principal RBAC）とタグ付け（Authoritative）によるカタログ分離を行い、非公式データのインデックス混入を構造的に遮断します。"
            },
            {
                "key": "C",
                "text": "Manually inspect every vector index query in real-time by a human operator",
                "verdict": "誤り。自動エージェント運用のリアルタイム要件を満たしません。"
            },
            {
                "key": "D",
                "text": "Drop the entire Unity Catalog metastore and use local sqlite files instead",
                "verdict": "誤り。企業のガバナンスとデータセキュリティを全否定する行為です。"
            }
        ],
        "correct": "B",
        "explanation": "Unity Catalog ガバナンスによる探索空間の統制：エージェントがテストデータや非公式ドラフトを参照する事故（Context Poisoning）を防ぐには、プロンプトでの指示ではなく、Unity Catalog のアクセス権限（Service Principal 権限）とメタデータタグを活用します。`Authoritative`（認定済み）とタグ付けされた正規データのみを Vector Search の同期元に限定するのが鉄則です。",
        "rules": [
            "Authoritative vs Derived: 正規認定資産と派生・テスト資産をカタログとタグで厳格分離",
            "Service Principal RBAC: エージェントの権限を必要最小限の本番カタログに制限する"
        ]
    },
    {
        "id": "Q25",
        "num": 25,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q25: Evaluating Retrieval Failures via MLflow LLM Evaluation Metrics",
        "question": "An evaluation of a Databricks RAG pipeline in MLflow 3 displays: High Context Recall (95%), but Low Faithfulness (52%) and Low Answer Relevance (48%). What does this specific metric profile diagnose about the retrieval and generation pipeline?",
        "options": [
            {
                "key": "A",
                "text": "The vector search failed to retrieve the necessary ground-truth documents",
                "verdict": "誤り。Context Recall が 95% と高いため、必要な正解ドキュメント自体は確実にコンテキストに拾えています。"
            },
            {
                "key": "B",
                "text": "The retriever fetched the correct information, but the generator hallucinated or suffered Context Distraction from excessive noise, failing to base its final answer faithfully on the retrieved context",
                "verdict": "正解！ Context Recall が高いにもかかわらず Faithfulness（忠実度）が低いのは、必要な情報は渡されているものの、モデルがハルシネーションを起こしているかノイズに惑わされている証拠です。"
            },
            {
                "key": "C",
                "text": "The cluster running MLflow was under-provisioned in disk space",
                "verdict": "誤り。評価メトリクスの意味解釈の問題です。"
            },
            {
                "key": "D",
                "text": "The user questions were written in SQL instead of natural language",
                "verdict": "誤り。無関係な推測です。"
            }
        ],
        "correct": "B",
        "explanation": "MLflow LLM 評価メトリクスの診断：\n- **Context Recall**: 正解に必要な情報が検索結果に含まれていたか。\n- **Faithfulness（忠実度）**: 生成された回答が、渡されたコンテキストに基づいているか（ハルシネーションの有無）。\nContext Recall が高く Faithfulness が低い場合、「検索自体は成功しているが、チャンクが長すぎて注意散漫になっているか、モデルがプロンプトの指示を無視して勝手な推論をしている」と診断できます。",
        "rules": [
            "Context Recall 高 ＋ Faithfulness 低: 検索は成功しているが、生成時にハルシネーションや注意散漫が発生",
            "対策: チャンクサイズの縮小、プロンプト指示の厳密化（Grounding強化）"
        ]
    },
    {
        "id": "Q26",
        "num": 26,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q26: Stale Embeddings and Delta Sync Automation",
        "question": "An internal HR policy Delta table is updated weekly on Databricks. However, employees complain that the company HR agent continues to answer questions based on last month's parental leave rules. What is the root cause and recommended remediation in Databricks Vector Search?",
        "options": [
            {
                "key": "A",
                "text": "Vector Search endpoints permanently freeze index weights upon creation; the entire workspace must be deleted and recreated",
                "verdict": "誤り。Databricks Vector Search は動的な継続同期をサポートしています。"
            },
            {
                "key": "B",
                "text": "The Vector Search index was configured for one-time manual snapshot; reconfigure the index as a Delta Sync Index with 'Triggered' or 'Continuous' pipeline sync managed by Unity Catalog",
                "verdict": "正解！ ソースのDeltaテーブルが更新されても、Vector Searchのインデックス同期が動いていなければ陳腐化（Stale）します。Delta Sync Index の自動同期を設定します。"
            },
            {
                "key": "C",
                "text": "The employees are querying from outdated web browsers",
                "verdict": "誤り。サーバー側のインデックス陳腐化が原因です。"
            },
            {
                "key": "D",
                "text": "Delta Lake does not support storing policy text",
                "verdict": "誤り。Delta Lakeはテキストデータを完全にサポートしています。"
            }
        ],
        "correct": "B",
        "explanation": "Databricks Vector Search の Delta Sync Index：Delta テーブルの更新をリアルタイムまたは定期的にベクトルインデックスへ反映するには、インデックスを「Delta Sync」モードに設定し、Unity Catalog 経由でトリガー同期（Triggered）または継続同期（Continuous）を構成する必要があります。ワンタイムのスナップショットのままだと埋め込みが陳腐化します。",
        "rules": [
            "Delta Sync Index: ソースのDeltaテーブルの変更（CDC）を検知して自動的にベクトルを更新",
            "陳腐化（Stale Index）防止: スナップショットではなく自動同期パイプラインを組む"
        ]
    },
    {
        "id": "Q27",
        "num": 27,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q27: Cross-Catalog Search Governance and Row-Level Masking",
        "question": "A multinational corporation deploys an HR query agent on Databricks across European (GDPR) and US operations. European employee salaries are subject to strict row-level security and column-level masking in Unity Catalog. How does Unity Catalog enforce these policies when the agent searches employee records?",
        "options": [
            {
                "key": "A",
                "text": "Unity Catalog security policies are automatically bypassed whenever an LLM agent accesses tables through AI Search",
                "verdict": "誤り。Databricks のセキュリティモデルでは、LLM やエージェント経由であっても UC の行・列マスクは絶対にバイパスされません。"
            },
            {
                "key": "B",
                "text": "Unity Catalog seamlessly enforces row filters and column masks at query runtime based on the calling user's or Service Principal's identity, ensuring unauthorized European salary rows never enter the agent's context window",
                "verdict": "正解！ Unity Catalog の一元化ガバナンスにより、行フィルタ（Row Filters）と列マスク（Column Masks）が実行時に適用され、権限のないデータはコンテキストにそもそも入りません。"
            },
            {
                "key": "C",
                "text": "The agent must be instructed in natural language to close its eyes when reading salary columns",
                "verdict": "誤り。プロンプトによるセキュリティは完全に無効です。"
            },
            {
                "key": "D",
                "text": "European employees must be stored in plain text CSV files outside of Unity Catalog",
                "verdict": "誤り。重大なコンプライアンス違反です。"
            }
        ],
        "correct": "B",
        "explanation": "Unity Catalog の行フィルタ・列マスクによるコンテキスト保護：Unity Catalog は、エージェントや Genie、AI Search がデータにアクセスする際にも、呼び出し主（Service Principal やエンドユーザー）の権限に基づいて Row Filters および Column Masks を自動的に適用します。これにより、機密情報がコンテキストウィンドウに漏洩することを根本から防ぎます。",
        "rules": [
            "UC Row/Column Filters: 権限のない行や列は実行時に自動マスクされ、プロンプトに到達しない",
            "ゼロトラスト: LLMの善意に頼らず、データベースレイヤーで情報漏洩を遮断する"
        ]
    },
    {
        "id": "Q28",
        "num": 28,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q28: Context Window Sizing vs Retrieval Top-K Balancing",
        "question": "A developer expands the vector retrieval Top-K parameter from 5 to 30 chunks (consuming 12,000 tokens) to ensure no facts are missed. However, evaluation shows that the agent's answer quality drops significantly. What context engineering mechanism explains this degradation?",
        "options": [
            {
                "key": "A",
                "text": "Over-retrieval leads to Context Distraction and Dilution of Attention, where low-relevance noise overpowers critical signal and misleads reasoning",
                "verdict": "正解！ Top-K を無暗に増やすと、類似度の低い無関係なチャンクが大量に流れ込み、アテンションが希釈されて重要な手がかりを見失う（Context Distraction / Dilution）が発生します。"
            },
            {
                "key": "B",
                "text": "Top-K values greater than 10 are mathematically incompatible with cosine similarity",
                "verdict": "誤り。コサイン類似度の計算自体に件数制限はありません。"
            },
            {
                "key": "C",
                "text": "The embeddings in Delta Lake turn negative when Top-K exceeds 20",
                "verdict": "誤り。ナンセンスです。"
            },
            {
                "key": "D",
                "text": "The LLM will automatically convert all text to hexadecimal format",
                "verdict": "誤り。事実に反します。"
            }
        ],
        "correct": "A",
        "explanation": "過剰取得（Over-retrieval）の弊害：想起漏れを恐れて Top-K を過度に大きくすると（例: Top-30）、関連度の低いノイズチャンクがコンテキストの大部分を占拠します。これにより、真に必要な情報へのアテンションが希釈（Attention Dilution）され、モデルが混乱して誤答を出力する「Context Distraction」が引き起こされます。",
        "rules": [
            "Over-retrieval: 検索件数が多すぎるとノイズが増加し、回答品質が低下する",
            "バランス: 厳選した Top-3〜5 件 ＋ リランキング（Reranking）が推奨される"
        ]
    },
    {
        "id": "Q29",
        "num": 29,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q29: Embedding Model Selection - Multilingual Support",
        "question": "A global retailer deploys a customer support agent serving queries in Japanese, English, and German against Databricks documentation. When querying Japanese manuals, the agent returns completely irrelevant paragraphs in English. The pipeline currently uses a lightweight English-only embedding model (`bge-small-en`). What is the necessary architectural change?",
        "options": [
            {
                "key": "A",
                "text": "Translate all Japanese documents into English using an offline Python dictionary before embedding",
                "verdict": "誤り。運用の負荷と翻訳ロスの観点から非効率です。"
            },
            {
                "key": "B",
                "text": "Switch the Databricks Vector Search embedding endpoint to a certified Multilingual Embedding model (such as `bge-m3` or multilingual GTE) that maps cross-lingual queries and documents into a shared vector space",
                "verdict": "正解！ 多言語クエリと多言語文書を扱う場合、共有の多言語意味空間を持つ「多言語対応埋め込みモデル（Multilingual Embedding）」を採用することが必須です。"
            },
            {
                "key": "C",
                "text": "Force Japanese customers to submit their queries in Latin alphabet phonetic transliteration",
                "verdict": "誤り。実用に耐えません。"
            },
            {
                "key": "D",
                "text": "Set the similarity metric to Manhattan distance instead of Cosine",
                "verdict": "誤り。言語非互換の解決にはなりません。"
            }
        ],
        "correct": "B",
        "explanation": "埋め込みモデルの選定：英語特化のモデル（`*-en`）は、日本語や他言語のトークン化およびセマンティックマッピングが適切に行われません。多言語サポートが必要な場合は、`bge-m3` 等の多言語対応エンベディングモデル（Multilingual Embedding Model）を Vector Search エンドポイントに指定する必要があります。",
        "rules": [
            "Multilingual Embeddings: 異なる言語間で共通のセマンティック空間を形成するモデルを選定",
            "英語専用モデルの限界: 多言語環境で英語特化モデルを使うとセマンティック検索が完全に破綻する"
        ]
    },
    {
        "id": "Q30",
        "num": 30,
        "type": "mock",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "Q30: Reranking in RAG Retrieval Pipelines",
        "question": "An enterprise RAG pipeline retrieves Top-25 chunks via hybrid vector search. To minimize token consumption and place only the highest-precision evidence into the final LLM prompt, which component should be added between retrieval and prompt assembly?",
        "options": [
            {
                "key": "A",
                "text": "A Cross-Encoder Reranker model that scores and filters down the Top-25 candidates to the Top-3 most relevant chunks",
                "verdict": "正解！ 高速な一次検索（Top-25）で網羅的に取得し、より高精度なクロスエンコーダー・リランカー（Reranker）で Top-3 に絞り込むことで、トークン消費を抑えつつ最高の Faithfulness を達成できます。"
            },
            {
                "key": "B",
                "text": "A random shuffle function that permutes the 25 chunks",
                "verdict": "誤り。関連度の高いチャンクが埋もれてしまいます。"
            },
            {
                "key": "C",
                "text": "An encryption cipher that obscures the retrieved text",
                "verdict": "誤り。LLMが読めなくなります。"
            },
            {
                "key": "D",
                "text": "A gzip compression module that sends binary zip bytes directly to the prompt",
                "verdict": "誤り。テキストプロンプトとして認識できません。"
            }
        ],
        "correct": "A",
        "explanation": "リランキング（Reranking）アーキテクチャ：広範囲の一次検索（Top-20〜50）で候補を逃さず拾った後、Cross-Encoder 等のリランカーを通して質問との関連度を再評価し、上位3〜5件の超高関連チャンクのみをLLMプロンプトに注入します。これにより、Context Distraction を排除しつつ、想起漏れ（Recall）も防げます。",
        "rules": [
            "Reranking: 一次検索（Top-K大）→ リランカーで厳選（Top-K小）→ プロンプト注入",
            "効果: コンテキストトークン節約 ＋ アテンション集中による回答精度の最大化"
        ]
    }
]

print(f"Loaded {len(D3_QUESTIONS)} questions for Domain 3.")
