# SanTOK Cognitive Documentation

## Overview

This directory contains deep technical documentation for SanTOK Cognitive.

---

## Complete Document Index

### Core Documents

| Document | Lines | Description |
|----------|-------|-------------|
| `../ARCHITECTURE.md` | ~1200 | Complete system architecture |
| `../WHITEPAPER.md` | ~500 | Academic paper / RFC |

### Deep Technical Specifications

| Document | Lines | Description |
|----------|-------|-------------|
| `GRAPH_DEEP.md` | ~520 | Graph module internals |
| `TREES_DEEP.md` | ~600 | Trees module internals |
| `ALGORITHMS_DEEP.md` | ~710 | All algorithm formulas |
| `REASONING_DEEP.md` | ~670 | 20+ inference rules |

### Formal & Planning Documents

| Document | Lines | Description |
|----------|-------|-------------|
| `INVARIANTS.md` | ~450 | 32 formal guarantees |
| `ROADMAP_V2.md` | ~500 | v2 future features |

---

## Quick Navigation

### 📐 Architecture Overview (`../ARCHITECTURE.md`)
- System components diagram
- Module dependencies
- Data flow diagrams
- Mathematical foundations
- 11 major sections

### 📄 Whitepaper (`../WHITEPAPER.md`)
- Problem statement
- Design philosophy
- Architecture overview
- Comparison with LLMs
- Formal properties

### 🔷 Graph Module (`GRAPH_DEEP.md`)
- GraphNode structure (100 bytes)
- GraphEdge structure (150 bytes)
- RelationType enum (15+ types)
- GraphStore internals (O(1) ops)
- Serialization formats

### 🌲 Trees Module (`TREES_DEEP.md`)
- TreeNode structure
- 4 tree types (Concept, Document, Reasoning, Version)
- Traversal algorithms (DFS, BFS)
- Path operations
- Tree metrics

### 🧮 Algorithms (`ALGORITHMS_DEEP.md`)
- SanTOKRanker: `score = α·R + β·C + γ·H + δ·F`
- SanTOK9Scorer: Digital root math
- SanTOKSimilarity: 4-component formula
- SanTOKGraphWalker: Energy-based traversal
- SanTOKPatternMatcher: 34 patterns

### 🧠 Reasoning (`REASONING_DEEP.md`)
- 20+ inference rules (transitivity, inverse, etc.)
- InferenceEngine algorithm
- Contradiction detection (5 types)
- SanTOKVerbalizer templates
- Complete pipeline diagram

### ✅ Invariants (`INVARIANTS.md`)
- 32 formal invariants
- Graph invariants (G1-G8)
- Tree invariants (T1-T5)
- Memory invariants (M1-M2)
- Inference invariants (I1-I4)
- Algorithm invariants (A1-A9)
- System guarantees (S1-S4)

### 🚀 Roadmap v2 (`ROADMAP_V2.md`)
- Phase 1: Belief Revision
- Phase 2: Incremental Learning
- Phase 3: Advanced Contradictions
- Phase 4: Enhanced Verbalization
- Phase 5: Performance Optimization

---

## Running Demos

```bash
# Complete showcase
python -m santok_cognitive.showcase

# Pure SanTOK demo
python -m santok_cognitive.demo_pure

# Algorithms demo
python -m santok_cognitive.demo_algorithms
```

---

## Key Principles

1. **100% Unique** - No borrowed algorithms
2. **No Neural Networks** - Pure symbolic
3. **Explainable** - Every decision traceable
4. **Modular** - Components work independently
5. **Safe** - Never modifies `santok_complete`

---

## Document Statistics

| Metric | Count |
|--------|-------|
| Total documents | 8 |
| Total lines | ~5,000+ |
| Formal invariants | 32 |
| Inference rules | 20+ |
| Algorithm formulas | 15+ |
| ASCII diagrams | 50+ |

