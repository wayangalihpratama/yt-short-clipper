---
description: how to commit and push changes to GitHub
---
// turbo-all
1. **Review**: Check the changes you've made using `git status` and `git diff`.
2. **Stage & Group**: Add files related to a **single topic or task**. If you have changes for different features or bugs, commit them separately.
   ```bash
   # Topic 1: Feature addition
   git add path/to/feature_a.py
   git commit -m "[#issue_number] feat: implement feature A"

   # Topic 2: Bug fix
   git add path/to/bug_fix_b.py
   git commit -m "[#issue_number] fix: resolve bug B"
   ```
3. **Commit Message Best Practices**:
   - **Prefix**: Start with the issue number or project tag in brackets (e.g., `[#123]`).
   - **Clarity**: Use the imperative mood after the prefix ("feat: add feature" not "feat: added feature").
   - **Conciseness**: Keep the subject line under 50 characters.
   - **Context**: Ensure the prefix reflects the current task or ticket.
   - **Separation**: Separate subject from body with a blank line if more explanation is needed.
4. **Push**: Push your branch to the remote fork:
   ```bash
   git push origin <your-branch-name>
   ```
5. **PR**: After pushing, create a Pull Request on GitHub and provide the link.
