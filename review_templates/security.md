# Security Code Review Template

## Input Validation
- [ ] All user inputs are properly validated
- [ ] Input validation happens on the server side
- [ ] Validation errors are properly handled and reported
- [ ] Input size limits are enforced

## Authentication & Authorization
- [ ] Authentication mechanisms follow best practices
- [ ] Authorization checks are in place for all secure operations
- [ ] Session management is secure
- [ ] Password policies are enforced

## Data Protection
- [ ] Sensitive data is encrypted at rest
- [ ] Secure transmission protocols are used
- [ ] No sensitive data in logs or error messages
- [ ] Proper key management practices

## Injection Prevention
- [ ] SQL injection protections are in place
- [ ] Cross-site scripting (XSS) protections are implemented
- [ ] Command injection risks are mitigated
- [ ] CSRF protections are implemented

## Error Handling & Logging
- [ ] Errors don't reveal sensitive information
- [ ] Security events are properly logged
- [ ] Log data is protected from tampering
- [ ] Adequate error handling is in place

## Dependency Security
- [ ] Third-party dependencies are up-to-date
- [ ] No known vulnerabilities in dependencies
- [ ] Dependency sources are trusted
- [ ] Proper version pinning is used

## Code Secrets
- [ ] No hardcoded secrets in the code
- [ ] Secrets are stored in appropriate secret management systems
- [ ] API keys and credentials are properly secured
- [ ] No sensitive data in repositories or comments

## Additional Security Concerns
- Add any specific security feedback or concerns here