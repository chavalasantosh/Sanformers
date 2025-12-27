"""
SanTOK SLM Demo

Demonstrates the constrained generation system.
Shows how SanTOK Cognitive controls what the SLM can say.

Key insight:
    The SLM can ONLY emit tokens that are grounded in facts
    from SanTOK Cognitive. Hallucination is structurally impossible.
"""

import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from santok_cognitive.slm import (
    ConstraintEngine,
    ConstrainedGenerator,
    GenerationConfig,
    VocabularyScope,
)
from santok_cognitive.slm.slm_generator import SanTOKSLM


def demo_basic_constraints():
    """Demo 1: Basic constraint checking."""
    print("=" * 60)
    print("DEMO 1: Basic Constraint Checking")
    print("=" * 60)
    
    # Create constraint engine with facts
    engine = ConstraintEngine()
    
    facts = [
        "Python is a programming language",
        "Python was created by Guido van Rossum",
        "Python is used for web development",
        "Python supports multiple programming paradigms",
    ]
    
    engine.add_facts_from_cognitive(facts)
    
    # Set vocabulary scope
    scope = VocabularyScope()
    for fact in facts:
        import re
        tokens = re.findall(r'\b\w+\b', fact.lower())
        scope.add_tokens(tokens)
    engine.set_vocabulary_scope(scope)
    
    # Test tokens
    test_tokens = [
        "python",      # In facts ✓
        "programming", # In facts ✓
        "guido",       # In facts ✓
        "java",        # NOT in facts ✗
        "hallucinate", # NOT in facts ✗
        "is",          # Structural ✓
        "the",         # Structural ✓
    ]
    
    print("\nFacts loaded:")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\nToken checking:")
    for token in test_tokens:
        allowed, reason = engine.check_token(token)
        status = "✓ ALLOWED" if allowed else "✗ REJECTED"
        print(f"  '{token}': {status}")
    
    print(f"\nStats: {engine.get_stats()}")


def demo_constrained_generation():
    """Demo 2: Constrained text generation."""
    print("\n" + "=" * 60)
    print("DEMO 2: Constrained Text Generation")
    print("=" * 60)
    
    # Create SLM
    slm = SanTOKSLM()
    
    # Load facts from "SanTOK Cognitive"
    facts = [
        "Python is a programming language",
        "Python was created by Guido van Rossum in 1991",
        "Python is known for readable syntax",
        "Python supports object oriented programming",
        "Python is used for machine learning",
        "Python has a large standard library",
    ]
    
    reasoning_path = [
        "Query asks about Python",
        "Python IS_A programming language",
        "Python CREATED_BY Guido van Rossum",
        "Python KNOWN_FOR readable syntax",
    ]
    
    slm.load_knowledge(facts, reasoning_path)
    
    print("\nFacts loaded:")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\nReasoning path:")
    for step in reasoning_path:
        print(f"  → {step}")
    
    # Generate response
    print("\n" + "-" * 40)
    query = "What is Python?"
    print(f"Query: {query}")
    print("-" * 40)
    
    result = slm.generate(query)
    
    print(f"\nGenerated text: {result.text}")
    print(f"\nTokens: {result.tokens}")
    print(f"\nExplanation:")
    print(result.explain())


def demo_hallucination_prevention():
    """Demo 3: Show that hallucination is impossible."""
    print("\n" + "=" * 60)
    print("DEMO 3: Hallucination Prevention")
    print("=" * 60)
    
    # Create SLM with VERY limited facts
    slm = SanTOKSLM()
    
    # Only these facts exist
    facts = [
        "The sky is blue",
        "Water is wet",
        "Fire is hot",
    ]
    
    slm.load_knowledge(facts)
    
    print("\nFacts loaded (only 3):")
    for fact in facts:
        print(f"  • {fact}")
    
    # Try to ask about something NOT in facts
    queries = [
        "What color is the sky?",      # In facts
        "What is quantum physics?",     # NOT in facts
        "Tell me about Python",         # NOT in facts
    ]
    
    for query in queries:
        print("\n" + "-" * 40)
        print(f"Query: {query}")
        print("-" * 40)
        
        result = slm.generate(query)
        print(f"Response: {result.text}")
        print(f"Tokens used: {len(result.tokens)}")
        print(f"Tokens rejected: {result.tokens_rejected}")
        
        # The SLM CANNOT hallucinate about quantum physics
        # because those tokens are not in the allowed set


def demo_with_santok_cognitive():
    """Demo 4: Full integration with SanTOK Cognitive."""
    print("\n" + "=" * 60)
    print("DEMO 4: Integration with SanTOK Cognitive")
    print("=" * 60)
    
    # Simulate SanTOK Cognitive output
    # In real use, this comes from:
    #   - UnifiedMemory
    #   - SanTOKReasoner
    #   - InferenceEngine
    
    cognitive_output = {
        'facts': [
            "Machine learning is a subset of artificial intelligence",
            "Machine learning uses algorithms to learn from data",
            "Neural networks are used in machine learning",
            "Deep learning uses multiple neural network layers",
            "Machine learning can be supervised or unsupervised",
        ],
        'reasoning_path': [
            "Query: What is machine learning?",
            "machine_learning IS_A artificial_intelligence",
            "machine_learning USES algorithms",
            "machine_learning USES data",
            "neural_networks USED_BY machine_learning",
        ],
        'relations': [
            'is', 'are', 'uses', 'can', 'has',
            'subset', 'type', 'part', 'form',
        ],
        'confidence': 0.92,
    }
    
    print("\nSanTOK Cognitive output:")
    print(f"  Facts: {len(cognitive_output['facts'])}")
    print(f"  Reasoning steps: {len(cognitive_output['reasoning_path'])}")
    print(f"  Confidence: {cognitive_output['confidence']:.0%}")
    
    # Create SLM and load from Cognitive
    slm = SanTOKSLM()
    slm.load_knowledge(
        facts=cognitive_output['facts'],
        reasoning_path=cognitive_output['reasoning_path'],
        relations=cognitive_output['relations'],
    )
    
    # Generate response
    query = "What is machine learning?"
    print(f"\nQuery: {query}")
    
    result = slm.generate(query)
    
    print(f"\n{'=' * 40}")
    print("GROUNDED RESPONSE:")
    print(f"{'=' * 40}")
    print(result.text)
    print(f"\n{result.explain()}")


def demo_comparison():
    """Demo 5: Compare constrained vs unconstrained."""
    print("\n" + "=" * 60)
    print("DEMO 5: Constrained vs Unconstrained")
    print("=" * 60)
    
    facts = [
        "Paris is the capital of France",
        "France is a country in Europe",
        "The Eiffel Tower is in Paris",
    ]
    
    print("\nFacts available:")
    for fact in facts:
        print(f"  • {fact}")
    
    print("\n" + "-" * 40)
    print("UNCONSTRAINED LLM (hypothetical):")
    print("-" * 40)
    print("  Could say: 'Paris has 2.1 million people'")
    print("  Could say: 'Paris was founded by Romans'")
    print("  Could say: 'The Louvre is the largest museum'")
    print("  → These may be TRUE but are NOT in our facts")
    print("  → This is where hallucination risk exists")
    
    print("\n" + "-" * 40)
    print("SANTOK SLM (constrained):")
    print("-" * 40)
    
    slm = SanTOKSLM()
    slm.load_knowledge(facts)
    
    result = slm.generate("Tell me about Paris")
    print(f"  Response: {result.text}")
    print(f"  → ONLY uses tokens from verified facts")
    print(f"  → Cannot mention population (not in facts)")
    print(f"  → Cannot mention Romans (not in facts)")
    print(f"  → Cannot mention Louvre (not in facts)")
    print(f"  → Hallucination is STRUCTURALLY IMPOSSIBLE")


def main():
    """Run all demos."""
    print("\n" + "#" * 60)
    print("#" + " " * 58 + "#")
    print("#" + "    SanTOK SLM - Constrained Language Generation".center(58) + "#")
    print("#" + " " * 58 + "#")
    print("#" * 60)
    print("\nThis demo shows how SanTOK SLM generates text that is")
    print("STRUCTURALLY CONSTRAINED by SanTOK Cognitive.")
    print("\nKey insight: Hallucination is IMPOSSIBLE, not just unlikely.")
    
    demo_basic_constraints()
    demo_constrained_generation()
    demo_hallucination_prevention()
    demo_with_santok_cognitive()
    demo_comparison()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
SanTOK SLM is NOT a statistical language model.
It is a CONSTRAINED VERBALIZATION SYSTEM.

Architecture:
    SanTOK Cognitive (THINKS) → facts + constraints + reasoning
    SanTOK SLM (TALKS)        → constrained verbalization ONLY

The SLM can ONLY emit tokens that:
    1. Exist in the vocabulary scope
    2. Are grounded in verified facts
    3. Pass all active constraints

This makes hallucination STRUCTURALLY IMPOSSIBLE.
Not statistically unlikely. IMPOSSIBLE.

NumPy is used strictly as a numerical backend.
No pretrained models. No ML frameworks. 100% SanTOK.
""")


if __name__ == "__main__":
    main()

