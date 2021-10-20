# Supply and Demand

## Solve Path

1. Find suspicious package in `package-lock.json`
2. Deobfuscate package, find embedded `.pyc` file
3. Decompile `.pyc` file, then deobfuscate, and find reference to GitHub repository/fork
4. Use shell injection through a GitHub issue to recover flag in secrets through GitHub Actions
