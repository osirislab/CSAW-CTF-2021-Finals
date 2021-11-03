# Supply and Demand

## Solve Path

1. Find suspicious package in `package-lock.json`
2. Go to GitHub repository listed in manifest
3. Traverse all the branches, find embedded `key.pyc` file
4. Decompile `.pyc` file, then deobfuscate for a AES key
5. Find additional reference in `requirements.txt` to another Git repo with encrypted flag
6. Solve!

## Stages

1. `package-lock.json`

Contains ~2k random packages pulled from the NPM registry, plus the one we own, `touchbase`.
Player will have to figure out that's the one and introspect the manifest to find the GitHub repo.

2. `key.pyc`

This is found in commit XX on branch XX in https://github.com/JermaineCole/touchbase

3. `git+https://git.sr.ht/~ex0dus/supply`

Final repository with encrypted flag


