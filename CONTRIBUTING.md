# Contributing to Annuity Comparison Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the Annuity Comparison Tool.

---

## 🎯 Code of Conduct

- Be respectful and professional
- Focus on the code, not the person
- Help others learn and grow
- Report issues constructively

---

## 🐛 Reporting Bugs

Found a bug? Please open an issue with:

1. **Clear title** — describe the bug concisely
2. **Steps to reproduce** — how to trigger the bug
3. **Expected behavior** — what should happen
4. **Actual behavior** — what actually happens
5. **System info** — Python version, OS, etc.
6. **Screenshots** — if applicable

### Example Issue

```
Title: CSV export fails with special characters in product names

Steps to reproduce:
1. Create a product with "®" symbol: "Fixed Annuity – Carrier A®"
2. Run: python annuity_comparator.py --export results.csv
3. Error occurs

Expected: CSV file should be created with escaped characters
Actual: UnicodeEncodeError thrown

System: Python 3.9, Windows 10
```

---

## ✨ Suggesting Features

Have an idea? Open an issue with:

1. **Problem statement** — what issue does it solve?
2. **Proposed solution** — how would it work?
3. **Alternative approaches** — other ways to solve it
4. **Use case examples** — real scenarios

### Example Feature Request

```
Title: Add option to compare annuities by liquidity score

Problem: Advisors need to quickly assess liquidity needs for clients
Solution: Add a --liquidity flag that ranks products by ease of withdrawal
Use case: Senior clients needing emergency access to funds
```

---

## 💻 Contributing Code

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Comparing-Annuities.git
   cd Comparing-Annuities
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Development Guidelines

#### Code Style
- Follow **PEP 8** standards
- Use **meaningful variable names**
- Write **clear comments** for complex logic
- Aim for **readability over cleverness**

#### Testing
- Test your changes locally before submitting
- Verify with multiple Python versions if possible
- Test with various config files and scenarios
- Check CSV export works correctly

#### Commits
- Write **clear, concise commit messages**
- Use present tense: "Add feature" not "Added feature"
- Reference issues when relevant: "Fix #42"
- Keep commits **focused and logical**

### Pull Request Process

1. **Update your branch** with latest main:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub with:
   - **Clear title** describing the changes
   - **Description** of what was changed and why
   - **Related issue numbers** (e.g., "Fixes #42")
   - **Testing notes** — how you tested the changes

4. **Respond to feedback** promptly and professionally

### Example PR Description

```markdown
## Description
Adds support for variable interest rates in MYGA projections, allowing year-to-year interest rate changes.

## Type of Change
- [x] Bug fix
- [ ] New feature
- [x] Enhancement
- [ ] Breaking change

## Related Issues
Fixes #34

## Testing
- Tested with example_scenario.json with variable rates
- Verified CSV export includes all rate columns
- Tested with constant rates to ensure backward compatibility
- Output matches manual calculations

## Checklist
- [x] Code follows PEP 8 style guide
- [x] Tested locally with Python 3.8+
- [x] Updated relevant documentation
- [x] Commit messages are clear
```

---

## 📝 Documentation

Help improve documentation by:

- **Clarifying existing docs** — make them easier to understand
- **Adding examples** — show real-world use cases
- **Creating tutorials** — step-by-step guides for common tasks
- **Fixing typos** — catch and correct errors

When contributing documentation:
- Use **clear, simple language**
- Include **practical examples**
- Link to **related sections**
- Test **code examples** to ensure they work

---

## 🆕 Adding New Annuity Types

Want to add support for a new annuity type? Here's the process:

1. **Discuss first** — open an issue to get feedback
2. **Research requirements** — understand the product's unique features
3. **Implement modeling** — add calculation logic
4. **Add config support** — allow it in JSON configs
5. **Write tests** — verify calculations are correct
6. **Update docs** — document new annuity type in README
7. **Submit PR** — with clear explanation of changes

---

## 🎓 Areas for Contribution

### High Priority
- 🧪 Unit tests and test coverage
- 📖 Documentation and examples
- 🐛 Bug fixes
- ♿ Accessibility improvements

### Medium Priority
- ✨ New features (after discussion)
- 🚀 Performance optimizations
- 🎨 UI/UX improvements

### Low Priority
- 💄 Code style refinements
- 📝 Comment improvements
- 🔧 Tool configuration

---

## 📚 Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Git Commit Best Practices](https://cbea.ms/git-commit/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Financial Annuity Standards](https://www.soa.org/) — SOA resources

---

## ❓ Questions?

- **Before you start** — check existing issues and PRs
- **Need clarification?** — ask in an issue
- **General questions?** — start a discussion

---

## 🙏 Thank You

Your contributions make this tool better for financial professionals everywhere. Thank you for helping!

---

**Happy contributing!** 🚀