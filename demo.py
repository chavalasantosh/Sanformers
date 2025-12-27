"""
SanTOK Cognitive - Demo Script
==============================

Run this to see the cognitive system in action:
    python -m santok_cognitive.demo
    
Demonstrates:
- Knowledge Graph with relations
- Knowledge Trees with hierarchy
- Unified Memory linking everything
- SYMBOLIC REASONING (NEW):
  - Rule-based inference
  - Transitive closure (IS_A, PART_OF)
  - Confidence propagation
  - Contradiction detection
- HYBRID REASONING (NEW):
  - Structured context generation
  - Ready for LLM verbalization
"""

from .graph import GraphStore, GraphNode, RelationType, RelationExtractor
from .trees import Tree, TreeStore
from .memory import UnifiedMemory
from .reasoning import (
    InferenceEngine, RuleBase, 
    ContradictionDetector,
    HybridReasoner, StructuredContext
)


def demo_graph():
    """Demonstrate the Knowledge Graph."""
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH DEMO")
    print("="*60)
    
    graph = GraphStore()
    
    # Add nodes
    graph.add_node(GraphNode(1, "Machine Learning", node_type="concept"))
    graph.add_node(GraphNode(2, "Deep Learning", node_type="concept"))
    graph.add_node(GraphNode(3, "Neural Networks", node_type="concept"))
    graph.add_node(GraphNode(4, "Transformers", node_type="concept"))
    graph.add_node(GraphNode(5, "Attention", node_type="concept"))
    
    # Add relationships
    graph.add_edge(2, 1, RelationType.IS_A)      # Deep Learning IS_A Machine Learning
    graph.add_edge(3, 2, RelationType.PART_OF)   # Neural Networks PART_OF Deep Learning
    graph.add_edge(4, 3, RelationType.IS_A)      # Transformers IS_A Neural Networks
    graph.add_edge(4, 5, RelationType.USES)      # Transformers USES Attention
    
    print(f"\nCreated graph with {len(graph)} nodes")
    stats = graph.get_stats()
    print(f"Stats: nodes={stats.node_count}, edges={stats.edge_count}")
    
    # Get neighbors
    print("\nNeighbors of 'Transformers' (node 4):")
    neighbors = graph.get_neighbors(4, direction="both")
    for neighbor, edge in neighbors:
        print(f"  - {neighbor.text} ({edge.relation_type.value})")


def demo_inference():
    """Demonstrate symbolic inference."""
    print("\n" + "="*60)
    print("SYMBOLIC INFERENCE DEMO")
    print("="*60)
    
    graph = GraphStore()
    
    # Build a type hierarchy
    # Dog IS_A Mammal IS_A Animal IS_A LivingThing
    graph.add_node(GraphNode(1, "Dog", node_type="entity"))
    graph.add_node(GraphNode(2, "Mammal", node_type="class"))
    graph.add_node(GraphNode(3, "Animal", node_type="class"))
    graph.add_node(GraphNode(4, "LivingThing", node_type="class"))
    graph.add_node(GraphNode(5, "Cat", node_type="entity"))
    graph.add_node(GraphNode(6, "Spine", node_type="part"))
    
    # Direct edges
    graph.add_edge(1, 2, RelationType.IS_A)  # Dog IS_A Mammal
    graph.add_edge(2, 3, RelationType.IS_A)  # Mammal IS_A Animal
    graph.add_edge(3, 4, RelationType.IS_A)  # Animal IS_A LivingThing
    graph.add_edge(5, 2, RelationType.IS_A)  # Cat IS_A Mammal
    graph.add_edge(2, 6, RelationType.HAS_PART)  # Mammal HAS_PART Spine
    
    print("Direct edges:")
    for edge in graph.get_all_edges():
        src = graph.get_node(edge.source_id)
        tgt = graph.get_node(edge.target_id)
        print(f"  {src.text} --[{edge.relation_type.value}]--> {tgt.text}")
    
    # Run inference
    print("\nRunning inference...")
    engine = InferenceEngine(graph)
    engine.rules.add_builtin_rules()
    result = engine.infer_all()
    
    print(f"\nInference complete:")
    print(f"  - Facts inferred: {len(result.inferred_facts)}")
    print(f"  - Iterations: {result.total_iterations}")
    print(f"  - Time: {result.time_elapsed*1000:.1f}ms")
    
    print("\nInferred facts:")
    for fact in result.inferred_facts[:10]:
        src = graph.get_node(fact.source_id)
        tgt = graph.get_node(fact.target_id)
        print(f"  {src.text} --[{fact.relation.value}]--> {tgt.text}")
        print(f"    (via {fact.rule_id}, confidence: {fact.confidence:.0%})")
    
    # Show transitive IS_A
    print("\nTransitive closure for 'Dog' (IS_A):")
    closure = engine.get_transitive_closure(1, RelationType.IS_A)
    for node_id, conf, depth in closure:
        node = graph.get_node(node_id)
        print(f"  Dog IS_A {node.text} (depth={depth}, conf={conf:.0%})")


def demo_contradiction():
    """Demonstrate contradiction detection."""
    print("\n" + "="*60)
    print("CONTRADICTION DETECTION DEMO")
    print("="*60)
    
    graph = GraphStore()
    
    # Add some nodes
    graph.add_node(GraphNode(1, "Hot", node_type="property"))
    graph.add_node(GraphNode(2, "Cold", node_type="property"))
    graph.add_node(GraphNode(3, "Water", node_type="substance"))
    
    # Add contradictory edges
    graph.add_edge(1, 2, RelationType.OPPOSITE_OF)  # Hot OPPOSITE_OF Cold
    graph.add_edge(1, 2, RelationType.SIMILAR_TO)   # Hot SIMILAR_TO Cold (contradiction!)
    
    # Add a self-reference (violation)
    graph.add_node(GraphNode(4, "Thing", node_type="class"))
    graph.add_edge(4, 4, RelationType.IS_A)  # Thing IS_A Thing (reflexive violation)
    
    print("Checking for contradictions...")
    detector = ContradictionDetector(graph)
    report = detector.detect_all()
    
    print(f"\n{report.summary()}")


def demo_hybrid_reasoning():
    """Demonstrate hybrid symbolic + neural reasoning."""
    print("\n" + "="*60)
    print("HYBRID REASONING DEMO")
    print("="*60)
    print("(Symbolic cognition → Structured context → LLM verbalization)")
    
    # Build knowledge base
    memory = UnifiedMemory()
    
    # Add facts about AI
    facts = [
        ("Transformers are a type of neural network architecture", "fact"),
        ("Attention mechanism allows models to focus on relevant parts", "fact"),
        ("BERT uses bidirectional attention", "fact"),
        ("GPT uses causal (left-to-right) attention", "fact"),
        ("Self-attention computes relationships between all positions", "concept"),
        ("Transformers have replaced RNNs in many NLP tasks", "fact"),
    ]
    
    objs = []
    for content, ctype in facts:
        obj = memory.add(content, ctype, auto_link_graph=True)
        objs.append(obj)
    
    # Add relationships
    memory.add_relation(objs[0].uid, objs[1].uid, RelationType.USES)
    memory.add_relation(objs[2].uid, objs[1].uid, RelationType.USES)
    memory.add_relation(objs[3].uid, objs[1].uid, RelationType.USES)
    memory.add_relation(objs[4].uid, objs[1].uid, RelationType.IS_A)
    memory.add_relation(objs[2].uid, objs[0].uid, RelationType.IS_A)
    memory.add_relation(objs[3].uid, objs[0].uid, RelationType.IS_A)
    
    print(f"Knowledge base: {len(memory)} facts, {memory.graph.edge_count} relations")
    
    # Create hybrid reasoner
    reasoner = HybridReasoner(memory)
    
    # Build context for a query
    query = "How does attention work in transformers?"
    print(f"\nQuery: {query}")
    
    context = reasoner.build_context(query)
    
    print("\n--- STRUCTURED CONTEXT (for LLM) ---")
    print(context.to_prompt())
    
    # Answer without generator (returns structured summary)
    print("\n--- ANSWER (without neural generator) ---")
    answer = reasoner.answer(query)
    print(answer.answer)
    
    print("\n--- REASONING TRACE ---")
    print(answer.explain())


def demo_full_pipeline():
    """Show the complete cognitive pipeline."""
    print("\n" + "="*60)
    print("FULL COGNITIVE PIPELINE")
    print("="*60)
    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                    SanTOK Cognitive                         │
    │                                                             │
    │  Query: "What can dogs do?"                                │
    │    ↓                                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 1. RETRIEVAL (Graph + Tree + Memory)                │   │
    │  │    - Find "Dog" node                                 │   │
    │  │    - Get direct relations                            │   │
    │  │    - Get tree context                                │   │
    │  └─────────────────────────────────────────────────────┘   │
    │    ↓                                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 2. INFERENCE (Symbolic Reasoning)                    │   │
    │  │    - Apply transitivity (IS_A chains)                │   │
    │  │    - Property inheritance                            │   │
    │  │    - Confidence propagation                          │   │
    │  └─────────────────────────────────────────────────────┘   │
    │    ↓                                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 3. VALIDATION (Contradiction Check)                  │   │
    │  │    - Flag conflicts                                  │   │
    │  │    - Adjust confidence                               │   │
    │  └─────────────────────────────────────────────────────┘   │
    │    ↓                                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 4. STRUCTURED CONTEXT                                │   │
    │  │    - Facts + Inferences + Paths + Hierarchy          │   │
    │  │    - Ready for LLM verbalization                     │   │
    │  └─────────────────────────────────────────────────────┘   │
    │    ↓                                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 5. NEURAL VERBALIZATION (Optional LLM)               │   │
    │  │    - LLM is SPEAKER, not THINKER                     │   │
    │  │    - Converts structure to natural language          │   │
    │  └─────────────────────────────────────────────────────┘   │
    │    ↓                                                        │
    │  Answer + Explanation + Confidence                         │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    """)


def main():
    """Run all demos."""
    print("\n" + "#"*60)
    print("#" + " "*16 + "SANTOK COGNITIVE v0.2" + " "*17 + "#")
    print("#" + " "*12 + "Symbolic + Neural Reasoning" + " "*15 + "#")
    print("#"*60)
    
    demo_graph()
    demo_inference()
    demo_contradiction()
    demo_hybrid_reasoning()
    demo_full_pipeline()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("""
The SanTOK Cognitive system now provides:

  GRAPH:
  ✓ Knowledge Graph with 17+ relation types
  ✓ Path finding (BFS, Dijkstra)
  ✓ Relation extraction from text

  TREES:
  ✓ Hierarchical knowledge organization
  ✓ Tree traversal (BFS, DFS)
  ✓ Subtree operations

  MEMORY:
  ✓ Unified Memory linking vectors + graphs + trees
  ✓ Cross-store queries

  SYMBOLIC REASONING (NEW):
  ✓ Rule-based inference engine
  ✓ 20+ built-in inference rules
  ✓ Transitive closure (IS_A, PART_OF, CAUSES, etc.)
  ✓ Property inheritance
  ✓ Confidence propagation through chains
  ✓ Contradiction detection + flags

  HYBRID REASONING (NEW):
  ✓ Structured context generation
  ✓ Ready for LLM verbalization
  ✓ "The LLM becomes a speaker, not a thinker"
  ✓ Explainable answers with reasoning traces

All separate from santok_complete - no modifications needed!
""")


if __name__ == "__main__":
    main()
