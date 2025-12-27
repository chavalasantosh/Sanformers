"""
SanTOK Cognitive - PURE SANTOK Demo
===================================

NO GPT. NO TRANSFORMERS. NO NEURAL NETWORKS. NO EXTERNAL AI.

This demonstrates 100% SanTOK-native:
- Tokenization (SanTOK's 9 methods)
- Embeddings (SanTOK's feature-based)
- Knowledge Graph (SanTOK's custom)
- Symbolic Inference (SanTOK's rule engine)
- Text Generation (SanTOK's template verbalizer)

Run:
    python -m santok_cognitive.demo_pure
"""

from .graph import GraphStore, GraphNode, RelationType
from .trees import TreeStore
from .memory import UnifiedMemory
from .reasoning import (
    SanTOKReasoner,
    InferenceEngine,
    ContradictionDetector,
)


def build_knowledge_base(memory: UnifiedMemory):
    """Build a knowledge base using ONLY SanTOK."""
    
    print("Building knowledge base (100% SanTOK)...")
    
    # Add facts
    facts = [
        ("SanTOK is a unique tokenization system", "fact"),
        ("SanTOK uses 9 different tokenization methods", "fact"),
        ("SanTOK generates embeddings without neural networks", "fact"),
        ("SanTOK uses feature-based embedding generation", "concept"),
        ("The backend number composition is a SanTOK algorithm", "fact"),
        ("xorshift64* is used for UID generation in SanTOK", "fact"),
        ("SanTOK supports word, subword, character, and semantic tokenization", "fact"),
        ("The digital root folding uses 9-centric numerology", "fact"),
        ("SanTOK can train language models using only NumPy", "fact"),
        ("Co-occurrence learning is used for semantic embeddings", "concept"),
    ]
    
    for content, ctype in facts:
        memory.add(content, ctype, auto_link_graph=True)
    
    # Add explicit relations
    graph = memory.graph
    
    # Create concept nodes
    concepts = [
        (1001, "SanTOK", "system"),
        (1002, "Tokenization", "concept"),
        (1003, "Embeddings", "concept"),
        (1004, "Knowledge Graph", "concept"),
        (1005, "Inference Engine", "concept"),
        (1006, "Verbalizer", "concept"),
    ]
    
    for node_id, text, ntype in concepts:
        graph.add_node(GraphNode(node_id, text, node_type=ntype))
    
    # Add relations
    relations = [
        (1001, 1002, RelationType.HAS_PART),    # SanTOK HAS_PART Tokenization
        (1001, 1003, RelationType.HAS_PART),    # SanTOK HAS_PART Embeddings
        (1001, 1004, RelationType.HAS_PART),    # SanTOK HAS_PART Knowledge Graph
        (1001, 1005, RelationType.HAS_PART),    # SanTOK HAS_PART Inference Engine
        (1001, 1006, RelationType.HAS_PART),    # SanTOK HAS_PART Verbalizer
        (1003, 1002, RelationType.DEPENDS_ON),  # Embeddings DEPENDS_ON Tokenization
        (1005, 1004, RelationType.USES),        # Inference Engine USES Knowledge Graph
        (1006, 1005, RelationType.USES),        # Verbalizer USES Inference Engine
    ]
    
    for src, tgt, rel in relations:
        graph.add_edge(src, tgt, rel)
    
    # Create hierarchy tree
    hierarchy = {
        "SanTOK Core": ["Tokenization", "UID Generation", "Backend Numbers"],
        "Tokenization": ["Word", "Subword", "Character", "Semantic", "Sentence"],
        "SanTOK Cognitive": ["Knowledge Graph", "Inference", "Verbalization"],
        "Knowledge Graph": ["Nodes", "Edges", "Relations"],
        "Inference": ["Rules", "Transitivity", "Contradictions"],
    }
    
    tree = memory.trees.create_tree("santok_arch", "SanTOK Architecture")
    
    added = set()
    for parent, children in hierarchy.items():
        if parent not in added:
            parent_id = parent.lower().replace(" ", "_")
            tree.add_node(parent_id, parent)
            added.add(parent)
        
        for child in children:
            if child not in added:
                child_id = child.lower().replace(" ", "_")
                tree.add_node(child_id, child, parent_id=parent.lower().replace(" ", "_"))
                added.add(child)
    
    print(f"  - Facts: {len(memory.objects)}")
    print(f"  - Graph nodes: {memory.graph.node_count}")
    print(f"  - Graph edges: {memory.graph.edge_count}")
    print(f"  - Tree nodes: {len(tree)}")


def demo_pure_reasoning():
    """Demonstrate pure SanTOK reasoning."""
    
    print("\n" + "="*60)
    print("PURE SANTOK REASONING")
    print("NO GPT. NO TRANSFORMERS. NO NEURAL NETWORKS.")
    print("="*60)
    
    # Create memory
    memory = UnifiedMemory()
    
    # Build knowledge
    build_knowledge_base(memory)
    
    # Create SanTOK Reasoner (100% SanTOK)
    reasoner = SanTOKReasoner(memory)
    
    # Ask questions
    questions = [
        "What is SanTOK?",
        "How does tokenization work?",
        "What are the parts of SanTOK?",
        "Is inference related to knowledge graph?",
    ]
    
    print("\n--- QUESTIONS & ANSWERS ---")
    
    for question in questions:
        print(f"\n📝 Question: {question}")
        print("-" * 40)
        
        answer = reasoner.ask(question)
        
        print(f"💬 Answer: {answer.text}")
        print(f"📊 Confidence: {answer.confidence:.0%}")
        
        if answer.inferences_made:
            print(f"🔧 Inferences: {len(answer.inferences_made)}")
        
        if answer.rules_applied:
            print(f"📜 Rules: {', '.join(answer.rules_applied[:3])}")


def demo_inference():
    """Demonstrate symbolic inference."""
    
    print("\n" + "="*60)
    print("SYMBOLIC INFERENCE (100% RULE-BASED)")
    print("="*60)
    
    graph = GraphStore()
    
    # Build type hierarchy
    nodes = [
        (1, "SanTOK Cognitive", "system"),
        (2, "Knowledge System", "class"),
        (3, "AI System", "class"),
        (4, "Software", "class"),
        (5, "Graph Store", "component"),
        (6, "Tree Store", "component"),
    ]
    
    for nid, text, ntype in nodes:
        graph.add_node(GraphNode(nid, text, node_type=ntype))
    
    # Add relations
    graph.add_edge(1, 2, RelationType.IS_A)    # SanTOK Cognitive IS_A Knowledge System
    graph.add_edge(2, 3, RelationType.IS_A)    # Knowledge System IS_A AI System
    graph.add_edge(3, 4, RelationType.IS_A)    # AI System IS_A Software
    graph.add_edge(1, 5, RelationType.HAS_PART)  # SanTOK Cognitive HAS_PART Graph Store
    graph.add_edge(1, 6, RelationType.HAS_PART)  # SanTOK Cognitive HAS_PART Tree Store
    
    print("\nDirect edges:")
    for edge in graph.get_all_edges():
        src = graph.get_node(edge.source_id)
        tgt = graph.get_node(edge.target_id)
        print(f"  {src.text} --[{edge.relation_type.value}]--> {tgt.text}")
    
    # Run inference
    engine = InferenceEngine(graph)
    engine.rules.add_builtin_rules()
    result = engine.infer_all()
    
    print(f"\n✨ Inferred {len(result.inferred_facts)} new facts:")
    
    for fact in result.inferred_facts:
        src = graph.get_node(fact.source_id)
        tgt = graph.get_node(fact.target_id)
        print(f"  {src.text} --[{fact.relation.value}]--> {tgt.text}")
        print(f"    Rule: {fact.rule_id}, Confidence: {fact.confidence:.0%}")
    
    # Show transitive closure
    print("\n🔗 Transitive closure for 'SanTOK Cognitive' (IS_A):")
    closure = engine.get_transitive_closure(1, RelationType.IS_A)
    for node_id, conf, depth in closure:
        node = graph.get_node(node_id)
        print(f"  SanTOK Cognitive IS_A {node.text} (depth={depth})")


def demo_verbalization():
    """Demonstrate template-based verbalization."""
    
    print("\n" + "="*60)
    print("TEMPLATE VERBALIZATION (NO NEURAL GENERATION)")
    print("="*60)
    
    memory = UnifiedMemory()
    build_knowledge_base(memory)
    
    reasoner = SanTOKReasoner(memory)
    
    # Get detailed explanation
    question = "What are the components of SanTOK?"
    
    print(f"\n📝 Question: {question}")
    print("\n--- FULL REASONING TRACE ---")
    
    answer = reasoner.ask(question)
    print(answer.explain())


def main():
    """Run pure SanTOK demo."""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                  SANTOK COGNITIVE                              ║
║                                                               ║
║   100% UNIQUE. 100% SANTOK-NATIVE.                            ║
║                                                               ║
║   NO GPT          NO TRANSFORMERS      NO NEURAL NETWORKS     ║
║   NO PYTORCH      NO TENSORFLOW        NO EXTERNAL AI         ║
║                                                               ║
║   Pure symbolic reasoning + template verbalization            ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    demo_inference()
    demo_pure_reasoning()
    demo_verbalization()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("""
SanTOK Cognitive is 100% UNIQUE:

  ✗ NO GPT
  ✗ NO Transformers
  ✗ NO Neural Networks
  ✗ NO PyTorch/TensorFlow
  ✗ NO External AI APIs

  ✓ Pure symbolic inference
  ✓ Rule-based reasoning (20+ rules)
  ✓ Template verbalization
  ✓ Custom knowledge graph
  ✓ SanTOK tokenization integration
  ✓ Feature-based embeddings
  ✓ 100% explainable

This is what makes SanTOK STAND OUT.
    """)


if __name__ == "__main__":
    main()

