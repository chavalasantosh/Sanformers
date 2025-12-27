"""
SanTOK Custom Algorithms Demo
=============================

Demonstrates SANTOK-ORIGINAL algorithms:
1. SanTOKRanker - Hybrid relevance scoring
2. SanTOKPatternMatcher - Relation extraction without ML
3. SanTOK9Scorer - 9-centric confidence propagation
4. SanTOKGraphWalker - Custom graph traversal

Run:
    python -m santok_cognitive.demo_algorithms
"""

from .graph import GraphStore, GraphNode, RelationType
from .memory import UnifiedMemory
from .algorithms import (
    SanTOKRanker,
    SanTOKPatternMatcher,
    SanTOK9Scorer,
    SanTOKGraphWalker,
    WalkMode,
)


def demo_ranker():
    """Demonstrate SanTOK Ranker."""
    print("\n" + "="*60)
    print("SANTOK RANKER - Custom Hybrid Scoring")
    print("="*60)
    print("""
Formula:
    score = α·Relevance + β·Connectivity + γ·Hierarchy + δ·Freshness
    
    With 9-centric digital root transformation.
""")
    
    # Create memory with some content
    memory = UnifiedMemory()
    
    contents = [
        ("SanTOK is a unique tokenization system", "fact"),
        ("The ranker uses hybrid scoring", "fact"),
        ("Relevance is computed using token overlap", "fact"),
        ("Connectivity measures graph centrality", "concept"),
        ("Digital root folds scores to 1-9 range", "concept"),
    ]
    
    for content, ctype in contents:
        memory.add(content, ctype, auto_link_graph=True)
    
    # Create ranker
    ranker = SanTOKRanker(memory.graph, memory.trees)
    
    # Rank candidates
    query_tokens = ["santok", "ranking", "scoring"]
    
    print(f"Query tokens: {query_tokens}")
    print("\nRanking results:")
    print("-" * 40)
    
    results = ranker.rank(query_tokens, list(memory.objects.values()))
    
    for i, result in enumerate(results[:5]):
        obj = memory.objects.get(result.item_id)
        content = obj.content[:40] if obj else "?"
        
        print(f"\n{i+1}. {content}...")
        print(f"   Score: {result.score:.4f}")
        print(f"   Relevance: {result.relevance_score:.4f}")
        print(f"   Connectivity: {result.connectivity_score:.4f}")
        print(f"   Digital Root: {result.digital_root}")


def demo_pattern_matcher():
    """Demonstrate SanTOK Pattern Matcher."""
    print("\n" + "="*60)
    print("SANTOK PATTERN MATCHER - Relation Extraction Without ML")
    print("="*60)
    print("""
NO neural NER. NO dependency parsing. Pure regex patterns.
""")
    
    matcher = SanTOKPatternMatcher()
    
    texts = [
        "Python is a programming language. It uses dynamic typing.",
        "Machine learning is part of artificial intelligence.",
        "Transformers use attention mechanisms.",
        "The CPU causes faster processing.",
        "Deep learning depends on large datasets.",
        "A dog is similar to a wolf.",
    ]
    
    print("Extracting relations from text:")
    print("-" * 40)
    
    for text in texts:
        print(f"\nText: \"{text}\"")
        matches = matcher.extract(text)
        
        if matches:
            for match in matches:
                print(f"  ✓ {match}")
                print(f"    Confidence: {match.confidence:.2f}, Pattern: {match.pattern_id}")
        else:
            print("  (no relations found)")
    
    print(f"\nMatcher stats: {matcher.get_pattern_stats()}")


def demo_9_scorer():
    """Demonstrate SanTOK 9-Scorer."""
    print("\n" + "="*60)
    print("SANTOK 9-SCORER - 9-Centric Confidence Propagation")
    print("="*60)
    print("""
Based on SanTOK's 9-centric numerology:
    Digital Root: dr(n) = 1 + ((n - 1) mod 9)
    
    9 = completion, 8 = power, 7 = analysis, etc.
""")
    
    scorer = SanTOK9Scorer()
    
    # Convert values to 9-scale
    values = [0.95, 0.72, 0.5, 0.33, 0.1]
    
    print("\nValue → 9-Scale conversion:")
    print("-" * 40)
    
    for value in values:
        score = scorer.to_9(value)
        meaning = scorer.interpret_root(score.digital_root)
        print(f"{value:.2f} → DR={score.digital_root} ({meaning}), cycle={score.cycle}")
    
    # Combine scores
    print("\n\nCombining scores:")
    print("-" * 40)
    
    test_scores = [0.8, 0.6, 0.9, 0.7]
    print(f"Input: {test_scores}")
    
    for method in ["mean", "product", "max", "min"]:
        combined = scorer.combine_9(test_scores, method=method)
        print(f"  {method:8s}: {combined.raw:.4f} → DR={combined.digital_root}")
    
    # Confidence propagation
    print("\n\nConfidence propagation through chain:")
    print("-" * 40)
    
    chain_length = 5
    initial = 0.9
    
    print(f"Initial confidence: {initial}")
    print(f"Chain length: {chain_length}")
    print()
    
    scores = scorer.propagate_9(initial, chain_length)
    
    for i, score in enumerate(scores):
        meaning = scorer.interpret_root(score.digital_root)
        bar = "█" * int(score.raw * 20)
        print(f"Step {i+1}: {score.raw:.4f} DR={score.digital_root} ({meaning:10s}) {bar}")


def demo_graph_walker():
    """Demonstrate SanTOK Graph Walker."""
    print("\n" + "="*60)
    print("SANTOK GRAPH WALKER - Custom Graph Traversal")
    print("="*60)
    print("""
Energy-based traversal with relation-weighted edges.
""")
    
    # Build a graph
    graph = GraphStore()
    
    nodes = [
        (1, "SanTOK", "system"),
        (2, "Tokenization", "module"),
        (3, "Embeddings", "module"),
        (4, "Knowledge Graph", "module"),
        (5, "Inference", "module"),
        (6, "Verbalization", "module"),
        (7, "Answer", "output"),
    ]
    
    for nid, text, ntype in nodes:
        graph.add_node(GraphNode(nid, text, node_type=ntype))
    
    edges = [
        (1, 2, RelationType.HAS_PART),
        (1, 3, RelationType.HAS_PART),
        (1, 4, RelationType.HAS_PART),
        (2, 3, RelationType.PRECEDES),
        (3, 4, RelationType.PRECEDES),
        (4, 5, RelationType.CAUSES),
        (5, 6, RelationType.CAUSES),
        (6, 7, RelationType.CAUSES),
        (1, 7, RelationType.RELATED_TO),  # Direct shortcut
    ]
    
    for src, tgt, rel in edges:
        graph.add_edge(src, tgt, rel)
    
    walker = SanTOKGraphWalker(graph, initial_energy=10.0)
    
    # Shortest path
    print("\n1. SHORTEST PATH (SanTOK → Answer):")
    print("-" * 40)
    
    result = walker.walk(1, 7, mode=WalkMode.SHORTEST)
    print(result.explain())
    
    # Weighted path (prefers strong relations)
    print("\n2. WEIGHTED PATH (SanTOK → Answer):")
    print("-" * 40)
    
    result = walker.walk(1, 7, mode=WalkMode.WEIGHTED)
    print(result.explain())
    
    # All paths
    print("\n3. ALL PATHS (SanTOK → Answer):")
    print("-" * 40)
    
    all_paths = walker.find_all_paths(1, 7, max_hops=6)
    
    for i, path in enumerate(all_paths[:3]):
        print(f"\nPath {i+1} (score={path.total_score:.4f}):")
        nodes_str = " → ".join(s.node_text for s in path.path)
        print(f"  {nodes_str}")
    
    # Random walk
    print("\n4. RANDOM WALK (from SanTOK, 5 steps):")
    print("-" * 40)
    
    result = walker.random_walk(1, steps=5)
    print(result.explain())


def main():
    """Run all algorithm demos."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         SANTOK COGNITIVE - CUSTOM ALGORITHMS                   ║
║                                                               ║
║   100% SANTOK-ORIGINAL. NOT BM25. NOT PageRank. NOT TF-IDF.   ║
║                                                               ║
║   These algorithms are UNIQUE to SanTOK:                      ║
║                                                               ║
║   • SanTOKRanker     - Hybrid relevance scoring               ║
║   • SanTOKPatternMatcher - Relation extraction (no ML)        ║
║   • SanTOK9Scorer    - 9-centric confidence                   ║
║   • SanTOKGraphWalker - Energy-based traversal                ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    demo_ranker()
    demo_pattern_matcher()
    demo_9_scorer()
    demo_graph_walker()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("""
These algorithms are what make SanTOK UNIQUE:

  ✗ NOT BM25
  ✗ NOT TF-IDF  
  ✗ NOT PageRank
  ✗ NOT Neural NER
  ✗ NOT Attention
  
  ✓ SanTOK Hybrid Ranking
  ✓ SanTOK Pattern Extraction
  ✓ SanTOK 9-Centric Scoring
  ✓ SanTOK Graph Walking
  
All custom. All original. All SanTOK.
    """)


if __name__ == "__main__":
    main()

