# build_rich_guide.py
# Comprehensive textbook-grade study guide for Databricks Certified Context Engineer Associate

RICH_GUIDE_CHAPTERS = [
    {
        "id": "ch-overview",
        "title": "1. 試験概要・公式シラバス・学習戦略",
        "content": """
<p class="guide-p"><strong>Databricks Certified Context Engineer Associate</strong> は、推論時において AI エージェントや LLM に提供する情報空間（コンテキスト）の設計・アセンブリ・メモリ管理・ツール統合・ガバナンスを評価・認定する業界初の専門資格です。</p>

<div class="table-container"><table class="guide-table">
<thead><tr><th>項目</th><th>詳細仕様</th><th>受験上の重要注意点</th></tr></thead><tbody>
<tr><td><strong>正式名称</strong></td><td>Databricks Certified Context Engineer Associate</td><td>2026年最新認定試験</td></tr>
<tr><td><strong>問題数</strong></td><td>45問（採点対象）</td><td>多肢選択式（シナリオベースの実務問題中心）</td></tr>
<tr><td><strong>制限時間</strong></td><td>90分（1問あたり約2分）</td><td>長文シナリオが多いため、設問と選択肢を先に確認する</td></tr>
<tr><td><strong>合格ライン</strong></td><td>約70%（約32問以上の正解）</td><td>全ドメインから均等に出題される</td></tr>
<tr><td><strong>出題言語</strong></td><td><strong>英語のみ（English）</strong></td><td>コードは Python 主体、データ操作は SQL も含む</td></tr>
<tr><td><strong>受験方式</strong></td><td>オンラインプロクター（Webassessor / Kryterion）またはテストセンター</td><td>カメラ・マイク必須、身分証明書確認</td></tr>
<tr><td><strong>持ち込み資料</strong></td><td><strong>一切不可（APIドキュメント等も参照不可）</strong></td><td>メソッド名、引数名、設定パラメータの暗記が必要</td></tr>
<tr><td><strong>有効期間</strong></td><td>2年間</td><td>再認定はその時点の最新試験を再受験</td></tr>
<tr><td><strong>前提知識推奨</strong></td><td>Databricks Data Engineer Associate レベル知識</td><td>Unity Catalog, Delta Lake, SQL, Python SDK</td></tr>
</tbody></table></div>

<h3 class="guide-h3">全 7 出題ドメイン構成比 & 配点詳細</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>ドメイン</th><th>配点比率</th><th>出題数目安</th><th>出題の核心論点</th></tr></thead><tbody>
<tr><td><strong>Domain 1: Foundations of Context Engineering</strong></td><td>20%</td><td>約9問</td><td>コンテキスト4大障害（Poisoning, Distraction, Confusion, Clash）、推論モード、アテンションバジェット、Databricks スタック選定</td></tr>
<tr><td><strong>Domain 2: System Prompt & Instruction Design</strong></td><td>15%</td><td>約7問</td><td>AI/BI Genie スペースのキュレーション、セマンティックレイヤー（Metric Views）、Trusted Assets（View/UDF）、Few-shot選定（Marginal Contribution）、構造化出力（JSON Schema）</td></tr>
<tr><td><strong>Domain 3: Knowledge Retrieval & Governance</strong></td><td>15%</td><td>約7問</td><td>Unity Catalog ガバナンス（Row/Column Masking）、AI Search、チャンキング戦略、Pre-inference vs JIT 検索、MLflow Eval</td></tr>
<tr><td><strong>Domain 4: Memory Architecture with Lakebase</strong></td><td>15%</td><td>約7問</td><td>Lakebase / Delta-backed State、In-context Scratchpad、意図解決（Intent Resolution）、構造化クエリ vs ベクトル検索、Over-retrieval</td></tr>
<tr><td><strong>Domain 5: Tool & Action Design with MCP</strong></td><td>15%</td><td>約7問</td><td>Model Context Protocol (MCP)、Progressive Disclosure、中間生出力プルーニング、Agent Skills、冪等性・副作用管理</td></tr>
<tr><td><strong>Domain 6: Compression & Compaction Strategies</strong></td><td>10%</td><td>約4問</td><td>Recall First 原則、安全な破棄対象、FIFO Trimming の欠陥 vs Compaction、構造化要約スキーマ、Telephone Game防止</td></tr>
<tr><td><strong>Domain 7: Multi-Agent Systems & Long-Horizon Tasks</strong></td><td>10%</td><td>約4問</td><td>親トレース漏洩防止、オーケストレーター飽和防止（Delta Lake ポインタ渡し）、境界設計、ステートフルチェックポインティング</td></tr>
</tbody></table></div>

<h3 class="guide-h3">本番試験を突破するための「3大解法テクニック」</h3>
<ul class="guide-list">
<li><strong>1. プロンプトでの精神論を疑う（ガバナンスとコードの優先）</strong>:
選択肢に「プロンプトに『絶対に〜するな』と強く念押しする」「プロンプトを長文化する」とあるものは、ほぼ確実に誤答（Distractor）です。Databricks では **Unity Catalog の権限モデル、タグ、Metric Views、Trusted Assets、JSON Schema による物理的・決定論的制御** が常に正解になります。</li>
<li><strong>2. 確定キー vs 意味的探索の峻別</strong>:
CustomerID や OrderID などの一意な識別子を検索する際、「ベクトル類似度検索（Vector Search）」とある選択肢はアンチパターンです。一意キーには必ず「構造化クエリ（Structured SQL / Key-Value Lookup）」を選択してください。</li>
<li><strong>3. トークン節約の鉄則（Progressive Disclosure & Pruning）</strong>:
全ツールの完全スキーマを最初からプロンプトに常駐させたり、数千行の生APIレスポンスを履歴に残し続ける設計は誤りです。「初期は名前と概要のみ提示しJIT取得」「抽出完了後に生データをサマリーに置換」が正解パターンです。</li>
</ul>
"""
    },
    {
        "id": "ch-domain1",
        "title": "2. Domain 1: コンテキストエンジニアリングの基礎と障害分析 (20%)",
        "content": """
<p class="guide-p">コンテキストエンジニアリング（Context Engineering）とは、LLMが推論を行う瞬間に受け取る入力ウィンドウ内の情報（指示、知識、ツール定義、履歴、メタデータ）を最適に選定・配置・統制する技術体系です。</p>

<h3 class="guide-h3">コンテキスト障害の 4 大分類（最重要出題分野）</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>障害モード</th><th>メカニズム</th><th>具体的シナリオ例</th><th>Databricks での推奨恒久対策</th></tr></thead><tbody>
<tr>
  <td><strong>Context Poisoning<br>（コンテキスト汚染）</strong></td>
  <td>信頼できない外部検索、未承認ドラフト、悪意あるプロンプト注入がコンテキストに混入し、モデルがそれを「疑いようのない事実」として受け入れてしまう現象。</td>
  <td>ベクトル検索が開発用スキーマのテストデータ（売上0円）や、古い非公式ドラフト規約（90日以内全額返金）を取得し、顧客に誤案内してしまう。</td>
  <td>Unity Catalog で <code>governance_status = 'Authoritative'</code> とタグ付けされた正規データのみを検索対象に制限。入力サニタイズ。</td>
</tr>
<tr>
  <td><strong>Context Distraction<br>（注意散漫）</strong></td>
  <td>過剰な未加工ログ、無関係な長文ドキュメント、過度なFew-shot例がウィンドウを埋め尽くし、モデルのアテンションが分散して重要な制約を見落とす現象。</td>
  <td>ツールが返した 8,000 行の生 JSON ログにより、システムプロンプトの「出力は JSON 形式とし、IPアドレスを含めるな」という必須制約を忘れて平文で出力する。</td>
  <td>マークダウン構造化チャンキング（256〜512トークン）、中間ツールの生出力プルーニング（Pruning）、JIT スキーマ取得。</td>
</tr>
<tr>
  <td><strong>Context Confusion<br>（混同）</strong></td>
  <td>名前や説明文が類似した複数のツール、または同名のテーブル・カラムが存在し、モデルが境界や責務を区別できずに誤選択する現象。</td>
  <td><code>fetch_active_subscribers</code> と <code>fetch_subscriber_history</code> の説明文が曖昧なため、現在の契約確認に履歴ツールを呼び出して引数エラーを起こす。</td>
  <td>ツールの Description で「いつ使うべきか（When to use）」と「いつ使ってはならないか（When NOT to use）」を用途境界として明確に差別化（Disambiguation）。</td>
</tr>
<tr>
  <td><strong>Context Clash<br>（論理衝突）</strong></td>
  <td>システムプロンプトの指示と、検索ドキュメントの記述、あるいは複数ドキュメント間でルールが真っ向から対立し、挙動が破綻・デッドロックする現象。</td>
  <td>プロンプトの「社内原価は絶対に非公開」と、検索された営業資料の「顧客には原価内訳を明示せよ」が衝突し、回答拒否と漏洩を繰り返す。</td>
  <td>システムプロンプトで明示的な優先順位ルール（Precedence Hierarchy）を定義（例: 『社内基本ポリシーは検索結果に常に優先する』）。</td>
</tr>
</tbody></table></div>

<div class="mermaid-card"><div class="mermaid-header"><span>📊 障害モード診断フローチャート</span></div>
<pre class="mermaid">flowchart TD
    Start[エージェントの推論失敗トレース] --> Q1{誤情報・非公式データを真実と信じ込んでいるか?}
    Q1 -- Yes --> Poisoning["🚨 Context Poisoning (汚染)<br/>未検証データ・ドラフトの混入<br/>対策: Unity Catalog Authoritative 制限"]
    Q1 -- No --> Q2{大量のトークンにより重要指示を見落としているか?}
    Q2 -- Yes --> Distraction["🌪️ Context Distraction (注意散漫)<br/>生ログ・ノイズによる埋没<br/>対策: プルーニング & 構造化チャンキング"]
    Q2 -- No --> Q3{似たツールやカラムの選択を間違えているか?}
    Q3 -- Yes --> Confusion["🔀 Context Confusion (混同)<br/>定義の曖昧さ・類似性<br/>対策: Description での境界明確化"]
    Q3 -- No --> Clash["⚔️ Context Clash (衝突)<br/>矛盾する指示・ルールの競合<br/>対策: プロンプトでの優先順位明示"]
</pre></div>

<h3 class="guide-h3">Reasoning Modes（推論モード）の比較と選定基準</h3>
<p class="guide-p">タスクの特性に応じて思考トークン（Thinking Budget）を適切に割り当て、コストとレイテンシを最適化します。</p>
<div class="table-container"><table class="guide-table">
<thead><tr><th>推論モード</th><th>割り当てトークン特性</th><th>適したユースケース</th><th>避けるべきユースケース</th></tr></thead><tbody>
<tr>
  <td><strong>Extended Thinking<br>（拡張推論）</strong></td>
  <td>数千〜数万の思考トークンを消費し、自己検証・多段階探索を実行</td>
  <td>複雑なマルチホップ SQL 生成、多段階コードレビュー、数理的整合性検証、複雑なルール調停</td>
  <td>単純な問い合わせ、固定フォーマット変換、低遅延が必須なチャットボット</td>
</tr>
<tr>
  <td><strong>Standard Mode<br>（標準モード）</strong></td>
  <td>通常の推論ステップで直接回答を生成</td>
  <td>一般的なドキュメント検索 QA、一般的な要約、定型的なツール実行</td>
  <td>極めて複雑な多変数最適化や数千行の依存関係解析</td>
</tr>
<tr>
  <td><strong>Reduced Thinking<br>（最小推論）</strong></td>
  <td>思考トークンをゼロまたは極小に抑制し、直接マッピング</td>
  <td>テキスト分類、センチメント判定、単純なキーワード抽出、定型エンティティ抽出</td>
  <td>推論ロジックが必要なタスク（ハルシネーションが発生する）</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">アテンションバジェット（Attention Budget）と「Lost in the Middle」</h3>
<p class="guide-p">Transformer のアテンション機構は、プロンプトの **「冒頭（Beginning）」** と **「末尾（End）」** に強く集中し、**「中央部（Middle）」** に配置された情報を見落としやすいという特性（U字型カーブ）を持っています。</p>
<ul class="guide-list">
  <li><strong>プロアクティブ配置原則</strong>: システムの絶対的制約（出力スキーマ、安全基準）は冒頭に配置し、最新のユーザー指示および高関連度の検索結果は末尾に配置する。</li>
  <li><strong>中央部のプルーニング</strong>: 検索スコアの中位〜低位のチャンクや、過去ターンの不要な中間ログは中央部から積極的に除外する。</li>
</ul>
"""
    },
    {
        "id": "ch-domain2",
        "title": "3. Domain 2: プロンプト設計 & AI/BI Genie・セマンティックレイヤー (15%)",
        "content": """
<p class="guide-p">プロンプトを長文化させてLLMに無理な推論を強いるのではなく、Databricks のデータ資産（Unity Catalog、Metric Views、AI/BI Genie）を活用して<strong>セマンティック（意味論）を物理的・決定論的に確立・統制する設計</strong>が本ドメインの最大の核心です。</p>

<h3 class="guide-h3">なぜ Databricks に「セマンティック整備（Semantic Preparation）」が不可欠なのか？</h3>
<p class="guide-p">AI/BI Genie や自律エージェントに未加工の生テーブル（Bronze / Silver 層）をそのまま提示すると、次のようなコンテキスト崩壊が必然的に発生します：</p>
<ul class="guide-list">
  <li><strong>集計ロジックの不一致（Metric Drift）</strong>: ユーザーが「今月の売上は？」と質問した際、LLM が <code>SUM(sales)</code> を計算するのか、値引きや返品を差し引いた <code>SUM(amount - discount - refund)</code> を計算するのかが都度ブレてしまい、ダッシュボードと回答の数値が乖離する。</li>
  <li><strong>結合事故とファンアウト（Context Confusion）</strong>: テーブル間のリレーションシップが定義されていないため、LLM が誤った外部キーで多対多結合を行い、レコード数が数百万件に爆発して誤った数値を生成する。</li>
  <li><strong>アテンション散漫（Context Distraction）</strong>: 1つのテーブルに存在する100個以上のカラム定義をすべてプロンプトに流し込み、重要なビジネス制約を見落とす。</li>
  <li><strong>プロンプト精神論の破綻</strong>: プロンプトに「MRRとは〜で、キャンセル注文は除外し〜」と50行の計算ルールを自然言語で書き連ねても、LLM は確率的に条件を失念する。</li>
</ul>

<div class="mermaid-card"><div class="mermaid-header"><span>📊 Unity Catalog 一元管理型セマンティックレイヤー・アーキテクチャ</span></div>
<pre class="mermaid">flowchart TD
    subgraph DataFoundation["1. データ基盤 & リレーションシップ層"]
        Delta["Gold Layer Delta Tables<br/>(クレンジング済み厳選テーブル)"]
        PKFK["Informational PK / FK 制約<br/>(結合グラフを決定論的に定義)"]
        Comments["Table & Column Comments<br/>(コード値・単位・ビジネス注釈)"]
    end

    subgraph SemanticLayer["2. セマンティックレイヤー (Unity Catalog)"]
        MV["📐 Unity Catalog Metric Views<br/>(YAMLベースの宣言型メジャー/ディメンション/同義語)"]
        TA["🛡️ Trusted Assets<br/>(認定集計View, SQL UDF, パラメータ化クエリ)"]
    end

    subgraph GenieSpace["3. AI/BI Genie Space (キュレーション空間)"]
        Curated["Curated Dataset<br/>(厳選5〜10テーブル)"]
        Instructions["Genie Instructions<br/>(会計年度, デフォルト除外方針)"]
        SampleQ["Sample Questions<br/>(5〜15問の厳選ゴールデンQA)"]
        Ontology["Genie Ontology<br/>(自動推論されたビジネス文脈)"]
    end

    subgraph Consumers["4. 統合コンシューマー (Single Source of Truth)"]
        GenieAgent["🤖 AI/BI Genie (自然言語対話)"]
        Dashboards["📊 AI/BI Dashboards (公式レポート)"]
        DBSQL["💻 Databricks SQL / ノートブック"]
        CustomAgent["🦾 外部カスタムAIエージェント (MCP連携)"]
    end

    DataFoundation --> SemanticLayer
    SemanticLayer --> GenieSpace
    GenieSpace --> Consumers
    SemanticLayer -.-> Dashboards
    SemanticLayer -.-> DBSQL
    SemanticLayer -.-> CustomAgent
</pre></div>

<h3 class="guide-h3">セマンティック整備の 5 段階ピラミッド</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>階層</th><th>構成要素</th><th>Databricks 実装手法</th><th>エージェント / Genie に対する効果</th></tr></thead><tbody>
<tr>
  <td><strong>第1層: データ基盤</strong></td>
  <td>Gold層集約 & リレーションシップ</td>
  <td>INFORMATIONAL PK / FK 制約（<code>NOT ENFORCED</code>）</td>
  <td>テーブル間の結合パス（Join Path）を決定論的に理解させ、誤結合やカーテシアン積を根絶する。</td>
</tr>
<tr>
  <td><strong>第2層: メタデータ注釈</strong></td>
  <td>カタログコメント & タグ</td>
  <td><code>COMMENT ON TABLE / COLUMN</code>、Certification（認定）</td>
  <td>ステータスコード値（'A'=有効, 'S'=停止）や略語の意味をコンテキストとして直接供給する。</td>
</tr>
<tr>
  <td><strong>第3層: メトリクスビュー</strong></td>
  <td>宣言型セマンティックレイヤー</td>
  <td><strong>Unity Catalog Metric Views（YAML仕様 1.1）</strong></td>
  <td>メジャー（指標計算）、ディメンション（分析軸）、同義語（Synonyms）を全社一元化し Metric Drift を防止。</td>
</tr>
<tr>
  <td><strong>第4層: 信頼できる資産</strong></td>
  <td>Trusted Assets</td>
  <td>集計ビュー（View）、SQL UDF、パラメータ化クエリ</td>
  <td>複雑な多段階ビジネス計算（MRR、LTV等）を LLM のアドホック SQL 生成に任せず、確定実行させる。</td>
</tr>
<tr>
  <td><strong>第5層: スペース調整</strong></td>
  <td>Genie キュレーション & ループ</td>
  <td>Instructions、Sample Questions、Fix it フィードバック</td>
  <td>組織固有ルール（会計期間、除外方針）の伝達と、ユーザーの利用フィードバックによる継続的チューニング。</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">Unity Catalog Metric Views（メトリクスビュー）完全詳解</h3>
<p class="guide-p">Metric Views は、Unity Catalog 上にファーストクラスのセキュリティ保護対象オブジェクトとして登録される<strong>宣言型のセマンティックレイヤー</strong>です。従来の BI ツール（Looker の LookML や Tableau データモデル）に閉じ込められていたビジネス定義を、データプラットフォームの中心（Unity Catalog）へ解放します。</p>

<div class="code-block"><div class="code-header"><span>SQL / YAML: Unity Catalog Metric View の定義構文（Version 1.1）</span><button class="copy-btn" onclick="copyCode(this)">コピー</button></div><pre><code class="language-sql">-- Unity Catalog に公式メトリクスビューを宣言型 YAML で作成
CREATE OR REPLACE VIEW sales_prod.analytics.mv_revenue_and_orders
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
comment: "全社公式の受注および売上収益セマンティックビュー (AI/BI Genie & ダッシュボード共通)"
source: sales_prod.gold.fact_orders

# 1. ディメンション (分析軸・グループ化・スライス項目)
fields:
  - name: order_date
    expression: order_timestamp::DATE
    display_name: "注文日"
  - name: order_year
    expression: EXTRACT(YEAR FROM order_timestamp)
    display_name: "注文年"
  - name: customer_tier
    expression: CASE WHEN total_lifetime_spend > 500000 THEN 'Enterprise' ELSE 'Standard' END
    display_name: "顧客ティア"
    comment: "累積利用額に基づく顧客重要度分類"

# 2. メジャー (集計指標・ビジネス計算ロジック)
measures:
  - name: net_revenue
    expr: SUM(order_amount - discount_amount)
    display_name: "純売上高 (Net Revenue)"
    comment: "値引き適用後の確定売上高。キャンセル・返品注文は除外済"
    # Agent Metadata: Genieが自然言語のゆらぎを解釈するための同義語 (最大10個)
    synonyms: ["売上", "収益", "sales", "revenue", "純売上", "入金額"]
    format: "$#,##0.00"

  - name: order_count
    expr: COUNT(DISTINCT order_id)
    display_name: "総受注件数"
    comment: "一意な注文番号のカウント"
    synonyms: ["注文件数", "オーダー数", "number of orders", "件数"]
    format: "#,##0"

# 3. リレーションシップ (スタースキーマ / スノーフレーク結合)
joins:
  - name: dim_customer
    source: sales_prod.gold.dim_customers
    on: source.customer_id = dim_customer.customer_id

# 4. グローバルフィルタ (除外条件の一貫適用)
filter: order_status != 'CANCELLED'
$$;
</code></pre></div>

<h4 class="guide-h4">Metric View YAML の重要キーと役割</h4>
<ul class="guide-list">
  <li><strong><code>version: 1.1</code></strong>: Agent Metadata（<code>synonyms</code> や <code>display_name</code>）を完全サポートする仕様バージョン。</li>
  <li><strong><code>source</code></strong>: メトリクスビューが参照する基盤の Gold 層テーブルまたはビュー。</li>
  <li><strong><code>fields</code> (Dimensions)</strong>: <code>EXTRACT</code>、<code>CASE WHEN</code>、型キャストなどの SQL 式を用いて導出される分析軸。</li>
  <li><strong><code>measures</code> (Metrics)</strong>: <code>SUM</code>、<code>COUNT DISTINCT</code>、<code>AVG</code> などの集計関数を用いた公式計算ロジック。</li>
  <li><strong><code>synonyms</code> (同義語)</strong>: <strong>Genie やエージェントの自然言語認識精度を高める最重要プロパティ</strong>。ビジネスユーザーが「売上高」「収益」「Sales」「入金額」のどの言葉で質問しても、自動的に <code>net_revenue</code> メジャーにマッピングされます。</li>
  <li><strong><code>joins</code></strong>: テーブル間の結合キーと参照先を宣言。Genie が適切なディメンション結合を構築するための基盤となります。</li>
  <li><strong><code>filter</code></strong>: 「キャンセル済み注文は除外する」などの全社基本ルールをグローバルに強制。LLM が WHERE 句を書き忘れる事故を根絶します。</li>
</ul>

<h3 class="guide-h3">リレーションシップと Informational PK / FK 制約の役割</h3>
<p class="guide-p">レイクハウス（Delta Lake）では、リレーショナル DB のような厳格な主キー制約の強制（Enforcement）は書き込みパフォーマンス維持のため行いません。しかし、Unity Catalog では <strong>Informational PK/FK（<code>NOT ENFORCED</code>）</strong> を定義することが強く推奨されます。</p>

<div class="code-block"><div class="code-header"><span>SQL: Informational PK / FK 制約の定義</span><button class="copy-btn" onclick="copyCode(this)">コピー</button></div><pre><code class="language-sql">-- 主キーの定義 (NOT ENFORCED)
ALTER TABLE sales_prod.gold.dim_customers 
  ADD CONSTRAINT pk_dim_customers PRIMARY KEY (customer_id) NOT ENFORCED;

-- 外部キーの定義 (NOT ENFORCED)
ALTER TABLE sales_prod.gold.fact_orders 
  ADD CONSTRAINT fk_orders_to_customers 
  FOREIGN KEY (customer_id) REFERENCES sales_prod.gold.dim_customers(customer_id) NOT ENFORCED;
</code></pre></div>
<ul class="guide-list">
  <li><strong>Genie に対する効果</strong>: Genie は Unity Catalog の制約メタデータを読み取ってテーブル間の結合グラフ（Entity-Relationship Graph）を自動構築します。これにより、外部キーの同名異義や結合キーの当て推量を完全に防止します。</li>
  <li><strong>クエリオプティマイザへの効果</strong>: Databricks Photon エンジンは Informational 制約を活用して不要な JOIN を除去（Join Elimination）し、クエリを高速化します。</li>
</ul>

<h3 class="guide-h3">AI/BI Genie Space のキュレーション原則（運用とチューニング）</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>キュレーション項目</th><th>推奨ベストプラクティス</th><th>アンチパターン（試験の代表的誤答）</th></tr></thead><tbody>
<tr>
  <td><strong>テーブル数の絞り込み<br>（Curated Dataset）</strong></td>
  <td>1つの Genie Space に登録するテーブル数は <strong>5〜10 個の Gold / Metric Views</strong> に厳選する。</td>
  <td>スキーマ内の Bronze / Silver を含む全 80 テーブルをすべて Genie Space に追加する（Context Distraction による大混乱）。</td>
</tr>
<tr>
  <td><strong>Trusted Assets<br>（信頼できる資産）</strong></td>
  <td>Metric Views、集計ビュー、SQL UDF、パラメータ化クエリを登録し、Unity Catalog で「Certified（認定）」を付与する。</td>
  <td>プロンプト（Instructions）の中に 50 行の複雑な SQL 文を手動で書き連ねる（トークン浪費＆文法エラー誘発）。</td>
</tr>
<tr>
  <td><strong>Instructions<br>（スペース指示）</strong></td>
  <td>組織特有の前提条件（例: 「会計年度は4月開始」「今期は2026年度を指す」「通貨は日本円換算」）を簡潔に記述する。</td>
  <td>テーブルのカラム名一覧やデータ型をそのまま Instructions にコピー＆ペーストする（メタデータと二重管理になり衝突の原因）。</td>
</tr>
<tr>
  <td><strong>Sample Questions<br>（サンプル質問）</strong></td>
  <td>代表的な KPI、複雑なフィルタ条件、エッジケースを含む質問を <strong>5〜15問厳選</strong> して登録する。</td>
  <td>「先月の売上」「先々月の売上」のような類似した定型質問を 100 個以上登録する（内部ベクトルの衝突を招く）。</td>
</tr>
<tr>
  <td><strong>反復改善ループ<br>（Curator Loop）</strong></td>
  <td>ユーザーの会話ログ、👍/👎評価、<strong>「Fix it（修正）」機能</strong> を定期レビューし、不足している同義語や指示を順次補正する。</td>
  <td>Genie Space を一度公開したら放置し、精度低下時にモデル全体の再ファインチューニングを検討する。</td>
</tr>
</tbody></table></div>

<div class="code-block"><div class="code-header"><span>SQL: Unity Catalog Trusted Asset (SQL UDF) の定義例</span><button class="copy-btn" onclick="copyCode(this)">コピー</button></div><pre><code class="language-sql">-- 複雑な法人顧客の解約リスクスコア計算を SQL UDF (Trusted Asset) としてカプセル化
CREATE OR REPLACE FUNCTION sales_prod.analytics.calc_churn_risk(
    last_login_days INT,
    ticket_count INT,
    contract_mrr DOUBLE
)
RETURNS DOUBLE
COMMENT 'Authoritative churn risk calculation logic approved by CRO'
RETURN (last_login_days * 0.4) + (ticket_count * 5.0) - (LOG10(GREATEST(contract_mrr, 1.0)) * 2.0);

-- これを Genie Space の Trusted Asset に登録することで、Genie は独自計算せずこの UDF を正確に呼ぶ
</code></pre></div>

<h3 class="guide-h3">Few-shot サンプルの選定原則「Marginal Contribution」</h3>
<ul class="guide-list">
  <li><strong>Marginal Contribution（限界貢献度）の最大化</strong>:
  ゼロショットで既にモデルが正答できる標準的なクエリ例を並べても、トークンを浪費するだけで精度向上価値（限界貢献度）はゼロです。</li>
  <li><strong>優先的に含めるべきエッジケース（2〜3例）</strong>:
    <ol>
      <li>未知・未指定のパラメータが渡された場合の「聞き返し / フォールバック」パターン</li>
      <li>厳格な JSON 出力スキーマ（ネスト構造）の強制パターン</li>
      <li>ユーザー入力に曖昧な同音異義語が含まれる場合の曖昧性解消パターン</li>
    </ol>
  </li>
</ul>

<h3 class="guide-h3">構造化出力の強制（Structured Outputs）</h3>
<p class="guide-p">プロンプト内で「JSON 形式で出力してください」と依頼するだけでは、<code>```json</code> などのマークダウン装飾や前置き会話文が混入し、下流の API パースがクラッシュします。Databricks Model Serving では、<strong>Pydantic スキーマや JSON Schema を API レベルで直接指定（Structured Outputs）</strong> することで、決定論的な構文整合性を保証します。</p>
"""
    },
    {
        "id": "ch-domain3",
        "title": "4. Domain 3: 知識検索 & ガバナンス（Databricks AI Search & UC） (15%)",
        "content": """
<p class="guide-p">本ドメインでは、Databricks AI Search / Vector Search の最適化と、Unity Catalog を用いた探索空間のセキュリティ統制が問われます。</p>

<h3 class="guide-h3">Pre-inference Retrieval vs Just-in-Time (JIT) Agentic Retrieval</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>方式</th><th>実行タイミング</th><th>適したシナリオ</th><th>メリットと制約</th></tr></thead><tbody>
<tr>
  <td><strong>Pre-inference Retrieval<br>（事前取得 / RAG 先読み）</strong></td>
  <td>ユーザー入力直後、推論が始まる前</td>
  <td>静的な社内規程 FAQ、製品マニュアル検索など、1ターンのドキュメント検索で完結するタスク</td>
  <td><strong>メリット</strong>: 実装が単純、低レイテンシ。<br><strong>制約</strong>: 動的な集計や多段階推論、条件分岐には対応不可。</td>
</tr>
<tr>
  <td><strong>Just-in-Time (JIT) Retrieval<br>（動的エージェント検索）</strong></td>
  <td>LLM の推論の途中（ツール呼出ステップ）</td>
  <td>ライブな Delta テーブルの集計、多段階の深掘り調査、異常値検知時の詳細ログ参照</td>
  <td><strong>メリット</strong>: 必要な差分データのみを動的に取得しトークンを節約。<br><strong>制約</strong>: 推論ターン数が増加しレイテンシが増大。</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">チャンキング戦略の選定基準</h3>
<ul class="guide-list">
  <li><strong>Markdown構造化チャンキング（256〜512トークン）</strong>:
  API リファレンス、コードブロック、エラーコード照会など、ピンポイントな定義が求められるドキュメントに最適。見出しタグ（H1, H2, H3）をメタデータとして各チャンクに付与することで、小さなチャンクでも文脈を見失いません。</li>
  <li><strong>階層的チャンキング（Hierarchical Chunking）</strong>:
  法務契約書や長大な技術仕様書など、詳細な条文と全体概要の両方を参照する必要がある文書に適用。親チャンク（大局観）と子チャンク（詳細）をリンク管理します。</li>
  <li><strong>固定長大チャンク（1,000〜4,000トークン）の危険性</strong>:
  無関係な段落が大量に混入し、<strong>Context Distraction</strong> を引き起こして Faithfulness（忠実度）を著しく低下させます。</li>
</ul>

<h3 class="guide-h3">Databricks AI Search のハイブリッド検索（Hybrid Search）</h3>
<p class="guide-p">高次元ベクトル埋め込み（Dense Vectors）は意味的な概念理解に優れていますが、**「部品型番（SN-8820-X）」「特定エラーコード（ERR_4092）」「製品型式」** などの希少な固有文字列の検索には弱点があります。</p>
<ul class="guide-list">
  <li><strong>Hybrid Search の仕組み</strong>: Dense Vector（セマンティック検索）＋ Sparse Vector / BM25（キーワード完全一致）を統合。</li>
  <li><strong>効果</strong>: 概念のゆらぎをカバーしつつ、固有識別子の確実なヒットを両立。</li>
</ul>

<h3 class="guide-h3">Unity Catalog ガバナンスによるコンテキスト保護</h3>
<div class="mermaid-card"><div class="mermaid-header"><span>📊 Unity Catalog ガバナンスとコンテキスト供給</span></div>
<pre class="mermaid">flowchart LR
    Source[Delta Lake Tables] --> UC{Unity Catalog<br/>ガバナンス層}
    UC -- "Row Filter / Column Mask" --> SafeData[マスキング済データ]
    UC -- "Authoritative Tag" --> VS[Databricks Vector Search]
    SafeData --> Agent[Agent Context Window]
    VS --> Agent
    Sandbox[Sandbox / Dev Tables] -- "権限拒否 (REVOKE)" --> Blocked[遮断: コンテキスト混入不可]
</pre></div>
<ul class="guide-list">
  <li><strong>Authoritative（正規資産）と Derived（派生資産）の分離</strong>:
  本番エージェントには、開発スキーマ（<code>dev_*</code>）や未検証の個人テーブルを検索させず、Unity Catalog のタグで認定された正規ソースのみを Vector Search の同期元に指定します。</li>
  <li><strong>行フィルタ（Row Filters）と列マスク（Column Masks）の自動強制</strong>:
  エージェントが実行するクエリや検索であっても、Unity Catalog の権限モデルは常に適用されます。権限のない行や機密カラム（給与、PIIなど）は実行時に自動マスクされ、コンテキストに到達しません。</li>
</ul>

<h3 class="guide-h3">MLflow 3 LLM Evaluation メトリクスによる障害診断</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>評価メトリクス</th><th>測定内容</th><th>典型的な障害パターンと是正アクション</th></tr></thead><tbody>
<tr>
  <td><strong>Context Recall<br>（文脈想起率）</strong></td>
  <td>正解に必要な情報が検索結果に含まれていた割合</td>
  <td><strong>低スコア時</strong>: 検索の失敗。インデックス設定の見直し、ハイブリッド検索の導入、埋め込みモデルの再選定が必要。</td>
</tr>
<tr>
  <td><strong>Faithfulness<br>（忠実度 / 根拠性）</strong></td>
  <td>生成された回答が、コンテキスト内の事実に厳密に基づいている割合</td>
  <td><strong>低スコア時（ハルシネーション）</strong>: Recall は高いのに Faithfulness が低い場合、チャンクが長すぎて Context Distraction が起きているか、プロンプトの Grounding 指示が弱い。</td>
</tr>
<tr>
  <td><strong>Answer Relevance<br>（回答関連度）</strong></td>
  <td>生成された回答がユーザーの意図・質問に的確に答えている度合い</td>
  <td><strong>低スコア時</strong>: 質問と無関係な長文が出力されている。プロンプトでの回答フォーマット指定や出力制約の再キャリブレーションが必要。</td>
</tr>
</tbody></table></div>
"""
    },
    {
        "id": "ch-domain4",
        "title": "5. Domain 4: メモリ設計と Lakebase (15%)",
        "content": """
<p class="guide-p">会話内の短期記憶と、Databricks Lakebase / Delta Lake を用いた永続的な長期記憶の役割分担を理解します。</p>

<h3 class="guide-h3">3層メモリ階層アーキテクチャ</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>メモリレイヤー</th><th>保持場所</th><th>ライフサイクル</th><th>典型的な格納データ</th><th>参照・検索方式</th></tr></thead><tbody>
<tr>
  <td><strong>In-context Scratchpad<br>（インコンテキスト作業領域）</strong></td>
  <td>プロンプト内部</td><td>単一推論ターンのみ</td><td>計算の中間変数、現在のサブゴール、推論ステップの思考ログ</td><td>プロンプト内直接参照</td>
</tr>
<tr>
  <td><strong>Session History<br>（短期対話履歴）</strong></td>
  <td>メッセージ履歴配列</td><td>ユーザー対話の1セッション</td><td>直前の対話ターン、指示代名詞（「先ほどの件」）の文脈</td><td>直近メッセージ走査</td>
</tr>
<tr>
  <td><strong>Delta-backed State / Lakebase<br>（長期永続メモリ）</strong></td>
  <td>Delta Lake / Unity Catalog</td><td>永続（複数日・複数セッション横断）</td><td>ユーザー嗜好プロファイル、長期タスクの進捗ステート、耐障害性チェックポイント</td><td>確定キー: 構造化 SQL<br>概念・類似: ベクトル検索</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">意図解決（Intent Resolution）パイプライン</h3>
<p class="guide-p">ユーザーが「先ほど提案された 2 つ目のプランについて進めてください」と発話した際、直ちに外部の長期メモリ（Lakebase）を検索してはなりません。外部検索をかけると、2 年前の古い契約プランがヒットして誤爆します。</p>
<ul class="guide-list">
  <li><strong>ステップ 1</strong>: 直前の短期会話履歴（Session History）を参照し、指示代名詞（「2つ目のプラン」）が「Plan B (Standard Enterprise)」であることを特定（Intent Resolution）。</li>
  <li><strong>ステップ 2</strong>: 具体的なエンティティ名「Plan B」にクエリを正規化した上で、必要に応じて外部メモリや DB を照会する。</li>
</ul>

<h3 class="guide-h3">確定キー取得におけるアンチパターン</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>検索対象</th><th>推奨されるメカニズム</th><th>アンチパターン（試験の誤答例）</th></tr></thead><tbody>
<tr>
  <td><strong>確定キー・ID<br>（<code>user_id = 'U12345'</code>）</strong></td>
  <td><strong>構造化クエリ（Structured SQL / Key-Value Lookup）</strong><br>主キー検索で 100% 確実に一致レコードをロード。</td>
  <td>ベクトル類似度検索（Cosine Similarity）で検索する（類似した別ユーザー ID が誤ヒットする危険大）。</td>
</tr>
<tr>
  <td><strong>意味的嗜好・概念<br>（「アウトドア系の趣味」）</strong></td>
  <td><strong>ベクトル検索（AI Search Vector Similarity）</strong><br>過去の会話ログやレビューからセマンティックに抽出。</td>
  <td>完全一致 SQL フィルタをかける（表記揺れでヒットしない）。</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">過剰取得（Over-retrieval）とコンテキスト汚染（Context Pollution）</h3>
<p class="guide-p">「過去の情報を漏らさず渡したい」として、過去 3 年分の全チャット履歴を生のままプロンプトに流し込むと、次のような破綻が生じます：</p>
<ul class="guide-list">
  <li><strong>Context Pollution</strong>: 過去の一時的な関心（例: 2年前のギフト検索）が、現在の検索文脈を歪めてしまう。</li>
  <li><strong>対策</strong>: セッション終了時に <strong>Fact Extraction（事実抽出）</strong> パイプラインを実行し、恒久的なユーザープロファイルのみを構造化 JSON として Lakebase に保存。次回セッションでは要約プロファイルのみを読み込む。また、時間経過に伴う <strong>Temporal Decay（時間的減衰）</strong> と TTL を設定する。</li>
</ul>
"""
    },
    {
        "id": "ch-domain5",
        "title": "6. Domain 5: ツール設計と Model Context Protocol (MCP) (15%)",
        "content": """
<p class="guide-p">Model Context Protocol (MCP) を活用したオープンなツール連携と、ツールのトークン効率化設計を学習します。</p>

<h3 class="guide-h3">MCP Progressive Disclosure（段階的情報開示）</h3>
<p class="guide-p">企業内のツール数が 50〜100 種類に増えた際、すべてのツールの完全な JSON Schema を最初からプロンプトに常駐させると、それだけで 30,000〜40,000 トークンを常時浪費します。</p>
<div class="mermaid-card"><div class="mermaid-header"><span>📊 MCP Progressive Disclosure の動作ステップ</span></div>
<pre class="mermaid">sequenceDiagram
    participant LLM as LLM Agent
    participant MCP as MCP Registry
    participant Tool as Actual Backend Tool
    Note over LLM: 初期プロンプトにはツール名と1行概要のインデックスのみ提示 (軽量)
    LLM->>MCP: 1. query_customer_orders の詳細スキーマを要求 (JIT Fetch)
    MCP-->>LLM: 2. 完全な JSON 引数スキーマを返却
    LLM->>Tool: 3. 正しい引数で実ツールを実行
    Tool-->>LLM: 4. 実行結果 (生データ) を返却
    Note over LLM: 抽出完了後、生データは要約にプルーニング
</pre></div>

<h3 class="guide-h3">中間生出力のプルーニング（Pruning）</h3>
<p class="guide-p">ツールが返した 5,000 行の未加工 JSON データから、エージェントが「当期の不良品率は 2.3% であった」という結論を導き出したら、後続ターンでは巨大な生 JSON を履歴に残し続ける必要はありません。</p>
<ul class="guide-list">
  <li><strong>プルーニング処理</strong>: メッセージ履歴内の生データを、抽出された結論やコンパクトな構造化サマリー（<code>{"defect_rate": 0.023}</code>）に置き換える。</li>
  <li><strong>効果</strong>: ウィンドウの空き容量を確保し、Context Distraction を根本防止。</li>
</ul>

<h3 class="guide-h3">Agent Skills へのカプセル化（Skills Packaging）</h3>
<p class="guide-p">年に数回しか発生しないレガシー DB の緊急ロールバック手順や、特殊な障害解析スクリプトを常時システムプロンプトに記載するのはトークンの浪費です。これらは独立した **「Agent Skill（ファイルまたは Unity Catalog SQL 関数）」** として定義し、該当する緊急時のみオンデマンドでロードさせます。</p>

<h3 class="guide-h3">ツールの耐障害性と副作用安全性</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>安全性メカニズム</th><th>目的と動作</th><th>違反時のリスク</th></tr></thead><tbody>
<tr>
  <td><strong>Idempotency Keys<br>（冪等性キー）</strong></td>
  <td>注文確定や送金などの書き込みツール実行時に一意のリクエスト ID を付与。ネットワーク再試行時に同一処理を二重実行しない。</td>
  <td>二重請求、重複発注などの重大障害。</td>
</tr>
<tr>
  <td><strong>HITL Confirmation<br>（人間承認ゲート）</strong></td>
  <td>不可逆なデータ変更（DELETE、大量更新、資産凍結）の前に、人間のレビュー承認ステップを必須とする。</td>
  <td>自律エージェントによる偶発的なデータ破壊。</td>
</tr>
<tr>
  <td><strong>Self-Describing Errors<br>（自己記述的エラー）</strong></td>
  <td>引数エラー時に <code>Error 500</code> ではなく、<code>{"expected": "YYYY-MM-DD", "got": "2024/05/01"}</code> のように修正指針を構造化して返す。</td>
  <td>エージェントが原因を理解できず諦めてハルシネーションを起こす。</td>
</tr>
</tbody></table></div>
"""
    },
    {
        "id": "ch-domain6",
        "title": "7. Domain 6: コンパクションと圧縮戦略 (10%)",
        "content": """
<p class="guide-p">ウィンドウ上限に近づいた際の情報損失を防ぐ、高度なコンテキスト圧縮・要約技法を学習します。</p>

<h3 class="guide-h3">Compaction Tuning: 「Recall First, Precision Second」の原則</h3>
<p class="guide-p">コンテキスト要約（Compaction）において最も致命的なのは、文章を美しく短くまとめようとするあまり、**「ユーザーが最初に指定した前提条件・除外条件・重要 ID」** を切り落としてしまうことです。</p>
<ul class="guide-list">
  <li><strong>Recall First</strong>: ユーザーが提示したすべての制約条件、除外ルール、確定した ID を 100% 漏らさず保持するプロンプトをまず設計する。</li>
  <li><strong>Precision Second</strong>: 情報の脱落がゼロになったことを確認した上で、不要な装飾語や会話フィラーを削る。</li>
</ul>

<h3 class="guide-h3">安全に破棄できる要素 vs 保持必須要素</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>安全に破棄できる要素（Safe Purge Targets）</th><th>絶対に破棄してはならない保持必須要素（Must Preserve）</th></tr></thead><tbody>
<tr>
  <td>抽出・集計が完了した過去ツールの生 JSON 出力</td><td>ユーザーの最終的な達成目標（Primary Goal）</td></tr>
<tr>
  <td>リトライによって解決済みの古いエラースタックトレース</td><td>前提条件、除外ルール、フィルタ条件（Constraints）</td></tr>
<tr>
  <td>挨拶、お礼、過度な相槌などの会話フィラー</td><td>確定したエンティティ識別子（CustomerID, OrderID, UUID）</td></tr>
<tr>
  <td>途中計算の一時的なメモ（確定値が算出された後のもの）</td><td>現在のタスク完了ステータスおよび未完了の残課題</td></tr>
</tbody></table></div>

<h3 class="guide-h3">Trimming vs Compaction の比較</h3>
<div class="table-container"><table class="guide-table">
<thead><tr><th>手法</th><th>メカニズム</th><th>適したシナリオ</th><th>致命的欠陥</th></tr></thead><tbody>
<tr>
  <td><strong>Trimming<br>（FIFO スライディング窓）</strong></td>
  <td>トークン上限に近づいたら、最も古いメッセージから機械的に切り捨てる。</td>
  <td>直前の 1 往復だけで完結する単純なチャット。</td>
  <td><strong>最初に入力された「全体方針・大前提ルール」が真っ先に消滅する</strong>ため、長期タスクでは破綻する。</td>
</tr>
<tr>
  <td><strong>Compaction<br>（意味的要約）</strong></td>
  <td>LLM を呼び出して過去の文脈を構造化要約に圧縮する。</td>
  <td>複数日・複数ターンに及ぶ長期タスク、前提制約を維持し続ける必要がある分析業務。</td>
  <td>要約処理自体のトークン消費とレイテンシが発生する。</td>
</tr>
</tbody></table></div>

<h3 class="guide-h3">再帰的要約による伝言ゲーム現象（Telephone Game Effect）の防止</h3>
<p class="guide-p">要約文をさらに要約することを繰り返すと、細部のニュアンスが徐々に欠落し、最終的に要件が大きく歪んでしまいます。</p>
<ul class="guide-list">
  <li><strong>Canonical State によるアンカー固定</strong>:
  初回のユーザー指示や Lakebase の永続状態を「不変のアンカー（Canonical State）」として固定し、要約対象は直近ターンの未要約メッセージのみに限定します。</li>
  <li><strong>プロアクティブ発火閾値</strong>:
  コンテキストウィンドウの <strong>70%〜80%</strong> に達した段階で発火させ、要約処理自体の生成枠と次ターンの推論枠（ヘッドルーム）を確保します。</li>
</ul>
"""
    },
    {
        "id": "ch-domain7",
        "title": "8. Domain 7: マルチエージェント & 長期タスク (10%)",
        "content": """
<p class="guide-p">複数のエージェントが協調して動作する際のコンテキスト分離と、長期タスクの耐障害性を学びます。</p>

<h3 class="guide-h3">親トレース漏洩の防止（Parent Trace Leakage Prevention）</h3>
<p class="guide-p">オーケストレーターが特定のサブタスク（例: SQL 文法チェック）をサブエージェントに依頼する際、親の過去 20 ターンの全思考ログや過去の全ツール出力を子に丸ごと渡してはなりません。</p>
<ul class="guide-list">
  <li><strong>スコープ分離原則</strong>: サブエージェントの目的達成に必要な「タスク指示」と「対象データ」のみを切り出して渡す。</li>
  <li><strong>効果</strong>: 子のコンテキストが初期から飽和するのを防ぎ、アテンションを専門タスクに集中させる。</li>
</ul>

<h3 class="guide-h3">Pass-by-Reference（参照渡し）によるオーケストレーター飽和防止</h3>
<p class="guide-p">サブエージェントが 100 万行のログを解析して 30 MB の詳細結果を生成した際、その生テキストをメッセージ本文で親に返信すると、親のコンテキストウィンドウは瞬時にパンクします。</p>
<div class="mermaid-card"><div class="mermaid-header"><span>📊 大規模データの Pass-by-Reference アーキテクチャ</span></div>
<pre class="mermaid">sequenceDiagram
    participant Sub as Worker Subagent
    participant Lake as Unity Catalog (Delta Lake)
    participant Orch as Parent Orchestrator
    Sub->>Lake: 1. 30MBの分析詳細結果を Delta テーブルに保存
    Sub-->>Orch: 2. 軽量サマリー ＋ Delta テーブル URI ポインタのみを返信
    Note over Orch: オーケストレーターのコンテキストは数十トークンのみ消費で健全維持
    Orch->>Lake: 3. 必要時のみ特定行を SQL でピンポイント照会
</pre></div>

<h3 class="guide-h3">エージェント境界の設計（Boundary Placement）</h3>
<ul class="guide-list">
  <li><strong>細かすぎる境界（マイクロエージェント構成）の弊害</strong>:
  エージェント間のハンドオフ（引継ぎ処理、コンテキスト要約、通信往復）に伴うオーバーヘッドとレイテンシが爆発し、伝言ゲームのように文脈が劣化する。</li>
  <li><strong>粗すぎる境界（モノリシックエージェント）の弊害</strong>:
  単一エージェントにツールと責務が集中し、コンテキスト飽和と Context Confusion が発生する。</li>
  <li><strong>適正設計</strong>: 明確なビジネス責務と独立したデータドメインに基づいて境界を引く。</li>
</ul>

<h3 class="guide-h3">循環委譲ループ（Circular Delegation）の防止</h3>
<p class="guide-p">エージェント A がエージェント B に委譲し、エージェント B がエージェント A に差し戻すような無限ループを防ぐため、ハンドオフメタデータに <strong>Hop Counter（最大委譲ホップ数）</strong> と <strong>Call Stack（委譲履歴）</strong> を保持し、上限超過時に自動で人間にエスカレーションします。</p>
"""
    }
]

print(f"Rich guide chapters defined: {len(RICH_GUIDE_CHAPTERS)}")
