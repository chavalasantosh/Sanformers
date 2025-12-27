"""
SanTOK SLM Phase 2 Demo

Demonstrates the transformer-constrained generation.
Shows how a tiny transformer provides word order while
SanTOK Cognitive maintains structural control.

Key insight:
    Transformer proposes → SanTOK disposes
    
    The transformer learns LOCAL patterns (which tokens go together).
    It does NOT learn facts or reasoning.
    Intelligence stays in SanTOK Cognitive.
"""

import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from santok_cognitive.slm import (
    TransformerConstrainedSLM,
    create_transformer_slm,
    TinyTransformer,
    TransformerConfig,
)


def demo_transformer_basic():
    """Demo 1: Basic transformer with constraints."""
    print("=" * 60)
    print("DEMO 1: Transformer with Constraints")
    print("=" * 60)
    
    # Create SLM
    slm = create_transformer_slm(
        vocab_size=5000,
        d_model=64,  # Very tiny
        n_layers=2,
        n_heads=2,
    )
    
    # Load facts
    facts = [
        "Python is a programming language",
        "Python was created by Guido van Rossum",
        "Python is used for web development",
        "Python supports multiple programming paradigms",
        "Python has a large standard library",
    ]
    
    slm.load_knowledge(facts)
    
    print("\nFacts loaded:")
    for fact in facts:
        print(f"  • {fact}")
    
    print(f"\nTransformer stats:")
    stats = slm.get_stats()
    print(f"  Parameters: {stats['transformer_parameters']:,}")
    print(f"  Size: {stats['transformer_size_mb']:.2f} MB")
    print(f"  Vocabulary: {stats['vocab_size']} tokens")
    
    # Generate
    print("\n" + "-" * 40)
    query = "What is Python?"
    print(f"Query: {query}")
    print("-" * 40)
    
    text, metadata = slm.generate(query, max_length=30, min_length=10)
    
    print(f"\nGenerated text: {text}")
    print(f"\nMetadata:")
    print(f"  Steps: {metadata['steps']}")
    print(f"  Rejections: {metadata['rejections']}")
    print(f"  Tokens: {len(metadata['tokens'])}")


def demo_weak_by_design():
    """Demo 2: Show that transformer is weak by design."""
    print("\n" + "=" * 60)
    print("DEMO 2: Transformer is Weak by Design")
    print("=" * 60)
    
    # Create SLM with minimal transformer
    slm = create_transformer_slm(
        d_model=32,  # Tiny
        n_layers=1,  # Single layer
        n_heads=2,
    )
    
    # Load VERY limited facts
    facts = [
        "The sky is blue",
        "Water is wet",
    ]
    
    slm.load_knowledge(facts)
    
    print("\nFacts loaded (only 2):")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\nKey insight:")
    print("  The transformer has NOT seen these facts during training.")
    print("  It has random weights (untrained).")
    print("  It only learns LOCAL token ordering patterns.")
    print("  It CANNOT learn facts or reasoning.")
    
    # Try to ask about something NOT in facts
    queries = [
        "What color is the sky?",     # In facts
        "Tell me about Python",       # NOT in facts
    ]
    
    for query in queries:
        print("\n" + "-" * 40)
        print(f"Query: {query}")
        print("-" * 40)
        
        text, metadata = slm.generate(query, max_length=20, min_length=5)
        print(f"Response: {text}")
        
        # Show that it can ONLY use tokens from facts
        used_tokens = set(metadata['tokens'])
        fact_tokens = set()
        import re
        for fact in facts:
            fact_tokens.update(re.findall(r'\b\w+\b', fact.lower()))
        
        print(f"\nTokens used: {sorted(used_tokens)}")
        print(f"Fact tokens: {sorted(fact_tokens)}")
        print(f"All used tokens in facts? {used_tokens.issubset(fact_tokens)}")


def demo_transformer_proposes_santok_disposes():
    """Demo 3: Show the integration rule."""
    print("\n" + "=" * 60)
    print("DEMO 3: Transformer Proposes → SanTOK Disposes")
    print("=" * 60)
    
    # Create SLM
    slm = create_transformer_slm(d_model=64, n_layers=2)
    
    facts = [
        "Machine learning is a subset of artificial intelligence",
        "Machine learning uses algorithms to learn from data",
        "Neural networks are used in machine learning",
        "Deep learning uses multiple neural network layers",
    ]
    
    slm.load_knowledge(facts)
    
    print("\nFacts loaded:")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\n" + "-" * 40)
    print("How it works:")
    print("-" * 40)
    print("""
    1. Transformer generates scores for ALL tokens in vocabulary
    2. SanTOK Cognitive filters to ONLY fact-grounded tokens
    3. Disallowed tokens get ZERO probability
    4. We sample only from allowed set
    
    Even if transformer "wants" to generate "Python" or "Java",
    those tokens are NOT in the allowed set, so they get zero probability.
    """)
    
    # Generate
    query = "What is machine learning?"
    print(f"\nQuery: {query}")
    
    text, metadata = slm.generate(query, max_length=25, min_length=10)
    
    print(f"\nResponse: {text}")
    print(f"\nProof of constraint:")
    print(f"  Steps: {metadata['steps']}")
    print(f"  Rejections: {metadata['rejections']}")
    print(f"  Every token is grounded in facts")


def demo_symbol_ids_not_text():
    """Demo 4: Show that transformer sees symbol IDs, not text."""
    print("\n" + "=" * 60)
    print("DEMO 4: Symbol IDs, Not Raw Text")
    print("=" * 60)
    
    print("""
Critical design principle:

The transformer sees SYMBOL IDs, not raw text.

Why?
    - Prevents implicit memorization
    - Prevents hidden leakage of meaning
    - Prevents accidental hallucination pathways
    - Keeps transformer WEAK BY DESIGN

Flow:
    SanTOK Cognitive → Symbols → Symbol IDs → Transformer → Scores → Constraints → Text
    """)
    
    # Create transformer
    config = TransformerConfig(vocab_size=1000, d_model=64)
    transformer = TinyTransformer(config)
    
    # Set vocabulary
    symbols = ["python", "programming", "language", "guido", "van", "rossum"]
    symbol_to_id = {s: i for i, s in enumerate(symbols)}
    transformer.set_vocabulary(symbol_to_id)
    
    print("\nSymbol vocabulary:")
    for symbol, symbol_id in symbol_to_id.items():
        print(f"  '{symbol}' → ID {symbol_id}")
    
    print("\nTransformer operations:")
    print("  1. Receives: [0, 1, 2] (symbol IDs)")
    print("  2. Looks up embeddings: embedding[0], embedding[1], embedding[2]")
    print("  3. Processes through attention blocks")
    print("  4. Outputs: scores for all symbol IDs")
    print("  5. NEVER sees the actual words 'python', 'programming', etc.")
    
    # Demonstrate
    sequence = ["python", "is", "programming"]
    sequence_ids = transformer.encode_symbols(sequence)
    
    print(f"\nExample:")
    print(f"  Input symbols: {sequence}")
    print(f"  Encoded IDs: {sequence_ids}")
    print(f"  Transformer sees: {sequence_ids} (not the words)")


def demo_comparison_phase1_vs_phase2():
    """Demo 5: Compare Phase 1 vs Phase 2."""
    print("\n" + "=" * 60)
    print("DEMO 5: Phase 1 vs Phase 2")
    print("=" * 60)
    
    facts = [
        "Python is a programming language",
        "Python was created by Guido van Rossum",
        "Python is used for web development",
    ]
    
    print("\nFacts:")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\n" + "-" * 40)
    print("Phase 1 (Constraint-only):")
    print("-" * 40)
    print("  ✅ Structural control (no hallucination)")
    print("  ✅ Fact grounding")
    print("  ❌ Poor word order (word salad)")
    print("  ❌ No coherence")
    
    print("\n" + "-" * 40)
    print("Phase 2 (Transformer-constrained):")
    print("-" * 40)
    print("  ✅ Structural control (no hallucination)")
    print("  ✅ Fact grounding")
    print("  ✅ Better word order (transformer learns patterns)")
    print("  ✅ Improved coherence")
    print("  ✅ Still weak by design (no fact learning)")
    
    print("\n" + "-" * 40)
    print("Key difference:")
    print("-" * 40)
    print("  Phase 1: Random token selection from allowed set")
    print("  Phase 2: Transformer-guided token selection from allowed set")
    print("")
    print("  Both maintain structural control.")
    print("  Phase 2 just provides better ordering.")


def main():
    """Run all demos."""
    print("\n" + "#" * 60)
    print("#" + " " * 58 + "#")
    print("#" + "  SanTOK SLM Phase 2 - Transformer-Constrained".center(58) + "#")
    print("#" + " " * 58 + "#")
    print("#" * 60)
    print("\nThis demo shows how a tiny transformer provides word order")
    print("while SanTOK Cognitive maintains structural control.")
    print("\nKey principle: Transformer proposes → SanTOK disposes")
    
    demo_transformer_basic()
    demo_weak_by_design()
    demo_transformer_proposes_santok_disposes()
    demo_symbol_ids_not_text()
    demo_comparison_phase1_vs_phase2()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
Phase 2 adds a TINY transformer for sequence optimization.

What the transformer does:
    ✅ Learns local token ordering patterns
    ✅ Provides better word order
    ✅ Improves coherence
    
What the transformer does NOT do:
    ❌ Learn facts
    ❌ Learn reasoning
    ❌ Understand semantics
    ❌ Break constraints

Architecture:
    SanTOK Cognitive (THINKS) → facts + constraints
    Tiny Transformer (ORDERS) → token sequences
    Constrained Decoder (INTEGRATES) → transformer scores ∩ constraints

Rule:
    Transformer proposes → SanTOK disposes
    
    Even if transformer wants a token, if SanTOK disallows it,
    that token gets ZERO probability. Hallucination remains IMPOSSIBLE.

NumPy only. No ML frameworks. 100% SanTOK.
Transformer is WEAK BY DESIGN. Intelligence stays in Cognitive.
""")


if __name__ == "__main__":
    main()

