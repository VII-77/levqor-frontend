interface RejectLog {
  userId: string;
  timestamp: string;
  matchedKeywords: string[];
  workflowTitle: string;
  description?: string;
}

export function logHighRiskReject(log: RejectLog) {
  const redactedLog = {
    ...log,
    timestamp: new Date(log.timestamp).toISOString(),
  };

  console.log(
    `[HIGH-RISK REJECT] User: ${redactedLog.userId} | ` +
    `Time: ${redactedLog.timestamp} | ` +
    `Keywords: ${redactedLog.matchedKeywords.join(', ')} | ` +
    `Title: "${redactedLog.workflowTitle}"`
  );

  console.log(
    `[HIGH-RISK REJECT] Action: workflow_rejected | ` +
    `User: ${redactedLog.userId} | ` +
    `Keywords: [${redactedLog.matchedKeywords.join(', ')}] | ` +
    `Timestamp: ${redactedLog.timestamp}`
  );
}
