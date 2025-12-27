"""
SanTOK Cognitive - Complete Showcase
====================================

This demonstrates ALL SanTOK Cognitive capabilities in one place:

1. Knowledge Graph - Store and query relationships
2. Knowledge Trees - Hierarchical organization
3. Unified Memory - Link everything together
4. Symbolic Reasoning - Infer new facts
5. Custom Algorithms - 100% SanTOK-original

Run:
    python -m santok_cognitive.showcase
"""

from .graph import GraphStore, GraphNode, RelationType
from .trees import TreeStore, Tree
from .memory import UnifiedMemory
from .reasoning import (
    SanTOKReasoner,
    InferenceEngine,
    ContradictionDetector,
    PathFinder,
)
from .algorithms import (
    SanTOKRanker,
    SanTOKPatternMatcher,
    SanTOK9Scorer,
    SanTOKGraphWalker,
    SanTOKSimilarity,
    SanTOKQueryParser,
    WalkMode,
)


def print_header(title: str):
    """Print a section header."""
    print("\n" + "═" * 60)
    print(f"  {title}")
    print("═" * 60)


def demo_knowledge_graph():
    """Demonstrate Knowledge Graph capabilities."""
    print_header("1. KNOWLEDGE GRAPH")
    
    graph = GraphStore()
    
    # Create nodes
    nodes = [
        (1, "SanTOK", "system"),
        (2, "Tokenization", "module"),
        (3, "Embeddings", "module"),
        (4, "AI System", "class"),
        (5, "NLP Tool", "class"),
    ]
    
    for nid, text, ntype in nodes:
        graph.add_node(GraphNode(nid, text, node_type=ntype))
    
    # Create edges
    edges = [
        (1, 2, RelationType.HAS_PART),
        (1, 3, RelationType.HAS_PART),
        (1, 4, RelationType.IS_A),
        (4, 5, RelationType.IS_A),
        (2, 3, RelationType.PRECEDES),
    ]
    
    for src, tgt, rel in edges:
        graph.add_edge(src, tgt, rel)
    
    print(f"\nGraph: {graph.node_count} nodes, {graph.edge_count} edges")
    print("\nRelationships:")
    for edge in graph.get_all_edges():
        src = graph.get_node(edge.source_id)
        tgt = graph.get_node(edge.target_id)
        print(f"  {src.text} --[{edge.relation_type.value}]--> {tgt.text}")
    
    return graph


def demo_knowledge_trees():
    """Demonstrate Knowledge Trees capabilities."""
    print_header("2. KNOWLEDGE TREES")
    
    trees = TreeStore()
    
    # Create a concept tree
    tree = trees.create_tree("ai_taxonomy", "AI Taxonomy")
    
    # Add nodes
    tree.add_node("ai", "Artificial Intelligence")
    tree.add_node("ml", "Machine Learning", parent_id="ai")
    tree.add_node("dl", "Deep Learning", parent_id="ml")
    tree.add_node("nlp", "NLP", parent_id="ai")
    tree.add_node("tokenization", "Tokenization", parent_id="nlp")
    tree.add_node("embeddings", "Embeddings", parent_id="nlp")
    tree.add_node("cv", "Computer Vision", parent_id="ai")
    
    print(f"\nTree: {tree.name} ({len(tree)} nodes)")
    print("\nHierarchy:")
    
    def print_tree(node_id: str, indent: int = 0):
        node = tree.get_node(node_id)
        if node:
            print("  " * indent + f"├─ {node.content}")
            for child_id in node.children_ids:
                print_tree(child_id, indent + 1)
    
    print_tree("ai")
    
    # Path finding
    path = tree.get_path_from_root("embeddings")
    print(f"\nPath to 'Embeddings': {' → '.join(n.content for n in path)}")
    
    return trees


def demo_unified_memory():
    """Demonstrate Unified Memory capabilities."""
    print_header("3. UNIFIED MEMORY")
    
    memory = UnifiedMemory()
    
    # Add knowledge
    facts = [
        ("SanTOK is a unique tokenization system", "fact"),
        ("SanTOK uses 9 different tokenization methods", "fact"),
        ("Tokenization converts text to tokens", "concept"),
        ("Embeddings represent tokens as vectors", "concept"),
        ("SanTOK generates embeddings without neural networks", "fact"),
    ]
    
    for content, ctype in facts:
        memory.add(content, ctype, auto_link_graph=True)
    
    # Add relations
    graph = memory.graph
    nodes = list(graph.get_all_nodes())
    if len(nodes) >= 2:
        graph.add_edge(nodes[0].node_id, nodes[1].node_id, RelationType.RELATED_TO)
    
    print(f"\nMemory: {len(memory)} objects")
    print(f"Graph: {memory.graph.node_count} nodes")
    print(f"Trees: {len(memory.trees)} trees")
    
    print("\nStored facts:")
    for obj in list(memory.objects.values())[:5]:
        print(f"  - {obj.content[:50]}...")
    
    return memory


def demo_symbolic_reasoning(memory: UnifiedMemory):
    """Demonstrate Symbolic Reasoning capabilities."""
    print_header("4. SYMBOLIC REASONING")
    
    # Build a graph for reasoning
    graph = GraphStore()
    
    nodes = [
        (1, "SanTOK", "system"),
        (2, "Knowledge System", "class"),
        (3, "AI System", "class"),
        (4, "Software", "class"),
    ]
    
    for nid, text, ntype in nodes:
        graph.add_node(GraphNode(nid, text, node_type=ntype))
    
    edges = [
        (1, 2, RelationType.IS_A),
        (2, 3, RelationType.IS_A),
        (3, 4, RelationType.IS_A),
    ]
    
    for src, tgt, rel in edges:
        graph.add_edge(src, tgt, rel)
    
    # Run inference
    engine = InferenceEngine(graph)
    engine.rules.add_builtin_rules()
    result = engine.infer_all()
    
    print("\nDirect relationships:")
    for edge in graph.get_all_edges():
        src = graph.get_node(edge.source_id)
        tgt = graph.get_node(edge.target_id)
        print(f"  {src.text} IS_A {tgt.text}")
    
    print(f"\n✨ Inferred {len(result.inferred_facts)} new facts:")
    for fact in result.inferred_facts:
        src = graph.get_node(fact.source_id)
        tgt = graph.get_node(fact.target_id)
        print(f"  {src.text} --[{fact.relation.value}]--> {tgt.text}")
        print(f"    (Rule: {fact.rule_id}, Confidence: {fact.confidence:.0%})")


def demo_custom_algorithms():
    """Demonstrate all custom algorithms."""
    print_header("5. CUSTOM ALGORITHMS")
    
    # 5.1 Query Parser
    print("\n5.1 QUERY PARSER")
    print("-" * 40)
    
    parser = SanTOKQueryParser()
    
    queries = [
        "What is machine learning?",
        "How does SanTOK work?",
        "Is Python a programming language?",
        "What are the parts of a computer?",
    ]
    
    for query in queries:
        parsed = parser.parse(query)
        print(f"\n  Q: \"{query}\"")
        print(f"  Type: {parsed.query_type.value}")
        print(f"  Subject: {parsed.subject}")
    
    # 5.2 Pattern Matcher
    print("\n5.2 PATTERN MATCHER")
    print("-" * 40)
    
    matcher = SanTOKPatternMatcher()
    
    texts = [
        "Python is a programming language.",
        "Machine learning depends on data.",
        "SanTOK uses tokenization.",
    ]
    
    for text in texts:
        matches = matcher.extract(text)
        if matches:
            print(f"\n  \"{text}\"")
            for match in matches:
                print(f"    → {match}")
    
    # 5.3 Semantic Similarity
    print("\n5.3 SEMANTIC SIMILARITY")
    print("-" * 40)
    
    sim = SanTOKSimilarity()
    
    pairs = [
        ("machine learning", "deep learning"),
        ("dog", "cat"),
        ("tokenization", "embedding"),
        ("hello world", "goodbye universe"),
    ]
    
    for text_a, text_b in pairs:
        result = sim.compute(text_a, text_b)
        print(f"\n  \"{text_a}\" vs \"{text_b}\"")
        print(f"    Score: {result.score:.4f} (DR={result.digital_root})")
    
    # 5.4 9-Centric Scorer
    print("\n5.4 9-CENTRIC SCORER")
    print("-" * 40)
    
    scorer = SanTOK9Scorer()
    
    values = [0.95, 0.72, 0.5, 0.33]
    for value in values:
        score = scorer.to_9(value)
        meaning = scorer.interpret_root(score.digital_root)
        print(f"  {value:.2f} → DR={score.digital_root} ({meaning})")
    
    # 5.5 Graph Walker
    print("\n5.5 GRAPH WALKER")
    print("-" * 40)
    
    graph = GraphStore()
    for i in range(1, 5):
        graph.add_node(GraphNode(i, f"Node{i}", "test"))
    graph.add_edge(1, 2, RelationType.RELATED_TO)
    graph.add_edge(2, 3, RelationType.RELATED_TO)
    graph.add_edge(3, 4, RelationType.RELATED_TO)
    
    walker = SanTOKGraphWalker(graph)
    result = walker.walk(1, 4, mode=WalkMode.WEIGHTED)
    
    print(f"\n  Path from Node1 to Node4:")
    path = " → ".join(s.node_text for s in result.path)
    print(f"    {path}")
    print(f"    Score: {result.total_score:.4f}")


def demo_full_pipeline():
    """Demonstrate complete pipeline."""
    print_header("6. FULL PIPELINE")
    
    # Create memory
    memory = UnifiedMemory()
    
    # Add knowledge
    texts = [
        "SanTOK is a unique tokenization system",
        "SanTOK uses 9 different methods",
        "Tokenization is part of NLP",
        "NLP is a branch of AI",
        "SanTOK generates embeddings without neural networks",
    ]
    
    for text in texts:
        memory.add(text, "fact", auto_link_graph=True)
    
    # Create reasoner
    reasoner = SanTOKReasoner(memory)
    
    # Answer questions
    questions = [
        "What is SanTOK?",
        "How does tokenization work?",
    ]
    
    print("\nQ&A Demo:")
    
    for question in questions:
        print(f"\n  Q: {question}")
        answer = reasoner.ask(question)
        print(f"  A: {answer.text}")
        print(f"  Confidence: {answer.confidence:.0%}")
        if answer.inferences_made:
            print(f"  Inferences: {len(answer.inferences_made)}")


def main():
    """Run complete showcase."""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         SANTOK COGNITIVE SHOWCASE                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   A complete demonstration of SanTOK's cognitive capabilities.                ║
║                                                                               ║
║   100% UNIQUE. 100% SANTOK-NATIVE.                                            ║
║                                                                               ║
║   ✗ NO GPT              ✗ NO Transformers        ✗ NO Neural Networks         ║
║   ✗ NO PyTorch          ✗ NO TensorFlow          ✗ NO External AI             ║
║                                                                               ║
║   ✓ Pure Symbolic       ✓ Rule-Based             ✓ Template Generation        ║
║   ✓ Custom Algorithms   ✓ 9-Centric Math         ✓ 100% Explainable           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run demos
    graph = demo_knowledge_graph()
    trees = demo_knowledge_trees()
    memory = demo_unified_memory()
    demo_symbolic_reasoning(memory)
    demo_custom_algorithms()
    demo_full_pipeline()
    
    # Summary
    print_header("SHOWCASE COMPLETE")
    
    print("""
What makes SanTOK Cognitive UNIQUE:

  KNOWLEDGE STORAGE
    ├── Graph Store     → Relationships, multi-hop reasoning
    ├── Tree Store      → Hierarchy, taxonomy, inheritance
    └── Unified Memory  → Links vectors, graphs, trees

  REASONING ENGINE
    ├── Inference Engine    → Rule chaining (20+ rules)
    ├── Contradiction Detector → Find conflicts
    └── Path Finder         → Multi-hop paths

  CUSTOM ALGORITHMS
    ├── SanTOKRanker        → Hybrid relevance scoring
    ├── SanTOKPatternMatcher → Relation extraction (no ML)
    ├── SanTOK9Scorer       → 9-centric confidence
    ├── SanTOKGraphWalker   → Energy-based traversal
    ├── SanTOKSimilarity    → Semantic similarity (no neural)
    └── SanTOKQueryParser   → NL to structured query

  VERBALIZATION
    └── Template-based generation (NO neural LLM)

All of this is 100% SanTOK-original.
No borrowed algorithms. No external AI.

This is what makes SanTOK STAND OUT.
    """)


if __name__ == "__main__":
    main()

