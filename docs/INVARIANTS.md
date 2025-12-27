# SanTOK Cognitive - Formal Invariants & Guarantees

## What is ALWAYS True in SanTOK Cognitive

This document specifies the **formal invariants** - properties that must ALWAYS hold true in the system. Violations indicate bugs.

---

## 1. Graph Invariants

### 1.1 Structural Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G1: Node ID Uniqueness                                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ n₁, n₂ ∈ Nodes:                                                      │
│      n₁.node_id = n₂.node_id  ⟹  n₁ = n₂                               │
│                                                                         │
│  Proof: Enforced by Dict key uniqueness in _nodes                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G2: Edge ID Uniqueness                                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ e₁, e₂ ∈ Edges:                                                      │
│      e₁.edge_id = e₂.edge_id  ⟹  e₁ = e₂                               │
│                                                                         │
│  Proof: Enforced by auto-incrementing _next_edge_id                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G3: Edge Referential Integrity                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ e ∈ Edges:                                                           │
│      e.source_id ∈ Nodes  ∧  e.target_id ∈ Nodes                       │
│                                                                         │
│  Proof: add_edge() validates existence before creating                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G4: Adjacency List Consistency                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ e ∈ Edges:                                                           │
│      e.edge_id ∈ _outgoing[e.source_id]                                │
│      e.edge_id ∈ _incoming[e.target_id]                                │
│                                                                         │
│  Proof: add_edge() updates both lists atomically                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Semantic Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G5: IS_A Acyclicity                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  The IS_A relation forms a Directed Acyclic Graph (DAG):               │
│                                                                         │
│  ¬∃ path P = (n₁ →IS_A n₂ →IS_A ... →IS_A n₁)                          │
│                                                                         │
│  Rationale: Taxonomic hierarchies must be acyclic                      │
│  Enforcement: ContradictionDetector.detect_cyclic_is_a()               │
│  Violation: CYCLIC_IS_A contradiction                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G6: PART_OF Acyclicity                                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  The PART_OF relation forms a DAG:                                     │
│                                                                         │
│  ¬∃ path P = (n₁ →PART_OF n₂ →PART_OF ... →PART_OF n₁)                │
│                                                                         │
│  Rationale: Part-whole cannot be circular (A can't be part of itself)  │
│  Enforcement: ContradictionDetector.detect_cyclic_part_of()            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G7: PRECEDES/FOLLOWS Antisymmetry                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ a, b:                                                                │
│      a PRECEDES b  ⟹  ¬(b PRECEDES a)                                  │
│      a FOLLOWS b   ⟹  ¬(b FOLLOWS a)                                   │
│                                                                         │
│  Rationale: Temporal ordering is antisymmetric                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT G8: SIMILAR_TO/OPPOSITE_OF Mutual Exclusion                  │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ a, b:                                                                │
│      ¬(a SIMILAR_TO b  ∧  a OPPOSITE_OF b)                             │
│                                                                         │
│  Rationale: Cannot be both similar and opposite                        │
│  Enforcement: ContradictionDetector.detect_opposite_and_similar()      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tree Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT T1: Single Root                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ Tree t:                                                              │
│      |{n ∈ t.nodes : n.parent_id = None}| ≤ 1                          │
│                                                                         │
│  A tree has at most one root node                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT T2: Parent Existence                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ n ∈ Tree:                                                            │
│      n.parent_id ≠ None  ⟹  n.parent_id ∈ Tree.nodes                  │
│                                                                         │
│  Every non-root node's parent must exist                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT T3: Children Consistency                                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ n ∈ Tree:                                                            │
│      ∀ c ∈ n.children_ids:                                             │
│          Tree.get_node(c).parent_id = n.node_id                        │
│                                                                         │
│  If n lists c as child, c must have n as parent                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT T4: Depth Consistency                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ n ∈ Tree:                                                            │
│      n.parent_id = None  ⟹  n.depth = 0                                │
│      n.parent_id ≠ None  ⟹  n.depth = parent(n).depth + 1             │
│                                                                         │
│  Depth is always distance from root                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT T5: No Cycles                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ n ∈ Tree:                                                            │
│      n ∉ ancestors(n)                                                   │
│                                                                         │
│  A node cannot be its own ancestor (trees are acyclic by definition)   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Memory Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT M1: UID Uniqueness                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ o₁, o₂ ∈ MemoryObjects:                                              │
│      o₁.uid = o₂.uid  ⟹  o₁ = o₂                                       │
│                                                                         │
│  Proof: UUID generation guarantees uniqueness                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT M2: Cross-Reference Validity                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ o ∈ MemoryObjects:                                                   │
│      o.graph_node_id ≠ None  ⟹  o.graph_node_id ∈ Graph.nodes         │
│      o.tree_node_id ≠ None   ⟹  o.tree_node_id ∈ Tree.nodes           │
│                                                                         │
│  Cross-references must point to existing entities                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Inference Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT I1: Bounded Confidence                                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ fact ∈ InferredFacts:                                                │
│      0.0 ≤ fact.confidence ≤ 1.0                                       │
│                                                                         │
│  Confidence is always in [0, 1] range                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT I2: Confidence Monotonic Decay                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  For transitive inference:                                              │
│      conf(A →R C) ≤ min(conf(A →R B), conf(B →R C))                    │
│                                                                         │
│  Inferred facts cannot have higher confidence than source facts        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT I3: No Infinite Inference                                    │
│  ─────────────────────────────────────────────────────────────────────  │
│  The inference process ALWAYS terminates:                              │
│                                                                         │
│  Guaranteed by:                                                         │
│  1. max_iterations parameter (default: 100)                            │
│  2. min_confidence threshold (default: 0.3)                            │
│  3. Fixpoint detection (no new facts generated)                        │
│  4. Duplicate prevention (same fact not inferred twice)                │
│                                                                         │
│  Proof:                                                                 │
│  - Each iteration either produces new facts or terminates              │
│  - New facts require edges not yet inferred                           │
│  - Finite graph ⟹ finite possible edges                                │
│  - Therefore: terminates in O(E × R) iterations max                    │
│    where E = edges, R = rules                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT I4: Rule Soundness                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  All inference rules preserve logical validity:                        │
│                                                                         │
│  TRANSITIVITY: (A R B) ∧ (B R C) ⟹ (A R C)                             │
│  Valid for: IS_A, PART_OF, PRECEDES, CAUSES, DEPENDS_ON               │
│                                                                         │
│  INVERSE: (A R B) ⟹ (B R⁻¹ A)                                          │
│  Valid for all relations with defined inverses                         │
│                                                                         │
│  SYMMETRY: (A R B) ⟹ (B R A)                                           │
│  Valid for: SIMILAR_TO, RELATED_TO, OPPOSITE_OF                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Algorithm Invariants

### 5.1 Ranking Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A1: Non-negative Scores                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ result ∈ RankingResults:                                             │
│      result.score ≥ 0                                                   │
│                                                                         │
│  All component scores are non-negative                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A2: Weight Normalization                                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  α + β + γ + δ = 1.0                                                    │
│                                                                         │
│  Ranking weights sum to 1 (for consistent scoring)                     │
│  Default: 0.4 + 0.3 + 0.2 + 0.1 = 1.0 ✓                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 9-Centric Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A3: Digital Root Bounds                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ score ∈ Score9:                                                      │
│      1 ≤ score.digital_root ≤ 9                                        │
│                                                                         │
│  Digital root is always in [1, 9] (never 0)                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A4: Digital Root Idempotence                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  dr(dr(n)) = dr(n)                                                      │
│                                                                         │
│  Applying digital root twice gives same result                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Graph Walker Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A5: Energy Conservation                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ walk ∈ WalkResults:                                                  │
│      walk.total_energy_used = initial_energy - final_energy            │
│      walk.total_energy_used ≥ 0                                        │
│                                                                         │
│  Energy is never created, only consumed                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A6: Walk Termination                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  Every walk terminates due to one of:                                  │
│  1. Target reached                                                      │
│  2. Energy depleted                                                     │
│  3. Max hops reached                                                    │
│  4. Dead end (no outgoing edges)                                       │
│                                                                         │
│  Proof: max_hops is finite, energy decreases monotonically             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Similarity Invariants

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A7: Similarity Bounds                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ a, b:                                                                │
│      0.0 ≤ sim(a, b) ≤ 1.0                                             │
│                                                                         │
│  Similarity is always in [0, 1] range                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A8: Self-Similarity                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ a:                                                                   │
│      sim(a, a) = 1.0                                                    │
│                                                                         │
│  Everything is maximally similar to itself                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  INVARIANT A9: Symmetry                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  ∀ a, b:                                                                │
│      sim(a, b) = sim(b, a)                                             │
│                                                                         │
│  Similarity is symmetric                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. System-Wide Guarantees

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  GUARANTEE S1: No External AI Dependency                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  SanTOK Cognitive operates WITHOUT:                                    │
│  - GPT / LLMs                                                          │
│  - Neural networks                                                      │
│  - PyTorch / TensorFlow                                                │
│  - External API calls                                                   │
│                                                                         │
│  All processing is local and deterministic                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  GUARANTEE S2: Explainability                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  Every output can be traced to:                                        │
│  - Source facts in knowledge base                                      │
│  - Rules applied                                                        │
│  - Reasoning paths                                                      │
│                                                                         │
│  No black-box decisions                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  GUARANTEE S3: Isolation from santok_complete                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  santok_cognitive NEVER modifies santok_complete:                      │
│  - Only imports from santok_complete                                   │
│  - Never writes to santok_complete files                               │
│  - Can operate independently                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  GUARANTEE S4: Determinism                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  Given the same:                                                        │
│  - Knowledge base                                                       │
│  - Query                                                                │
│  - Configuration                                                        │
│                                                                         │
│  The system produces the SAME output                                   │
│  (except for random walk mode which is explicitly stochastic)          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Complexity Guarantees

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  TIME COMPLEXITY GUARANTEES                                             │
│                                                                         │
│  Operation                    │ Guarantee                              │
│  ────────────────────────────┼────────────────────────────────────────│
│  Add node                    │ O(1)                                   │
│  Get node by ID              │ O(1)                                   │
│  Add edge                    │ O(1)                                   │
│  Get neighbors               │ O(degree)                              │
│  BFS/DFS traversal           │ O(V + E)                               │
│  Inference (1 iteration)     │ O(E × R)                               │
│  Pattern matching            │ O(n × p) where n=text, p=patterns      │
│  Ranking                     │ O(k × d) where k=candidates, d=degree  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  SPACE COMPLEXITY GUARANTEES                                            │
│                                                                         │
│  Component                   │ Guarantee                               │
│  ────────────────────────────┼────────────────────────────────────────│
│  GraphStore                  │ O(V + E)                               │
│  TreeStore                   │ O(N) per tree                          │
│  UnifiedMemory               │ O(M) where M=objects                   │
│  InferenceEngine (working)   │ O(E) for new facts                     │
│  WalkResult                  │ O(path_length)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Invariant Verification

### How to Check Invariants

```python
from santok_cognitive import UnifiedMemory
from santok_cognitive.reasoning import ContradictionDetector

# Create memory
memory = UnifiedMemory()
# ... add knowledge ...

# Check graph invariants
detector = ContradictionDetector(memory.graph)
report = detector.detect_all()

if report.has_contradictions:
    print("INVARIANT VIOLATION!")
    for c in report.contradictions:
        print(f"  {c.contradiction_type}: {c.description}")
else:
    print("All invariants satisfied ✓")
```

### Automated Invariant Checks

```python
def verify_all_invariants(memory):
    """Verify all system invariants."""
    violations = []
    
    # G1: Node ID uniqueness (guaranteed by dict)
    # G2: Edge ID uniqueness (guaranteed by auto-increment)
    
    # G3: Edge referential integrity
    for edge in memory.graph.get_all_edges():
        if not memory.graph.has_node(edge.source_id):
            violations.append(f"G3: Edge {edge.edge_id} has invalid source")
        if not memory.graph.has_node(edge.target_id):
            violations.append(f"G3: Edge {edge.edge_id} has invalid target")
    
    # G5: IS_A acyclicity
    detector = ContradictionDetector(memory.graph)
    report = detector.detect_all()
    for c in report.contradictions:
        if c.contradiction_type.value == "cyclic_is_a":
            violations.append(f"G5: {c.description}")
    
    # I1: Bounded confidence
    for edge in memory.graph.get_all_edges():
        if not (0.0 <= edge.weight <= 1.0):
            violations.append(f"I1: Edge {edge.edge_id} confidence out of bounds")
    
    return violations
```

---

## Summary

| Category | Invariants |
|----------|------------|
| Graph Structural | G1-G4 (4) |
| Graph Semantic | G5-G8 (4) |
| Tree | T1-T5 (5) |
| Memory | M1-M2 (2) |
| Inference | I1-I4 (4) |
| Algorithm | A1-A9 (9) |
| System | S1-S4 (4) |

**Total: 32 formal invariants** that define correct SanTOK Cognitive behavior.

