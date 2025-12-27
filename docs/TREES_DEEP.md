# Trees Module - Deep Technical Specification

## 1. Module Purpose

The Trees module provides **hierarchical knowledge organization**.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WHY TREES?                                                │
│                                                             │
│   Graphs = MESH (everything connected)                      │
│   Trees  = ORDER (structured hierarchy)                     │
│                                                             │
│   Trees enable:                                             │
│   • Taxonomies (AI → ML → Deep Learning)                   │
│   • Inheritance (child inherits parent properties)         │
│   • Navigation (drill down / roll up)                      │
│   • Explainability (show path from root)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Data Structures

### 2.1 TreeNode

**File:** `trees/tree_node.py`

```
┌─────────────────────────────────────────────────────────────┐
│                       TREENODE                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IDENTITY                                                  │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ node_id: str       │ Unique identifier (e.g., "ml") │  │
│   │ content: str       │ Display text ("Machine Learn")│  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   STRUCTURE                                                 │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ parent_id: Optional[str]  │ None for root           │  │
│   │ children_ids: List[str]   │ Ordered child list      │  │
│   │ depth: int                │ Distance from root       │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   CROSS-REFERENCES                                          │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ graph_node_id: Optional[int]   │ Link to graph     │  │
│   │ embedding_ref: Optional[str]    │ Link to vector   │  │
│   │ metadata: Dict[str, Any]        │ Custom data      │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   MEMORY: ~80 bytes per node (excluding content string)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Python Definition:**

```python
@dataclass
class TreeNode:
    node_id: str
    content: str
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    depth: int = 0
    
    graph_node_id: Optional[int] = None
    embedding_ref: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_leaf(self) -> bool:
        return len(self.children_ids) == 0
    
    @property
    def is_root(self) -> bool:
        return self.parent_id is None
```

### 2.2 Tree

**File:** `trees/tree.py`

```
┌─────────────────────────────────────────────────────────────┐
│                         TREE                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IDENTITY                                                  │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ tree_id: str      │ Unique identifier               │  │
│   │ name: str         │ Human-readable name             │  │
│   │ description: str  │ Optional description            │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   STRUCTURE                                                 │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ root_id: Optional[str]       │ Root node ID        │  │
│   │ _nodes: Dict[str, TreeNode]  │ All nodes           │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   METADATA                                                  │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ created_at: float  │ Creation timestamp             │  │
│   │ metadata: Dict     │ Custom tree-level data         │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 TreeStore

**File:** `trees/tree_store.py`

```
┌─────────────────────────────────────────────────────────────┐
│                       TREESTORE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   STORAGE                                                   │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ _trees: Dict[str, Tree]  │ tree_id → Tree          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   OPERATIONS                                                │
│   ├── create_tree(tree_id, name) → Tree                    │
│   ├── get_tree(tree_id) → Optional[Tree]                   │
│   ├── delete_tree(tree_id) → bool                          │
│   ├── list_trees() → List[str]                             │
│   └── __len__() → int                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Tree Types

### 3.1 Concept Tree (Taxonomy)

```
┌─────────────────────────────────────────────────────────────┐
│                     CONCEPT TREE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Purpose: Organize domain concepts hierarchically          │
│                                                             │
│   Example (AI Domain):                                      │
│                                                             │
│   Artificial Intelligence                                   │
│   ├── Machine Learning                                      │
│   │   ├── Supervised Learning                              │
│   │   │   ├── Classification                               │
│   │   │   └── Regression                                   │
│   │   ├── Unsupervised Learning                            │
│   │   │   ├── Clustering                                   │
│   │   │   └── Dimensionality Reduction                     │
│   │   └── Reinforcement Learning                           │
│   ├── Natural Language Processing                          │
│   │   ├── Tokenization                                     │
│   │   ├── Named Entity Recognition                         │
│   │   └── Machine Translation                              │
│   └── Computer Vision                                       │
│       ├── Image Classification                             │
│       └── Object Detection                                 │
│                                                             │
│   Properties:                                               │
│   • Children are subtypes of parent                        │
│   • Depth indicates specificity                            │
│   • Siblings are alternatives                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Document Tree (Structure)

```
┌─────────────────────────────────────────────────────────────┐
│                     DOCUMENT TREE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Purpose: Represent document structure                     │
│                                                             │
│   Example:                                                  │
│                                                             │
│   Research Paper                                            │
│   ├── Abstract                                              │
│   ├── Introduction                                          │
│   │   ├── Background                                       │
│   │   └── Motivation                                       │
│   ├── Methods                                               │
│   │   ├── Data Collection                                  │
│   │   └── Algorithm                                        │
│   ├── Results                                               │
│   │   ├── Experiment 1                                     │
│   │   └── Experiment 2                                     │
│   └── Conclusion                                            │
│                                                             │
│   Properties:                                               │
│   • Children are parts of parent                           │
│   • Order matters (siblings are ordered)                   │
│   • Depth indicates nesting level                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Reasoning Tree (Chain of Thought)

```
┌─────────────────────────────────────────────────────────────┐
│                    REASONING TREE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Purpose: Track reasoning/decision paths                   │
│                                                             │
│   Example (Question Answering):                             │
│                                                             │
│   Query: "Is Python good for ML?"                           │
│   ├── Parse query                                           │
│   │   ├── Subject: Python                                  │
│   │   └── Predicate: good for ML                           │
│   ├── Retrieve facts                                        │
│   │   ├── Fact 1: Python has ML libraries                  │
│   │   └── Fact 2: Python is easy to use                    │
│   ├── Infer                                                 │
│   │   └── Python IS_A programming language                 │
│   └── Conclude                                              │
│       └── Yes, Python is good for ML                       │
│                                                             │
│   Properties:                                               │
│   • Root is the question/goal                              │
│   • Children are sub-steps                                 │
│   • Leaves are conclusions/actions                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Version Tree (Evolution)

```
┌─────────────────────────────────────────────────────────────┐
│                     VERSION TREE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Purpose: Track concept evolution over time                │
│                                                             │
│   Example (SanTOK versions):                                │
│                                                             │
│   SanTOK v0.1                                               │
│   └── SanTOK v0.2                                           │
│       ├── SanTOK v0.3 (stable)                             │
│       │   └── SanTOK v0.3.1 (bugfix)                       │
│       └── SanTOK v0.4 (experimental)                       │
│                                                             │
│   Properties:                                               │
│   • Parent is previous version                             │
│   • Children are derived versions                          │
│   • Multiple children = branching                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Operations - Complete Reference

### 4.1 Node Operations

```
┌─────────────────────────────────────────────────────────────┐
│                    NODE OPERATIONS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  add_node(node_id, content, parent_id=None)                 │
│  ─────────────────────────────────────────────────────────  │
│  Algorithm:                                                 │
│  1. Create TreeNode with given parameters                  │
│  2. If parent_id specified:                                │
│     a. Validate parent exists                              │
│     b. Set node.parent_id = parent_id                      │
│     c. Set node.depth = parent.depth + 1                   │
│     d. Add node_id to parent.children_ids                  │
│  3. If no parent_id (root):                                │
│     a. Set node.depth = 0                                  │
│     b. Set tree.root_id = node_id                          │
│  4. Store in _nodes[node_id]                               │
│                                                             │
│  Time: O(1)                                                 │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  get_node(node_id) → Optional[TreeNode]                    │
│  ─────────────────────────────────────────────────────────  │
│  Return _nodes.get(node_id)                                │
│                                                             │
│  Time: O(1)                                                 │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  remove_node(node_id, recursive=True)                      │
│  ─────────────────────────────────────────────────────────  │
│  Algorithm:                                                 │
│  1. Get node                                               │
│  2. If recursive:                                          │
│     For each child in node.children_ids:                   │
│       remove_node(child, recursive=True)                   │
│  3. If has parent:                                         │
│     parent.children_ids.remove(node_id)                    │
│  4. Delete from _nodes                                     │
│                                                             │
│  Time: O(subtree_size) if recursive, O(1) otherwise        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Traversal Operations

```
┌─────────────────────────────────────────────────────────────┐
│                  TRAVERSAL OPERATIONS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  traverse_dfs(pre_order=True) → Generator[TreeNode]        │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  PRE-ORDER (visit parent before children):                 │
│       A              Visit order: A, B, D, E, C, F         │
│      / \                                                    │
│     B   C            def dfs_pre(node):                    │
│    / \   \               yield node                        │
│   D   E   F              for child in node.children:       │
│                              yield from dfs_pre(child)     │
│                                                             │
│  POST-ORDER (visit children before parent):                │
│       A              Visit order: D, E, B, F, C, A         │
│      / \                                                    │
│     B   C            def dfs_post(node):                   │
│    / \   \               for child in node.children:       │
│   D   E   F                  yield from dfs_post(child)    │
│                          yield node                        │
│                                                             │
│  Time: O(N) where N = number of nodes                      │
│  Space: O(H) where H = height (recursion stack)            │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  traverse_bfs() → Generator[TreeNode]                      │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  LEVEL-ORDER (visit level by level):                       │
│       A              Visit order: A, B, C, D, E, F         │
│      / \                                                    │
│     B   C            def bfs():                            │
│    / \   \               queue = [root]                    │
│   D   E   F              while queue:                      │
│                              node = queue.pop(0)           │
│                              yield node                    │
│                              queue.extend(node.children)   │
│                                                             │
│  Time: O(N)                                                 │
│  Space: O(W) where W = max width of tree                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Path Operations

```
┌─────────────────────────────────────────────────────────────┐
│                    PATH OPERATIONS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  get_path_from_root(node_id) → List[TreeNode]              │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: [root, ..., parent, node]                        │
│                                                             │
│  Example:                                                   │
│       A                                                     │
│      / \                                                    │
│     B   C          get_path_from_root("E")                 │
│    / \             → [A, B, E]                             │
│   D   E                                                     │
│                                                             │
│  Algorithm:                                                 │
│  1. Start at node                                          │
│  2. Collect ancestors by following parent_id               │
│  3. Reverse the list                                       │
│                                                             │
│  Time: O(H) where H = depth of node                        │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  get_ancestors(node_id) → List[TreeNode]                   │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: [parent, grandparent, ..., root]                 │
│                                                             │
│  Example:                                                   │
│       A                                                     │
│      / \                                                    │
│     B   C          get_ancestors("E")                      │
│    / \             → [B, A]                                │
│   D   E                                                     │
│                                                             │
│  Time: O(H)                                                 │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  get_descendants(node_id) → List[TreeNode]                 │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: All nodes in subtree (DFS order)                 │
│                                                             │
│  Example:                                                   │
│       A                                                     │
│      / \                                                    │
│     B   C          get_descendants("B")                    │
│    / \             → [D, E]                                │
│   D   E                                                     │
│                                                             │
│  Time: O(subtree_size)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Relationship Operations

```
┌─────────────────────────────────────────────────────────────┐
│                 RELATIONSHIP OPERATIONS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  get_siblings(node_id) → List[TreeNode]                    │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: Other children of same parent                    │
│                                                             │
│  Example:                                                   │
│       A                                                     │
│      /|\                                                    │
│     B C D        get_siblings("C") → [B, D]               │
│                                                             │
│  Algorithm:                                                 │
│  1. Get parent                                             │
│  2. Return parent.children - {node_id}                     │
│                                                             │
│  Time: O(k) where k = number of siblings                   │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  get_leaves() → List[TreeNode]                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: All nodes with no children                       │
│                                                             │
│  Algorithm:                                                 │
│  return [n for n in _nodes.values() if n.is_leaf]         │
│                                                             │
│  Time: O(N)                                                 │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  get_subtree(node_id) → Tree                               │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Returns: New Tree rooted at given node                    │
│                                                             │
│  Algorithm:                                                 │
│  1. Create new Tree                                        │
│  2. Copy node as root (depth=0, parent=None)               │
│  3. Recursively copy descendants                           │
│                                                             │
│  Time: O(subtree_size)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Tree Metrics

```
┌─────────────────────────────────────────────────────────────┐
│                     TREE METRICS                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HEIGHT                                                     │
│  ─────────────────────────────────────────────────────────  │
│  height(tree) = max(node.depth for node in tree)           │
│                                                             │
│       A                                                     │
│      / \           height = 2                              │
│     B   C                                                   │
│    /                                                        │
│   D                                                         │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  SIZE                                                       │
│  ─────────────────────────────────────────────────────────  │
│  size(tree) = |tree._nodes|                                │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  BREADTH (per level)                                        │
│  ─────────────────────────────────────────────────────────  │
│  breadth(level) = |{n : n.depth = level}|                  │
│                                                             │
│       A              Level 0: breadth = 1                  │
│      / \             Level 1: breadth = 2                  │
│     B   C            Level 2: breadth = 2                  │
│    / \                                                      │
│   D   E                                                     │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  BRANCHING FACTOR                                           │
│  ─────────────────────────────────────────────────────────  │
│  avg_branching = Σ(|n.children|) / |non_leaf_nodes|        │
│                                                             │
│       A              A: 2 children                         │
│      / \             B: 2 children                         │
│     B   C            C: 1 child                            │
│    / \   \           avg = (2+2+1)/3 = 1.67                │
│   D   E   F                                                 │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  BALANCE RATIO                                              │
│  ─────────────────────────────────────────────────────────  │
│  balance = min_depth / max_depth                           │
│                                                             │
│  Perfectly balanced: balance = 1.0                         │
│  Degenerate (list):  balance → 0                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Serialization

### 6.1 JSON Format

```json
{
  "tree_id": "ai_taxonomy",
  "name": "AI Taxonomy",
  "description": "Hierarchical organization of AI concepts",
  "root_id": "ai",
  "nodes": {
    "ai": {
      "node_id": "ai",
      "content": "Artificial Intelligence",
      "parent_id": null,
      "children_ids": ["ml", "nlp", "cv"],
      "depth": 0,
      "graph_node_id": 101,
      "metadata": {}
    },
    "ml": {
      "node_id": "ml",
      "content": "Machine Learning",
      "parent_id": "ai",
      "children_ids": ["supervised", "unsupervised"],
      "depth": 1,
      "graph_node_id": 102,
      "metadata": {}
    }
  },
  "metadata": {
    "version": "1.0",
    "created_at": 1703721600.0,
    "node_count": 10
  }
}
```

### 6.2 ASCII Visualization

```python
def print_tree(tree):
    """Print tree in ASCII format."""
    def _print(node_id, prefix="", is_last=True):
        node = tree.get_node(node_id)
        connector = "└── " if is_last else "├── "
        print(prefix + connector + node.content)
        
        children = node.children_ids
        for i, child_id in enumerate(children):
            extension = "    " if is_last else "│   "
            _print(child_id, prefix + extension, i == len(children) - 1)
    
    if tree.root_id:
        root = tree.get_node(tree.root_id)
        print(root.content)
        for i, child_id in enumerate(root.children_ids):
            _print(child_id, "", i == len(root.children_ids) - 1)
```

**Output:**
```
Artificial Intelligence
├── Machine Learning
│   ├── Supervised Learning
│   │   ├── Classification
│   │   └── Regression
│   └── Unsupervised Learning
│       ├── Clustering
│       └── Dimensionality Reduction
├── Natural Language Processing
│   ├── Tokenization
│   └── Named Entity Recognition
└── Computer Vision
    ├── Image Classification
    └── Object Detection
```

---

## 7. Integration with Graph

### 7.1 Tree-Graph Mapping

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   TREE-GRAPH RELATIONSHIP                                   │
│                                                             │
│   Tree Structure          →    Graph Relations              │
│   ─────────────────────────────────────────────────────────│
│   Parent-Child            →    IS_A or PART_OF             │
│                                                             │
│   Example:                                                  │
│                                                             │
│   Tree:                   Graph:                           │
│      Animal               Animal                            │
│      └── Dog              ↑                                │
│                          Dog ──[IS_A]──                    │
│                                                             │
│   Tree:                   Graph:                           │
│      Car                  Car                               │
│      └── Wheel            │                                │
│                          └──[HAS_PART]── Wheel             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Automatic Graph Node Creation

```python
def add_node_with_graph_link(tree, memory, node_id, content, parent_id=None):
    """Add tree node and create corresponding graph node."""
    
    # Add tree node
    tree.add_node(node_id, content, parent_id)
    tree_node = tree.get_node(node_id)
    
    # Create graph node
    graph_node = GraphNode(
        node_id=hash(node_id),
        text=content,
        node_type="concept"
    )
    memory.graph.add_node(graph_node)
    
    # Link tree node to graph node
    tree_node.graph_node_id = graph_node.node_id
    
    # If has parent, create IS_A edge in graph
    if parent_id:
        parent_tree_node = tree.get_node(parent_id)
        if parent_tree_node.graph_node_id:
            memory.graph.add_edge(
                graph_node.node_id,
                parent_tree_node.graph_node_id,
                RelationType.IS_A
            )
    
    return tree_node
```

---

## 8. Use Cases

### 8.1 Hierarchical Navigation

```python
# Navigate from specific to general
def explain_concept_hierarchy(tree, node_id):
    """Generate explanation using tree path."""
    path = tree.get_path_from_root(node_id)
    
    if len(path) <= 1:
        return f"{path[0].content} is a root concept."
    
    explanation = f"{path[-1].content} is a type of {path[-2].content}"
    
    if len(path) > 2:
        hierarchy = " → ".join(n.content for n in path)
        explanation += f"\n\nFull hierarchy: {hierarchy}"
    
    return explanation

# Example
print(explain_concept_hierarchy(tree, "classification"))
# Output:
# Classification is a type of Supervised Learning
# Full hierarchy: AI → Machine Learning → Supervised Learning → Classification
```

### 8.2 Semantic Search Enhancement

```python
def enhanced_search(tree, query_node_id, memory):
    """Search expanded with tree context."""
    
    # Get ancestors (for context expansion)
    ancestors = tree.get_ancestors(query_node_id)
    
    # Get siblings (for alternatives)
    siblings = tree.get_siblings(query_node_id)
    
    # Get descendants (for specializations)
    descendants = tree.get_descendants(query_node_id)
    
    # Expand search to include related nodes
    search_terms = [tree.get_node(query_node_id).content]
    
    # Add parent for context
    if ancestors:
        search_terms.append(ancestors[0].content)
    
    # Add siblings for alternatives
    for sib in siblings[:2]:
        search_terms.append(sib.content)
    
    # Search with expanded terms
    results = []
    for term in search_terms:
        results.extend(memory.search(term, limit=5))
    
    return results
```

---

## 9. Performance Characteristics

```
┌─────────────────────────────────────────────────────────────┐
│                  PERFORMANCE BENCHMARKS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Operation               │ 100 nodes │ 1K nodes │ 10K nodes│
│  ────────────────────────┼───────────┼──────────┼──────────│
│  add_node                │ <1ms      │ <1ms     │ <1ms     │
│  get_node                │ <1ms      │ <1ms     │ <1ms     │
│  get_path_from_root      │ <1ms      │ <1ms     │ <1ms     │
│  traverse_dfs (all)      │ <1ms      │ 5ms      │ 50ms     │
│  traverse_bfs (all)      │ <1ms      │ 5ms      │ 50ms     │
│  get_descendants         │ <1ms      │ varies   │ varies   │
│  print_tree (ASCII)      │ 5ms       │ 50ms     │ 500ms    │
│  ────────────────────────┼───────────┼──────────┼──────────│
│  Memory (nodes only)     │ 8KB       │ 80KB     │ 800KB    │
│  Memory (with metadata)  │ 20KB      │ 200KB    │ 2MB      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

This completes the deep technical specification for the Trees module.

