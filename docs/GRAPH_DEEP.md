# Graph Module - Deep Technical Specification

## 1. Module Purpose

The Graph module implements a **custom knowledge graph** that stores:
- Entities (nodes)
- Relationships (edges)
- Type hierarchies
- Confidence scores

**NOT using:** Neo4j, NetworkX, or any graph database.

---

## 2. Data Structures

### 2.1 GraphNode Internal Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      GRAPHNODE                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   REQUIRED FIELDS                                           │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ node_id: int        │ Unique identifier (hash-based) │  │
│   │ text: str           │ Node content/label             │  │
│   │ node_type: str      │ "entity"|"concept"|"event"     │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   OPTIONAL FIELDS                                           │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ embedding_ref: str  │ Reference to vector embedding  │  │
│   │ metadata: Dict      │ Custom key-value pairs         │  │
│   │ created_at: float   │ Unix timestamp                 │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   MEMORY FOOTPRINT: ~100 bytes per node                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 GraphEdge Internal Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      GRAPHEDGE                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   REQUIRED FIELDS                                           │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ edge_id: int           │ Auto-generated unique ID    │  │
│   │ source_id: int         │ Source node ID              │  │
│   │ target_id: int         │ Target node ID              │  │
│   │ relation_type: RelType │ Enum value                  │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   OPTIONAL FIELDS                                           │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ weight: float          │ Confidence 0.0-1.0          │  │
│   │ evidence: str          │ Source/reason for edge      │  │
│   │ metadata: Dict         │ Custom key-value pairs      │  │
│   │ created_at: float      │ Unix timestamp              │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   MEMORY FOOTPRINT: ~150 bytes per edge                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 GraphStore Internal Data Structures

```
┌─────────────────────────────────────────────────────────────┐
│                     GRAPHSTORE INTERNALS                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   PRIMARY STORAGE (Dict-based for O(1) access)              │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ _nodes: Dict[int, GraphNode]                         │  │
│   │   Key: node_id                                       │  │
│   │   Value: GraphNode object                            │  │
│   │                                                      │  │
│   │ _edges: Dict[int, GraphEdge]                         │  │
│   │   Key: edge_id                                       │  │
│   │   Value: GraphEdge object                            │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ADJACENCY LISTS (For efficient traversal)                 │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ _outgoing: Dict[int, Set[int]]                       │  │
│   │   Key: node_id                                       │  │
│   │   Value: Set of edge_ids leaving this node           │  │
│   │                                                      │  │
│   │ _incoming: Dict[int, Set[int]]                       │  │
│   │   Key: node_id                                       │  │
│   │   Value: Set of edge_ids entering this node          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   INDICES (For fast lookup by attribute)                    │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ _by_relation_type: Dict[str, Set[int]]               │  │
│   │   Key: relation_type.value (e.g., "is_a")            │  │
│   │   Value: Set of edge_ids with this relation          │  │
│   │                                                      │  │
│   │ _by_node_type: Dict[str, Set[int]]                   │  │
│   │   Key: node_type (e.g., "entity")                    │  │
│   │   Value: Set of node_ids with this type              │  │
│   │                                                      │  │
│   │ _by_text: Dict[str, Set[int]]                        │  │
│   │   Key: text.lower()                                  │  │
│   │   Value: Set of node_ids with this text              │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. RelationType Enum - Complete Reference

```python
class RelationType(Enum):
    """All 15+ supported relation types."""
    
    # ═══════════════════════════════════════════════════════
    # TAXONOMIC RELATIONS
    # ═══════════════════════════════════════════════════════
    
    IS_A = "is_a"
    # Meaning: Subject is a type/instance of Object
    # Example: Dog IS_A Animal
    # Inverse: None (use HAS_INSTANCE if needed)
    # Transitive: Yes (Dog IS_A Animal, Animal IS_A Organism → Dog IS_A Organism)
    
    PART_OF = "part_of"
    # Meaning: Subject is a component of Object
    # Example: Wheel PART_OF Car
    # Inverse: HAS_PART
    # Transitive: Yes (Piston PART_OF Engine, Engine PART_OF Car → Piston PART_OF Car)
    
    HAS_PART = "has_part"
    # Meaning: Subject contains Object as component
    # Example: Car HAS_PART Wheel
    # Inverse: PART_OF
    # Transitive: Yes
    
    # ═══════════════════════════════════════════════════════
    # CAUSAL RELATIONS
    # ═══════════════════════════════════════════════════════
    
    CAUSES = "causes"
    # Meaning: Subject leads to/produces Object
    # Example: Fire CAUSES Smoke
    # Inverse: CAUSED_BY
    # Transitive: Yes (A CAUSES B, B CAUSES C → A CAUSES C)
    
    CAUSED_BY = "caused_by"
    # Meaning: Subject is produced by Object
    # Example: Smoke CAUSED_BY Fire
    # Inverse: CAUSES
    # Transitive: Yes
    
    # ═══════════════════════════════════════════════════════
    # FUNCTIONAL RELATIONS
    # ═══════════════════════════════════════════════════════
    
    USES = "uses"
    # Meaning: Subject utilizes Object
    # Example: Chef USES Knife
    # Inverse: USED_BY
    # Transitive: No
    
    USED_BY = "used_by"
    # Meaning: Subject is utilized by Object
    # Example: Knife USED_BY Chef
    # Inverse: USES
    # Transitive: No
    
    DEPENDS_ON = "depends_on"
    # Meaning: Subject requires Object
    # Example: App DEPENDS_ON Database
    # Inverse: None (asymmetric)
    # Transitive: Yes
    
    # ═══════════════════════════════════════════════════════
    # SEMANTIC RELATIONS
    # ═══════════════════════════════════════════════════════
    
    SIMILAR_TO = "similar_to"
    # Meaning: Subject resembles Object
    # Example: Cat SIMILAR_TO Dog
    # Inverse: Self (symmetric)
    # Transitive: No (similarity is not transitive)
    
    OPPOSITE_OF = "opposite_of"
    # Meaning: Subject contrasts with Object
    # Example: Hot OPPOSITE_OF Cold
    # Inverse: Self (symmetric)
    # Transitive: No
    
    RELATED_TO = "related_to"
    # Meaning: Generic association
    # Example: AI RELATED_TO Machine_Learning
    # Inverse: Self (symmetric)
    # Transitive: No
    
    # ═══════════════════════════════════════════════════════
    # TEMPORAL RELATIONS
    # ═══════════════════════════════════════════════════════
    
    PRECEDES = "precedes"
    # Meaning: Subject comes before Object in time/sequence
    # Example: Monday PRECEDES Tuesday
    # Inverse: FOLLOWS
    # Transitive: Yes
    
    FOLLOWS = "follows"
    # Meaning: Subject comes after Object in time/sequence
    # Example: Tuesday FOLLOWS Monday
    # Inverse: PRECEDES
    # Transitive: Yes
    
    # ═══════════════════════════════════════════════════════
    # SOURCE RELATIONS
    # ═══════════════════════════════════════════════════════
    
    DERIVED_FROM = "derived_from"
    # Meaning: Subject originates from Object
    # Example: French DERIVED_FROM Latin
    # Inverse: None
    # Transitive: Yes
    
    MENTIONS = "mentions"
    # Meaning: Subject references Object
    # Example: Document MENTIONS Person
    # Inverse: None
    # Transitive: No
    
    CONTAINS = "contains"
    # Meaning: Subject includes Object (for collections)
    # Example: Book CONTAINS Chapter
    # Inverse: None (similar to HAS_PART)
    # Transitive: No
```

---

## 4. Operations - Deep Dive

### 4.1 add_node Operation

```
Input: GraphNode
Output: node_id (int)

Algorithm:
┌─────────────────────────────────────────────────────────────┐
│ 1. Store node in _nodes dict                                │
│    _nodes[node.node_id] = node                              │
│                                                             │
│ 2. Update node_type index                                   │
│    _by_node_type[node.node_type].add(node.node_id)         │
│                                                             │
│ 3. Update text index                                        │
│    _by_text[node.text.lower()].add(node.node_id)           │
│                                                             │
│ 4. Return node_id                                           │
└─────────────────────────────────────────────────────────────┘

Time Complexity: O(1)
Space Complexity: O(1)
```

### 4.2 add_edge Operation

```
Input: source_id, target_id, relation_type, weight, evidence
Output: edge_id (int)

Algorithm:
┌─────────────────────────────────────────────────────────────┐
│ 1. Validate source and target exist                         │
│    if source_id not in _nodes: raise ValueError             │
│    if target_id not in _nodes: raise ValueError             │
│                                                             │
│ 2. Generate edge_id                                         │
│    edge_id = _next_edge_id                                  │
│    _next_edge_id += 1                                       │
│                                                             │
│ 3. Create edge object                                       │
│    edge = GraphEdge(edge_id, source_id, target_id, ...)    │
│                                                             │
│ 4. Store edge                                               │
│    _edges[edge_id] = edge                                   │
│                                                             │
│ 5. Update adjacency lists                                   │
│    _outgoing[source_id].add(edge_id)                       │
│    _incoming[target_id].add(edge_id)                       │
│                                                             │
│ 6. Update relation type index                               │
│    _by_relation_type[relation_type.value].add(edge_id)     │
│                                                             │
│ 7. Return edge_id                                           │
└─────────────────────────────────────────────────────────────┘

Time Complexity: O(1)
Space Complexity: O(1)
```

### 4.3 get_neighbors Operation

```
Input: node_id, direction ("outgoing"|"incoming"|"both"), relation_types (optional)
Output: List[GraphNode]

Algorithm:
┌─────────────────────────────────────────────────────────────┐
│ 1. Collect relevant edge_ids based on direction             │
│    edge_ids = set()                                         │
│    if direction in ("outgoing", "both"):                    │
│        edge_ids |= _outgoing[node_id]                       │
│    if direction in ("incoming", "both"):                    │
│        edge_ids |= _incoming[node_id]                       │
│                                                             │
│ 2. Get edges                                                │
│    edges = [_edges[eid] for eid in edge_ids]               │
│                                                             │
│ 3. Filter by relation type (if specified)                   │
│    if relation_types:                                       │
│        edges = [e for e in edges                           │
│                 if e.relation_type in relation_types]       │
│                                                             │
│ 4. Extract neighbor node_ids                                │
│    neighbor_ids = set()                                     │
│    for edge in edges:                                       │
│        if edge.source_id == node_id:                       │
│            neighbor_ids.add(edge.target_id)                │
│        else:                                                │
│            neighbor_ids.add(edge.source_id)                │
│                                                             │
│ 5. Return neighbor nodes                                    │
│    return [_nodes[nid] for nid in neighbor_ids]            │
└─────────────────────────────────────────────────────────────┘

Time Complexity: O(k) where k = number of edges connected to node
Space Complexity: O(k)
```

---

## 5. RelationExtractor - Pattern Details

### 5.1 Pattern Format

```
Each pattern is a tuple:
(regex_pattern, relation_type, subject_group, object_group)

Example:
(r"(\w+) is a (\w+)", RelationType.IS_A, 1, 2)
│        │              │               │  │
│        │              │               │  └── Object is in group 2
│        │              │               └───── Subject is in group 1
│        │              └───────────────────── Relation to assign
│        └──────────────────────────────────── Regex pattern
└───────────────────────────────────────────── Raw string
```

### 5.2 All 34 Patterns

```
IS_A PATTERNS (5):
1. "(\w+(?:\s+\w+)?)\s+is\s+a\s+(\w+(?:\s+\w+)?)"
2. "(\w+(?:\s+\w+)?)\s+are\s+(\w+(?:\s+\w+)?)"
3. "(\w+(?:\s+\w+)?)\s+is\s+an?\s+(\w+(?:\s+\w+)?)"
4. "(\w+)\s+,\s+a\s+type\s+of\s+(\w+)"
5. "(\w+)\s+is\s+known\s+as\s+(\w+)"

PART_OF PATTERNS (4):
6. "(\w+)\s+is\s+part\s+of\s+(\w+)"
7. "(\w+)\s+belongs\s+to\s+(\w+)"
8. "(\w+)\s+is\s+a\s+component\s+of\s+(\w+)"
... (continued in pattern_matcher.py)
```

---

## 6. Serialization

### 6.1 JSON Format

```json
{
  "nodes": [
    {
      "node_id": 1,
      "text": "SanTOK",
      "node_type": "system",
      "embedding_ref": null,
      "metadata": {},
      "created_at": 1703721600.0
    }
  ],
  "edges": [
    {
      "edge_id": 1,
      "source_id": 1,
      "target_id": 2,
      "relation_type": "has_part",
      "weight": 1.0,
      "evidence": "explicit",
      "metadata": {},
      "created_at": 1703721600.0
    }
  ],
  "metadata": {
    "version": "1.0",
    "created_at": 1703721600.0,
    "node_count": 1,
    "edge_count": 1
  }
}
```

### 6.2 Pickle Format

```python
# Save
with open("graph.pkl", "wb") as f:
    pickle.dump(graph_store, f)

# Load
with open("graph.pkl", "rb") as f:
    graph_store = pickle.load(f)
```

---

## 7. Performance Characteristics

```
┌─────────────────────────────────────────────────────────────┐
│                  PERFORMANCE BENCHMARKS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Operation              │ 1K nodes │ 10K nodes │ 100K nodes│
│   ──────────────────────┼──────────┼───────────┼───────────│
│   add_node               │ <1ms     │ <1ms      │ <1ms      │
│   get_node               │ <1ms     │ <1ms      │ <1ms      │
│   add_edge               │ <1ms     │ <1ms      │ <1ms      │
│   get_neighbors (avg k)  │ <1ms     │ <1ms      │ <1ms      │
│   get_all_nodes          │ <1ms     │ 5ms       │ 50ms      │
│   BFS traversal          │ 10ms     │ 100ms     │ 1000ms    │
│   ──────────────────────┼──────────┼───────────┼───────────│
│   Memory (nodes only)    │ 100KB    │ 1MB       │ 10MB      │
│   Memory (with edges)    │ 250KB    │ 2.5MB     │ 25MB      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Usage Examples

### 8.1 Basic Graph Operations

```python
from santok_cognitive.graph import GraphStore, GraphNode, RelationType

# Create store
graph = GraphStore()

# Add nodes
graph.add_node(GraphNode(1, "Dog", "entity"))
graph.add_node(GraphNode(2, "Animal", "class"))
graph.add_node(GraphNode(3, "Mammal", "class"))

# Add edges
graph.add_edge(1, 3, RelationType.IS_A)  # Dog IS_A Mammal
graph.add_edge(3, 2, RelationType.IS_A)  # Mammal IS_A Animal

# Query
neighbors = graph.get_neighbors(1, direction="outgoing")
# Returns: [GraphNode(3, "Mammal", ...)]

# Get all edges of a type
is_a_edges = graph.get_edges_by_type(RelationType.IS_A)
# Returns: [edge1, edge2]
```

### 8.2 Traversal

```python
# BFS from node 1
from collections import deque

def bfs(graph, start_id):
    visited = {start_id}
    queue = deque([start_id])
    path = []
    
    while queue:
        node_id = queue.popleft()
        path.append(node_id)
        
        for edge in graph.get_outgoing_edges(node_id):
            if edge.target_id not in visited:
                visited.add(edge.target_id)
                queue.append(edge.target_id)
    
    return path

path = bfs(graph, 1)  # [1, 3, 2]
```

---

This completes the deep technical specification for the Graph module.

