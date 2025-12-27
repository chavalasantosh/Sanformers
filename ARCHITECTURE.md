# SanTOK Cognitive - Complete Architecture

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Core Philosophy](#2-core-philosophy)
3. [Module Architecture](#3-module-architecture)
4. [Graph Module](#4-graph-module)
5. [Trees Module](#5-trees-module)
6. [Memory Module](#6-memory-module)
7. [Reasoning Module](#7-reasoning-module)
8. [Algorithms Module](#8-algorithms-module)
9. [Integration Module](#9-integration-module)
10. [Data Flow](#10-data-flow)
11. [Mathematical Foundations](#11-mathematical-foundations)

---

## 1. System Overview

### 1.1 What is SanTOK Cognitive?

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SANTOK COGNITIVE                                │
│                                                                     │
│   A cognitive knowledge system that transforms SanTOK from          │
│   "vector-only memory" to "structured + symbolic knowledge"         │
│                                                                     │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│   │   GRAPH     │    │   TREES     │    │   MEMORY    │            │
│   │  (Relations)│    │ (Hierarchy) │    │  (Unified)  │            │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘            │
│          │                  │                  │                    │
│          └──────────────────┼──────────────────┘                    │
│                             │                                       │
│                    ┌────────┴────────┐                              │
│                    │    REASONING    │                              │
│                    │   (Inference)   │                              │
│                    └────────┬────────┘                              │
│                             │                                       │
│                    ┌────────┴────────┐                              │
│                    │   ALGORITHMS    │                              │
│                    │ (100% Original) │                              │
│                    └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **100% Unique** | No borrowed algorithms, no external AI |
| **No Neural Networks** | Pure symbolic + rule-based |
| **Explainable** | Every decision can be traced |
| **Modular** | Each component works independently |
| **Safe** | Never modifies `santok_complete` |

### 1.3 Technology Stack

```
┌─────────────────────────────────────────┐
│             SANTOK COGNITIVE            │
├─────────────────────────────────────────┤
│  Language:     Python 3.8+              │
│  Dependencies: None (stdlib only)       │
│  Data Format:  JSON / Pickle            │
│  Memory:       In-memory + Serializable │
└─────────────────────────────────────────┘
```

---

## 2. Core Philosophy

### 2.1 The Four Pillars

```
    ┌─────────────────────────────────────────────────────────┐
    │                    KNOWLEDGE TYPES                       │
    ├─────────────┬─────────────┬─────────────┬───────────────┤
    │   VECTORS   │   GRAPHS    │   TREES     │    RULES      │
    ├─────────────┼─────────────┼─────────────┼───────────────┤
    │  "What is   │  "What is   │  "How is it │  "What        │
    │   similar?" │  connected?"│  organized?"│   follows?"   │
    ├─────────────┼─────────────┼─────────────┼───────────────┤
    │  Semantic   │ Relational  │ Hierarchical│  Logical      │
    │  Search     │ Reasoning   │ Navigation  │  Inference    │
    └─────────────┴─────────────┴─────────────┴───────────────┘
```

### 2.2 The 9-Centric Philosophy

SanTOK uses 9-centric numerology throughout:

```
Digital Root Formula:
    dr(n) = 1 + ((n - 1) mod 9)

Meaning:
    1 = Origin      6 = Balance
    2 = Duality     7 = Analysis
    3 = Synthesis   8 = Power
    4 = Structure   9 = Completion
    5 = Change
```

### 2.3 No External AI

```
┌────────────────────────────────────────────────────────────┐
│                   WHAT WE DON'T USE                        │
├────────────────────────────────────────────────────────────┤
│  ✗ GPT / ChatGPT / LLMs                                   │
│  ✗ Transformers / Attention                               │
│  ✗ BERT / Word2Vec / Neural Embeddings                    │
│  ✗ PyTorch / TensorFlow                                   │
│  ✗ spaCy / NLTK (for core logic)                         │
│  ✗ External APIs                                          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   WHAT WE USE INSTEAD                      │
├────────────────────────────────────────────────────────────┤
│  ✓ Symbolic inference (rule chaining)                     │
│  ✓ Template-based verbalization                           │
│  ✓ Pattern matching (regex-based)                         │
│  ✓ Graph traversal algorithms                             │
│  ✓ Mathematical formulas (custom)                         │
│  ✓ 9-centric scoring                                      │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Module Architecture

### 3.1 Directory Structure

```
santok_cognitive/
│
├── __init__.py                 # Main exports (50+ classes)
│
├── graph/                      # KNOWLEDGE GRAPH
│   ├── __init__.py
│   ├── graph_node.py          # GraphNode dataclass
│   ├── graph_edge.py          # GraphEdge + RelationType
│   ├── graph_store.py         # GraphStore (main storage)
│   └── relation_extractor.py  # Extract relations from text
│
├── trees/                      # KNOWLEDGE TREES
│   ├── __init__.py
│   ├── tree_node.py           # TreeNode dataclass
│   ├── tree.py                # Tree structure
│   └── tree_store.py          # TreeStore (manages trees)
│
├── memory/                     # UNIFIED MEMORY
│   ├── __init__.py
│   ├── memory_object.py       # MemoryObject dataclass
│   └── unified_memory.py      # UnifiedMemory (central hub)
│
├── reasoning/                  # REASONING ENGINE
│   ├── __init__.py
│   ├── path_finder.py         # Find paths in graph
│   ├── query_engine.py        # Execute queries
│   ├── explainer.py           # Generate explanations
│   ├── rule_base.py           # 20+ inference rules
│   ├── inference_engine.py    # Rule chaining
│   ├── contradiction_detector.py
│   ├── santok_reasoner.py     # Pure SanTOK reasoner
│   ├── santok_verbalizer.py   # Template verbalization
│   └── hybrid_reasoner.py     # Optional LLM bridge
│
├── algorithms/                 # CUSTOM ALGORITHMS
│   ├── __init__.py
│   ├── santok_ranker.py       # Hybrid ranking
│   ├── pattern_matcher.py     # Relation extraction
│   ├── nine_scorer.py         # 9-centric scoring
│   ├── graph_walker.py        # Graph traversal
│   ├── semantic_similarity.py # Similarity (no neural)
│   └── query_parser.py        # NL → structured query
│
├── integration/                # BRIDGES TO SANTOK_COMPLETE
│   ├── __init__.py
│   ├── token_bridge.py        # Tokenizer integration
│   ├── vector_bridge.py       # Vector store integration
│   ├── embedding_bridge.py    # Embedding integration
│   └── cognitive_pipeline.py  # End-to-end pipeline
│
├── utils/                      # UTILITIES
│   ├── __init__.py
│   ├── scoring.py             # Scoring utilities
│   ├── formatting.py          # Output formatting
│   └── validation.py          # Knowledge validation
│
├── examples/                   # EXAMPLES
│   └── numpy_gpt_integration.py
│
├── showcase.py                 # Complete demo
├── demo_pure.py               # Pure SanTOK demo
└── demo_algorithms.py         # Algorithms demo
```

### 3.2 Module Dependencies

```
                    ┌─────────────────┐
                    │  santok_complete │  (EXTERNAL - NEVER MODIFIED)
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   integration/   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│    graph/     │   │    trees/     │   │   memory/     │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                   ┌────────┴────────┐
                   │   reasoning/    │
                   └────────┬────────┘
                            │
                   ┌────────┴────────┐
                   │   algorithms/   │
                   └─────────────────┘
```

---

## 4. Graph Module

### 4.1 Overview

The Graph module provides a **custom knowledge graph** implementation.

```
┌─────────────────────────────────────────────────────────────┐
│                      GRAPH MODULE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   GraphNode ──────────── GraphEdge ──────────── GraphStore  │
│   (Entity)               (Relation)              (Storage)  │
│                                                             │
│           RelationType ─────────── RelationExtractor        │
│           (Enum: 15+)              (Pattern-based)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 GraphNode

**File:** `graph/graph_node.py`

```python
@dataclass
class GraphNode:
    """A node in the knowledge graph."""
    
    node_id: int              # Unique identifier
    text: str                 # Node content/label
    node_type: str            # "entity", "concept", "event"
    
    # Optional
    embedding_ref: str        # Link to vector embedding
    metadata: Dict[str, Any]  # Custom metadata
    created_at: float         # Timestamp
```

**Memory:** ~100 bytes per node

**Example:**
```python
node = GraphNode(
    node_id=1,
    text="SanTOK",
    node_type="system"
)
```

### 4.3 GraphEdge

**File:** `graph/graph_edge.py`

```python
@dataclass
class GraphEdge:
    """A directed edge from source to target."""
    
    edge_id: int                    # Unique identifier
    source_id: int                  # Source node ID
    target_id: int                  # Target node ID
    relation_type: RelationType     # Type of relation
    weight: float                   # Confidence (0.0 - 1.0)
    evidence: str                   # Why this edge exists
```

**Memory:** ~150 bytes per edge

### 4.4 RelationType Enum

```python
class RelationType(Enum):
    """15+ relation types supported."""
    
    # Taxonomic
    IS_A = "is_a"              # Dog IS_A Animal
    PART_OF = "part_of"        # Wheel PART_OF Car
    HAS_PART = "has_part"      # Car HAS_PART Wheel
    
    # Causal
    CAUSES = "causes"          # Fire CAUSES Smoke
    CAUSED_BY = "caused_by"    # Smoke CAUSED_BY Fire
    
    # Functional
    USES = "uses"              # Chef USES Knife
    USED_BY = "used_by"        # Knife USED_BY Chef
    DEPENDS_ON = "depends_on"  # App DEPENDS_ON Database
    
    # Semantic
    SIMILAR_TO = "similar_to"  # Cat SIMILAR_TO Dog
    OPPOSITE_OF = "opposite_of"# Hot OPPOSITE_OF Cold
    RELATED_TO = "related_to"  # (generic)
    
    # Temporal
    PRECEDES = "precedes"      # A PRECEDES B
    FOLLOWS = "follows"        # B FOLLOWS A
    
    # Source
    DERIVED_FROM = "derived_from"
    MENTIONS = "mentions"
    CONTAINS = "contains"
```

### 4.5 GraphStore

**File:** `graph/graph_store.py`

```
┌─────────────────────────────────────────────────────────────┐
│                       GRAPHSTORE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   PRIMARY STORAGE                                           │
│   ├── _nodes: Dict[int, GraphNode]                          │
│   └── _edges: Dict[int, GraphEdge]                          │
│                                                             │
│   ADJACENCY LISTS (O(1) traversal)                          │
│   ├── _outgoing: Dict[int, Set[int]]  # node → edge_ids     │
│   └── _incoming: Dict[int, Set[int]]  # node → edge_ids     │
│                                                             │
│   INDICES (Fast lookup)                                     │
│   ├── _by_relation_type: Dict[str, Set[int]]               │
│   ├── _by_node_type: Dict[str, Set[int]]                   │
│   └── _by_text: Dict[str, Set[int]]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Methods:**

| Method | Complexity | Description |
|--------|------------|-------------|
| `add_node(node)` | O(1) | Add a node |
| `get_node(id)` | O(1) | Get node by ID |
| `add_edge(src, tgt, rel)` | O(1) | Add an edge |
| `get_outgoing_edges(id)` | O(k) | Get edges from node |
| `get_incoming_edges(id)` | O(k) | Get edges to node |
| `get_neighbors(id)` | O(k) | Get connected nodes |

### 4.6 RelationExtractor

**File:** `graph/relation_extractor.py`

Extracts relations from text using **pattern matching** (no ML).

```
Text: "Python is a programming language"
      ↓
Pattern: "(\w+) is a (\w+)"
      ↓
Extracted: (Python) --[IS_A]--> (programming language)
```

---

## 5. Trees Module

### 5.1 Overview

The Trees module provides **hierarchical knowledge organization**.

```
┌─────────────────────────────────────────────────────────────┐
│                      TREES MODULE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   TreeNode ────────────── Tree ────────────── TreeStore     │
│   (Item)                 (Structure)          (Collection)  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 TreeNode

**File:** `trees/tree_node.py`

```python
@dataclass
class TreeNode:
    """A node in a tree structure."""
    
    node_id: str              # Unique identifier
    content: str              # Node content
    parent_id: Optional[str]  # Parent node ID
    children_ids: List[str]   # Child node IDs
    depth: int                # Distance from root
    
    # Links
    graph_node_id: Optional[int]    # Link to graph
    embedding_ref: Optional[str]     # Link to vector
```

**Example Tree:**
```
Artificial Intelligence (depth=0)
├── Machine Learning (depth=1)
│   ├── Supervised (depth=2)
│   ├── Unsupervised (depth=2)
│   └── Deep Learning (depth=2)
├── NLP (depth=1)
│   ├── Tokenization (depth=2)
│   └── Embeddings (depth=2)
└── Computer Vision (depth=1)
```

### 5.3 Tree

**File:** `trees/tree.py`

```
┌─────────────────────────────────────────────────────────────┐
│                         TREE                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   tree_id: str                    # Unique identifier       │
│   name: str                       # Human-readable name     │
│   root_id: Optional[str]          # Root node ID            │
│   _nodes: Dict[str, TreeNode]     # All nodes               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Traversal Methods:**

| Method | Type | Description |
|--------|------|-------------|
| `traverse_dfs(pre_order=True)` | Generator | Depth-first |
| `traverse_bfs()` | Generator | Breadth-first |
| `get_path_from_root(node_id)` | List | Root → Node path |
| `get_ancestors(node_id)` | List | All ancestors |
| `get_descendants(node_id)` | List | All descendants |

### 5.4 TreeStore

**File:** `trees/tree_store.py`

Manages multiple trees:

```python
store = TreeStore()

# Create trees
concept_tree = store.create_tree("concepts", "Concept Taxonomy")
doc_tree = store.create_tree("docs", "Document Structure")

# Access
tree = store.get_tree("concepts")
all_trees = store.list_trees()
```

---

## 6. Memory Module

### 6.1 Overview

The Memory module provides **unified knowledge access**.

```
┌─────────────────────────────────────────────────────────────┐
│                     MEMORY MODULE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   MemoryObject ────────────── UnifiedMemory                 │
│   (Knowledge Item)           (Central Hub)                  │
│                                                             │
│   Links together:                                           │
│   • Vector embeddings (from santok_complete)                │
│   • Graph nodes (from graph/)                               │
│   • Tree nodes (from trees/)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 MemoryObject

**File:** `memory/memory_object.py`

```python
@dataclass
class MemoryObject:
    """A unified knowledge object."""
    
    uid: str                          # Unique identifier
    content: str                      # Text content
    content_type: str                 # "fact", "concept", etc.
    
    # Cross-references (the unified memory contract)
    embedding_id: Optional[str]       # → Vector store
    graph_node_id: Optional[int]      # → Graph store
    tree_id: Optional[str]            # → Tree
    tree_node_id: Optional[str]       # → Tree node
    
    # Metadata
    confidence: float                 # 0.0 - 1.0
    source: str                       # Origin
    created_at: float                 # Timestamp
```

### 6.3 UnifiedMemory

**File:** `memory/unified_memory.py`

```
┌─────────────────────────────────────────────────────────────┐
│                    UNIFIED MEMORY                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│   │   objects   │   │    graph    │   │    trees    │      │
│   │ Dict[uid,   │   │ GraphStore  │   │ TreeStore   │      │
│   │ MemoryObj]  │   │             │   │             │      │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘      │
│          │                 │                 │              │
│          └─────────────────┼─────────────────┘              │
│                            │                                │
│                   ┌────────┴────────┐                       │
│                   │  Cross-linking  │                       │
│                   │    via UIDs     │                       │
│                   └─────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Methods:**

```python
# Add knowledge
obj = memory.add(
    content="SanTOK is unique",
    content_type="fact",
    auto_link_graph=True  # Auto-create graph node
)

# Add relations
memory.add_relation(uid1, uid2, RelationType.IS_A)

# Search
results = memory.search("tokenization", limit=10)

# Get by UID
obj = memory.get(uid)
```

---

## 7. Reasoning Module

### 7.1 Overview

The Reasoning module provides **symbolic inference**.

```
┌─────────────────────────────────────────────────────────────┐
│                    REASONING MODULE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   CORE                                                      │
│   ├── PathFinder         (Find paths in graph)              │
│   ├── QueryEngine        (Execute queries)                  │
│   └── Explainer          (Generate explanations)            │
│                                                             │
│   SYMBOLIC REASONING                                        │
│   ├── RuleBase           (20+ inference rules)              │
│   ├── InferenceEngine    (Rule chaining)                    │
│   └── ContradictionDetector (Find conflicts)                │
│                                                             │
│   PURE SANTOK (RECOMMENDED)                                 │
│   ├── SanTOKReasoner     (Complete reasoner)                │
│   └── SanTOKVerbalizer   (Template generation)              │
│                                                             │
│   OPTIONAL                                                  │
│   └── HybridReasoner     (LLM integration bridge)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 RuleBase

**File:** `reasoning/rule_base.py`

Contains 20+ inference rules:

```
┌─────────────────────────────────────────────────────────────┐
│                    INFERENCE RULES                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   TRANSITIVITY RULES                                        │
│   ├── transitive_is_a:     A IS_A B, B IS_A C → A IS_A C   │
│   ├── transitive_part_of:  A PART B, B PART C → A PART C   │
│   └── transitive_causes:   A CAUSE B, B CAUSE C → A CAUSE C│
│                                                             │
│   INVERSE RULES                                             │
│   ├── inverse_has_part:    A HAS_PART B → B PART_OF A      │
│   ├── inverse_causes:      A CAUSES B → B CAUSED_BY A      │
│   └── inverse_uses:        A USES B → B USED_BY A          │
│                                                             │
│   INHERITANCE RULES                                         │
│   ├── inherit_property:    A IS_A B, B HAS P → A HAS P     │
│   └── inherit_part:        A IS_A B, B HAS_PART C → ...    │
│                                                             │
│   SYMMETRY RULES                                            │
│   ├── symmetric_similar:   A SIMILAR B → B SIMILAR A       │
│   ├── symmetric_related:   A RELATED B → B RELATED A       │
│   └── symmetric_opposite:  A OPPOSITE B → B OPPOSITE A     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 InferenceEngine

**File:** `reasoning/inference_engine.py`

```python
class InferenceEngine:
    """
    Applies rules to infer new facts.
    
    Process:
    1. Load rules from RuleBase
    2. Find applicable rules
    3. Apply rules to generate new facts
    4. Propagate confidence
    5. Repeat until fixpoint
    """
```

**Confidence Propagation:**

```
New confidence = rule_confidence × min(source_confidences)

Example:
    A IS_A B (conf=0.9)
    B IS_A C (conf=0.8)
    → A IS_A C (conf=0.95 × min(0.9, 0.8) = 0.76)
```

### 7.4 ContradictionDetector

**File:** `reasoning/contradiction_detector.py`

Detects logical conflicts:

```
┌─────────────────────────────────────────────────────────────┐
│                  CONTRADICTION TYPES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   DIRECT:        A IS_A B  AND  A IS_NOT B                  │
│   CYCLIC:        A IS_A B  AND  B IS_A A                    │
│   SYMMETRIC:     A OPPOSITE B  AND  A SIMILAR B             │
│   TRANSITIVE:    A PRECEDES B  AND  B PRECEDES A            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.5 SanTOKReasoner

**File:** `reasoning/santok_reasoner.py`

The **complete pure-SanTOK reasoning system**:

```
┌─────────────────────────────────────────────────────────────┐
│                    SANTOK REASONER                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Input: Natural language question                          │
│   ↓                                                         │
│   1. Search UnifiedMemory for relevant facts                │
│   ↓                                                         │
│   2. Run InferenceEngine to derive new facts                │
│   ↓                                                         │
│   3. Find reasoning paths via PathFinder                    │
│   ↓                                                         │
│   4. Check for contradictions                               │
│   ↓                                                         │
│   5. Verbalize via SanTOKVerbalizer (templates)             │
│   ↓                                                         │
│   Output: SanTOKAnswer (text + explanation)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.6 SanTOKVerbalizer

**File:** `reasoning/santok_verbalizer.py`

Template-based text generation (**NO neural LLM**):

```
Query Type Templates:
─────────────────────
DEFINITION: "{subject} is {definition}."
RELATION:   "{subject} is {relation} {object}."
PROCESS:    "{subject} works by {mechanism}."
LIST:       "The following are relevant: {items}."
YES_NO:     "Yes, {explanation}." / "No, {explanation}."

Relation Phrases:
─────────────────
IS_A      → "is a type of"
PART_OF   → "is part of"
CAUSES    → "causes"
USES      → "uses"
...
```

---

## 8. Algorithms Module

### 8.1 Overview

**100% SANTOK-ORIGINAL algorithms.**

```
┌─────────────────────────────────────────────────────────────┐
│                  ALGORITHMS MODULE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   SanTOKRanker         → Hybrid relevance scoring           │
│   SanTOKPatternMatcher → Relation extraction (no ML)        │
│   SanTOK9Scorer        → 9-centric confidence               │
│   SanTOKGraphWalker    → Energy-based traversal             │
│   SanTOKSimilarity     → Semantic similarity (no neural)    │
│   SanTOKQueryParser    → NL → structured query              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 SanTOKRanker

**File:** `algorithms/santok_ranker.py`

**The SanTOK Ranking Formula:**

```
score = α·Relevance + β·Connectivity + γ·Hierarchy + δ·Freshness

Where:
    α = 0.4 (default)
    β = 0.3
    γ = 0.2
    δ = 0.1
```

**Component Formulas:**

```
┌─────────────────────────────────────────────────────────────┐
│                    RELEVANCE                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   relevance = Σ(token_match × position_boost) / |tokens|    │
│                                                             │
│   position_boost = 1 / (1 + log(position + 1))              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   CONNECTIVITY                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   connectivity = centrality × avg_relation_strength         │
│                                                             │
│   centrality = degree / (total_nodes - 1)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    HIERARCHY                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   hierarchy = depth_weight × (1 - sibling_penalty)          │
│               × parent_inheritance                          │
│                                                             │
│   depth_weight = 1 / (1 + depth)                            │
│   parent_inheritance = 0.9^depth                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FRESHNESS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   freshness = length_factor × access_boost                  │
│                                                             │
│   length_factor = 1 / (1 + log(content_length + 1))         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**9-Centric Transformation:**

```
digital_root = 1 + ((score × 1000 - 1) mod 9)
```

### 8.3 SanTOKPatternMatcher

**File:** `algorithms/pattern_matcher.py`

Extracts relations using **34 lexical patterns** (no ML):

```
┌─────────────────────────────────────────────────────────────┐
│                   PATTERN CATEGORIES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IS_A PATTERNS (5)                                         │
│   ├── "(\w+) is a (\w+)"                                   │
│   ├── "(\w+) are (\w+)"                                    │
│   ├── "(\w+), a type of (\w+)"                             │
│   └── ...                                                   │
│                                                             │
│   PART_OF PATTERNS (4)                                      │
│   ├── "(\w+) is part of (\w+)"                             │
│   ├── "(\w+) belongs to (\w+)"                             │
│   └── ...                                                   │
│                                                             │
│   CAUSES PATTERNS (4)                                       │
│   ├── "(\w+) causes (\w+)"                                 │
│   ├── "(\w+) leads to (\w+)"                               │
│   └── ...                                                   │
│                                                             │
│   ... 25 more pattern categories                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Confidence Formula:**

```
confidence = base × frequency_boost × proximity_boost × length_penalty

Where:
    base = 0.7
    frequency_boost = 1.0 + 0.1 × min(mentions, 5)
    proximity_boost = 1.0 / (1.0 + distance / 100)
    length_penalty = min(1.0, avg_entity_length / 3)
```

### 8.4 SanTOK9Scorer

**File:** `algorithms/nine_scorer.py`

**9-Centric mathematics:**

```
┌─────────────────────────────────────────────────────────────┐
│                  9-CENTRIC FORMULAS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   DIGITAL ROOT                                              │
│   dr(n) = 1 + ((n - 1) mod 9)                              │
│                                                             │
│   COMBINATION (mean)                                        │
│   combined = Σ(values) / len(values)                        │
│   result = to_9(combined)                                   │
│                                                             │
│   PROPAGATION                                               │
│   conf[i] = conf[0] × decay^i × (1 - dr_penalty[i])        │
│   dr_penalty = (9 - dr) / 9                                 │
│                                                             │
│   DECAY                                                     │
│   decayed = value × (dr / 9)^steps                         │
│                                                             │
│   HARMONIC                                                  │
│   harmonic = n / Σ(1/dr_i)                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.5 SanTOKGraphWalker

**File:** `algorithms/graph_walker.py`

**Energy-based graph traversal:**

```
┌─────────────────────────────────────────────────────────────┐
│                  GRAPH WALKER ALGORITHM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. Start at source node with energy E                     │
│                                                             │
│   2. At each step:                                          │
│      a. Get outgoing edges                                  │
│      b. Compute edge costs (by relation type)               │
│      c. Check energy budget                                 │
│      d. Choose next node (weighted by score)                │
│      e. Subtract cost from energy                           │
│      f. Record path                                         │
│                                                             │
│   3. Stop when:                                             │
│      - Target reached                                       │
│      - Energy depleted                                      │
│      - Max hops reached                                     │
│      - Dead end                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Relation Costs:**

| Relation | Cost | Score |
|----------|------|-------|
| IS_A | 0.5 | 1.0 |
| PART_OF | 0.5 | 0.9 |
| CAUSES | 0.7 | 0.85 |
| USES | 0.6 | 0.8 |
| SIMILAR_TO | 0.8 | 0.6 |
| RELATED_TO | 0.9 | 0.5 |

### 8.6 SanTOKSimilarity

**File:** `algorithms/semantic_similarity.py`

**Semantic similarity WITHOUT neural embeddings:**

```
┌─────────────────────────────────────────────────────────────┐
│              SIMILARITY FORMULA                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   sim(a, b) = α·Lexical + β·Ngram + γ·Position + δ·Graph   │
│                                                             │
│   α = 0.35, β = 0.25, γ = 0.20, δ = 0.20                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Component Formulas:**

```
LEXICAL (Jaccard + Dice average):
    jaccard = |A ∩ B| / |A ∪ B|
    dice = 2|A ∩ B| / (|A| + |B|)
    lexical = (jaccard + dice) / 2

N-GRAM (Character 3-grams):
    ngram_sim = 2 × |ngrams_A ∩ ngrams_B| / (|ngrams_A| + |ngrams_B|)

POSITION (Token position matching):
    position = Σ(match × position_weight) / total_weight
    position_weight = 1 / (1 + log(i + 2))

GRAPH (If available):
    - Direct edge: 1.0
    - Common neighbors: 0.5-0.8
    - 2-hop path: 0.4
    - No connection: 0.0
```

### 8.7 SanTOKQueryParser

**File:** `algorithms/query_parser.py`

**Natural language → Structured query:**

```
┌─────────────────────────────────────────────────────────────┐
│                  QUERY TYPES                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   DEFINITION    "What is X?"                                │
│   RELATION      "How is X related to Y?"                    │
│   LIST          "What are the parts of X?"                  │
│   BOOLEAN       "Is X a Y?"                                 │
│   COMPARISON    "What is the difference between X and Y?"   │
│   PROCESS       "How does X work?"                          │
│   COUNT         "How many X?"                               │
│   CAUSE         "Why does X happen?"                        │
│   EXAMPLE       "Give example of X"                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Output Structure:**

```python
@dataclass
class ParsedQuery:
    original: str           # "What is machine learning?"
    query_type: QueryType   # DEFINITION
    subject: str           # "machine learning"
    object: str            # None
    relation_hint: str     # None
    negated: bool          # False
    quantifier: str        # None
    confidence: float      # 0.9
```

---

## 9. Integration Module

### 9.1 Overview

Bridges `santok_cognitive` with `santok_complete`:

```
┌─────────────────────────────────────────────────────────────┐
│                 INTEGRATION MODULE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   TokenBridge      → SanTOK tokens → Graph nodes            │
│   VectorBridge     → SanTOK vectors ↔ Memory objects        │
│   EmbeddingBridge  → SanTOK embeddings → Node features      │
│   CognitivePipeline → End-to-end processing                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 TokenBridge

Converts SanTOK tokens to graph nodes:

```
SanTOK Token                    Graph Node
─────────────────────────────────────────────
{                               GraphNode(
  "token": "machine",             node_id=hash("machine"),
  "uid": "abc123",                text="machine",
  "type": "word"                  node_type="token",
}                                 embedding_ref="abc123"
                                )
```

### 9.3 CognitivePipeline

End-to-end processing:

```
Text Input
    ↓
[1] Tokenize (via santok_complete)
    ↓
[2] Generate embeddings (via santok_complete)
    ↓
[3] Store in UnifiedMemory
    ↓
[4] Extract relations (SanTOKPatternMatcher)
    ↓
[5] Build graph edges
    ↓
[6] Query processing
    ↓
[7] Inference (InferenceEngine)
    ↓
[8] Verbalize (SanTOKVerbalizer)
    ↓
Answer Output
```

---

## 10. Data Flow

### 10.1 Knowledge Ingestion Flow

```
                    ┌─────────────┐
                    │  Raw Text   │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ Tokenizer   │ (santok_complete)
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  Embedding  │ │   Pattern   │ │   Memory    │
    │  Generator  │ │   Matcher   │ │   Object    │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   Vector    │ │    Graph    │ │   Unified   │
    │   Store     │ │    Store    │ │   Memory    │
    └─────────────┘ └─────────────┘ └─────────────┘
```

### 10.2 Query Processing Flow

```
                    ┌─────────────┐
                    │   Query     │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ QueryParser │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ QueryEngine │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   Vector    │ │    Graph    │ │    Tree     │
    │   Search    │ │  Traversal  │ │  Navigation │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────┴──────┐
                    │  Inference  │
                    │   Engine    │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ Verbalizer  │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   Answer    │
                    └─────────────┘
```

---

## 11. Mathematical Foundations

### 11.1 Core Formulas Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SANTOK MATHEMATICS                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  DIGITAL ROOT (9-centric)                                           │
│  dr(n) = 1 + ((n - 1) mod 9)                                       │
│                                                                     │
│  HYBRID RANKING                                                     │
│  score = 0.4·R + 0.3·C + 0.2·H + 0.1·F                             │
│                                                                     │
│  SIMILARITY (multi-component)                                       │
│  sim = 0.35·Lex + 0.25·Ngram + 0.20·Pos + 0.20·Graph               │
│                                                                     │
│  CONFIDENCE PROPAGATION                                             │
│  conf_new = rule_conf × min(source_confs)                          │
│                                                                     │
│  GRAPH CENTRALITY                                                   │
│  centrality = degree / (N - 1)                                     │
│                                                                     │
│  POSITION BOOST                                                     │
│  boost = 1 / (1 + log(position + 1))                               │
│                                                                     │
│  TREE DEPTH WEIGHT                                                  │
│  weight = 1 / (1 + depth)                                          │
│                                                                     │
│  ENERGY DECAY (graph walk)                                          │
│  energy_new = energy - relation_cost - decay_rate                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 11.2 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Add node | O(1) | O(1) |
| Get node | O(1) | O(1) |
| Add edge | O(1) | O(1) |
| Get neighbors | O(k) | O(k) |
| BFS traversal | O(V+E) | O(V) |
| DFS traversal | O(V+E) | O(V) |
| Inference (1 round) | O(E×R) | O(E) |
| Pattern matching | O(n×p) | O(1) |

Where: V=nodes, E=edges, R=rules, n=text_length, p=patterns, k=degree

---

## Summary

SanTOK Cognitive is a **100% unique cognitive system** with:

- **6 modules**: Graph, Trees, Memory, Reasoning, Algorithms, Integration
- **50+ classes**: All custom implementations
- **6 custom algorithms**: Ranker, PatternMatcher, 9Scorer, GraphWalker, Similarity, QueryParser
- **20+ inference rules**: Transitivity, inverse, inheritance, symmetry
- **15+ relation types**: IS_A, PART_OF, CAUSES, USES, etc.
- **0 external AI dependencies**: No GPT, no transformers, no neural networks

**This is what makes SanTOK STAND OUT.**

