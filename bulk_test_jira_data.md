### **Jira Issue 1**

* **Priority:** Major
* **Summary:** Enhance monitoring for database connection pool exhaustion to provide early warnings.
* **Description:**
    * **Issue:** During service disruptions, there was no visibility into the health of the database connection pools, making it difficult to distinguish between credential failures and connection exhaustion.
    * **Corrective Action:** Implement Prometheus metrics to track active versus idle database connections. A new alert should be configured to trigger when active connections exceed 90% of the available pool for a sustained period.
    * **Result:** This will provide engineers with immediate insight into database connection health, enabling faster diagnosis and proactive response before the service becomes unavailable.
* **Assignee:** Team1

***

### **Jira Issue 2**

* **Priority:** Critical
* **Summary:** Implement automated secret-scrubbing in CI/CD pipelines to prevent credential leaks in logs.
* **Description:**
    * **Issue:** An audit revealed that deployment scripts occasionally log configuration file snippets to CI/CD job logs, creating a high risk of accidental secret exposure.
    * **Corrective Action:** Integrate a secret-scrubbing tool into the CI/CD runner environment. This tool will automatically scan all log outputs for patterns matching known secret formats and mask them before they are saved.
    * **Result:** This action will significantly lower the risk of sensitive credentials being exposed in build and deployment logs.
* **Assignee:** Team2

***

### **Jira Issue 3**

* **Priority:** Major
* **Summary:** Establish a quarterly disaster recovery drill to practice and document the regional failover process.
* **Description:**
    * **Issue:** The regional failover process during the incident was slow because the procedure was not recently practiced or well-documented.
    * **Corrective Action:** Schedule and conduct a full disaster recovery (DR) drill each quarter. This exercise will include failing over production traffic, verifying full system functionality in the secondary region, and then failing back. The entire procedure must be updated in the official runbook.
    * **Result:** Regular DR drills will reduce the Mean Time to Recovery (MTTR) during a real outage and ensure the failover process remains effective.
* **Assignee:** Team1

***

### **Jira Issue 4**

* **Priority:** Normal
* **Summary:** Audit and update stale third-party application dependencies to mitigate known vulnerabilities.
* **Description:**
    * **Issue:** An internal audit discovered that several application components rely on outdated third-party libraries, some of which have known security vulnerabilities.
    * **Corrective Action:** Integrate a dependency scanning tool like Snyk or Dependabot into the CI pipeline. A policy should be created to automatically generate tickets for any high or critical severity vulnerabilities found.
    * **Result:** This will improve the application's overall security posture by ensuring components are not exposed to previously discovered vulnerabilities.
* **Assignee:** Team2

***

### **Jira Issue 5**

* **Priority:** Normal
* **Summary:** Update on-call runbooks with specific troubleshooting steps for `HTTP 500` authentication failures.
* **Description:**
    * **Issue:** The on-call engineer had to manually diagnose that a Kinesis key rotation was the cause of `HTTP 500` errors on authentication requests, as this information was not available in any runbook.
    * **Corrective Action:** Update the primary on-call runbook to include a troubleshooting guide for authentication failures. This guide should list potential causes like credential rotation or logging failures, along with commands and dashboard links to investigate each one.
    * **Result:** This will decrease the time it takes for an on-call engineer to diagnose and resolve common critical errors.
* **Assignee:** Team1