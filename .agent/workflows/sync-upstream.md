---
description: how to sync the fork with the upstream repository
---
// turbo-all
1. **Fetch**: Get the latest changes from the upstream repository:
   ```bash
   git fetch upstream
   ```
2. **Merge**: Merge the upstream master branch into your local master:
   ```bash
   git checkout master
   git merge upstream/master
   ```
3. **Resolve**: If there are conflicts, resolve them carefully, ensuring that project preservation rules are followed.
4. **Push**: Update your remote fork:
   ```bash
   git push origin master
   ```
