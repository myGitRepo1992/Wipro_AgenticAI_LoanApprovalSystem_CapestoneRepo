# Development Rules & Guidelines

## Core Principles

### 1. **Error-First, Scoped Fixes**
- ✅ Only address the specific error/issue mentioned in the chat
- ✅ Make minimal changes to fix the problem
- ❌ Do NOT add features, refactor, or "improve" code beyond the scope
- ❌ Do NOT reorganize imports, rename variables, or touch unrelated code

### 2. **Preserve Existing Functionality**
- ✅ Run tests after changes to verify nothing broke
- ✅ Keep the same function signatures and interfaces
- ✅ Maintain compatibility with other modules that depend on the code
- ❌ Do NOT restructure classes, move methods between files, or split functions
- ❌ Do NOT change API contracts or return types

### 3. **Isolation & Independence**
- ✅ Treat each bug fix as independent (no cross-file refactors)
- ✅ Check if similar patterns exist elsewhere but only fix what's broken
- ✅ Document the specific change with line numbers
- ❌ Do NOT apply "fixes" to working code just because similar patterns exist
- ❌ Do NOT make speculative changes "in case they might help"

### 4. **Change Transparency**
- ✅ Clearly state what was changed and why
- ✅ Show before/after code when it helps clarity
- ✅ Explain the root cause of the error
- ✅ Mention any files modified and their locations
- ❌ Do NOT make silent, hidden changes
- ❌ Do NOT assume the error is elsewhere without evidence

### 5. **Code Stability First**
- ✅ Verify the fix actually solves the stated problem
- ✅ Check that error messages are gone or behavior is corrected
- ✅ Test edge cases related to the specific fix
- ❌ Do NOT trade one bug for another
- ❌ Do NOT introduce new complexity to "future-proof" code

## When Asking Questions

If the error description is unclear, ask:
1. What is the exact error message?
2. Which file/function is affected?
3. What is the expected behavior?
4. What is the actual behavior?

**Do NOT guess or explore the codebase** to "figure out" the issue—ask for clarification first.

## Example Workflow

**❌ BAD:**
```
User: "Fix the login bug"
→ Search entire codebase for auth issues
→ Refactor auth module
→ Add new logging
→ Restructure state management
```

**✅ GOOD:**
```
User: "Fix the login bug in login.py line 42"
→ Read only that function
→ Identify the specific issue
→ Apply minimal fix
→ Test that login works
→ Report: "Fixed one-line typo at login.py:42"
```

## Rules Checklist Before Every Change

- [ ] Have I addressed ONLY the stated error?
- [ ] Is my change the smallest possible fix?
- [ ] Will this break any existing tests?
- [ ] Did I verify other code still works?
- [ ] Is the code clearer, not more complex?
- [ ] Can I revert this change in 5 seconds if needed?

## Special Cases

### Adding New Code
- Only if explicitly asked or if the error requires it
- Even then, keep it minimal and focused
- Make sure it doesn't duplicate existing functionality

### Deleting Code
- Only remove code you're certain is dead/unused
- Check git history or grep for references first
- Ask if unsure—better to leave it than break something

### Modifying Tests
- Only if the test itself is broken
- Don't "fix" tests by changing their assertions
- If a test reveals a bug, fix the code, not the test

### Dependencies & Versions
- Don't upgrade/downgrade packages without explicit request
- Don't change configuration beyond what's needed for the fix
- Don't modify environment variables or build scripts

---

**As an expert developer, please:**
- Focus on precision over perfection
- Favor the surgical fix over the comprehensive overhaul
- Ask before you change what you're unsure about
- Remember: the best code change is the one that fixes exactly one thing