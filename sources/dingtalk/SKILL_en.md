---
title: dingtalk
excerpt: A skill for calling DingTalk Open Platform APIs, supporting user and department management, message sending, and approval management.
date: 2026-04-09
---

# DingTalk API Skill

This skill integrates with the DingTalk Open Platform to perform organization directory queries and approvals operations. It covers:
- User search and details, department search and details
- Listing sub-departments and department users
- Sending messages via bots to users or groups
- Listing bots in a group
- HR utilities such as resigned records and inactive users
- Approvals: list instances, fetch instance details, create/terminate instances, execute/transfer tasks, add comments, query todo counts

## Prerequisites

- Set environment variables `DINGTALK_APP_KEY` and `DINGTALK_APP_SECRET`
- The DingTalk app must be created with required API permissions

```bash
export DINGTALK_APP_KEY="<your-app-key>"
export DINGTALK_APP_SECRET="<your-app-secret>"
```

## Typical Commands

- Search users by name:
```bash
npx ts-node scripts/search-user.ts "<keyword>"
```

- Search departments by name:
```bash
npx ts-node scripts/search-department.ts "<keyword>" [--debug]
```

- Get department details / list sub-departments / list users:
```bash
npx ts-node scripts/get-department.ts <deptId>
npx ts-node scripts/list-sub-departments.ts <deptId>
npx ts-node scripts/list-department-users.ts <deptId>
```

- Send messages (user or group):
```bash
npx ts-node scripts/send-user-message.ts "<userId>" "<robotCode>" "<text>"
npx ts-node scripts/send-group-message.ts "<openConversationId>" "<robotCode>" "<text>"
```

- Approvals (examples):
```bash
npx ts-node scripts/list-approval-instance-ids.ts <processCode> --startTime <ts> --endTime <ts>
npx ts-node scripts/get-approval-instance.ts <instanceId>
npx ts-node scripts/create-approval-instance.ts <processCode> <originatorUserId> <deptId> '<formValuesJson>'
npx ts-node scripts/terminate-approval-instance.ts <instanceId> <operatorUserId> [--remark "..."]
npx ts-node scripts/execute-approval-task.ts <instanceId> <userId> <agree|refuse> [--remark "..."]
```

## Error Handling

All scripts return a unified structure on error:
```json
{
  "success": false,
  "error": { "code": "ERROR_CODE", "message": "Description" }
}
```

Common error codes:
- MISSING_CREDENTIALS
- INVALID_ARGUMENTS
- AUTH_FAILED
- UNKNOWN_ERROR
