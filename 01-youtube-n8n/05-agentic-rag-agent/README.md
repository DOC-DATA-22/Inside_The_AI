# Agentic RAG Agent — Google Drive + MongoDB Atlas + OpenAI

**The one-sentence takeaway:** Drop a file in a Google Drive folder, and an agent can answer
questions about it — and decide *how* to answer: search, read, or calculate.

**Needs:** a Google Drive OAuth2 credential · a MongoDB Atlas cluster (free tier works) ·
an OpenAI API key

## What it does

An **agentic RAG** (retrieval-augmented generation) system built entirely in n8n:

1. **Ingestion (automatic)** — two Google Drive triggers watch one folder for new and updated
   files. Each file is downloaded, routed by type (PDF, CSV, XLSX, TXT, Google Docs, Google
   Sheets), split into chunks, embedded with OpenAI, and stored in **MongoDB Atlas** as a vector
   store. Tabular files also get their rows stored so the agent can run calculations on them.
   Re-uploading a file wipes its old chunks and rows first, so the knowledge base never drifts.
2. **The agent (chat)** — one AI Agent node (OpenAI `gpt-4o-mini`) with four tools, and it
   decides at runtime which to call:

   | Tool | What it does |
   |------|-------------|
   | `searchDocuments` | vector search (RAG) over the chunks in `local_docs` |
   | `listDocuments` | lists every file in the knowledge base (plus column schema for tabular files) |
   | `getFileContents` | pulls the full text of one file when a snippet isn't enough |
   | `queryDocumentRows` | runs a MongoDB aggregation over the rows of a CSV/XLSX — sums, averages, counts |

   Chat memory lives in MongoDB too (`local_chat_history`), so the conversation persists.

That's the difference between a chatbot and an agent: a plain RAG bot always does one vector
search. This one chooses — search, list, read, or calculate — based on the question.

## Files here

| File | What it is |
|------|-----------|
| `agentic-rag-agent.json` | The core workflow — ingestion pipeline + agent, no annotations. Fastest to import if you already know your way around n8n. |
| `agentic-rag-agent-google-drive-mongodb-atlas-openai.json` | The **Google Drive + MongoDB Atlas + OpenAI** version — the same build with sticky-note documentation on the canvas explaining each section, plus dedicated Extract-from-File nodes per file type. Start here if you're following the video. |

Both export the same architecture; import whichever you prefer (not both, unless you want two
copies polling the same folder).

## Setup — how to run it

1. **Import the workflow.** In n8n, go to the **Workflows list** → **Import from File** and pick
   one of the JSON files above. (Import from the list, *not* by pasting onto an open canvas.)
2. **Create the three credentials** in n8n (**Credentials** → **Add credential**):
   - **Google Drive OAuth2 API** — connect the Google account that owns the folder you want to
     watch.
   - **MongoDB** — the connection string for your Atlas cluster (**Atlas** → **Connect** →
     **Drivers**), with the database name set to the one you'll use (the workflow assumes
     `rlhf_bot`; change it in the MongoDB nodes if you use a different name).
   - **OpenAI API** — an API key from platform.openai.com.
3. **Attach the credentials to the nodes.** The imported workflow references credentials by
   name (`Google Drive account 3`, `MongoDB account 2`, `OpenAi account 6`) that won't exist in
   your n8n. Open each node that shows a credential warning and select your own:
   - Google Drive → the **File Created** and **File Updated** triggers and the **Download File**
     node
   - MongoDB → every MongoDB node, **MongoDB Atlas Vector Store Insert**, **Search Documents**,
     and **MongoDB Chat Memory**
   - OpenAI → **OpenAI Chat Model** and both **Embeddings OpenAI** nodes
4. **Replace the folder placeholder.** The **File Created** and **File Updated** triggers both
   have the folder set to `YOUR_GOOGLE_DRIVE_FOLDER_ID`. Open each trigger, switch the folder
   field to **By ID** (or pick from the list), and enter your own Google Drive folder ID — the
   long string at the end of the folder's URL: `https://drive.google.com/drive/folders/<THIS_PART>`.
5. **Create the vector search index in Atlas (one time).** In Atlas, create the `local_docs`
   collection by hand, then under **Atlas Search** → **Create Search Index** → **JSON Editor**,
   create a **Vector Search** index named `local_docs_index` on `local_docs`:
   ```json
   {
     "fields": [
       { "type": "vector", "path": "embedding", "numDimensions": 1536, "similarity": "cosine" },
       { "type": "filter", "path": "file_id" }
     ]
   }
   ```
   The other collections (`doc_metadata`, `doc_rows`, `local_chat_history`) are created
   automatically on first insert.
6. **Activate the workflow** (toggle in the top right). Drop a PDF, CSV, or Google Doc into the
   watched folder and wait for the trigger to poll (once a minute). Check **Executions** to
   confirm the ingestion run succeeded.
7. **Talk to it.** Open the chat panel at the bottom of the canvas and try:
   - "What documents do you have?"
   - "Summarize the key points of [document name]"
   - "What's the total of the Amount column in [spreadsheet name]?"

## Keys & safety

No API keys, secrets, connection strings, or personal folder IDs are included in these JSON
files. The credential entries inside them are only *names* — n8n stores the actual secrets
encrypted in your own instance, never in the export. You must supply your own Google Drive
account, MongoDB Atlas connection, OpenAI key, and Drive folder ID.

- The agent only **reads** from Drive and **writes** to your own MongoDB database.
- OpenAI embeddings and chat calls cost money — start with a small folder.
- The free Atlas tier allows a limited number of search indexes; this build uses one.

**Stuck?** [Troubleshooting](../../docs/troubleshooting.md)
