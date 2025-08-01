---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

## 🐛 Bug Description

A clear and concise description of what the bug is.

## 🔄 Steps to Reproduce

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior

A clear and concise description of what you expected to happen.

## ❌ Actual Behavior

A clear and concise description of what actually happened.

## 📸 Screenshots

If applicable, add screenshots to help explain your problem.

## 🖥️ Environment

**Desktop (please complete the following information):**
 - OS: [e.g. Windows 10, macOS, Ubuntu]
 - Browser: [e.g. Chrome, Firefox, Safari]
 - Version: [e.g. 22]

**Mobile (please complete the following information):**
 - Device: [e.g. iPhone 6, Samsung Galaxy]
 - OS: [e.g. iOS 8.1, Android 4.4]
 - Browser: [e.g. stock browser, safari]
 - Version: [e.g. 22]

## 📋 Additional Context

Add any other context about the problem here.

## 🔍 Debug Information

### Browser Console Errors
```
Paste any console errors here
```

### Network Tab
- Any failed requests?
- Response codes?

### Application Logs
```
Paste any relevant logs here
```

## 🧪 Reproduction Steps

### Minimal Test Case
```python
# If applicable, provide a minimal test case
import requests

response = requests.post('http://localhost:5001/analyze', json={
    'name': 'Test User',
    'education': 'Bachelor',
    'experience': 'junior',
    'skills': ['python'],
    'interests': ['ai']
})
print(response.status_code)
print(response.json())
```

## 📊 Impact Assessment

- [ ] **Critical**: Application crashes or data loss
- [ ] **High**: Major functionality broken
- [ ] **Medium**: Minor functionality affected
- [ ] **Low**: Cosmetic issue or minor inconvenience

## 🔧 Possible Solutions

If you have suggestions on a fix for the bug, please describe it here.

## 📝 Additional Notes

Any other information that might be helpful.

---

**Checklist:**
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have provided all requested information
- [ ] I have tested on multiple browsers/devices
- [ ] I have included relevant error messages
- [ ] I have provided steps to reproduce the issue 