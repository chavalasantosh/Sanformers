# Reasoning Module - Deep Technical Specification

## 1. Module Purpose

The Reasoning module provides **symbolic inference** without neural networks.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   REASONING MODULE COMPONENTS                               │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                    CORE                              │  │
│   ├─────────────────────────────────────────────────────┤  │
│   │ PathFinder          │ Find paths in graph           │  │
│   │ QueryEngine         │ Execute queries               │  │
│   │ Explainer           │ Generate explanations         │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                  SYMBOLIC                            │  │
│   ├─────────────────────────────────────────────────────┤  │
│   │ RuleBase            │ 20+ inference rules           │  │
│   │ InferenceEngine     │ Rule chaining                 │  │
│   │ ContradictionDetector│ Find logical conflicts       │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │               PURE SANTOK                            │  │
│   ├─────────────────────────────────────────────────────┤  │
│   │ SanTOKReasoner      │ Complete reasoner (no LLM)   │  │
│   │ SanTOKVerbalizer    │ Template generation          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. RuleBase - Complete Rule Reference

### 2.1 Rule Structure

```python
@dataclass
class InferenceRule:
    """A single inference rule."""
    
    rule_id: str              # Unique identifier
    rule_type: RuleType       # TRANSITIVITY | INVERSE | INHERITANCE | SYMMETRY
    
    # Pattern matching
    pattern_relations: List[RelationType]   # Input relation types
    pattern_count: int                       # Number of edges needed
    
    # Output
    inferred_relation: RelationType          # Resulting relation
    confidence_factor: float                 # Confidence multiplier
    
    # Conditions (optional)
    require_same_target: bool                # For 2-edge patterns
    require_chain: bool                      # Source1 → X → Target1
```

### 2.2 All 20+ Rules

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TRANSITIVITY RULES                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RULE: transitive_is_a                                                  │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[IS_A]--> B --[IS_A]--> C                              │
│  Infers:    A --[IS_A]--> C                                            │
│  Confidence: 0.95 × min(conf_AB, conf_BC)                              │
│  Example:   Dog IS_A Mammal, Mammal IS_A Animal → Dog IS_A Animal      │
│                                                                         │
│  RULE: transitive_part_of                                               │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[PART_OF]--> B --[PART_OF]--> C                        │
│  Infers:    A --[PART_OF]--> C                                         │
│  Confidence: 0.90 × min(conf_AB, conf_BC)                              │
│  Example:   Piston PART_OF Engine, Engine PART_OF Car                  │
│             → Piston PART_OF Car                                        │
│                                                                         │
│  RULE: transitive_causes                                                │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[CAUSES]--> B --[CAUSES]--> C                          │
│  Infers:    A --[CAUSES]--> C                                          │
│  Confidence: 0.85 × min(conf_AB, conf_BC)                              │
│  Example:   Fire CAUSES Heat, Heat CAUSES Burn → Fire CAUSES Burn      │
│                                                                         │
│  RULE: transitive_precedes                                              │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[PRECEDES]--> B --[PRECEDES]--> C                      │
│  Infers:    A --[PRECEDES]--> C                                        │
│  Confidence: 0.95 × min(conf_AB, conf_BC)                              │
│  Example:   Monday PRECEDES Tuesday, Tuesday PRECEDES Wednesday        │
│             → Monday PRECEDES Wednesday                                 │
│                                                                         │
│  RULE: transitive_depends                                               │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[DEPENDS_ON]--> B --[DEPENDS_ON]--> C                  │
│  Infers:    A --[DEPENDS_ON]--> C                                      │
│  Confidence: 0.85 × min(conf_AB, conf_BC)                              │
│  Example:   App DEPENDS_ON API, API DEPENDS_ON Database                │
│             → App DEPENDS_ON Database                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        INVERSE RULES                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RULE: inverse_has_part                                                 │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[HAS_PART]--> B                                        │
│  Infers:    B --[PART_OF]--> A                                         │
│  Confidence: 1.0 × conf_AB (no loss)                                   │
│  Example:   Car HAS_PART Wheel → Wheel PART_OF Car                     │
│                                                                         │
│  RULE: inverse_part_of                                                  │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[PART_OF]--> B                                         │
│  Infers:    B --[HAS_PART]--> A                                        │
│  Confidence: 1.0 × conf_AB                                             │
│                                                                         │
│  RULE: inverse_causes                                                   │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[CAUSES]--> B                                          │
│  Infers:    B --[CAUSED_BY]--> A                                       │
│  Confidence: 1.0 × conf_AB                                             │
│  Example:   Fire CAUSES Smoke → Smoke CAUSED_BY Fire                   │
│                                                                         │
│  RULE: inverse_caused_by                                                │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[CAUSED_BY]--> B                                       │
│  Infers:    B --[CAUSES]--> A                                          │
│  Confidence: 1.0 × conf_AB                                             │
│                                                                         │
│  RULE: inverse_uses                                                     │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[USES]--> B                                            │
│  Infers:    B --[USED_BY]--> A                                         │
│  Confidence: 1.0 × conf_AB                                             │
│  Example:   Chef USES Knife → Knife USED_BY Chef                       │
│                                                                         │
│  RULE: inverse_used_by                                                  │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[USED_BY]--> B                                         │
│  Infers:    B --[USES]--> A                                            │
│  Confidence: 1.0 × conf_AB                                             │
│                                                                         │
│  RULE: inverse_precedes                                                 │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[PRECEDES]--> B                                        │
│  Infers:    B --[FOLLOWS]--> A                                         │
│  Confidence: 1.0 × conf_AB                                             │
│  Example:   Monday PRECEDES Tuesday → Tuesday FOLLOWS Monday           │
│                                                                         │
│  RULE: inverse_follows                                                  │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[FOLLOWS]--> B                                         │
│  Infers:    B --[PRECEDES]--> A                                        │
│  Confidence: 1.0 × conf_AB                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      INHERITANCE RULES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RULE: inherit_through_is_a                                             │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[IS_A]--> B, B --[HAS_PART]--> C                       │
│  Infers:    A --[HAS_PART]--> C                                        │
│  Confidence: 0.80 × min(conf_AB, conf_BC)                              │
│  Example:   Dog IS_A Mammal, Mammal HAS_PART Lungs                     │
│             → Dog HAS_PART Lungs                                        │
│                                                                         │
│  RULE: inherit_uses_through_is_a                                        │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[IS_A]--> B, B --[USES]--> C                           │
│  Infers:    A --[USES]--> C                                            │
│  Confidence: 0.75 × min(conf_AB, conf_BC)                              │
│  Example:   Poodle IS_A Dog, Dog USES Paws → Poodle USES Paws          │
│                                                                         │
│  RULE: inherit_depends_through_is_a                                     │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[IS_A]--> B, B --[DEPENDS_ON]--> C                     │
│  Infers:    A --[DEPENDS_ON]--> C                                      │
│  Confidence: 0.80 × min(conf_AB, conf_BC)                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                       SYMMETRY RULES                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RULE: symmetric_similar                                                │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[SIMILAR_TO]--> B                                      │
│  Infers:    B --[SIMILAR_TO]--> A                                      │
│  Confidence: 1.0 × conf_AB                                             │
│  Example:   Cat SIMILAR_TO Dog → Dog SIMILAR_TO Cat                    │
│                                                                         │
│  RULE: symmetric_related                                                │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[RELATED_TO]--> B                                      │
│  Infers:    B --[RELATED_TO]--> A                                      │
│  Confidence: 1.0 × conf_AB                                             │
│                                                                         │
│  RULE: symmetric_opposite                                               │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[OPPOSITE_OF]--> B                                     │
│  Infers:    B --[OPPOSITE_OF]--> A                                     │
│  Confidence: 1.0 × conf_AB                                             │
│  Example:   Hot OPPOSITE_OF Cold → Cold OPPOSITE_OF Hot                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                       COMPOSITE RULES                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RULE: part_is_a_closure                                                │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[PART_OF]--> B, B --[IS_A]--> C                        │
│  Infers:    A --[PART_OF]--> C (indirect membership)                   │
│  Confidence: 0.70 × min(conf_AB, conf_BC)                              │
│  Example:   Wheel PART_OF Car, Car IS_A Vehicle                        │
│             → Wheel PART_OF Vehicle (loosely)                           │
│                                                                         │
│  RULE: cause_chain_contains                                             │
│  ────────────────────────────────────────────────────────────────────── │
│  Pattern:   A --[CAUSES]--> B, B --[CONTAINS]--> C                     │
│  Infers:    A --[CAUSES]--> C                                          │
│  Confidence: 0.65 × min(conf_AB, conf_BC)                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. InferenceEngine - Algorithm Details

### 3.1 Main Algorithm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   INFERENCE ENGINE ALGORITHM                                            │
│                                                                         │
│   Input:                                                                │
│     graph: GraphStore                                                   │
│     max_iterations: int (default 100)                                  │
│     min_confidence: float (default 0.3)                                │
│                                                                         │
│   Algorithm:                                                            │
│   ────────────────────────────────────────────────────────────────────  │
│   1. Initialize                                                         │
│      inferred = []                                                      │
│      iteration = 0                                                      │
│                                                                         │
│   2. While iteration < max_iterations:                                  │
│      a. new_facts = []                                                  │
│                                                                         │
│      b. For each rule in RuleBase:                                      │
│         i. Find matching edge patterns                                  │
│         ii. For each match:                                             │
│             - Compute new edge (source, target, relation)              │
│             - Compute confidence                                        │
│             - If conf >= min_confidence AND edge not exists:           │
│               new_facts.append(InferredFact(...))                      │
│                                                                         │
│      c. If no new_facts: break (fixpoint reached)                      │
│                                                                         │
│      d. Add new_facts to graph (optionally)                            │
│      e. inferred.extend(new_facts)                                     │
│      f. iteration += 1                                                  │
│                                                                         │
│   3. Return InferenceResult(inferred, iterations=iteration)            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Pattern Matching

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   TRANSITIVITY PATTERN MATCHING                                         │
│                                                                         │
│   For rule: A --[R]--> B --[R]--> C → A --[R]--> C                     │
│                                                                         │
│   1. Get all edges of type R                                            │
│      edges_R = graph.get_edges_by_type(R)                              │
│                                                                         │
│   2. Build edge index                                                   │
│      by_source = {}                                                     │
│      for edge in edges_R:                                               │
│          by_source[edge.source_id].append(edge)                        │
│                                                                         │
│   3. Find chains                                                        │
│      for edge_AB in edges_R:                                           │
│          B = edge_AB.target_id                                         │
│          for edge_BC in by_source.get(B, []):                          │
│              C = edge_BC.target_id                                     │
│              A = edge_AB.source_id                                     │
│              if A != C:  # Prevent self-loops                          │
│                  yield (A, C, conf_AB × conf_BC × rule_conf)           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Confidence Propagation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   CONFIDENCE PROPAGATION FORMULAS                                       │
│                                                                         │
│   TRANSITIVITY:                                                         │
│   conf_new = rule_conf × min(conf_edge1, conf_edge2)                   │
│                                                                         │
│   INVERSE:                                                              │
│   conf_new = 1.0 × conf_original (no loss)                             │
│                                                                         │
│   INHERITANCE:                                                          │
│   conf_new = rule_conf × min(conf_is_a, conf_property)                 │
│   (rule_conf typically 0.75-0.80 for inheritance)                      │
│                                                                         │
│   SYMMETRY:                                                             │
│   conf_new = 1.0 × conf_original (symmetric = equal)                   │
│                                                                         │
│   MULTI-HOP (distance > 2):                                            │
│   conf_new = base_conf × decay^(hops-1)                                │
│   (decay typically 0.9)                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. ContradictionDetector - Complete Specification

### 4.1 Contradiction Types

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   CONTRADICTION TYPES                                                   │
│                                                                         │
│   TYPE: DIRECT_CONFLICT                                                 │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: Two edges assert contradictory facts                      │
│   Example:    A IS_A B  AND  A IS_NOT B                                │
│   Detection:  Check for negative relations (if supported)              │
│                                                                         │
│   TYPE: CYCLIC_IS_A                                                     │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: A IS_A cycle exists                                       │
│   Example:    A IS_A B  AND  B IS_A A                                  │
│   Detection:  DFS cycle detection on IS_A edges                        │
│   Note:       IS_A should be acyclic (DAG)                             │
│                                                                         │
│   TYPE: CYCLIC_PART_OF                                                  │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: A PART_OF cycle exists                                    │
│   Example:    A PART_OF B  AND  B PART_OF A                            │
│   Detection:  DFS cycle detection on PART_OF edges                     │
│   Note:       Part-whole should be acyclic                             │
│                                                                         │
│   TYPE: OPPOSITE_AND_SIMILAR                                            │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: X is both similar to and opposite of Y                   │
│   Example:    A SIMILAR_TO B  AND  A OPPOSITE_OF B                     │
│   Detection:  Check for both relations between same nodes              │
│                                                                         │
│   TYPE: TEMPORAL_CYCLE                                                  │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: Circular temporal ordering                               │
│   Example:    A PRECEDES B  AND  B PRECEDES A                          │
│   Detection:  DFS cycle detection on PRECEDES/FOLLOWS                  │
│                                                                         │
│   TYPE: MULTIPLE_EXCLUSIVE                                              │
│   ────────────────────────────────────────────────────────────────────  │
│   Definition: X belongs to mutually exclusive categories               │
│   Example:    Animal IS_A Vertebrate AND Animal IS_A Invertebrate      │
│   Detection:  Check for IS_A to known exclusive types                  │
│   Note:       Requires ontology knowledge                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Detection Algorithm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   CONTRADICTION DETECTION ALGORITHM                                     │
│                                                                         │
│   def detect_all(graph):                                                │
│       contradictions = []                                               │
│                                                                         │
│       # 1. Check IS_A cycles                                            │
│       for node in graph.get_all_nodes():                               │
│           if has_cycle(node, RelationType.IS_A):                       │
│               contradictions.append(                                    │
│                   Contradiction(CYCLIC_IS_A, node, ...)                │
│               )                                                         │
│                                                                         │
│       # 2. Check PART_OF cycles                                         │
│       for node in graph.get_all_nodes():                               │
│           if has_cycle(node, RelationType.PART_OF):                    │
│               contradictions.append(                                    │
│                   Contradiction(CYCLIC_PART_OF, node, ...)             │
│               )                                                         │
│                                                                         │
│       # 3. Check opposite-and-similar                                   │
│       similar_edges = graph.get_edges_by_type(SIMILAR_TO)              │
│       opposite_edges = graph.get_edges_by_type(OPPOSITE_OF)            │
│                                                                         │
│       similar_pairs = {(e.source_id, e.target_id) for e in similar}    │
│       opposite_pairs = {(e.source_id, e.target_id) for e in opposite}  │
│                                                                         │
│       conflicts = similar_pairs & opposite_pairs                        │
│       for (a, b) in conflicts:                                          │
│           contradictions.append(                                        │
│               Contradiction(OPPOSITE_AND_SIMILAR, a, b)                │
│           )                                                             │
│                                                                         │
│       # 4. Check temporal cycles                                        │
│       # Similar to IS_A cycle detection                                 │
│                                                                         │
│       return ContradictionReport(contradictions)                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. SanTOKVerbalizer - Template System

### 5.1 Template Categories

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   TEMPLATE CATEGORIES                                                   │
│                                                                         │
│   DEFINITION (what_is):                                                 │
│   ├── "{subject} is {definition}."                                     │
│   ├── "Based on the knowledge base, {subject} can be described as..."  │
│   └── "{subject} refers to {definition}."                              │
│                                                                         │
│   RELATIONSHIP (how_related):                                           │
│   ├── "{subject} is {relation} {object}."                              │
│   ├── "The relationship between {subject} and {object} is: ..."       │
│   └── "{subject} and {object} are connected: {subject} {rel} {obj}."  │
│                                                                         │
│   PROCESS (how_works):                                                  │
│   ├── "{subject} works by {mechanism}."                                │
│   ├── "The process involves: {steps}."                                 │
│   └── "{subject} operates through {mechanism}."                        │
│                                                                         │
│   COMPARISON (difference):                                              │
│   ├── "The key difference: {subject} {diff1}, while {object} {diff2}.│
│   └── "{subject} differs from {object} in that {explanation}."        │
│                                                                         │
│   BOOLEAN (yes_no):                                                     │
│   ├── "Yes, {explanation}."                                            │
│   ├── "No, {explanation}."                                             │
│   └── "Based on the knowledge: {explanation}."                         │
│                                                                         │
│   LIST (list):                                                          │
│   ├── "The following are relevant: {items}."                           │
│   └── "Key items include: {items}."                                    │
│                                                                         │
│   UNKNOWN:                                                              │
│   ├── "The knowledge base does not contain sufficient info about..."  │
│   └── "Unable to find relevant information for: {query}."             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Relation Verbalization

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   RELATION → PHRASE MAPPING                                             │
│                                                                         │
│   ┌──────────────┬─────────────────────────────────────────────────┐   │
│   │ Relation     │ Natural Language Phrase                          │   │
│   ├──────────────┼─────────────────────────────────────────────────┤   │
│   │ IS_A         │ "is a type of"                                   │   │
│   │ PART_OF      │ "is part of"                                     │   │
│   │ HAS_PART     │ "contains"                                       │   │
│   │ CAUSES       │ "causes"                                         │   │
│   │ CAUSED_BY    │ "is caused by"                                   │   │
│   │ RELATED_TO   │ "is related to"                                  │   │
│   │ SIMILAR_TO   │ "is similar to"                                  │   │
│   │ OPPOSITE_OF  │ "is opposite to"                                 │   │
│   │ PRECEDES     │ "comes before"                                   │   │
│   │ FOLLOWS      │ "comes after"                                    │   │
│   │ DERIVED_FROM │ "is derived from"                                │   │
│   │ USES         │ "uses"                                           │   │
│   │ USED_BY      │ "is used by"                                     │   │
│   │ CONTAINS     │ "contains"                                       │   │
│   │ DEPENDS_ON   │ "depends on"                                     │   │
│   └──────────────┴─────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Query Classification

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   QUERY TYPE CLASSIFICATION RULES                                       │
│                                                                         │
│   def classify_query(query):                                            │
│       q = query.lower()                                                 │
│                                                                         │
│       # Definition questions                                            │
│       if q.startswith(("what is", "what are", "define")):              │
│           return "what_is"                                              │
│                                                                         │
│       # Process questions                                               │
│       if q.startswith(("how does", "how do", "how is")):               │
│           if "work" in q:                                               │
│               return "how_works"                                        │
│           return "explain"                                              │
│                                                                         │
│       # Boolean questions                                               │
│       if q.startswith(("is ", "are ", "does ", "do ", "can ")):        │
│           return "yes_no"                                               │
│                                                                         │
│       # Comparison questions                                            │
│       if "difference" in q or "different" in q:                        │
│           return "difference"                                           │
│                                                                         │
│       # Relation questions                                              │
│       if "relation" in q or "related" in q or "between" in q:          │
│           return "how_related"                                          │
│                                                                         │
│       # List questions                                                  │
│       if q.startswith(("list", "what are the", "name")):               │
│           return "list"                                                 │
│                                                                         │
│       # Default                                                         │
│       return "explain"                                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. SanTOKReasoner - Complete Pipeline

### 6.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   SANTOK REASONER PIPELINE                                              │
│                                                                         │
│   ┌─────────────┐                                                      │
│   │   Query     │  "What is machine learning?"                         │
│   └──────┬──────┘                                                      │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ STEP 1: SEARCH                                                   │  │
│   │ ─────────────────────────────────────────────────────────────── │  │
│   │ • Query UnifiedMemory for relevant facts                        │  │
│   │ • Match query tokens against stored content                     │  │
│   │ • Return top-k results by relevance                             │  │
│   └──────────────────────────────────────┬──────────────────────────┘  │
│                                          │                              │
│          ┌───────────────────────────────┘                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ STEP 2: INFERENCE                                                │  │
│   │ ─────────────────────────────────────────────────────────────── │  │
│   │ • Run InferenceEngine on graph                                  │  │
│   │ • Apply transitivity, inverse, inheritance rules                │  │
│   │ • Generate new facts with confidence scores                     │  │
│   └──────────────────────────────────────┬──────────────────────────┘  │
│                                          │                              │
│          ┌───────────────────────────────┘                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ STEP 3: PATH FINDING                                             │  │
│   │ ─────────────────────────────────────────────────────────────── │  │
│   │ • Find reasoning paths between relevant nodes                   │  │
│   │ • Score paths by relation strength                              │  │
│   │ • Select best explanatory paths                                 │  │
│   └──────────────────────────────────────┬──────────────────────────┘  │
│                                          │                              │
│          ┌───────────────────────────────┘                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ STEP 4: CONTRADICTION CHECK                                      │  │
│   │ ─────────────────────────────────────────────────────────────── │  │
│   │ • Run ContradictionDetector                                     │  │
│   │ • Flag any logical conflicts                                    │  │
│   │ • Reduce confidence if contradictions found                     │  │
│   └──────────────────────────────────────┬──────────────────────────┘  │
│                                          │                              │
│          ┌───────────────────────────────┘                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ STEP 5: VERBALIZATION                                            │  │
│   │ ─────────────────────────────────────────────────────────────── │  │
│   │ • Classify query type                                           │  │
│   │ • Select appropriate template                                   │  │
│   │ • Fill template with extracted facts                            │  │
│   │ • Polish output text                                            │  │
│   └──────────────────────────────────────┬──────────────────────────┘  │
│                                          │                              │
│          ┌───────────────────────────────┘                              │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────┐                                                      │
│   │  Answer     │  SanTOKAnswer with explanation                       │
│   └─────────────┘                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Output Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   SANTOK ANSWER STRUCTURE                                               │
│                                                                         │
│   SanTOKAnswer:                                                         │
│   ├── text: str                    # Generated answer                   │
│   ├── confidence: float            # 0.0 - 1.0                          │
│   │                                                                     │
│   ├── facts_used: List[str]        # Evidence from knowledge base       │
│   ├── inferences_made: List[str]   # Derived facts                      │
│   ├── rules_applied: List[str]     # Which rules fired                  │
│   ├── reasoning_path: List[str]    # Path through graph                 │
│   │                                                                     │
│   ├── query: str                   # Original question                  │
│   ├── processing_time: float       # Seconds                            │
│   └── contradictions_found: int    # Number of conflicts                │
│                                                                         │
│   Methods:                                                              │
│   ├── explain() → str              # Human-readable explanation         │
│   └── to_dict() → Dict             # JSON-serializable                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

This completes the deep technical specification for the Reasoning module.

