import chromadb
import uuid
import time

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./memory_store")
collection = client.get_or_create_collection(name="memory")


def store_memory(content, weight=1.0, tags=None):
    """Store a memory in the database, avoiding duplicates."""

    tags = tags or []

    # Convert tags list to a string (comma-separated) since ChromaDB does not support lists
    tag_string = ",".join(tags) if tags else ""

    # 🔹 Step 1: Retrieve **all stored memories** and check for an exact match
    existing_memories = collection.get()["documents"]

    if content in existing_memories:
        print("⚠ Memory already exists, skipping storage.")
        return None  # Avoid duplicates

    # 🔹 Step 2: Generate a unique ID and store new memory
    memory_id = str(uuid.uuid4())
    metadata = {"timestamp": time.time(), "weight": weight, "tags": tag_string}

    collection.add(ids=[memory_id], metadatas=[metadata], documents=[content])
    print(f"📝 Memory stored: {content} (ID: {memory_id})")
    return memory_id


def retrieve_memories(query, n_results=5):
    """Retrieve the most relevant memories, ensuring diversity and auto-linking related concepts."""

    total_memories = len(collection.get()["documents"])
    n_results = min(n_results, total_memories)  # Prevents excessive retrieval warnings

    results = collection.query(query_texts=[query], n_results=n_results)

    if not results or "documents" not in results or not results["documents"]:
        return []

    # Extract and deduplicate memories
    retrieved_memories = list(set(results["documents"][0]))  # Remove duplicates
    retrieved_metadata = results.get("metadatas", [[]])[0]  # Default to empty list if missing

    # 🔹 Step 1: Sort by weight (higher = better) and timestamp (newer = better)
    sorted_memories = sorted(
        zip(retrieved_memories, retrieved_metadata),
        key=lambda x: (x[1].get("weight", 1.0), x[1].get("timestamp", 0)),  # Defaults for safety
        reverse=True
    )

    # 🔹 Step 2: Extract sorted results
    final_memories = [mem[0] for mem in sorted_memories]

    # 🔹 Step 3: **Detect Auto-Linking** (When two memories are often retrieved together)
    top_memory = final_memories[0] if final_memories else None
    linked_memories = final_memories[1:] if len(final_memories) > 1 else []

    if linked_memories:
        print(f"🔗 Auto-Linking: {top_memory} ↔ {linked_memories}")

    print(f"🔍 Retrieved memories → Top Memory: {top_memory} | Linked Memories: {linked_memories}")
    return final_memories


def update_memory(memory_id, new_content, weight=None):
    """Update a memory's content only if it has changed."""

    memory = collection.get(ids=[memory_id])

    if not memory["documents"]:  # Ensure the memory exists
        print("⚠️ Memory not found.")
        return

    existing_content = memory["documents"][0]

    if existing_content == new_content:
        print("⚠ No changes detected. Update skipped.")
        return  # Skip update if content is unchanged

    metadata = memory["metadatas"][0]

    # 🔹 If weight is not provided, **keep existing weight**
    if weight is None:
        weight = metadata.get("weight", 1.0)  # Default to 1.0 if missing

    metadata["weight"] = weight  # Update weight if provided

    collection.update(ids=[memory_id], metadatas=[metadata], documents=[new_content])

    print(f"🔄 Memory updated: {new_content}")


# ✅ **Testing the refined memory system**
test_id = store_memory("You love lilac-colored things.", weight=1.5, tags=["preference"])
retrieve_memories("lilac")

if test_id:  # Only update if a new memory was actually stored
    update_memory(test_id, "You love lilac and soft pastel colors.")

retrieve_memories("pastel")


