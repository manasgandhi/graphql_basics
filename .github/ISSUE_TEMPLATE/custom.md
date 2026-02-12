---
name: Custom issue template
about: Describe this issue template's purpose here.
title: ''
labels: ''
assignees: ''

---

## Description
<!-- What does this PR do? Link to relevant ticket(s). -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Migration / schema change
- [ ] Other: ___

## Checklist

### General
- [ ] Self-reviewed my own code
- [ ] No debugging artifacts (print statements, commented-out code) left in
- [ ] Functions and classes have type hints
- [ ] Public functions and classes have docstrings

### Django / DRF
- [ ] New queries use `select_related` / `prefetch_related` where appropriate
- [ ] Raw SQL lives in dedicated query files, not inline in views or serializers
- [ ] DRF serializers validate input explicitly — no implicit trust of request data
- [ ] API changes are backward-compatible or versioned appropriately
- [ ] New or changed models include a migration and the migration has been tested

### Security
- [ ] No secrets or credentials hardcoded
- [ ] Permission checks are in place for new endpoints

### Testing
- [ ] Unit tests added or updated for new logic
- [ ] API endpoint tests cover success and error cases
