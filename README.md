# SnipVault
SnipVault is a simple, secured storage solution for saving and managing snippets in a local database file. Access and manage your snippets easily via a Command Line Interface (CLI).

## Features
* **Secure Storage**: Store your snippets securely in a local database.
* **CLI Access**: Manage your snippets directly from the command line.

## CLI Commands

### 1. `snippet save <name> <value>`
Saves a new snippet with a specified name and value.

Example:

```bash
snippet save mySnippet value
```

### 2. `snippet update <name> <value>`
Updates an existing snippet with the specified name.

Example:

```bash
snippet update mySnippet "new Value"
```

### 3. `snippet get <name>`
Retrieves the snippet with the specified name.

Example:

```bash
snippet get mySnippet
```

### 4. `snippet delete <name>`
Deletes the snippet with the specified name.

Example:

```bash
snippet delete mySnippet
```

### 5. `snippet list`
Lists all saved snippets.

Example:

```bash
snippet list
```

### 6. `snippet clear`
Clears all saved snippets.

Example:

```bash
snippet clear
```

## Installation
1) Clone the repository:
```bash
git clone https://github.com/marcelnoehre/snippet-vault.git
```

2) Navigate to the project directory:
```bash
cd snippet-vault
```

3) Run Shell Script
```bash
sh snip_vault.sh
```

## Usage
Once installed, you can start using SnipVault via the command line. For example, to save a snippet:

```bash
snippet save mySnippet "Your Value"
```

If everything works fine, the following output should be displayed:

```
🗂️ SnipVault: Stored Snippet 'mySnippet'
```

## Contributing
Feel free to fork, use, and modify this project as you like! It's open-source and licensed under the MIT License.
