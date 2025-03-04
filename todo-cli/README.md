# To-Do List Manager (CLI)

A simple command-line To-Do List Manager built with Python and Click, managed using **UV** package manager.

## Getting Started

### 1️⃣ Install UV

First, install **UV** (if not already installed):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```sh
uv --version
```

---

### 2️⃣ Create and Initialize the Project

```sh
uv init todo-cli
cd todo-cli
```

---

### 3️⃣ Install Click (Dependency)

```sh
uv add click
```

---

### 4️⃣ Activate UV Virtual Environment (Windows)

```sh
.venv\Scripts\activate
```

For Linux/macOS:

```sh
source .venv/bin/activate
```

---

### 5️⃣ Run To-Do List Commands

#### ➕ Add a New Task
```sh
uv run python todo.py add "Buy grocery for sehri and iftari"
```

#### 📜 List All Tasks
```sh
uv run python todo.py list
```

#### ✅ Mark a Task as Completed
```sh
uv run python todo.py complete 1
```

#### ❌ Remove a Task
```sh
uv run python todo.py remove 1
```

🎉 **That's it! Your To-Do CLI is ready to use.** 🚀
