# Test Strategy – QA Automation Framework

## 1. Testing Approach

A layered testing strategy is implemented:

### UI Testing
- Page Object Model (POM)
- Smoke & Regression tagging
- Parallel execution (pytest-xdist)
- Screenshot capture on failure

### API Testing
- API client abstraction layer
- Status code validation
- JSON schema validation
- Response time assertions
- Negative test cases

### Performance Testing
- Load simulation using Locust
- 50+ concurrent user testing
- Percentile-based latency analysis

---

## 2. Automation Strategy
- Tests categorized using pytest markers
- Executed in CI pipeline on pull requests
- Allure reports generated and stored as artifacts
- Dockerized execution for environment consistency

---

## 3. CI/CD Integration
- Path-based GitHub Actions workflow
- Parallel execution in CI
- Non-blocking API execution strategy for external endpoints

---

## 4. Test Data Strategy
- Static test credentials for demo environment
- Environment variables managed via `.env`
- Configurable base URLs