# Test Plan – E-Commerce Automation Framework

## 1. Objective
To validate the functionality, reliability, and performance of the demo e-commerce platform through automated UI, API, and performance testing.

## 2. Scope
### In Scope:
- User login (valid & invalid scenarios)
- Product listing and cart functionality
- API validation (GET endpoints, schema validation)
- Performance testing under concurrent load

### Out of Scope:
- Payment gateway integration
- Database validation
- Third-party integrations

## 3. Test Types
- Smoke Testing
- Regression Testing
- API Functional Testing
- Negative Testing
- Load Testing

## 4. Tools & Framework
- Playwright (UI)
- Pytest (Test Runner)
- Requests (API)
- Locust (Performance)
- Allure (Reporting)
- GitHub Actions (CI/CD)
- Docker (Containerization)

## 5. Entry Criteria
- Test environment accessible
- Required credentials available
- CI pipeline operational

## 6. Exit Criteria
- All smoke tests pass
- No critical defects open
- Performance within acceptable thresholds

## 7. Risks
- External API instability
- Public endpoint rate limiting
- Cloud runner IP restrictions