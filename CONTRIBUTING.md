# Contributing to SanTOK Cognitive

Thank you for your interest in contributing to SanTOK Cognitive!

## Philosophy

Before contributing, please understand our core principles:

1. **No external AI dependencies** - We don't use GPT, transformers, or neural networks in the core system
2. **Explainability first** - Every feature must be traceable and auditable
3. **Formal correctness** - New features should maintain our 32 invariants
4. **Standard library only** - No pip dependencies for core functionality

---

## Ways to Contribute

### 🐛 Bug Reports

Found a bug? Please open an issue with:
- Python version
- Minimal reproduction code
- Expected vs actual behavior
- Error traceback (if any)

### 📚 Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify explanations
- Add examples
- Improve diagrams

### 🧪 Tests

Help us improve test coverage:
- Unit tests for existing code
- Edge case tests
- Integration tests
- Performance benchmarks

### ✨ New Features

We welcome new features that align with our philosophy:

#### Good contributions:
- New inference rules (with formal specification)
- New relation types (with clear semantics)
- Performance optimizations
- Domain-specific extensions
- Better verbalization templates

#### Not accepted:
- Neural network integrations in core
- External API dependencies
- Features that break determinism
- Changes that violate invariants

---

## Development Setup

```bash
# Clone the repo
git clone https://github.com/[username]/santok-cognitive.git
cd santok-cognitive

# No dependencies needed! Just Python 3.8+

# Run tests
python -m pytest tests/

# Run demos
python -m santok_cognitive.showcase
python -m santok_cognitive.demo_pure
python -m santok_cognitive.demo_algorithms
```

---

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small

### Example:
```python
def add_inference_rule(
    self,
    rule_id: str,
    pattern: List[RelationType],
    output: RelationType,
    confidence_factor: float = 0.9
) -> None:
    """
    Add a new inference rule to the rule base.

    Args:
        rule_id: Unique identifier for the rule
        pattern: List of relation types that trigger this rule
        output: Relation type to infer
        confidence_factor: Multiplier for confidence propagation

    Raises:
        ValueError: If rule_id already exists
    """
    ...
```

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** (`git checkout -b feature/your-feature`)
3. **Make changes** following our code style
4. **Test** your changes thoroughly
5. **Update documentation** if needed
6. **Submit PR** with clear description

### PR Checklist:
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] No new dependencies added
- [ ] Invariants still hold

---

## Adding New Inference Rules

To add a new inference rule:

1. **Specify formally** in `docs/REASONING_DEEP.md`:
   ```
   RULE: your_rule_name
   Pattern: A --[REL1]--> B --[REL2]--> C
   Infers: A --[REL3]--> C
   Confidence: 0.X × min(conf_AB, conf_BC)
   ```

2. **Implement** in `reasoning/rule_base.py`:
   ```python
   def _apply_your_rule(self, edge1, edge2):
       # Implementation
   ```

3. **Test** with examples:
   ```python
   def test_your_rule():
       # Add nodes and edges
       # Run inference
       # Assert expected results
   ```

4. **Document** the rule's semantics and use cases

---

## Adding New Relation Types

To add a new relation type:

1. **Add to enum** in `graph/graph_edge.py`:
   ```python
   class RelationType(Enum):
       YOUR_RELATION = "your_relation"
   ```

2. **Document semantics** in `docs/GRAPH_DEEP.md`:
   - Meaning
   - Example
   - Inverse (if any)
   - Transitivity (yes/no)

3. **Add patterns** in `algorithms/pattern_matcher.py` (if extractable from text)

4. **Update verbalization** in `reasoning/santok_verbalizer.py`:
   ```python
   RELATION_PHRASES = {
       RelationType.YOUR_RELATION: "is your-relation to",
   }
   ```

---

## Questions?

- Open an issue for questions
- Tag with `question` label
- Be specific about what you're trying to achieve

---

## Code of Conduct

- Be respectful
- Be constructive
- Focus on the work, not the person
- Assume good intentions

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make SanTOK Cognitive better! 🙏

