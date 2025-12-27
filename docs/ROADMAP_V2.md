# SanTOK Cognitive v2 Roadmap

## Current State (v1.0)

**Completed:**
- ✅ Graph module (nodes, edges, 15 relation types)
- ✅ Trees module (hierarchy, traversal)
- ✅ Memory module (unified access)
- ✅ Reasoning module (20+ inference rules)
- ✅ 6 custom algorithms
- ✅ Full documentation
- ✅ Formal invariants

**Limitations:**
- Static knowledge (no learning)
- Simple contradiction handling
- Template-based verbalization
- No belief revision

---

## v2 Roadmap

### Phase 1: Belief Revision (v2.1)

**Goal:** Handle conflicting information gracefully

```
┌─────────────────────────────────────────────────────────────┐
│                   BELIEF REVISION                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CURRENT (v1):                                              │
│  • New fact added                                           │
│  • Contradictions detected                                  │
│  • ❌ Manual resolution required                            │
│                                                             │
│  PROPOSED (v2):                                             │
│  • New fact added                                           │
│  • Contradictions detected                                  │
│  • ✅ Automatic resolution via trust/recency ranking        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
1. **Trust Scoring**
   ```python
   class SourceTrust:
       def __init__(self):
           self.trust_scores: Dict[str, float] = {}
       
       def get_trust(self, source: str) -> float:
           return self.trust_scores.get(source, 0.5)
       
       def update_trust(self, source: str, feedback: bool):
           # Increase/decrease based on feedback
   ```

2. **Recency Weighting**
   ```python
   def recency_weight(timestamp: float) -> float:
       age_days = (time.time() - timestamp) / 86400
       return 0.9 ** age_days  # Exponential decay
   ```

3. **Conflict Resolution Strategies**
   ```python
   class ConflictStrategy(Enum):
       TRUST_BASED = "trust"      # Higher trust source wins
       RECENCY = "recency"        # More recent wins
       CONFIDENCE = "confidence"  # Higher confidence wins
       CONSERVATIVE = "keep_old"  # Keep existing, reject new
       AGGRESSIVE = "keep_new"    # Accept new, remove old
   ```

4. **Belief Retraction**
   ```python
   def retract_belief(graph, fact_id):
       """Remove fact and all inferences derived from it."""
       # 1. Find all facts inferred from this one
       # 2. Recursively retract inferred facts
       # 3. Remove the original fact
       # 4. Re-run inference to rebuild consistent state
   ```

---

### Phase 2: Incremental Learning (v2.2)

**Goal:** Learn from interactions without retraining

```
┌─────────────────────────────────────────────────────────────┐
│                  INCREMENTAL LEARNING                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT WE DON'T DO:                                          │
│  • Neural network training                                  │
│  • Gradient descent                                         │
│  • Weight updates                                           │
│                                                             │
│  WHAT WE DO:                                                │
│  • Pattern learning (new regex patterns)                    │
│  • Template learning (new verbalization templates)          │
│  • Relation strength learning (adjust weights)              │
│  • Co-occurrence learning (statistical patterns)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**

1. **Pattern Learning**
   ```python
   class PatternLearner:
       """Learn new extraction patterns from examples."""
       
       def learn_from_example(self, text: str, relation: Tuple[str, str, RelationType]):
           """
           Given: "Python is used for machine learning"
                  (Python, machine learning, USED_FOR)
           
           Learn: r"(\w+) is used for (\w+)" → USED_FOR
           """
           subject, obj, rel_type = relation
           
           # Find text between subject and object
           # Generalize to pattern
           # Add to pattern database
   ```

2. **Template Learning**
   ```python
   class TemplateLearner:
       """Learn verbalization templates from examples."""
       
       def learn_from_example(self, query_type: str, output: str, facts: List[str]):
           """
           Given: 
             query_type = "definition"
             output = "Machine learning is a subset of AI that learns from data"
             facts = ["Machine learning IS_A AI", "Machine learning learns from data"]
           
           Learn: "{subject} is a {parent} that {property}"
           """
   ```

3. **Relation Weight Learning**
   ```python
   class RelationWeightLearner:
       """Adjust relation weights based on feedback."""
       
       def update_weight(self, relation_type: RelationType, feedback: float):
           """
           If users consistently prefer paths with CAUSES relations,
           increase CAUSES weight in SanTOKRanker.
           """
           current = self.weights[relation_type]
           self.weights[relation_type] = current * 0.9 + feedback * 0.1
   ```

4. **Co-occurrence Learning**
   ```python
   class CooccurrenceLearner:
       """Learn which concepts frequently appear together."""
       
       def __init__(self):
           self.cooccurrence: Dict[Tuple[str, str], int] = {}
       
       def observe(self, concepts: List[str]):
           for i, c1 in enumerate(concepts):
               for c2 in concepts[i+1:]:
                   key = tuple(sorted([c1, c2]))
                   self.cooccurrence[key] = self.cooccurrence.get(key, 0) + 1
       
       def get_related(self, concept: str) -> List[str]:
           """Return concepts that frequently co-occur."""
   ```

---

### Phase 3: Advanced Contradiction Resolution (v2.3)

**Goal:** Sophisticated handling of inconsistencies

```
┌─────────────────────────────────────────────────────────────┐
│              ADVANCED CONTRADICTION RESOLUTION               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CONTRADICTION TYPES:                                       │
│                                                             │
│  1. HARD CONTRADICTION                                      │
│     A IS_A B AND A IS_NOT B                                │
│     Resolution: Remove one (trust-based)                   │
│                                                             │
│  2. SOFT CONTRADICTION                                      │
│     A IS_A B (conf=0.9) AND A IS_A C (conf=0.8)            │
│     where B and C are exclusive                            │
│     Resolution: Keep higher confidence                     │
│                                                             │
│  3. TEMPORAL CONTRADICTION                                  │
│     A IS_A B (2020) AND A IS_NOT B (2024)                  │
│     Resolution: Facts evolve, keep most recent             │
│                                                             │
│  4. SCOPE CONTRADICTION                                     │
│     "Dogs are pets" (general) AND "Wild dogs are not pets" │
│     Resolution: Create scope hierarchy                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**

1. **Contradiction Severity Scoring**
   ```python
   def contradiction_severity(c: Contradiction) -> float:
       """Score how serious a contradiction is."""
       base = {
           ContradictionType.DIRECT: 1.0,
           ContradictionType.CYCLIC: 0.8,
           ContradictionType.SEMANTIC: 0.6,
           ContradictionType.TEMPORAL: 0.4,
       }
       return base[c.type] * average_confidence(c.facts)
   ```

2. **Resolution Strategies**
   ```python
   class ResolutionStrategy:
       def resolve(self, contradiction: Contradiction) -> Resolution:
           raise NotImplementedError
   
   class TrustBasedResolution(ResolutionStrategy):
       def resolve(self, c):
           # Keep fact from more trusted source
   
   class RecencyResolution(ResolutionStrategy):
       def resolve(self, c):
           # Keep more recent fact
   
   class ConfidenceResolution(ResolutionStrategy):
       def resolve(self, c):
           # Keep higher confidence fact
   
   class ConsensusResolution(ResolutionStrategy):
       def resolve(self, c):
           # Keep fact supported by more sources
   ```

3. **Scope-Aware Facts**
   ```python
   @dataclass
   class ScopedFact:
       content: str
       scope: Optional[str] = None  # None = universal
       
       # Examples:
       # ("Dogs are pets", scope=None) - universal
       # ("Wild dogs are not pets", scope="wild") - scoped
   ```

4. **Non-Monotonic Reasoning**
   ```python
   class NonMonotonicReasoner:
       """Support default reasoning with exceptions."""
       
       def query(self, subject: str, predicate: str) -> Tuple[bool, float, str]:
           """
           Returns (answer, confidence, explanation)
           
           Query: "Is Tweety a bird?"
           Default: "Birds fly" (confidence 0.9)
           Exception: "Penguins don't fly" (confidence 1.0)
           
           If Tweety IS_A Penguin:
               Return (False, 1.0, "Tweety is a penguin, penguins don't fly")
           Else:
               Return (True, 0.9, "Tweety is a bird, birds typically fly")
           """
   ```

---

### Phase 4: Enhanced Verbalization (v2.4)

**Goal:** More natural output without neural networks

```
┌─────────────────────────────────────────────────────────────┐
│               ENHANCED VERBALIZATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CURRENT (v1):                                              │
│  • Fixed templates                                          │
│  • Simple slot filling                                      │
│  • Limited variation                                        │
│                                                             │
│  PROPOSED (v2):                                             │
│  • Template variants (5-10 per type)                       │
│  • Markov chain sentence variation                         │
│  • Rhetorical structure awareness                          │
│  • Complexity-appropriate language                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**

1. **Template Variants**
   ```python
   DEFINITION_TEMPLATES = [
       "{subject} is {definition}.",
       "{subject} can be defined as {definition}.",
       "{subject} refers to {definition}.",
       "The term {subject} describes {definition}.",
       "In this context, {subject} means {definition}.",
   ]
   
   def select_template(templates: List[str], context: Dict) -> str:
       """Select appropriate template based on context."""
       # Consider: formality level, length preference, previous templates used
   ```

2. **Sentence Variation (Non-Neural)**
   ```python
   class SentenceVariator:
       """Vary sentences using rules, not neural networks."""
       
       SYNONYM_MAP = {
           "is": ["represents", "denotes", "means"],
           "contains": ["includes", "comprises", "encompasses"],
           "causes": ["leads to", "results in", "produces"],
       }
       
       def vary(self, sentence: str) -> str:
           """Replace words with synonyms probabilistically."""
   ```

3. **Rhetorical Structures**
   ```python
   class RhetoricalPlanner:
       """Plan answer structure based on query complexity."""
       
       def plan(self, query_type: str, fact_count: int) -> List[str]:
           """
           Simple query (1-2 facts): Direct answer
           Complex query (3+ facts): Introduction → Body → Summary
           """
           if fact_count <= 2:
               return ["direct_answer"]
           else:
               return ["introduction", "main_points", "conclusion"]
   ```

4. **Complexity Adaptation**
   ```python
   class ComplexityAdapter:
       """Adjust language complexity for audience."""
       
       LEVELS = {
           "simple": {"max_sentence_length": 15, "vocabulary": "basic"},
           "normal": {"max_sentence_length": 25, "vocabulary": "standard"},
           "expert": {"max_sentence_length": 40, "vocabulary": "technical"},
       }
       
       def adapt(self, text: str, level: str) -> str:
           """Simplify or complexify text as needed."""
   ```

---

### Phase 5: Performance Optimization (v2.5)

**Goal:** Scale to larger knowledge bases

```
┌─────────────────────────────────────────────────────────────┐
│              PERFORMANCE OPTIMIZATION                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CURRENT LIMITS:                                            │
│  • ~100K nodes comfortable                                  │
│  • Inference can be slow on dense graphs                   │
│  • All in-memory                                           │
│                                                             │
│  TARGETS:                                                   │
│  • 1M+ nodes                                               │
│  • Sub-second inference                                    │
│  • Optional disk persistence                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**

1. **Lazy Loading**
   ```python
   class LazyGraphStore:
       """Load subgraphs on demand."""
       
       def __init__(self, storage_path: str):
           self._loaded_nodes: Dict[int, GraphNode] = {}
           self._storage = storage_path
       
       def get_node(self, node_id: int) -> GraphNode:
           if node_id not in self._loaded_nodes:
               self._loaded_nodes[node_id] = self._load_from_disk(node_id)
           return self._loaded_nodes[node_id]
   ```

2. **Inference Caching**
   ```python
   class InferenceCache:
       """Cache inference results."""
       
       def __init__(self, max_size: int = 10000):
           self._cache: Dict[Tuple, InferenceResult] = {}
           self._lru: List[Tuple] = []
       
       def get_or_compute(self, key: Tuple, compute_fn) -> InferenceResult:
           if key in self._cache:
               return self._cache[key]
           result = compute_fn()
           self._cache[key] = result
           return result
   ```

3. **Parallel Inference**
   ```python
   class ParallelInferenceEngine:
       """Run independent rules in parallel."""
       
       def infer_all(self) -> InferenceResult:
           # Group rules by independence
           independent_groups = self._group_independent_rules()
           
           # Run each group in parallel
           with ThreadPoolExecutor() as executor:
               futures = [
                   executor.submit(self._apply_rule_group, group)
                   for group in independent_groups
               ]
               results = [f.result() for f in futures]
           
           return self._merge_results(results)
   ```

4. **Disk Persistence**
   ```python
   class PersistentGraphStore(GraphStore):
       """Graph with disk persistence."""
       
       def __init__(self, db_path: str):
           super().__init__()
           self._db = sqlite3.connect(db_path)
           self._setup_tables()
       
       def add_node(self, node: GraphNode) -> int:
           # Add to memory
           super().add_node(node)
           # Persist to disk
           self._db.execute(
               "INSERT INTO nodes VALUES (?, ?, ?)",
               (node.node_id, node.text, node.node_type)
           )
           return node.node_id
   ```

---

## Timeline

| Phase | Version | Target | Features |
|-------|---------|--------|----------|
| 1 | v2.1 | Q1 2025 | Belief Revision |
| 2 | v2.2 | Q2 2025 | Incremental Learning |
| 3 | v2.3 | Q3 2025 | Advanced Contradictions |
| 4 | v2.4 | Q4 2025 | Enhanced Verbalization |
| 5 | v2.5 | Q1 2026 | Performance Optimization |

---

## Non-Goals for v2

**We will NOT add:**
- ❌ Neural networks
- ❌ LLM integration as core feature
- ❌ External API dependencies
- ❌ GPU requirements
- ❌ Cloud-only features

**SanTOK Cognitive remains 100% local, 100% symbolic, 100% explainable.**

---

## Contributing

To contribute to v2 development:

1. Choose a phase/feature
2. Create new files in `santok_cognitive/` (never modify existing)
3. Add tests
4. Update documentation
5. Submit PR

Remember: **Safety first** - never modify `santok_complete` or existing `santok_cognitive` modules.

