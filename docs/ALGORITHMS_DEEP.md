# Algorithms Module - Deep Technical Specification

## 1. Module Purpose

The Algorithms module contains **100% SanTOK-original algorithms**.

```
┌─────────────────────────────────────────────────────────────┐
│                   WHAT WE DON'T USE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ✗ BM25 (Okapi)                                            │
│   ✗ TF-IDF (Term Frequency-Inverse Document Frequency)      │
│   ✗ PageRank                                                │
│   ✗ Word2Vec / GloVe / FastText                             │
│   ✗ BERT / Transformers                                     │
│   ✗ Neural NER                                              │
│   ✗ Dependency Parsing                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. SanTOKRanker - Complete Mathematical Specification

### 2.1 The Master Formula

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   SANTOK RANKING FORMULA                                    │
│                                                             │
│   score(q, d) = α·R(q,d) + β·C(d) + γ·H(d) + δ·F(d)        │
│                                                             │
│   Where:                                                    │
│     q = query tokens                                        │
│     d = document/candidate                                  │
│     R = Relevance score                                     │
│     C = Connectivity score                                  │
│     H = Hierarchy score                                     │
│     F = Freshness score                                     │
│                                                             │
│   Default weights:                                          │
│     α = 0.4                                                 │
│     β = 0.3                                                 │
│     γ = 0.2                                                 │
│     δ = 0.1                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Relevance Score R(q,d)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   R(q, d) = Σᵢ [match(qᵢ, d) × boost(i)] / |q|             │
│                                                             │
│   Where:                                                    │
│                                                             │
│   match(qᵢ, d) = {                                          │
│       1.0    if qᵢ ∈ tokens(d)     [exact match]           │
│       0.5    if partial_match      [substring]              │
│       0.0    otherwise                                      │
│   }                                                         │
│                                                             │
│   boost(i) = 1 / (1 + ln(i + 2))                           │
│                                                             │
│   Position boost values:                                    │
│   ┌────────┬────────┐                                      │
│   │ Position│ Boost  │                                      │
│   ├────────┼────────┤                                      │
│   │ 0      │ 0.591  │                                      │
│   │ 1      │ 0.476  │                                      │
│   │ 2      │ 0.419  │                                      │
│   │ 3      │ 0.379  │                                      │
│   │ 4      │ 0.349  │                                      │
│   └────────┴────────┘                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Connectivity Score C(d)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   C(d) = centrality(d) × avg_strength(d)                   │
│                                                             │
│   centrality(d) = degree(d) / (N - 1)                      │
│                                                             │
│   degree(d) = |outgoing_edges| + |incoming_edges|          │
│                                                             │
│   avg_strength(d) = Σₑ [rel_weight(e)] / |edges|           │
│                                                             │
│   Relation weights:                                         │
│   ┌──────────────┬────────┐                                │
│   │ Relation     │ Weight │                                │
│   ├──────────────┼────────┤                                │
│   │ IS_A         │ 0.9    │                                │
│   │ PART_OF      │ 0.85   │                                │
│   │ HAS_PART     │ 0.85   │                                │
│   │ CAUSES       │ 0.8    │                                │
│   │ DERIVED_FROM │ 0.75   │                                │
│   │ USES         │ 0.7    │                                │
│   │ DEPENDS_ON   │ 0.75   │                                │
│   │ SIMILAR_TO   │ 0.6    │                                │
│   │ RELATED_TO   │ 0.5    │                                │
│   │ MENTIONS     │ 0.3    │                                │
│   └──────────────┴────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Hierarchy Score H(d)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   H(d) = W_depth × (1 - P_sibling) × I_parent              │
│                                                             │
│   W_depth = 1 / (1 + depth)                                 │
│                                                             │
│   P_sibling = siblings / (siblings + 10)                    │
│                                                             │
│   I_parent = 0.9^depth                                      │
│                                                             │
│   Example values:                                           │
│   ┌───────┬─────────┬──────────┬──────────┬────────┐       │
│   │ Depth │ W_depth │ Siblings │ P_sibling│ I_parent│       │
│   ├───────┼─────────┼──────────┼──────────┼────────┤       │
│   │ 0     │ 1.000   │ 0        │ 0.000    │ 1.000  │       │
│   │ 1     │ 0.500   │ 2        │ 0.167    │ 0.900  │       │
│   │ 2     │ 0.333   │ 5        │ 0.333    │ 0.810  │       │
│   │ 3     │ 0.250   │ 3        │ 0.231    │ 0.729  │       │
│   └───────┴─────────┴──────────┴──────────┴────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 Freshness Score F(d)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   F(d) = length_factor × access_boost                       │
│                                                             │
│   length_factor = 1 / (1 + ln(|content| + 1))              │
│                                                             │
│   access_boost = 1 + ln(access_count + 1) × 0.1            │
│                                                             │
│   Length factor examples:                                   │
│   ┌────────────┬───────────────┐                           │
│   │ Length     │ Factor        │                           │
│   ├────────────┼───────────────┤                           │
│   │ 10 chars   │ 0.706         │                           │
│   │ 50 chars   │ 0.560         │                           │
│   │ 100 chars  │ 0.521         │                           │
│   │ 500 chars  │ 0.446         │                           │
│   │ 1000 chars │ 0.421         │                           │
│   └────────────┴───────────────┘                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.6 9-Centric Transformation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DIGITAL ROOT TRANSFORMATION                               │
│                                                             │
│   dr(score) = 1 + ((⌊score × 1000⌋ - 1) mod 9)             │
│                                                             │
│   Example mappings:                                         │
│   ┌────────────┬──────────────┬─────────┐                  │
│   │ Score      │ Integer      │ DR      │                  │
│   ├────────────┼──────────────┼─────────┤                  │
│   │ 0.001      │ 1            │ 1       │                  │
│   │ 0.009      │ 9            │ 9       │                  │
│   │ 0.010      │ 10           │ 1       │                  │
│   │ 0.500      │ 500          │ 5       │                  │
│   │ 0.999      │ 999          │ 9       │                  │
│   └────────────┴──────────────┴─────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. SanTOK9Scorer - Complete Mathematical Specification

### 3.1 Digital Root Formula

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   STANDARD DIGITAL ROOT                                     │
│                                                             │
│   dr(n) = {                                                 │
│       9           if n = 0                                  │
│       9           if n mod 9 = 0 and n ≠ 0                 │
│       n mod 9     otherwise                                 │
│   }                                                         │
│                                                             │
│   SANTOK DIGITAL ROOT (1-indexed)                           │
│                                                             │
│   dr_santok(n) = 1 + ((n - 1) mod 9)                       │
│                                                             │
│   This ensures output is always 1-9 (not 0-8)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Score9 Structure

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Score9 = (raw, digital_root, cycle)                       │
│                                                             │
│   raw: float           Original value                       │
│   digital_root: int    1-9 value                           │
│   cycle: int           Which 9-cycle (0, 1, 2, ...)        │
│                                                             │
│   Conversion:                                               │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ int_value = |raw × 1000|                             │  │
│   │ digital_root = 1 + ((int_value - 1) mod 9)          │  │
│   │ cycle = int_value // 9                               │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   Example:                                                  │
│   raw=0.72 → int=720 → dr=9, cycle=80                      │
│   raw=0.95 → int=950 → dr=5, cycle=105                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Combination Methods

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   MEAN COMBINATION                                          │
│   combined = Σ(values) / |values|                           │
│   result = to_9(combined)                                   │
│                                                             │
│   PRODUCT COMBINATION                                       │
│   combined = Π(values)                                      │
│   result = to_9(combined)                                   │
│                                                             │
│   ROOT SUM COMBINATION                                      │
│   root_sum = Σ(dr(v) for v in values)                      │
│   result = to_9(root_sum / 1000)                           │
│                                                             │
│   HARMONIC COMBINATION                                      │
│   harmonic = |values| / Σ(1/dr(v) for v in values)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Confidence Propagation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PROPAGATION FORMULA                                       │
│                                                             │
│   conf[i] = conf[i-1] × decay × (0.9 + 0.1 × dr/9)        │
│                                                             │
│   Where:                                                    │
│     decay = 0.9 (default)                                   │
│     dr = digital_root(conf[i-1])                           │
│                                                             │
│   Example propagation (initial=0.9, decay=0.9):            │
│   ┌──────┬────────┬────┬──────────┐                        │
│   │ Step │ Conf   │ DR │ Meaning  │                        │
│   ├──────┼────────┼────┼──────────┤                        │
│   │ 0    │ 0.9000 │ 9  │ complete │                        │
│   │ 1    │ 0.8100 │ 9  │ complete │                        │
│   │ 2    │ 0.7290 │ 9  │ complete │                        │
│   │ 3    │ 0.6488 │ 9  │ complete │                        │
│   │ 4    │ 0.5710 │ 3  │ synthesis│                        │
│   │ 5    │ 0.5139 │ 9  │ complete │                        │
│   └──────┴────────┴────┴──────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.5 Root Meanings

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DIGITAL ROOT INTERPRETATIONS                              │
│                                                             │
│   ┌────┬─────────────┬────────────────────────────────────┐│
│   │ DR │ Name        │ Interpretation                     ││
│   ├────┼─────────────┼────────────────────────────────────┤│
│   │ 1  │ Origin      │ Beginning, source, seed            ││
│   │ 2  │ Duality     │ Opposition, comparison, binary     ││
│   │ 3  │ Synthesis   │ Combination, creation, growth      ││
│   │ 4  │ Structure   │ Foundation, stability, order       ││
│   │ 5  │ Change      │ Transformation, adaptation         ││
│   │ 6  │ Balance     │ Harmony, equilibrium, fairness     ││
│   │ 7  │ Analysis    │ Investigation, depth, wisdom       ││
│   │ 8  │ Power       │ Strength, confidence, authority    ││
│   │ 9  │ Completion  │ Fullness, cycle end, wholeness     ││
│   └────┴─────────────┴────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. SanTOKSimilarity - Complete Mathematical Specification

### 4.1 Master Formula

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   SANTOK SIMILARITY FORMULA                                 │
│                                                             │
│   sim(a, b) = α·Lex + β·Ngram + γ·Pos + δ·Graph            │
│                                                             │
│   Where:                                                    │
│     α = 0.35 (Lexical weight)                              │
│     β = 0.25 (N-gram weight)                               │
│     γ = 0.20 (Position weight)                             │
│     δ = 0.20 (Graph weight)                                │
│                                                             │
│   Note: Unlike neural embeddings, each component is         │
│   interpretable and explainable.                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Lexical Similarity (Lex)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Lex(a, b) = (Jaccard + Dice) / 2                         │
│                                                             │
│   Jaccard Coefficient:                                      │
│   J(A, B) = |A ∩ B| / |A ∪ B|                              │
│                                                             │
│   Dice Coefficient:                                         │
│   D(A, B) = 2|A ∩ B| / (|A| + |B|)                         │
│                                                             │
│   Example:                                                  │
│   A = {"machine", "learning"}                              │
│   B = {"deep", "learning"}                                 │
│                                                             │
│   A ∩ B = {"learning"}         |A ∩ B| = 1                 │
│   A ∪ B = {"machine", "learning", "deep"}  |A ∪ B| = 3    │
│                                                             │
│   Jaccard = 1/3 = 0.333                                    │
│   Dice = 2×1/(2+2) = 0.5                                   │
│   Lex = (0.333 + 0.5) / 2 = 0.417                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 N-gram Similarity (Ngram)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Ngram(a, b) = 2 × |ngrams_a ∩ ngrams_b|                  │
│                 ─────────────────────────                   │
│                 |ngrams_a| + |ngrams_b|                     │
│                                                             │
│   Using character 3-grams (default):                        │
│                                                             │
│   text = "machine" → ["mac", "ach", "chi", "hin", "ine"]   │
│                                                             │
│   Example:                                                  │
│   a = "machine"  → 5 trigrams                              │
│   b = "matching" → 6 trigrams                              │
│                                                             │
│   Common: ["mac", "ach", "chi", "hin"] = 4                 │
│                                                             │
│   Ngram = 2×4 / (5+6) = 8/11 = 0.727                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Position Similarity (Pos)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Pos(a, b) = [Σᵢ match(i) × weight(i)] / Σᵢ weight(i)     │
│               × length_penalty                              │
│                                                             │
│   weight(i) = 1 / (1 + ln(i + 2))                          │
│                                                             │
│   match(i) = {                                              │
│       1.0    if tokens_a[i] == tokens_b[i]                 │
│       0.5    if tokens_a[i] similar to tokens_b[i]         │
│       0.0    otherwise                                      │
│   }                                                         │
│                                                             │
│   length_penalty = min(|a|, |b|) / max(|a|, |b|)           │
│                                                             │
│   "similar" = substring match OR prefix ≥ 3 chars          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.5 Graph Similarity (Graph)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Graph(a, b) = avg(relatedness(nᵢ, nⱼ))                   │
│                 for nᵢ ∈ nodes(a), nⱼ ∈ nodes(b)           │
│                                                             │
│   relatedness(n₁, n₂) = {                                   │
│       1.0        if n₁ == n₂ (same node)                   │
│       1.0        if direct edge exists                     │
│       0.5-0.8    if common neighbors (more = higher)       │
│       0.4        if 2-hop path exists                      │
│       0.0        if no connection                          │
│   }                                                         │
│                                                             │
│   Note: If no graph available, Graph(a,b) = 0.5 (neutral)  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. SanTOKGraphWalker - Complete Algorithm Specification

### 5.1 Walk Algorithm

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   SANTOK GRAPH WALK ALGORITHM                               │
│                                                             │
│   Input:                                                    │
│     source: starting node ID                                │
│     target: optional target node ID                         │
│     energy: initial energy budget (default: 10.0)          │
│     mode: SHORTEST | WEIGHTED | RANDOM                     │
│                                                             │
│   Algorithm (WEIGHTED mode):                                │
│   ────────────────────────────────────────────────────────  │
│   1. Initialize                                             │
│      priority_queue = [(0, source, [source], [])]          │
│      visited = {}                                           │
│                                                             │
│   2. While queue not empty:                                 │
│      a. Pop (neg_score, current, path, edges)              │
│      b. If current == target: return path                  │
│      c. If current in visited: continue                    │
│      d. Mark visited                                        │
│                                                             │
│   3. For each outgoing edge:                                │
│      a. If target not visited:                             │
│         edge_score = rel_score × edge_weight               │
│         new_score = -neg_score + edge_score                │
│         Push (-new_score, target, path+[target], edges+e)  │
│                                                             │
│   4. Return best path found                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Relation Costs and Scores

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   RELATION COSTS (energy consumption)                       │
│                                                             │
│   ┌──────────────┬──────┬────────────────────────────────┐ │
│   │ Relation     │ Cost │ Reasoning                      │ │
│   ├──────────────┼──────┼────────────────────────────────┤ │
│   │ IS_A         │ 0.5  │ Strong, direct relationship    │ │
│   │ PART_OF      │ 0.5  │ Strong structural relation     │ │
│   │ HAS_PART     │ 0.5  │ Strong structural relation     │ │
│   │ USES         │ 0.6  │ Functional relationship        │ │
│   │ DEPENDS_ON   │ 0.6  │ Functional relationship        │ │
│   │ CAUSES       │ 0.7  │ Causal, some uncertainty       │ │
│   │ CAUSED_BY    │ 0.7  │ Causal, some uncertainty       │ │
│   │ SIMILAR_TO   │ 0.8  │ Weak, fuzzy relationship       │ │
│   │ RELATED_TO   │ 0.9  │ Weakest, generic               │ │
│   │ OPPOSITE_OF  │ 1.0  │ Contrasting, costly            │ │
│   │ MENTIONS     │ 1.0  │ Surface-level only             │ │
│   └──────────────┴──────┴────────────────────────────────┘ │
│                                                             │
│   RELATION SCORES (path quality)                            │
│                                                             │
│   ┌──────────────┬───────┐                                 │
│   │ Relation     │ Score │                                 │
│   ├──────────────┼───────┤                                 │
│   │ IS_A         │ 1.0   │                                 │
│   │ PART_OF      │ 0.9   │                                 │
│   │ HAS_PART     │ 0.9   │                                 │
│   │ CAUSES       │ 0.85  │                                 │
│   │ USES         │ 0.8   │                                 │
│   │ DEPENDS_ON   │ 0.8   │                                 │
│   │ DERIVED_FROM │ 0.75  │                                 │
│   │ SIMILAR_TO   │ 0.6   │                                 │
│   │ RELATED_TO   │ 0.5   │                                 │
│   │ OPPOSITE_OF  │ 0.4   │                                 │
│   │ MENTIONS     │ 0.3   │                                 │
│   └──────────────┴───────┘                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Walk Result Structure

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WalkResult:                                               │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ path: List[WalkStep]                                 │  │
│   │   Each step: (node_id, text, relation, energy, score)│  │
│   │                                                      │  │
│   │ total_score: float                                   │  │
│   │   Sum of edge scores along path                     │  │
│   │                                                      │  │
│   │ total_energy_used: float                             │  │
│   │   initial_energy - final_energy                     │  │
│   │                                                      │  │
│   │ hops: int                                            │  │
│   │   Number of edges traversed                         │  │
│   │                                                      │  │
│   │ reached_target: bool                                 │  │
│   │   Whether target was found                          │  │
│   │                                                      │  │
│   │ terminated_reason: str                               │  │
│   │   "target" | "energy" | "dead_end" | "max_hops"     │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. SanTOKPatternMatcher - Pattern Database

### 6.1 Pattern Statistics

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PATTERN DATABASE STATISTICS                               │
│                                                             │
│   Total patterns: 34                                        │
│                                                             │
│   By relation type:                                         │
│   ┌──────────────┬───────────┐                             │
│   │ Relation     │ Patterns  │                             │
│   ├──────────────┼───────────┤                             │
│   │ IS_A         │ 5         │                             │
│   │ PART_OF      │ 4         │                             │
│   │ HAS_PART     │ 4         │                             │
│   │ CAUSES       │ 4         │                             │
│   │ USES         │ 3         │                             │
│   │ DEPENDS_ON   │ 3         │                             │
│   │ DERIVED_FROM │ 3         │                             │
│   │ PRECEDES     │ 3         │                             │
│   │ SIMILAR_TO   │ 3         │                             │
│   │ OPPOSITE_OF  │ 2         │                             │
│   └──────────────┴───────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Confidence Calculation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   CONFIDENCE FORMULA                                        │
│                                                             │
│   conf = base × freq × prox × len                          │
│                                                             │
│   base = 0.7                                                │
│                                                             │
│   freq = 1.0 + 0.1 × min(mentions, 5)                      │
│        [more mentions = higher confidence]                  │
│                                                             │
│   prox = 1.0 / (1.0 + distance / 100)                      │
│        [closer entities = higher confidence]                │
│                                                             │
│   len = min(1.0, avg_length / 3)                           │
│        [longer entities = higher confidence]                │
│                                                             │
│   Final confidence capped at 1.0                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. SanTOKQueryParser - Query Classification

### 7.1 Query Type Detection

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   QUERY TYPE DETECTION RULES                                │
│                                                             │
│   DEFINITION (confidence: 0.9)                              │
│   └── Starts with: "what is", "what are", "define"         │
│   └── Contains: "definition", "meaning"                     │
│                                                             │
│   RELATION (confidence: 0.9)                                │
│   └── Pattern: "how is X related to Y"                     │
│   └── Pattern: "relationship between X and Y"              │
│                                                             │
│   LIST (confidence: 0.85)                                   │
│   └── Pattern: "what are the parts of"                     │
│   └── Starts with: "list", "name all"                      │
│                                                             │
│   BOOLEAN (confidence: 0.85)                                │
│   └── Starts with: "is", "are", "does", "can"              │
│   └── Expects yes/no answer                                │
│                                                             │
│   COMPARISON (confidence: 0.9)                              │
│   └── Contains: "difference between"                       │
│   └── Pattern: "compare X and Y"                           │
│                                                             │
│   PROCESS (confidence: 0.85)                                │
│   └── Pattern: "how does X work"                           │
│   └── Starts with: "explain how"                           │
│                                                             │
│   CAUSE (confidence: 0.85)                                  │
│   └── Starts with: "why"                                   │
│   └── Pattern: "what causes"                               │
│                                                             │
│   UNKNOWN (confidence: 0.5)                                 │
│   └── No pattern matched                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Implementation Notes

### 8.1 Why These Algorithms?

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DESIGN DECISIONS                                          │
│                                                             │
│   Q: Why not BM25?                                          │
│   A: BM25 ignores graph structure and hierarchy.           │
│      SanTOKRanker integrates all knowledge types.          │
│                                                             │
│   Q: Why not Word2Vec/BERT for similarity?                 │
│   A: Neural embeddings are black boxes.                    │
│      SanTOKSimilarity is 100% explainable.                 │
│                                                             │
│   Q: Why 9-centric scoring?                                │
│   A: Creates bounded, interpretable scores.                │
│      Aligns with SanTOK's tokenization philosophy.         │
│                                                             │
│   Q: Why pattern-based extraction?                          │
│   A: No training data needed.                              │
│      Rules are transparent and editable.                   │
│      Works in any domain without fine-tuning.              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Extensibility

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   HOW TO EXTEND                                             │
│                                                             │
│   Add new ranking component:                                │
│   1. Create _compute_new_component() method                │
│   2. Add weight to DEFAULT_WEIGHTS                         │
│   3. Include in _score_candidate()                         │
│                                                             │
│   Add new pattern:                                          │
│   matcher.add_pattern(                                     │
│       r"(\w+)\s+leads\s+to\s+(\w+)",                       │
│       RelationType.CAUSES,                                 │
│       subject_group=1,                                     │
│       object_group=2                                       │
│   )                                                         │
│                                                             │
│   Add new query type:                                       │
│   1. Add to QueryType enum                                 │
│   2. Add pattern to PATTERNS list                          │
│   3. Recompile patterns                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

This completes the deep technical specification for the Algorithms module.

