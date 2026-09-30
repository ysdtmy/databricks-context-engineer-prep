# build_data.py
# Generate complete data.js for Databricks Certified Context Engineer Associate Portal

import json

guide_chapters = [
    {
        "id": "ch-overview",
        "title": "1. 試験概要 & 出題シラバス",
        "content": """
<p class="guide-p">Databricks Certified Context Engineer Associate は、2026年5月の Data + AI Summit で発表された、AI エージェントの本番運用（Production-grade）における「推論時コンテキスト制御・メモリ管理・ツール連携」を評価・認定する業界初の専門資格です。</p>
<div class="table-container"><table class="guide-table">
<thead><tr><th>項目</th><th>詳細仕様</th></tr></thead><tbody>
<tr><td>試験名</td><td>Databricks Certified Context Engineer Associate</td></tr>
<tr><td>問題数</td><td>45問（多肢選択式・シナリオ問題中心）</td></tr>
<tr><td>制限時間</td><td>90分（1問あたり約2分）</td></tr>
<tr><td>言語</td><td><strong>英語のみ（問題文・選択肢とも英語、コードはPython/SQL）</strong></td></tr>
<tr><td>合格ライン</td><td>約70%（約32問正解）</td></tr>
<tr><td>受験方式</td><td>オンラインプロクター監視 (Kryterion / Webassessor) またはテストセンター</td></tr>
<tr><td>参照資料</td><td><strong>持ち込み不可（APIドキュメント等の参照不可）</strong></td></tr>
<tr><td>有効期間</td><td>2年間</td></tr>
</tbody></table></div>

<h3 class="guide-h3">出題ドメイン構成比（7 Domains）</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>ドメイン</th><th>配点比率</th><th>本番出題数目安</th><th>主要トピック</th></tr></thead><tbody>
<tr><td>Domain 1: Foundations of Context Engineering</td><td>20%</td><td>約9問</td><td>コンテキスト4大障害、推論モード、アテンションバジェット、スタック選定</td></tr>
<tr><td>Domain 2: System Prompt & Instruction Design</td><td>15%</td><td>約7問</td><td>AI/BI Genie スペース、Trusted Assets、Few-shot選定、プロンプト修正</td></tr>
<tr><td>Domain 3: Knowledge Retrieval & Governance</td><td>15%</td><td>約7問</td><td>Unity Catalog ガバナンス、AI Search、チャンキング戦略、Pre-inference vs JIT</td></tr>
<tr><td>Domain 4: Memory Architecture with Lakebase</td><td>15%</td><td>約7問</td><td>Lakebase、In-context vs Delta-backed State、意図解決、過剰取得防止</td></tr>
<tr><td>Domain 5: Tool & Action Design with MCP</td><td>15%</td><td>約7問</td><td>Model Context Protocol (MCP)、Progressive Disclosure、プルーニング、Agent Skills</td></tr>
<tr><td>Domain 6: Compression & Compaction Strategies</td><td>10%</td><td>約4問</td><td>Recall First 原則、安全な破棄対象、Trimming vs Compaction</td></tr>
<tr><td>Domain 7: Multi-Agent Systems & Long-Horizon Tasks</td><td>10%</td><td>約4問</td><td>親トレース漏洩防止、オーケストレーター飽和防止、境界設計、チェックポイント</td></tr>
</tbody></table></div>
"""
    },
    {
        "id": "ch-domain1",
        "title": "2. Domain 1: コンテキストエンジニアリングの基礎と障害分析 (20%)",
        "content": """
<p class="guide-p">本ドメインでは、LLMのコンテキストウィンドウ内で発生する異常の診断と、プロアクティブな制御手法が問われます。特に<strong>コンテキスト障害の4大分類</strong>は本試験の最重要基礎です。</p>

<h3 class="guide-h3">コンテキスト障害の4大分類（必須暗記）</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>障害モード</th><th>根本原因</th><th>典型的症状</th><th>Databricks での推奨対策</th></tr></thead><tbody>
<tr><td><strong>Context Poisoning（汚染）</strong></td><td>信頼できない外部検索、ドラフト文書、不正入力がコンテキストに混入</td><td>誤った前提やデマを事実として受け入れ、後続推論全体が狂う</td><td>Unity Catalog で Authoritative（認定正規データ）のみに検索スコープを制限、データ検証ガードレール</td></tr>
<tr><td><strong>Context Distraction（注意散漫）</strong></td><td>大量の生ログ、不要な長文テーブル、低品質な検索チャンクの過剰流入</td><td>システムプロンプトの重要制約（例: 出力JSON形式）を見落とす</td><td>Markdown構造化チャンキング、生ツール出力のプルーニング、JITスキーマ取得</td></tr>
<tr><td><strong>Context Confusion（混同）</strong></td><td>類似したツール名・説明文、同名カラムの存在による境界曖昧性</td><td>誤ったツールを呼び出す、引数の型や意味を取り違える</td><td>ツールの説明文（Description）で用途と差別化を明確化、明確な命名規則</td></tr>
<tr><td><strong>Context Clash（衝突）</strong></td><td>プロンプト内の指示同士、またはプロンプトと検索ドキュメント間の矛盾</td><td>エージェントのデッドロック、回答の揺らぎ、指示無視</td><td>システムプロンプトで明確な優先順位ルール（例: 社内規程 ＞ 外部資料）を明示</td></tr>
</tbody></table></div>

<div class="mermaid-card"><div class="mermaid-header"><span>📊 障害モード診断フローチャート</span></div>
<pre class="mermaid">flowchart TD
    Start[エージェントの推論失敗] --> Q1{誤情報・非公式データを真実と信じている?}
    Q1 -- Yes --> Poisoning["🚨 Context Poisoning<br/>(汚染: 信頼できないデータ流入)"]
    Q1 -- No --> Q2{重要な指示や制約を見落としている?}
    Q2 -- Yes --> Distraction["🌪️ Context Distraction<br/>(注意散漫: トークン過多で埋没)"]
    Q2 -- No --> Q3{似たツールやカラムの選択を間違えている?}
    Q3 -- Yes --> Confusion["🔀 Context Confusion<br/>(混同: 類似定義による判断迷い)"]
    Q3 -- No --> Clash["⚔️ Context Clash<br/>(衝突: 矛盾する指示・ルールの競合)"]
</pre></div>

<h3 class="guide-h3">Reasoning Mode（推論モード）の使い分け</h3>
<ul class="guide-list">
<li><strong>Standard</strong>: 通常のマルチターン対話や定型的なタスク。</li>
<li><strong>Extended Thinking</strong>: 複雑な構文解析、マルチホップ推論、高度なコード生成、数理検証。追加の推論トークンを消費するため、トークンバジェットの厳密な監視が必要。</li>
<li><strong>Reduced Thinking</strong>: 単純なキーワード抽出、固定フォーマット変換、センチメント分類。レイテンシとコストを極小化。</li>
</ul>
"""
    },
    {
        "id": "ch-domain2",
        "title": "3. Domain 2: プロンプト設計 & Genie スペース (15%)",
        "content": """
<p class="guide-p">プロンプトを長文化させるのではなく、Databricks のデータ資産（Unity Catalog, Genie Space）と協調させる設計が問われます。</p>

<h3 class="guide-h3">AI/BI Genie スペースのキュレーション原則</h3>
<ul class="guide-list">
<li><strong>Trusted Assets（信頼できる資産）の優先</strong>: 複雑な売上集計や解約率計算をLLMのアドホックSQL生成に頼るとハルシネーションを起こす。検証済みの<strong>SQL UDF、集計ビュー、パラメータ化クエリ</strong>を Unity Catalog に作成し、Genie の Trusted Asset として登録する。</li>
<li><strong>Few-shot の限界貢献度（Marginal Contribution）</strong>: 成功例を無暗に増やすとトークンを圧迫する。「エージェントが過去に失敗したエッジケース」「特殊なJSON出力スキーマの強制」「曖昧な質問に対する聞き返し」など、効用の高い2〜3例に絞る。</li>
<li><strong>メタデータの整備</strong>: テーブルコメントやカラムコメント（`COMMENT ON COLUMN`）にコード値（'A'=Active, 'S'=Suspendedなど）の定義を記載する。</li>
</ul>
"""
    },
    {
        "id": "ch-domain3",
        "title": "4. Domain 3: 知識検索 & ガバナンス (15%)",
        "content": """
<p class="guide-p">RAG パイプラインにおける情報選別と、Unity Catalog ガバナンスの適用を学習します。</p>

<h3 class="guide-h3">Pre-inference vs Just-in-Time (JIT) Agentic Retrieval</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>方式</th><th>実行タイミング</th><th>適したシナリオ</th><th>メリット・制約</th></tr></thead><tbody>
<tr><td><strong>Pre-inference（事前取得）</strong></td><td>ユーザー入力直後、推論開始前</td><td>静的なFAQ検索、単一ステップのQA</td><td>シンプルだが、複数ステップや動的な深掘りには対応不可</td></tr>
<tr><td><strong>JIT Retrieval（動的検索）</strong></td><td>エージェントの推論途中（ツール呼出）</td><td>動的なSQL集計、マルチホップ調査、条件分岐</td><td>必要な差分のみ取得してトークンを節約できるが、レイテンシが増加</td></tr>
</tbody></table></div>

<h3 class="guide-h3">チャンキング戦略の選定</h3>
<ul class="guide-list">
<li><strong>局所的情報（API引数、エラーコード）</strong>: Markdown構造化チャンキングを用い、256〜512トークンの小チャンクに親ドキュメントのメタデータを付与して管理。無関係なノイズを排除。</li>
<li><strong>広域的サマリー</strong>: 階層的チャンキングや要約レイヤーを活用。</li>
<li><strong>ハイブリッド検索（Hybrid Search）</strong>: 特殊な専門用語や型番にはBM25キーワード検索、概念理解には高次元ベクトル類似度検索を組み合わせる。</li>
</ul>
"""
    },
    {
        "id": "ch-domain4",
        "title": "5. Domain 4: メモリ設計と Lakebase (15%)",
        "content": """
<p class="guide-p">会話内の短期記憶と、Databricks Lakebase / Delta Lake を用いた永続的な長期記憶の役割分担を理解します。</p>

<h3 class="guide-h3">短期記憶 vs 長期永続メモリ</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>メモリ種別</th><th>保持場所</th><th>ライフサイクル</th><th>典型的な用途</th></tr></thead><tbody>
<tr><td><strong>In-context Scratchpad</strong></td><td>プロンプト内（短期）</td><td>単一セッション・推論中のみ</td><td>計算の中間変数、現在のサブゴール、推論トレース</td></tr>
<tr><td><strong>Session History</strong></td><td>メッセージ配列（短期）</td><td>ユーザー対話の1セッション</td><td>指示代名詞（「先ほどの件」）の解決、直近の文脈</td></tr>
<tr><td><strong>Delta-backed State / Lakebase</strong></td><td>Delta テーブル（長期）</td><td>永続（複数日・複数セッション）</td><td>ユーザー嗜好、長期ワークフロー状態、耐障害性復旧</td></tr>
</tbody></table></div>

<h3 class="guide-h3">メモリ検索の注意点</h3>
<ul class="guide-list">
<li><strong>Intent Resolution（意図解決）</strong>: 「先ほど提案された2つ目について」などの代名詞は、外部メモリではなくまず直前の会話履歴（Session History）で解決してから検索を実行する。</li>
<li><strong>確定キーには構造化クエリ</strong>: `user_id = 'U123'` のような一意キーにはベクトル類似度検索を使わず、SQL / Key-Value 等の構造化クエリを用いる。</li>
<li><strong>Over-retrieval の防止</strong>: 過去の履歴を無差別に数十件コンテキストにロードすると、Context Pollution / Distraction を引き起こす。</li>
</ul>
"""
    },
    {
        "id": "ch-domain5",
        "title": "6. Domain 5: ツール設計と MCP (15%)",
        "content": """
<p class="guide-p">Model Context Protocol (MCP) を活用した拡張性と、ツールのトークン効率化が問われます。</p>

<h3 class="guide-h3">MCP Progressive Disclosure（段階的情報開示）</h3>
<p class="guide-p">数多くのツール（数十〜数百種類）を連携させる際、全ツールの完全な JSON スキーマをプロンプトに常駐させると、それだけで数万トークンを消費します。</p>
<ul class="guide-list">
<li><strong>初期状態</strong>: ツール名と1行の概要（Index）のみをコンテキストに提示。</li>
<li><strong>動的取得</strong>: エージェントがそのツールを必要と判断した段階で、スキーマ取得メタツールを介して詳細定義をJITロード。</li>
</ul>

<h3 class="guide-h3">中間生出力のプルーニング（Pruning）</h3>
<p class="guide-p">APIツールが返した数千行の生JSONデータから必要な集計値や結論を導き出したら、後続ターンでは巨大な生データを履歴から削除するか、簡潔な要約に置き換えてコンテキストを保護します。</p>
"""
    },
    {
        "id": "ch-domain6",
        "title": "7. Domain 6: コンパクションと圧縮戦略 (10%)",
        "content": """
<p class="guide-p">ウィンドウ上限に近づいた際の、情報の圧縮・要約テクニックを学習します。</p>

<h3 class="guide-h3">Compaction Tuning: 「Recall First, Precision Second」</h3>
<p class="guide-p">コンテキスト要約における鉄則は、<strong>「まず重要な制約・ゴール・確定値を100%漏らさず拾い切る（Recall First）」</strong> ことです。その上で不要な装飾語やノイズを削ります（Precision Second）。</p>
<div class="table-container"><table class="guide-table">
<thead><tr><th>保持すべき要素（絶対に捨ててはならない）</th><th>安全に破棄できる要素（Purge対象）</th></tr></thead><tbody>
<tr><td>ユーザーが指定した前提条件・除外条件・フィルタルール</td><td>完了済みツールの生JSONダンプ（集計済みのもの）</td></tr>
<tr><td>確定したID（顧客ID、注文番号、トランザクションID）</td><td>リトライして解決済みのエラーログ・スタックトレース</td></tr>
<tr><td>現在のタスク完了状況と未完了の残課題</td><td>対話の挨拶、お礼、過度な相槌などのフィラー</td></tr>
</tbody></table></div>

<p class="guide-p"><strong>Trimming vs Compaction</strong>: Trimming（古いメッセージのFIFO削除）は、最初に入力された「大前提ルール」から順に消去されるため、長期タスクでは破綻します。</p>
"""
    },
    {
        "id": "ch-domain7",
        "title": "8. Domain 7: マルチエージェント & 長期タスク (10%)",
        "content": """
<p class="guide-p">複数のエージェントが協調して動作する際のコンテキスト伝播の制御です。</p>

<h3 class="guide-h3">親トレース漏洩の防止</h3>
<p class="guide-p">オーケストレーターがサブエージェントを呼ぶ際、親の全思考ログをそのまま渡すと、子のコンテキストが即座に飽和し Context Distraction を招きます。サブエージェントには<strong>目的達成に必要な入力パラメータと指示のみ</strong>を分離して渡します。</p>

<h3 class="guide-h3">Delta Lake によるポインタ受け渡し</h3>
<p class="guide-p">サブエージェントが大量のデータ（数十万行のログ解析結果など）を処理した場合、生テキストを親に返信するのではなく、<strong>Delta テーブルに書き込み、親には「軽量なサマリー ＋ Delta テーブルのURIポインタ」のみを返信</strong>します。</p>
"""
    }
]

cheatsheets = [
    {
        "id": "cs-failures",
        "title": "コンテキスト4大障害 徹底比較表",
        "category": "Domain 1: 基礎 & 障害分析",
        "headers": ["障害モード", "本質的トリガー", "典型的現象", "是正アクション"],
        "rows": [
            ["Context Poisoning", "信頼できない外部データ、誤ったナレッジの注入", "誤情報を事実と信じ込み、誤答を確定的に出力する", "Unity Catalog で Authoritative 認定資産に制限"],
            ["Context Distraction", "大量の未加工ログ、無関係なトークンの流入", "システムプロンプトの指示や出力フォーマットを失念する", "構造化チャンキング、生出力プルーニング、JITスキーマ"],
            ["Context Confusion", "類似した複数のツール名・同名カラムの存在", "誤ったツールを選択、誤った引数を渡す", "ツール・カラムの Description で役割・差異を明確化"],
            ["Context Clash", "指示同士、または指示と検索ドキュメントの矛盾", "推論のデッドロック、挙動の不安定化、指示無視", "プロンプトで明示的な優先ルール（社内方針 ＞ 外部資料）を設定"]
        ]
    },
    {
        "id": "cs-memory",
        "title": "エージェントメモリ アーキテクチャ比較表",
        "category": "Domain 4: メモリ設計",
        "headers": ["メモリレイヤー", "保存場所", "永続性", "主な用途", "検索方式"],
        "rows": [
            ["In-context Scratchpad", "プロンプト内", "単一推論ターンのみ", "中間計算、現ステップの推論トレース", "ダイレクト参照"],
            ["Session History", "メッセージ履歴配列", "セッション中", "指示代名詞（「先ほどの件」）の解決", "短期コンテキスト走査"],
            ["Lakebase / Delta-backed State", "Delta Lake / Unity Catalog", "永続（複数セッション横断）", "ユーザープロファイル、長期タスク状態、耐障害性復旧", "確定キー: 構造化SQL / 概念: ベクトル検索"]
        ]
    },
    {
        "id": "cs-retrieval",
        "title": "情報検索・チャンキング戦略 比較表",
        "category": "Domain 3: 知識検索 & ガバナンス",
        "headers": ["アプローチ", "特徴", "推奨シナリオ", "注意点・アンチパターン"],
        "rows": [
            ["Pre-inference Retrieval", "推論前に類似チャンクをプロンプトに事前注入", "静的ドキュメント検索、単一ステップのFAQ", "動的集計や条件分岐には不向き"],
            ["JIT Agentic Retrieval", "推論途中で動的にSQLやAPIツールを実行", "リアルタイムデータ照会、集計、マルチホップ推論", "過剰取得（Over-retrieval）によるトークン浪費に注意"],
            ["Markdown構造化チャンキング", "見出し単位で256〜512トークンに小分割", "コード仕様書、エラーコード照会、技術ドキュメント", "親メタデータ（文書タイトル・章）を付与すること"],
            ["Hybrid Search", "高次元ベクトル検索 ＋ BM25キーワード検索", "型番、特定のエラーコード、略語を含む検索", "疎密検索のウェイト比率調整が必要"]
        ]
    },
    {
        "id": "cs-mcp-compaction",
        "title": "MCP & コンパクション設計 比較表",
        "category": "Domain 5 & 6: ツール & 圧縮",
        "headers": ["パターン / 原則", "目的", "メカニズム", "効果"],
        "rows": [
            ["MCP Progressive Disclosure", "大量ツールの常駐トークン削減", "名前と概要のみを先行提示、必要時のみ動的スキーマ取得", "初期トークン消費を最大80%削減"],
            ["Raw Output Pruning", "中間生データによるウィンドウ圧迫防止", "集計完了後に生JSONをサマリーやポインタに置換", "長時間の対話でもコンテキストを健全に維持"],
            ["Recall First, Precision Second", "要約による重要情報の欠落防止", "制約・除外条件・確定IDを100%保持してから装飾語を削減", "下流タスクでの前提崩壊を完全に防止"],
            ["Agent Skills Packaging", "めったに使われない専門知識の外部化", "オンデマンドで読み込めるスクリプトやUC関数として定義", "システムプロンプトの肥大化と保守コストを抑制"]
        ]
    }
]

print("Base definitions ready.")
