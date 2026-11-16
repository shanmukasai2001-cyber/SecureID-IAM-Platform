
# IAM System Architecture

## Overview

The IAM system manages employee identities,
access permissions, and identity lifecycle events.

## Main Components

1. Identity Repository
   - Stores employee identity information.

2. Provisioning Engine
   - Creates and updates user accounts.

3. RBAC Engine
   - Determines access based on assigned roles.

4. Deprovisioning Engine
   - Disables accounts and removes permissions.

5. Access Review Engine
   - Reviews user permissions and identifies
     excessive access.

6. Audit Logging
   - Records identity and access activities.

## Identity Lifecycle

Employee Joining
       |
       v
User Provisioning
       |
       v
Role Assignment
       |
       v
Access Management
       |
       v
Periodic Access Review
       |
       v
Employee Termination
       |
       v
Account Deactivation

## Security Principles

- Least Privilege
- Separation of Duties
- Role-Based Access Control
- Auditability
- Identity Governance
