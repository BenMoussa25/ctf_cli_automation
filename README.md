# CTF Challenge Utilities

This repository contains two helpful Bash scripts to prepare, fix, and push CTF challenges to a new platform or GitHub repository.

---

## Scripts

### 1. `fix_challenges`

**Purpose:**  
Standardizes folder names and fixes common typos across the project directory. Also updates challenge configuration files.

**What it does:**
- Renames incorrectly named folders:
  - `Challange`, `challange`, `Challenge` ➔ `challenge`
  - `Solver` ➔ `solver`
  - `Handout` ➔ `handout`
- Replaces the word `Handout` with `handout` inside all `challenge.yml` files.

**Usage:**

```bash
chmod +x fix_challenges
./fix_challenges
```

No parameters are needed — it will work recursively in the current directory.

---

### 2. `push_ctf_challenges`

**Purpose:**  
Initializes a new CTF project and installs all CTF challenges from a given tasks directory.

**What it does:**
- Runs `ctf init` to initialize the platform.
- Installs all challenge folders from the specified tasks directory.

**Usage:**

```bash
chmod +x push_ctf_challenges
./push_ctf_challenges -d <tasks_directory>
```

**Options:**
- `-d <tasks_directory>`:  
  Path to the directory containing your CTF challenge folders.

**Example:**

```bash
./push_ctf_challenges -d ./tasks
```

This will automatically initialize the CTF platform and install all challenges found under `./tasks/`.

---

## Example Workflow

```bash
# 1. Fix folder names and content
./fix_challenges

# 2. Initialize CTF project and install challenges
./push_ctf_challenges -d ./tasks

# 3. (Optional) Reset Git history for a fresh repo
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-new-repo.git
git push -u origin main
```

---

## Installation Requirements

You need `ctfcli` installed. Here's how you can set it up:

```bash
# Install pipx if you don't have it
sudo apt update
sudo apt install pipx

# Ensure pipx is available immediately
pipx ensurepath

# Install ctfcli using pipx
pipx install ctfcli
```

> `ctfcli` is a command-line tool for managing CTF challenges easily, used in the `push_ctf_challenges` script.

---

## Requirements Summary

- `bash`
- `git`
- `pipx`
- `ctfcli`

---

## License

This project is open source and available under the [MIT License](LICENSE).

