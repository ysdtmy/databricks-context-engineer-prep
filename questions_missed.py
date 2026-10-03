# questions_missed.py
# Real Mock Exam Missed Questions & In-Depth Review
# Added dynamically from actual exam sessions

MISSED_QUESTIONS = [
    {
        "id": "R1",
        "num": 1,
        "type": "review",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "R1: Sub-Agent Task Dispatch & State Propagation (Coordinator Pattern)",
        "question": "A coordinator agent delegates a customer investigation to three sub-agents:\n- transaction analysis\n- fraud analysis\n- customer-history analysis\n\nEach sub-agent receives only its own task description. Fraud analysis concludes the transaction is suspicious, but the transaction-analysis agent already determined that the transaction was a known test transaction. The fraud agent never received that information.\n\nWhat architectural change would most directly improve consistency?",
        "code": """# Desired Orchestrator / Coordinator State Propagation Pattern:
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class InvestigationTaskState:
    transaction_id: str
    is_test_transaction: bool = False
    verified_findings: Dict[str, Any] = field(default_factory=dict)

# Coordinator dispatching with selective shared state:
def dispatch_fraud_analysis(coordinator_state: InvestigationTaskState):
    # Pass ONLY the relevant findings needed by the specialist:
    subagent_payload = {
        "task": "Perform fraud pattern evaluation",
        "transaction_id": coordinator_state.transaction_id,
        # Critical shared context propagated at dispatch time:
        "known_flags": {
            "is_test_transaction": coordinator_state.is_test_transaction,
            "transaction_verdict": coordinator_state.verified_findings.get("transaction_analysis")
        }
    }
    return fraud_agent.invoke(subagent_payload)""",
        "options": [
            {
                "key": "A",
                "text": "Run all sub-agents sequentially without passing any intermediate information to minimize potential inconsistencies.",
                "verdict": "誤り。中間知見（intermediate findings）を渡さずに単に順次実行（Sequential execution）しても、情報の断絶そのものは解決されません。必要なのは実行順序の変更ではなく、確定したタスク状態の伝播（State Propagation）です。"
            },
            {
                "key": "B",
                "text": "Increase the number of tools available to every sub-agent to enhance their analysis capabilities.",
                "verdict": "誤り。ツールの不足が原因ではありません。fraud-analysis エージェントは不正検知を行う能力を既に持っていますが、欠けているのは他エージェントが確定させた前提事実（Known test transaction）というコンテキストです。"
            },
            {
                "key": "C",
                "text": "Propagate the relevant shared findings and task state to sub-agents at dispatch time to ensure they have a unified understanding of the task.",
                "verdict": "正解！ コーディネーターがサブエージェントへタスクを割り振るディスパッチ時に、先行エージェントの確定知見（Relevant shared findings）とタスク状態（Task state）を渡すことで、各エージェントの専門性を保ちながら判断の整合性（Consistency）を保証できます。"
            },
            {
                "key": "D",
                "text": "Implement a centralized knowledge base that all sub-agents can access and update in real-time.",
                "verdict": "誤り（要注意アンチパターン！）。すべてのサブエージェントが全会話や巨大ナレッジベースを無制限にリアルタイム共有すると、過剰なコンテキスト肥大化と注意散漫（Context Distraction）、他の試行錯誤による汚染、指示の衝突を招き、サブエージェント特化のメリットが失われます。"
            }
        ],
        "correct": "C",
        "explanation": """【問題の診断とアーキテクチャの核心】
この不整合（Inconsistency）は、サブエージェントが「完全に孤立したコンテキスト（Isolated Context）」で動作しているために発生しています。

1. **問題の発生原因**:
   先行する `transaction-analysis` エージェントはすでに「この取引は既知のテスト取引である（Known test transaction）」という決定的な事実を確定させていました。
   しかし、`fraud-analysis` エージェントはその情報を渡されず、テスト取引である事実を知らないまま単独で「疑わしい取引」と判定してしまいました。

2. **正解（C）のアプローチ**:
   コーディネーター（親オーケストレーター）は、各サブエージェントにタスクをディスパッチ（dispatch）するタイミングで、**関連する共有知見（Relevant shared findings）とタスク状態（Task state）** をペイロードに含めて伝播させる必要があります。
   - Transaction ID
   - 前段エージェントの確定結論（例: `is_test_transaction = True`）
   - 調査全体の進行ステータス
   これにより、各専門エージェントは軽量なコンテキストと専門特化（Specialization）を維持したまま、共通の前提事実に基づいた一貫性のある推論を行うことができます。

3. **なぜ D（中央ナレッジベースのリアルタイム共有）は不適なのか？（重要落とし穴）**:
   全サブエージェントが無制限に読み書きする共有ブラックボードやナレッジベースを導入すると、以下の深刻な問題が発生します：
   - **Context Distraction / Bloat**: 他のエージェントの冗長な試行錯誤ログや中間データが全員のコンテキストを圧迫し、モデルの注意力（アテンション）が散漫になる。
   - **Specialization の崩壊**: 各サブエージェントに特化した最小限のプロンプトという利点が失われ、巨大な単一エージェントと同じ弊害が生じる。
   - **競合と汚染**: 未検証の仮説が共有ストレージに即時反映されると、後続エージェントが未確定情報を事実と信じ込む Context Poisoning を引き起こす恐れがある。

したがって、「何でもかんでも共有する（D）」のではなく、「コーディネーターが必要最小限の確定知見を選別してディスパッチ時に渡す（C）」がコンテキストエンジニアリングのベストプラクティスです。""",
        "rules": [
            "Coordinator Pattern: ディスパッチ時に必要最小限の確定知見（Shared Findings）とタスク状態を子に伝播させる",
            "Context Isolation vs Bloat: 全履歴や中央ナレッジを無制限に共有すると Context Distraction を招く",
            "Sequential だけでは解決しない: 実行順序を変えるだけでなく、状態（State）を後続に渡す仕組みが不可欠"
        ]
    },
    {
        "id": "R2",
        "num": 2,
        "type": "review",
        "domain": "Domain 7: Multi-Agent Systems",
        "category": "Domain 7: Multi-Agent Systems and Long-Horizon Tasks",
        "title": "R2: Long-Horizon Workflow Resilience & Dependency Task Graph (Select TWO)",
        "question": "A financial services company has deployed a multi-agent AI system that handles customer dispute investigations. A Supervisor Agent delegates work to specialized agents for transaction retrieval, policy verification, fraud analysis, and case summarization.\n\nIn production, investigations involving 15–20 dependent steps occasionally fail after several minutes. The system sometimes repeats completed investigations, loses intermediate decisions after an agent timeout, and produces final summaries that omit evidence collected earlier in the workflow. The team wants to improve reliability without simply increasing the model context window.\n\nWhich TWO changes would BEST address the underlying production issues?",
        "code": """# Resilient Multi-Agent Architecture with DAG & Checkpointing
from typing import TypedDict, Annotated, List, Dict, Any, Optional

class DisputeInvestigationState(TypedDict):
    dispute_id: str
    completed_steps: List[str]
    checkpoints: Dict[str, Any]
    retrieved_tx: Optional[Dict[str, Any]]
    policy_verdict: Optional[str]
    fraud_score: Optional[float]
    summary_evidence: List[str]

# 1. Dependency-aware Task Graph (DAG):
#    - Parallel execution: [transaction_retrieval] and [policy_verification] can run concurrently
#    - Dependency enforcement: [fraud_analysis] waits for both prerequisites to complete
# 2. Persistent Checkpointed State:
#    - Each node commits state to Delta Lake / Lakebase
#    - On agent timeout, workflow resumes from last checkpoint without restarting""",
        "options": [
            {
                "key": "A",
                "text": "Model the workflow as a dependency-aware task graph and allow independent tasks to execute in parallel while enforcing prerequisites for dependent tasks.",
                "verdict": "正解（1つ目）！ 15〜20ステップに及ぶ長期依存ワークフローは、単純な直列ループではなくDAG（有向非巡回グラフ）としてモデル化します。独立したタスク（取引取得と規約確認など）は並行実行してレイテンシとタイムアウトを抑え、依存関係のあるタスクのみ先行完了を待機させます。"
            },
            {
                "key": "B",
                "text": "Increase the context-window size of the Supervisor Agent so that all intermediate results remain in the prompt throughout the investigation.",
                "verdict": "誤り。プロンプトのコンテキストを単に広げても、状態管理、タイムアウト時の復旧（Checkpointing）、依存関係の保証は行えません。また、問題文で「without simply increasing the model context window」と明記されています。"
            },
            {
                "key": "C",
                "text": "Introduce persistent, structured workflow state that records completed steps, dependencies, intermediate results, and recovery checkpoints so execution can resume after failures.",
                "verdict": "正解（2つ目）！ エージェントのタイムアウト時に最初から再実行（重複調査）されたり中間判定が消失するのを防ぐには、各ステップの成果物と依存状態を永続ストレージ（Delta/Lakebase）にチェックポイント保存し、失敗地点から再開（Resume）可能にする必要があります。"
            },
            {
                "key": "D",
                "text": "Give every specialized agent the complete conversation history and all outputs from every other agent to ensure maximum context availability.",
                "verdict": "誤り（要注意アンチパターン！）。すべての専門エージェントに全履歴と他エージェントの全出力を渡すと、コンテキストウィンドウが急膨張してトークンコストが爆発し、注意散漫（Context Distraction）と証拠の見落とし（Lost in the Middle）がむしろ悪化します。"
            },
            {
                "key": "E",
                "text": "Add more few-shot examples to the Supervisor Agent prompt showing how a successful 20-step investigation should be completed.",
                "verdict": "誤り。Few-shot例はモデルの推論スタイルを誘導するプロンプト技術に過ぎず、タイムアウト耐性、永続ステート管理、依存関係グラフの保証といった分散システム・インフラレベルの信頼性課題を解決できません。"
            }
        ],
        "correct": ["A", "C"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**15〜20ステップに及ぶ長期依存ワークフロー（Long-Horizon Tasks）における本番障害**への対処法を問う、極めて実践的な問題です。

1. **本番環境で発生している3大課題**:
   - **タイムアウトと重複実行**: 数分かかった後にタイムアウトし、完了済みステップまで最初からやり直している。
   - **中間決定の消失**: エージェントが途中でコケると、それまでの分析結果が揮発してしまう。
   - **証拠の欠落（Omit evidence）**: 最終サマリー作成時に、初期に集めた証拠がプロンプト内で埋没・忘却されている。

2. **2つの正解（A と C）が根本治療となる理由**:
   - **【正解 A】依存関係を意識したタスクグラフ（Dependency-aware Task Graph / DAG）**:
     15〜20ステップを愚直に1本道の直列で回すと、全体の実行時間が長くなりタイムアウト率が跳ね上がります。DAGによって「互いに独立したタスクは並行実行（Parallel）」し、「前提結果を必要とするタスクのみ待機」させることで、実行時間を最短化しデッドロックを防ぎます。
   - **【正解 C】永続化された構造化状態 ＆ チェックポイント（Persistent State & Checkpoints）**:
     各エージェントの処理結果や完了ステータスを外部ストア（Delta Lake / Lakebase）に耐久性を持って記録します。これにより、途中でエージェントがタイムアウトしても**「最後の成功チェックポイントから再開（Resume）」**でき、重複実行と中間データの消失を完全に防げます。

3. **なぜ D（全履歴・全出力の垂れ流し共有）は選んではいけないのか？（最重要アンチパターン）**:
   「証拠が抜けているなら、全員に最初からの全会話と全エージェントの出力を渡せば解決するのでは？」と考えがちですが、これは**逆効果（改悪）**です。
   - 20ステップ分の全思考ログ・APIレスポンスを全員に渡すと、数万〜数十万トークンに達します。
   - モデルは長大なコンテキストの中央部にある情報を見落とす **「Lost in the Middle」** や、無関係なログに惑わされる **「Context Distraction」** を起こし、むしろ証拠の脱落やハルシネーションが悪化します。
   - **鉄則**: サブエージェントには「そのタスクに必要な最小限の入力（Selective State）」のみを渡し、全体の証拠は「永続化された構造化状態（C）」からサマリーエージェントが必要な分だけクエリして引っ張るのが正しい設計です。

4. **B と E が不適な理由**:
   - **B（コンテキストウィンドウ拡大）**: 問題文に「without simply increasing the model context window」と明記されている上、メモリサイズを広げてもタイムアウト復旧や重複実行は解決しません。
   - **E（Few-shot例の追加）**: プロンプト例はLLMの出力フォーマットを整えるものであり、実行基盤としてのチェックポイント復旧やDAGスケジューリングの代替にはなりません。""",
        "rules": [
            "Long-Horizon Tasks: 直列ループではなく DAG (Dependency-aware Task Graph) で並行性と依存関係を制御する",
            "Checkpointing & Resume: 中間状態はメモリではなく外部ストア（Delta Lake等）に永続化し、障害時はチェックポイントから再開する",
            "Full Context Sharing はアンチパターン: 全員に全履歴を渡すと Context Distraction / Lost in the Middle が悪化する"
        ]
    },
    {
        "id": "R3",
        "num": 3,
        "type": "review",
        "domain": "Domain 6: Compaction Strategies",
        "category": "Domain 6: Compression and Compaction Strategies",
        "title": "R3: High-Fidelity Compaction vs Sliding-Window Truncation (100+ Tool Calls)",
        "question": "A customer support agent handles conversations with more than 100 tool calls. MLflow traces show that when conversations exceed roughly 75% of the model’s context window, the agent begins mis-citing earlier tool outputs and ignoring constraints from prior turns. The team wants to preserve the session without truncating important facts.\n\nWhat is the best intervention?",
        "code": """# High-Fidelity Compaction Pipeline in Databricks Agent Framework
def compact_conversation_history(history: list[dict], threshold_ratio: float = 0.75) -> list[dict]:
    # MLflow Trace Alert: Context utilization >= 75%
    if current_token_count(history) >= CONTEXT_WINDOW_LIMIT * threshold_ratio:
        # High-Fidelity Semantic Compaction:
        # Extract critical business constraints, validated user facts, and finalized tool verdicts
        compacted_summary = llm_compactor.invoke({
            "instruction": "Preserve all user constraints, IDs, decisions, and resolved entities strictly. Discard raw tool JSON dumps.",
            "history": history[:-5]  # Keep the immediate last 5 active turns intact
        })
        return [
            {"role": "system", "content": f"Active Session Summary (Compacted Facts):\\n{compacted_summary}"},
            *history[-5:]
        ]
    return history""",
        "options": [
            {
                "key": "A",
                "text": "Periodically summarize completed interaction segments and store the summaries in session memory to maintain key information.",
                "verdict": "誤り。セッション外部のメモリに要約を退避するだけでは、モデルのアクティブなプロンプト内に居座り続ける100件以上の生ツール出力や冗長な履歴を直接削減できず、75%飽和による推論劣化を解消できません。"
            },
            {
                "key": "B",
                "text": "Enable high-fidelity conversation compaction to preserve critical facts while reducing context volume.",
                "verdict": "正解！ 100件以上のツール呼び出しによる大量の生JSONや冗長なログから、決定事項・制約・確定事実のみを高精度（High-fidelity）に構造化要約・圧縮（Compaction）することで、重要事実の脱落を防ぎつつコンテキスト体積を激減させます。"
            },
            {
                "key": "C",
                "text": "Upgrade to a larger context window model to increase the amount of information the model can process.",
                "verdict": "誤り。単にモデルのコンテキスト枠を広げても、不要な生データによる注意散漫（Context Distraction）、コスト高騰、レイテンシ悪化の根本解決にはならず、問題を先送りするだけです。"
            },
            {
                "key": "D",
                "text": "Apply sliding-window truncation and retain only the most recent conversation turns to reduce context volume.",
                "verdict": "誤り（要注意アンチパターン！）。スライディングウィンドウによる単純な切り捨て（Truncation）は、古いターンにあった初期の重要制約やツール結果まで無差別に破棄するため、要件の『without truncating important facts（重要事実を切り捨てない）』に正面から反します。"
            }
        ],
        "correct": "B",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**100回以上のツール呼び出しを伴うセッションにおける長期コンテキスト劣化（Long-context degradation）への対処法**を問う問題です。

1. **MLflowトレースから読み取れる症状**:
   - ツール呼び出しが100回を超え、コンテキストウィンドウの約75%に達している。
   - エージェントが過去のツール出力を誤引用（mis-citing）し、以前のターンの制約を無視（ignoring constraints）し始めている。
   - チームの要件: **「重要な事実を切り捨てることなく（without truncating important facts）セッションを維持したい」**。

2. **正解（B: High-fidelity Conversation Compaction）が最適な理由**:
   - ツールを多用するエージェントでは、生のJSONレスポンスや試行錯誤のメッセージがコンテキストの大部分を無駄に占有しています。
   - **高忠実度コンパクション（High-fidelity Compaction）** は、生ログを単に捨てるのではなく、**「重要な制約」「確定した事実・エンティティ」「過去の決定事項」の意味情報（Semantic facts）を抽出し、コンパクトな表現に変換**します。
   - これにより、コンテキスト利用率を大幅に引き下げつつ、推論に必要な情報を100%維持してセッションを続行できます。

3. **なぜ D（Sliding-window truncation）はダメなのか？（出題の罠）**:
   - スライディングウィンドウは「直近Nターンだけ残して過去を全部捨てる」単純な切り捨て手法です。
   - これを行うと、例えば「ターン2でユーザーが指定した重要な制約（例: 返金は不可、特定住所への配送など）」が綺麗サッパリ消失します。
   - 問題文に **"without truncating important facts"（重要な事実を切り捨てずに）** と明記されているため、Truncation を選んだ瞬間に誤答となります。

4. **試験対策のキーワード対応**:
   - `Bigger Context Window` → 容量を増やすだけ（一時しのぎ、コスト増）
   - `Sliding Window / Truncation` → 古いものを無差別に破棄（重要制約が消える）
   - `High-fidelity Compaction` → 重要事実・制約を保持してトークン量を削減（最善手！）""",
        "rules": [
            "Compaction vs Truncation: 単純切り捨て（Truncation）は重要制約を喪失させる。事実保持には Compaction を採用する",
            "75% Context Threshold: 75%超でアテンション劣化（誤引用・制約無視）が始まるため、Compaction のトリガーとする",
            "Bigger Window は根本解決にならない: 100+ツール呼び出しの冗長データを放置するといずれパンクしコストも激増する"
        ]
    },
    {
        "id": "R4",
        "num": 4,
        "type": "review",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Memory Architecture with Lakebase and MLflow",
        "title": "R4: Diagnosing Lakebase LangGraph Checkpoint Failures (Select TWO)",
        "question": "A LangGraph agent deployed on Databricks stores conversation state in Lakebase PostgreSQL using AsyncPostgresSaver.\n\nDuring testing:\n- Users can resume conversations after application restarts.\n- Tool outputs remain available.\n- User preferences collected during previous sessions disappear.\n- Database inspection confirms that checkpoint records exist.\n\nWhich TWO explanations are most likely?",
        "code": """# LangGraph StateSchema & Lakebase Recovery Diagnosis
from typing import TypedDict, Annotated, List, Optional
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# Failure Scenario 1: Field missing from Graph StateSchema (Never Captured)
class IncompleteGraphState(TypedDict):
    messages: list
    tool_outputs: list
    # BUG: 'user_preferences' was NEVER added to graph state, so saver never persists it!

# Failure Scenario 2: Graph State has field, but Recovery fails to merge (Never Restored)
class CompleteGraphState(TypedDict):
    messages: list
    tool_outputs: list
    user_preferences: dict

# During app restart / recovery:
# BUG: The application initializes a new state and loads checkpoint['messages'],
# but forgets to merge checkpoint['user_preferences'] back into the active runtime state!""",
        "options": [
            {
                "key": "A",
                "text": "MLflow checkpoint recovery automatically overrides Lakebase checkpoints and removes user preferences.",
                "verdict": "誤り。MLflow はオブザーバビリティ（トレース・評価）ツールであり、Lakebase のチェックポイントを上書き・削除する機能や責務はありません。"
            },
            {
                "key": "B",
                "text": "Conversation checkpoints persist only the state present in the graph, and user preferences were never added to the graph state before checkpointing.",
                "verdict": "正解（1つ目）！ チェックポイント保存機構（AsyncPostgresSaver）は、LangGraphのグラフ状態（StateSchema）に実際に含まれているフィールドのみを永続化します。会話内でユーザーが好みを伝えていても、それがグラフステートのフィールドとして追加されていなければ、DBに保存されず消滅します。"
            },
            {
                "key": "C",
                "text": "The database schema used by Lakebase for storing checkpoints does not support the data type required for user preferences, leading to their loss.",
                "verdict": "誤り。Lakebase / AsyncPostgresSaver は状態全体をバイナリやJSONB等としてシリアライズして格納するため、ユーザー設定のデータ型が原因で消失することはありません。"
            },
            {
                "key": "D",
                "text": "The application failed to restore or merge the stored user preference fields into the active graph state during recovery, even though checkpoints exist.",
                "verdict": "正解（2つ目）！ DB内にチェックポイントレコード自体は存在しているため、データは正しく保存されていたものの、アプリ再起動時のリカバリー（復元）処理で、保存された preference フィールドをアクティブなグラフ状態にマージ/展開し忘れている可能性が極めて高いです。"
            },
            {
                "key": "E",
                "text": "The AsyncPostgresSaver configuration is set to store only specific parts of the graph state, inadvertently excluding user preferences from being persisted.",
                "verdict": "誤り（要注意アンチパターン！）。AsyncPostgresSaver には特定フィールドだけを選択的に除外して保存するような設定はありません。永続化ストレージ側の設定ではなく、アプリ側のグラフ状態定義（未登録）または復元ロジック（未マージ）に問題があります。"
            }
        ],
        "correct": ["B", "D"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**Lakebase（PostgreSQL / AsyncPostgresSaver）と LangGraph を組み合わせた永続メモリ障害の切り分け**を問う実践的な問題です。

1. **与えられた症状の整理**:
   - アプリ再起動後も会話は再開できている（セッション復旧は動作している）。
   - ツール出力（tool outputs）は保持されている。
   - しかし、以前のセッションで収集した**「ユーザーの好み（User preferences）」だけが消滅**している。
   - **DBを直接確認すると、チェックポイントレコードは正常に存在している（レコード破損ではない）**。

2. **チェックポイント障害診断の鉄則:「Captured? → Persisted? → Restored?」**:
   データが消えた場合、永続化パイプラインのどこで途切れたかを以下の順で検証します。
   - **Step 1: Captured? (グラフ状態に入っていたか？)**
     チェックポイント機能は、LangGraph の StateSchema に明示的に定義され、代入された値しか保存できません。会話テキスト内で好みが言及されていても、エージェントがそれを `state["user_preferences"]` に格納していなければ保存対象になりません。（**正解 B**）
   - **Step 2: Persisted? (DBに書き込まれたか？)**
     問題文で「Database inspection confirms that checkpoint records exist」とあるため、DBへの保存そのものは成功しています。
   - **Step 3: Restored? (再開時にアクティブ状態へ復元されたか？)**
     DBにレコードがあっても、アプリ再起動時に `messages` だけを復元し、`user_preferences` フィールドのデシリアライズやマージ処理を実装していなければ、実行中のエージェントからは好みが消えたように見えます。（**正解 D**）

3. **なぜ E（AsyncPostgresSaver の設定で除外された）は誤りなのか？**:
   - AsyncPostgresSaver（Lakebase）は、与えられた Graph State 全体を直列化（Pickle / JSON）してそのままスナップショット保存するインフラ層のコンポーネントです。
   - 「このフィールドだけ除外して保存する」といったビジネスロジック的な除外設定は存在しません。
   - インフラ（DB/Saver）を疑うのではなく、**アプリ層の状態定義（Captured: B）と復元マージ処理（Restored: D）** を疑うのが正しいアプローチです。

4. **短期記憶（Short-term）と長期記憶（Long-term）の分離**:
   - 会話やツール出力は「スレッド単位の短期チェックポイント（Short-term thread state）」。
   - 一方、セッションをまたぐ「ユーザーの好み（User preferences）」は、本来スレッドチェックポイントではなく、**ユーザーIDに紐づく専用の長期プロファイルストア（Long-term user profile table in Lakebase）** に永続化するのが本番設計の定石です。""",
        "rules": [
            "Checkpoint 診断フロー: Captured? (グラフ定義に含まれるか) → Persisted? (DBに存在するか) → Restored? (復元時にマージされたか)",
            "Saver は丸ごと保存する: AsyncPostgresSaver はステートを直列化するだけであり、特定フィールドを選択除外する設定はない",
            "Short-term vs Long-term: ユーザー設定（Preferences）は会話スレッドではなく専用の長期プロファイルストアで管理すべき"
        ]
    },
    {
        "id": "R5",
        "num": 5,
        "type": "review",
        "domain": "Domain 1: Foundations of Context Engineering",
        "category": "Domain 1: Foundations of Context Engineering",
        "title": "R5: Pre-inference vs Just-In-Time (JIT) Retrieval Strategy",
        "question": "A Databricks agent assists a financial operations team in investigating failed payments. At the beginning of each investigation, the agent retrieves the customer's profile, recent transactions, payment policies, and account status into its context.\n\nThe account status and transaction records can change while the investigation is in progress. In most investigations, only a subset of these data elements is needed, depending on the failure being investigated.\n\nWhich architecture would most effectively reduce unnecessary context while ensuring that the agent uses current information?",
        "code": """# Optimal Hybrid Retrieval Pattern: Pre-inference + Just-In-Time (JIT)
class PaymentInvestigationContext:
    # 1. Pre-inference (Loaded ONCE at session start - Stable context):
    customer_profile: dict       # Stable identity, KYC status
    payment_policies: list[str]  # Corporate refund / SLA rules

    # 2. Just-In-Time (Fetched JIT via tools ONLY when conditionally required):
    async def get_live_account_status(self, account_id: str) -> dict:
        \"\"\"Fetch volatile status immediately before evaluation to ensure freshness.\"\"\"
        return await lakebase_client.fetch_account_status(account_id)

    async def get_failed_transaction(self, tx_id: str) -> dict:
        \"\"\"Fetch specific transaction record only if investigated failure warrants it.\"\"\"
        return await payments_api.fetch_transaction(tx_id)""",
        "options": [
            {
                "key": "A",
                "text": "Preload customer profiles and payment policies at the beginning of the investigation, then retrieve account-status and transaction information only when needed.",
                "verdict": "正解！ 変化しない静的データ（顧客プロファイルや規約ポリシー）は初期にプリロード（Pre-inference）して前提基盤とし、調査中に変動し得る動的データ（口座ステータスや取引記録）は必要になった瞬間に JIT（Just-In-Time）取得することで、コンテキストの最小化とデータの最新鮮度を両立できます。"
            },
            {
                "key": "B",
                "text": "Preload customer profiles and payment policies, but refresh all retrieved information on a fixed schedule throughout the investigation.",
                "verdict": "誤り。固定スケジュールでの一括定期リフレッシュ（Fixed schedule refresh）は、不要なデータまで無駄に再取得し、APIレイテンシとコンテキストウィンドウの圧迫を招きます。"
            },
            {
                "key": "C",
                "text": "Retrieve all information dynamically for every reasoning step, including customer profiles and payment policies, regardless of whether they change.",
                "verdict": "誤り（要注意アンチパターン！）。毎推論ステップですべての情報を動的再取得すると、変動しない静的データまで毎回フェッチされ、トークン消費とコストが爆発し、無関係なデータによるアテンション散漫（Context Distraction）を招きます。"
            },
            {
                "key": "D",
                "text": "Preload all customer, policy, account, and transaction data at session start so the agent can reason without additional retrieval.",
                "verdict": "誤り。セッション開始時に全データを一括プリロードすると、コンテキストが初期から過大になる上、調査中に口座ステータスや取引データが更新された場合に古い情報（Stale data）に基づいた推論ミスを引き起こします。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、コンテキストエンジニアリングの基本原則である**「推論前プリロード（Pre-inference Retrieval）と必要時動的取得（Just-In-Time Retrieval）の適切な使い分け」**を問う重要問題です。

1. **データ特性の2分類**:
   - **静的・準静的データ（Stable Information）**:
     顧客プロファイル（氏名、属性、KYC情報）や決済ポリシー（規約、SLA文書）。これらは調査中に突然変わることは稀であり、調査全体の土台となるため、**セッション開始時にプリロード（Pre-inference）** しておくのが最も効率的です。
   - **動的・揮発性データ（Volatile / Dynamic Information）**:
     口座ステータス（凍結・残高不足等）や取引ログ。これらは調査中にもリアルタイムで変動する可能性があり、また問題文に「調査内容に応じてその一部しか使われない」と明記されています。したがって、**必要になった瞬間に最新状態を取得（Just-In-Time / JIT）** するのが鉄則です。

2. **なぜ C（毎ステップすべて動的取得）はアンチパターンなのか？（出題の罠）**:
   - 「最新データが必要なら、毎回全部取り直せば一番安全では？」と考えがちですが、これは**過剰取得（Over-fetching）の典型例**です。
   - 変わらない規約やプロファイルまで毎ステップ大量に取得してコンテキストに再注入すると、トークンコストが高騰し、長大な不要ログによってモデルのアテンションが散漫（Context Distraction）になります。
   - また、今回の調査で使わない取引データまで毎回取得することになり、効率性を著しく損ないます。

3. **試験対策の暗記ルール（Key Takeaways）**:
   - **Stable ＋ タスク全体で普遍的に必要** → 事前プリロード（Pre-inference）
   - **Dynamic ＋ 鮮度が重要** → 必要時に動的取得（JIT）
   - **Conditional（条件付きで一部のみ必要）** → 初期にはロードせず、トリガー発生時に取得
   - **Everything on every turn（毎ターン全取得）** → 常に過剰・非効率なアンチパターン！""",
        "rules": [
            "Pre-inference vs JIT: 静的データ（プロファイル/規約）は事前ロード、動的データ（口座状態/取引）は必要時JIT取得",
            "Conditional Fetching: 一部しか使われないデータは最初から入れず、必要になった瞬間のみツールで取得する",
            "Everything on Every Turn はアンチパターン: 毎ステップ全データを取り直すとトークンとレイテンシが爆発する"
        ]
    },
    {
        "id": "R6",
        "num": 6,
        "type": "review",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "R6: Diagnosing AI Search: Lexical Success vs Semantic Failure",
        "question": "A RAG agent retrieves documents from a Databricks AI Search index. Evaluation shows:\n- exact product names are frequently retrieved correctly,\n- conceptual questions perform poorly,\n- semantically related documents are often missing,\n- keyword-heavy queries perform much better.\nThe source corpus is appropriate and current.\n\nWhich investigation should be prioritized?",
        "code": """# Databricks Vector Search Diagnostic: Lexical vs Semantic Performance
# MLflow Evaluation Observation:
evaluation_metrics = {
    "exact_match_retrieval_accuracy": 0.94,   # Lexical / Keyword BM25 succeeds
    "semantic_similarity_recall": 0.32,       # Semantic retrieval fails!
    "corpus_freshness": "Current & Valid"
}

# Root Cause Investigation Layer:
# - Inspect Vector Search Endpoint configuration
# - Validate Embedding Model domain suitability (e.g. bge-large-en vs domain embedding)
# - Review Hybrid Search alpha blending parameter (lexical weight vs dense vector weight)
# - Examine Chunking strategy (did bad chunk boundaries ruin sentence embeddings?)""",
        "options": [
            {
                "key": "A",
                "text": "Whether the retrieval configuration and embedding/index strategy are appropriate for semantic queries.",
                "verdict": "正解！ キーワード検索や完全一致（Exact match）は成功している一方、概念的な質問や意味的類似文書の取得に失敗している場合、障害の発生レイヤーは『埋め込み（Embedding）モデル、Vector Search インデックス設定、リトリーバル戦略』にあります。コーパス自体が正常であるため、セマンティック埋め込みの品質とハイブリッド検索の重み付けを最優先で調査すべきです。"
            },
            {
                "key": "B",
                "text": "Whether the index is properly optimized for handling conceptual and semantic searches.",
                "verdict": "誤り。インデックスの最適化という曖昧な表現ではなく、根本となる埋め込みモデル（Embedding）や検索戦略（Retrieval configuration）そのものの適合性を調査する必要があります。"
            },
            {
                "key": "C",
                "text": "Whether the query formulation is correctly capturing the intent behind the user's questions.",
                "verdict": "誤り。プロンプトやクエリ成形（Query Formulation）ではなく、意味的に関連するドキュメント自体のベクトル類似度がスコア化されていないリトリーバル層の不具合が主因です。"
            },
            {
                "key": "D",
                "text": "Whether the system's natural processing capabilities are adequately trained for the domain.",
                "verdict": "誤り。モデル全体の再学習（ファインチューニング）やプロンプト例（Few-shot）の追加を検討する前に、ドキュメントの埋め込みパイプラインと検索設定を検証するのが先決です。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、Databricks AI Search（Vector Search）において**「キーワード一致は成功するが、セマンティック（意味論的）検索が失敗する」場合の根本原因特定レイヤー**を問う問題です。

1. **評価メトリクスが示す明確な兆候**:
   - **完全一致・キーワード検索は成功**: `exact product names are retrieved correctly`, `keyword-heavy queries perform much better`
     → 単語の字面（Lexical / BM25）による一致は正常に機能している。
   - **概念的・意味的検索は失敗**: `conceptual questions perform poorly`, `semantically related documents are missing`
     → 類語や概念の文脈を捉える「埋め込みベクトル（Dense Embedding）」の類似度計算が機能していない。
   - **コーパスは最新かつ適切**: `source corpus is appropriate and current`
     → ドキュメント内容の不足や陳腐化が原因ではない。

2. **調査すべき最優先レイヤー（正解 A）**:
   この兆候は、100% **「埋め込み（Embedding）モデル選定」または「ベクトル検索インデックス・リトリーバル設定」** の不整合を指し示しています。
   - ドメインに適した埋め込みモデルが選ばれているか？（一般的なモデルが専門用語の意味ベクトルを捉えられていない可能性）
   - ハイブリッド検索のブレンド比率（キーワード重視に偏りすぎていないか？）
   - チャンキングサイズが不適切で、文脈（Semantic context）が寸断されていないか？

3. **試験対策の「障害レイヤー分類（Failure Layers）」**:
   Databricks Context Engineer 試験では、症状からどのレイヤーを疑うべきかが体系化されています：
   - **キーワードは当たるが意味が外れる** → **Retrieval / Embedding / Index レイヤー（本問！）**
   - **検索されたドキュメントは完璧だが回答が間違っている** → **Generation / Prompt レイヤー**
   - **ツールの引数や呼び出しを間違える** → **Tool / MCP レイヤー**
   - **前回のセッションの記憶が消えている** → **Memory / Lakebase レイヤー**""",
        "rules": [
            "Lexical Success + Semantic Failure: キーワード成功・意味失敗は『Embedding / Vector Index / Retrieval戦略』を最優先調査",
            "コーパスが正常ならデータ品質を疑わない: Source corpus is current とあればデータ自体の不備は除外する",
            "Failure Layer の特定: 症状に応じて『検索層（Retrieval）』と『生成層（Generation）』と『記憶層（Memory）』を厳密に切り分ける"
        ]
    },
    {
        "id": "R7",
        "num": 7,
        "type": "review",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool Design, MCP, and Agent Context",
        "title": "R7: Pre-inference vs Just-In-Time (JIT) for High-Volatility Data",
        "question": "A financial reporting agent requires various types of information including:\n- Regulatory reporting rules that change quarterly.\n- Current exchange rates updated every minute.\n- Today's stock prices.\n- Company accounting policy.\n\nWhich information should be retrieved dynamically through tool calls?",
        "code": """# Optimal Data Fetching Architecture: Static vs Dynamic JIT
class FinancialReportingPipeline:
    # 1. Static / Periodically Refreshed Context (Pre-inference / Managed RAG):
    company_accounting_policy = "dbfs:/policies/accounting_v2026.md"  # Stable
    quarterly_regulations = "catalog.compliance.sec_rules_q3"       # Quarterly refresh

    # 2. High-Volatility / Real-time Context (Just-In-Time Tool Calls):
    @tool
    def get_live_market_data(ticker: str, currency_pair: str):
        \"\"\"Must be called at inference time immediately before report generation.\"\"\"
        return {
            "exchange_rate": fetch_live_forex(currency_pair),  # Changes every minute!
            "stock_price": fetch_realtime_quote(ticker)        # Changes throughout the day!
        }""",
        "options": [
            {
                "key": "A",
                "text": "Current exchange rates and today's stock prices.",
                "verdict": "正解！ 為替レート（毎分更新）と当日の株価（取引時間中に常に変動）は、極めて時間的感応度が高い（High volatility / Time-sensitive）データです。静的コンテキストに含めると即座に陳腐化（Stale data）して誤報の原因となるため、エージェントが必要とする直前に動的ツール呼び出し（JIT）で最新値を取得する必要があります。"
            },
            {
                "key": "B",
                "text": "Current exchange rates only.",
                "verdict": "誤り。当日の株価（Today's stock prices）も為替レートと同様に取引時間中リアルタイムに変動するデータです。為替レートのみをJIT対象にし、株価を静的コンテキストに入れてしまうと、古い株価を参照する重大な不整合が発生します。"
            },
            {
                "key": "C",
                "text": "Regulatory rules and accounting policy.",
                "verdict": "誤り。四半期ごとに変わる規制ルールや社内会計方針は比較的安定した情報であり、事前インデックス（RAG）や定期スケジュール更新で管理すべきデータです。毎回の動的ツール呼び出しの対象には適しません。"
            },
            {
                "key": "D",
                "text": "All information including regulatory rules, accounting policy, exchange rates and stock prices.",
                "verdict": "誤り（典型的な過剰取得トラップ！）。静的な規約や会計ルールまで毎回ツールで動的取得すると、無駄なAPIレイテンシ、コスト増、コンテキスト肥大化を招きます。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、情報ソースの**「変動頻度（Volatility）と時間的感応度（Time-sensitivity）」に基づいた取得戦略の切り分け**を問う問題です。

1. **4つの情報の特性比較**:
   - **Current exchange rates（為替レート）**: 毎分更新（超高揮発性）→ **JIT ツール呼び出し必須**
   - **Today's stock prices（当日の株価）**: 取引時間中に刻一刻と変動（超高揮発性）→ **JIT ツール呼び出し必須**
   - **Regulatory reporting rules（規制ルール）**: 四半期単位で変更 → スケジュール更新 / RAG検索
   - **Company accounting policy（会計方針）**: 年単位・恒久規程（静的）→ 事前ロード / インデックス

2. **なぜ「為替レートのみ（B）」では不十分なのか？**:
   - 株価（Today's stock prices）も為替と同様、1分・1秒単位で変動するリアルタイムデータです。
   - レポート作成の正確性は「その瞬間の最新値」を取得できるかにかかっているため、**為替と株価の両方**をJITツール呼び出しで取得する必要があります。

3. **試験対策のデータ配置マトリクス**:
   - **静的（年単位）**: 事前プリロード / インデックス化
   - **周期的（四半期・月単位）**: スケジュールリフレッシュ
   - **超高頻度・リアルタイム（分・秒単位）**: **Just-In-Time ツール呼び出し（本問！）**""",
        "rules": [
            "Time-sensitive Data: 為替レートやリアルタイム株価など、分刻みで変わるデータは必ず JIT ツール呼び出しで取得する",
            "株価も高揮発性: 為替だけでなく当日の株価も高揮発性データであり、静的コンテキストに入れてはならない",
            "Everything JIT はアンチパターン: 変化しない会計方針まで毎回ツールで叩くとレイテンシとコストが悪化する"
        ]
    },
    {
        "id": "R8",
        "num": 8,
        "type": "review",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "R8: Enterprise Data Query Interface: NLP-to-SQL & Visual Builder (Select TWO)",
        "question": "A Databricks data engineering team is developing an internal analytics assistant that enables business analysts to explore a large Delta Lake dataset without writing SQL.\n\nGiven that:\n- Many analysts are unfamiliar with SQL syntax.\n- A significant percentage of failed requests are caused by malformed SQL statements.\n\nWhich TWO design approaches would BEST improve usability while reducing query errors?",
        "code": """# Safe Enterprise Data Access Architecture (AI/BI Genie Pattern)
# Approach 1: NL-to-Validated-SQL Interface
class GenieQueryEngine:
    def process_natural_language(self, user_question: str) -> DataFrame:
        # 1. Translate question to SQL intent using semantic metadata
        raw_sql = llm_translator.generate_sql(user_question, trusted_assets_schema)
        # 2. Syntax & Semantic AST Validation (Prevent malformed SQL execution)
        validated_sql = sql_validator.verify_and_sandbox(raw_sql)
        # 3. Safe Execution against Delta Lake
        return spark.sql(validated_sql)

# Approach 2: Visual Query Builder
# - Users select UI widgets: [Table] -> [Dimension Filters] -> [Aggregations (SUM/AVG)]
# - Interface constructs guaranteed-valid SQL under the hood, eliminating syntax errors entirely.""",
        "options": [
            {
                "key": "A",
                "text": "Create a natural language processing (NLP) interface that translates business questions into validated SQL queries before execution.",
                "verdict": "正解（1つ目）！ ビジネスアナリストが普段使っている自然言語（例: 『先四半期で最も売上が高かった製品は？』）を解釈し、スキーマに対して構文・意味検証（Validation）済みの安全な SQL に自動変換して実行する仕組み（Databricks AI/BI Genie の核）を導入することで、SQLの知識がなくても構文エラー（Malformed SQL）を根絶できます。"
            },
            {
                "key": "B",
                "text": "Design an interactive query assistant that provides step-by-step guidance on constructing SQL queries, including auto-completed and error detection.",
                "verdict": "誤り。アナリストが『SQL構文に不慣れ（unfamiliar with SQL）』であるという前提があるため、いくらSQLの書き方をステップバイステップで補助しても、依然としてユーザー自身がSQLを書く責任を負わされるため根本的な認知的負担とエラーは解消されません。"
            },
            {
                "key": "C",
                "text": "Increase the LLM context window and include the full database schema in every prompt so users can continue writing raw SQL with AI assistance.",
                "verdict": "誤り。コンテキストウィンドウを広げて巨大な全スキーマを毎プロンプトに流し込んでも、トークンコストが跳ね上がるだけであり、アナリストのSQLスキル不足や構文エラーの根本解決にはなりません。"
            },
            {
                "key": "D",
                "text": "Develop a query recommendation system that suggests relevant queries based on the user's search history and frequent queries.",
                "verdict": "誤り。定型クエリの推薦は、ビジネスアナリストが求める多様な組み合わせ（アドホックな探索）に対応できず、事前に想定された質問以外に対応できなくなります。"
            },
            {
                "key": "E",
                "text": "Implement a visual query builder with real-time validation guiding users through selecting tables, filters and aggregations.",
                "verdict": "正解（2つ目）！ テーブル、フィルタ条件、集計関数をGUI上でドロップダウンやGUIウィジェットから視覚的に選択させるビジュアルクエリビルダーを導入することで、ユーザーがSQL構文を一切記述することなく、構文エラーのない安全なクエリを動的生成・実行できます。"
            }
        ],
        "correct": ["A", "E"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**SQLを書けない非技術者（ビジネスアナリスト）に対して、構文エラー（Malformed SQL）を起こさずに大規模Delta Lakeをアドホック探索させるためのインターフェース設計**を問う問題です。

1. **現場の2大課題**:
   - アナリストはSQL構文に不慣れである。
   - 失敗リクエストの大部分が「不正なSQL構文（Malformed SQL）」に起因している。

2. **2つの正解（A と E）がベストソリューションとなる理由**:
   - **【正解 A】NLP-to-SQL インターフェース ＋ 実行前バリデーション**:
     アナリストが「自然言語」で質問を入力し、システムがセマンティックレイヤーに基づいてSQLを生成・事前検証（Validation）して実行します（Databricks AI/BI Genie の標準パターン）。ユーザーはSQLを意識する必要がありません。
   - **【正解 E】リアルタイム検証付きビジュアルクエリビルダー（Visual Query Builder）**:
     テーブルやカラム、集計方法をGUI上で選択させることで、構文エラーを物理的に発生させない仕組みを作ります。定型クエリの固定推薦（D）とは異なり、様々な条件を自由に組み合わせて探索できる柔軟性も維持されます。

3. **なぜ B（SQL作成アシスタント）や C（スキーマ全提示）はダメなのか？**:
   - **B**: 依然としてユーザーにSQLを書かせようとしており、「SQLを知らないアナリスト」の根本課題を解決していません。
   - **C**: 単にプロンプトに巨大スキーマを詰め込むだけであり、トークン浪費とContext Distractionを招くだけです。""",
        "rules": [
            "Non-SQL Users の鉄則: ユーザーにSQLを書かせるな。上位インターフェース（自然言語 / GUI）で意図を表現させる",
            "NL-to-SQL: 自然言語を安全にSQLへ変換し、必ず実行前にバリデーション（Validation）を挟む",
            "Visual Query Builder: GUIによる構造化選択で、構文エラー（Malformed SQL）を物理的に排除する"
        ]
    },
    {
        "id": "R9",
        "num": 9,
        "type": "review",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool Design, MCP, and Agent Context",
        "title": "R9: Progressive Disclosure Strategy: Balancing Detail and Attention",
        "question": "A large e-commerce company is designing a new product recommendation engine for their online store, aiming to provide personalized product suggestions to customers without overwhelming them with too much information.\n\nWhich progressive disclosure strategy would best achieve this goal?",
        "code": """# Progressive Disclosure Pattern in E-Commerce Agent Recommendations
# Step 1: Initial Recommendation (Minimal High-Value Information)
initial_recommendation = {
    "product_id": "PROD-9912",
    "name": "Noise-Cancelling Wireless Headphones",
    "price": "$249.00",
    "highlight": "Best match for your recent travel searches"
    # NOTE: Technical specs, 50 reviews, warranty clauses are DEFERRED!
}

# Step 2: On-Demand Detail Retrieval (Revealed ONLY upon customer interaction)
@tool
def get_product_deep_dive(product_id: str, detail_type: str):
    \"\"\"Invoked only when customer clicks 'View Specs' or asks 'What do reviews say?'.\"\"\"
    return catalog_service.fetch_details(product_id, detail_type)""",
        "options": [
            {
                "key": "A",
                "text": "Use a dynamic filtering system that adjusts the product information displayed based on the customer's past purchases and browsing history, prioritizing relevance over comprehensive details.",
                "verdict": "誤り。これは『パーソナライズ推薦アルゴリズム』の説明であり、情報の提示タイミングと認知負荷・コンテキストを制御する『Progressive Disclosure（段階的情報開示）』のアーキテクチャではありません。"
            },
            {
                "key": "B",
                "text": "Design an adaptive layout that adjusts the level of product detail shown based on the device and screen size used by the customer, ensuring an optimal viewing experience across different platforms.",
                "verdict": "誤り。これは画面サイズに対応するレスポンシブWebデザイン（Responsive Layout）の話であり、コンテキスト管理やAIエージェントにおける情報開示の戦略とは異なります。"
            },
            {
                "key": "C",
                "text": "Implement a tiered information display, where basic product details are shown initially with additional information revealed through user interactions such as hovering or clicking.",
                "verdict": "誤り。フロントエンドUIのクリック/ホバー挙動にとどまっており、顧客のエンゲージメントと対話の深さに応じて動的に情報の詳細度を段階的に引き上げていくシステム全体のアーキテクチャ戦略としては不十分です。"
            },
            {
                "key": "D",
                "text": "Gradually reveal product information as the customer interacts with the recommendations balancing the amount of information presented with the customer's engagement level.",
                "verdict": "正解！ Progressive Disclosure（段階的情報開示）の本質は、『最初は必要不可欠なコア情報（商品名、価格、推薦理由）のみを提示し、顧客の関心や対話・エンゲージメントの深まりに応じて追加の詳細情報を段階的に開示・取得する』ことです。これにより、顧客とLLMコンテキストの双方を情報過多（Overwhelming / Distraction）から守ることができます。"
            }
        ],
        "correct": "D",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、AIエージェントおよびコンテキストエンジニアリングにおける重要概念**「Progressive Disclosure（段階的情報開示）」の定義と適用**を問う問題です。

1. **Progressive Disclosure（段階的情報開示）の真の定義**:
   - **初期提示**: ユーザーの意思決定に直結する「最小限の有用な情報（商品名、価格、推薦理由など）」だけを提示する。
   - **段階的開示**: ユーザーが興味を示して質問したりクリックしたタイミングで、詳細スペックやレビュー、代替品などの追加情報を後から引き出す（または動的取得する）。
   - **公式**: `Progressive Disclosure = 今必要な最小限の情報 ＋ 求められた時の追加情報`

2. **コンテキストエンジニアリングにおける意義**:
   - カタログの全属性や大量のツールスキーマを最初からプロンプトに流し込むと、**コンテキストが圧迫され、モデルの注意力が散漫（Context Distraction）になり、トークンコストも爆発**します。
   - 段階的開示を採用することで、常に「現在必要な情報だけ」をコンテキストウィンドウに保つことができます。

3. **なぜ A（動的フィルタリング）は不正解なのか？**:
   - 過去の購入履歴によるフィルタリングは「何を推薦するか（Recommendation / Filtering）」のロジックです。
   - 問題が求めているのは「情報をどう段階的に開示して情報過多を防ぐか（Progressive Disclosure Strategy）」であるため、問われているレイヤーが異なります。""",
        "rules": [
            "Progressive Disclosure: 初期は最小限のコア情報のみ提示 → ユーザーの対話/関心に応じて段階的に詳細を開示する",
            "Not Everything, Not Nothing: 最初から全部出すのも、何も出さないのも間違い。最適な初期要約が必須",
            "Context Distraction 防止: 不要な詳細を遅延ロード（Deferred Loading）することで、LLMのアテンションを保護する"
        ]
    },
    {
        "id": "R10",
        "num": 10,
        "type": "review",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Context Management and Lakebase Memory",
        "title": "R10: Multi-Session Memory Architecture: Working Memory + Lakebase",
        "question": "Objective: Select an appropriate memory architecture for multi-session conversational agents.\n\nA financial services company is developing a customer support assistant on Databricks. Customers frequently return over several weeks to perform account-related tasks. During each session, the assistant must remember the current conversation, while across sessions it should retain user-specific preferences such as preferred notification channels and communication language.\n\nThe engineering team must also ensure:\n- Conversation state does not grow indefinitely within a session.\n- User data remains isolated between customers.\n- Long-term preferences persist even after application restarts.\n- Memory retrieval remains efficient as the user base grows.\n\nWhich memory architecture BEST satisfies these requirements?",
        "code": """# Optimal 2-Tier Memory Architecture for Multi-Session Agents
class FinancialCustomerAgent:
    def __init__(self, user_id: str, session_id: str):
        self.user_id = user_id
        self.session_id = session_id
        
        # 1. Bounded Working Memory: Scoped only to current session
        self.working_memory = SessionWorkingMemory(session_id=session_id, max_tokens=4096)
        
        # 2. Long-term Persistent Memory: Stored in Lakebase with User Isolation
        # Only relevant preferences retrieved on session start
        self.user_preferences = lakebase.retrieve_relevant_memory(
            user_id=user_id, 
            query="notification_channels, language_preference"
        )
        
    def step(self, user_message: str):
        # Context Assembly: System Prompt + Lakebase Prefs + Session Working Memory
        context = assemble(self.user_preferences, self.working_memory.get_context(), user_message)
        response = llm.generate(context)
        self.working_memory.append(user_message, response)
        return response""",
        "options": [
            {
                "key": "A",
                "text": "Use session-scoped working memory for the active conversation and persist user-specific long-term memory in Lakebase, retrieving only relevant memories when a new session begins.",
                "verdict": "正解！ 4大要件（無制限肥大化防止、顧客間隔離、再起動耐性、検索効率）を完全に満たす2層アーキテクチャです。現在進行中の会話は短期セッション作業メモリに限定し、長期設定（言語・通知チャネル等）はLakebaseに永続化し、新セッション開始時に必要な設定のみを選択的（Selective retrieval）に取得します。"
            },
            {
                "key": "B",
                "text": "Maintain a distributed user-isolated cache layer for storing short-term conversation state and a centralized database for long-term user preferences, ensuring data separation and efficient retrieval.",
                "verdict": "誤り。分散キャッシュ＋中央DBという汎用構成では、LLMコンテキスト生成時の選択的メモリ取得（Selective retrieval）やLakebaseとの統合によるエンタープライズ認可・ガバナンス分離が考慮されておらず、モデル層での情報漏洩リスクが残ります。"
            },
            {
                "key": "C",
                "text": "Implement a graph database to store the entire conversation history for each user, enabling efficient querying and retrieval of context across sessions.",
                "verdict": "誤り。全会話履歴をグラフDBに保存して再取得するアプローチは、会話が増えるにつれてプロンプト肥大化、推論レイテンシ悪化、アテンション競合を引き起こします。"
            },
            {
                "key": "D",
                "text": "Store all conversation history in a single in-memory cache with a fixed time-to-live (TTL), allowing expired conversations to be automatically discarded while preserving active sessions.",
                "verdict": "誤り。インメモリTTLキャッシュでは、アプリ再起動時にメモリが消失し、また数週間にわたる長期設定の永続化要件を満たせません。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、Databricks環境における**「マルチセッション・エージェントの2層メモリ設計（Two-Tier Memory Pattern）」**を問う最重要問題です。

1. **4大要件と対応ソリューション**:
   - **会話がセッション内で無制限に肥大化しない**: Session-scoped working memory（短期作業メモリで上限制御）
   - **顧客間のデータ隔離**: Lakebase / Unity Catalog による行レベル・ユーザーID単位の認可境界
   - **アプリ再起動後も数週間にわたり永続化**: Lakebase による永続ストレージ
   - **ユーザー増加後も効率的なメモリ取得**: 新セッション開始時に「関連するメモリのみ」を選択的取得（Selective retrieval）

2. **記憶設計のゴールデンルール**:
   - **Working Memory**: 現在の対話・タスクの実行用（短命・コンテキストウィンドウ管理対象）
   - **Persistent Memory (Lakebase)**: ユーザープロファイル・長期設定用（永続・推論直前に必要な分だけ注入）
   - **Persist broadly, retrieve selectively**: 保存は広く、取得は厳選して行う。""",
        "rules": [
            "2層メモリ設計: 現在の会話は『セッション作業メモリ』、長期設定は『Lakebase』に永続化",
            "Selective Retrieval: 新セッション開始時は全履歴ではなく『必要なメモリのみ』を選択的に注入する",
            "Cache + TTL の限界: インメモリキャッシュやTTLでは再起動耐性と数週間にわたる長期永続化は満たせない"
        ]
    },
    {
        "id": "R11",
        "num": 11,
        "type": "review",
        "domain": "Domain 1: Context Architecture",
        "category": "Domain 1: Foundations of Context Engineering",
        "title": "R11: Balancing JIT Context Retrieval with Efficient Context Management (Select TWO)",
        "question": "Objective: Balance just-in-time context retrieval with efficient context management.\n\nA financial services company is deploying a Databricks-powered AI assistant that generates real-time investment recommendations for wealth management clients.\n\nFor every request, the assistant may need access to:\n- The customer's portfolio and risk profile\n- Current market data\n- Analyst research reports\n- Regulatory investment guidelines\n\nGiven that loading all available customer and market data into every prompt significantly increases token usage and inference latency and most requests require only a small subset of the available information.\n\nWhich TWO architectural approaches BEST satisfy the requirement of retrieving only the information required for the current request, minimizing context window pressure, reducing repeated retrieval latency for stale data and avoiding sending unnecessary context to the LLM?",
        "code": """# Optimal JIT + Selective Caching Pipeline
class InvestmentRecommendationEngine:
    # 1. Cache stable context to avoid repeated retrieval latency
    @cache_layer.cached(ttl_seconds=3600)
    def get_customer_profile(self, customer_id: str):
        return crm_service.fetch_profile(customer_id) # Stable: Risk tolerance, horizon
        
    # 2. Just-In-Time (JIT) retrieval: Fetch ONLY what is needed for current query
    def prepare_context_for_request(self, customer_id: str, query: str):
        profile = self.get_customer_profile(customer_id) # From Cache
        
        # Analyze query intent to selectively fetch only relevant tickers & research
        required_tickers = nlp_parser.extract_tickers(query)
        live_market_data = market_api.fetch_realtime(required_tickers) # Fresh JIT
        relevant_reports = vector_search.query(query, top_k=3)        # Selective JIT
        
        return assemble_prompt(profile, live_market_data, relevant_reports, query)""",
        "options": [
            {
                "key": "A",
                "text": "Maintain a cache for relatively stable customer profile information while retrieving rapidly changing market data on demand.",
                "verdict": "正解（1つ目）！ 顧客プロファイルなどの比較的変化しない情報はキャッシュして再取得レイテンシを削減し、毎分刻みで変化する市場データはオンデマンド（JIT）で都度取得することで、鮮度と効率性を両立します。"
            },
            {
                "key": "B",
                "text": "Use just-in-time retrieval to fetch only the customer records, market data, and research relevant to the current investment request before inference.",
                "verdict": "正解（2つ目）！ 全顧客データや市場レポートを毎プロンプトに流し込むのではなく、現在の投資リクエストに直接必要なサブセット（該当銘柄の市況や関連リサーチ）のみを推論直前にJIT取得することで、コンテキスト圧迫と無駄なトークン消費を最小化します。"
            },
            {
                "key": "C",
                "text": "Implement a data warehousing approach to store all customer and market data and user query optimization techniques to retrieve the required data for each request.",
                "verdict": "誤り。DWHに全データを集約してクエリを最適化しても、モデルのコンテキストウィンドウに何をどう流し込むかというコンテキスト管理問題は解決されません。"
            },
            {
                "key": "D",
                "text": "Deploy a data streaming pipeline to continuously update the AI model with the latest market data and customer information.",
                "verdict": "誤り。ストリーミングでモデルやプロンプトを常に更新し続ける構成は、リクエストで使わない大量の情報まで流し込むことになり、コンテキスト圧迫を悪化させます。"
            },
            {
                "key": "E",
                "text": "Increase the LLM context window so the assistant can include complete customer histories and market reports in every prompt without requiring retrieval optimization.",
                "verdict": "誤り（典型的なアンチパターン！）。コンテキストウィンドウを広げて全部詰め込むのは、トークンコスト高騰、レイテンシ増加、アテンション散漫を招く最悪のアプローチです。"
            }
        ],
        "correct": ["A", "B"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**「データの鮮度（Freshness）」と「アクセス頻度・局所性（Locality）」に応じたコンテキスト最適化手法**を問う複数選択問題です。

1. **2つの正解アプローチの相乗効果**:
   - **【正解 A】安定情報のキャッシュ ＋ 高頻度変動情報のオンデマンド取得**:
     顧客プロファイル（安定）はキャッシュで高速再利用し、市場データ（超動的）は都度取得（JIT）するハイブリッド構成。
   - **【正解 B】現在のリクエストに必要なサブセットのみを推論直前にJIT取得**:
     今回のリクエスト（例: テック株のリバランス）に関連する銘柄の市況とレポートだけを厳選してロードする。

2. **試験で絶対選んではいけないアンチパターン**:
   - **コンテキストウィンドウ拡大（E）**: 容量が増えても不要な情報はノイズでしかなく、回答品質を低下させる。
   - **全データを事前ロード / 常時ストリーミング注入（C, D）**: ほとんどのリクエストは一部のデータしか使わないため、莫大なリソースとトークンが無駄になる。""",
        "rules": [
            "JIT + Cache ハイブリッド: 安定データ（プロファイル）はキャッシュ、動的データ（市場価格）はオンデマンド取得",
            "Request-Specific Subset: 全データを入れず、現在のリクエストに関連するサブセットのみを推論直前にJIT取得する",
            "Larger Context Window is NOT a solution: 窓を広げて全部入れるのはコスト高・レイテンシ増・注意散漫の誤答フラグ"
        ]
    },
    {
        "id": "R12",
        "num": 12,
        "type": "review",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "R12: Well-Grounded RAG Pipeline Steps: Retrieve != Ground",
        "question": "A financial services company is implementing a Retrieval-Augmented Generation (RAG) system to provide personalized investment recommendations to their customers. The system needs to retrieve the most relevant information from a large knowledge base and generate grounded responses.\n\nWhich of the following steps should be included in the RAG pipeline to ensure the responses are well-grounded?",
        "code": """# Canonical Grounded RAG Pipeline Architecture
def grounded_rag_pipeline(customer_query: str, system_prompt: str) -> str:
    # Step 1: Embed the customer query
    query_vector = embedding_model.embed(customer_query)
    
    # Step 2: Retrieve most similar chunks from Vector Search index
    retrieved_chunks = vector_search_index.similarity_search(query_vector, k=5)
    
    # Step 3: Context Assembly (CRITICAL: Retrieve != Ground without this step!)
    # Concatenate system instructions, retrieved evidence, and user query
    assembled_context = f\"\"\"{system_prompt}
    
=== RETRIEVED GROUNDING EVIDENCE ===
{format_chunks(retrieved_chunks)}
====================================

User Question: {customer_query}\"\"\"

    # Step 4: Generation based strictly on assembled evidence
    return llm.generate(assembled_context)""",
        "options": [
            {
                "key": "A",
                "text": "Embed the customer's query, retrieve the most similar chunks from the Vector Search index, assemble them with the system prompt and query, and then generate the grounded response",
                "verdict": "正解！ グラウンデッドRAGの完全な4大ステップ（Query Embedding → Vector Retrieval → Context Assembly → Generation）を正確に網羅しています。検索（Retrieve）しただけでは回答は根拠付けされず、プロンプト内で検索結果を構造化して組み込む『Context Assembly』を経て初めて根拠のある回答が生成されます。"
            },
            {
                "key": "B",
                "text": "Implement a two-stage approach where the system first retrieves a broad set of relevant information from the knowledge base and then uses a filtering mechanism to narrow down the information before generating the response.",
                "verdict": "誤り。2段階検索やフィルタリング（Reranking等）自体は有用ですが、Context Assembly（検索結果をプロンプトに組み立ててLLMに渡すステップ）が抜けており、生成モデルへどう根拠を接続するかが不完全です。"
            },
            {
                "key": "C",
                "text": "Embed the customer's query and retrieve relevant chunks from the knowledge base using a keyword search, then generate the response based on these chunks.",
                "verdict": "誤り。クエリを埋め込みベクトル化した後にキーワード検索を行うという不整合があり、またプロンプトへのコンテキスト組み立て（Assembly）工程が明示されていません。"
            },
            {
                "key": "D",
                "text": "Use a natural language processing (NLP) model to analyze the customer's query and generate a response without retrieving any external information, relying solely on the model's training data.",
                "verdict": "誤り。外部ナレッジを検索せず事前学習データのみに頼るのはRAGの正反対（素のLLM推論）であり、ハルシネーションが発生します。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**RAGにおける最も重要かつ頻出の教訓「Retrieve ≠ Ground（検索しただけでは根拠付けにならない）」**を問う問題です。

1. **正しいRAGパイプラインのフロー**:
   - `Query` → `Embed` → `Retrieve` → **`Assemble context`** → `Generate`
   - 多くの不合格者が「検索（Retrieval）すれば回答が作られる」と錯覚しますが、**検索されたチャンクをシステムプロンプトやユーザー質問と共に1つのプロンプトに組み立てる（Context Assembly）工程**がなければ、LLMは何の根拠も参照できません。

2. **試験の鉄則格言**:
   - **「Retrieve finds evidence; context assembly makes that evidence available to generation.」**
   （検索は証拠を見つけるだけ。コンテキスト組み立てが、その証拠を生成に利用可能にする。）""",
        "rules": [
            "Retrieve != Ground: 検索しただけでは不十分。必ず Context Assembly でプロンプトに注入して初めて根拠付けされる",
            "RAG パイプライン標準順序: Query → Embed → Retrieve → Assemble context → Generate",
            "Context Assembly の役割: システム指示・検索証拠・ユーザー質問を1つの明確な入力に構造化する"
        ]
    },
    {
        "id": "R13",
        "num": 13,
        "type": "review",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "R13: Diagnosing Vector Search: Optimize Embedding Model First",
        "question": "A large e-commerce company is experiencing issues with their product search functionality, resulting in irrelevant search results and difficulty for customers to find desired products.\n\nThe engineering team has identified the underlying issue to the vector search configuration.\n\nWhat should be the FIRST step the team takes to address this problem?",
        "code": """# Diagnostic Order of Vector Search Pipeline:
# 1. Product Data  ==[ Embedding Model ]==> 2. Vector Representations
#                                                    ||
#                                            3. Vector Search Index
#                                                    ||
#                                            4. Ranking / Filtering
#
# RULE: If vector space representations are defective, downstream tweaks are futile!
def diagnose_retrieval_failure():
    # STEP 1: Verify & Optimize Embedding Model representation quality
    test_embedding_quality(model="databricks-bge-large-en", domain="ecommerce_catalog")
    
    # STEP 2 (Later): Query rewriting / Hybrid search tuning
    # STEP 3 (Later): Downstream business re-ranking (reviews, margin)""",
        "options": [
            {
                "key": "A",
                "text": "Optimize the text embedding model to improve the quality of product representations",
                "verdict": "正解！ ベクトル検索の品質は、元データをベクトル空間に写像する『埋め込み（Embedding）モデルの表現品質』に完全に依存します。無関係なカテゴリの商品が検索されてしまう根本原因は、ベクトル表現そのものが商品の意味的特徴（防水、防寒、靴など）を正しく捉えられていないことにあります。下流のランキングやクエリ書き換えをいじる前に、まず埋め込みモデルの選定と最適化を最初に行う必要があります。"
            },
            {
                "key": "B",
                "text": "Implement a query rewriting system to better understand user intent and context.",
                "verdict": "誤り。クエリ書き換えは『ユーザーの質問が曖昧・不十分な場合』に有効な手法です。本問では問題が『ベクトル検索の設定・表現の不備』にあると特定されているため、クエリをいくら書き換えてもインデックス側のベクトル表現が壊れていれば無関係な商品がヒットし続けます。"
            },
            {
                "key": "C",
                "text": "Re-evaluate and adjust the indexing parameters for better data distribution.",
                "verdict": "誤り。インデックスパラメータやカテゴリ数を調整しても、根本のベクトル埋め込みが粗悪であればセマンティック検索精度は向上しません。"
            },
            {
                "key": "D",
                "text": "Adjust the search result ranking algorithm to prioritize products based on customer reviews.",
                "verdict": "誤り。検索結果が無関係な商品だらけの状態でレビュー数順にソートすると、『無関係だがレビューが多い人気商品』が上位に出てくるだけであり、検索の関連性（Relevance）問題は何も解決しません。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**ベクトル検索パイプラインにおけるトラブルシューティングの優先順位（Diagnostic Order）**を問う問題です。

1. **トラブルシューティングの標準順序**:
   - `Query` → **`Embedding`** → `Retrieval` → `Ranking`
   - ベクトル検索で「無関係な結果（Irrelevant results）」が返る場合、表現層（Representation Layer）である埋め込みモデルが、商品のセマンティックな関係性を正しく数値化できていないことが根本原因です。

2. **「クエリ書き換え（Query rewriting）」との違い**:
   - **Poor query understanding（ユーザーの質問が下手）** → クエリ書き換え（Query rewriting）
   - **Poor semantic representation（インデックスのベクトル表現が粗悪）** → **埋め込みモデルの最適化（Embedding optimization - 本問！）**

3. **ランキング調整（Review順）の罠**:
   - 関連性のないデータが取得されている状態で下流のランキングを変えても、不適切な商品が高順位になるだけで本末転倒です。""",
        "rules": [
            "Vector Search トラブルシューティング順序: Query → Embedding → Retrieval → Ranking",
            "意味表現の欠陥は最上流で直す: ベクトル表現が不適切なら、クエリ書き換えやランキングではなく Embedding モデルを最優先で最適化する",
            "Poor Query vs Poor Embedding: 質問が曖昧ならQuery Rewriting、意味的検索が外れるならEmbedding Optimization"
        ]
    },
    {
        "id": "R14",
        "num": 14,
        "type": "review",
        "domain": "Domain 2: Context Compression",
        "category": "Domain 2: Context Compression and Compaction",
        "title": "R14: Failure of Age-Based Trimming vs Semantic Compaction",
        "question": "Objective: Determine when fixed trimming heuristics are insufficient.\n\nA research agent investigates security incidents over several hours, with an early message identifying the affected production system, and a later message referencing it by an internal identifier.\n\nA fixed policy removes all messages older than 30 turns, causing the agent to confuse the affected system with another environment after the older message is removed.\n\nWhich change is most appropriate to address this issue?",
        "code": """# Age-based Trimming vs Semantic Compaction
# Flawed Approach: Fixed Age-based Trimming (Sliding Window)
# Turn 1: Affected System = "prod-db-cluster-01" (Internal ID: SYS-994)
# ... 30 turns of log analysis ...
# Turn 32: Trimming kicks in! Turn 1 is PURGED!
# Turn 33: "Restart SYS-994" -> Agent confuses with "test-db-SYS-994"! (DISASTER)

# Correct Approach: Semantic Compaction
compacted_state = {
    "critical_entities": {"affected_production_system": "prod-db-cluster-01", "internal_id": "SYS-994"},
    "decisions_made": ["Isolated from VPC", "Dumped memory logs"],
    "active_constraints": ["Do not restart without L3 approval"]
}
# Compacted state is ALWAYS retained in context regardless of message age!""",
        "options": [
            {
                "key": "A",
                "text": "Preserve task-relevant entities, decisions, dependencies, and constraints through semantic compaction rather than relying solely on message age.",
                "verdict": "正解！ メッセージの『新しさ・古さ（Age）』は情報の『重要度（Importance）』の指標にはなりません。初期ターンで定義された重要エンティティ（対象システムID、制約、決定事項）が後のターンで参照される場合、時間経過だけで破棄すると致命的な取り違えが起きます。セマンティック・コンパクション（Semantic Compaction）を用いて、重要エンティティ・決定・制約・依存関係を構造化して永続保持することが不可欠です。"
            },
            {
                "key": "B",
                "text": "Enhance the agent's understanding by incorporating external knowledge graphs that can provide additional context to messages.",
                "verdict": "誤り。外部ナレッジグラフを追加しても、現在のインシデント対話内で動的に定義されたセッション固有のエンティティや決定事項の破棄問題は解決されません。"
            },
            {
                "key": "C",
                "text": "Implement a hybrid approach that consider both message age and content relevance to determine which messages to retain.",
                "verdict": "誤り。ユーザー発言や決定事項をメッセージ単位で単純に選別するだけでは、文脈間の参照依存関係（Turn 32の内部IDがTurn 1の定義に依存している状態）が破壊されるリスクを防げません。"
            },
            {
                "key": "D",
                "text": "Increase the retention threshold from 30 to 60 turns to potentially retain more relevant information.",
                "verdict": "誤り（典型的な対症療法！）。ウィンドウサイズを30から60に広げても問題の発生を少し遅らせるだけであり、調査が長引けば61ターン目に同じ障害が再発します。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、コンテキスト管理における**「固定トリミング（Fixed Age-based Trimming）の構造的欠陥」と「セマンティック・コンパクション（Semantic Compaction）」の必要性**を問う超頻出問題です。

1. **なぜ固定トリミング（直近Nターン保持）は失敗するのか？**:
   - **経過時間（Age）と重要度（Importance）は無相関**:
     インシデントの初期（Turn 1〜3）で特定された「対象システムID」「根本原因」「制約条件」は、どれだけ時間が経っても調査全体で不可欠なアンカー情報です。
   - 後続メッセージが内部IDや代名詞（"that system", "SYS-994"）で初期の定義を参照している場合、初期メッセージが削除されると参照先を見失い、別環境と誤認する大事故を起こします。

2. **試験の鉄則対比**:
   - **Age-based trimming asks**: "Is this old?"（古いか？）
   - **Semantic compaction asks**: "Is this still important?"（今も重要か？）
   - 保持すべき4大要素: **Entities（重要エンティティ）, Decisions（決定事項）, Dependencies（依存関係）, Constraints（制約条件）**

3. **「ウィンドウを30から60に広げる（D）」が不正解な理由**:
   - ウィンドウ拡大は「容量の拡張（Capacity）」であって「コンテキスト管理（Management）」ではありません。長時間の調査では必ず再度上限に達します。""",
        "rules": [
            "Age != Importance: メッセージが古いことと重要でないことは別。初期の重要エンティティを経過時間だけで捨てるな",
            "Semantic Compaction の保持対象: Entities（エンティティ）, Decisions（決定事項）, Dependencies（依存関係）, Constraints（制約条件）",
            "Threshold 拡大は対症療法: 30ターンを60ターンに広げる選択肢は根本解決にならない誤答パターン"
        ]
    },
    {
        "id": "R15",
        "num": 15,
        "type": "review",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool Design, MCP, and Agent Context",
        "title": "R15: Context Scoping & Context Caching for Attention Budget Optimization (Select TWO)",
        "question": "A team is building a cloud-based data analytics platform that processes large volumes of sensor data from industrial equipment. The platform uses a combination of stream processing and batch processing to handle the workload. The team notices that the agent responsible for context management is frequently spending a significant portion of its attention budget on retrieving and processing raw sensor logs, even when the current business question does not require that level of detail.\n\nWhich TWO changes would be most effective in optimizing the agent's context management?",
        "code": """# Context Optimization: Scoping + Caching Pattern
class IndustrialSensorAgent:
    def __init__(self):
        self.context_cache = {}  # Context Caching: Store processed representations
        
    def answer_query(self, query: str):
        # 1. Context Scoping: Filter strictly by equipment, time range, & metrics
        scope_criteria = extract_metadata_scope(query)
        cache_key = generate_cache_key(scope_criteria)
        
        # 2. Context Caching: Avoid repeated retrieval of the same raw logs
        if cache_key in self.context_cache:
            scoped_context = self.context_cache[cache_key]
        else:
            scoped_context = fetch_scoped_aggregates(scope_criteria) # Scoped retrieval
            self.context_cache[cache_key] = scoped_context
            
        # Protect attention budget: Send ONLY relevant aggregated facts to LLM
        return llm.generate(f"Context: {scoped_context}\\nQuery: {query}")""",
        "options": [
            {
                "key": "A",
                "text": "Implement a context scoping mechanism to selectively retrieve only the relevant portions of the raw logs",
                "verdict": "正解（1つ目）！ コンテキストスコープ（Context Scoping）は、設備ID、時間枠、異常タイプ、指標などのメタデータに基づいて検索・取得範囲を厳格に絞り込む技術です。業務上の質問（例: 保守コスト超過の工場）に不要な生温度・振動ログの流入を物理的に遮断し、エージェントの有限な Attention Budget を保護します。"
            },
            {
                "key": "B",
                "text": "Implement a context caching mechanism to reduce the need for repeated retrieval of raw logs",
                "verdict": "正解（2つ目）！ 一度取得・加工した表現や集計結果をコンテキストキャッシュに保存することで、後続のリクエストで同じ生ログを繰り返し取得（Repeated retrieval）する無駄を根絶し、レイテンシとトークン消費を大幅に削減します。"
            },
            {
                "key": "C",
                "text": "Offload the raw log processing to a separate service, reducing the agent's workload",
                "verdict": "誤り。別サービスへのオフロードはシステム全体のマイクロサービス化・負荷分散にはなりますが、問題が求めている『エージェント自身のコンテキスト管理（何をプロンプトに含めるか）』の最適化には直接寄与しません。"
            },
            {
                "key": "D",
                "text": "Increase the overall attention budget allocated to the agent to handle the high volume of data",
                "verdict": "誤り（典型的なアンチパターン！）。アテンション予算やコンテキスト窓を拡大しても、無関係な生データがノイズとして注意力を奪う（Attention Competition）根本原因を放置するため、コストと遅延が増大するだけです。"
            },
            {
                "key": "E",
                "text": "Store the entire raw sensor log permanently in the agent's conversation memory so future requests never need retrieval",
                "verdict": "誤り（最悪のアンチパターン！）。会話メモリに膨大な生ログを永続的に溜め込むと、メモリが巨大なゴミ捨て場と化し、ターンが進むごとにコンテキストが破綻します。"
            }
        ],
        "correct": ["A", "B"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、大量データ処理における**「Attention Budget（アテンション予算）の保護」と「コンテキストスコープ ＋ キャッシュ」の相乗効果**を問う問題です。

1. **2大アプローチの組み合わせ**:
   - **【正解 A】Context Scoping（スコープ絞り込み）**:
     「何でもかんでも取ってこない」。質問に必要な属性（設備・期間・メトリクス）で検索範囲をフィルタリングし、不要な生データのプロンプト流入を防ぐ。
   - **【正解 B】Context Caching（コンテキストキャッシュ）**:
     「同じものを何度も取ってこない」。一度処理したコンテキストを再利用し、Repeated retrieval を撲滅する。

2. **試験のゴールデンルール**:
   - **「The best context is not the largest context — it is the smallest sufficient context.」**
   （最良のコンテキストとは、最大のコンテキストではなく、最小にして十分なコンテキストである）
   - 「生データが多すぎる / 注意力が奪われている」 $\rightarrow$ **Scoping / Filtering**
   - 「同じデータの取得が繰り返されている」 $\rightarrow$ **Caching**""",
        "rules": [
            "Context Scoping: 生データを全件入れず、メタデータ（設備/時間等）で必要最小限にスコープを絞る",
            "Context Caching: Repeated retrieval を防ぐため、一度取得・処理したコンテキストを再利用する",
            "Smallest Sufficient Context: コンテキスト窓の拡大や全ログのメモリ永続化は常に誤答フラグ"
        ]
    },
    {
        "id": "R16",
        "num": 16,
        "type": "review",
        "domain": "Domain 3: Knowledge Retrieval",
        "category": "Domain 3: Knowledge Retrieval and Genie Configuration",
        "title": "R16: Coreference Resolution & Query Rewriting Before Retrieval (Select TWO)",
        "question": "Objective: Prevent retrieval failures caused by unresolved conversational references.\n\nA global bank deploys a Databricks-powered AI assistant to help relationship managers review customer financial products. During one conversation, the following interaction occurs:\nCustomer: \"Summarize my Platinum Credit Card benefits.\"\nThe assistant correctly retrieves and summarizes the Platinum Credit Card details.\nA few turns later, after discussing mortgage rates, the customer asks:\n\"How about the other account?\"\nThe customer is referring to their Premier Savings Account, but the assistant retrieves information about the Platinum Credit Card because the retrieval query never resolved what \"the other account\" referred to.\n\nMLflow traces show:\n- AI Search consistently retrieves the highest-ranked documents for the generated query.\n- Retrieval latency and ranking quality remain normal.\n- The ambiguous phrase \"the other account\" is passed directly to the retriever without first being linked to an entity from the conversation history.\n- Once the retrieval query is generated, downstream response generation behaves correctly.\n\nThe engineering team wants to eliminate this failure without increasing retrieval latency or expanding the search index.\n\nWhich TWO pipeline modifications would BEST address the root cause without increasing retrieval latency or expanding the search index?",
        "code": """# Coreference Resolution & Pre-Retrieval Rewriting Pipeline
class ConversationalRAGPipeline:
    def process_turn(self, conversation_history, raw_user_message):
        # Customer asks: "How about the other account?"
        
        # 1. Pre-Retrieval Coreference & Intent Resolution Layer
        # Analyzes conversation state to resolve pronouns / ambiguous references
        resolved_entity = coreference_engine.resolve(
            reference="the other account",
            history=conversation_history # Links to "Premier Savings Account"
        )
        
        # 2. Query Rewriting: Construct explicit search query
        explicit_retrieval_query = f"{resolved_entity} benefits"
        # explicit_retrieval_query is now: "Premier Savings Account benefits"
        
        # 3. AI Search executes with precise entity
        docs = ai_search.retrieve(query=explicit_retrieval_query)
        return llm.generate_response(docs)""",
        "options": [
            {
                "key": "A",
                "text": "Resolve conversational references (coreference resolution) against the active conversation state before constructing the retrieval query so ambiguous phrases are replaced with the intended entity.",
                "verdict": "正解（1つ目）！ 「the other account」のような照応指示（代名詞・曖昧な指示語）を、検索クエリを作成する前にアクティブな会話状態と照合して解決（Coreference resolution）し、意図されたエンティティ（Premier Savings Account）に置き換えることで、根本原因を直接解消します。"
            },
            {
                "key": "B",
                "text": "Introduce an intent and entity-resolution stage before retrieval that rewrites ambiguous user requests into explicit retrieval queries, such as 'Premier Savings Account benefits'.",
                "verdict": "正解（2つ目）！ 検索パイプラインの前段に『意図・エンティティ解決ステージ』を挟み、曖昧な指示を『Premier Savings Account benefits』のような完全かつ明示的なクエリに書き直して（Query rewriting）からRetrieverに渡すことで、検索エンジンが正確な文書を取得できるようにします。"
            },
            {
                "key": "C",
                "text": "Append a clarification message after the assistant generates its response asking whether the retrieved account was the intended one.",
                "verdict": "誤り。回答生成後に確認メッセージを付けるのは『手遅れ（Too late）』です。すでに誤ったドキュメントを取得して誤った回答を出力した後に聞き返すのはUX・信頼性の面で最悪です。確認するなら検索前に行うべきです。"
            },
            {
                "key": "D",
                "text": "Implement a hybrid search approach that combines vector search with keyword matching to better identifying phrases such as 'the other account'.",
                "verdict": "誤り。検索エンジンは渡されたクエリ通りに正常動作しています。クエリが『the other account』という曖昧な単語のままでは、キーワード検索を併用しても口座を特定できません。問題は検索エンジンではなくクエリ側にあります。"
            },
            {
                "key": "E",
                "text": "Expand the system prompt with additional few-shot conversations demonstrating banking terminology and account summaries to improve the model's understanding of context.",
                "verdict": "誤り。プロンプトにFew-shot例を追加しても、検索パイプラインが未解決の指示語をAI Searchに送信してしまう構造的バグは解決されません。"
            }
        ],
        "correct": ["A", "B"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、対話型RAGにおける**「照応解析（Coreference Resolution）と検索前クエリ書き換え（Query Rewriting）」**の必須パターンを問う問題です。

1. **MLflow Trace が示す決定的な証拠**:
   - AI Search のレイテンシもランキングも正常。渡されたクエリに対しては最高精度の文書を返している。
   - すなわち、**「検索エンジン（Retriever）に罪はなく、渡されたクエリ自体が壊れている（Good retrieval + bad query）」**状態です。

2. **解決すべきポイント（Resolve Before Retrieval）**:
   - `this`, `that`, `it`, `the other one` などの指示語は、**検索エンジンに渡す前（Before Retrieval）に会話履歴から具体的なエンティティへ解決**しなければなりません。
   - 会話履歴 $\rightarrow$ 照応解析（Coreference Resolution） $\rightarrow$ 明示的クエリ作成（Query Rewriting） $\rightarrow$ AI Search""",
        "rules": [
            "Good retrieval + bad query = query-understanding problem: 検索が正常ならインデックスではなくクエリ生成層を修正する",
            "Resolve before retrieval: 代名詞や曖昧な指示語は検索前に必ず明示的エンティティへ解決・書き換える",
            "事後確認は手遅れ: 誤回答を生成した後に確認メッセージを出す設計は不適切"
        ]
    },
    {
        "id": "R17",
        "num": 17,
        "type": "review",
        "domain": "Domain 1: Context Architecture",
        "category": "Domain 1: Foundations of Context Engineering",
        "title": "R17: Purpose of Multiple Independent Experiment Runs in Prompt Evaluation",
        "question": "Objective: Evaluate prompt experiment results to identify a configuration that is reliable for production.\n\nA retail company is using a Generative AI-powered recommendation assistant to generate personalized product recommendations. The team is testing multiple prompt configurations to determine which prompt produces the best business outcomes.\n\nThe team conducts the same A/B experiment across multiple independent runs because individual runs can vary due to differences in user traffic, recommendation requests, and model generation behavior.\n\nThe experiment results show that one prompt configuration achieves a high conversion rate in a single run, while another configuration produces slightly lower but more consistent conversion performance across all runs.\n\nThe product team wants to select a prompt for production and is concerned about choosing a configuration that performs well only under a particular experiment run.\n\nWhat is the primary benefit of analyzing the experiment results across multiple runs?",
        "code": """# Production Prompt Evaluation: Single-Run Fluke vs Multi-Run Reliability
experiment_results = {
    "Prompt_A": [0.85, 0.42, 0.38, 0.45], # High single-run peak (0.85), but volatile!
    "Prompt_B": [0.68, 0.67, 0.70, 0.69]  # Highly consistent & reproducible across runs!
}

# Production Selection Rule:
# Choose Prompt_B! Reliability and consistency across multiple runs outweigh a single lucky run.""",
        "options": [
            {
                "key": "A",
                "text": "To identify the most reliable prompt configuration for consistent performance",
                "verdict": "正解！ A/Bテストを複数回独立して実行する最大の目的は、単一の試行における偶発的なブレ（Random variation）を排除し、本番環境で一貫した成果を再現性高く発揮できる『最も信頼性の高いプロンプト構成』を特定することです。"
            },
            {
                "key": "B",
                "text": "To mitigate the impact of external factors on experiment results and ensure the selected prompt configuration is robust",
                "verdict": "誤り。外部要因の影響緩和という表現は一般的な統計の目的の一部ですが、プロンプト選定において複数回評価を行う直接の主目的は『一貫したパフォーマンスを発揮する信頼性（Reliable configuration for consistent performance）』の確認です。"
            },
            {
                "key": "C",
                "text": "To determine the minimum number of runs required for a statistically significant result",
                "verdict": "誤り。必要試行回数の計算は実験設計段階の作業であり、複数回実行結果を分析する主目的ではありません。"
            },
            {
                "key": "D",
                "text": "To compare the performance of different models used in the recommendation assistant",
                "verdict": "誤り。本実験でテストされている変数は『プロンプト構成（Prompt configurations）』であり、モデルの比較ではありません。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、プロンプト評価における**「単一試行の偶然（Single-run fluke）」と「複数回試行による信頼性（Multi-run reliability）」の評価基準**を問う問題です。

1. **本番運用におけるプロンプト選定基準**:
   - LLMには生成の揺らぎ（Temperatureやトラフィックの偏り）が存在するため、1回だけ突出した高スコアを出したプロンプト（Prompt A）は過学習や偶然の産物であるリスクがあります。
   - 本番環境で求められるのは、**「いつ誰が使っても安定して高いパフォーマンスを維持できる一貫性（Consistency & Reproducibility）」**です。

2. **試験の鉄則格言**:
   - **「One run shows performance; repeated runs provide evidence of reliability.」**
   （1回の実行は単なるその場のパフォーマンスを示すに過ぎない。繰り返しの実行が初めて信頼性の証拠となる。）""",
        "rules": [
            "One run shows performance; repeated runs provide evidence of reliability",
            "本番プロンプト選定基準: 最高瞬間風速ではなく『一貫性（Consistency）』と『再現性（Reproducibility）』を最優先する",
            "A/B Testing 複数回実行: 偶発的ブレを排除し、安定した Reliable configuration を特定する"
        ]
    },
    {
        "id": "R18",
        "num": 18,
        "type": "review",
        "domain": "Domain 2: Context Compression",
        "category": "Domain 2: Context Compression and Compaction",
        "title": "R18: Context Compaction & Selective JIT for Recommendation Agents (Select TWO)",
        "question": "Objective: Optimize context management for a recommendation agent.\n\nA global e-commerce company deploys a Databricks-powered shopping assistant that generates personalized product recommendations. For every customer interaction, the assistant creates a detailed reasoning summary containing:\n- Previously viewed products\n- Purchase history\n- Product comparisons\n- Recommendation rationale\n- Promotional campaigns\n- Customer preferences\n\nAs customers continue interacting over multiple sessions, MLflow traces reveal:\n- Prompt token counts steadily increase.\n- Response latency and inference cost continue to rise.\n- Many older recommendation summaries are rarely referenced again.\n- The assistant still needs to retain key customer preferences and important purchase history for future recommendations.\n\nWhich TWO architectural improvements BEST address the requirement to reduce context window pressure without sacrificing quality of personalized recommendations?",
        "code": """# Optimal Recommendation Context Architecture
class RecommendationContextManager:
    # 1. Compaction: Replace bulky historical reports with concise, future-useful summaries
    def compact_history(self, full_interaction_log):
        return {
            "stable_preferences": "Prefers premium wireless headphones with long battery life",
            "purchase_milestones": ["Purchased Model-X in Jan 2026"],
            "active_constraints": ["Budget under $300"]
        } # Only 50 tokens instead of 5,000!
        
    # 2. Selective JIT: Fetch detailed past reports ONLY when customer asks about them
    def handle_request(self, user_query, customer_id):
        prompt = assemble(self.get_compact_preferences(customer_id), user_query)
        if "compare with what you recommended last month" in user_query:
            prompt += fetch_detailed_history_jit(customer_id) # JIT on demand!
        return llm.generate(prompt)""",
        "options": [
            {
                "key": "A",
                "text": "Replace detailed historical recommendation reports with context-aware summaries that preserve only information needed for future reasoning.",
                "verdict": "正解（1つ目）！ 過去の長大な推薦レポート（比較表、キャンペーン文、長文推論）をそのまま残さず、将来の推薦に必要な重要情報（嗜好、制約、重要購入決定）だけを凝縮したコンテキスト認識型サマリーに置き換える（Compaction）ことで、トークン数を劇的に削減します。"
            },
            {
                "key": "B",
                "text": "Persist concise customer preference summaries while retrieving detailed recommendation history only when it is relevant to the current request.",
                "verdict": "正解（2つ目）！ 顧客の好みのサマリーは永続化して常時プロンプトに薄く保持しつつ、過去の詳細な推薦理由や比較などの重たい情報は、顧客から具体的に尋ねられた時だけオンデマンドで JIT 取得することで、コンテキスト圧迫を最小化します。"
            },
            {
                "key": "C",
                "text": "Use a hierarchical context storage system to store frequently accesses customer preferences and purchase history in a faster, more accessible layer.",
                "verdict": "誤り。階層型ストレージは『DBからのデータ読み込み速度（I/O）』を速くするインフラ技術であり、『LLMプロンプトに流し込むトークンサイズが増大して推論コストと遅延が悪化している』というコンテキストエンジニアリングのボトルネックを解決しません。"
            },
            {
                "key": "D",
                "text": "Implement a context expiration policy to automatically remove outdated recommendations summaries after a specified period.",
                "verdict": "誤り。時間経過だけで一律に自動削除すると、過去に購入した重要な履歴や、顧客の長期的な好みの定義まで消去されてしまい、推薦のパーソナライズ品質が損なわれます。"
            },
            {
                "key": "E",
                "text": "Precompute and cache all popular product recommendations so the assistant no longer needs to retrieve customer-specific context.",
                "verdict": "誤り。人気商品の推薦を使い回すと顧客ごとの個別化（Personalization）が完全に失われます。"
            }
        ],
        "correct": ["A", "B"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、レコメンドエージェントにおける**「コンパクション（Compaction）」と「選択的JIT取得（Selective JIT Retrieval）」によるコンテキスト最適化**を問う問題です。

1. **3層コンテキスト設計のベストプラクティス**:
   - **Compress（要約）**: 将来の推論に必要な情報（好み、制約）だけを抽出し、肥大化した推論レポートを圧縮する。
   - **Persist（永続化）**: 簡潔なプロファイルサマリーとして保持する。
   - **Retrieve Selectively（選択的JIT）**: 過去の詳細な経緯は常時プロンプトに入れず、リクエストで求められた時だけ取得する。

2. **「階層型ストレージ（C）」が誤答である理由**:
   - ストレージのI/Oを速くしても、LLMプロンプトに入るトークン数が多ければ、モデルの推論時間（数秒〜十数秒）とトークン課金は一切下がりません。
   - ボトルネックは「インフラの容量」ではなく「LLMのコンテキスト管理」です。""",
        "rules": [
            "Compress based on future usefulness: 単に古いものを捨てるのではなく、将来必要な情報に絞って圧縮する",
            "Concise Persistence + Selective JIT: 簡潔な嗜好サマリーを保持し、過去の詳細は必要時のみJIT取得する",
            "インフラ vs コンテキスト: 階層型ストレージやDB最適化はプロンプトトークン数を減らせないため誤答"
        ]
    },
    {
        "id": "R19",
        "num": 19,
        "type": "review",
        "domain": "Domain 6: Multi-Agent & Production Workflows",
        "category": "Domain 6: Multi-Agent and Long-Horizon Task Design",
        "title": "R19: Multi-Agent Boundary Placement: Specialization & Shared Summaries",
        "question": "Objective: Diagnose multi-agent boundary placement.\n\nA Databricks workflow relies on a single agent to handle multiple tasks including:\n- Planning\n- Data retrieval\n- Financial analysis\n- Chart generation\n- Report writing\n- Executive review\n\nAs the projects grow in size, the context windows approach capacity leading to deteriorated response quality.\n\nWhich architectural redesign would most effectively address this issue?",
        "code": """# Decomposing Monolithic Agent into Specialized Agents with Shared Summaries
# BAD: Single agent accumulates all 6 stages into one context!
# context = planning + raw_data + python_calc + chart_code + draft + review_notes (OVERLOAD!)

# GOOD: Clean agent boundaries with concise structured handoffs
planner_summary = planner_agent.run(project_goal) # -> goal & scope
research_summary = research_agent.run(planner_summary) # -> key findings & citations
analysis_summary = financial_agent.run(research_summary) # -> metrics & formulas
chart_artifacts = chart_agent.run(analysis_summary) # -> image URLs
report_draft = writer_agent.run(analysis_summary, chart_artifacts) # -> draft
approval = review_agent.run(report_draft) # -> approved / feedback""",
        "options": [
            {
                "key": "A",
                "text": "Split responsibilities into specialized agents with clearly defined interfaces and shared summaries, allowing for more efficient task distribution and reduces context window overload.",
                "verdict": "正解！ 6つの責務（企画〜レビュー）を個別の専門エージェントに分割し、明確なインターフェースと共有サマリー（Shared summaries）を介して連携させることで、下流のエージェントが前段の不要な生ログや計算過程を背負い込むのを防ぎ、コンテキストの過負荷を解消します。"
            },
            {
                "key": "B",
                "text": "Adopt a dynamic task allocation strategy, where tasks are assigned to available agents based on their current workload and capabilities, aiming to optimize resource utilization and minimize bottlenecks.",
                "verdict": "誤り。動的タスク割り当て（ロードバランシング）はサーバーの負荷分散には寄与しますが、エージェントが背負う『コンテキストの肥大化・アテンション希釈』という根本的なアーキテクチャ課題には直接対処しません。"
            },
            {
                "key": "C",
                "text": "Enhance the single agent's capabilities by integrating additional tools and plugins, increasing its capacity to handle complex tasks without compromising performance.",
                "verdict": "誤り。単一エージェントにさらにツールやプラグインを追加すると、ツールスキーマだけでプロンプトが肥大化し、どのツールを使うべきかモデルが迷子（Tool-selection ambiguity）になって悪化します。"
            },
            {
                "key": "D",
                "text": "Implement a hierarchical agent structure, where each task is managed by a separate sub-agent, but all sub-agents report to a central controlling agent.",
                "verdict": "誤り。すべてのサブエージェントが中央エージェントに全詳細を報告すると、中央エージェントのコンテキストウィンドウが破綻し、単一障害点になります。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、マルチエージェント設計における**「エージェントの境界配置（Boundary Placement）」と「専門化（Specialization）」**を問う問題です。

1. **単一エージェント（モノリス）の破綻理由**:
   - 1体に「企画」「検索」「分析」「作図」「執筆」「レビュー」をやらせると、前段の全コンテキスト（検索生データ、Pythonコード、ドラフト）が雪だるま式に蓄積します。
   - これにより、コンテキストウィンドウが満杯になり、モデルの注意力が散漫（Attention Dilution）になって回答精度が崩壊します。

2. **専門エージェントと共有サマリー（正解 A）**:
   - 各エージェントにタスク遂行に必要な最小限の情報のみを渡し、エージェント間は「構造化サマリー（Shared summaries）」のみでハンドオフします。
   - レポート執筆エージェントは、膨大な生ログを見ずに「分析メトリクスの要約」だけを見て執筆に集中できます。""",
        "rules": [
            "Specialized Agents: 1体のエージェントに多くの工程をやらせず、専門エージェントに分割する",
            "Shared Summaries: エージェント間のハンドオフは全履歴ではなく『共有サマリー』で行う",
            "Smallest Sufficient Context: 各エージェントにはその責務を果たすための最小十分なコンテキストだけを与える"
        ]
    },
    {
        "id": "R20",
        "num": 20,
        "type": "review",
        "domain": "Domain 6: Multi-Agent & Production Workflows",
        "category": "Domain 6: Multi-Agent and Long-Horizon Task Design",
        "title": "R20: Long-Horizon Workflow Resilience: Durable Checkpoints & Resumable Execution",
        "question": "A legal-tech company is deploying an AI audit agent to review 4,000 contracts over a three-day compliance window. During review, the agent must preserve references to earlier contract decisions, exceptions, and reviewer-approved interpretations. Some reviews may run for several hours, and the workflow must recover automatically if an agent process fails.\n\nWhich architecture best supports this workload?",
        "code": """# Long-Horizon Resilient Execution Pattern
class ResilientContractAuditor:
    def process_all_contracts(self, contracts):
        # 1. Resumable Execution: Load last successful checkpoint
        checkpoint = state_store.load_checkpoint()
        start_idx = checkpoint.get("last_processed_idx", 0)
        
        for idx in range(start_idx, len(contracts)):
            contract = contracts[idx]
            decision = self.audit_contract(contract, checkpoint.get("compact_rules"))
            
            # 2. Periodic Compaction & Durable Checkpoints
            if idx % 50 == 0:
                compact_rules = compact_precedents(checkpoint.get("rules"), decision)
                state_store.save_checkpoint({
                    "last_processed_idx": idx,
                    "compact_rules": compact_rules
                }) # Persisted to Delta Lake / external store!""",
        "options": [
            {
                "key": "A",
                "text": "Use durable checkpoints with periodic context compaction and resumable execution, allowing the agent to save its progress and resume from the last checkpoint in case of failure.",
                "verdict": "正解！ 4,000件・3日間にわたる長大タスクでは、耐久性のあるチェックポイント（Durable checkpoints）で進捗と決定事項を永続化し、定期的なコンパクションでコンテキスト爆発を防ぎ、クラッシュ時は最後のチェックポイントから再開（Resumable execution）するアーキテクチャが不可欠です。"
            },
            {
                "key": "B",
                "text": "Include all previous decisions in the prompt each time the agent processes a contract, effectively passing the entire history of decisions as input to the agent for each new contract review.",
                "verdict": "誤り。契約が進むにつれて過去の全決定がプロンプトに累積し、1,000件、4,000件と進むうちにトークン上限超過、コスト高騰、アテンション競合を引き起こします。"
            },
            {
                "key": "C",
                "text": "Maintain one uninterrupted conversation containing the entire review history, ensuring all context is preserved within a single, continuous interaction.",
                "verdict": "誤り。1つの会話スレッドに依存すると、数千件の対話でコンテキストが飽和する上、プロセスが予期せず終了した際に進行中の全作業が失われて最初からやり直しになります。"
            },
            {
                "key": "D",
                "text": "Store the agent's working state only in browser session storage, relying on the client-side storage to retain the necessary context for the review process.",
                "verdict": "誤り。ブラウザのセッションストレージはクライアント依存であり、タブを閉じたりセッションが切れたら消去されます。数日間のサーバーサイドのコンプライアンスバッチ処理には全く不適格です。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、数千件・数日間に及ぶ**長大タスク（Long-Horizon Task）における耐障害性と状態管理**を問う問題です。

1. **長大ワークフローの3大鉄則**:
   - **Checkpoint**: 途中の進捗と重要な決定・例外事項を Delta Lake などの外部ストアに確実に記録する。
   - **Compact**: 蓄積したコンテキストを定期的に圧縮し、プロンプトの肥大化を防ぐ。
   - **Resume**: 途中でプロセスが落ちても、最後のチェックポイントから即座に復旧・再開する。
   - **合言葉: 「Checkpoint $\rightarrow$ Compact $\rightarrow$ Resume」**

2. **会話履歴（Conversation history）を永続状態と混同してはならない**:
   - 会話履歴は揮発性の一時コンテキストに過ぎず、障害復旧の基盤にはなり得ません。""",
        "rules": [
            "Long-Horizon Task の3原則: Durable Checkpoint（保存） + Periodic Compaction（圧縮） + Resumable Execution（再開）",
            "会話履歴 != 永続状態: プロセスが落ちた時に備え、外部永続ストアにチェックポイントを取る",
            "全決定の再注入はアンチパターン: 4,000件の全決定をプロンプトに入れ続けるとトークンと遅延が爆発する"
        ]
    },
    {
        "id": "R21",
        "num": 21,
        "type": "review",
        "domain": "Domain 5: Tool & MCP",
        "category": "Domain 5: Tool Design, MCP, and Agent Context",
        "title": "R21: Tool & Data Source Overload: Just-In-Time Context Selection",
        "question": "A financial services company is building an AI-powered data analysis assistant that can access multiple data sources and analytical tools. The analysts conduct various investigations, each requiring a specific subset of the available data and tools.\n\nThe team wants to reduce unnecessary context passed to the model while maintaining accurate, efficient analysis.\n\nWhat approach would be best reduce unnecessary context passed to the model while maintaining accurate and efficient analysis?",
        "code": """# Progressive / JIT Tool & Data Retrieval
class AnalysisAgent:
    def handle_investigation(self, analyst_query: str):
        # BAD: Inject all 50 database schemas and 100 tool definitions upfront!
        
        # GOOD: Identify task intent and JIT-retrieve only relevant tools/schemas
        required_subset = tool_registry.resolve_needed_tools(analyst_query)
        # e.g., only ['fetch_regional_revenue', 'plot_bar_chart']
        
        system_prompt = build_minimal_prompt(tools=required_subset)
        return llm.generate(system_prompt, analyst_query)""",
        "options": [
            {
                "key": "A",
                "text": "Utilize just-in-time retrieval to provide the model with only the data sources and tools relevant to its current analysis context.",
                "verdict": "正解！ 多数のツールやデータソースが存在しても、各調査で必要なのは一部です。推論直前に現在の分析タスクに関連するツール定義とデータソースのみをジャストインタイム（JIT）取得して提供することで、不要なコンテキストを削ぎ落とし、ツールの選択ミス（Tool-selection ambiguity）を防ぎます。"
            },
            {
                "key": "B",
                "text": "Implement a comprehensive data warehouse that stores all possible data sources and tools, ensuring the model has access to all information.",
                "verdict": "誤り。DWHに全データを集約しても、プロンプトに何をどう渡すかというコンテキスト管理問題は解決せず、全情報を渡そうとすればコンテキスト肥大化が悪化します。"
            },
            {
                "key": "C",
                "text": "Design a dynamic system prompt that incorporates detailed documentation for every available data source and tool, allowing the model to select the appropriate resources.",
                "verdict": "誤り（超重要トラップ！）。すべてのツールの詳細ドキュメントをプロンプトに埋め込むと、使わないツールの説明だけでコンテキストが埋まり、トークンコスト高騰とアテンション散漫を招きます。"
            },
            {
                "key": "D",
                "text": "Develop a unified platform that integrates all data sources and analytical tools, enabling the model to operate within a single, cohesive environment.",
                "verdict": "誤り。単一プラットフォームへの統合はインフラの話であり、モデルのコンテキストウィンドウに不要な情報が入り込む根本課題を解決しません。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、ツールやデータソースが膨大にある場合の**「JIT取得（Just-In-Time Retrieval）によるコンテキスト最小化」**を問う問題です。

1. **ツール過多（Tool Overload）の弊害**:
   - 100個のツール仕様書を最初から全部システムプロンプトに書くと、プロンプトの大部分がツール定義で埋まります。
   - モデルは関係ないツールの説明に惑わされ、誤ったツールを呼び出す確率が高まります。

2. **JIT取得 / Progressive Disclosure の威力**:
   - ユーザーの質問からタスクを特定し、**「今回必要な3〜4個のツールとスキーマだけ」を動的に取得してプロンプトに渡す**。
   - これにより、トークン消費を最小限に抑えつつ、最高精度のツール呼び出しを実現できます。""",
        "rules": [
            "JIT Tool Selection: 多数のツールがある場合は最初から全提示せず、タスクに必要なサブセットのみJIT取得する",
            "Expose all tools upfront は誤答: 全ツールのドキュメントをプロンプトに入れる選択肢は常にコンテキスト肥大化の罠",
            "Tool-Selection Ambiguity 防止: 選択肢を最小限に絞ることでモデルの誤呼び出しを根絶する"
        ]
    },
    {
        "id": "R22",
        "num": 22,
        "type": "review",
        "domain": "Domain 2: Context Compression",
        "category": "Domain 2: Context Compression and Compaction",
        "title": "R22: Core Purpose of Context Compaction: Preserve Meaning, Reduce Footprint",
        "question": "A large e-commerce company is experiencing rapid growth in their online sales, leading to a significant increase in the volume of customer interactions and order data. The company's data engineering team is tasked with optimizing the performance and scalability of their data processing pipeline. One key challenge they face is the growing size of the context data, which is impacting the efficiency of their machine learning models.\n\nWhat is the primary purpose of implementing a compaction strategy in this scenario?",
        "code": """# Context Compaction: Semantics Preserved, Footprint Reduced
# Raw customer interactions: 10,000 tokens of chat logs & order events
raw_history = [
    "User complained about shipping delay on Jan 5...",
    "Support refunded $20 on Jan 6...",
    "User asked for size 10 black boots on Feb 1...",
    "... (90 more turns) ..."
]

# Compacted Representation: 150 tokens
compact_context = {
    "preferences": "Prefers size 10 footwear, black color",
    "account_status": "Past shipping issue resolved with $20 credit",
    "active_cart": "None"
}
# Result: Model processes 150 tokens with 100% semantic grounding!""",
        "options": [
            {
                "key": "A",
                "text": "Preserve the historical context while reducing the data footprint to enhance model efficiency.",
                "verdict": "正解！ コンパクション（Compaction）の本質は、過去のやり取りや注文データに含まれる『将来の推論に必要な重要情報（嗜好、解決状況、制約）』を保持したまま、不要な長文ログを圧縮してデータフットプリント（トークン数）を削減し、モデルの処理効率を高めることです。"
            },
            {
                "key": "B",
                "text": "Improve model accuracy by increasing the density of historical customer interaction data.",
                "verdict": "誤り。コンパクションの主目的は不要なトークンを削減することであり、データの密度を高めてトークンを増やすことではありません。"
            },
            {
                "key": "C",
                "text": "Enhance data retrieval speed by reorganizing context data into more accessible formats.",
                "verdict": "誤り。データの再編成による検索速度向上はインデックス作成（Indexing）やキャッシュの目的であり、コンテキストコンパクションの定義ではありません。"
            },
            {
                "key": "D",
                "text": "Reduce the overall storage requirements for the context data while maintaining recent interactions.",
                "verdict": "誤り（最大のトラップ！）。ストレージ容量（Storage requirements）の削減は物理ディスク圧縮（GzipやParquet等）の目的です。本問の課題は『MLモデル/LLMの処理効率（コンテキストウィンドウ圧迫）』であるため、対象レイヤーが異なります。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、コンテキストエンジニアリングにおける**「コンパクション（Compaction）の真の目的」と他概念との識別**を問う問題です。

1. **各概念の明確な切り分け**:
   - **Compaction（コンパクション）**: 重要情報（意味論）を保持しつつ、モデルに渡すトークン量を削減する（⭕ 正解）。
   - **Truncation（切り捨て）**: 古いものを機械的に消す（❌ 重要な前提が消える）。
   - **Deletion（削除）**: データを恒久的に消去する。
   - **Storage compression（ストレージ圧縮）**: 物理ディスク容量を減らす（❌ LLMのトークン数は減らない）。

2. **コンパクションの鉄則**:
   - **「Compaction reduces context size while retaining task-relevant information.」**
   （コンパクションとは、タスクに関連する情報を保持しながらコンテキストサイズを縮小することである。）""",
        "rules": [
            "Compaction の定義: 重要情報を保持（Preserve）しながら、トークンフットプリントを削減（Reduce footprint）する",
            "Storage Compression と混同するな: 物理ディスクの節約ではなく、モデルに渡すコンテキストの圧縮が目的",
            "Compaction != Deletion: 単に古い履歴を消すのではなく、重要なエッセンスを凝縮して残す"
        ]
    },
    {
        "id": "R23",
        "num": 23,
        "type": "review",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Context Management and Lakebase Memory",
        "title": "R23: Managing IoT Sensor Data Retention in Lakebase: Time-Series Auto-Aging",
        "question": "Your organization is building a real-time analytics platform that ingests high-volume sensor data from IoT devices. To ensure low-latency access to the most recent data, the team plans to use Lakebase to store the sensor readings.\n\nWhat is the recommended approach to manage the retention of this sensor data?",
        "code": """# Lakebase Native Time-Series Retention Configuration
# CREATE TABLE iot_sensor_readings (...)
# TBLPROPERTIES (
#   'lakebase.timeseries.enabled' = 'true',
#   'lakebase.timeseries.timestampCol' = 'event_timestamp',
#   'lakebase.retention.policy' = 'CONFIGURABLE_AGE_OUT',
#   'lakebase.retention.duration' = '14 DAYS' -- Automatically purged by Lakebase!
# );
#
# No manual DELETE jobs, no Delta Time Travel misuse! Native lifecycle management.""",
        "options": [
            {
                "key": "A",
                "text": "Leverage Lakebase's time-series data management features to automatically age out sensor data based on a configurable retention policy.",
                "verdict": "正解！ IoTセンサーなどの高頻度時系列データに対しては、Lakebase にネイティブに備わっている時系列データ管理機能（Time-series data management）を活用し、業務要件に合わせた設定可能な保持ポリシー（Configurable retention policy）によって古いデータを自動的に期限切れ（Age out）させるのが推奨アプローチです。"
            },
            {
                "key": "B",
                "text": "Configure a TTL policy on the Lakebase table to automatically delete records older than 30 days.",
                "verdict": "誤り。一見TTLとしてもっともらしく見えますが、業務要件を確認せずに『30日固定』という恣意的な数値を指定している点、および時系列データ専用のマネージド機能に言及していない点で劣ります。"
            },
            {
                "key": "C",
                "text": "Use Delta Lake time travel capabilities to manually delete old sensor data as needed, ensuring data consistency and versioning.",
                "verdict": "誤り。Delta Lake のタイムトラベルは過去の特定時点のデータを参照・復元するための機能であり、運用データの自動削除メカニズムではありません。手動削除を強いる点も不適切です。"
            },
            {
                "key": "D",
                "text": "Implement a Databricks job that periodically compacts the Lakebase table to remove old data based on a custom retention policy.",
                "verdict": "誤り。プラットフォームがネイティブなライフサイクル管理機能を提供しているにもかかわらず、手動で定期実行バッチジョブ（Scheduled job）を組んで保守運用するのは無駄な運用オーバーヘッドです。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、Lakebase における**「時系列センサーデータのネイティブ保持期間管理（Lifecycle / Retention）」**を問う問題です。

1. **時系列データ（Time-Series Data）の特性**:
   - センサーデータは「直近の最新データは低遅延で読みたいが、古くなったデータは自動的に消えてほしい」という明確な時間減衰パターンを持ちます。
   - これに対して手動削除ジョブやカスタムスクリプトを書くのは非推奨です。

2. **Lakebase の推奨アプローチ（正解 A）**:
   - Lakebase に組み込まれた時系列ライフサイクル機能を使用し、**「設定可能な保持ポリシー（Configurable retention policy）」**で古いデータを自動的にエージングアウト（Age-out）させます。
   - 開発者が削除バッチのスケジュールや失敗ハンドリングを自作する必要がありません。""",
        "rules": [
            "IoT / Time-Series Retention: Lakebase のネイティブな時系列エージングアウト（Automatic age-out）を活用する",
            "カスタムジョブは避ける: プラットフォームに自動機能がある場合、Databricks定期ジョブで手動削除するのは誤答",
            "Time Travel != Deletion: タイムトラベルは過去バージョンの参照機能であり、データ削除の仕組みではない"
        ]
    },
    {
        "id": "R24",
        "num": 24,
        "type": "review",
        "domain": "Domain 6: Multi-Agent & Production Workflows",
        "category": "Domain 6: Multi-Agent and Long-Horizon Task Design",
        "title": "R24: Reducing Orchestrator Context Load: Sub-Agent Structured Handoffs",
        "question": "Objective: Reduce orchestrator context load without losing task coherence.\n\nA coordinator agent delegates 12 subtasks to specialized agents.\nEach sub-agent currently returns:\n- its complete reasoning trace,\n- every tool response,\n- intermediate calculations,\n- final conclusion.\n\nThe coordinator uses only the final conclusion, confidence level, and unresolved dependencies when deciding the next step.\n\nWhat change would most directly reduce context consumption?",
        "code": """# Structured Sub-Agent Handoff Contract
# BAD: Raw Sub-Agent Return (5,000 tokens per sub-agent * 12 = 60,000 tokens!)
# return {"full_trace": "...", "tool_responses": [raw_json_1, raw_json_2], ...}

# GOOD: Structured Task Summary (Only 150 tokens per sub-agent!)
class SubAgentHandoff(BaseModel):
    conclusion: str                  # e.g., "Supplier risk is MEDIUM"
    confidence: float                 # e.g., 0.88
    evidence_references: List[str]   # e.g., ["doc_id:sec_10k_p44", "order_id:991"]
    unresolved_dependencies: List[str] # e.g., ["pending_legal_clearance"]

# Coordinator receives only this concise contract!""",
        "options": [
            {
                "key": "A",
                "text": "Ask sub-agents to return structured task summaries containing the conclusion, confidence, supporting evidence references, and unresolved dependencies.",
                "verdict": "正解！ コーディネーターが必要としている情報（結論、確信度、証拠の参照リンク、未解決の依存関係）のみを定義した『構造化タスクサマリー（Structured task summaries）』を出力コントラクトとして規定することで、12個のサブエージェントから膨大な推論生ログが親に流入するのを元から防ぎ、コンテキスト消費を劇的に削減します。"
            },
            {
                "key": "B",
                "text": "Increase the coordinator's context window so complete sub-agent traces for potential future reference.",
                "verdict": "誤り。親エージェントのコンテキストウィンドウを拡大しても、不要な冗長ログをすべて読み込ませる構造は変わらず、トークン消費と推論遅延が増加するだけです。"
            },
            {
                "key": "C",
                "text": "Design a caching mechanism to store sub-agent traces in a temporary buffer, allowing the coordinator to retrieve them as needed.",
                "verdict": "誤り。バッファキャッシュは監査や詳細調査には役立ちますが、サブエージェントが親に過剰なデータを返しているという根本問題を直接解決しません。"
            },
            {
                "key": "D",
                "text": "Implement a lossless compression algorithm to reduce the size of sub-agent outputs before passing them to the coordinator.",
                "verdict": "誤り。可逆圧縮した文字列を渡してもLLMは自然言語として直接理解できません。最初から不要な情報を削ぎ落とした構造化サマリーを返させるべきです。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、マルチエージェント協調における**「サブエージェントから親へのハンドオフ・コントラクト（Handoff Contract）」**を問う問題です。

1. **受取手（Consumer）が必要とする情報だけを返す**:
   - 12個のサブタスクから「思考プロセス全部、ツールの生レスポンス全部」を受け取ったら、親エージェントはパンクします。
   - 親が必要としているのは「次の行動を決めるための4つのフィールド」だけです。
     - **Final conclusion**（最終結論）
     - **Confidence level**（確信度）
     - **Supporting evidence references**（証拠のID・参照先）
     - **Unresolved dependencies**（未解決の依存関係）

2. **証拠参照（Evidence references）の役割**:
   - 生データを全部渡すのではなく、「文書IDや取引番号」などの参照（ポインタ）だけを渡すことで、トレーサビリティを確保しつつトークンを激減させます。""",
        "rules": [
            "Structured Task Summaries: サブエージェントには推論全ログではなく、構造化サマリーを返させる",
            "API Contract の発想: 親エージェントが次の判断に必要なフィールドだけをコントラクトとして定義する",
            "Evidence References: 生データを全部渡さず、証拠への参照リンク（ポインタ）を渡す"
        ]
    },
    {
        "id": "R25",
        "num": 25,
        "type": "review",
        "domain": "Domain 6: Multi-Agent & Production Workflows",
        "category": "Domain 6: Multi-Agent and Long-Horizon Task Design",
        "title": "R25: Overcoming Monolithic LLM Bottlenecks: Distributed Multi-Model Architecture",
        "question": "A large e-commerce platform is experiencing significant performance issues due to the growing volume of customer interactions and product data. The current architecture relies on a single, monolithic language model to process all incoming requests, leading to unacceptable latency and context window pressure.\n\nWhat is the best architectural approach to address these challenges?",
        "code": """# Monolithic vs Distributed Multi-Model Architecture
# BOTTLE NECK: Single Monolithic Model
# [All Requests] ===> [Gigantic 70B Model with 100 tools & all context] ===> SLOW & EXPENSIVE!

# SOLUTION: Distributed Multi-Model Architecture with Routing
def handle_incoming_request(request):
    intent = router.classify(request) # Fast & lightweight classification
    
    if intent == "PRODUCT_SEARCH":
        return catalog_specialized_model.run(request)   # Optimized for search
    elif intent == "ORDER_SUPPORT":
        return support_specialized_model.run(request)   # Optimized for ticketing
    elif intent == "RECOMMENDATION":
        return recommendation_engine.run(request)       # Optimized for ranking""",
        "options": [
            {
                "key": "A",
                "text": "Implement a distributed, multi-model architecture with specialized models for different data types and use cases allowing for more efficient processing and reduced latency.",
                "verdict": "正解！ 単一のモノリシックモデルに全責務を負わせるのをやめ、データ型やユースケース（商品検索、問い合わせ、レコメンド等）に応じて専門化されたモデル群に分散させることで、各モデルが最小限のコンテキストで効率的に処理できるようになり、遅延を大幅に削減できます。"
            },
            {
                "key": "B",
                "text": "Develop a hybrid approach that combines the strengths of batch-oriented data pipelines and real-time language models, enabling the platform to handle both historical data analysis and instantaneous customer interactions.",
                "verdict": "誤り。バッチ処理へのオフロードは分析ワークロードには有効ですが、リアルタイム対話リクエストにおけるコンテキスト圧迫と遅延の根本解決にはなりません。"
            },
            {
                "key": "C",
                "text": "Design a hierarchical language model that can adaptively allocate resources based on the complexity of incoming requests, prioritizing real-time interactions and optimizing context window utilization.",
                "verdict": "誤り。計算リソースの適応型割り当てはインフラの最適化にとどまり、1つのモデルが全リクエストの過剰なコンテキストを抱え込むという根本設計を是正しません。"
            },
            {
                "key": "D",
                "text": "Introduce a context summarization layer to progressively disclose relevant information to the language model, reducing the dimensionality of the input data and mitigating context window pressure.",
                "verdict": "誤り。要約層の導入はコンテキスト削減手法の一つですが、本問が問うている『モノリシックモデルによる単一障害点とスケーラビリティの限界』を解決する包括的なアーキテクチャ再設計（B）には及びません。"
            }
        ],
        "correct": "A",
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、**「モノリシック（一枚岩）モデルの限界」と「分散型マルチモデル（Distributed Multi-Model）への分解」**を問う問題です。

1. **なぜ単一モノリシックモデルは破綻するのか？**:
   - ECサイトには「商品検索」「FAQ対応」「注文変更」「パーソナライズ推薦」など全く性質の異なるリクエストが殺到します。
   - 1つの超巨大モデルにこれら全てを処理させようとすると、あらゆるツールのスキーマやドキュメントを常にロードする必要があり、遅延とコンテキスト圧迫が爆発します。

2. **分散型マルチモデルアーキテクチャの原則**:
   - **「Decompose broad responsibilities into specialized components.」**
   - リクエストをルーターで分類し、専門化された小型・軽量モデル（または特化型コンポーネント）に振り分けることで、独立したスケーラビリティと超低遅延を実現します。""",
        "rules": [
            "Monolithic LLM の限界: 単一巨大モデルに全責任を負わせず、専門モデルに分散（Distributed Multi-Model）させる",
            "Specialization by Use Case: 検索、サポート、推薦などユースケースごとに特化したモデルを用意する",
            "Decompose & Route: リクエストを分類し、最も適した専門コンポーネントに最小コンテキストでルーティングする"
        ]
    },
    {
        "id": "R26",
        "num": 26,
        "type": "review",
        "domain": "Domain 4: Memory Architecture",
        "category": "Domain 4: Context Management and Lakebase Memory",
        "title": "R26: Recommendation Agent Memory Architecture: Cache + Lakebase Persistent Store (Select TWO)",
        "question": "Objective: Select the appropriate memory architecture for personalized recommendation agents.\n\nA global retail company is building a Databricks-powered AI shopping assistant that recommends personalized product bundles. During each customer interaction, the assistant uses:\n- Customer preferences (favorite brands, sizes, budget)\n- Purchase history spanning several years\n- Recently viewed products during the current session\n- Current shopping cart contents\n\nProduction monitoring shows:\n- Long-term customer preferences change infrequently.\n- Shopping cart contents and browsing activity change continuously during a session.\n- Querying the customer profile service for every request increases response latency.\n- Customer data must remain available across sessions and application restarts.\n\nThe architects want to:\n1. Minimize repeated lookups for stable customer information.\n2. Preserve long-term personalization across multiple sessions.\n3. Avoid placing the entire customer history into every LLM prompt.\n\nWhich TWO memory architecture patterns BEST satisfy these requirements?",
        "code": """# Cache-Aside + Persistent Store Pattern
class RetailRecommendationEngine:
    # Layer 1: Distributed Cache (Fast lookup for stable preferences)
    @cache.cached(key="profile:{user_id}", ttl=3600)
    def get_cached_preferences(self, user_id):
        # Layer 2: Lakebase (Authoritative Master Store)
        return lakebase.query_user_profile(user_id)
        
    def recommend(self, user_id, current_cart, user_query):
        # 1. Fetch stable preferences in 1ms from Cache!
        prefs = self.get_cached_preferences(user_id)
        
        # 2. Selective JIT: Retrieve ONLY relevant past purchases (NOT entire history!)
        relevant_history = lakebase.vector_search_purchases(
            user_id=user_id, query=user_query, top_k=3
        )
        
        # 3. Layer 3: Working context (Current cart & query)
        prompt = assemble_prompt(prefs, relevant_history, current_cart, user_query)
        return llm.generate(prompt)""",
        "options": [
            {
                "key": "A",
                "text": "Maintain a distributed cache for frequently accessed customer profiles and preferences to reduce repeated retrieval latency, ensuring data is updated in real-time to reflect changing customer behavior.",
                "verdict": "正解（1つ目）！ 顧客の好みやプロファイルは滅多に変わらない（Infrequently）にもかかわらず、毎リクエストDBへ問い合わせると遅延が悪化します。分散キャッシュ（Distributed cache）を維持することで、重複検索の遅延をミリ秒単位に短縮します。"
            },
            {
                "key": "B",
                "text": "Store long-term customer preferences and purchase history in persistent memory such as Lakebase, retrieving only relevant information when needed to minimize data transfer and optimize system performance.",
                "verdict": "正解（2つ目）！ 数年分の購買履歴や長期設定を Lakebase などの永続メモリ（Persistent memory）に保存し、アプリ再起動やセッションを跨いでも消失しないようにします。さらに、全履歴を毎プロンプトに流し込まず『必要な情報のみを選択的JIT取得』することで、コンテキスト圧迫を防止します。"
            },
            {
                "key": "C",
                "text": "Implement a hybrid approach combining a distributed cache for frequently accessed customer profiles with a persistent store like Lakebase for long-term customer preferences and purchase history.",
                "verdict": "誤り。文脈上スクラッチパッドや作業メモリを永続化に使おうとする不完全な代替案として出題されており、A と B の具体的な機能分離が正解となります。"
            },
            {
                "key": "D",
                "text": "Utilize an in-memory data grid to store customer preferences and purchase history, allowing for fast access and minimizing the need for disk storage, but ensuring data persistence across sessions through regular snapshots.",
                "verdict": "誤り。インメモリデータグリッドに全履歴を置いても、『プロンプトに全履歴を入れずに必要な情報だけを厳選して渡す』というコンテキスト管理要件を解決しません。"
            },
            {
                "key": "E",
                "text": "Replace persistent customer memory with a larger LLM context window so previous shopping behavior can remain in memory indefinitely.",
                "verdict": "誤り（最悪のアンチパターン！）。コンテキストウィンドウは永続ストレージではありません。アプリ再起動で消去され、数年分の履歴を毎プロンプトに入れるためコストと遅延が爆発します。"
            }
        ],
        "correct": ["A", "B"],
        "correctCount": 2,
        "explanation": """【問題の診断とアーキテクチャの核心】
本問は、EC推薦エージェントにおける**「分散キャッシュ（速度向上）」と「Lakebase永続化 ＋ 選択的JIT取得（耐久性＆トークン抑制）」の2層ハイブリッド設計**を問う問題です。

1. **「キャッシュ」と「Lakebase」に両方入れる理由**:
   - **Lakebase（原本・永続ストア）**:
     顧客が数週間後に戻ってきても、アプリが再起動しても、絶対にデータを消さないためのマスターデータストア。
   - **分散キャッシュ（高速コピー）**:
     同一セッション中や高頻度アクセス時に、毎回LakebaseにSELECTクエリを投げる遅延を防ぐための高速読み出し用コピー。

2. **3大要件と対応ソリューション**:
   - **重複問い合わせ遅延の削減** $\rightarrow$ **分散キャッシュ（A）**
   - **セッション跨ぎ・再起動後の永続化** $\rightarrow$ **Lakebase永続メモリ（B）**
   - **全履歴をプロンプトに入れない** $\rightarrow$ **必要な情報のみ選択的取得（B）**""",
        "rules": [
            "Cache + Lakebase ハイブリッド: 原本は Lakebase に永続化し、高速読み出しのために分散キャッシュにコピーを置く",
            "Selective JIT for Long History: 数年分の購入履歴はプロンプトに全ロードせず、今回の質問に関連するものだけをJIT取得する",
            "Context Window is NOT Storage: コンテキスト窓の拡大はアプリ再起動に耐えられず永続化の代替にならない"
        ]
    }
]



