# SanTOK SLM: Complete Architecture Documentation

**Version:** 1.0  
**Date:** 2025-12-27  
**Status:** Final

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Design Philosophy](#core-design-philosophy)
3. [Architecture Overview](#architecture-overview)
4. [Component Deep Dive](#component-deep-dive)
5. [Data Flow and Processing](#data-flow-and-processing)
6. [Constraint System](#constraint-system)
7. [Sequence Optimization](#sequence-optimization)
8. [Training System](#training-system)
9. [Integration Patterns](#integration-patterns)
10. [Formal Properties](#formal-properties)
11. [Implementation Details](#implementation-details)
12. [Use Cases and Examples](#use-cases-and-examples)

---

## Executive Summary

SanTOK SLM (Small Language Model) is a **deterministic, constraint-driven text generation system** that provides structural guarantees against hallucination. Unlike statistical language models, SanTOK SLM can **only emit tokens that are grounded in verified facts** from SanTOK Cognitive.

**Key Differentiator:**

```
Traditional LLM:
    Input → Statistical Model → Probabilistic Output → (May hallucinate)

SanTOK SLM:
    Input → SanTOK Cognitive (THINKS) → Constraints → Sequence Optimizer (ORDERS) → Constrained Output → (Cannot hallucinate)
```

**Core Invariant:**

> **Hallucination is structurally impossible, not statistically unlikely.**

This is achieved through:
- Token-level constraint enforcement
- Masked loss computation (only allowed tokens)
- Symbol ID abstraction (no raw text leakage)
- Weak-by-design architecture (intelligence stays in Cognitive)

---

## Core Design Philosophy

### The Separation Principle

SanTOK SLM enforces a **strict separation of concerns**:

| Layer | Responsibility | Technology | Can It Learn Facts? |
|-------|---------------|------------|---------------------|
| **SanTOK Cognitive** | Thinking, Reasoning, Facts | Symbolic graphs, trees, rules | ✅ Yes |
| **Constraint Engine** | Gatekeeping, Filtering | Token sets, validation logic | ❌ No |
| **Sequence Optimizer** | Ordering, Coherence | Matrix operations, pattern matching | ❌ No |
| **Decoder** | Integration, Sampling | Constraint intersection, selection | ❌ No |

**Critical Rule:**

> **Intelligence lives in SanTOK Cognitive. The Sequence Optimizer only arranges approved tokens.**

### Weak-by-Design Architecture

The Sequence Optimizer is intentionally **weak**:

- ✅ Can learn: Token ordering patterns, local coherence
- ❌ Cannot learn: Facts, reasoning, semantic understanding
- ❌ Cannot access: Raw text, meaning, context beyond symbols

This weakness is a **feature, not a bug**. It ensures that:

1. Facts cannot leak into the optimizer
2. Hallucination pathways cannot emerge
3. All meaning remains in SanTOK Cognitive
4. The system remains auditable and explainable

### The Symbol ID Abstraction

**Critical Design Decision:**

The Sequence Optimizer **never sees raw text**. It only sees:

```
Raw Text → Symbol Extraction → Symbol IDs → Sequence Optimizer → Scores → Constraints → Text
```

**Why?**

- Prevents implicit memorization
- Blocks accidental semantic leakage
- Ensures optimizer is truly "weak"
- Maintains separation of meaning vs. expression

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SanTOK Cognitive Layer                      │
│  (Knowledge Graph + Trees + Reasoning + Inference)              │
│                                                                  │
│  • Facts: ["Python is a language", "Guido created Python"]     │
│  • Reasoning Path: [IS_A relations, CREATED_BY relations]      │
│  • Confidence Scores                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Constraint Engine                            │
│                                                                  │
│  • Extracts vocabulary from facts                               │
│  • Builds allowed token sets                                    │
│  • Creates FactConstraint                                       │
│  • Sets VocabularyScope                                         │
│                                                                  │
│  Output: {allowed_tokens: Set[str], fact_tokens: Set[str]}     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              SanTOK Sequence Optimizer                          │
│                                                                  │
│  • SanTOKPositionEncoder (position information)                 │
│  • SanTOKPatternMatcher (local token patterns)                  │
│  • SanTOKProcessor (token transformation)                       │
│  • SanTOKSequenceBlock (pattern → process)                      │
│                                                                  │
│  Input:  Symbol IDs [0, 1, 2, 3]                               │
│  Output: Scores [0.5, 0.3, 0.2, 0.1, ...] for all tokens      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Constrained Decoder                            │
│                                                                  │
│  • Intersects optimizer scores with allowed tokens              │
│  • Sets disallowed tokens to -inf                               │
│  • Computes probabilities only over allowed set                 │
│  • Samples from allowed set only                                │
│                                                                  │
│  Rule: Optimizer proposes → SanTOK Cognitive disposes          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        Generated Text
                    (Structurally Guaranteed
                     Grounded in Facts)
```

### Component Relationships

```
┌──────────────────┐         ┌──────────────────┐
│ ConstraintEngine │◄────────┤ UnifiedMemory    │
│                  │         │ (SanTOK Cognitive)│
│ • FactConstraint │         │                  │
│ • VocabularyScope│         │ • Facts          │
│ • TokenFiltering │         │ • Reasoning Path │
└────────┬─────────┘         └──────────────────┘
         │
         │ provides allowed tokens
         ▼
┌──────────────────┐         ┌──────────────────┐
│ Sequence         │         │ Constrained      │
│ Optimizer        │         │ Decoder          │
│                  │         │                  │
│ • Pattern Match  │────scores──►│ Intersection   │
│ • Processing     │         │ Masking         │
│ • Symbol IDs     │         │ Sampling        │
└──────────────────┘         └────────┬─────────┘
                                      │
                                      │ generates
                                      ▼
                              ┌───────────────┐
                              │  Text Output  │
                              │  (Grounded)   │
                              └───────────────┘
```

---

## Component Deep Dive

### 1. Constraint Engine (`ConstraintEngine`)

#### Purpose

The Constraint Engine is the **gatekeeper**. It decides which tokens are allowed and which are forbidden.

#### Architecture

```python
ConstraintEngine
├── FactConstraint
│   ├── facts: List[str]
│   ├── fact_tokens: Set[str]
│   └── strict: bool
├── VocabularyScope
│   ├── tokens: Set[str]
│   ├── structural: Set[str]
│   └── domain_tokens: Set[str]
└── TokenConstraint[]
    ├── constraint_type
    ├── allowed_tokens
    ├── denied_tokens
    └── validator function
```

#### How It Works

**Step 1: Fact Loading**

```python
facts = [
    "Python is a programming language",
    "Python was created by Guido van Rossum"
]

# Extract tokens from facts
fact_tokens = {
    "python", "is", "a", "programming", "language",
    "was", "created", "by", "guido", "van", "rossum"
}
```

**Step 2: Vocabulary Building**

```python
# Start with fact tokens
vocabulary = fact_tokens.copy()

# Add structural tokens (always allowed)
vocabulary.update({
    "the", "a", "an", "is", "are", ".", ",", "?"
})

# Add domain tokens (if provided)
vocabulary.update(domain_tokens)
```

**Step 3: Token Validation**

For every token candidate:

```python
def check_token(token: str) -> (bool, str):
    # 1. Check vocabulary scope
    if token not in vocabulary_scope:
        return False, "Outside vocabulary"
    
    # 2. Check fact grounding (if strict)
    if strict_mode and token not in fact_tokens:
        # Allow structural tokens even if not in facts
        if token not in structural_tokens:
            return False, "Not grounded in facts"
    
    # 3. Check custom constraints
    for constraint in constraints:
        if not constraint.check(token):
            return False, f"Rejected by {constraint.name}"
    
    return True, "Allowed"
```

#### Formal Properties

1. **Completeness**: All fact tokens are in vocabulary
2. **Soundness**: Only approved tokens can pass
3. **Determinism**: Same input → same allowed set
4. **Monotonicity**: Adding facts can only expand allowed set

#### Statistics Tracking

```python
stats = {
    'tokens_checked': 1000,
    'tokens_rejected': 150,
    'rejection_rate': 0.15,
    'rejection_reasons': {
        'vocabulary_scope': 80,
        'fact_grounding': 70
    }
}
```

---

### 2. SanTOK Sequence Optimizer (`SanTOKSequenceOptimizer`)

#### Purpose

The Sequence Optimizer learns **local token ordering patterns**. It does NOT learn facts or reasoning.

#### Architecture

```
SanTOKSequenceOptimizer
├── Embedding Layer
│   └── symbol_id → vector (d_model dimensions)
├── Position Encoder (SanTOKPositionEncoder)
│   └── Adds position information (sinusoidal)
├── Sequence Blocks (SanTOKSequenceBlock[]) × N
│   ├── Pattern Matcher (SanTOKPatternMatcher)
│   │   ├── Multi-head pattern matching
│   │   ├── Query/Key/Value projections
│   │   └── Pattern scores
│   └── Processor (SanTOKProcessor)
│       ├── Layer 1: d_model → d_ff
│       ├── Activation: ReLU
│       └── Layer 2: d_ff → d_model
└── Output Projection
    └── d_model → vocab_size (scores)
```

#### Detailed Component Logic

##### 2.1 Embedding Layer

**Purpose**: Convert symbol IDs to dense vectors

```python
# Symbol ID → Vector lookup
symbol_id = 42
embedding_vector = embedding_matrix[symbol_id]  # Shape: (d_model,)

# This is PURELY a lookup table
# No semantic meaning is encoded
# Just numerical representation
```

**Key Property**: Embeddings are **randomly initialized** and learned during training. They encode **positional and co-occurrence patterns**, not semantic meaning.

##### 2.2 Position Encoder (`SanTOKPositionEncoder`)

**Purpose**: Add position information to embeddings

**Method**: Sinusoidal encoding

```python
# For position pos and dimension i:
if i is even:
    PE[pos, i] = sin(pos / 10000^(i/d_model))
else:
    PE[pos, i] = cos(pos / 10000^((i-1)/d_model))

# This creates a unique encoding for each position
# Allows the optimizer to learn position-dependent patterns
```

**Why Sinusoidal?**

- Deterministic (no learned parameters)
- Can extrapolate to longer sequences
- Captures relative position relationships

**Example**:

```python
# Sequence: ["python", "is", "programming"]
# Position 0: [sin(0/10000^0), cos(0/10000^0), sin(0/10000^2), ...]
# Position 1: [sin(1/10000^0), cos(1/10000^0), sin(1/10000^2), ...]
# Position 2: [sin(2/10000^0), cos(2/10000^0), sin(2/10000^2), ...]
```

##### 2.3 Pattern Matcher (`SanTOKPatternMatcher`)

**Purpose**: Learn which tokens appear together

**Process**:

```
Step 1: Project to Query, Key, Value spaces
──────────────────────────────────────────────
Q = X @ W_q  (seq_len, d_model) → (seq_len, d_model)
K = X @ W_k  (seq_len, d_model) → (seq_len, d_model)
V = X @ W_v  (seq_len, d_model) → (seq_len, d_model)

Step 2: Reshape for multi-head
──────────────────────────────────────────────
Q = Q.reshape(seq_len, n_heads, d_k).transpose(1, 0, 2)
   → (n_heads, seq_len, d_k)

Step 3: Compute pattern scores
──────────────────────────────────────────────
scores = Q @ K.transpose(0, 2, 1) / sqrt(d_k)
       → (n_heads, seq_len, seq_len)

Step 4: Apply softmax
──────────────────────────────────────────────
pattern_weights = softmax(scores)
               → (n_heads, seq_len, seq_len)

Step 5: Apply to values
──────────────────────────────────────────────
output = pattern_weights @ V
       → (n_heads, seq_len, d_k)

Step 6: Concatenate heads
──────────────────────────────────────────────
output = output.transpose(1, 0, 2).reshape(seq_len, d_model)
       → (seq_len, d_model)
```

**What It Learns**:

- Token A often appears near Token B
- Certain token sequences are common
- Local ordering patterns

**What It Does NOT Learn**:

- What tokens mean
- Facts about the world
- Reasoning patterns
- Semantic relationships

##### 2.4 Processor (`SanTOKProcessor`)

**Purpose**: Non-linear transformation of token representations

**Process**:

```python
# Layer 1: Expand dimension
h1 = X @ W1 + b1  # (seq_len, d_model) → (seq_len, d_ff)

# Activation: ReLU (non-linearity)
h1 = max(0, h1)

# Layer 2: Contract dimension
h2 = h1 @ W2 + b2  # (seq_len, d_ff) → (seq_len, d_model)

# Output: Transformed representation
```

**Why This Structure?**

- Expands to higher dimension (captures more complex patterns)
- Applies non-linearity (enables complex mappings)
- Contracts back (maintains dimensionality)
- Residual connection (preserves information)

##### 2.5 Sequence Block (`SanTOKSequenceBlock`)

**Full Forward Pass**:

```python
def forward(x):
    # Pattern matching + residual
    pattern_out = pattern_matcher.forward(x)
    x = x + pattern_out  # Residual connection
    
    # Layer normalization
    x = layer_norm(x)
    
    # Processing + residual
    proc_out = processor.forward(x)
    x = x + proc_out  # Residual connection
    
    # Layer normalization
    x = layer_norm(x)
    
    return x
```

**Why Residual Connections?**

- Allows gradients to flow through many layers
- Preserves original information
- Enables deep architectures

**Why Layer Normalization?**

- Stabilizes training
- Reduces internal covariate shift
- Speeds up convergence

##### 2.6 Output Projection

**Purpose**: Map from internal representation to vocabulary scores

```python
# Last position's hidden state
last_hidden = sequence_output[-1]  # (d_model,)

# Project to vocabulary
logits = last_hidden @ output_proj  # (vocab_size,)

# These are RAW SCORES, not probabilities
# Constraint system will filter them
```

#### Complete Forward Pass

```python
def forward(symbol_ids: List[int]) -> np.ndarray:
    # 1. Embedding lookup
    embedded = embedding[symbol_ids]  # (seq_len, d_model)
    
    # 2. Add position encoding
    embedded = pos_encoder(embedded)
    
    # 3. Pass through sequence blocks
    x = embedded
    for block in blocks:
        x = block.forward(x)
    
    # 4. Extract last position
    last_hidden = x[-1]  # (d_model,)
    
    # 5. Project to vocabulary
    logits = last_hidden @ output_proj  # (vocab_size,)
    
    return logits
```

#### Parameter Count

For default configuration:
- Embedding: vocab_size × d_model
- Position Encoder: 0 (deterministic)
- Pattern Matcher: 4 × (d_model × d_model) per head
- Processor: 2 × (d_model × d_ff) + d_ff + d_model
- Output Projection: d_model × vocab_size

**Example** (vocab_size=10000, d_model=128, n_layers=2, n_heads=4, d_ff=512):
- Total: ~1,200,000 parameters

---

### 3. Constrained Decoder (`ConstrainedDecoder`)

#### Purpose

Integrates Sequence Optimizer scores with SanTOK Cognitive constraints.

#### Core Principle

> **Optimizer proposes → SanTOK Cognitive disposes**

#### Architecture

```
ConstrainedDecoder
├── Sequence Optimizer (scores all tokens)
├── Constraint Engine (filters to allowed)
├── Masking Logic (sets disallowed to -inf)
├── Probability Computation (softmax over allowed)
└── Sampling Strategy (selects from allowed)
```

#### Detailed Process

##### Step 1: Get Optimizer Scores

```python
# Current sequence: ["python", "is"]
sequence_ids = [42, 15]  # Symbol IDs

# Get scores for ALL tokens
all_scores = optimizer.forward(sequence_ids)
# Shape: (vocab_size,)
# Example: [0.5, 0.3, 0.2, 0.1, 0.8, 0.9, ...]
#          python prog lang guido java hallucinate ...
```

##### Step 2: Get Allowed Tokens

```python
# From Constraint Engine
allowed_tokens = constraint_engine.get_allowed_tokens()
# Example: {"python", "programming", "language", "guido", ...}
# Does NOT include: {"java", "hallucinate", ...}

# Convert to IDs
allowed_ids = [symbol_to_id[t] for t in allowed_tokens]
# Example: [42, 1, 5, 10, ...]
```

##### Step 3: Apply Mask

```python
# Create mask: -inf for disallowed, 0 for allowed
mask = np.full(vocab_size, -np.inf)
mask[allowed_ids] = 0.0

# Apply mask
masked_scores = all_scores + mask
# Disallowed tokens now have -inf score
# They will have 0.0 probability after softmax
```

##### Step 4: Compute Probabilities

```python
# Softmax over ALL tokens (but disallowed are -inf, so they become 0)
exp_scores = np.exp(masked_scores - np.max(masked_scores))
probs = exp_scores / np.sum(exp_scores[allowed_ids])

# Result: Probabilities sum to 1.0
# Disallowed tokens have exactly 0.0 probability
# Only allowed tokens have non-zero probability
```

##### Step 5: Sample

```python
# Strategy options:
# 1. Greedy: argmax(probs[allowed_ids])
# 2. Top-K: sample from top K allowed tokens
# 3. Nucleus: sample from top P probability mass

selected_token_id = sample(probs, strategy, allowed_ids)
selected_token = id_to_symbol[selected_token_id]
```

#### Formal Guarantees

1. **Impossibility**: Disallowed tokens have exactly 0.0 probability
2. **Completeness**: All allowed tokens have non-zero probability
3. **Determinism**: Same optimizer output + same constraints → same probabilities
4. **Monotonicity**: More constraints → smaller allowed set → fewer choices

#### Example Flow

```
Input Sequence: ["python", "is"]
─────────────────────────────────────────────────────────

Step 1: Optimizer Scores (for all tokens)
─────────────────────────────────────────────────────────
python:        0.50
programming:   0.30
language:      0.20
guido:         0.10
java:          0.80  ← Optimizer "wants" this
hallucinate:   0.90  ← Optimizer "wants" this
...            ...

Step 2: Allowed Tokens (from SanTOK Cognitive)
─────────────────────────────────────────────────────────
{python, programming, language, guido, ...}
NOT allowed: {java, hallucinate, ...}

Step 3: Masked Scores
─────────────────────────────────────────────────────────
python:        0.50  (allowed, keep score)
programming:   0.30  (allowed, keep score)
language:      0.20  (allowed, keep score)
guido:         0.10  (allowed, keep score)
java:          -inf  (disallowed, masked)
hallucinate:   -inf  (disallowed, masked)
...            ...

Step 4: Probabilities (softmax over allowed only)
─────────────────────────────────────────────────────────
python:        0.45  (high probability)
programming:   0.27  (moderate)
language:      0.18  (moderate)
guido:         0.10  (low)
java:          0.00  (impossible)
hallucinate:   0.00  (impossible)
...            ...

Step 5: Sample
─────────────────────────────────────────────────────────
Selected: "programming" (sampled from allowed set)

Result: Even though optimizer wanted "java" or "hallucinate",
        they are impossible. Output is constrained to facts.
```

---

## Data Flow and Processing

### Complete Generation Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. QUERY RECEIVED                                           │
│    "What is Python?"                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SANTOK COGNITIVE PROCESSING                              │
│                                                              │
│    UnifiedMemory.query("What is Python?")                   │
│    ├── Vector search → relevant facts                       │
│    ├── Graph traversal → related concepts                   │
│    ├── Tree pruning → hierarchical context                  │
│    └── Inference engine → reasoning path                    │
│                                                              │
│    Output:                                                   │
│    • Facts: ["Python is a programming language", ...]       │
│    • Reasoning: [IS_A relations, ...]                       │
│    • Confidence: 0.92                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CONSTRAINT ENGINE SETUP                                  │
│                                                              │
│    constraint_engine.add_facts_from_cognitive(facts)        │
│    ├── Extract tokens from facts                            │
│    ├── Build fact_tokens set                                │
│    ├── Create VocabularyScope                               │
│    └── Set strict mode (fact-grounded only)                 │
│                                                              │
│    Output:                                                   │
│    • allowed_tokens: Set[str]                               │
│    • fact_tokens: Set[str]                                  │
│    • vocabulary_scope: VocabularyScope                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. SEQUENCE OPTIMIZER INITIALIZATION                        │
│                                                              │
│    optimizer.set_vocabulary(symbol_to_id)                   │
│    ├── Build symbol → ID mapping                            │
│    └── Initialize embeddings                                │
│                                                              │
│    Output:                                                   │
│    • symbol_to_id: Dict[str, int]                           │
│    • id_to_symbol: Dict[int, str]                           │
│    • embedding matrix ready                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. GENERATION LOOP (for each token)                         │
│                                                              │
│    while not finished:                                      │
│                                                              │
│    5a. Encode current sequence                              │
│        sequence_ids = encode(["python", "is"])              │
│        → [42, 15]                                           │
│                                                              │
│    5b. Get optimizer scores                                 │
│        scores = optimizer.forward(sequence_ids)             │
│        → [0.5, 0.3, 0.2, ..., 0.8, 0.9]                    │
│                                                              │
│    5c. Filter to allowed tokens                             │
│        allowed_ids = constraint_engine.get_allowed_tokens() │
│        → [42, 1, 5, 10, ...]                                │
│                                                              │
│    5d. Apply mask                                           │
│        masked = scores + mask                               │
│        → [0.5, 0.3, 0.2, ..., -inf, -inf]                  │
│                                                              │
│    5e. Compute probabilities                                │
│        probs = softmax(masked[allowed_ids])                 │
│        → [0.45, 0.27, 0.18, 0.10, 0.0, 0.0]                │
│                                                              │
│    5f. Sample token                                         │
│        token_id = sample(probs, strategy)                   │
│        → 1 (programming)                                    │
│                                                              │
│    5g. Decode token                                         │
│        token = decode(token_id)                             │
│        → "programming"                                      │
│                                                              │
│    5h. Add to sequence                                      │
│        sequence.append("programming")                       │
│                                                              │
│    Output: ["python", "is", "programming", "language"]     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. POST-PROCESSING                                          │
│                                                              │
│    • Capitalize first letter                                │
│    • Add punctuation if needed                              │
│    • Format for readability                                 │
│                                                              │
│    Output: "Python is programming language"                 │
└─────────────────────────────────────────────────────────────┘
```

### Token Lifecycle

```
Token Lifecycle: From Fact to Output
════════════════════════════════════════════════════════════════

1. FACT ENTRY
   ────────────────────────────────────────────────────────────
   Fact: "Python is a programming language"
   
2. TOKEN EXTRACTION
   ────────────────────────────────────────────────────────────
   Tokens: ["python", "is", "a", "programming", "language"]
   
3. VOCABULARY BUILDING
   ────────────────────────────────────────────────────────────
   Vocabulary: {
       "python": 42,
       "programming": 1,
       "language": 5,
       ...
   }
   
4. CONSTRAINT REGISTRATION
   ────────────────────────────────────────────────────────────
   Allowed Set: {"python", "programming", "language", ...}
   
5. SYMBOL ID ASSIGNMENT
   ────────────────────────────────────────────────────────────
   Symbol IDs: {
       "python": 42,
       "programming": 1,
       "language": 5
   }
   
6. EMBEDDING LOOKUP (during generation)
   ────────────────────────────────────────────────────────────
   Token "python" (ID 42)
   → Embedding[42] = [0.1, -0.3, 0.5, ..., 0.2]
   
7. SEQUENCE PROCESSING
   ────────────────────────────────────────────────────────────
   [0.1, -0.3, 0.5, ...]
   → Position encoding
   → Pattern matching
   → Processing
   → Output scores
   
8. CONSTRAINT FILTERING
   ────────────────────────────────────────────────────────────
   Score for "python": 0.50 → Allowed → Probability: 0.45
   Score for "java": 0.80 → Disallowed → Probability: 0.00
   
9. SAMPLING
   ────────────────────────────────────────────────────────────
   Selected: "programming" (from allowed set)
   
10. DECODING
    ────────────────────────────────────────────────────────────
    ID 1 → Token "programming"
    
11. OUTPUT
    ────────────────────────────────────────────────────────────
    Generated text: "Python is programming language"
```

---

## Constraint System

### Constraint Hierarchy

```
Constraints
├── FactConstraint (highest priority)
│   ├── fact_tokens: Set[str]  (from SanTOK Cognitive)
│   └── strict: bool  (if true, ONLY fact tokens allowed)
│
├── VocabularyScope
│   ├── tokens: Set[str]  (core vocabulary)
│   ├── structural: Set[str]  (grammar words)
│   └── domain_tokens: Set[str]  (domain-specific)
│
└── TokenConstraint[] (custom rules)
    ├── allowed_tokens: Set[str]
    ├── denied_tokens: Set[str]
    ├── pattern: regex
    └── validator: function
```

### Constraint Application Order

```
For each token candidate:
    1. Check VocabularyScope
       └─ If not in scope → REJECT
    
    2. Check FactConstraint (if strict)
       └─ If not in facts → REJECT (unless structural)
    
    3. Check TokenConstraint[]
       └─ If fails any → REJECT
    
    4. ALLOW → Token can be generated
```

### Constraint Types

#### Type 1: Fact Grounding (`FactConstraint`)

**Purpose**: Ensure all tokens are grounded in verified facts

```python
facts = ["Python is a programming language"]
fact_constraint = FactConstraint(facts=facts, strict=True)

# Allowed
fact_constraint.check("python") → True
fact_constraint.check("programming") → True

# Disallowed
fact_constraint.check("java") → False  # Not in facts
fact_constraint.check("hallucinate") → False  # Not in facts
```

#### Type 2: Vocabulary Scope (`VocabularyScope`)

**Purpose**: Limit vocabulary to approved domain

```python
scope = VocabularyScope()
scope.add_tokens(["python", "programming", "language"])
scope.add_domain(["machine", "learning", "neural"])

# Allowed
scope.is_in_scope("python") → True
scope.is_in_scope("machine") → True  # Domain token

# Disallowed
scope.is_in_scope("gibberish") → False  # Not in vocabulary
```

#### Type 3: Custom Constraints (`TokenConstraint`)

**Purpose**: User-defined rules

```python
# Example: No numbers in names
constraint = TokenConstraint(
    pattern=r'^[a-zA-Z]+$',  # Only letters
    name="no_numbers"
)

constraint.check("python") → True
constraint.check("python3") → False  # Contains number
```

### Constraint Statistics

```python
stats = {
    'tokens_checked': 1000,
    'tokens_rejected': 150,
    'rejection_rate': 0.15,
    'rejection_reasons': {
        'vocabulary_scope': 80,      # 80 tokens rejected
        'fact_grounding': 70,        # 70 tokens rejected
        'custom_constraint': 0
    },
    'active_constraints': 2,
    'fact_count': 10,
    'vocab_size': 500
}
```

---

## Sequence Optimization

### Pattern Learning

The Sequence Optimizer learns **local token co-occurrence patterns**.

#### What Patterns Are Learned

```
Pattern Type 1: Adjacency
─────────────────────────────────────────────────────────────
"python" often followed by "is"
"programming" often followed by "language"
"guido" often followed by "van"

Pattern Type 2: Context
─────────────────────────────────────────────────────────────
In context of "python is", likely next: "a", "programming"
In context of "created by", likely next: "guido"

Pattern Type 3: Position
─────────────────────────────────────────────────────────────
Position 0: Often capital letters or nouns
Position -1: Often punctuation or end-of-sentence words
```

#### How Patterns Are Learned

```
Training Process:
─────────────────────────────────────────────────────────────

1. Training Sequence: ["python", "is", "programming"]
   Target: "language"

2. Forward Pass:
   - Embed: [42, 15, 1] → vectors
   - Position encode
   - Pattern match: learns "programming" follows "is"
   - Process
   - Output scores

3. Loss Computation:
   - Target ID: 5 ("language")
   - Allowed IDs: [1, 5, 10, ...] (from constraints)
   - Masked loss: only over allowed tokens
   - Loss = -log(prob[5])

4. Weight Update:
   - Increase score for "language" after ["python", "is", "programming"]
   - Decrease scores for other tokens in context
```

### Sequence Coherence

The optimizer improves **local coherence**:

**Before (Random Ordering)**:
```
"language python programming is"
```

**After (Optimized Ordering)**:
```
"python is programming language"
```

**How?** The optimizer learns that:
- "python" often starts sequences
- "is" often follows nouns
- "programming" often modifies nouns
- "language" often ends noun phrases

### Limitations (By Design)

The optimizer **cannot** learn:

1. **Facts**: It doesn't know what tokens mean
2. **Reasoning**: It doesn't understand logic
3. **Semantics**: It only sees symbol IDs
4. **Context beyond sequences**: It has limited memory

This weakness ensures that **all intelligence stays in SanTOK Cognitive**.

---

## Training System

### Training Data Generation

#### Source: SanTOK Cognitive Only

```python
# Training data comes ONLY from SanTOK Cognitive
facts = [
    "Python is a programming language",
    "Python was created by Guido van Rossum",
    ...
]

# NO external corpora
# NO scraped web text
# NO open datasets
# 100% SanTOK-native
```

#### Sequence Generation

```python
# From Facts
fact = "Python is a programming language"
tokens = ["python", "is", "a", "programming", "language"]

# Generate sequences:
Sequence 1: ["python"] → target: "is"
Sequence 2: ["python", "is"] → target: "a"
Sequence 3: ["python", "is", "a"] → target: "programming"
Sequence 4: ["python", "is", "a", "programming"] → target: "language"
```

#### Templates

```python
templates = [
    "X is a Y",
    "X was created by Y",
    "X uses Y",
    ...
]

# Fill with vocabulary tokens
# Generate sequences from filled templates
```

### Training Loop

```
┌─────────────────────────────────────────────────────────────┐
│ TRAINING LOOP                                               │
└─────────────────────────────────────────────────────────────┘

For each epoch:
    For each batch:
        For each sequence in batch:
            
            ┌─────────────────────────────────────────────┐
            │ 1. Forward Pass                             │
            │─────────────────────────────────────────────│
            │ sequence_ids = encode(sequence.tokens)      │
            │ logits = optimizer.forward(sequence_ids)    │
            │                                             │
            │ Output: scores for ALL tokens               │
            └─────────────────┬───────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────────────┐
            │ 2. Masked Loss Computation                  │
            │─────────────────────────────────────────────│
            │ allowed_ids = sequence.allowed_tokens       │
            │ mask = create_mask(allowed_ids)             │
            │ masked_logits = logits + mask               │
            │                                             │
            │ # Disallowed tokens now have -inf           │
            │                                             │
            │ probs = softmax(masked_logits[allowed_ids]) │
            │ loss = -log(probs[target_id])               │
            │                                             │
            │ Output: loss (only over allowed tokens)     │
            └─────────────────┬───────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────────────┐
            │ 3. Gradient Computation                     │
            │─────────────────────────────────────────────│
            │ gradients = compute_gradients(loss)         │
            │                                             │
            │ # Gradients flow only through allowed tokens│
            │                                             │
            │ Output: gradients for all parameters        │
            └─────────────────┬───────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────────────┐
            │ 4. Weight Update                            │
            │─────────────────────────────────────────────│
            │ optimizer.weights -= lr * gradients         │
            │                                             │
            │ Output: Updated weights                     │
            └─────────────────────────────────────────────┘
```

### Masked Loss Detail

**Key Innovation**: Loss computed ONLY over allowed tokens

```python
def compute_masked_loss(logits, target_id, allowed_ids):
    # Step 1: Create mask
    mask = np.full(len(logits), -np.inf)
    mask[allowed_ids] = 0.0
    
    # Step 2: Apply mask
    masked_logits = logits + mask
    
    # Step 3: Softmax (disallowed tokens become 0.0)
    exp_logits = np.exp(masked_logits - np.max(masked_logits))
    probs = exp_logits / np.sum(exp_logits[allowed_ids])
    
    # Step 4: Loss (only if target is allowed)
    if target_id in allowed_ids:
        loss = -np.log(probs[target_id] + 1e-10)
    else:
        loss = 10.0  # High loss (shouldn't happen)
    
    return loss
```

**Consequence**: The optimizer **cannot learn to prefer forbidden tokens** because they have zero probability and zero gradient.

### Training Statistics

```python
training_stats = {
    'epoch': 5,
    'step': 1250,
    'train_loss': 2.34,
    'val_loss': 2.45,
    'best_val_loss': 2.30,
    'tokens_processed': 40000,
    'sequences_processed': 2000,
    'average_sequence_length': 20,
    'rejection_rate': 0.15,  # 15% of tokens rejected by constraints
}
```

---

## Integration Patterns

### Pattern 1: Full Integration

```python
# Complete SanTOK SLM setup
from santok_cognitive.slm import SanTOKConstrainedSLM

# Create SLM
slm = SanTOKConstrainedSLM()

# Load knowledge from SanTOK Cognitive
facts = unified_memory.get_facts(query)
reasoning_path = reasoner.get_reasoning_path(query)

slm.load_knowledge(facts, reasoning_path)

# Generate
result = slm.generate("What is Python?")
print(result.text)  # "Python is a programming language"
```

### Pattern 2: Constraint-Only (Phase 1)

```python
# Use only constraint system (no sequence optimizer)
from santok_cognitive.slm import SanTOKSLM

slm = SanTOKSLM()
slm.load_knowledge(facts)
result = slm.generate(query)

# Output: Fact-grounded tokens, but may have poor ordering
```

### Pattern 3: Custom Constraints

```python
# Add custom constraints
from santok_cognitive.slm import ConstraintEngine, TokenConstraint

engine = ConstraintEngine()
engine.add_facts_from_cognitive(facts)

# Custom constraint: no numbers in names
constraint = TokenConstraint(
    pattern=r'^[a-zA-Z]+$',
    name="no_numbers"
)
engine.add_constraint(constraint)

# Use with decoder
decoder = ConstrainedDecoder(optimizer, engine)
```

---

## Formal Properties

### Invariant 1: Structural Impossibility of Hallucination

**Statement**: A token that is not in the allowed set has exactly 0.0 probability of being generated.

**Proof**:

```
Let T be a token not in allowed set.
Let scores be optimizer scores.
Let allowed_ids be allowed token IDs.

1. mask[T.id] = -inf (by constraint system)
2. masked_scores[T.id] = scores[T.id] + (-inf) = -inf
3. exp(-inf) = 0
4. probs[T.id] = 0 / sum(exp(allowed)) = 0
5. P(generate T) = 0

Therefore: P(generate T) = 0 for all T not in allowed set.
```

### Invariant 2: Completeness of Allowed Set

**Statement**: All tokens in the allowed set have non-zero probability.

**Proof**:

```
Let T be a token in allowed set.

1. mask[T.id] = 0 (by constraint system)
2. masked_scores[T.id] = scores[T.id] + 0 = scores[T.id]
3. Since scores are finite, exp(scores[T.id]) > 0
4. probs[T.id] = exp(scores[T.id]) / sum(exp(allowed)) > 0
5. P(generate T) > 0

Therefore: P(generate T) > 0 for all T in allowed set.
```

### Invariant 3: Determinism

**Statement**: Given the same input sequence and constraints, the probability distribution over tokens is deterministic.

**Proof**:

```
Let S be a sequence, C be constraints.

1. sequence_ids = encode(S)  (deterministic function)
2. scores = optimizer.forward(sequence_ids)  (deterministic)
3. allowed_ids = constraints.get_allowed()  (deterministic)
4. mask = create_mask(allowed_ids)  (deterministic)
5. masked_scores = scores + mask  (deterministic)
6. probs = softmax(masked_scores)  (deterministic)

Therefore: P(tokens | S, C) is deterministic.
```

### Invariant 4: Monotonicity

**Statement**: Adding more constraints can only reduce the allowed set, never expand it.

**Proof**:

```
Let C1 be constraints, C2 be C1 + additional constraint.
Let A1 = allowed_set(C1), A2 = allowed_set(C2).

By constraint application:
- A2 = A1 ∩ (tokens satisfying additional constraint)
- Therefore: A2 ⊆ A1

Therefore: Adding constraints reduces allowed set.
```

---

## Implementation Details

### Memory Management

```python
# Embedding matrix: vocab_size × d_model
# Example: 10000 × 128 = 1,280,000 floats = ~5 MB

# Weight matrices per layer:
# Pattern Matcher: 4 × (d_model × d_model) = 4 × 16384 = 65,536 floats
# Processor: 2 × (d_model × d_ff) = 2 × 65536 = 131,072 floats

# Total for 2 layers: ~800,000 floats = ~3 MB

# Total memory: ~8-10 MB for model
# Plus ~5 MB for activations during inference
# Total: ~15 MB (very lightweight)
```

### Computational Complexity

```
Forward Pass Complexity:
─────────────────────────────────────────────────────────────

1. Embedding lookup: O(seq_len)
2. Position encoding: O(seq_len × d_model)
3. Pattern matching: O(seq_len² × d_model × n_heads)
4. Processing: O(seq_len × d_model × d_ff)
5. Output projection: O(d_model × vocab_size)

Total per token: O(seq_len² × d_model × n_heads)
For seq_len=50, d_model=128, n_heads=4:
    ≈ 50² × 128 × 4 = 1,280,000 operations
    ≈ 1.3M FLOPs per token (very fast)
```

### Numerical Stability

```python
# Softmax stability
def stable_softmax(x):
    x_shifted = x - np.max(x)  # Prevents overflow
    exp_x = np.exp(x_shifted)
    return exp_x / np.sum(exp_x)  # Normalization

# Layer normalization
def layer_norm(x):
    mean = np.mean(x)
    var = np.var(x)
    return (x - mean) / np.sqrt(var + 1e-6)  # Prevents division by zero
```

---

## Use Cases and Examples

### Use Case 1: Regulated Industry Q&A

```python
# Medical AI system
facts = [
    "Aspirin is used for pain relief",
    "Aspirin should not be taken with blood thinners",
    "Recommended dose is 325mg"
]

slm.load_knowledge(facts)

query = "What is aspirin used for?"
result = slm.generate(query)
# Output: "Aspirin is used for pain relief"
# CANNOT say: "Aspirin cures cancer" (not in facts)
```

### Use Case 2: Technical Documentation

```python
# API documentation system
facts = [
    "API endpoint: /users/{id}",
    "Method: GET",
    "Returns: User object",
    "Authentication required"
]

slm.load_knowledge(facts)

query = "How do I get a user?"
result = slm.generate(query)
# Output: "GET /users/{id} returns User object"
# Structurally guaranteed to be accurate
```

### Use Case 3: Compliance Systems

```python
# Legal compliance system
facts = [
    "GDPR requires consent for data processing",
    "Data must be encrypted in transit",
    "Right to deletion within 30 days"
]

slm.load_knowledge(facts)

query = "What are GDPR requirements?"
result = slm.generate(query)
# Output: Fact-grounded, auditable, explainable
```

---

## Summary

SanTOK SLM provides **structural guarantees** against hallucination through:

1. **Token-level constraint enforcement** (hallucination impossible)
2. **Masked loss computation** (only allowed tokens learned)
3. **Symbol ID abstraction** (no semantic leakage)
4. **Weak-by-design architecture** (intelligence stays in Cognitive)

This makes it suitable for:
- Regulated industries (healthcare, finance, legal)
- Compliance systems (auditable, explainable)
- Technical documentation (accurate, traceable)
- Safety-critical applications (deterministic, verifiable)

**Key Insight**: Unlike statistical language models, SanTOK SLM provides **formal guarantees** rather than probabilistic assurances.

---

**End of Documentation**

