# SanTOK Cognitive

**A deterministic reasoning substrate for LLM-based systems.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)]()

---

## What is this?

SanTOK Cognitive is a **cognitive substrate** that sits between your knowledge and your LLM. It provides:

- **Structured knowledge** (graphs + trees, not just documents)
- **Symbolic reasoning** (20+ inference rules, not statistical patterns)
- **Constraint enforcement** (LLMs can only use verified facts)
- **Full explainability** (every answer has a reasoning trace)

**The key insight:** LLMs are great at *talking*, but unreliable at *thinking*. SanTOK Cognitive does the thinking. The LLM just verbalizes.

```
Query → SanTOK Cognitive → Structured Context + Constraints → LLM → Grounded Answer
              ↓                        ↓                           ↓
         Knowledge Graph          Reasoning Path              Cannot hallucinate
         Inference Rules          Hard constraints            Full audit trail
```

---

## Why does this exist?

| Problem | How SanTOK Solves It |
|---------|---------------------|
| LLMs hallucinate | Constrain output to verified facts |
| LLMs can't explain | Provide full reasoning traces |
| LLMs are non-deterministic | Symbolic reasoning is deterministic |
| RAG has no reasoning | 20+ inference rules (transitivity, inheritance, etc.) |
| Can't audit AI decisions | Every output traceable to source facts |

---

## Quick Start

```bash
# Clone
git clone https://github.com/[username]/santok-cognitive.git
cd santok-cognitive

# No dependencies to install! Just Python 3.8+

# Run the demo
python -m santok_cognitive.showcase
```

### Basic Usage

```python
from santok_cognitive import UnifiedMemory, SanTOKReasoner, RelationType

# Create memory
memory = UnifiedMemory()

# Add knowledge
memory.add("Python is a programming language", "fact", auto_link_graph=True)
memory.add("Programming languages are used for software development", "fact", auto_link_graph=True)

# Create reasoner
reasoner = SanTOKReasoner(memory)

# Ask a question
answer = reasoner.ask("What is Python?")

print(answer.text)
# "Python is a type of programming language."

print(answer.explain())
# Query: What is Python?
# Answer: Python is a type of programming language.
# Confidence: 85%
# 
# Reasoning Process:
#   Facts used (2):
#     - Python is a programming language
#     - Programming languages are used for software...
#   Rules applied: transitive_is_a
#   Path: Python → programming language
```

---

## Features

### 🔷 Knowledge Graph
- 15 relation types (IS_A, PART_OF, CAUSES, USES, etc.)
- O(1) node/edge operations
- Full serialization (JSON/Pickle)

### 🌲 Knowledge Trees
- Hierarchical organization
- Concept taxonomies
- Document structures
- BFS/DFS traversal

### 🧠 Symbolic Reasoning
- 20+ inference rules
- Transitivity, inverse, inheritance, symmetry
- Confidence propagation
- Contradiction detection

### 🎯 Custom Algorithms
- **SanTOKRanker**: Hybrid relevance scoring
- **SanTOK9Scorer**: 9-centric confidence math
- **SanTOKSimilarity**: Semantic similarity without neural networks
- **SanTOKGraphWalker**: Energy-based graph traversal

### ✅ Formal Guarantees
- 32 specified invariants
- Inference termination proof
- Bounded confidence [0,1]
- Acyclic taxonomies

---

## Architecture

```
santok_cognitive/
├── graph/              # Knowledge graph (nodes, edges, relations)
├── trees/              # Hierarchical trees
├── memory/             # Unified memory system
├── reasoning/          # Inference engine, rules, explanations
├── algorithms/         # Custom SanTOK algorithms
├── integration/        # Bridges to external systems
└── utils/              # Utilities
```

**No external dependencies.** Pure Python standard library.

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete system architecture |
| [WHITEPAPER.md](WHITEPAPER.md) | Technical overview |
| [docs/INVARIANTS.md](docs/INVARIANTS.md) | 32 formal guarantees |
| [docs/ALGORITHMS_DEEP.md](docs/ALGORITHMS_DEEP.md) | Algorithm specifications |
| [docs/REASONING_DEEP.md](docs/REASONING_DEEP.md) | All 20+ inference rules |

---

## Use Cases

### Regulated Industries
- **Healthcare**: Explainable medical AI
- **Finance**: Auditable decision systems
- **Legal**: Traceable legal reasoning

### Enterprise Knowledge
- Internal knowledge bases with guarantees
- Customer support with full audit trails
- Compliance systems

### AI Safety
- Constraint layer for LLMs
- Hallucination prevention
- Output validation

---

## Comparison

| Feature | RAG | Knowledge Graphs | SanTOK Cognitive |
|---------|-----|------------------|------------------|
| Structured knowledge | ❌ | ✅ | ✅ |
| Inference rules | ❌ | ❌ | ✅ (20+) |
| Constraint enforcement | ❌ | ❌ | ✅ |
| Natural language output | ✅ | ❌ | ✅ |
| Explainability | ❌ | Partial | ✅ Full |
| No hallucination | ❌ | ✅ | ✅ |

---

## Philosophy

> **"The most powerful AI of 2026 won't be just a bigger LLM; it will be an LLM that uses a system like SanTOK Cognitive as its Source of Truth."**

SanTOK Cognitive is **System 2** for AI:
- LLMs = System 1 (fast, intuitive, error-prone)
- SanTOK = System 2 (slow, deliberate, correct)

We don't compete with LLMs. We **complete** them.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

We welcome:
- Bug reports
- Documentation improvements
- New inference rules
- Domain-specific extensions
- Performance optimizations

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Citation

If you use SanTOK Cognitive in research:

```bibtex
@software{santok_cognitive,
  author = {Chavala, Santosh},
  title = {SanTOK Cognitive: A Deterministic Reasoning Substrate for LLM-Based Systems},
  year = {2024},
  url = {https://github.com/[username]/santok-cognitive}
}
```

---

## Links

- [Documentation](docs/)
- [Architecture](ARCHITECTURE.md)
- [Whitepaper](WHITEPAPER.md)
- [Research Abstract](RESEARCH_ABSTRACT.md)

---

**Built with no external dependencies. Runs anywhere Python runs.**

